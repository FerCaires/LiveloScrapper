# Fluxo de Desenvolvimento - LiveloScrapper

> Este documento é a base de conhecimento consolidada do fluxo de desenvolvimento do projeto LiveloScrapper.
> **IMPORTANTE:** Este documento deve ser atualizado a cada nova feature para manter-se sempre na versão mais recente.

---

## 1. Arquitetura do Projeto

### Estrutura de Pastas
```
LiveloScrapper/
├── main.py                          # Ponto de entrada CLI e scheduler
├── Dockerfile                       # Imagem Docker
├── docker-compose.yml               # Orquestração do container
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── parity.py                # Dataclass ParityInfo
│   │   └── partner.py               # Dataclass Partner
│   ├── scraper.py                   # Lógica de extração (parsing __NEXT_DATA__)
│   ├── storage.py                   # Persistência JSON/CSV em /data
│   └── scheduler.py                 # Agendamento diário às 10:00 BRT
├── data/                            # Resultados das extrações
├── docs/                            # Documentação por feature
│   ├── regras-de-negocio.md         # Base de conhecimento: regras de negócio
│   ├── fluxo-de-desenvolvimento.md  # Base de conhecimento: fluxo de dev
│   └── {featureName}/
│       ├── spec-{featureName}.md    # Especificação (PM)
│       ├── plan-{featureName}.md    # Plano técnico (Tech Lead)
│       ├── tasks-{featureName}.md   # Tarefas de implementação (Dev)
│       └── tests-{featureName}.md   # Relatório de QA
├── .github/workflows/scrape.yml     # GitHub Actions
├── requirements.txt
└── README.md
```

### Stack Tecnológica
- **Linguagem:** Python 3.12
- **Parsing HTML:** BeautifulSoup4
- **HTTP:** Requests
- **Dados:** Pandas (CSV/JSON)
- **Containerização:** Docker / Docker Compose
- **CI/CD:** GitHub Actions
- **Timezone:** America/Sao_Paulo (BRT)

## 2. Padrões de Código

- **Dataclasses** para modelos de dados (`src/models/`)
- **Separação de responsabilidades:** scraper, storage, scheduler
- **Nomenclatura:** snake_case para funções/variáveis, PascalCase para classes
- **Idioma do código:** Inglês para nomes de variáveis/funções, Português para docs/comments

## 3. Fluxo de Desenvolvimento por Feature

Cada nova feature segue o workflow padronizado:

1. **PM** → Cria `docs/{featureName}/spec-{featureName}.md` com requisitos e critérios de aceite
2. **Tech Lead** → Cria `docs/{featureName}/plan-{featureName}.md` com spec técnica e tarefas
3. **Developer** → Implementa + cria `docs/{featureName}/tasks-{featureName}.md` + PR
4. **QA** → Testa + cria `docs/{featureName}/tests-{featureName}.md` + relatório

### Documentação Obrigatória por Feature
Toda feature DEVE ter os 4 arquivos na pasta `docs/{featureName}/`:
- `spec-{featureName}.md` — Especificação de requisitos
- `plan-{featureName}.md` — Plano técnico
- `tasks-{featureName}.md` — Registro de implementação
- `tests-{featureName}.md` — Relatório de QA

### Base de Conhecimento
Além dos docs por feature, dois arquivos devem ser atualizados a cada entrega:
- `docs/regras-de-negocio.md` — Regras de negócio (atualizado pelo PM e QA)
- `docs/fluxo-de-desenvolvimento.md` — Fluxo de dev (atualizado pelo Tech Lead e QA)

## 4. Como Executar

| Ação | Comando |
|------|---------|
| Execução única | `python main.py` |
| Com agendamento | `python main.py --schedule` |
| Via Docker | `docker compose up -d` |
| Build Docker | `docker build -t livelo-scrapper-test .` |
| Verificar timezone | `docker run --rm livelo-scrapper-test date +"%Z %z"` |

## 5. Deploy e CI/CD

- **GitHub Actions** (`.github/workflows/scrape.yml`): execução automática diária
- **Docker Compose**: execução contínua com timezone configurado
- Resultados disponíveis como artefatos do workflow

## 6. Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| BeautifulSoup4 para parsing | Simplicidade e confiabilidade para extração de HTML |
| __NEXT_DATA__ como fonte | Dados estruturados já disponíveis no JSON embutido |
| Docker com TZ fixo | Garantir horário correto de execução (BRT) |
| JSON + CSV dual storage | Flexibilidade para análise (CSV) e programática (JSON) |
| Rede Docker isolada (livelo-network) | Segurança e isolamento do serviço |

---

## Histórico de Atualizações

| Data | Feature | Alteração |
|------|---------|----------|
| 2026-05-10 | Documento inicial | Criação da base de conhecimento com fluxo existente |
