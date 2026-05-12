# Spec Técnica: Clube Category

**Feature Name:** clube-category
**Data:** 2026-05-12
**Autor:** Tech Lead Agent

---

## Resumo

Ajustar os módulos de **notificação** (`notifier.py`), **filtro** (`filters.py`) e **summary** (`scheduler.py`) para utilizarem a **maior pontuação disponível** entre `points` e `points_club` na ordenação e exibição. Adicionar indicador visual `🏆 (Clube)` quando a melhor pontuação provém do Clube Livelo. A persistência (JSON/CSV) e o scraper permanecem inalterados.

## Arquitetura

### Visão Geral

A mudança é cirúrgica e de baixo risco: centralizar o cálculo de `best_points` como `@property` no modelo `ParityInfo` e substituir as referências diretas a `parity.points` nos três módulos de exibição/ordenação.

```
ParityInfo (modelo)
  ├── best_points (nova @property) → max(points, points_club)
  └── is_club_best (nova @property) → points_club > points

Módulos consumidores:
  ├── notifier.py  → ordena por best_points, exibe 🏆 (Clube)
  ├── filters.py   → ordena por best_points
  └── scheduler.py → ordena por best_points, exibe 🏆
```

### Decisão Arquitetural: `@property` no modelo vs. função auxiliar

| Critério | `@property` no modelo | Função auxiliar em módulo separado |
|----------|----------------------|-----------------------------------|
| Centralização | No próprio objeto — acesso direto `parity.best_points` | Requer import e chamada `best_points(parity)` |
| Impacto na serialização | Nenhum — `dataclasses.asdict()` ignora properties | Nenhum |
| Consistência com codebase | O projeto já usa `@dataclass` — properties são idiomáticas | Adicionaria um módulo ou função avulsa |
| Manutenibilidade | Lógica acoplada ao dado que ela opera | Lógica separada do dado |

**Decisão:** Usar `@property` no `ParityInfo`. É a abordagem mais Pythonica, centralizada, e não altera os campos do dataclass (satisfaz RF07 e RNF02). A função `dataclasses.asdict()` usada em `storage.py` **não serializa properties**, portanto a persistência permanece intacta.

## Stack / Tecnologias

- **Linguagem:** Python 3.12
- **Sem novas dependências** — apenas alterações em código existente
- Frameworks e bibliotecas permanecem os mesmos (requests, BeautifulSoup4, schedule)

## Convenções de Código

- Código em português (BR): docstrings, logs e mensagens internas em português
- Nomes de variáveis e funções em inglês (snake_case), conforme padrão existente
- Tipagem via type hints nativos do Python
- Properties seguem o padrão `@property` do Python, sem setter (read-only)

## Mudanças no Código

### Arquivos a Modificar

| Arquivo | Mudança |
|---------|--------|
| `src/models/parity.py` | Adicionar properties `best_points` e `is_club_best` |
| `src/notifier.py` | Ordenar por `best_points`; exibir `best_points` no ranking; tag `🏆 (Clube)` quando `is_club_best` |
| `src/filters.py` | Ordenar por `best_points` em vez de `points` |
| `src/scheduler.py` | Ordenar por `best_points`; exibir `best_points` no ranking; tag `🏆` quando `is_club_best` |

### Arquivos Inalterados

| Arquivo | Motivo |
|---------|--------|
| `src/scraper.py` | Já extrai `parityClub` corretamente |
| `src/storage.py` | `asdict()` ignora properties; serialização intacta |
| `src/models/partner.py` | Sem mudanças |
| `main.py` | Sem mudanças |

## Detalhamento da Implementação

### 1. `src/models/parity.py` — Adicionar properties

```python
@dataclass
class ParityInfo:
    # ... campos existentes inalterados ...

    @property
    def best_points(self) -> int:
        """Retorna a melhor pontuação entre normal/promoção e Clube."""
        return max(self.points, self.points_club)

    @property
    def is_club_best(self) -> bool:
        """Indica se a melhor pontuação provém do Clube Livelo."""
        return self.points_club > self.points
```

**Notas:**
- `best_points` retorna `max(points, points_club)` — `points_base` **NÃO** participa
- `is_club_best` usa `>` estrito: quando `points == points_club`, retorna `False` (sem tag)
- Parceiros com `points_club = 0` → `max(points, 0)` = `points` (comportamento correto)

### 2. `src/notifier.py` — `_build_message()`

**Antes (linha 45):**
```python
sorted_partners = sorted(partners, key=lambda p: p.parity.points, reverse=True)
```

**Depois:**
```python
sorted_partners = sorted(partners, key=lambda p: p.parity.best_points, reverse=True)
```

**Antes (linhas 56-59) — formatação da linha:**
```python
line = (
    f"{i}. {partner.name} - {partner.parity.points} pts/"
    f"{partner.parity.currency}{partner.parity.currency_value}"
)
```

