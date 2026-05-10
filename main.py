"""Ponto de entrada principal do LiveloScrapper.

Uso:
    python main.py              # Executa a extração uma vez
    python main.py --schedule   # Inicia o agendamento diário às 10:00
"""

import argparse
import logging
import os
import sys

from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.dirname(__file__))

from src.scheduler import job, start_scheduler


def setup_logging() -> None:
    """Configura o logging do sistema."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LiveloScrapper - Extração diária de parceiros da Livelo"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Inicia o agendamento diário às 10:00 (horário de Brasília)",
    )
    args = parser.parse_args()

    setup_logging()

    if args.schedule:
        start_scheduler()
    else:
        job()


if __name__ == "__main__":
    main()
