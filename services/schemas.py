"""Pydantic schemas for Global Trade Automation."""

from pydantic import BaseModel
from typing import List


class ComplianceIssue(BaseModel):
    message: str
    critical: bool


class ComplianceOutput(BaseModel):
    compliant: bool
    issues: List[ComplianceIssue]


class CustomsOutput(BaseModel):
    documents_required: List[str]
    clearance_possible: bool


class SanctionsOutput(BaseModel):
    sanctioned: bool
    entities: List[str]


class TariffOutput(BaseModel):
    tariff_rate: float
    total_duty: float
