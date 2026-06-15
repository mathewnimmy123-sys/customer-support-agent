# server.py
import uvicorn
from google.adk.cli.fast_api import create_api_app
from support_agent.supervisor import customer_support_supervisor  # fixed: was bare import
 
app = create_api_app(agents=[customer_support_supervisor])
 
if __name__ == "__main__":
    print("--- Launching ADK Server ---")
    uvicorn.run(app, host="127.0.0.1", port=8000)