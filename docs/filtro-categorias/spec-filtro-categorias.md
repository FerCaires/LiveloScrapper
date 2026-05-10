# Spec: Filtro de Categorias na Notificação

**Feature Name:** filtro-categorias  
**Data:** 2026-05-10  
**Autor:** PM (Orquestrador)

## 1. Contexto

O LiveloScrapper extrai dados de todos os parceiros da Livelo (200+ parceiros). Atualmente, a notificação Telegram e o summary no console exibem os parceiros com maior pontuação sem distinção de categoria. Para tornar a informação mais relevante para os clientes, precisamos filtrar por categorias específicas de interesse.

## 2. Objetivo

Filtrar a lista de parceiros exibida na **notificação Telegram** e no **summary do console** para mostrar apenas parceiros das categorias relevantes, mantendo a ordenação decrescente por pontuação.

**IMPORTANTE:** O salvamento dos dados (JSON e CSV) **NÃO** deve ser afetado. Todos os parceiros continuam sendo salvos normalmente.

## 3. Categorias a Filtrar

As seguintes categorias devem ser incluídas no filtro:

| Categoria (valor no campo `categories`) | Descrição |
|------------------------------------------|-----------|
| `perfumariaecosmeticos` | Perfumaria e Cosméticos |
| `modaebeleza` | Moda e Beleza |
| `modaeacessorios` | Moda e Acessórios |
| `calcados` | Calçados |

## 4. Escopo

### 4.1 Afetado pelo filtro
- **Notificação Telegram** (`src/notifier.py`): Apenas parceiros das categorias filtradas devem aparecer no ranking enviado
- **Summary no console** (`src/scheduler.py` → `_print_summary`): Apenas parceiros das categorias filtradas devem aparecer nos destaques

### 4.2 NÃO afetado pelo filtro
- **Salvamento JSON** (`src/storage.py` → `save_json`): Continua salvando TODOS os parceiros
- **Salvamento CSV** (`src/storage.py` → `save_csv`): Continua salvando TODOS os parceiros
- **Extração/Scraping** (`src/scraper.py`): Continua extraindo TODOS os parceiros

## 5. Regras de Negócio

1. O campo `categories` do parceiro é uma string que pode conter múltiplas categorias separadas por espaço (ex: `"perfumariaecosmeticos modaebeleza"`)
2. Um parceiro deve ser incluído se **qualquer uma** de suas categorias estiver na lista de categorias filtradas
3. A comparação deve ser case-insensitive para evitar problemas com variações de capitalização
4. A ordenação por pontuação (`parity.points`) decrescente deve ser mantida após o filtro
5. As categorias filtradas devem ser configuráveis (constante ou variável de fácil manutenção)

## 6. Critérios de Aceite

- [ ] **CA-01:** A notificação Telegram exibe apenas parceiros que possuem pelo menos uma das categorias: perfumariaecosmeticos, modaebeleza, modaeacessorios, calcados
- [ ] **CA-02:** O summary no console exibe apenas parceiros das categorias filtradas
- [ ] **CA-03:** Os parceiros exibidos estão ordenados por `parity.points` em ordem decrescente
- [ ] **CA-04:** O salvamento em JSON continua incluindo TODOS os parceiros (sem filtro)
- [ ] **CA-05:** O salvamento em CSV continua incluindo TODOS os parceiros (sem filtro)
- [ ] **CA-06:** Parceiros com múltiplas categorias são incluídos se pelo menos uma categoria corresponder
- [ ] **CA-07:** A lista de categorias é facilmente configurável/manutenível

## 7. Fora de Escopo

- Filtro dinâmico via interface ou API
- Filtro configurável via variáveis de ambiente (pode ser implementado futuramente)
- Alterações no modelo de dados Partner ou ParityInfo
