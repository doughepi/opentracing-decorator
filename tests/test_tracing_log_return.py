import unittest

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()
        self.tracing = Tracing(self.tracer)
        self.span = self.tracer.start_active_span("TestSpan").span

    def test_simple(self):
        correct = {"return": 10}
        self.tracing._log_return(self.span, 10)
        self.assertDictEqual(self.span.logs[0].key_values, correct)

    def test_prefix(self):
        correct = {"test": 10}
        self.tracing._log_return(self.span, 10, return_prefix="test")
        self.assertDictEqual(self.span.logs[0].key_values, correct)

    def test_complex(self):
        input = {"key_1": 10, "key_2": 20, "key_3": {"a": 30}}
        correct = {"return.key_1": 10, "return.key_2": 20, "return.key_3.a": 30}
        self.tracing._log_return(self.span, input)
        self.assertDictEqual(self.span.logs[0].key_values, correct)

    def test_path(self):
        input = {"key_1": 10, "key_2": 20, "key_3": {"a": 30}}
        correct = {"return/key_1": 10, "return/key_2": 20, "return/key_3/a": 30}
        self.tracing._log_return(self.span, input, return_reducer="path")
        self.assertDictEqual(self.span.logs[0].key_values, correct)

    def test_none(self):
        correct = {"return": None}
        self.tracing._log_return(self.span, None)
        self.assertDictEqual(self.span.logs[0].key_values, correct)

    def test_object(self):
        self.tracing._log_return(self.span, MockTracer())
        self.assertIsInstance(self.span.logs[0].key_values["return"], str)
