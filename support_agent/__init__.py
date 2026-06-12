# support_agent/__init__.py
import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_engine")

PROJECT_ID = "gci-techss-gcp-pjnp-01nl165115"

# Initialize OpenTelemetry immediately inside the execution wrapper
try:
    from opentelemetry.exporter.gcp.trace import CloudTraceSpanExporter
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(CloudTraceSpanExporter(project_id=PROJECT_ID)))
    trace.set_tracer_provider(provider)
    logger.info("[OTel] OpenTelemetry CloudTraceSpanExporter successfully initialized.")
except Exception as e:
    logger.warning("[OTel] Telemetry tracking initialization deferred: %s", e)

class SimpleSupportAgent:
    """Production-grade interface conforming to Vertex AI requirements."""
    def set_up(self):
        logger.info("Initializing Agent Core Infrastructure...")
        
    def query(self, input: dict, **kwargs):
        tracer = trace.get_tracer("support_agent")
        with tracer.start_as_current_span("agent_execution_runtime") as span:
            span.set_attribute("gcp.project_id", PROJECT_ID)
            user_msg = input.get("input", "Hello")
            logger.info("Processing user query via pipeline: %s", user_msg)
            return {"content": f"System Live. Echoing input: {user_msg}"}

# Expose the direct object reference for the deployment pipeline
agent = SimpleSupportAgent()