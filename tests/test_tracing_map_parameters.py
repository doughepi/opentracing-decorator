import unittest
from typing import Dict

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()
        self.tracing = Tracing(self.tracer)

    def test_simple_parameters(self):
        def simple_func(x, y, z):
            pass

        correct = {"x": 10, "y": 30, "z": 20}
        result = self.tracing._map_parameters(simple_func, 10, 30, 20)
        self.assertDictEqual(result, correct)

    def test_missing_parameters(self):
        def simple_func(x, y, z):
            pass

        self.assertRaises(TypeError, self.tracing._map_parameters, simple_func, 30, 20)

    def test_default_parameters(self):
        def simple_func_with_default(x, y, z=30):
            pass

        correct = {"x": 10, "y": 30, "z": 30}
        result = self.tracing._map_parameters(simple_func_with_default, 10, 30)
        self.assertDictEqual(result, correct)

    def test_named_parameters(self):
        def func_with_named_parameters(x, y, z):
            pass

        correct = {"x": 10, "y": 30, "z": 30}
        result = self.tracing._map_parameters(func_with_named_parameters, 10, 30, z=30)
        self.assertDictEqual(result, correct)

    def test_typed_parameters(self):
        def func_with_types(x: int, y: int, z: int):
            pass

        correct = {"x": 10, "y": 10, "z": 10}
        result = self.tracing._map_parameters(func_with_types, 10, 10, 10)
        self.assertDictEqual(result, correct)

    def test_no_parameters(self):
        def func_with_no_args():
            pass

        correct: Dict = {}
        result = self.tracing._map_parameters(func_with_no_args)
        self.assertDictEqual(result, correct)
