# support_agent/agent.py
import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

try:
    from google.cloud.opentelemetry_instrumentation.cloud_trace import CloudTraceSpanExporter
    _cloud_trace_available = True
except ImportError:
    _cloud_trace_available = False

from google.adk.telemetry import setup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = "gci-techss-gcp-pjnp-01nl165115"
LOCATION   = "us-central1"

def _configure_telemetry() -> None:
    provider = TracerProvider()
    if _cloud_trace_available:
        exporter = CloudTraceSpanExporter(project_id=PROJECT_ID)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        logger.info("OpenTelemetry → Cloud Trace exporter registered.")
    else:
        logger.warning("google-cloud-opentelemetry not installed; spans will NOT be exported to Cloud Trace.")

    trace.set_tracer_provider(provider)
    try:
        setup.setup_telemetry()
        logger.info("ADK telemetry setup complete.")
    except Exception as exc:
        logger.warning("ADK telemetry setup raised: %s", exc)

_configure_telemetry()

from .supervisor import customer_support_supervisor
agent = customer_support_supervisor