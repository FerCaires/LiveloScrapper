"""Módulo responsável pelo agendamento diário da extração."""

import logging
import time
from datetime import datetime

import schedule

from src.filters import filter_partners_by_category
from src.notifier import send_telegram_notification
from src.scraper import scrape_partners
from src.storage import save_csv, save_json

logger = logging.getLogger(__name__)

EXECUTION_TIME = "19:25"


def job() -> None:
    """Executa a extração e salva os resultados."""
    logger.info(
        "Executando job agendado em %s",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    try:
        partners = scrape_partners()
        json_path = save_json(partners)
        csv_path = save_csv(partners)

        filtered = filter_partners_by_category(partners)

        send_telegram_notification(filtered)

        promos = [p for p in filtered if p.parity.is_promotion]
        logger.info(
            "Resumo: %d parceiros extraídos | %d filtrados | %d em promoção",
            len(partners),
            len(filtered),
            len(promos),
        )
        logger.info("Arquivos salvos: %s, %s", json_path, csv_path)

        _print_summary(filtered)
    except Exception:
        logger.exception("Erro durante a extração")


def _print_summary(partners: list) -> None:
    """Imprime um resumo dos parceiros filtrados no console."""
    promos = [p for p in partners if p.parity.is_promotion]

    print("\n" + "=" * 60)
    print(f"  LIVELO - Extração de {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Parceiros filtrados: {len(partners)}")
    print(f"  Em promoção: {len(promos)}")
    print("=" * 60)

    if partners:
        print("\n  Ranking por pontuação (categorias filtradas):")
        print("  " + "-" * 56)
        for p in sorted(partners, key=lambda x: x.parity.points, reverse=True):
            promo_tag = " ⭐" if p.parity.is_promotion else ""
            print(
                f"  {p.name:<30} {p.parity.points} pts/"
                f"{p.parity.currency}{p.parity.currency_value} "
                f"(base: {p.parity.points_base}){promo_tag}"
            )
        print("  " + "-" * 56)
    print()


def start_scheduler() -> None:
    """Inicia o agendamento para execução diária às 10:00 (horário local)."""
    schedule.every().day.at(EXECUTION_TIME).do(job)

    logger.info(
        "Scheduler iniciado. Próxima execução agendada para %s",
        schedule.next_run(),
    )
    print(f"Scheduler ativo - execução diária às {EXECUTION_TIME}")
    print(f"Próxima execução: {schedule.next_run()}")
    print("Pressione Ctrl+C para encerrar.\n")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Scheduler encerrado pelo usuário")
        print("\nScheduler encerrado.")
