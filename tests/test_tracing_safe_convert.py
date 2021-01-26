import unittest
import uuid

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()

    def test_simple(self):
        id = uuid.uuid4()
        input = {"a": {"b": "c"}, "b": {"a": id}}
        correct = {"a": {"b": "c"}, "b": {"a": str(id)}}
        tracing = Tracing(self.tracer)
        result = tracing._safe_convert(input)
        self.assertDictEqual(result, correct)

    def test_non_str_key(self):
        input = {"a": {"b": "c"}, uuid.uuid4(): {"a": 10}}
        tracing = Tracing(self.tracer)
        self.assertRaises(TypeError, tracing._safe_convert, input)
