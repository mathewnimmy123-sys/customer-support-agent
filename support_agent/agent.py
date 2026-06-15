import os
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI safely
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
        # Define the Agent's identity persona instructions
        system_instruction = (
            "You are an advanced Customer Support AI Agent. Assist users politely, "
            "accurately, and concisely. If they ask about order status, acknowledge "
            "their session tracker context."
        )
        
        # FIX: Pass system_instruction here during Model Initialization
        model = GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        # Generate the live completion response cleanly
        response = model.generate_content(
            f"Context Session: {session_id}\nUser Query: {text_query}",
            generation_config={"temperature": 0.2}
        )
        
        # Extract and return the final text
        if response.text:
            return response.text.strip()
        else:
            return "Agent executed successfully but returned an empty response."
            
    except Exception as e:
        print(f"[Agent Execution Error] Failed to generate agent content: {str(e)}")
        raise e
