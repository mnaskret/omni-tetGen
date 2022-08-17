import omni.kit.test
import omni.graph.core as og
import omni.graph.core.tests as ogts
import os
import carb


class TestOgn(ogts.test_case_class(use_schema_prims=True, allow_implicit_graph=False)):

    async def test_import(self):
        import mnresearch.tetgen.ogn.PBDBasicGravityDatabase
        self.assertTrue(hasattr(mnresearch.tetgen.ogn.PBDBasicGravityDatabase, "PBDBasicGravityDatabase"))

    async def test_usda(self):
        test_file_name = "PBDBasicGravityTemplate.usda"
        usd_path = os.path.join(os.path.dirname(__file__), "usd", test_file_name)
        if not os.path.exists(usd_path):
            self.assertTrue(False, f"{usd_path} not found for loading test")
        (result, error) = await ogts.load_test_file(usd_path)
        self.assertTrue(result, f'{error} on {usd_path}')
        test_node = og.Controller.node("/TestGraph/Template_mnresearch_tetgen_PBDBasicGravity")
        self.assertTrue(test_node.is_valid())
        node_type_name = test_node.get_type_name()
        self.assertEqual(og.GraphRegistry().get_node_type_version(node_type_name), 1)
        self.assertTrue(test_node.get_attribute_exists("inputs:edge"))

        input_attr = test_node.get_attribute("inputs:edge")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:edge attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:edgesRestLengths"))

        input_attr = test_node.get_attribute("inputs:edgesRestLengths")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:edgesRestLengths attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:elem"))

        input_attr = test_node.get_attribute("inputs:elem")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:elem attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:gravity"))

        input_attr = test_node.get_attribute("inputs:gravity")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([0.0, -9.8, 0.0], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:gravity attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:ground"))

        input_attr = test_node.get_attribute("inputs:ground")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values(-100.0, actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:ground attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:inverseMasses"))

        input_attr = test_node.get_attribute("inputs:inverseMasses")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:inverseMasses attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:ks_distance"))

        input_attr = test_node.get_attribute("inputs:ks_distance")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values(1.0, actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:ks_distance attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:ks_volume"))

        input_attr = test_node.get_attribute("inputs:ks_volume")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values(1.0, actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:ks_volume attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:num_substeps"))

        input_attr = test_node.get_attribute("inputs:num_substeps")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values(8, actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:num_substeps attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:points"))

        input_attr = test_node.get_attribute("inputs:points")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:points attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:sim_constraints"))

        input_attr = test_node.get_attribute("inputs:sim_constraints")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values(1, actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:sim_constraints attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:tetrahedronsRestVolumes"))

        input_attr = test_node.get_attribute("inputs:tetrahedronsRestVolumes")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:tetrahedronsRestVolumes attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:velocities"))

        input_attr = test_node.get_attribute("inputs:velocities")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values([], actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:velocities attribute value error")
        self.assertTrue(test_node.get_attribute_exists("inputs:velocity_dampening"))

        input_attr = test_node.get_attribute("inputs:velocity_dampening")
        actual_input = og.Controller.get(input_attr)
        ogts.verify_values(0.1, actual_input, "mnresearch.tetgen.PBDBasicGravity USD load test - inputs:velocity_dampening attribute value error")
