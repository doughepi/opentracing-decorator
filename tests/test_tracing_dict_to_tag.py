import unittest
import uuid
from typing import Dict, List

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()
        self.tracing = Tracing(self.tracer)

    def test_simple(self):

        span = self.tracer.start_active_span("TestSpan").span
        input = {"key_1": 10, "key_2": 20, "key_3": 30}
        correct = {"key_1": 10, "key_2": 20, "key_3": 30}
        self.tracing._dict_to_tag(span, input)
        self.assertDictEqual(span.tags, correct)

    def test_complex_types(self):

        span = self.tracer.start_active_span("TestSpan").span
        id = uuid.uuid4()
        input = {"key_1": id}
        correct = {"key_1": id}
        self.tracing._dict_to_tag(span, input)
        self.assertDictEqual(span.tags, correct)

    def test_empty(self):

        span = self.tracer.start_active_span("TestSpan").span
        input: Dict = {}
        correct: Dict = {}
        self.tracing._dict_to_tag(span, input)
        self.assertDictEqual(span.tags, correct)

    def test_none(self):

        span = self.tracer.start_active_span("TestSpan").span
        input = None
        self.assertRaises(TypeError, self.tracing._dict_to_tag, span, input)

    def test_non_dict(self):

        span = self.tracer.start_active_span("TestSpan").span
        input: List = []
        self.assertRaises(TypeError, self.tracing._dict_to_tag, span, input)
