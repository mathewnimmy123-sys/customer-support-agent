# support_agent/agent.py — v4.5
import os
import time
import logging
from typing import List, Any
 
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
 
PROJECT_ID     = os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "gci-techss-gcp-pjnp-01nl165115")
MCP_SERVER_URL = os.getenv(
    "MCP_SERVER_URL",
    "https://us-central1-aiplatform.googleapis.com/v1/projects/"
    "gci-techss-gcp-pjnp-01nl165115/locations/us-central1/"
    "registryMcpServers/bigquery-mcp-server",
)
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("customer_support_agent")
 
# ── OpenTelemetry bootstrap ───────────────────────────────────────────────────
def _setup_telemetry() -> None:
    try:
        from opentelemetry import trace, metrics
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
 
        # Cloud Trace exporter
        from opentelemetry.exporter.gcp.trace import CloudTraceSpanExporter
        tracer_provider = TracerProvider()
        tracer_provider.add_span_processor(
            BatchSpanProcessor(CloudTraceSpanExporter(project_id=PROJECT_ID))
        )
        trace.set_tracer_provider(tracer_provider)
 
        # Cloud Monitoring metrics exporter
        try:
            from opentelemetry.exporter.gcp.monitoring import CloudMonitoringMetricsExporter
            reader = PeriodicExportingMetricReader(
                CloudMonitoringMetricsExporter(project_id=PROJECT_ID),
                export_interval_millis=60_000,
            )
            metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
        except ImportError:
            pass   # monitoring exporter optional
 
        logger.info("[OTel] TracerProvider + CloudTraceSpanExporter registered for project %s", PROJECT_ID)
 
    except Exception as exc:
        logger.warning("[OTel] Telemetry setup skipped: %s", exc)
 
_setup_telemetry()
 
# ── OTel helpers (used in callbacks) ─────────────────────────────────────────
def _get_tracer():
    try:
        from opentelemetry import trace
        return trace.get_tracer("customer_support_agent.tracer")
    except Exception:
        return None
 
def _increment_counter(user_id: str) -> None:
    try:
        from opentelemetry import metrics
        meter   = metrics.get_meter("customer_support_agent.metrics")
        counter = meter.create_counter(
            name="agent_invocations_total",
            description="Total agent invocations",
            unit="1",
        )
        counter.add(1, {"user_id": user_id, "project_id": PROJECT_ID})
    except Exception as exc:
        logger.debug("[OTel] Counter skipped: %s", exc)
 
# ── ADK callbacks ─────────────────────────────────────────────────────────────
def before_agent_callback(callback_context) -> None:
    user_id = getattr(getattr(callback_context, "session", None), "user_id", "unknown")
    _increment_counter(user_id)
    logger.info("[OTel] before_agent_callback — user=%s", user_id)
 
def after_agent_callback(callback_context) -> None:
    session_id = getattr(getattr(callback_context, "session", None), "id", "unknown")
    logger.info("[OTel] after_agent_callback — session=%s", session_id)
 
# ── MCP toolset (lazy, cached) ────────────────────────────────────────────────
_toolset_cache: List[Any] = []
 
def get_mcp_toolset() -> List[Any]:
    if _toolset_cache:
        return _toolset_cache
    try:
        import google.auth
        import google.auth.transport.requests
        from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
        from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
 
        creds, _ = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ]
        )
        creds.refresh(google.auth.transport.requests.Request())
 
        toolset = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL,
                headers={
                    "Authorization": f"Bearer {creds.token}",
                    "x-goog-user-project": PROJECT_ID,
                    "Content-Type": "application/json",
                },
            )
        )
        _toolset_cache.append(toolset)
        logger.info("[MCP] Toolset initialised — %s", MCP_SERVER_URL)
    except Exception as exc:
        logger.warning("[MCP] Could not connect to MCP server: %s", exc)
    return _toolset_cache
 
# ── Agent factory ─────────────────────────────────────────────────────────────
def create_agent_runtime():
    from google.adk.agents import Agent
    tracer = _get_tracer()
 
    def _build():
        try:
            from support_agent.supervisor import customer_support_supervisor
            logger.info("Using multi-agent supervisor.")
            return customer_support_supervisor
        except Exception as err:
            logger.warning("Supervisor unavailable (%s); building standalone agent.", err)
 
        return Agent(
            name="customer_support_agent",
            description=f"Enterprise customer support assistant. Project: {PROJECT_ID}",
            model="gemini-2.5-flash",
            tools=get_mcp_toolset(),
            before_agent_callback=before_agent_callback,
            after_agent_callback=after_agent_callback,
        )
 
    if tracer:
        from opentelemetry.trace import Status, StatusCode
        with tracer.start_as_current_span("initialize_agent_ecosystem") as span:
            span.set_attribute("gcp.project_id", PROJECT_ID)
            result = _build()
            span.set_status(Status(StatusCode.OK))
            return result
    return _build()
 
# ── CloudAgentService — Reasoning Engine compatible wrapper ───────────────────
class CloudAgentService:
    """
    Vertex AI Reasoning Engine requires an object with:
      - set_up()  called once after the container starts
      - query()   called for every user request
    """
    def __init__(self):
        self._agent = None
 
    def set_up(self) -> None:
        logger.info("[CloudAgentService] set_up() — building agent...")
        self._agent = create_agent_runtime()
        logger.info("[CloudAgentService] set_up() complete.")
 
    def query(self, *, input: dict, **kwargs) -> dict:  # noqa: A002
        tracer = _get_tracer()
 
        def _run():
            if self._agent is None:
                self.set_up()
 
            messages = input.get("messages", [])
            if not messages:
                content = input.get("content") or input.get("input", "Hello")
                messages = [{"role": "user", "content": str(content)}]
 
            response = self._agent.run(messages=messages)
            return {"content": response.text if hasattr(response, "text") else str(response)}
 
        if tracer:
            from opentelemetry.trace import Status, StatusCode
            with tracer.start_as_current_span("agent_query") as span:
                try:
                    result = _run()
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as exc:
                    span.record_exception(exc)
                    span.set_status(Status(StatusCode.ERROR, description=str(exc)))
                    raise
        else:
            return _run()
 
# Instantiated at module level so deploy.py targeting discovers it cleanly
agent = CloudAgentService()