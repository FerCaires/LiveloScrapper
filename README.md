# LiveloScrapper

Extração automática diária dos parceiros e pontuações do programa de pontos [Livelo](https://www.livelo.com.br).

## Funcionalidades

- Extrai dados de **todos os parceiros** da Livelo (200+ parceiros)
- Captura **pontuação por real/dólar**, incluindo promoções ativas
- Salva os resultados em **JSON** e **CSV** com data da extração
- **Agendamento diário** às 10:00 (horário de Brasília)
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

- Python 3.10+

## Instalação

```bash
git clone https://github.com/FerCaires/LiveloScrapper.git
cd LiveloScrapper
pip install -r requirements.txt
```

## Uso

### Execução única

```bash
python main.py
```

Os resultados serão salvos na pasta `data/` em JSON e CSV.

### Agendamento diário (10:00 horário de Brasília)

```bash
python main.py --schedule
```

O processo ficará ativo e executará a extração diariamente às 10:00.

### GitHub Actions (automático)

O workflow `.github/workflows/scrape.yml` executa a extração automaticamente todos os dias às 10:00 (BRT). Os resultados ficam disponíveis como artefatos do workflow.

Para executar manualmente: vá em **Actions** > **Livelo Daily Scraper** > **Run workflow**.

## Estrutura do Projeto

```
LiveloScrapper/
├── main.py                          # Ponto de entrada
├── src/
│   ├── __init__.py
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
