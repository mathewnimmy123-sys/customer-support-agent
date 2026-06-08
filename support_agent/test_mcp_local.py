import os
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "gci-techss-gcp-pjnp-01nl165115")

import asyncio
import google.auth
from google.adk.integrations.agent_registry import AgentRegistry
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

PROJECT_ID = "gci-techss-gcp-pjnp-01nl165115"
LOCATION   = "global"

BQ_MCP_SERVER_RESOURCE = (
    f"projects/{PROJECT_ID}/locations/global/mcpServers/"
    "agentregistry-00000000-0000-0000-5446-003f30936da5"
)

async def test():
    print("Step 1: Authenticating local environment...")
    credentials, project = google.auth.default()
    print(f"  Target Project Workspace: {project}")

    print("Step 2: Testing connection to Agent Registry MCP Server...")
    registry = AgentRegistry(project_id=PROJECT_ID, location=LOCATION)
    toolset  = registry.get_mcp_toolset(BQ_MCP_SERVER_RESOURCE)
    print(f"  ✅ Toolset wrapper loaded: {toolset}")

    print("Step 3: Compiling agent schema...")
    agent = Agent(
        name="bq_test_agent",
        description=(
            f"You are a helpful BigQuery assistant for GCP project '{PROJECT_ID}'. "
            f"When using any MCP tools, always pass project_id='{PROJECT_ID}' "
            f"and location='US' as default parameters unless told otherwise. "
            "You can list datasets, run SQL queries, and look up order or shipping statuses."
        ),
        model=Gemini(
            model="gemini-2.5-flash",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        tools=[toolset],
    )

    print("Step 4: Executing runner simulation...")
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="bq_test",
        user_id="test_user",
    )

    runner = Runner(
        agent=agent,
        app_name="bq_test",
        session_service=session_service,
    )

    # ── Correct way to pass a message — must be a Content object ────────────
    message = types.Content(
        role="user",
        parts=[types.Part(text=f"List all available BigQuery datasets in project {PROJECT_ID}.")]
    )

    print("\n--- Sending request over Model Context Protocol ---")
    try:
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=message,
        ):
            print(f"  [Event]: {type(event).__name__}")

            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        print(f"  [MCP Tool Call]: {part.function_call.name}")
                        print(f"  [MCP Tool Args]: {part.function_call.args}")

                    if hasattr(part, 'function_response') and part.function_response:
                        print(f"  [MCP Tool Response]: {part.function_response.response}")

                    if hasattr(part, 'text') and part.text:
                        print(f"  [Text]: {part.text}")

            if hasattr(event, 'is_final_response') and event.is_final_response():
                if hasattr(event, 'content') and event.content and event.content.parts:
                    print(f"\n✅ [Final Agent Response]:\n{event.content.parts[0].text}")

    except Exception as e:
        print(f"\n❌ Runner error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())