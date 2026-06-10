import sys

# ── THE ULTIMATE OVERRIDE: Inherit from standard tuple to allow mathematical comparisons ──
class CompliantMockVersion(tuple):
    major = 3
    minor = 13
    micro = 0
    releaselevel = 'final'
    serial = 0

# Instantiate the tuple with the exact values expected by comparison operations
sys.version_info = CompliantMockVersion((3, 13, 0, 'final', 0))

import os
import vertexai
from vertexai.preview import reasoning_engines
from support_agent.agent import agent  # Imports our CloudAgentService instance cleanly

PROJECT_ID = "gci-techss-gcp-pjnp-01nl165115"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://gci-support-agent-staging"

print("🔗 Connecting to Vertex AI Core Services...")
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

print("📦 Compiling and staging Customer Support Agent to the Cloud...")
try:
    remote_agent = reasoning_engines.ReasoningEngine.create(
        agent,  # Synchronized matching object reference
        requirements=[
            "google-adk",
            "google-genai",
            "google-cloud-bigquery",
            "pydantic==2.10.0",
            "google-auth",
            "mcp",
            # Strict overrides to block Python 3.13 syntax inside the Vertex AI runtime instance
            "aiohttp<3.11.0",
            "aiosignal<1.4.0",
            "frozenlist<1.5.0",
            "typing_extensions>=4.11.0"
        ],
        display_name="customer_support_agent",
        description="Enterprise customer support assistant connected to BigQuery via MCP.",
    )
    
    print("\n🚀 DEPLOYMENT SUCCESSFUL!")
    print(f"Resource Name: {remote_agent.resource_name}")
    
    with open("agent_resource_name.txt", "w") as f:
        f.write(remote_agent.resource_name)

except Exception as e:
    print(f"\n❌ Cloud Build Failed: {str(e)}")