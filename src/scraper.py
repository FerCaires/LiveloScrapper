"""Módulo responsável por extrair os dados dos parceiros da Livelo."""

import json
import logging
from dataclasses import asdict
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.models import ParityInfo, Partner

logger = logging.getLogger(__name__)

LIVELO_URL = "https://www.livelo.com.br/juntar-pontos/todos-os-parceiros"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}


def fetch_page(url: str = LIVELO_URL) -> str:
    """Faz o request à página de parceiros da Livelo e retorna o HTML."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def parse_next_data(html: str) -> dict:
    """Extrai e parseia o JSON do __NEXT_DATA__ embutido na página."""
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")
    if not script_tag or not script_tag.string:
        raise ValueError("Não foi possível encontrar __NEXT_DATA__ na página")
    return json.loads(script_tag.string)


def extract_partners(data: dict) -> list[Partner]:
    """Extrai a lista de parceiros a partir do JSON do __NEXT_DATA__."""
    components = data["props"]["pageProps"]["page"]["components"]

    partner_list_component = None
    for component in components:
        if component.get("type") == "cb_partner_list":
            partner_list_component = component
            break

    if partner_list_component is None:
        raise ValueError(
            "Componente 'cb_partner_list' não encontrado na página"
        )

    raw_partners = partner_list_component["props"]["configPartners"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    partners = []

    for raw in raw_partners:
        parity_data = raw.get("parity", {})
        parity = ParityInfo(
            currency=parity_data.get("currency", "R$"),
            currency_value=parity_data.get("currencyValue", 1),
            points=parity_data.get("parity", 0),
            points_club=parity_data.get("parityClub", 0),
            points_base=parity_data.get("parityBau", 0),
            is_promotion=parity_data.get("promotion", False),
            promotion_start=parity_data.get("dateStart"),
            promotion_end=parity_data.get("dateEnd"),
            campaign_type=parity_data.get("activeCampaign", "BAU"),
            legal_terms=parity_data.get("legalTerms", ""),
        )

        partner = Partner(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            image_url=raw.get("image", ""),
            link=raw.get("link", ""),
            categories=raw.get("categories", ""),
            parity=parity,
            extracted_at=now,
        )
        partners.append(partner)

    return partners


def scrape_partners() -> list[Partner]:
    """Executa o fluxo completo de scraping: fetch + parse + extract."""
    logger.info("Iniciando extração dos parceiros da Livelo...")
    html = fetch_page()
    data = parse_next_data(html)
    partners = extract_partners(data)
    logger.info("Extração concluída: %d parceiros encontrados", len(partners))
    return partners


def partners_to_dicts(partners: list[Partner]) -> list[dict]:
    """Converte lista de parceiros para lista de dicts serializáveis."""
    return [asdict(p) for p in partners]
