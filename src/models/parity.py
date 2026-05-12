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

    @property
    def best_points(self) -> int:
        """Retorna a melhor pontuação entre normal/promoção e Clube."""
        return max(self.points, self.points_club)

    @property
    def is_club_best(self) -> bool:
        """Indica se a melhor pontuação provém do Clube Livelo."""
        return self.points_club > self.points
