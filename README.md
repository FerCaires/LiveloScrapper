# LiveloScrapper

Extração automática diária dos parceiros e pontuações do programa de pontos [Livelo](https://www.livelo.com.br).

## Funcionalidades

- Extrai dados de **todos os parceiros** da Livelo (200+ parceiros)
- Captura **pontuação por real/dólar**, incluindo promoções ativas
- Salva os resultados em **JSON** e **CSV** com data da extração
- **Agendamento diário** às 10:00 (horário de Brasília)
- **Docker** com timezone configurado para execução contínua
- **GitHub Actions** para execução automática sem servidor

## Dados extraídos por parceiro

| Campo | Descrição |
|-------|-----------|
| `id` | Código do parceiro |
| `name` | Nome do parceiro |
| `categories` | Categorias (ex: eletrônicos, moda) |
| `currency` | Moeda (R$ ou U$) |
| `points` | Pontos por unidade de moeda (atual) |
| `points_club` | Pontos para membros do Clube Livelo |
| `points_base` | Pontuação base (sem promoção) |
| `is_promotion` | Se está em promoção |
| `promotion_start` / `promotion_end` | Período da promoção |

## Requisitos

- **Docker** (recomendado) ou Python 3.10+

## Uso com Docker (recomendado)

### Iniciar o container (execução diária às 10:00 BRT)

```bash
docker compose up -d
```

O container roda continuamente com timezone `America/Sao_Paulo` e executa a extração todos os dias às 10:00. Os resultados são salvos na pasta `data/` via volume montado.

### Executar uma extração manualmente no container

```bash
docker compose run --rm scraper python main.py
```

### Ver logs

```bash
docker compose logs -f scraper
```

### Parar

```bash
docker compose down
```

## Uso sem Docker

### Criação de ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalação

```bash
git clone https://github.com/FerCaires/LiveloScrapper.git
cd LiveloScrapper
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuração do Telegram (opcional)

Para receber notificações via Telegram após cada extração:

1. Crie um bot no [@BotFather](https://t.me/botfather) e obtenha o token
2. Inicie uma conversa com seu bot e envie uma mensagem
3. Obtenha o chat ID fazendo uma requisição GET para:  
   `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
4. Copie o arquivo `.env.example` para `.env` e preencha as variáveis:

```bash
cp .env.example .env
# Edite o .env com seu token e chat ID
```

### Execução única

```bash
python main.py
```

### Agendamento diário (10:00 horário de Brasília)

```bash
python main.py --schedule
```

### GitHub Actions (automático)

O workflow `.github/workflows/scrape.yml` executa a extração automaticamente todos os dias às 10:00 (BRT). Os resultados ficam disponíveis como artefatos do workflow.

Para executar manualmente: vá em **Actions** > **Livelo Daily Scraper** > **Run workflow**.

## Estrutura do Projeto

```
LiveloScrapper/
├── main.py                          # Ponto de entrada
├── Dockerfile                       # Imagem Docker
├── docker-compose.yml               # Orquestração do container
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── parity.py                # Dataclass ParityInfo
│   │   └── partner.py               # Dataclass Partner
│   ├── scraper.py                   # Lógica de extração
│   ├── storage.py                   # Salvamento em JSON/CSV
│   └── scheduler.py                 # Agendamento diário
├── data/                            # Resultados das extrações
├── .github/workflows/scrape.yml     # GitHub Actions
├── requirements.txt
└── README.md
```

## Exemplo de saída (JSON)

```json
{
  "id": "MCL",
  "name": "Mercado Livre",
  "categories": "todos marketplace",
  "parity": {
    "currency": "R$",
    "currency_value": 1,
    "points": 2,
    "points_club": 2,
    "points_base": 1,
    "is_promotion": true,
    "promotion_start": "2026-04-28-00:00:00 GMT-03:00",
    "promotion_end": "2026-05-10-23:59:00 GMT-03:00",
    "campaign_type": "PROMOTION"
  },
  "extracted_at": "2026-05-09 18:45:00"
}
```
