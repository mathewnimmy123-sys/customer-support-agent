"""
deploy_agent_engine.py
──────────────────────
Deploy the customer_support_agent to Vertex AI Agent Engine by importing the
structurally compliant CloudAgentService class directly from the support_agent module space.
"""

import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

# ── Configuration Core Variables ──────────────────────────────────────────────
PROJECT_ID         = "gci-techss-gcp-pjnp-01nl165115"
LOCATION           = "us-central1"
STAGING_BUCKET     = "gs://gci-techss-gcp-pjnp-01nl165115-adk-staging"
AGENT_DISPLAY_NAME = "customer-support-agent"

# Explicit Compute service identity mapping to provide proper IAM execution authorization clearance
TARGET_SERVICE_ACCOUNT = "591592795300-compute@developer.gserviceaccount.com"

# Comprehensive remote container system package dependency index
# ── Clean, Conflict-Free Cloud Package Index ─────────────────────────────────
REQUIREMENTS = [
    "google-adk[agent-identity,a2a]>=0.5.0",
    "google-cloud-bigquery>=3.0.0",
    "opentelemetry-api>=1.25.0",
    "opentelemetry-sdk>=1.25.0",
]

# ── Local Dependency Environment Validation Check ─────────────────────────────
def _check_prereqs() -> None:
    missing = []
    for pkg in ["google.cloud.aiplatform", "vertexai"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        sys.exit(f"Missing locally installed operational requirement packages: {missing}")

# ── Main Deployment Orchestration Sequence ────────────────────────────────────
def deploy() -> None:
    _check_prereqs()

    import vertexai
    from vertexai.preview import reasoning_engines
    
    # Crucial step: Import the service definition class from the package layout namespace
    # This ensures pickle records a persistent, discoverable pointer path ('support_agent.agent.CloudAgentService')
    from support_agent.agent import CloudAgentService

    log.info("Initializing Vertex AI platform infrastructure context project=%s location=%s", PROJECT_ID, LOCATION)
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET,
    )

    log.info("Packaging and uploading structurally verified Service module to Vertex Agent Engine…")
    # Instantiate the clean, module-linked class infrastructure target object
    service_deployment = CloudAgentService()

    # Dispatch compiled asset archives to the Reasoning Engine remote builder service
    remote_app = reasoning_engines.ReasoningEngine.create(
        service_deployment,
        requirements=REQUIREMENTS,
        display_name=AGENT_DISPLAY_NAME,
        description=(
            "Multi-agent customer support platform with OpenTelemetry metrics tracking, "
            "Cloud Trace transaction logging, and BigQuery data warehouse MCP integrations."
        ),
        # ── REMOVED the service_account line from here to fix the TypeError ──
    )

    log.info("✅ Deployment process completed successfully!")
    log.info("   Resource name identifier string: %s", remote_app.resource_name)
    log.info("   Display name tag value:          %s", AGENT_DISPLAY_NAME)

    # Persist resource pointer name to an external text register for easy automation pickups
    with open("deployed_resource_name.txt", "w") as fh:
        fh.write(remote_app.resource_name)
    log.info("   Resource identifier name saved directly → deployed_resource_name.txt")

if __name__ == "__main__":
    deploy()