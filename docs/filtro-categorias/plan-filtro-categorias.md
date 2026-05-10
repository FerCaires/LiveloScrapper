# Plano Técnico: Filtro de Categorias na Notificação

**Feature Name:** filtro-categorias  
**Data:** 2026-05-10  
**Autor:** Tech Lead (Orquestrador)

## 1. Visão Geral da Solução

Criar um módulo de filtro centralizado (`src/filters.py`) que será utilizado pelo notifier e pelo scheduler para filtrar parceiros por categorias antes de exibi-los. O scraper e storage permanecem inalterados.

## 2. Arquitetura

### 2.1 Novo Arquivo: `src/filters.py`

Módulo responsável pela lógica de filtro de parceiros por categoria.

```python
FILTERED_CATEGORIES: set[str]  # Conjunto das categorias alvo (lowercase)

def filter_partners_by_category(partners: list[Partner]) -> list[Partner]:
    """Filtra parceiros que possuem pelo menos uma categoria na lista."""

def sort_partners_by_points(partners: list[Partner], descending: bool = True) -> list[Partner]:
    """Ordena parceiros por parity.points."""
```

**Decisões técnicas:**
- Constante `FILTERED_CATEGORIES` como `set` para lookup O(1)
- Valores em lowercase para comparação case-insensitive
- O campo `categories` do Partner (string) é splitado por espaço e comparado via interseção de conjuntos
- Funções puras e sem side effects para facilitar testes

### 2.2 Alterações em `src/notifier.py`

- Importar `filter_partners_by_category` de `src/filters.py`
- Na função `_build_message`: aplicar o filtro ANTES da ordenação e seleção dos top parceiros
- Manter o top N (TOP_PARTNERS_COUNT = 20) após o filtro

### 2.3 Alterações em `src/scheduler.py`

- Importar `filter_partners_by_category` de `src/filters.py`
- Na função `_print_summary`: aplicar o filtro na lista de parceiros antes de gerar destaques
- O summary geral (total de parceiros, parceiros em promoção) deve refletir apenas os filtrados
- Passar `partners` filtrados para `send_telegram_notification` ao invés da lista completa

### 2.4 Sem Alterações

- `src/scraper.py` — continua extraindo todos os parceiros
- `src/storage.py` — continua salvando todos os parceiros
- `src/models/` — sem mudanças nos modelos

## 3. Fluxo de Dados Atualizado

```
scrape_partners() → [todos os parceiros]
    ├── save_json(partners)         → JSON com todos
    ├── save_csv(partners)          → CSV com todos
    ├── filtered = filter_partners_by_category(partners)
    ├── send_telegram_notification(filtered)  → Telegram só com filtrados
    └── _print_summary(filtered)              → Console só com filtrados
```

## 4. Detalhamento da Implementação

### 4.1 `src/filters.py` (NOVO)

```python
FILTERED_CATEGORIES = {
    "perfumariaecosmeticos",
    "modaebeleza",
    "modaeacessorios",
    "calcados",
}

def filter_partners_by_category(partners, categories=None):
    if categories is None:
        categories = FILTERED_CATEGORIES
    target = {c.lower() for c in categories}
    return [
        p for p in partners
        if {c.lower() for c in p.categories.split()}.intersection(target)
    ]
```

### 4.2 `src/scheduler.py` — Alteração na função `job()`

```python
# Após salvar JSON/CSV (sem filtro), filtrar para notificação e summary:
from src.filters import filter_partners_by_category

filtered_partners = filter_partners_by_category(partners)
send_telegram_notification(filtered_partners)
_print_summary(filtered_partners)
```

### 4.3 `src/notifier.py` — Sem mudança na lógica interna

O notifier já ordena por points decrescente internamente. Basta receber a lista já filtrada.

## 5. Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Nenhum parceiro encontrado nas categorias filtradas | Log de warning + mensagem informativa no Telegram |
| Categorias com variação de capitalização | Comparação case-insensitive |
| Campo `categories` vazio ou None | Tratar string vazia como sem categorias (parceiro excluído) |

## 6. Testes Sugeridos

1. Parceiro com categoria exata (ex: `"perfumariaecosmeticos"`) → incluído
2. Parceiro com múltiplas categorias, uma delas filtrada → incluído
3. Parceiro sem categoria filtrada (ex: `"eletronicos"`) → excluído
4. Parceiro com `categories` vazio → excluído
5. Verificar que ordenação decrescente por points é mantida após filtro
6. Verificar que JSON/CSV continuam salvando todos os parceiros
