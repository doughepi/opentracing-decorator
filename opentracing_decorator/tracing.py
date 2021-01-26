import functools
import inspect
import numbers
import json

from typing import List

import opentracing
from opentracing import Span

from flatten_dict import flatten


class Tracing:
    def __init__(
        self,
        tracer: opentracing.Tracer = None,
    ):

        if not tracer:
            self.tracer = opentracing.tracer
        else:
            self.tracer = tracer

    def _safe_convert(self, dikt):
        return json.loads(json.dumps(dikt, default=str))

    def _dict_to_tag(self, span: Span, dikt: dict) -> None:
        for key, value in dikt.items():
            span.set_tag(key, value)

    def _map_parameters(
        self, func: callable, *args: List[any], **kwargs: dict[str, any]
    ) -> dict[str, any]:
        bound_arguments: inspect.BoundArguments = inspect.signature(func).bind(
            *args, **kwargs
        )
        bound_arguments.apply_defaults()
        parameters = {
            key: value
            for key, value in bound_arguments.arguments.items()
            if key != "self"
        }
        parameters = self._safe_convert(parameters)
        return parameters

    def _flatten_dict(self, dikt: dict[str, any], reducer) -> dict[str, any]:
        return flatten(dikt, reducer=reducer, enumerate_types=(list,))

    def _tag_parameters(
        self, span: Span, parameter_prefix, flatten_parameters, parameter_reducer, func: callable, *args: List[any], **kwargs: dict[str, any]
    ) -> None:
        mapped_parameters = self._map_parameters(func, *args, **kwargs)
        if flatten_parameters:
            mapped_parameters = self._flatten_dict(mapped_parameters, reducer=parameter_reducer)
        self._dict_to_tag(span, flattened_parameters)

    def _log_return(self, span: Span, return_prefix, flatten_return, return_reducer, value: any):
        return_log = {return_prefix: value}
        if flatten_return:
            return_log = self._flatten_dict(return_log, reducer=return_reducer)
        return_log = self._safe_convert(return_log)
        span.log_kv(return_log)

    def trace(
        self,
        operation_name: str,
        func=None,
        *,
        pass_span: bool = False,
        tag_parameters: bool = False,
        parameter_prefix: str = None,
        flatten_parameters: bool = True,
        parameter_reducer: str = 'dot',
        log_return: bool = False,
        return_prefix: str = "return",
        flatten_return: bool = True,
        return_reducer: str = 'dot',
    ) -> None:
        """Decorate a function for tracing.

        Args:
            pass_span (bool, optional): Pass the active span as a
                parameter to the function. Defaults to False.
            tag_parameters (bool, optional): Automatically tag the span with
                the names and values of the function's paramters. Defaults to False.
            log_return (bool, optional): Automatically log the return
                 value of the function to the span. Defaults to False.
        """
        if func is None:
            func = functools.partial(
                self.trace,
                pass_span=pass_span,
                tag_parameters=tag_parameters,
                parameter_prefix=parameter_prefix,
                flatten_parameters=flatten_parameters,
                parameter_reducer=parameter_reducer,
                log_return=log_return,
                return_prefix=return_prefix,
                flatten_return=flatten_return,
                return_reducer=return_reducer,
            )

        @functools.wraps(func)
        def wrapper_trace(*args, **kwargs):
            with self.tracer.start_active_span(operation_name) as scope:
                span = scope.span

                if pass_span:
                    kwargs["span"] = span

                if tag_parameters:
                    self._tag_parameters(span, parameter_prefix, flatten_parameters, parameter_reducer, func, *args, **kwargs)

                value = func(*args, **kwargs)

                if log_return:
                    self._log_return(span, return_prefix, flatten_return, return_reducer, value)

            return value

        return wrapper_trace