**Depois:**
```python
club_tag = " 🏆 (Clube)" if partner.parity.is_club_best else ""
line = (
    f"{i}. {partner.name} - {partner.parity.best_points} pts/"
    f"{partner.parity.currency}{partner.parity.currency_value}"
    f"{club_tag}"
)
```

**Formato resultante:**
```
1. Riachuelo - 10 pts/R$1 🏆 (Clube)
2. Amazon - 8 pts/R$1
```

### 3. `src/filters.py` — `filter_partners_by_category()`

**Antes (linha 43):**
```python
filtered.sort(key=lambda p: p.parity.points, reverse=True)
```

**Depois:**
```python
filtered.sort(key=lambda p: p.parity.best_points, reverse=True)
```

**Atualizar a docstring** para refletir que a ordenação agora é por `best_points`:
```python
"""...ordenada por melhor pontuação (``parity.best_points``) em ordem decrescente."""
```

### 4. `src/scheduler.py` — `_print_summary()`

**Antes (linha 61):**
```python
for p in sorted(partners, key=lambda x: x.parity.points, reverse=True):
```

**Depois:**
```python
for p in sorted(partners, key=lambda x: x.parity.best_points, reverse=True):
```

**Antes (linhas 62-66) — exibição:**
```python
promo_tag = " ⭐" if p.parity.is_promotion else ""
print(
    f"  {p.name:<30} {p.parity.points} pts/"
    f"{p.parity.currency}{p.parity.currency_value} "
    f"(base: {p.parity.points_base}){promo_tag}"
)
```

**Depois:**
```python
promo_tag = " ⭐" if p.parity.is_promotion else ""
club_tag = " 🏆" if p.parity.is_club_best else ""
print(
    f"  {p.name:<30} {p.parity.best_points} pts/"
    f"{p.parity.currency}{p.parity.currency_value} "
    f"(base: {p.parity.points_base}){promo_tag}{club_tag}"
)
```

**Formato resultante:**
```
Riachuelo                      10 pts/R$1 (base: 5) 🏆
Amazon                          8 pts/R$1 (base: 3) ⭐
Magazine Luiza                  12 pts/R$1 (base: 4) ⭐🏆
```

> **Nota sobre stacking de tags:** Um parceiro pode ter AMBAS as tags quando `is_promotion=True` **e** `points_club > points` simultaneamente. Ex: promoção ativa de 8 pts mas Clube oferece 12 pts. A tag ⭐ indica promoção ativa; 🏆 indica que a melhor pontuação vem do Clube. São informações ortogonais e complementares.

## Modelos de Dados

Sem alterações nos campos do `ParityInfo` (RF07). Apenas adição de duas `@property` computadas:

| Property | Tipo | Descrição |
|----------|------|-----------|
| `best_points` | `int` | `max(self.points, self.points_club)` |
| `is_club_best` | `bool` | `self.points_club > self.points` |

Verificação de compatibilidade com `dataclasses.asdict()`:
- `asdict()` só serializa **fields** (definidos no `@dataclass`)
- Properties são **descriptors** e **não** são incluídas no output de `asdict()`
- Portanto: `save_json()` e `save_csv()` em `storage.py` **continuam funcionando identicamente**

## API / Endpoints

Não se aplica — o projeto não expõe APIs REST. A interface é via Telegram Bot API (consumo) e console (stdout).

## Tarefas de Implementação

1. [ ] Adicionar `@property best_points` e `@property is_club_best` em `src/models/parity.py` — **Estimativa: 15 min**
2. [ ] Atualizar ordenação e exibição em `src/notifier.py` (`_build_message`) — **Estimativa: 15 min**
3. [ ] Atualizar ordenação em `src/filters.py` (`filter_partners_by_category`) e docstring — **Estimativa: 10 min**
4. [ ] Atualizar ordenação e exibição em `src/scheduler.py` (`_print_summary`) — **Estimativa: 15 min**
5. [ ] Testes manuais: executar `python main.py` e validar output do summary no console — **Estimativa: 15 min**
6. [ ] Testes manuais: validar mensagem Telegram (com bot de teste ou mock) — **Estimativa: 15 min**
7. [ ] Build Docker e validação em container — **Estimativa: 10 min**

**Total estimado:** ~1h30

## Testes Necessários

### Testes Unitários (sugeridos)
- [ ] `ParityInfo.best_points` retorna `max(points, points_club)` para diferentes combinações
- [ ] `ParityInfo.best_points` com `points_club = 0` retorna `points`
- [ ] `ParityInfo.is_club_best` retorna `True` quando `points_club > points`
- [ ] `ParityInfo.is_club_best` retorna `False` quando `points == points_club`
- [ ] `ParityInfo.is_club_best` retorna `False` quando `points > points_club`
- [ ] `dataclasses.asdict(parity)` **não** inclui `best_points` nem `is_club_best`

