# Regras de Negócio - LiveloScrapper

> Este documento é a base de conhecimento consolidada das regras de negócio do projeto LiveloScrapper.
> **IMPORTANTE:** Este documento deve ser atualizado a cada nova feature para manter-se sempre na versão mais recente.

---

## 1. Domínio do Negócio

O LiveloScrapper é um sistema ETL automatizado para extração diária das paridades de acúmulo de pontos do programa de fidelidade **Livelo**.

## 2. Conceitos e Terminologias

| Termo | Definição |
|-------|----------|
| **Paridade de Acúmulo** | Razão de pontos ganhos por unidade de moeda gasta |
| **Partner (Parceiro)** | Comerciante terceiro integrado à Livelo (ex: Amazon, Mercado Livre) |
| **Points Base** | Taxa padrão de acúmulo (sem promoção) |
| **Points Club** | Taxa preferencial para assinantes do Clube Livelo |
| **BAU (Business As Usual)** | Estado operacional padrão sem promoções ativas |
| **Is Promotion** | Flag booleana que indica se a paridade excede a taxa base |
| **Campaign Type** | Tipo da campanha (ex: PROMOTION) |
| **__NEXT_DATA__** | Blob JSON embutido no HTML usado para extração de dados |
| **cb_partner_list** | Componente Next.js que contém metadados dos parceiros |

## 3. Regras de Extração

- A extração deve ocorrer diariamente às **10:00 horário de Brasília** (America/Sao_Paulo)
- Os dados são extraídos do componente `__NEXT_DATA__` da página da Livelo
- Cada parceiro deve ter os seguintes dados coletados:
  - ID, Nome, Categorias
  - Moeda (R$ ou U$)
  - Pontos atuais, pontos Clube, pontos base
  - Status de promoção e período

## 4. Regras de Armazenamento

- Resultados salvos em formato **JSON** e **CSV** com timestamp da extração
- Arquivos armazenados na pasta `/data` do projeto
- Nome dos arquivos deve incluir a data da extração

## 5. Regras de Promoção

- Um parceiro está em promoção quando `is_promotion = true`
- Promoção é identificada quando a paridade atual excede a `points_base`
- Promoções possuem data de início (`promotion_start`) e fim (`promotion_end`)

## 6. Notificações

- O sistema envia notificação via **Telegram** após cada execução do scraping
- A notificação deve informar o status da extração (sucesso/falha)

---

## Histórico de Atualizações

| Data | Feature | Alteração |
|------|---------|----------|
| 2026-05-10 | Documento inicial | Criação da base de conhecimento com regras existentes |
