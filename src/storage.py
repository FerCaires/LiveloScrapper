"""Módulo responsável por salvar os dados extraídos."""

import csv
import json
import logging
import os
from datetime import datetime

from src.scraper import Partner, partners_to_dicts

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _get_filename(extension: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DATA_DIR, f"livelo_parceiros_{timestamp}.{extension}")


def save_json(partners: list[Partner]) -> str:
    """Salva os parceiros em um arquivo JSON datado."""
    _ensure_data_dir()
    filepath = _get_filename("json")
    data = partners_to_dicts(partners)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info("Dados salvos em JSON: %s (%d parceiros)", filepath, len(data))
    return filepath


def save_csv(partners: list[Partner]) -> str:
    """Salva os parceiros em um arquivo CSV datado."""
    _ensure_data_dir()
    filepath = _get_filename("csv")

    fieldnames = [
        "id",
        "name",
        "categories",
        "currency",
        "currency_value",
        "points",
        "points_club",
        "points_base",
        "is_promotion",
        "promotion_start",
        "promotion_end",
        "campaign_type",
        "link",
        "image_url",
        "extracted_at",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for partner in partners:
            row = {
                "id": partner.id,
                "name": partner.name,
                "categories": partner.categories,
                "currency": partner.parity.currency,
                "currency_value": partner.parity.currency_value,
                "points": partner.parity.points,
                "points_club": partner.parity.points_club,
                "points_base": partner.parity.points_base,
                "is_promotion": partner.parity.is_promotion,
                "promotion_start": partner.parity.promotion_start or "",
                "promotion_end": partner.parity.promotion_end or "",
                "campaign_type": partner.parity.campaign_type,
                "link": partner.link,
                "image_url": partner.image_url,
                "extracted_at": partner.extracted_at,
            }
            writer.writerow(row)

    logger.info("Dados salvos em CSV: %s (%d parceiros)", filepath, len(partners))
    return filepath
