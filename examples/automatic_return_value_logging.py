import time

from jaeger_client import Config

from opentracing_decorator import Tracing

# No sampler host and port specified because the Jaeger client picks localhost:6831 by default.
config = Config(
    config={
        "sampler": {
            "type": "const",  # Not advised to have constant sampling in production.
            "param": 1,
        },
        "logging": True,
    },
    service_name="example-service",
    validate=True,
)
jaeger_tracer = config.initialize_tracer()

# Pass in an instance of a tracer implementation.
# Here, we're using the Jaeger client.
tracing = Tracing(tracer=jaeger_tracer)

# Decorate functions with the @tracing.trace decorator and an operation_name.
@tracing.trace(operation_name="GetTime", log_return=True)
def get_time():
    return time.time()


if __name__ == "__main__":
    print(get_time())

    # Give some time to report traces.
    time.sleep(5)
    jaeger_tracer.close()
