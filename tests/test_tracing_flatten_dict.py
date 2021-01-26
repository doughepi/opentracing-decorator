import unittest

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()
        self.tracing = Tracing(self.tracer)

    def test_flatten_simple(self):
        correct = {"test.x": 10}
        result = self.tracing._flatten_dict({"test": {"x": 10}})
        self.assertDictEqual(result, correct)

    def test_flatten_path(self):
        correct = {"test/x": 10}
        result = self.tracing._flatten_dict({"test": {"x": 10}}, reducer="path")
        self.assertDictEqual(result, correct)

    def test_flatten_list(self):
        correct = {"test.x.0": 10, "test.x.1": 20}
        result = self.tracing._flatten_dict({"test": {"x": [10, 20]}}, reducer="dot")
        self.assertDictEqual(result, correct)
