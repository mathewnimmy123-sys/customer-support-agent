# support_agent/supervisor.py
from google.adk import Agent
from .sub_agents import order_agent, returns_agent

customer_support_supervisor = Agent(
    name="support_supervisor",
    model="gemini-2.5-pro",
    instruction=(
        "You are the primary customer support supervisor. Your job is to greet the customer, "
        "understand their issue, and delegate it to the appropriate specialist:\n"
        "- For tracking packages or checking order status, delegate to `order_specialist`.\n"
        "- For queries about returning products, refunds, or exchanges, delegate to `returns_specialist`.\n"
        "Always pass back the final answer from the specialist clearly to the customer."
    ),
    sub_agents=[order_agent, returns_agent]
)