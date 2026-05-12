"""Módulo responsável por filtrar parceiros por categoria."""

import logging

from src.models import Partner

logger = logging.getLogger(__name__)

FILTERED_CATEGORIES: set[str] = {
    "perfumariaecosmeticos",
    "modaebeleza",
    "modaeacessorios",
    "calcados",
}


def filter_partners_by_category(
    partners: list[Partner],
    categories: set[str] | None = None,
) -> list[Partner]:
    """Filtra parceiros que possuem pelo menos uma das categorias alvo.

    O campo ``categories`` do parceiro é uma string com categorias separadas
    por espaço.  A comparação é case-insensitive.

    Args:
        partners: Lista completa de parceiros extraídos.
        categories: Conjunto de categorias alvo.  Se ``None``, utiliza
            ``FILTERED_CATEGORIES``.

    Returns:
        Lista de parceiros que possuem pelo menos uma categoria correspondente,
        ordenada por melhor pontuação (``parity.best_points``) em ordem decrescente.
    """
    target = {c.lower() for c in (categories or FILTERED_CATEGORIES)}

    filtered = [
        p
        for p in partners
        if {c.lower() for c in p.categories.split()}.intersection(target)
    ]

    filtered.sort(key=lambda p: p.parity.best_points, reverse=True)

    logger.info(
        "Filtro de categorias aplicado: %d de %d parceiros selecionados",
        len(filtered),
        len(partners),
    )
    return filtered
