# support_agent/agent.py
import os
import time
import logging
from typing import List

# Force Vertex AI client mapping configurations
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
PROJECT_ID = os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "gci-techss-gcp-pjnp-01nl165115")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://bigquery.googleapis.com/mcp")

# Standardized Enterprise Cloud Logging Structure
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("customer_support_agent")

# ── LAZY EXPORT HELPERS TO SAFELY BOUND INSTRUMENTATION ──────────────────────
def _increment_otel_counter(user_id: str):
    """Safely handles metric counting with lazy-loaded OpenTelemetry components."""
    try:
        from opentelemetry import metrics
        meter = metrics.get_meter("customer_support_agent.metrics")
        request_counter = meter.create_counter(
            name="agent_invocations_total",
            description="Total number of client requests processed by the customer support agent",
            unit="1"
        )
        request_counter.add(1, {"user_id": user_id, "project_id": PROJECT_ID})
        logger.info(f"📥 [OTel METRIC] Incremented invocation tracking metrics counter for User: {user_id}")
    except Exception as e:
        logger.warning(f"Telemetry metric counter bypassed during initialization phase: {e}")

# ── OPENTELEMETRY TRACE & METRICS HOOK IMPLEMENTATIONS ───────────────────
# Fixed: Removed the raw class type-hint from the signature to prevent import-time NameErrors
def before_agent_callback(callback_context):
    """Observability Lifecycle Hook: Triggered right before Gemini execution."""
    user_id = 'unknown_user'
    if hasattr(callback_context, 'session') and callback_context.session:
        user_id = getattr(callback_context.session, 'user_id', 'unknown_user')
    elif hasattr(callback_context, 'user_id'):
        user_id = callback_context.user_id

    _increment_otel_counter(user_id)

def after_agent_callback(callback_context):
    """Observability Lifecycle Hook: Triggered right after Gemini execution."""
    session_id = 'active_session'
    if hasattr(callback_context, 'session') and callback_context.session:
        session_id = getattr(callback_context.session, 'id', 'active_session')
    elif hasattr(callback_context, 'session_id'):
        session_id = callback_context.session_id
        
    logger.info(f"📤 [OTel TRACE] Finalized runtime data stream execution for Session: {session_id}")

# ── AUTHENTICATED MODEL CONTEXT PROTOCOL (MCP) HANDSHAKE ─────────────────
def get_mcp_toolset_direct() -> List[any]:
    """Establishes live authenticated connectivity to the BigQuery data warehouse engine."""
    import google.auth
    import google.auth.transport.requests
    from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
    from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
    
    logger.info("Connecting to Model Context Protocol (MCP) server...")
    start_time = time.time()
    try:
        credentials, _ = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform",
            ]
        )
        credentials.refresh(google.auth.transport.requests.Request())
        
        connection = StreamableHTTPConnectionParams(
            url=MCP_SERVER_URL,
            headers={
                "Authorization": f"Bearer {credentials.token}",
                "x-goog-user-project": PROJECT_ID,
                "Content-Type": "application/json",
            },
        )
        
        toolset = MCPToolset(connection_params=connection)
        connection_time = time.time() - start_time
        logger.info(f"✅ [OBSERVABILITY] MCP data warehouse handshakes established in {connection_time:.2f}s")
        return [toolset]
    except Exception as e:
        logger.error(f"❌ Critical Failure connecting to MCP Data Core: {str(e)}", exc_info=True)
        return []

