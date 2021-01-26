<p align="center"><strong>opentracing-decorator</strong> <em>- A Python decorator for OpenTracing trace generation.</em></p>

<p align="center">
<a href="https://github.com/doughepi/opentracing-decorator/actions">
    <img src="https://github.com/doughepi/opentracing-decorator/workflows/Test%20Suite/badge.svg" alt="Test Suite">
</a>
<a href="https://pypi.org/project/httpx/">
    <img src="https://badge.fury.io/py/opentracing-decorator.svg" alt="Package Version">
</a>
</p>

Opentracing Decorator is a small Python library that adds a convenient
decorator for generating OpenTracing traces. It works with any client
implementation that follows the OpenTracing standard.

**Note**: _Opentracing Decorator is in early beta. Use in production at your own risk. Although the library is small and quite stable, some bugs arising from edge cases should be expected._

---

Let's get started...

```python
import time

from jaeger_client import Config

from opentracing_decorator import Tracing

config = Config(
    config={},
    service_name="example-service",
    validate=True,
)
jaeger_tracer = config.initialize_tracer()

# Pass in an instance of a tracer implementation.
# Here, we're using the Jaeger client.
tracing = Tracing(tracer=jaeger_tracer)

# Decorate functions with the @tracing.trace decorator and an operation_name.
@tracing.trace(operation_name="AddNumbersTogether")
def do_some_work(x, y, z):
    time.sleep(1)
    return x + y + z


@tracing.trace(operation_name="CountUp")
def count_up_slowly(n):
    for i in range(1, n):
        print(f"At {i}.")
        print(do_some_work(i, 10, 20))


if __name__ == "__main__":
    print("Counting up slowly.")
    count_up_slowly(1000)
```

## Features

- Automatic Span tagging of function parameters (Opt-In).
- Automatic Span logging of function return values (Opt-In).
- Works with any OpenTracing compatible tracing client.
  - [Jaeger](https://www.jaegertracing.io/)
  - [Zipkin](https://zipkin.io/)

## Installation

Install with pip:

```shell
$ pip install opentracing-decorator
```

Opentracing Decorator requires Python 3.6+.

## Documentation

Project documentation is available at [https://doughepi.github.io/opentracing-decorator/](https://doughepi.github.io/opentracing-decorator/).

For a run-through of all the basics, head over to the [QuickStart](https://doughepi.github.io/opentracing-decorator/quickstart/).

The [Developer Interface](https://doughepi.github.io/opentracing-decorator/api/) provides a comprehensive API reference.

To learn more about the OpenTracing standards, check out [The OpenTracing Project](https://opentracing.io/)

## Contribute

If you want to contribute to Opentracing Decorator check out the [Contributing Guide](https://opentracing.io/contributing/) to learn how to start.

## Dependencies

The Opentracing Decorator project relies on these excellent libraries:

- `opentracing` - The no-op implementation of the OpenTracing standard.
- `flatten-dict` - To support some of the parameter tagging and return logging.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Opentracing Decorator is <a href="https://github.com/doughepi/opentracing-decorator/blob/main/LICENSE">MIT licensed</a> code. Designed & built in Minneapolis, MN. Used at General Mills.</i></p>
