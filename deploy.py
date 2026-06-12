# deploy.py — v8.0 (Clean Baseline Demo)
import os
import sys
import logging
from google.cloud import aiplatform
from vertexai.preview import reasoning_engines

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ID     = "gci-techss-gcp-pjnp-01nl165115"
LOCATION       = "us-central1"
STAGING_BUCKET = "gs://gci-techss-gcp-pjnp-01nl165115-adk-staging"

# Clean baseline dependencies completely free of native binary/telemetry compile blocks
REQUIREMENTS = [
    "packaging==24.2",
    "google-cloud-aiplatform[reasoningengine]==1.71.1",
    "google-cloud-bigquery>=3.0.0",
    "pydantic>=2.10.0,<3.0.0",
]

log.info("Initialising Vertex AI project=%s location=%s", PROJECT_ID, LOCATION)
aiplatform.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

log.info("Importing Class Definition from support_agent...")
from support_agent.agent import SimpleSupportAgent

log.info("Registering Customer Support Agent using clean baseline class ingestion...")
remote = reasoning_engines.ReasoningEngine.create(
    reasoning_engine=SimpleSupportAgent,
    requirements=REQUIREMENTS,
    display_name="customer-support-agent",
    description="Multi-agent customer support base with BigQuery integration.",
)

log.info("🔥 SUCCESS — Resource Deployed: %s", remote.resource_name)
with open("agent_resource_name.txt", "w") as f:
    f.write(remote.resource_name)