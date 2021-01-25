import unittest

from opentracing.mocktracer import MockTracer

from opentracing_decorator.parameter_tagger import ParameterTagger


class TestParameterTagger(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()
        self.scope = self.tracer.start_active_span("TestSpan")

    def test_map_simple_parameters(self):

        parameter_tagger = ParameterTagger()

        def simple_func(self, x, y, z):
            pass

        correct = {"x": 10, "y": 30, "z": 20}
        result = parameter_tagger._map_parameters(simple_func, None, 10, 30, 20)
        self.assertDictEqual(correct, result)

    def test_map_missing_parameters(self):

        parameter_tagger = ParameterTagger()

        def simple_func(self, x, y, z):
            pass

        self.assertRaises(TypeError, simple_func, None, 30, 20)

    def test_map_default_parameters(self):

        parameter_tagger = ParameterTagger()

        def simple_func_with_default(self, x, y, z=30):
            pass

        correct = {"x": 10, "y": 30, "z": 30}
        result = parameter_tagger._map_parameters(simple_func_with_default, None, 10, 30)
        self.assertDictEqual(correct, result)

    def test_map_named_parameters(self):

        parameter_tagger = ParameterTagger()

        def func_with_named_parameters(self, x, y, z):
            pass

        correct = {"x": 10, "y": 30, "z": 30}
        result = parameter_tagger._map_parameters(func_with_named_parameters, None, 10, 30, z=30)
        self.assertDictEqual(correct, result)

    def test_map_typed_parameters(self):

        parameter_tagger = ParameterTagger()

        def func_with_types(x: int, y: int, z: int):
            pass

        correct = {"x": 10, "y": 10, "z": 10}
        result = parameter_tagger._map_parameters(func_with_types, 10, 10, 10)
        self.assertDictEqual(correct, result)

    def test_map_no_parameters(self):

        parameter_tagger = ParameterTagger()

        def func_with_no_args():
            pass

        correct = {}
        result = parameter_tagger._map_parameters(func_with_no_args)
        self.assertDictEqual(correct, result)

    def test_map_simple_prefix(self):

        parameter_tagger = ParameterTagger(parameter_prefix="test")

        def func_simple(x):
            pass

        correct = {"test": {"x": 10}}
        result = parameter_tagger._map_parameters(func_simple, 10)
        self.assertDictEqual(correct, result)

    def test_flatten_simple(self):

        parameter_tagger = ParameterTagger(parameter_prefix="test")

        correct = {"test.x": 10}
        result = parameter_tagger._flatten_parameters({"test": {"x": 10}})
        self.assertDictEqual(correct, result)

    def test_flatten_path(self):

        parameter_tagger = ParameterTagger(parameter_prefix="test", reducer="path")

        correct = {"test/x": 10}
        result = parameter_tagger._flatten_parameters({"test": {"x": 10}})
        self.assertDictEqual(correct, result)

    def test_flatten_list(self):

        parameter_tagger = ParameterTagger(parameter_prefix="test", reducer="dot")

        correct = {"test.x.0": 10, "test.x.1": 20}
        result = parameter_tagger._flatten_parameters({"test": {"x": [10, 20]}})
        self.assertDictEqual(correct, result)
