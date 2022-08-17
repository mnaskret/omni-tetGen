"""
This is the implementation of the OGN node defined in OgnNewNode.ogn
"""

# Array or tuple values are accessed as numpy arrays so you probably need this import
import math

import numpy as np
import warp as wp

import omni.timeline

from pxr import Usd, UsdGeom, Gf, Sdf

@wp.kernel
def boundsKer(predictedPositions: wp.array(dtype=wp.vec3),
              groundLevel: float):
    
    tid = wp.tid()

    x = predictedPositions[tid]

    if(x[1] < groundLevel):
        predictedPositions[tid] = wp.vec3(x[0], groundLevel, x[2])

@wp.kernel
def PBDStepKer(positions: wp.array(dtype=wp.vec3),
               predictedPositions: wp.array(dtype=wp.vec3),
               velocities: wp.array(dtype=wp.vec3),
               dT: float):
    
    tid = wp.tid()

    x = positions[tid]
    xPred = predictedPositions[tid]

    v = (xPred - x)*(1.0/dT)
    x = xPred

    positions[tid] = x
    velocities[tid] = v

@wp.kernel
def gravityKer(positions: wp.array(dtype=wp.vec3),
               predictedPositions: wp.array(dtype=wp.vec3),
               velocities: wp.array(dtype=wp.vec3),
               gravityConstant: wp.vec3,
               velocityDampening: float,
               dt: float):
    
    tid = wp.tid()

    x = positions[tid]
    v = velocities[tid]

    velocityDampening = 1.0 - velocityDampening

    v = v + gravityConstant*dt*velocityDampening

    xPred = x + v*dt

    predictedPositions[tid] = xPred

@wp.kernel
def distanceConstraints(predictedPositions: wp.array(dtype=wp.vec3),
                        dP: wp.array(dtype=wp.vec3),
                        constraintsNumber: wp.array(dtype=int),
                        edgesA: wp.array(dtype=int),
                        edgesB: wp.array(dtype=int),
                        edgesRestLengths: wp.array(dtype=float),
                        inverseMasses: wp.array(dtype=float),
                        kS: float):
    
    tid = wp.tid()

    edgeIndexA = edgesA[tid]
    edgeIndexB = edgesB[tid]

    edgePositionA = predictedPositions[edgeIndexA]
    edgePositionB = predictedPositions[edgeIndexB]
    
    edgeRestLength = edgesRestLengths[tid]

    dir = edgePositionA - edgePositionB
    len = wp.length(dir)

    inverseMass = inverseMasses[edgeIndexA] + inverseMasses[edgeIndexB]

    edgeDP = (len-edgeRestLength) * wp.normalize(dir) * kS / inverseMass
    
    wp.atomic_sub(dP, edgeIndexA, edgeDP)
    wp.atomic_add(dP, edgeIndexB, edgeDP)

    wp.atomic_add(constraintsNumber, edgeIndexA, 1)
    wp.atomic_add(constraintsNumber, edgeIndexB, 1)

@wp.kernel
def volumeConstraints(predictedPositions: wp.array(dtype=wp.vec3),
                      dP: wp.array(dtype=wp.vec3),
                      constraintsNumber: wp.array(dtype=int),
                      tetrahedronsA: wp.array(dtype=int),
                      tetrahedronsB: wp.array(dtype=int),
                      tetrahedronsC: wp.array(dtype=int),
                      tetrahedronsD: wp.array(dtype=int),
                      tetrahedronsRestVolumes: wp.array(dtype=float),
                      inverseMasses: wp.array(dtype=float),
                      kS: float):
    
    tid = wp.tid()

    tetrahedronIndexA = tetrahedronsA[tid]
    tetrahedronIndexB = tetrahedronsB[tid]
    tetrahedronIndexC = tetrahedronsC[tid]
    tetrahedronIndexD = tetrahedronsD[tid]

    tetrahedronPositionA = predictedPositions[tetrahedronIndexA]
    tetrahedronPositionB = predictedPositions[tetrahedronIndexB]
    tetrahedronPositionC = predictedPositions[tetrahedronIndexC]
    tetrahedronPositionD = predictedPositions[tetrahedronIndexD]
    
    tetrahedronRestVolume = tetrahedronsRestVolumes[tid]

    p1 = tetrahedronPositionB - tetrahedronPositionA
    p2 = tetrahedronPositionC - tetrahedronPositionA
    p3 = tetrahedronPositionD - tetrahedronPositionA

    q2 = wp.cross(p3, p1)
    q1 = wp.cross(p2, p3)
    q3 = wp.cross(p1, p2)
    q0 = - q1 - q2 - q3

    mA = inverseMasses[tetrahedronIndexA]
    mB = inverseMasses[tetrahedronIndexB]
    mC = inverseMasses[tetrahedronIndexC]
    mD = inverseMasses[tetrahedronIndexD]

    volume = wp.dot(wp.cross(p1, p2), p3) / 6.0

    lambd = mA * wp.dot(q0, q0) + mB * wp.dot(q1, q1) + mC * wp.dot(q2, q2) + mD * wp.dot(q3, q3)

    lambd = kS * (volume - tetrahedronRestVolume) / lambd

    wp.atomic_sub(dP, tetrahedronIndexA, q0 * lambd * mA)
    wp.atomic_sub(dP, tetrahedronIndexB, q1 * lambd * mB)
    wp.atomic_sub(dP, tetrahedronIndexC, q2 * lambd * mC)
    wp.atomic_sub(dP, tetrahedronIndexD, q3 * lambd * mD)

    wp.atomic_add(constraintsNumber, tetrahedronIndexA, 1)
    wp.atomic_add(constraintsNumber, tetrahedronIndexB, 1)
    wp.atomic_add(constraintsNumber, tetrahedronIndexC, 1)
    wp.atomic_add(constraintsNumber, tetrahedronIndexD, 1)

