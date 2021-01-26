import numbers
import unittest
import uuid
from unittest.mock import MagicMock, create_autospec

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()
        self.tracing = Tracing(self.tracer)

    def test_func_called(self):
        func = MagicMock()
        traced_func = self.tracing.trace("TestTrace", func)

        traced_func()

        self.assertTrue(func.called)

    def test_function_traced(self):
        func = MagicMock()
        traced_func = self.tracing.trace(str(uuid.uuid4()), func)

        traced_func()

        self.assertEqual(
            len(self.tracer.finished_spans()),
            1,
        )

    def test_span_passed(self):
        func = MagicMock()
        traced_func = self.tracing.trace("TestTrace", func, pass_span=True)

        traced_func()

        func.assert_called_with(span=self.tracer.finished_spans()[0])

    def test_parameters_tagged(self):
        def func_signature(a, b, c):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = self.tracing.trace("TestTrace", func, tag_parameters=True)

        traced_func(10, 20, 30)

        correct = {"a": 10, "b": 20, "c": 30}
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertDictEqual(correct, span_tags)

    def test_parameters_tagged_with_prefix(self):
        def func_signature(a, b, c):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = self.tracing.trace("TestTrace", func, tag_parameters=True, parameter_prefix="test")

        traced_func(10, 20, 30)

        correct = {"test.a": 10, "test.b": 20, "test.c": 30}
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertDictEqual(correct, span_tags)

    def test_parameters_tagged_type_class(self):
        def func_signature(a: int, b: MockTracer, c: str = "Test"):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = self.tracing.trace("TestTrace", func, tag_parameters=True)

        traced_func(10, MockTracer())
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertIsInstance(span_tags["b"], str)

    def test_parameters_tagged_type_number(self):
        def func_signature(a: int, b: MockTracer, c: str = "Test"):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = self.tracing.trace("TestTrace", func, tag_parameters=True)

        traced_func(10, MockTracer())
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertIsInstance(span_tags["a"], numbers.Number)

    def test_parameters_tagged_type_bool(self):
        def func_signature(a: bool, b: MockTracer, c: str = "Test"):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = self.tracing.trace("TestTrace", func, tag_parameters=True)

        traced_func(True, MockTracer())
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertIsInstance(span_tags["a"], bool)

    def test_function_log_return_only_once(self):
        func = MagicMock(return_value=3)
        traced_func = self.tracing.trace("TestTrace", func, log_return=True)

        traced_func()

        logs = self.tracer.finished_spans()[0].logs

        self.assertEqual(len(logs), 1, "There should only be one log.")

    def test_log_return_int(self):
        func = MagicMock(return_value=3)
        traced_func = self.tracing.trace("TestTrace", func, log_return=True)

        traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {"return": 3}
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_dict(self):
        func = MagicMock(return_value={"test_1": 3, "test_2": 6})
        traced_func = self.tracing.trace("TestTrace", func, log_return=True)

        traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {"return.test_1": 3, "return.test_2": 6}
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_list(self):
        func = MagicMock(return_value={"test_1": 3, "test_2": [1, 2, 3]})
        traced_func = self.tracing.trace("TestTrace", func, log_return=True)

        traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {
            "return.test_1": 3,
            "return.test_2.0": 1,
            "return.test_2.1": 2,
            "return.test_2.2": 3,
        }
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_num_key(self):
        func = MagicMock(return_value={3: 3, "test_2": [1, 2, 3]})
        traced_func = self.tracing.trace("TestTrace", func, log_return=True)

        traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {
            "return.3": 3,
            "return.test_2.0": 1,
            "return.test_2.1": 2,
            "return.test_2.2": 3,
        }
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_tuple_key(self):
        func = MagicMock(return_value={(1, 1): 3, "test_2": [1, 2, 3]})
        traced_func = self.tracing.trace("TestTrace", func, log_return=True)

        traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {
            "return.(1, 1)": 3,
            "return.test_2.0": 1,
            "return.test_2.1": 2,
            "return.test_2.2": 3,
        }
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_object_key(self):
        test_object = MockTracer()

        func = MagicMock(return_value={test_object: "Hello"})
        traced_func = self.tracing.trace("TestTrace", func, log_return=True)

        traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {f"return.{str(test_object)}": "Hello"}
        self.assertDictEqual(correct, logs[0].key_values)
