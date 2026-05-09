"""Módulo de notificação via Telegram Bot API.

Envia uma mensagem consolidada com os parceiros de maior pontuação
após cada execução do scraping.
"""

import logging
import os
import time
from datetime import datetime

import requests

from src.models import Partner

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"
MAX_RETRIES = 3
TOP_PARTNERS_COUNT = 20
MAX_MESSAGE_LENGTH = 4096


def send_telegram_notification(partners: list[Partner]) -> None:
    """Envia notificação com o ranking de parceiros para o Telegram."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.warning(
            "Variáveis TELEGRAM_BOT_TOKEN e/ou TELEGRAM_CHAT_ID não configuradas. "
            "Notificação ignorada."
        )
        return

    try:
        message = _build_message(partners)
        _send_telegram_message(token, chat_id, message)
    except Exception:
        logger.exception("Erro inesperado ao enviar notificação Telegram")


def _build_message(partners: list[Partner]) -> str:
    """Formata a mensagem com os top parceiros ordenados por pontuação."""
    sorted_partners = sorted(partners, key=lambda p: p.parity.points, reverse=True)
    top = sorted_partners[:TOP_PARTNERS_COUNT]

    header = (
        f"\U0001f4ca LIVELO - Consulta de "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        f"Top {TOP_PARTNERS_COUNT} Parceiros (pontos/real):\n\n"
    )

    lines: list[str] = []
    for i, partner in enumerate(top, start=1):
        line = (
            f"{i}. {partner.name} - {partner.parity.points} pts/"
            f"{partner.parity.currency}{partner.parity.currency_value}"
        )
        lines.append(line)

    message = header + "\n".join(lines)

    if len(message) > MAX_MESSAGE_LENGTH:
        while lines and len(header + "\n".join(lines)) > MAX_MESSAGE_LENGTH:
            lines.pop()
        message = header + "\n".join(lines)

    return message


def _send_telegram_message(token: str, chat_id: str, text: str) -> None:
    """Envia mensagem via Telegram Bot API com retry e exponential backoff."""
    url = TELEGRAM_API_URL.format(token=token)
    payload = {"chat_id": chat_id, "text": text}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Notificação Telegram enviada com sucesso")
            return
        except requests.RequestException:
            if attempt < MAX_RETRIES:
                wait_time = 2 ** (attempt - 1)
                logger.warning(
                    "Falha ao enviar Telegram (tentativa %d/%d). Retentando em %ds...",
                    attempt,
                    MAX_RETRIES,
                    wait_time,
                )
                time.sleep(wait_time)
            else:
                logger.error(
                    "Falha ao enviar notificação Telegram após %d tentativas",
                    MAX_RETRIES,
                )
