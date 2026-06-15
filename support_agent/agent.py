import os
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

# 1. Initialize Vertex AI safely using environment variables or defaults
PROJECT_ID = os.environ.get("GCP_PROJECT", "gci-techss-gcp-pjnp-01nl165115")
LOCATION = os.environ.get("GCP_LOCATION", "us-west1")

print(f"[Agent Init] Connecting to Vertex AI (Project: {PROJECT_ID}, Region: {LOCATION})...")
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def run_agent(text_query: str, session_id: str = "default-session") -> str:
    """
    Main orchestrator endpoint matching your FastAPI runtime wrapper.
    Processes the incoming text query and returns the agent's response.
    """
    print(f"[Agent Execution] Session {session_id} executing query: '{text_query}'")
    
    try:
        # 2. Define the core processing model
        # Using gemini-1.5-flash as a fast, production standard for agent tasks
        model = GenerativeModel("gemini-1.5-flash")
        
        # 3. Define the Agent's identity persona instructions
        system_instruction = (
            "You are an advanced Customer Support AI Agent. Assist users politely, "
            "accurately, and concisely. If they ask about order status, acknowledge "
            "their session tracker context."
        )
        
        # 4. Generate the live completion response
        response = model.generate_content(
            f"Context Session: {session_id}\nUser Query: {text_query}",
            generation_config={"temperature": 0.2},
            system_instruction=system_instruction
        )
        
        # 5. Extract and return the final text
        if response.text:
            return response.text.strip()
        else:
            return "Agent executed successfully but returned an empty response."
            
    except Exception as e:
        print(f"[Agent Execution Error] Failed to generate agent content: {str(e)}")
        # Pass the exact breakdown up to main.py's robust error logger
        raise e
