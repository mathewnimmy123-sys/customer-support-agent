import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from support_agent.agent import run_agent

app = FastAPI(title="Customer Support Agent Service")

class ChatRequest(BaseModel):
    text: str
    session_id: str = "default-session"

@app.get("/", response_class=HTMLResponse)
async def serve_web_interface():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Customer Support Agent</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; height: 100vh; box-sizing: border-box; }
            .chat-container { width: 100%; max-width: 600px; height: 80vh; background: white; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
            .chat-header { background: #1a73e8; color: white; padding: 20px; font-size: 1.2rem; font-weight: bold; text-align: center; }
            .chat-box { flex: 1; padding: 20px; overflow-y: auto; background: #fafafa; display: flex; flex-direction: column; gap: 15px; }
            .message { max-width: 80%; padding: 12px 16px; border-radius: 8px; font-size: 0.95rem; line-height: 1.4; }
            .message.user { background: #e3f2fd; color: #0d47a1; align-self: flex-end; border-bottom-right-radius: 2px; }
            .message.agent { background: #ffffff; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            .input-area { padding: 15px; background: white; border-top: 1px solid #eee; display: flex; gap: 10px; }
            input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; outline: none; transition: border 0.2s; }
            input:focus { border-color: #1a73e8; }
            button { background: #1a73e8; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 1rem; cursor: pointer; font-weight: bold; }
            button:hover { background: #1557b0; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">[AI Support] Customer Agent Portal</div>
            <div class="chat-box" id="chatBox">
                <div class="message agent">Hello! I am your AI assistant powered by Gemini 2.5. How can I help you with your order today?</div>
            </div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Ask about your order status..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            // FIX: Replaced 'async def' with correct native JS syntax 'async function'
            async function sendMessage() {
                const inputElement = document.getElementById('userInput');
                const text = inputElement.value.trim();
                if (!text) return;

                // Append user message to viewport
                appendMessage(text, 'user');
                inputElement.value = '';

                // Create placeholder status element
                const loaderId = appendMessage("Thinking...", 'agent');

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: text, session_id: 'web-session-' + Date.now() })
                    });
                    const data = await response.json();
                    
                    // Route response string safely into place
                    document.getElementById(loaderId).innerText = data.response;
                } catch (error) {
                    document.getElementById(loaderId).innerText = "Error contacting agent service.";
                }
            }

            function appendMessage(text, sender) {
                const chatBox = document.getElementById('chatBox');
                const msgDiv = document.createElement('div');
                const id = 'msg-' + Math.random().toString(36).substr(2, 9);
                msgDiv.className = 'message ' + sender;
                msgDiv.id = id;
                msgDiv.innerText = text;
                chatBox.appendChild(msgDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
                return id;
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') sendMessage();
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat_with_agent(query: ChatRequest):
    try:
        agent_response = run_agent(query.text, query.session_id)
        return {"response": agent_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": str(e)})

if __name__ == "__main__":
    # Cloud Run automatically injects the PORT environment variable (defaulting to 8080)
    port = int(os.environ.get("PORT", 8080))
    
    # CRITICAL: host must be '0.0.0.0' so the container listens externally
    app.run(host="0.0.0.0", port=port)
