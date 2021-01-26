import functools
import inspect
import json
from typing import Any, Callable, Dict, Optional

import opentracing
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

    def _safe_convert(self, dikt: Dict[Any, Any]) -> Dict[Any, Any]:
        return json.loads(json.dumps(dikt, default=str))

    def _dict_to_tag(self, span: opentracing.Span, dikt: Dict[Any, Any]) -> None:
        if not isinstance(dikt, dict):
            raise TypeError()
        if dikt:
            for key, value in dikt.items():
                span.set_tag(key, value)

    def _map_parameters(self, func: Callable, *args: Any, **kwargs: Any) -> Dict[Any, Any]:
        bound_arguments = inspect.signature(func).bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        return {key: value for key, value in bound_arguments.arguments.items() if key != "self"}

    def _flatten_dict(self, dikt: Dict[Any, Any], reducer: str = "dot") -> Dict[Any, Any]:
        return flatten(dikt, reducer=reducer, enumerate_types=(list,))

    def _tag_parameters(
        self,
        span: opentracing.Span,
        func: Callable,
        *args: Any,
        parameter_prefix: str = None,
        flatten_parameters: bool = True,
        parameter_reducer: str = "dot",
        **kwargs: Any,
    ) -> None:
        mapped_parameters = self._map_parameters(func, *args, **kwargs)
        if parameter_prefix:
            mapped_parameters = {parameter_prefix: mapped_parameters}
        if flatten_parameters:
            mapped_parameters = self._flatten_dict(mapped_parameters, reducer=parameter_reducer)
        mapped_parameters = self._safe_convert(mapped_parameters)
        self._dict_to_tag(span, mapped_parameters)

    def _log_return(
        self,
        span: opentracing.Span,
        value: Any,
        return_prefix: str = "return",
        flatten_return: bool = True,
        return_reducer: str = "dot",
    ) -> None:
        return_log = {return_prefix: value}
        if flatten_return:
            return_log = self._flatten_dict(return_log, reducer=return_reducer)
        return_log = self._safe_convert(return_log)
        span.log_kv(return_log)

    def trace(
        self,
        operation_name: str,
        func: Optional[Callable] = None,
        *,
        pass_span: bool = False,
        tag_parameters: bool = False,
        parameter_prefix: str = None,
        flatten_parameters: bool = True,
        parameter_reducer: str = "dot",
        log_return: bool = False,
        return_prefix: str = "return",
        flatten_return: bool = True,
        return_reducer: str = "dot",
    ) -> Callable:
        if func is None:
            func = functools.partial(
                self.trace,
                operation_name,
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
        def wrapper_trace(*args: Any, **kwargs: Any) -> Any:
            with self.tracer.start_active_span(operation_name) as scope:
                span = scope.span

                if pass_span:
                    kwargs["span"] = span

                assert func is not None

                if tag_parameters:
                    self._tag_parameters(
                        span,
                        func,
                        *args,
                        parameter_prefix=parameter_prefix,
                        flatten_parameters=flatten_parameters,
                        parameter_reducer=parameter_reducer,
                        **kwargs,
                    )

                value = func(*args, **kwargs)

                if log_return:
                    self._log_return(
                        span,
                        value,
                        return_prefix=return_prefix,
                        flatten_return=flatten_return,
                        return_reducer=return_reducer,
                    )

                return value

        return wrapper_trace
