# Fluxo de Desenvolvimento — LiveloScrapper

## 1. Stack Tecnológica

| Componente | Tecnologia |
|-----------|------------|
| Linguagem | Python 3.12 |
| Scraping | requests + BeautifulSoup4 |
| Persistência | JSON + CSV (filesystem local) |
| Agendamento | schedule (lib Python) |
| Notificação | Telegram Bot API (requests) |
| Container | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Timezone | America/Sao_Paulo |

## 2. Estrutura do Projeto

```
LiveloScrapper/
├── main.py                    # Entrypoint CLI
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── parity.py          # Dataclass ParityInfo
│   │   └── partner.py         # Dataclass Partner
│   ├── scraper.py             # Extração via __NEXT_DATA__
│   ├── filters.py             # Filtros de parceiros por categoria
│   ├── storage.py             # Persistência JSON/CSV
│   ├── scheduler.py           # Agendamento e orquestração do job
│   └── notifier.py            # Notificação Telegram
├── data/                      # Outputs das extrações
├── docs/                      # Documentação por feature
│   ├── regras-de-negocio.md
│   ├── fluxo-de-desenvolvimento.md
│   └── {featureName}/         # Docs específicos da feature
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/
```

## 3. Padrões de Arquitetura

### 3.1 Separação de Responsabilidades
- **scraper.py** → Apenas extração de dados (sem filtro, sem salvamento)
- **filters.py** → Lógica de filtro pura (sem I/O, sem side effects)
- **storage.py** → Apenas persistência (JSON/CSV)
- **notifier.py** → Apenas envio de notificação
- **scheduler.py** → Orquestração do fluxo (chama scraper → storage → filters → notifier)

### 3.2 Modelos de Dados
- Uso de `dataclass` do Python para modelos (Partner, ParityInfo)
- Sem ORM — persistência direta em arquivos

### 3.3 Configuração
- Variáveis de ambiente via `.env` (dotenv)
- Constantes de negócio como variáveis de módulo (ex: `FILTERED_CATEGORIES` em filters.py)

## 4. Convenções

- Código e logs em **português** (BR) onde aplicável
- Docstrings em **português**
- Nomes de variáveis e funções em **inglês** (snake_case)
- Tipagem via type hints nativos do Python (sem mypy obrigatório)
- Logging via módulo `logging` padrão

## 5. Fluxo de Execução

```
main.py → job() ou start_scheduler()
  job():
    1. scrape_partners()        → Lista completa de parceiros
    2. save_json(partners)      → Salva todos em JSON
    3. save_csv(partners)       → Salva todos em CSV
    4. filter_by_category()     → Filtra para notificação/summary
    5. send_telegram_notification(filtered)
    6. _print_summary(filtered)
```

## 6. Docker

- Imagem base: `python:3.12-slim`
- Timezone definida via `TZ=America/Sao_Paulo`
- Volume `./data:/app/data` para persistência
- Rede isolada `livelo-network`
