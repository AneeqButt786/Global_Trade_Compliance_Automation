# Global Trade Compliance Automation

## Overview

An AI-powered system for automating international trade compliance checks. It handles real-time compliance verification, customs documentation, sanctions screening, and tariff calculations, reducing risk and streamlining cross-border transactions.

## Features

- **Compliance verification** – Real-time checks for prohibited/banned goods
- **Customs documentation** – Determines required documents for clearance
- **Sanctions screening** – Checks entities and countries against sanctions lists
- **Tariff calculations** – Computes duty rates and total duties
- **Input guardrails** – Rejects inputs with forbidden terms (restricted, prohibited, banned)

## Tech Stack

- Python 3.12+
- OpenAI Agents SDK (openai-agents)
- Chainlit (chat UI)
- Pydantic (schemas)
- python-dotenv (environment variables)

## Setup

1. Navigate to the project folder:
   ```bash
   cd Global_Trade_Automation_Agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or, if using the workspace: `uv sync`

3. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY=sk-...
   ```

## Run Commands

```bash
chainlit run app.py
```

## Example Use Cases

1. **Electronics export:** "Exporting 1000 units of electronics to Country A. Quantity: 1000, Unit Price: $50"
2. **Textiles shipment:** "Shipping 500 units of textiles to Country B"
3. **Automobile export:** "Exporting 50 automobiles to Country A at $25,000 each"

## Folder Structure

```
Global_Trade_Automation_Agent/
├── app.py                 # Chainlit entry point
├── config.py              # Config wrapper
├── agent_defs/
│   └── __init__.py        # Agent definitions
├── services/
│   ├── __init__.py
│   └── schemas.py         # Pydantic schemas
├── utils/
│   ├── __init__.py
│   ├── config.py          # Env vars
│   ├── logging.py         # Logging setup
│   └── guardrails.py      # Input validation
├── .env.example
├── README.md
└── requirements.txt
```
