"""
Global Trade Compliance Automation - Chainlit App
Run with: chainlit run app.py
"""

import chainlit as cl
from agents import Runner, set_default_openai_key

from config import get_config
from agent_defs import (
    triage_agent,
    compliance_agent,
    customs_agent,
    sanctions_agent,
    tariff_agent,
)
from services.schemas import (
    ComplianceOutput,
    CustomsOutput,
    SanctionsOutput,
    TariffOutput,
)
from utils.logging import get_logger

logger = get_logger(__name__)


def _ensure_config():
    """Validate config at startup."""
    cfg = get_config()
    set_default_openai_key(cfg["openai_api_key"])
    return cfg


@cl.on_chat_start
async def on_chat_start():
    """Initialize session and send welcome message."""
    try:
        _ensure_config()
        await cl.Message(
            content="""**Global Trade Compliance Automation**

I help automate international trade compliance checks:
- **Compliance verification** – Real-time compliance checks
- **Customs documentation** – Required documents for clearance
- **Sanctions screening** – Entity and country sanctions checks
- **Tariff calculations** – Duty rates and total duties

Describe a trade transaction (e.g., "Exporting 1000 units of electronics to Country A. Quantity: 1000, Unit Price: $50") to get a full compliance report.""",
            author="Trade Compliance",
        ).send()
    except ValueError as e:
        await cl.Message(content=f"**Configuration Error:** {e}", author="System").send()
        raise


@cl.on_message
async def on_message(message: cl.Message):
    """Process trade transaction and return compliance report."""
    trade_input = message.content.strip()
    if not trade_input:
        await cl.Message(content="Please provide a trade transaction description.", author="System").send()
        return

    status_msg = await cl.Message(content="Processing compliance check...", author="Trade Compliance").send()

    try:
        _ensure_config()
        logger.info("Processing trade: %s", trade_input[:50])

        compliance_result = await Runner.run(compliance_agent, trade_input)
        compliance_output = compliance_result.final_output_as(ComplianceOutput)

        critical_issues = [
            i for i in compliance_output.issues
            if any(t in i.message.lower() for t in ["prohibited", "illegal", "banned"])
        ]
        if critical_issues:
            await status_msg.remove()
            await cl.Message(
                content="**Terminating:** Critical compliance issues detected. Transaction cannot proceed.",
                author="Trade Compliance",
            ).send()
            return

        customs_result = await Runner.run(customs_agent, trade_input)
        customs_output = customs_result.final_output_as(CustomsOutput)

        sanctions_result = await Runner.run(sanctions_agent, trade_input)
        sanctions_output = sanctions_result.final_output_as(SanctionsOutput)

        tariff_result = await Runner.run(tariff_agent, trade_input)
        tariff_output = tariff_result.final_output_as(TariffOutput)

        await status_msg.remove()

        report = f"""## Trade Compliance Report

### Compliance Check
- **Compliant:** {compliance_output.compliant}
- **Issues:** {", ".join(i.message for i in compliance_output.issues) if compliance_output.issues else "None"}

### Customs
- **Clearance Possible:** {customs_output.clearance_possible}
- **Required Documents:** {", ".join(customs_output.documents_required)}

### Sanctions
- **Sanctioned:** {sanctions_output.sanctioned}
- **Entities:** {", ".join(sanctions_output.entities) if sanctions_output.entities else "None"}

### Tariff
- **Tariff Rate:** {tariff_output.tariff_rate * 100}%
- **Total Duty:** ${tariff_output.total_duty}

---
Trade transaction processed successfully.
"""
        await cl.Message(content=report, author="Trade Compliance").send()
        logger.info("Trade processed successfully")
    except Exception as e:
        logger.exception("Trade processing failed")
        await status_msg.remove()
        await cl.Message(
            content="Something went wrong. Please try again or rephrase your request.",
            author="Trade Compliance",
        ).send()
