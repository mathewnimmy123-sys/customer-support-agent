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

# Import the clean file generated during the Cloud Build run step
from agent import SimpleSupportAgent

log.info("Triggering Agent Engine structural creation pass...")
remote = reasoning_engines.ReasoningEngine.create(
    reasoning_engine=SimpleSupportAgent,
    requirements="requirements.txt",
    extra_packages=["agent.py"],
    display_name="customer-support-agent",
    description="Production support agent via automated CI/CD pipeline."
)

log.info("🔥 SUCCESS — Resource Deployed: %s", remote.resource_name)