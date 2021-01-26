import unittest
from typing import Dict

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()
        self.tracing = Tracing(self.tracer)
        self.span = self.tracer.start_active_span("TestSpan").span

    def test_simple(self):
        def func_simple(x, y, z):
            pass

        correct = {"x": 10, "y": 20, "z": 30}
        self.tracing._tag_parameters(self.span, func_simple, 10, 20, 30)
        self.assertDictEqual(self.span.tags, correct)

    def test_dict(self):
        def func_dict(x: dict):
            pass

        input = {"key_1": 10, "key_2": 20, "key_3": {"a": 30}}
        correct = {"x.key_1": 10, "x.key_2": 20, "x.key_3.a": 30}

        self.tracing._tag_parameters(self.span, func_dict, input)
        self.assertDictEqual(self.span.tags, correct)

    def test_prefix(self):
        def func_prefix(x):
            pass

        correct = {"test.x": 10}

        self.tracing._tag_parameters(self.span, func_prefix, 10, parameter_prefix="test")
        self.assertDictEqual(self.span.tags, correct)

    def test_no_parameters(self):
        def func_no_parameters():
            pass

        correct: Dict = {}

        self.tracing._tag_parameters(self.span, func_no_parameters, parameter_prefix="test")
        self.assertDictEqual(self.span.tags, correct)

    def test_too_many_arguments(self):
        def func_too_many_arguments(x):
            pass

        self.assertRaises(
            TypeError,
            self.tracing._tag_parameters,
            self.span,
            func_too_many_arguments,
            10,
            20,
        )

    def test_no_flatten(self):
        def func_no_flatten(x):
            pass

        input = {"key_1": 10, "key_2": 20, "key_3": {"a": 30}}
        correct = {"x": {"key_1": 10, "key_2": 20, "key_3": {"a": 30}}}

        self.tracing._tag_parameters(self.span, func_no_flatten, input, flatten_parameters=False)
        self.assertDictEqual(self.span.tags, correct)

    def test_path_prefix(self):
        def func_path_prefix(x):
            pass

        input = {"key_1": 10, "key_2": 20, "key_3": {"a": 30}}
        correct = {"x/key_1": 10, "x/key_2": 20, "x/key_3/a": 30}

        self.tracing._tag_parameters(self.span, func_path_prefix, input, parameter_reducer="path")
        self.assertDictEqual(self.span.tags, correct)
