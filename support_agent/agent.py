<<<<<<< HEAD
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
=======
# support_agent/agent.py — v8.0 (Telemetry Deferred Pass)
import os
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("customer_support_agent")

# support_agent/agent.py
# support_agent/agent.py

class SimpleSupportAgent:
    def __init__(self): 
        pass
        
    def set_up(self): 
        pass
        
    def query(self, input_data, **kwargs):
        user_msg = input_data.get("input", "Hello")
        return {"content": f"Customer Support Agent Live. Processing input: {user_msg}"}

# Create the instance object that deploy.py imports
agent = SimpleSupportAgent()
>>>>>>> 2616edf286dd2289307638b8f52d8462f431fc03
