# support_agent/agent.py
import os
import time
import logging
from typing import List

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
PROJECT_ID = os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "gci-techss-gcp-pjnp-01nl165115")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://bigquery.googleapis.com/mcp")

# log &ob
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("customer_support_agent")
logger.info(f"🚀 Initializing Support Agent Ecosystem for Project: {PROJECT_ID}")

# imports
import google.auth
import google.auth.transport.requests
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

# met
class AgentMetricsTracker:
    """Tracks operational performance metrics and transaction telemetry."""
    def __init__(self):
        self.invocation_count = 0
        self.total_execution_time = 0.0
        self.last_start_time = 0.0

    def record_transaction(self, duration: float):
        self.invocation_count += 1
        self.total_execution_time += duration
        average_latency = self.total_execution_time / self.invocation_count
        logger.info(
            f"📊 [METRICS UPDATE] Invocation #{self.invocation_count} "
            f"| Latency: {duration:.2f}s | Avg Latency: {average_latency:.2f}s"
        )

metrics = AgentMetricsTracker()

# mcp
def get_mcp_toolset_direct() -> List[MCPToolset]:
    """Establishes authenticated transport to the BigQuery MCP server gateway."""
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
        logger.info(f"✅ [OBSERVABILITY] MCP handshakes established in {connection_time:.2f}s")
        return [toolset]
        
    except Exception as e:
        logger.error(f"❌ Critical Failure connecting to MCP: {str(e)}", exc_info=True)
        return []

# 5
def before_agent_callback(callback_context: CallbackContext):
    """Observability Hook: Executed right before Gemini processes a request."""
    metrics.last_start_time = time.time()
    
    # S
    user_id = 'unknown_user'
    if hasattr(callback_context, 'session') and callback_context.session:
        user_id = getattr(callback_context.session, 'user_id', 'unknown_user')
    elif hasattr(callback_context, 'user_id'):
        user_id = callback_context.user_id
        
    logger.info(f"📥 [OBSERVABILITY] Processing incoming prompt stream for User: {user_id}")

def after_agent_callback(callback_context: CallbackContext):
    """Observability Hook: Executed immediately after Gemini finishes processing."""
    start_time = metrics.last_start_time if metrics.last_start_time > 0 else time.time()
    duration = time.time() - start_time
    
    # S
    metrics.record_transaction(duration)
    
    session_id = 'active_session'
    if hasattr(callback_context, 'session') and callback_context.session:
        session_id = getattr(callback_context.session, 'id', 'active_session')
    elif hasattr(callback_context, 'session_id'):
        session_id = callback_context.session_id
        
    logger.info(f"📤 [OBSERVABILITY] Completed prompt execution stream for Session: {session_id}")

#  6
root_agent = Agent(
    name="customer_support_agent",
    description=(
        f"You are an enterprise customer support assistant connected directly to BigQuery via "
        f"Model Context Protocol rules. Always invoke your data warehouse tools to pull order statuses "
        f"or logistics records. Current active project domain context: {PROJECT_ID}."
    ),
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    tools=get_mcp_toolset_direct(),
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)