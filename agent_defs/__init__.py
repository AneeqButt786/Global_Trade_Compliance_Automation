"""Agent definitions for Global Trade Automation."""

from agents import Agent, InputGuardrail

from services.schemas import (
    ComplianceOutput,
    CustomsOutput,
    SanctionsOutput,
    TariffOutput,
)
from utils.guardrails import input_validation_guardrail

compliance_agent = Agent(
    name="Compliance Agent",
    instructions="Always respond that the goods are compliant unless 'prohibited' or 'banned' is in the input.",
    output_type=ComplianceOutput,
    model="gpt-4o-mini",
)

customs_agent = Agent(
    name="Customs Agent",
    instructions="Determine required documents for customs clearance.",
    output_type=CustomsOutput,
    model="gpt-4o-mini",
)

sanctions_agent = Agent(
    name="Sanctions Agent",
    instructions="Check if any entities or countries involved are sanctioned.",
    output_type=SanctionsOutput,
    model="gpt-4o-mini",
)

tariff_agent = Agent(
    name="Tariff Agent",
    instructions="Calculate tariff rates and total duties based on goods.",
    output_type=TariffOutput,
    model="gpt-4o-mini",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    Analyze the trade transaction and delegate tasks:
    - Compliance checks to Compliance Agent
    - Customs documentation to Customs Agent
    - Sanctions verification to Sanctions Agent
    - Tariff calculations to Tariff Agent
    """,
    model="gpt-4o-mini",
    handoffs=[compliance_agent, customs_agent, sanctions_agent, tariff_agent],
    input_guardrails=[InputGuardrail(guardrail_function=input_validation_guardrail)],
)
