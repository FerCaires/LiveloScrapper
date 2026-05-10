# Tasks: Filtro de Categorias

**Feature Name:** filtro-categorias  
**Data:** 2026-05-10  
**Autor:** Developer (Orquestrador)

## Tarefas Executadas

### 1. Criar módulo `src/filters.py`
- [x] Definir constante `FILTERED_CATEGORIES` com as 4 categorias
- [x] Implementar `filter_partners_by_category()` com:
  - Comparação case-insensitive
  - Split do campo `categories` por espaço
  - Interseção de conjuntos para matching
  - Ordenação por `parity.points` decrescente
  - Logging do resultado do filtro
- [x] Parâmetro `categories` opcional para flexibilidade

### 2. Alterar `src/scheduler.py`
- [x] Importar `filter_partners_by_category`
- [x] Aplicar filtro APÓS salvar JSON/CSV (preserva dados completos)
- [x] Passar lista filtrada para `send_telegram_notification()`
- [x] Passar lista filtrada para `_print_summary()`
- [x] Atualizar log de resumo para mostrar total extraído vs filtrado
- [x] Atualizar `_print_summary()` para exibir ranking completo (não apenas promoções)

### 3. Sem alterações necessárias em:
- [x] `src/scraper.py` — continua extraindo todos
- [x] `src/storage.py` — continua salvando todos
- [x] `src/notifier.py` — já recebe lista filtrada do scheduler
- [x] `src/models/` — modelos inalterados

## Arquivos Criados/Modificados

| Arquivo | Ação |
|---------|------|
| `src/filters.py` | **NOVO** — módulo de filtro por categoria |
| `src/scheduler.py` | **MODIFICADO** — integra filtro antes de notificar e exibir summary |
| `docs/filtro-categorias/spec-filtro-categorias.md` | **NOVO** — requisitos (PM) |
| `docs/filtro-categorias/plan-filtro-categorias.md` | **NOVO** — spec técnica (Tech Lead) |
| `docs/filtro-categorias/tasks-filtro-categorias.md` | **NOVO** — tarefas (Developer) |
| `docs/regras-de-negocio.md` | **NOVO** — base de conhecimento de negócio |
| `docs/fluxo-de-desenvolvimento.md` | **NOVO** — base de conhecimento técnico |
