# support_agent/sub_agents.py
from google.adk import Agent
from .tools import fetch_order_status

order_agent = Agent(
    name="order_specialist",
    model="gemini-2.5-flash",
    instruction=(
        "You are an expert in tracking shipments and order logistics. "
        "Use the `fetch_order_status` tool to look up order information. "
        "Summarize the tracking details politely for the customer."
    ),
    tools=[fetch_order_status]
)

returns_agent = Agent(
    name="returns_specialist",
    model="gemini-2.5-flash",
    instruction=(
        "You handle product returns and refunds according to company policy: "
        "- Customers can return items within 30 days of purchase. "
        "- Items must be unused and in original packaging. "
        "Be empathetic but strict about enforcing these guidelines."
    )
)