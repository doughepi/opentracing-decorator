import inspect

from typing import List

from flatten_dict import flatten
from opentracing import Span


class ParameterTagger:
    def __init__(self, parameter_prefix: str = None, reducer: str = "dot"):
        self.parameter_prefix = parameter_prefix
        self.reducer = reducer

    def _dict_to_tag(self, span: Span, dikt: dict) -> None:
        for key, value in dikt.items():
            span.set_tag(key, value)

    def _map_parameters(self, func: callable, *args: List[any], **kwargs: dict[str, any]) -> dict[str, any]:
        bound_arguments: inspect.BoundArguments = inspect.signature(func).bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        parameters = {key: value for key, value in bound_arguments.arguments.items() if key != "self"}
        if self.parameter_prefix:
            parameters = {self.parameter_prefix: parameters}
        return parameters

    def _flatten_parameters(self, parameters: dict[str, any]) -> dict[str, any]:
        return flatten(parameters, reducer=self.reducer, enumerate_types=(list,))

    def tag_parameters(self, span: Span, func: callable, *args: List[any], **kwargs: dict[str, any]) -> None:
        mapped_parameters = self._map_parameters(func, *args, **kwargs)
        flattened_parameters = self._flatten_parameters(mapped_parameters)
        self._dict_to_tag(span, flattened_params)
