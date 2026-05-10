# Testes QA: Filtro de Categorias

**Feature Name:** filtro-categorias  
**Data:** 2026-05-10  
**Autor:** QA (Orquestrador)

## 1. Resumo da Validação

| Métrica | Valor |
|---------|-------|
| Total de parceiros extraídos | 258 |
| Parceiros após filtro | 94 |
| Categorias filtradas | perfumariaecosmeticos, modaebeleza, modaeacessorios, calcados |
| PR | [#6](https://github.com/FerCaires/LiveloScrapper/pull/6) — Merged ✓ |

## 2. Critérios de Aceite — Resultados

| ID | Critério | Resultado | Observação |
|----|----------|-----------|------------|
| CA-01 | Notificação Telegram exibe apenas parceiros das categorias filtradas | ✅ PASS | `send_telegram_notification(filtered)` recebe lista já filtrada |
| CA-02 | Summary no console exibe apenas parceiros filtrados | ✅ PASS | `_print_summary(filtered)` recebe lista já filtrada |
| CA-03 | Parceiros ordenados por `parity.points` decrescente | ✅ PASS | Verificado: sequência de 10→8→8→7→7→6→...→1 pts |
| CA-04 | JSON salvo com TODOS os parceiros (sem filtro) | ✅ PASS | JSON: 258 parceiros (= total extraído) |
| CA-05 | CSV salvo com TODOS os parceiros (sem filtro) | ✅ PASS | CSV: 258 parceiros (= total extraído) |
| CA-06 | Parceiros com múltiplas categorias incluídos se ao menos uma corresponder | ✅ PASS | Ex: "Riachuelo" com 8 categorias, incluído por ter calcados, modaebeleza, etc. |
| CA-07 | Lista de categorias facilmente configurável | ✅ PASS | Constante `FILTERED_CATEGORIES` em `src/filters.py` |

## 3. Testes Executados

### 3.1 Teste de Filtro por Categoria
- **Input:** 258 parceiros extraídos da Livelo
- **Filtro:** perfumariaecosmeticos, modaebeleza, modaeacessorios, calcados
- **Output:** 94 parceiros selecionados
- **Validação:** Todos os 94 parceiros possuem pelo menos uma das categorias filtradas
- **Resultado:** ✅ PASS

### 3.2 Teste de Ordenação Decrescente
- **Validação:** Lista de pontuações `[p.parity.points for p in filtered]` está em ordem decrescente
- **Top 5:** Abelha Rainha (10), Beleza na web (8), Piatan Natural (8), CEA (7), Crocs (7)
- **Resultado:** ✅ PASS

### 3.3 Teste de Persistência Completa (JSON)
- **Validação:** Arquivo JSON salvo contém 258 parceiros (todos, sem filtro)
- **Resultado:** ✅ PASS

### 3.4 Teste de Persistência Completa (CSV)
- **Validação:** Arquivo CSV salvo contém 258 parceiros (todos, sem filtro)
- **Resultado:** ✅ PASS

### 3.5 Teste de Case-Insensitive
- **Validação:** Comparação de categorias é feita com `.lower()` — funciona independente de capitalização
- **Resultado:** ✅ PASS (verificado via teste unitário com categorias em maiúsculo)

### 3.6 Teste de Parceiro com Múltiplas Categorias
- **Exemplo:** "Riachuelo" — categorias: `perfumariaecosmeticos infantil todos calcados casaedecoracao bebes modaebeleza modaeacessorios`
- **Validação:** Incluído no resultado por ter 4 categorias correspondentes
- **Resultado:** ✅ PASS

### 3.7 Teste de Parceiro sem Categoria Filtrada
- **Validação:** Parceiros como "Mercado Livre" (cat: `todos marketplace`) foram corretamente excluídos
- **Resultado:** ✅ PASS

## 4. Bugs Encontrados

Nenhum bug encontrado durante os testes.

## 5. Observações

- O filtro reduziu a lista de 258 para 94 parceiros (~36% do total), tornando a notificação significativamente mais relevante
- As categorias mais representadas nos resultados são `modaebeleza` e `modaeacessorios`
- Parceiros da categoria `calcados` frequentemente também possuem `modaebeleza` e `modaeacessorios`
