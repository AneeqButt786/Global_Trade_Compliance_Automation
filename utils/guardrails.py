"""Input validation guardrails for Global Trade Automation."""

from agents import GuardrailFunctionOutput


async def input_validation_guardrail(ctx, agent, input_data: str):
    """Validate trade input for forbidden terms."""
    forbidden_terms = ["restricted", "prohibited", "banned"]
    issues = [term for term in forbidden_terms if term in input_data.lower()]
    if issues:
        return GuardrailFunctionOutput(
            output_info={"error": f"Input contains forbidden terms: {', '.join(issues)}."},
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(
        output_info={"message": "Input is valid."},
        tripwire_triggered=False,
    )