@wp.kernel
def applyConstraints(predictedPositions: wp.array(dtype=wp.vec3),
                     dP: wp.array(dtype=wp.vec3),
                     constraintsNumber: wp.array(dtype=int)):
    
    tid = wp.tid()

    if(constraintsNumber[tid] > 0):
        tmpDP = dP[tid]
        N = float(constraintsNumber[tid])
        DP = wp.vec3(tmpDP[0]/N, tmpDP[1]/N, tmpDP[2]/N)
        predictedPositions[tid] = predictedPositions[tid] + DP

    dP[tid] = wp.vec3(0.0, 0.0, 0.0)
    constraintsNumber[tid] = 0

class PBDBasicGravity:

    @staticmethod
    def compute(db) -> bool:

        timeline =  omni.timeline.get_timeline_interface()
        device = "cuda"

        # # reset on stop
        # if (timeline.is_stopped()):
        #     context.reset()

        # initialization
        if (timeline.is_playing()):

            with wp.ScopedCudaGuard():
            
                gravity = db.inputs.gravity
                velocity_dampening = db.inputs.velocity_dampening
                ground = db.inputs.ground
                kSDistance = db.inputs.ks_distance
                kSVolume = db.inputs.ks_volume

                # convert node inputs to a GPU array
                positions = wp.array(db.inputs.points, dtype=wp.vec3, device=device)
                predictedPositions = wp.zeros_like(positions)
                velocities = wp.array(db.inputs.velocities, dtype=wp.vec3, device=device)
                inverseMasses = wp.array(db.inputs.inverseMasses, dtype=float, device=device)

                dP = wp.zeros_like(positions)
                constraintsNumber = wp.zeros(len(dP), dtype=int, device=device)

                edgesSplit = np.hsplit(db.inputs.edge, 2)
                edgesA = wp.array(edgesSplit[0], dtype=int, device=device)
                edgesB = wp.array(edgesSplit[1], dtype=int, device=device)
                edgesRestLengths = wp.array(db.inputs.edgesRestLengths, dtype=float, device=device)

                tetrahedronsSplit = np.hsplit(db.inputs.elem, 4)
                tetrahedronsA = wp.array(tetrahedronsSplit[0], dtype=int, device=device)
                tetrahedronsB = wp.array(tetrahedronsSplit[1], dtype=int, device=device)
                tetrahedronsC = wp.array(tetrahedronsSplit[2], dtype=int, device=device)
                tetrahedronsD = wp.array(tetrahedronsSplit[3], dtype=int, device=device)
                tetrahedronsRestVolumes = wp.array(db.inputs.tetrahedronsRestVolumes, dtype=float, device=device)

                # step simulation
                with wp.ScopedTimer("Simulate", active=False):
                    # simulate
                    sim_substeps = db.inputs.num_substeps
                    sim_constraints = db.inputs.sim_constraints
                    sim_dt = (1.0/30)/sim_substeps

                    for i in range(sim_substeps):

                        # simulate
                        wp.launch(kernel=gravityKer,
                                  dim=len(positions),
                                  inputs=[positions,
                                          predictedPositions,
                                          velocities,
                                          gravity,
                                          velocity_dampening,
                                          sim_dt],
                                  device=device)

                        for j in range(sim_constraints):

                            wp.launch(
                                kernel=volumeConstraints,
                                dim=len(tetrahedronsA),
                                inputs=[predictedPositions,
                                        dP,
                                        constraintsNumber,
                                        tetrahedronsA,
                                        tetrahedronsB,
                                        tetrahedronsC,
                                        tetrahedronsD,
                                        tetrahedronsRestVolumes,
                                        inverseMasses,
                                        kSVolume],
                                device=device)

                            wp.launch(
                                kernel=distanceConstraints,
                                dim=len(edgesA),
                                inputs=[predictedPositions,
                                        dP,
                                        constraintsNumber,
                                        edgesA,
                                        edgesB,
                                        edgesRestLengths,
                                        inverseMasses,
                                        kSDistance],
                                device=device)

                            wp.launch(
                                kernel=applyConstraints,
                                dim=len(positions),
                                inputs=[predictedPositions,
                                        dP,
                                        constraintsNumber],
                                device=device)

                        wp.launch(kernel=boundsKer,
                                  dim=len(predictedPositions),
                                  inputs=[predictedPositions,
                                          ground],
                                  device=device)

                        wp.launch(kernel=PBDStepKer,
                                  dim=len(positions),
                                  inputs=[positions,
                                          predictedPositions,
                                          velocities,
                                          sim_dt],
                                  device=device)

                # write node outputs
                db.outputs.points = positions.numpy()
                db.outputs.velocities = velocities.numpy()

        else:
            
            with wp.ScopedTimer("Write", active=False):
                
                # timeline not playing and sim. not yet initialized, just pass through outputs
                db.outputs.points = db.inputs.points
                db.outputs.velocities = db.inputs.velocities