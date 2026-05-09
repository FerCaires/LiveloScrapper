"""Modelo de dados para informações de paridade/pontuação."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParityInfo:
    currency: str
    currency_value: int
    points: int
    points_club: int
    points_base: int
    is_promotion: bool
    promotion_start: Optional[str] = None
    promotion_end: Optional[str] = None
    campaign_type: str = "BAU"
    legal_terms: str = ""
