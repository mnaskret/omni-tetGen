import omni.ext
import omni.ui as ui
import omni.kit.commands as commands
import pxr
from pxr import Sdf
import numpy as np
import tetgenExt
import os
import math
import warp as wp


class MyExtension(omni.ext.IExt):

    fileUrl = ''

    def drop_accept(url, ext):
        # Accept drops of specific extension only
        print("File dropped")
        return url.endswith(ext)

    def drop(widget, event):
        widget.text = event.mime_data
        MyExtension.fileUrl = event.mime_data

    def drop_area(self, ext):
        # If drop is acceptable, the rectangle is blue
        style = {}
        style["Rectangle"] = {"background_color": 0xFF999999}
        style["Rectangle:drop"] = {"background_color": 0xFF994400}

        stack = ui.ZStack()

        with stack:
            ui.Rectangle(style=style)
            text = ui.Label(f"Accepts {ext}", alignment=ui.Alignment.CENTER, word_wrap=True)

        self.fileUrl = stack.set_accept_drop_fn(lambda d, e=ext: MyExtension.drop_accept(d, e))
        stack.set_drop_fn(lambda a, w=text: MyExtension.drop(w, a))

    def createMesh(usd_context, stage, meshName):
        commands.execute('CreateReferenceCommand',
                         usd_context=usd_context,
                         path_to='/World/' + meshName,
                         asset_path=MyExtension.fileUrl,
                         instanceable=True)
        prim = stage.GetPrimAtPath('/World/' + meshName + '/' + meshName + '/' + meshName)
        return prim

    def addAttributes(stage, prim, node, elem, face, edge, normals, colors, meshName):

        numberOfTris = int(face.shape[0] / 3)
        faceCount = np.full((numberOfTris), 3)

        mesh = pxr.PhysicsSchemaTools.createMesh(stage,
                                                 pxr.Sdf.Path('/World/' + meshName + 'Mesh'),
                                                 node.tolist(),
                                                 normals.tolist(),
                                                 face.tolist(),
                                                 faceCount.tolist())

        newPrim = stage.GetPrimAtPath('/World/' + meshName + 'Mesh')

        velocitiesNP = np.zeros_like(node)
        inverseMasses = np.ones(len(node), dtype=float)
        edgesRestLengths = np.zeros(len(edge), dtype=float)
        tetrahedronsRestVolumes = np.zeros(len(elem), dtype=float)

        for i in range(len(edge)):
            edgesRestLengths[i] = np.linalg.norm(node[edge[i][0]] - node[edge[i][1]])

        for i in range(len(elem)):
            tetrahedronPositionA = node[elem[i][0]]
            tetrahedronPositionB = node[elem[i][1]]
            tetrahedronPositionC = node[elem[i][2]]
            tetrahedronPositionD = node[elem[i][3]]

            p1 = tetrahedronPositionB - tetrahedronPositionA
            p2 = tetrahedronPositionC - tetrahedronPositionA
            p3 = tetrahedronPositionD - tetrahedronPositionA

            volume = wp.dot(wp.cross(p1, p2), p3) / 6.0

            tetrahedronsRestVolumes[i] = volume

        velocitiesValue = pxr.Vt.Vec3fArray().FromNumpy(velocitiesNP)
        elemValue = pxr.Vt.Vec4iArray().FromNumpy(elem)
        edgeValue = pxr.Vt.Vec2iArray().FromNumpy(edge)
        edgesRestLengthsValue = pxr.Vt.FloatArray().FromNumpy(edgesRestLengths)
        inverseMassesValue = pxr.Vt.FloatArray().FromNumpy(inverseMasses)
        tetrahedronsRestVolumesValue = pxr.Vt.FloatArray().FromNumpy(tetrahedronsRestVolumes)

        elemAtt = newPrim.CreateAttribute('elem', Sdf.ValueTypeNames.Int4Array)
        edgeAtt = newPrim.CreateAttribute('edge', Sdf.ValueTypeNames.Int2Array)
        edgesRestLengthsAtt = newPrim.CreateAttribute('edgesRestLengths', Sdf.ValueTypeNames.FloatArray)
        inverseMassesAtt = newPrim.CreateAttribute('inverseMasses', Sdf.ValueTypeNames.FloatArray)
        tetrahedronsRestVolumesAtt = newPrim.CreateAttribute('tetrahedronsRestVolumes', Sdf.ValueTypeNames.FloatArray)

        velocitiesAtt = newPrim.GetAttribute('velocities')

        velocitiesAtt.Set(velocitiesValue)
        elemAtt.Set(elemValue)
        edgeAtt.Set(edgeValue)
        edgesRestLengthsAtt.Set(edgesRestLengthsValue)
        inverseMassesAtt.Set(inverseMassesValue)
        tetrahedronsRestVolumesAtt.Set(tetrahedronsRestVolumesValue)

        return mesh, newPrim

    def extractMeshDataToNP(prim):
        points = prim.GetAttribute('points').Get()
        faces = prim.GetAttribute('faceVertexIndices').Get()

        pointsNP = np.array(points, dtype=float)
        facesNP = np.array(faces, dtype=int)
        facesNP = facesNP.reshape((-1, 3))

        return pointsNP, facesNP

    def setPLC(self, value):
        self.PLC = value

    def setQuality(self, value):
        self.Quality = value

    def cross(a, b):
        c = [a[1]*b[2] - a[2]*b[1],
             a[2]*b[0] - a[0]*b[2],
             a[0]*b[1] - a[1]*b[0]]

        return c

    def calculateNormals(node, face):
        numberOfTris = int(face.shape[0] / 3)
        normals = np.empty_like(node)

        for i in range(numberOfTris):
            pIdA = face[i][0]
            pIdB = face[i][1]
            pIdC = face[i][2]

            pA = node[pIdA]
            pB = node[pIdB]
            pC = node[pIdC]

            vA = pB - pA
            vB = pC - pA
            normal = MyExtension.cross(vA, vB)
            normalized = np.linalg.norm(normal)

            normals[pIdA] += normalized
            normals[pIdB] += normalized
            normals[pIdC] += normalized

        return normals

    def on_startup(self, ext_id):
        print("[mnresearch.tetgen] MyExtension startup")
        self._window = ui.Window("Tetrahedralizer", width=300, height=300)
        with self._window.frame:

            self.PLC = False
            self.Quality = False

            with ui.VStack():

                MyExtension.drop_area(self, ".obj")

                with ui.HStack():
                    ui.Label("PLC", height=0)
                    plcCB = ui.CheckBox(width=20)
                    plcCB.model.add_value_changed_fn(
                        lambda a: MyExtension.setPLC(self, a.get_value_as_bool()))
                with ui.HStack():
                    ui.Label("Quality", height=0)
                    qualityCB = ui.CheckBox(width=20)
                    qualityCB.model.add_value_changed_fn(
                        lambda a: MyExtension.setQuality(self, a.get_value_as_bool()))

                def on_click():
                    print("clicked!")

                    self.usd_context = omni.usd.get_context()
                    self.stage = self.usd_context.get_stage()

                    if MyExtension.fileUrl != "":
                        meshName = MyExtension.fileUrl.split(os.sep)[-1][:-4]
                        prim = MyExtension.createMesh(self.usd_context, self.stage, meshName)
                        points, faces = MyExtension.extractMeshDataToNP(prim)
                        tet = tetgenExt.TetGen(points, faces)

                        print('Running tetGen on: ', MyExtension.fileUrl,
                              '\nwith options:',
                              'PLC: ', self.PLC,
                              '\nQuality: ', self.Quality)

                        node, elem, face, edge = tet.tetrahedralize(quality=True,
                                                                    plc=True,
                                                                    facesout=1,
                                                                    edgesout=1)
                        normals = MyExtension.calculateNormals(node, face)
                        colors = np.ones_like(normals)
                        face = face.ravel()
                        mesh, newPrim = MyExtension.addAttributes(self.stage,
                                                                  prim,
                                                                  node,
                                                                  elem,
                                                                  face,
                                                                  edge,
                                                                  normals,
                                                                  colors,
                                                                  meshName)
                        pxr.Usd.Stage.RemovePrim(self.stage, '/World/' + meshName)

                ui.Button("Generate tetrahedral mesh", clicked_fn=lambda: on_click())

    def on_shutdown(self):
        print("[mnresearch.tetgen] MyExtension shutdown")
