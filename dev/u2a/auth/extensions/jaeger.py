from auth.extensions.flask import app
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from auth.core.config import JAEGER_AGENT_HOST, JAEGER_AGENT_PORT
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from functools import wraps
from auth.core.config import JAEGER_REQUEST_ID_MODE
from flask import request, has_request_context
import secrets

REQUEST_ID_HEADER = 'X-Request-Id'
REQUEST_ID_ATTRIBUTE = 'http.request_id'
AUTH_SERVICE_NAME_IN_JAEGER = 'auth'


def configure_tracer() -> None:
    resource = Resource(attributes={SERVICE_NAME: AUTH_SERVICE_NAME_IN_JAEGER})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=JAEGER_AGENT_HOST,
                agent_port=JAEGER_AGENT_PORT,
                udp_split_oversized_batches=True
            )
        )
    )
    if JAEGER_REQUEST_ID_MODE == 0:
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(
                    ConsoleSpanExporter(service_name=AUTH_SERVICE_NAME_IN_JAEGER)
            )
        )


def _request_id():
    if has_request_context():
        return request.headers.get(REQUEST_ID_HEADER, secrets.token_hex(16))
    return secrets.token_hex(16)


def _tracer():
    return app.tracer if hasattr(app, 'tracer') else None


def request_hook(span, environ):
    if span and span.is_recording():
        span.set_attribute(REQUEST_ID_ATTRIBUTE, _request_id())


def jaeger_init():
    configure_tracer()
    FlaskInstrumentor().instrument_app(
        app,
        request_hook=request_hook,
        excluded_urls='/auth/openapi'
    )

    def jaeger_before_request():
        if JAEGER_REQUEST_ID_MODE == 1:
            if request.headers.get('X-Request-Id') is None:
                raise RuntimeError('request id is required')
    app.execute_before_request.append(jaeger_before_request)

    return trace.get_tracer('auth-via-decorator')


def jaeger_tracing(
    get_tracer=_tracer,
    get_request_id=_request_id
):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            rid, tracer = get_request_id(), get_tracer()
            with tracer.start_as_current_span(name=func.__name__) as span:
                span.set_attribute(REQUEST_ID_ATTRIBUTE, rid)
                return func(*args, **kwargs)
        return inner
    return wrapper
