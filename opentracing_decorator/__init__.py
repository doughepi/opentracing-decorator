from .__version__ import __description__, __title__, __version__
from .tracing import Tracing

__all__ = ["__title__", "__description__", "__version__", "Tracing"]

__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        setattr(__locals[__name], "__module__", "opentracing_decorator")  # noqa
