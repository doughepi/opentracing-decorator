import unittest
import uuid
from unittest.mock import MagicMock, create_autospec
import numbers

from opentracing.mocktracer import MockTracer

from opentracing_decorator.tracing import Tracing


class TestTracing(unittest.TestCase):
    def setUp(self):
        self.tracer = MockTracer()

    def test_map_simple_parameters(self):
        tracing = Tracing(self.tracer)

        def simple_func(self, x, y, z):
            pass

        correct = {"x": 10, "y": 30, "z": 20}
        result = tracing._map_parameters(simple_func, None, 10, 30, 20)
        self.assertDictEqual(correct, result)

    def test_map_missing_parameters(self):
        tracing = Tracing(self.tracer)

        def simple_func(self, x, y, z):
            pass

        self.assertRaises(TypeError, simple_func, None, 30, 20)

    def test_map_default_parameters(self):
        tracing = Tracing(self.tracer)

        def simple_func_with_default(self, x, y, z=30):
            pass

        correct = {"x": 10, "y": 30, "z": 30}
        result = tracing._map_parameters(simple_func_with_default, None, 10, 30)
        self.assertDictEqual(correct, result)

    def test_map_named_parameters(self):
        tracing = Tracing(self.tracer)

        def func_with_named_parameters(self, x, y, z):
            pass

        correct = {"x": 10, "y": 30, "z": 30}
        result = tracing._map_parameters(func_with_named_parameters, None, 10, 30, z=30)
        self.assertDictEqual(correct, result)

    def test_map_typed_parameters(self):
        tracing = Tracing(self.tracer)

        def func_with_types(x: int, y: int, z: int):
            pass

        correct = {"x": 10, "y": 10, "z": 10}
        result = tracing._map_parameters(func_with_types, 10, 10, 10)
        self.assertDictEqual(correct, result)

    def test_map_no_parameters(self):
        tracing = Tracing(self.tracer)

        def func_with_no_args():
            pass

        correct = {}
        result = tracing._map_parameters(func_with_no_args)
        self.assertDictEqual(correct, result)

    def test_map_simple_prefix(self):
        tracing = Tracing(self.tracer)

        def func_simple(x):
            pass

        correct = {"test": {"x": 10}}
        result = tracing._map_parameters(parameter_prefix="test", func_simple, 10)
        self.assertDictEqual(correct, result)

    def test_flatten_simple(self):
        tracing = Tracing(self.tracer, parameter_prefix="test")

        correct = {"test.x": 10}
        result = tracing._flatten_dict({"test": {"x": 10}})
        self.assertDictEqual(correct, result)

    def test_flatten_path(self):
        tracing = Tracing(self.tracer, parameter_prefix="test", reducer="path")

        correct = {"test/x": 10}
        result = tracing._flatten_dict({"test": {"x": 10}})
        self.assertDictEqual(correct, result)

    def test_flatten_list(self):
        tracing = Tracing(self.tracer, parameter_prefix="test", reducer="dot")

        correct = {"test.x.0": 10, "test.x.1": 20}
        result = tracing._flatten_dict({"test": {"x": [10, 20]}})
        self.assertDictEqual(correct, result)

    def test_func_called(self):
        tracing = Tracing(self.tracer)

        func = MagicMock()
        traced_func = tracing.trace("TestTrace", func)

        result = traced_func()

        self.assertTrue(func.called)

    def test_function_traced(self):
        tracing = Tracing(self.tracer)

        func = MagicMock()
        traced_func = tracing.trace(uuid.uuid4(), func, pass_span=True)

        result = traced_func()

        call_args = func.call_args

        self.assertEqual(
            len(self.tracer.finished_spans()),
            1,
            "More than one span or no span was found on the tracer.",
        )

    def test_function_only_traced_once(self):
        tracing = Tracing(self.tracer)

        func = MagicMock()
        traced_func = tracing.trace(uuid.uuid4(), func, pass_span=True)

        result = traced_func()

        self.assertEqual(
            len(self.tracer.finished_spans()),
            1,
            "More than one span or no span was found on the tracer.",
        )

    def test_span_passed(self):
        tracing = Tracing(self.tracer)

        func = MagicMock()
        traced_func = tracing.trace("TestTrace", func, pass_span=True)

        result = traced_func()

        func.assert_called_with(span=self.tracer.finished_spans()[0])

    def test_parameters_tagged(self):
        tracing = Tracing(self.tracer)

        def func_signature(a, b, c):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = tracing.trace("TestTrace", func, tag_parameters=True)

        result = traced_func(10, 20, 30)

        correct = {"a": 10, "b": 20, "c": 30}
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertDictEqual(correct, span_tags)

    def test_parameters_tagged_with_prefix(self):
        tracing = Tracing(self.tracer, parameter_prefix="test")

        def func_signature(a, b, c):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = tracing.trace("TestTrace", func, tag_parameters=True)

        result = traced_func(10, 20, 30)

        correct = {"test.a": 10, "test.b": 20, "test.c": 30}
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertDictEqual(correct, span_tags)

    def test_parameters_tagged_type_class(self):
        tracing = Tracing(self.tracer)

        # Parameter 'b' can be any type really. Just trying to test how parameter tagging handles complex types.
        def func_signature(a: int, b: MockTracer, c: str = "Test"):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = tracing.trace("TestTrace", func, tag_parameters=True)

        result = traced_func(10, MockTracer())
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertIsInstance(span_tags["b"], str)

    def test_parameters_tagged_type_number(self):
        tracing = Tracing(self.tracer)

        # Parameter 'b' can be any type really. Just trying to test how parameter tagging handles complex types.
        def func_signature(a: int, b: MockTracer, c: str = "Test"):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = tracing.trace("TestTrace", func, tag_parameters=True)

        result = traced_func(10, MockTracer())
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertIsInstance(span_tags["a"], numbers.Number)

    def test_parameters_tagged_type_bool(self):
        tracing = Tracing(self.tracer)

        # Parameter 'b' can be any type really. Just trying to test how parameter tagging handles complex types.
        def func_signature(a: bool, b: MockTracer, c: str = "Test"):
            pass

        func = create_autospec(func_signature, spec_set=True)
        traced_func = tracing.trace("TestTrace", func, tag_parameters=True)

        result = traced_func(True, MockTracer())
        span_tags = self.tracer.finished_spans()[0].tags

        self.assertIsInstance(span_tags["a"], bool)

    def test_function_log_return_only_once(self):
        tracing = Tracing(self.tracer)

        func = MagicMock(return_value=3)
        traced_func = tracing.trace("TestTrace", func, log_return=True)

        result = traced_func()

        logs = self.tracer.finished_spans()[0].logs

        self.assertEqual(len(logs), 1, "There should only be one log.")
    
    def test_log_return_int(self):
        tracing = Tracing(self.tracer)

        func = MagicMock(return_value=3)
        traced_func = tracing.trace("TestTrace", func, log_return=True)

        result = traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {"return": 3}
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_dict(self):
        tracing = Tracing(self.tracer)

        func = MagicMock(return_value={"test_1": 3, "test_2": 6})
        traced_func = tracing.trace("TestTrace", func, log_return=True)

        result = traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {"return.test_1": 3, "return.test_2": 6}
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_list(self):
        tracing = Tracing(self.tracer)

        func = MagicMock(return_value={"test_1": 3, "test_2": [1, 2, 3]})
        traced_func = tracing.trace("TestTrace", func, log_return=True)

        result = traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {"return.test_1": 3, "return.test_2.0": 1, "return.test_2.1": 2, "return.test_2.2": 3}
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_num_key(self):
        tracing = Tracing(self.tracer)

        func = MagicMock(return_value={3: 3, "test_2": [1, 2, 3]})
        traced_func = tracing.trace("TestTrace", func, log_return=True)

        result = traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {"return.3": 3, "return.test_2.0": 1, "return.test_2.1": 2, "return.test_2.2": 3}
        self.assertDictEqual(correct, logs[0].key_values)
    
    def test_log_return_tuple_key(self):
        tracing = Tracing(self.tracer)

        func = MagicMock(return_value={(1, 1): 3, "test_2": [1, 2, 3]})
        traced_func = tracing.trace("TestTrace", func, log_return=True)

        result = traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {"return.(1, 1)": 3, "return.test_2.0": 1, "return.test_2.1": 2, "return.test_2.2": 3}
        self.assertDictEqual(correct, logs[0].key_values)

    def test_log_return_object_key(self):
        tracing = Tracing(self.tracer)

        test_object = MockTracer()

        func = MagicMock(return_value={test_object: "Hello"})
        traced_func = tracing.trace("TestTrace", func, log_return=True)

        result = traced_func()

        logs = self.tracer.finished_spans()[0].logs

        correct = {f"return.{str(test_object)}": "Hello"}
        self.assertDictEqual(correct, logs[0].key_values)