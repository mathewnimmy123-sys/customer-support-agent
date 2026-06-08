# server.py
import uvicorn
from google.adk.cli.fast_api import create_api_app
from supervisor import customer_support_supervisor

# We bypass auto-discovery by telling the app EXACTLY which agent object to use
app = create_api_app(agents=[customer_support_supervisor])

if __name__ == "__main__":
    print("\n--- Launching Explicit ADK Server ---")
    uvicorn.run(app, host="127.0.0.1", port=8000)