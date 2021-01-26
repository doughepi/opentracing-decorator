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
