# deploy.py
import logging
from google.cloud import aiplatform
from vertexai.preview import reasoning_engines

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PROJECT_ID     = "gci-techss-gcp-pjnp-01nl165115"
LOCATION       = "us-central1"
STAGING_BUCKET = "gs://gci-techss-gcp-pjnp-01nl165115-adk-staging"

log.info("Initialising Vertex AI connection metrics...")
aiplatform.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# FIX: Import directly from your project's support_agent directory
from support_agent.agent import SimpleSupportAgent

log.info("Triggering Agent Engine structural creation pass...")
remote = reasoning_engines.ReasoningEngine.create(
    reasoning_engine=SimpleSupportAgent,
    requirements=[
        "google-cloud-aiplatform[reasoningengine]==1.71.1",
        "pydantic>=2.10.0,<3.0.0"
    ],
    extra_packages=["support_agent"], # Packages the entire support_agent directory cleanly
    display_name="customer-support-agent",
    description="Production support agent via automated CI/CD pipeline."
)

log.info("🔥 SUCCESS — Resource Deployed: %s", remote.resource_name)