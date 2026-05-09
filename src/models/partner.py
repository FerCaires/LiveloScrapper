"""Modelo de dados para parceiro da Livelo."""

from dataclasses import dataclass

from src.models.parity import ParityInfo


@dataclass
class Partner:
    id: str
    name: str
    image_url: str
    link: str
    categories: str
    parity: ParityInfo
    extracted_at: str = ""
