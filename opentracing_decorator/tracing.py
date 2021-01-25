import functools

import opentracing

from opentracing_decorator.parameter_tagger import ParameterTagger


class Tracing:
    def __init__(self, tracer: opentracing.Tracer = None):
        self.tracer = tracer

    @property
    def tracer(self) -> opentracing.Tracer:
        """Get the underlying tracer.

        Returns:
            opentracing.Tracer: The underlying opentracing.Tracer instance.
        """
        return self.tracer or opentracing.tracer

    @tracer.setter
    def tracer(self, value: opentracing.Tracer) -> None:
        """Set the underlying tracer.

        Args:
            value (opentracing.Tracer): The underlying opentracing.Tracer instance.
        """
        self._tracer = value

    def trace(
        self,
        operation_name: str,
        func=None,
        *,
        pass_span: bool = False,
        tag_parameters: bool = False,
        parameter_prefix: str = None,
        log_return: bool = False,
        reducer: str = "dot",
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
                log_return=log_return,
                reducer=reducer,
            )

        @functools.wraps(func)
        def wrapper_trace(*args, **kwargs):
            with self.tracer.start_active_span(operation_name) as scope:
                span = scope.span

                if tag_parameters:
                    parameter_tagger = ParameterTagger(parameter_prefix=parameter_prefix, reducer=reducer)
                    parameter_tagger.tag_parameters(span, func, *args, **kwargs)

                value = func(*args, **kwargs)

                if log_return:
                    span.log_kv({"return": value})

            return value

        return wrapper_trace
