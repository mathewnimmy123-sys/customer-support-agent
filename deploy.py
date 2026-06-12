# deploy.py — v6.3 (Direct Instance Mapping)
import os
import sys
import logging
from google.cloud import aiplatform
from vertexai.preview import reasoning_engines

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# Guarantee local workspace modules are discoverable natively by the interpreter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ID     = "gci-techss-gcp-pjnp-01nl165115"
LOCATION       = "us-central1"
STAGING_BUCKET = "gs://gci-techss-gcp-pjnp-01nl165115-adk-staging"

REQUIREMENTS = [
    "packaging==24.2",
    "google-cloud-aiplatform[agent_engines,reasoningengine]==1.71.1",
    "google-adk[agent-identity,a2a]>=0.5.0",
    "mcp>=1.0.0",
    "google-cloud-bigquery>=3.0.0",
    "opentelemetry-api>=1.25.0,<2.0.0",
    "opentelemetry-sdk>=1.25.0,<2.0.0",
    "opentelemetry-exporter-gcp-trace>=1.5.0,<2.0.0",
    "google-auth>=2.0.0",
    "aiohttp>=3.10.0,<3.11.0",
    "pydantic>=2.10.0,<3.0.0",
]

log.info("Initialising Vertex AI project=%s location=%s", PROJECT_ID, LOCATION)
aiplatform.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

log.info("Directly importing initialized agent instance from support_agent layer...")
# Fetching the live object reference directly breaks any module path resolution ambiguity
from support_agent import agent as live_agent_instance

log.info("Registering Customer Support Agent object via direct instance mapping...")
remote = reasoning_engines.ReasoningEngine.create(
    reasoning_engine=live_agent_instance,
    requirements=REQUIREMENTS,
    display_name="customer-support-agent",
    description="Multi-agent customer support with OTel/Cloud Trace and BigQuery MCP.",
)

log.info("🔥 SUCCESS — Resource Deployed: %s", remote.resource_name)
with open("agent_resource_name.txt", "w") as f:
    f.write(remote.resource_name)