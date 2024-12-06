import logging

from fastapi import FastAPI
import colorlog
from fastapi_booster.LifeSpanManager import lifespan
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# set up logging
logger = logging.getLogger("FasterAPI-Booster")
stream_handler = logging.StreamHandler()

# Define log colors
cformat = "%(log_color)s%(levelname)-10s%(reset)s%(log_color)s%(message)s"
colors = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white",
}

stream_formatter = colorlog.ColoredFormatter(cformat, log_colors=colors)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


class App(FastAPI):
    def __init__(self, name: str, otel_endpoint: str | None = None, *args, **kwargs):

        # Initialize the FastAPI app
        super().__init__(*args, **kwargs)

        # Set the lifespan
        self.lifespan = lifespan

        # Set up tracing
        trace_provider = TracerProvider(
            resource=Resource.create(attributes={"service.name": name})
        )
        logger.info(f"Tracing provider created for {name}")

        # Set up the OTLP exporter
        if otel_endpoint:
            if otel_endpoint.startswith("http"):
                exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True)
                logger.info(f"OTLP exporter created for {otel_endpoint}")
            else:
                exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=False)
                logger.info(f"OTLP exporter created for {otel_endpoint}")
        else:
            exporter = ConsoleSpanExporter()
            logger.info("Console exporter created")

        # Add the exporter to the trace provider
        trace_provider.add_span_processor(BatchSpanProcessor(exporter))
        logger.info("Span processor added")

        # Set the tracer provider for the app
        trace.set_tracer_provider(trace_provider)

        # Instrument the FastAPI app
        FastAPIInstrumentor.instrument_app(self)
        logger.info("FastAPI app instrumented")