# support_agent/supervisor.py
from google.adk.agents import Agent        # correct import path (not google.adk)
from .sub_agents import order_agent, returns_agent
 
customer_support_supervisor = Agent(
    name="support_supervisor",
    model="gemini-2.5-flash",              # using flash (pro not needed for routing)
    instruction=(
        "You are the primary customer support supervisor. "
        "Understand the customer's issue and delegate to the right specialist:\n"
        "- Order tracking / shipment status → order_specialist\n"
        "- Returns, refunds, exchanges      → returns_specialist\n"
        "Always relay the specialist's answer back to the customer clearly."
    ),
    sub_agents=[order_agent, returns_agent],   # closing parenthesis was missing before
)
 