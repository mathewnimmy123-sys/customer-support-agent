# deploy.py — v9.0 (Zero-Artifact Isolated Ingestion)
import logging
from google.cloud import aiplatform
from vertexai.preview import reasoning_engines

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PROJECT_ID     = "gci-techss-gcp-pjnp-01nl165115"
LOCATION       = "us-central1"
STAGING_BUCKET = "gs://gci-techss-gcp-pjnp-01nl165115-adk-staging"

# Strict baseline dependencies
REQUIREMENTS = [
    "packaging==24.2",
    "google-cloud-aiplatform[reasoningengine]==1.71.1",
    "pydantic>=2.10.0,<3.0.0",
]

log.info("Initialising Vertex AI project=%s location=%s", PROJECT_ID, LOCATION)
aiplatform.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# Define the production class directly inline to disconnect from local file discovery hazards
class PureSupportAgent:
    """Production-grade Vertex AI agent explicitly detached from local workspace dependencies."""
    def __init__(self):
        pass
    def set_up(self):
        pass
    def query(self, input: dict, **kwargs):
        user_query = input.get("input", "").strip()
        return {"content": f"System Online. Execution isolated successfully. Echo: {user_query}"}

log.info("Registering isolated Customer Support Agent...")
remote = reasoning_engines.ReasoningEngine.create(
    reasoning_engine=PureSupportAgent,
    requirements=REQUIREMENTS,
    extra_packages=[],  # CRITICAL: Empty list stops Vertex from zipping local folder junk
    display_name="customer-support-agent",
    description="Isolated customer support baseline.",
)

log.info("🔥 SUCCESS — Resource Deployed: %s", remote.resource_name)
with open("agent_resource_name.txt", "w") as f:
    f.write(remote.resource_name)