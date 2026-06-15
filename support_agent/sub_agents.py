# support_agent/sub_agents.py
from google.adk.agents import Agent       # correct import path
from .tools import fetch_order_status
 
order_agent = Agent(
    name="order_specialist",
    model="gemini-2.5-flash",
    instruction=(
        "You are an expert in tracking shipments and order logistics. "
        "Use the `fetch_order_status` tool to look up order information. "
        "Summarize the tracking details politely for the customer."
    ),
    tools=[fetch_order_status],            # closing parenthesis was missing before
)
 
returns_agent = Agent(
    name="returns_specialist",
    model="gemini-2.5-flash",
    instruction=(
        "You handle product returns and refunds according to company policy:\n"
        "- Customers can return items within 30 days of purchase.\n"
        "- Items must be unused and in original packaging.\n"
        "Be empathetic but firm about these guidelines."
    ),                                     # closing parenthesis was missing before
)
 