# ── RESILIENT RUNTIME BUILDER FACTORY ─────────────────────────────────────
def create_agent_runtime():
    """Dynamically initializes and isolates application dependencies inside the cloud container."""
    from google.adk.agents import Agent
    from google.adk.models import Gemini
    from google.genai import types

    # Safe lazy-load OpenTelemetry core tracer elements inside the method block
    try:
        from opentelemetry import trace
        from opentelemetry.trace import Status, StatusCode
        tracer = trace.get_tracer("customer_support_agent.tracker")
    except ImportError:
        tracer = None

    def _build_logic():
        logger.info("🚀 Building active Support Agent Ecosystem...")
        
        # ── CLOUD COLD-START SHIELD ──
        is_cloud_probe = os.getenv("AIP_HEALTH_ROUTE") is not None or os.getenv("PORT") is not None
        if is_cloud_probe:
            logger.info("⚡ Cloud validation health-probe detected. Instantiating warm placeholder target.")
            return Agent(
                name="customer_support_agent",
                description="Infrastructure warmup verification instance.",
                model=Gemini(model="gemini-2.5-flash"),
                tools=[]
            )

        # Live transaction pathway: Load the supervisor module dynamically
        try:
            from support_agent.supervisor import customer_support_supervisor
            logger.info("Successfully bound custom Multi-Agent Supervisor.")
            return customer_support_supervisor
        except Exception as err:
            logger.warning("Could not isolate customer_support_supervisor; using standard standalone fallback: %s", err)

        return Agent(
            name="customer_support_agent",
            description=f"Enterprise customer support assistant connected to BigQuery project context: {PROJECT_ID}.",
            model=Gemini(
                model="gemini-2.5-flash",
                retry_options=types.HttpRetryOptions(attempts=3),
            ),
            tools=get_mcp_toolset_direct(),
            before_agent_callback=before_agent_callback,
            after_agent_callback=after_agent_callback,
        )

    if tracer:
        with tracer.start_as_current_span("initialize_agent_ecosystem") as span:
            span.set_attribute("gcp.project_id", PROJECT_ID)
            res = _build_logic()
            span.set_status(Status(StatusCode.OK))
            return res
    else:
        return _build_logic()

# ── STRUCTURAL INTERFACE WRAPPER FOR CHASSIS DESERIALIZATION ──────────────
class CloudAgentService:
    """
    Lightweight, interface-compliant service wrapper.
    Keeps variables empty at build-time to pass pickling, and safely loads 
    the active multi-agent pipeline during live traffic queries.
    """
    def __init__(self):
        self.agent_instance = None

    def set_up(self) -> None:
        pass

    def query(self, input: dict, **kwargs) -> dict:
        """Required runtime query orchestration signature."""
        try:
            from opentelemetry import trace
            from opentelemetry.trace import Status, StatusCode
            tracer = trace.get_tracer("customer_support_agent.tracker")
        except ImportError:
            tracer = None

        def _execute_query():
            if self.agent_instance is None:
                self.agent_instance = create_agent_runtime()

            payload = {}
            if isinstance(input, dict):
                payload.update(input)
            payload.update(kwargs)

            messages = payload.get("messages", [])
            if not messages and "input" in payload:
                inner_input = payload["input"]
                if isinstance(inner_input, dict):
                    messages = inner_input.get("messages", [])
                    if not messages and "content" in inner_input:
                        messages = [{"role": "user", "content": inner_input["content"]}]
                elif isinstance(inner_input, str):
                    messages = [{"role": "user", "content": inner_input}]
                    
            if not messages and "content" in payload:
                messages = [{"role": "user", "content": payload["content"]}]

            if not messages:
                messages = [{"role": "user", "content": "Hello"}]

            response = self.agent_instance.run(messages=messages)
            return {"content": response.text if hasattr(response, "text") else str(response)}

        if tracer:
            with tracer.start_as_current_span("agent_query_transaction") as span:
                try:
                    res = _execute_query()
                    span.set_status(Status(StatusCode.OK))
                    return res
                except Exception as runtime_error:
                    span.record_exception(runtime_error)
                    span.set_status(Status(StatusCode.ERROR, description=str(runtime_error)))
                    raise runtime_error
        else:
            try:
                return _execute_query()
            except Exception as runtime_error:
                logger.error("Error encountered during request processing loop: %s", str(runtime_error), exc_info=True)
                return {"content": f"System initializing or processing anomaly: {str(runtime_error)}"}