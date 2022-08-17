"""Support for simplified access to data on nodes of type mnresearch.tetgen.PBDBasicGravity

PBDGravity
"""

import omni.graph.core as og
import sys
import traceback
import numpy
class OgnNewNodeDatabase(og.Database):
    """Helper class providing simplified access to data on nodes of type mnresearch.tetgen.PBDBasicGravity

    Class Members:
        node: Node being evaluated

    Attribute Value Properties:
        Inputs:
            inputs.edge
            inputs.edgesRestLengths
            inputs.elem
            inputs.gravity
            inputs.ground
            inputs.inverseMasses
            inputs.ks_distance
            inputs.ks_volume
            inputs.num_substeps
            inputs.points
            inputs.sim_constraints
            inputs.tetrahedronsRestVolumes
            inputs.velocities
            inputs.velocity_dampening
        Outputs:
            outputs.points
            outputs.velocities
    """
    # This is an internal object that provides per-class storage of a per-node data dictionary
    PER_NODE_DATA = {}
    # This is an internal object that describes unchanging attributes in a generic way
    # The values in this list are in no particular order, as a per-attribute tuple
    #     Name, Type, ExtendedTypeIndex, UiName, Description, Metadata, Is_Required, DefaultValue
    # You should not need to access any of this data directly, use the defined database interfaces
    INTERFACE = og.Database._get_interface([
        ('inputs:edge', 'int2[]', 0, None, 'Input edges', {og.MetadataKeys.DEFAULT: '[]'}, True, []),
        ('inputs:edgesRestLengths', 'float[]', 0, None, 'Input edges rest lengths', {og.MetadataKeys.DEFAULT: '[]'}, True, []),
        ('inputs:elem', 'int4[]', 0, None, 'Input tetrahedrons', {og.MetadataKeys.DEFAULT: '[]'}, True, []),
        ('inputs:gravity', 'vector3f', 0, None, 'Gravity constant', {og.MetadataKeys.DEFAULT: '[0.0, -9.8, 0.0]'}, True, [0.0, -9.8, 0.0]),
        ('inputs:ground', 'float', 0, None, 'Ground level', {og.MetadataKeys.DEFAULT: '-100.0'}, True, -100.0),
        ('inputs:inverseMasses', 'float[]', 0, None, 'Inverse masses', {og.MetadataKeys.DEFAULT: '[]'}, True, []),
        ('inputs:ks_distance', 'float', 0, None, '', {og.MetadataKeys.DEFAULT: '1.0'}, True, 1.0),
        ('inputs:ks_volume', 'float', 0, None, '', {og.MetadataKeys.DEFAULT: '1.0'}, True, 1.0),
        ('inputs:num_substeps', 'int', 0, None, '', {og.MetadataKeys.DEFAULT: '8'}, True, 8),
        ('inputs:points', 'point3f[]', 0, None, 'Input points', {og.MetadataKeys.DEFAULT: '[]'}, True, []),
        ('inputs:sim_constraints', 'int', 0, None, '', {og.MetadataKeys.DEFAULT: '1'}, True, 1),
        ('inputs:tetrahedronsRestVolumes', 'float[]', 0, None, 'Input tetrahedrons rest volumes', {og.MetadataKeys.DEFAULT: '[]'}, True, []),
        ('inputs:velocities', 'vector3f[]', 0, None, 'Input velocities', {og.MetadataKeys.DEFAULT: '[]'}, True, []),
        ('inputs:velocity_dampening', 'float', 0, None, '', {og.MetadataKeys.DEFAULT: '0.1'}, True, 0.1),
        ('outputs:points', 'point3f[]', 0, None, 'Output points', {}, True, None),
        ('outputs:velocities', 'vector3f[]', 0, None, 'Output velocities', {}, True, None),
    ])
    @classmethod
    def _populate_role_data(cls):
        """Populate a role structure with the non-default roles on this node type"""
        role_data = super()._populate_role_data()
        role_data.inputs.gravity = og.Database.ROLE_VECTOR
        role_data.inputs.points = og.Database.ROLE_POINT
        role_data.inputs.velocities = og.Database.ROLE_VECTOR
        role_data.outputs.points = og.Database.ROLE_POINT
        role_data.outputs.velocities = og.Database.ROLE_VECTOR
        return role_data
    class ValuesForInputs(og.DynamicAttributeAccess):
        """Helper class that creates natural hierarchical access to input attributes"""
        def __init__(self, node: og.Node, attributes, dynamic_attributes: og.DynamicAttributeInterface):
            """Initialize simplified access for the attribute data"""
            context = node.get_graph().get_default_graph_context()
            super().__init__(context, node, attributes, dynamic_attributes)

        @property
        def edge(self):
            data_view = og.AttributeValueHelper(self._attributes.edge)
            return data_view.get()

        @edge.setter
        def edge(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.edge)
            data_view = og.AttributeValueHelper(self._attributes.edge)
            data_view.set(value)
            self.edge_size = data_view.get_array_size()

        @property
        def edgesRestLengths(self):
            data_view = og.AttributeValueHelper(self._attributes.edgesRestLengths)
            return data_view.get()

        @edgesRestLengths.setter
        def edgesRestLengths(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.edgesRestLengths)
            data_view = og.AttributeValueHelper(self._attributes.edgesRestLengths)
            data_view.set(value)
            self.edgesRestLengths_size = data_view.get_array_size()

        @property
        def elem(self):
            data_view = og.AttributeValueHelper(self._attributes.elem)
            return data_view.get()

        @elem.setter
        def elem(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.elem)
            data_view = og.AttributeValueHelper(self._attributes.elem)
            data_view.set(value)
            self.elem_size = data_view.get_array_size()

        @property
        def gravity(self):
            data_view = og.AttributeValueHelper(self._attributes.gravity)
            return data_view.get()

        @gravity.setter
        def gravity(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.gravity)
            data_view = og.AttributeValueHelper(self._attributes.gravity)
            data_view.set(value)

        @property
        def ground(self):
            data_view = og.AttributeValueHelper(self._attributes.ground)
            return data_view.get()

        @ground.setter
        def ground(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.ground)
            data_view = og.AttributeValueHelper(self._attributes.ground)
            data_view.set(value)

        @property
        def inverseMasses(self):
            data_view = og.AttributeValueHelper(self._attributes.inverseMasses)
            return data_view.get()

        @inverseMasses.setter
        def inverseMasses(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.inverseMasses)
            data_view = og.AttributeValueHelper(self._attributes.inverseMasses)
            data_view.set(value)
            self.inverseMasses_size = data_view.get_array_size()

        @property
        def ks_distance(self):
            data_view = og.AttributeValueHelper(self._attributes.ks_distance)
            return data_view.get()

        @ks_distance.setter
        def ks_distance(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.ks_distance)
            data_view = og.AttributeValueHelper(self._attributes.ks_distance)
            data_view.set(value)

        @property
        def ks_volume(self):
            data_view = og.AttributeValueHelper(self._attributes.ks_volume)
            return data_view.get()

        @ks_volume.setter
        def ks_volume(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.ks_volume)
            data_view = og.AttributeValueHelper(self._attributes.ks_volume)
            data_view.set(value)

        @property
        def num_substeps(self):
            data_view = og.AttributeValueHelper(self._attributes.num_substeps)
            return data_view.get()

        @num_substeps.setter
        def num_substeps(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.num_substeps)
            data_view = og.AttributeValueHelper(self._attributes.num_substeps)
            data_view.set(value)

        @property
        def points(self):
            data_view = og.AttributeValueHelper(self._attributes.points)
            return data_view.get()

        @points.setter
        def points(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.points)
            data_view = og.AttributeValueHelper(self._attributes.points)
            data_view.set(value)
            self.points_size = data_view.get_array_size()

        @property
        def sim_constraints(self):
            data_view = og.AttributeValueHelper(self._attributes.sim_constraints)
            return data_view.get()

        @sim_constraints.setter
        def sim_constraints(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.sim_constraints)
            data_view = og.AttributeValueHelper(self._attributes.sim_constraints)
            data_view.set(value)

        @property
        def tetrahedronsRestVolumes(self):
            data_view = og.AttributeValueHelper(self._attributes.tetrahedronsRestVolumes)
            return data_view.get()

        @tetrahedronsRestVolumes.setter
        def tetrahedronsRestVolumes(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.tetrahedronsRestVolumes)
            data_view = og.AttributeValueHelper(self._attributes.tetrahedronsRestVolumes)
            data_view.set(value)
            self.tetrahedronsRestVolumes_size = data_view.get_array_size()

        @property
        def velocities(self):
            data_view = og.AttributeValueHelper(self._attributes.velocities)
            return data_view.get()

        @velocities.setter
        def velocities(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.velocities)
            data_view = og.AttributeValueHelper(self._attributes.velocities)
            data_view.set(value)
            self.velocities_size = data_view.get_array_size()

        @property
        def velocity_dampening(self):
            data_view = og.AttributeValueHelper(self._attributes.velocity_dampening)
            return data_view.get()

        @velocity_dampening.setter
        def velocity_dampening(self, value):
            if self._setting_locked:
                raise og.ReadOnlyError(self._attributes.velocity_dampening)
            data_view = og.AttributeValueHelper(self._attributes.velocity_dampening)
            data_view.set(value)
    class ValuesForOutputs(og.DynamicAttributeAccess):
        """Helper class that creates natural hierarchical access to output attributes"""
        def __init__(self, node: og.Node, attributes, dynamic_attributes: og.DynamicAttributeInterface):
            """Initialize simplified access for the attribute data"""
            context = node.get_graph().get_default_graph_context()
            super().__init__(context, node, attributes, dynamic_attributes)
            self.points_size = None
            self.velocities_size = None

        @property
        def points(self):
            data_view = og.AttributeValueHelper(self._attributes.points)
            return data_view.get(reserved_element_count = self.points_size)

        @points.setter
        def points(self, value):
            data_view = og.AttributeValueHelper(self._attributes.points)
            data_view.set(value)
            self.points_size = data_view.get_array_size()

        @property
        def velocities(self):
            data_view = og.AttributeValueHelper(self._attributes.velocities)
            return data_view.get(reserved_element_count = self.velocities_size)

        @velocities.setter
        def velocities(self, value):
            data_view = og.AttributeValueHelper(self._attributes.velocities)
            data_view.set(value)
            self.velocities_size = data_view.get_array_size()
    class ValuesForState(og.DynamicAttributeAccess):
        """Helper class that creates natural hierarchical access to state attributes"""
        def __init__(self, node: og.Node, attributes, dynamic_attributes: og.DynamicAttributeInterface):
            """Initialize simplified access for the attribute data"""
            context = node.get_graph().get_default_graph_context()
            super().__init__(context, node, attributes, dynamic_attributes)
    def __init__(self, node):
        super().__init__(node)
        dynamic_attributes = self.dynamic_attribute_data(node, og.AttributePortType.ATTRIBUTE_PORT_TYPE_INPUT)
        self.inputs = OgnNewNodeDatabase.ValuesForInputs(node, self.attributes.inputs, dynamic_attributes)
        dynamic_attributes = self.dynamic_attribute_data(node, og.AttributePortType.ATTRIBUTE_PORT_TYPE_OUTPUT)
        self.outputs = OgnNewNodeDatabase.ValuesForOutputs(node, self.attributes.outputs, dynamic_attributes)
        dynamic_attributes = self.dynamic_attribute_data(node, og.AttributePortType.ATTRIBUTE_PORT_TYPE_STATE)
        self.state = OgnNewNodeDatabase.ValuesForState(node, self.attributes.state, dynamic_attributes)
    class abi:
        """Class defining the ABI interface for the node type"""
        @staticmethod
        def get_node_type():
            get_node_type_function = getattr(OgnNewNodeDatabase.NODE_TYPE_CLASS, 'get_node_type', None)
            if callable(get_node_type_function):
                return get_node_type_function()
            return 'mnresearch.tetgen.PBDBasicGravity'
        @staticmethod
        def compute(context, node):
            db = OgnNewNodeDatabase(node)
            try:
                db.inputs._setting_locked = True
                compute_function = getattr(OgnNewNodeDatabase.NODE_TYPE_CLASS, 'compute', None)
                if callable(compute_function) and compute_function.__code__.co_argcount > 1:
                    return compute_function(context, node)
                return OgnNewNodeDatabase.NODE_TYPE_CLASS.compute(db)
            except Exception as error:
                stack_trace = "".join(traceback.format_tb(sys.exc_info()[2].tb_next))
                db.log_error(f'Assertion raised in compute - {error}\n{stack_trace}', add_context=False)
            finally:
                db.inputs._setting_locked = False
            return False
        @staticmethod
        def initialize(context, node):
            OgnNewNodeDatabase._initialize_per_node_data(node)

            # Set any default values the attributes have specified
            if not node._do_not_use():
                db = OgnNewNodeDatabase(node)
                db.inputs.edge = []
                db.inputs.edgesRestLengths = []
                db.inputs.elem = []
                db.inputs.gravity = [0.0, -9.8, 0.0]
                db.inputs.ground = -100.0
                db.inputs.inverseMasses = []
                db.inputs.ks_distance = 1.0
                db.inputs.ks_volume = 1.0
                db.inputs.num_substeps = 8
                db.inputs.points = []
                db.inputs.sim_constraints = 1
                db.inputs.tetrahedronsRestVolumes = []
                db.inputs.velocities = []
                db.inputs.velocity_dampening = 0.1
            initialize_function = getattr(OgnNewNodeDatabase.NODE_TYPE_CLASS, 'initialize', None)
            if callable(initialize_function):
                initialize_function(context, node)
        @staticmethod
        def release(node):
            release_function = getattr(OgnNewNodeDatabase.NODE_TYPE_CLASS, 'release', None)
            if callable(release_function):
                release_function(node)
            OgnNewNodeDatabase._release_per_node_data(node)
        @staticmethod
        def update_node_version(context, node, old_version, new_version):
            update_node_version_function = getattr(OgnNewNodeDatabase.NODE_TYPE_CLASS, 'update_node_version', None)
            if callable(update_node_version_function):
                return update_node_version_function(context, node, old_version, new_version)
            return False
        @staticmethod
        def initialize_type(node_type):
            initialize_type_function = getattr(OgnNewNodeDatabase.NODE_TYPE_CLASS, 'initialize_type', None)
            needs_initializing = True
            if callable(initialize_type_function):
                needs_initializing = initialize_type_function(node_type)
            if needs_initializing:
                node_type.set_metadata(og.MetadataKeys.EXTENSION, "mnaskret.pbdgravity")
                node_type.set_metadata(og.MetadataKeys.UI_NAME, "PBDGravity")
                node_type.set_metadata(og.MetadataKeys.DESCRIPTION, "PBDGravity")
                node_type.set_metadata(og.MetadataKeys.LANGUAGE, "Python")
                OgnNewNodeDatabase.INTERFACE.add_to_node_type(node_type)
        @staticmethod
        def on_connection_type_resolve(node):
            on_connection_type_resolve_function = getattr(OgnNewNodeDatabase.NODE_TYPE_CLASS, 'on_connection_type_resolve', None)
            if callable(on_connection_type_resolve_function):
                on_connection_type_resolve_function(node)
    NODE_TYPE_CLASS = None
    GENERATOR_VERSION = (1, 4, 0)
    TARGET_VERSION = (2, 29, 1)
    @staticmethod
    def register(node_type_class):
        OgnNewNodeDatabase.NODE_TYPE_CLASS = node_type_class
        og.register_node_type(OgnNewNodeDatabase.abi, 1)
    @staticmethod
    def deregister():
        og.deregister_node_type("mnaskret.pbdgravity.PBDGravity")
