# Requisitos: Clube Category

**Feature Name:** clube-category
**Data:** 2026-05-12
**Autor:** PM Agent

---

## Contexto

O programa Livelo possui **três categorias de pontuação** para cada parceiro:

| Categoria | Campo no modelo | Origem no JSON | Descrição |
|-----------|----------------|----------------|-----------|
| Normal/Promoção | `points` | `parity` | Pontuação padrão ou promocional (a que estiver ativa) |
| Clube | `points_club` | `parityClub` | Pontuação preferencial para assinantes do Clube Livelo |
| Base (BAU) | `points_base` | `parityBau` | Pontuação base sem promoção (apenas referência) |

**Problema atual:** O scraper já extrai corretamente o campo `points_club` do JSON da Livelo e o armazena no modelo `ParityInfo`. Porém, os módulos de **notificação** (`notifier.py`), **filtro** (`filters.py`) e **summary** (`scheduler.py`) utilizam exclusivamente `parity.points` para ordenação e exibição — **ignorando completamente** a pontuação do Clube.

**Exemplo real:** A Riachuelo oferece 8 pontos no normal e 10 pontos para assinantes do Clube Livelo. Hoje, o sistema exibe apenas 8 pontos, descartando a melhor oferta disponível.

## Objetivo

Ajustar o sistema para que, em todos os pontos de **ordenação e exibição** (notificação Telegram, filtro de categorias e summary no console), seja utilizada a **maior pontuação disponível** entre `points` e `points_club` — garantindo que o usuário sempre veja a melhor oferta de cada parceiro.

Adicionalmente, a mensagem deve **indicar visualmente** quando a pontuação exibida provém do Clube Livelo.

## Requisitos Funcionais

### RF01 — Cálculo da melhor pontuação
- Para cada parceiro, calcular: `best_points = max(parity.points, parity.points_club)`
- O campo `points_base` (BAU) **NÃO** entra neste cálculo — é apenas referência

### RF02 — Identificação da origem da pontuação
- Determinar se a melhor pontuação vem do Clube (`points_club > points`) ou do canal normal/promoção (`points >= points_club`)
- Esta informação será usada para a indicação visual na mensagem

### RF03 — Ordenação por melhor pontuação
- Em **todos** os pontos onde hoje se ordena por `parity.points`, passar a ordenar por `best_points`:
  - `src/notifier.py` → `_build_message()` — `sorted(..., key=lambda p: p.parity.points)`
  - `src/filters.py` → `filter_partners_by_category()` — `filtered.sort(key=lambda p: p.parity.points)`
  - `src/scheduler.py` → `_print_summary()` — `sorted(..., key=lambda x: x.parity.points)`

### RF04 — Exibição com indicador visual na notificação Telegram
- Na mensagem Telegram (`_build_message`), exibir a melhor pontuação com indicador de origem
- **Formato quando a pontuação é do Clube:**
  ```
  1. Riachuelo - 10 pts/R$1 🏆 (Clube)
  ```
- **Formato quando a pontuação é normal/promoção (sem mudança):**
  ```
  2. Amazon - 8 pts/R$1
  ```

### RF05 — Exibição com indicador visual no summary do console
- No summary do console (`_print_summary`), exibir a melhor pontuação com indicador de origem
- Manter a tag ⭐ existente para promoções
- Adicionar tag 🏆 quando a melhor pontuação vem do Clube
- **Formato:**
  ```
  Riachuelo                      10 pts/R$1 (base: 5) 🏆
  Amazon                          8 pts/R$1 (base: 3) ⭐
  ```

### RF06 — Persistência de dados inalterada
- O salvamento em JSON e CSV **NÃO** deve ser alterado
- Todos os campos originais (`points`, `points_club`, `points_base`) continuam sendo persistidos
- Todos os parceiros continuam sendo salvos (sem filtro)

### RF07 — Modelo de dados inalterado
- O modelo `ParityInfo` **NÃO** precisa ser alterado
- Os campos `points`, `points_club` e `points_base` permanecem como estão
- O cálculo de `best_points` deve ser feito nos módulos de exibição/ordenação (ou como propriedade/método auxiliar)

## Requisitos Não-Funcionais

### RNF01 — Retrocompatibilidade
- A alteração não deve quebrar a estrutura dos arquivos JSON/CSV existentes
- A mensagem Telegram deve respeitar o limite de 4096 caracteres

### RNF02 — Manutenibilidade
- A lógica de cálculo de `best_points` deve estar centralizada (evitar duplicação em 3 arquivos)
- Sugestão: criar uma função auxiliar ou propriedade no modelo para calcular `best_points`

### RNF03 — Performance
- O cálculo de `max()` é trivial e não deve impactar a performance da extração

## Critérios de Aceite

- [ ] **CA-01:** A ordenação na notificação Telegram usa `max(points, points_club)` em vez de apenas `points`
- [ ] **CA-02:** A ordenação no filtro de categorias usa `max(points, points_club)` em vez de apenas `points`
- [ ] **CA-03:** A ordenação no summary do console usa `max(points, points_club)` em vez de apenas `points`
- [ ] **CA-04:** A mensagem Telegram exibe a tag `🏆 (Clube)` quando `points_club > points`
- [ ] **CA-05:** O summary do console exibe a tag `🏆` quando `points_club > points`
- [ ] **CA-06:** Quando `points >= points_club`, a exibição permanece como antes (sem tag de Clube)
- [ ] **CA-07:** O salvamento em JSON continua incluindo TODOS os parceiros com TODOS os campos
- [ ] **CA-08:** O salvamento em CSV continua incluindo TODOS os parceiros com TODOS os campos
- [ ] **CA-09:** Parceiros com `points_club = 0` usam `points` normalmente (sem tag de Clube)
- [ ] **CA-10:** O campo `points_base` (BAU) **NÃO** é considerado no cálculo de `best_points`

## Arquivos Impactados

| Arquivo | Alteração necessária |
|---------|---------------------|
| `src/notifier.py` | Ordenar por `best_points`; exibir tag 🏆 (Clube) quando aplicável |
| `src/filters.py` | Ordenar por `best_points` em vez de `parity.points` |
| `src/scheduler.py` | Ordenar e exibir por `best_points`; tag 🏆 quando aplicável |
| `src/models/parity.py` | *(Opcional)* Adicionar propriedade `best_points` para centralizar lógica |

## Fora do Escopo

- Alteração no scraper (`src/scraper.py`) — já extrai `parityClub` corretamente
- Alteração na estrutura dos arquivos JSON/CSV
- Criação de nova categoria de filtro para parceiros exclusivos do Clube
- Interface ou configuração dinâmica para escolher qual categoria priorizar
- Considerar `points_base` no cálculo de melhor pontuação

## Riscos e Dependências

| Risco/Dependência | Mitigação |
|-------------------|-----------|
| Parceiros com `points_club = 0` (não participam do Clube) | `max()` naturalmente retorna `points`; sem impacto |
| Empate entre `points` e `points_club` | Quando iguais, não exibir tag de Clube (comportamento normal) |
| Mudança futura na API da Livelo (novos campos de pontuação) | Lógica centralizada facilita extensão |

## Prioridade

**Alta** — A ausência da consideração do Clube faz com que o sistema exiba pontuações menores do que as realmente disponíveis, reduzindo o valor da notificação para o usuário. Exemplo concreto: Riachuelo mostra 8 pts quando na verdade oferece 10 pts via Clube.
