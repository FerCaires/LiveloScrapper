---
name: testing-livelo-scrapper
description: Test the LiveloScrapper end-to-end. Use when verifying scraper, Docker, scheduler, or data output changes.
---

# Testing LiveloScrapper

This project is a Python CLI scraper (no web UI). All testing is shell-based — do NOT record.

## Prerequisites

- Docker installed and running
- No secrets or credentials needed (scraper accesses public Livelo page)

## How the Scraper Works

- Fetches `https://www.livelo.com.br/juntar-pontos/todos-os-parceiros`
- Parses `__NEXT_DATA__` JSON embedded in the HTML (Next.js SSR page)
- Extracts partner data from the `cb_partner_list` component inside `props.pageProps.page.components`
- Saves results to `data/` as dated JSON and CSV files

## Test Procedure

### 1. Docker Build
```bash
cd /path/to/LiveloScrapper
docker build -t livelo-scrapper-test .
```
Expect: exit code 0.

### 2. Timezone Verification
```bash
docker run --rm livelo-scrapper-test date +"%Z %z"
```
Expect: `-03 -0300` (BRT). If it shows UTC, the Dockerfile timezone config is broken.

### 3. Single Extraction
```bash
docker run --rm -v $(pwd)/data:/app/data livelo-scrapper-test python main.py
```
Expect:
- Exit code 0
- Log: `parceiros encontrados` with count >= 200
- Files: `data/livelo_parceiros_YYYY-MM-DD.json` and `.csv` created
- JSON: array of objects with keys `id`, `name`, `parity.currency`, `parity.points`
- At least 1 partner with `parity.is_promotion = true`

### 4. CSV Validation
Check the CSV has headers: `id,name,categories,currency,currency_value,points,points_club,points_base,is_promotion,...`
Data rows should have non-empty `id` and `name` values.

### 5. Scheduler Mode
```bash
docker run --rm livelo-scrapper-test timeout 5 python main.py --schedule || true
```
Expect output containing `execução diária às 10:00` and `Próxima execução:` with a valid datetime.

### 6. docker-compose Lifecycle
```bash
docker compose up -d && sleep 5 && docker compose ps && docker compose logs && docker compose down
```
Expect: container shows as running, logs show scheduler started with next run at 10:00.

## Common Issues

- If Livelo changes their page structure, the `cb_partner_list` component type or `__NEXT_DATA__` format might change. Check `src/scraper.py` and verify the component type name and data path.
- The page returns 200+ partners. If the count drops significantly, Livelo may have changed their rendering approach (e.g., moved to client-side fetching).
- Timezone issues: ensure `TZ=America/Sao_Paulo` is set both in the Dockerfile and docker-compose.yml.

## Devin Secrets Needed

None — the scraper accesses a public page without authentication.
