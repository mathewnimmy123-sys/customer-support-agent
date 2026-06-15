import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Vertex AI Customer Support Agent Service",
    description="Production-grade runtime wrapper for multi-agent workflows.",
    version="1.0.0"
)

class AgentQuery(BaseModel):
    text: str
    session_id: str = "default-session"

@app.get("/")
def read_root():
    return {
        "status": "Healthy",
        "service": "customer-support-agent-service",
        "runtime": "Python 3.11-slim"
    }

@app.get("/healthz")
def health_check():
    return {"status": "OK"}

@app.post("/chat")
async def chat_with_agent(query: AgentQuery):
    try:
        # Simple placeholder return to guarantee structural compile success
        return {"response": f"Received query: {query.text}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Launching Server on host 0.0.0.0 binding to port {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
