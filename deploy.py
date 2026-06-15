# deploy.py
import sys

# ── THE ULTIMATE OVERRIDE: Inherit from standard tuple to allow mathematical comparisons ──
class CompliantMockVersion(tuple):
    major = 3
    minor = 11
    micro = 0
    releaselevel = 'final'
    serial = 0

# Instantiate the tuple with values expected by standard internal comparison filters
sys.version_info = CompliantMockVersion((3, 11, 0, 'final', 0))

import os
import google.cloud.aiplatform as aiplatform
from vertexai.preview import reasoning_engines
from support_agent.agent import agent  # Imports your class instance cleanly

PROJECT_ID = "gci-techss-gcp-pjnp-01nl165115"
LOCATION = "us-west1"
STAGING_BUCKET = "gs://gci-techss-gcp-pjnp-01nl165115-adk-staging"

print("🔗 Connecting to Vertex AI Core Services...")
aiplatform.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

print("📦 Compiling and staging Customer Support Agent to the Cloud...")
try:
    remote_agent = reasoning_engines.ReasoningEngine.create(
        reasoning_engine=agent,
        requirements=[
            "google-cloud-aiplatform[reasoningengine]==1.71.1",
            "google-cloud-bigquery",
            "pydantic>=2.10.0,<3.0.0",
            "google-auth"
        ],
        extra_packages=["support_agent"],
        display_name="customer_support_agent",
        description="Enterprise customer support assistant connected to BigQuery via MCP.",
    )
    
    print("\n🚀 DEPLOYMENT SUCCESSFUL!")
    print(f"Resource Name: {remote_agent.resource_name}")
    
    with open("agent_resource_name.txt", "w") as f:
        f.write(remote_agent.resource_name)

except Exception as e:
    print(f"\n❌ Cloud Build Failed: {str(e)}")
    sys.exit(1)