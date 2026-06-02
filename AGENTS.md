# AGENTS.md — LiveloScrapper

> Arquivo de memória e convenções para agentes de IA (Devin, Cursor, etc.) trabalhando neste projeto.

---

## 1. Skills Disponíveis

As skills abaixo estão registradas em `.devin/skills/` e podem ser invocadas via `skill({ name: "..." })`.

| Skill | Quando Usar | Não Faz |
|-------|-------------|---------|
| `tech-lead-py` | Design arquitetural, ADR, decisões técnicas não-triviais | Nunca escreve código |
| `senior-dev-py` | Implementação de feature com TDD, código idiomático Python | Nunca escreve specs ou SDDs |
| `pm-analyst-py` | Análise de demandas, escrita de specs, critérios de aceite | Nunca implementa |
| `qa-engineer-py` | Review de código, validação de critérios de aceite, criação de PRs | Nunca implementa código |
| `bugfix-workflow-py` | Correção de bugs regressivos em código existente | Não substitui feature-workflow-py para novas funcionalidades |
| `testing-livelo-scrapper` | Validação end-to-end do scraper, Docker, scheduler, output | Testa o sistema completo |

### 1.1 Escolha de Skill por Tipo de Trabalho

```
NOVA FEATURE (média/grande)
  → pm-analyst-py → tech-lead-py → senior-dev-py → qa-engineer-py

NOVA FEATURE (pequena/trivial)
  → senior-dev-py → qa-engineer-py

CORREÇÃO DE BUG
  → bugfix-workflow-py (fluxo enxuto)
    → Escalar para tech-lead-py se arquitetural
    → Escalar para pm-analyst-py se regra de negócio ambígua
    → Chamar qa-engineer-py na fase de validação

VALIDAÇÃO / SANITY CHECK
  → testing-livelo-scrapper
```

---

## 2. Fluxo de Bugfix (bugfix-workflow-py)

Para correções de bugs, usar obrigatoriamente o fluxo leve documentado em `.devin/skills/bugfix-workflow-py/SKILL.md`.

### 2.1 Fases

1. **Investigação + Reprodução**
   - Coletar stacktrace, logs, git blame
   - Isolar input mínimo que reproduz o bug
   - Escrever teste que **FALHA** antes de tocar código de produção

2. **Correção**
   - Menor diff possível (≤ 50 linhas ideal)
   - Passar teste de reprodução
   - Rodar suite completa (`pytest`) para evitar regressão
   - **1 commit** com mensagem clara

3. **Validação + PR**
   - Self-review do diff
   - Rodar testes E2E (`testing-livelo-scrapper`) se disponíveis
   - Criar PR com root cause descrito

### 2.2 Artefato Obrigatório: `docs/bugs/fix-{bugName}/`

> **REGRA CRÍTICA**: Todo bugfix deve gerar um artefato documental em `docs/bugs/fix-{bugName}/bug-report.md`.

**Por que:**
- Histórico técnico para investigações futuras de regressão
- Base de conhecimento de causas raiz recorrentes
- Onboarding de novos devs com casos reais

**Como criar:**
```bash
mkdir -p docs/bugs/fix-{bugName}
cp docs/bugs/TEMPLATE.md docs/bugs/fix-{bugName}/bug-report.md
# Preencher todas as seções do template
```

**Seções obrigatórias do artefato:**
- Metadados (identificador, data, autor, severidade, commit)
- Sintoma (stacktrace ou descrição)
- Causa Raiz (o POR QUÊ, não só o O QUÊ)
- Reprodução (input mínimo)
- Correção Aplicada (diff/descrição)
- Validação (checklist + evidências)
- Lições Aprendidas / Prevenção

**Checklist de entrega do bugfix:**
- [ ] Código corrigido e testado
- [ ] Teste de regressão adicionado
- [ ] `pytest` passando sem regressões
- [ ] `ruff check` limpo
- [ ] Artefato `docs/bugs/fix-{bugName}/bug-report.md` criado e preenchido
- [ ] PR criado com root cause descrito

---

## 3. Stack e Convenções

| Aspecto | Convenção |
|---------|-----------|
| Linguagem | Python 3.12 |
| Scraping | requests + BeautifulSoup4 |
| Persistência | JSON + CSV (filesystem) |
| Agendamento | schedule |
| Notificação | Telegram Bot API |
| Container | Docker + docker-compose |
| Testes | pytest |
| Lint | ruff |
| Código/logs | Português (BR) |
| Variáveis/funções | Inglês (snake_case) |
| Type hints | Nativos do Python (não obrigatório mypy) |
| Máx linhas por função | 20 |
| Máx commits por bugfix | 1 |

### 3.1 Estrutura de Diretórios

```
LiveloScrapper/
├── main.py
├── src/
│   ├── scraper.py
│   ├── filters.py
│   ├── storage.py
│   ├── scheduler.py
│   └── notifier.py
├── data/
├── docs/
│   ├── bugs/                    # Artefatos de bugfix (OBRIGATÓRIO)
│   │   ├── TEMPLATE.md
│   │   └── fix-{bugName}/
│   │       └── bug-report.md
│   ├── {featureName}/            # Docs por feature
│   ├── regras-de-negocio.md
│   └── fluxo-de-desenvolvimento.md
├── .devin/skills/               # Skills do projeto
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 4. Critérios de Escalação

| Situação | Ação |
|----------|------|
| Bug é sintoma de problema arquitetural | Escalar para `tech-lead-py` na Fase 1 |
| Regra de negócio não documentada / ambígua | Escalar para `pm-analyst-py` na Fase 1 |
| Fix quebra contrato de API ou schema de DB | `tech-lead-py` revisar antes da Fase 2 |
| Correção > 150 linhas de diff | `tech-lead-py` validar se não deveria ser feature |
| Bug reaparece frequentemente | `tech-lead-py` propor refatoração após Fase 3 |

---

## 5. Comandos de Verificação

```bash
# Testes
pytest

# Lint
ruff check .

# Build Docker
docker build -t livelo-scrapper:test .
docker-compose up -d

# Testes E2E / integração
skill({ name: "testing-livelo-scrapper" })
```

---

> Última atualização: 2026-06-01 — Adicionado fluxo de bugfix e artefato obrigatório em `docs/bugs/`.