### Testes de Integração (sugeridos)
- [ ] `filter_partners_by_category()` ordena por `best_points` (não por `points`)
- [ ] `_build_message()` exibe `best_points` e tag `🏆 (Clube)` quando aplicável
- [ ] `_print_summary()` exibe `best_points` e tags `⭐`/`🏆` corretamente
- [ ] `_print_summary()` exibe ambas as tags `⭐🏆` quando parceiro tem promoção E clube melhor

### Testes E2E (sugeridos)
- [ ] Execução completa via `python main.py` — validar summary no console
- [ ] Build Docker: `docker build -t livelo-scrapper-test . && docker run --rm livelo-scrapper-test python main.py`
- [ ] Validar que JSON/CSV gerados mantêm todos os campos originais sem `best_points`

## Riscos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| `points_club = 0` para parceiros sem Clube | Alta (esperado) | Nenhum | `max(points, 0) = points` — comportamento correto por definição |
| Empate `points == points_club` | Média | Nenhum | `is_club_best` usa `>` estrito → `False` → sem tag (RF02/CA-06) |
| `asdict()` inclui properties em versão futura do Python | Muito baixa | Alto | Validar com teste unitário; monitorar changelogs do Python |
| Mensagem Telegram excede 4096 chars com tags extras | Baixa | Médio | Tag `🏆 (Clube)` adiciona ~14 chars/linha × 20 linhas = ~280 chars. Margem confortável. Truncamento existente já protege. |
| Mudança na API Livelo (novos tipos de pontuação) | Baixa | Médio | Lógica centralizada em `@property` facilita extensão futura |

## Decisões de Design

| # | Decisão | Justificativa |
|---|---------|---------------|
| 1 | `@property` no `ParityInfo` em vez de função auxiliar | Centraliza a lógica no objeto, é idiomático em Python, não altera serialização |
| 2 | Duas properties separadas (`best_points` e `is_club_best`) | Separação de responsabilidades: uma para o valor, outra para a flag visual |
| 3 | `is_club_best` usa `>` estrito (não `>=`) | Quando iguais, não há vantagem do Clube — manter comportamento original |
| 4 | Tags ⭐ e 🏆 são independentes e podem coexistir | Representam informações ortogonais (promoção vs. origem da melhor pontuação) |
| 5 | Tag no Telegram: `🏆 (Clube)` / Tag no summary: `🏆` | Telegram precisa do texto "(Clube)" por ser contexto único; summary já tem cabeçalho explicativo |
| 6 | Não alterar campos do `@dataclass` | Satisfaz RF07; properties não são campos e não afetam `__init__`, `__repr__`, `asdict()` |

## Cenários de Exemplo

| Parceiro | points | points_club | best_points | is_club_best | Tags (summary) |
|----------|--------|-------------|-------------|-------------|----------------|
| Riachuelo | 8 | 10 | 10 | `True` | 🏆 |
| Amazon | 8 | 0 | 8 | `False` | (nenhuma) |
| Netshoes | 5 | 5 | 5 | `False` | (nenhuma) |
| Magazine Luiza | 6 | 12 | 12 | `True` | ⭐🏆 (se is_promotion=True) |
| Centauro | 10 | 3 | 10 | `False` | ⭐ (se is_promotion=True) |

## Checklist de Critérios de Aceite

| CA | Descrição | Implementação |
|----|-----------|---------------|
| CA-01 | Ordenação Telegram usa `best_points` | `notifier.py` → `sorted(..., key=lambda p: p.parity.best_points)` |
| CA-02 | Ordenação filtro usa `best_points` | `filters.py` → `filtered.sort(key=lambda p: p.parity.best_points)` |
| CA-03 | Ordenação summary usa `best_points` | `scheduler.py` → `sorted(..., key=lambda x: x.parity.best_points)` |
| CA-04 | Tag `🏆 (Clube)` no Telegram | `notifier.py` → `club_tag = " 🏆 (Clube)" if partner.parity.is_club_best else ""` |
| CA-05 | Tag `🏆` no summary | `scheduler.py` → `club_tag = " 🏆" if p.parity.is_club_best else ""` |
| CA-06 | Sem tag quando `points >= points_club` | `is_club_best` retorna `False` → tag vazia |
| CA-07 | JSON salva todos os parceiros/campos | Sem alteração em `storage.py` |
| CA-08 | CSV salva todos os parceiros/campos | Sem alteração em `storage.py` |
| CA-09 | `points_club=0` usa `points` sem tag | `max(points, 0) = points`; `0 > points` → `False` |
| CA-10 | `points_base` não entra no cálculo | `best_points = max(self.points, self.points_club)` — sem `points_base` |
