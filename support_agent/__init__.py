# support_agent/__init__.py — v6.4
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_engine")

PROJECT_ID = "gci-techss-gcp-pjnp-01nl165115"

# Initialize OpenTelemetry safely without blocking server initialization
_tracer = None
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.gcp.trace import CloudTraceSpanExporter
    
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(CloudTraceSpanExporter(project_id=PROJECT_ID)))
    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer("support_agent")
    logger.info("[OTel] OpenTelemetry CloudTraceSpanExporter initialized.")
except Exception as e:
    logger.warning("[OTel] Telemetry tracing deferred: %s", e)

class SimpleSupportAgent:
    """Production interface conforming exactly to Vertex AI specifications."""
    def set_up(self):
        logger.info("Initializing Agent Core Infrastructure...")
        
    def query(self, input: dict, **kwargs):
        global _tracer
        user_msg = input.get("input", "Hello")
        logger.info("Processing user query: %s", user_msg)
        
        if _tracer:
            with _tracer.start_as_current_span("agent_execution_runtime") as span:
                span.set_attribute("gcp.project_id", PROJECT_ID)
                return {"content": f"System Live. Echoing input: {user_msg}"}
        
        return {"content": f"System Live (Telemetry Bypassed). Echoing input: {user_msg}"}

# Expose the instance reference cleanly for the deployment runner
agent = SimpleSupportAgent()