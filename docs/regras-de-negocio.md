# Regras de Negócio — LiveloScrapper

## 1. Conceitos

| Termo | Definição |
|-------|-----------|
| **Parceiro** | Loja/empresa integrada ao programa Livelo (ex: Amazon, Netshoes) |
| **Paridade de Acúmulo** | Razão de pontos acumulados por unidade monetária gasta |
| **Points Base (BAU)** | Pontuação padrão, sem promoção ativa |
| **Points Club** | Pontuação preferencial para membros do Clube Livelo |
| **Promoção** | Período em que a paridade é superior à base |
| **Categoria** | Classificação do parceiro (ex: perfumariaecosmeticos, modaebeleza). Um parceiro pode ter múltiplas categorias separadas por espaço |
| **Melhor Pontuação (best_points)** | `max(points, points_club)` — a maior pontuação disponível entre normal/promoção e Clube para um parceiro |
| **Clube Livelo** | Programa de assinatura da Livelo que oferece pontuações diferenciadas (geralmente superiores) em parceiros selecionados |

## 2. Regras Gerais

- A extração diária captura **todos** os parceiros da Livelo, sem exceção
- Os dados completos são sempre persistidos em JSON e CSV (sem filtro)
- O campo `categories` é uma string com categorias separadas por espaço

## 3. Categorias de Pontuação

Cada parceiro possui **três tipos de pontuação**:

| Categoria | Campo | Origem JSON | Uso |
|-----------|-------|-------------|-----|
| Normal/Promoção | `points` | `parity` | Pontuação ativa (normal ou promocional) |
| Clube | `points_club` | `parityClub` | Pontuação para assinantes do Clube Livelo |
| Base (BAU) | `points_base` | `parityBau` | Referência — **NÃO** entra no ranking |

### Regra de Melhor Pontuação
- Para ordenação e exibição, utilizar sempre `best_points = max(points, points_club)`
- O campo `points_base` é apenas referência e **NÃO** participa do cálculo
- Quando `points_club > points`, a pontuação exibida vem do Clube
- Quando `points >= points_club`, a pontuação exibida vem do canal normal/promoção
- Parceiros com `points_club = 0` usam `points` normalmente

## 4. Filtro de Categorias (Notificação e Summary)

- **Onde se aplica:** Notificação Telegram e summary no console
- **Categorias filtradas:** `perfumariaecosmeticos`, `modaebeleza`, `modaeacessorios`, `calcados`
- Um parceiro é incluído se **qualquer uma** de suas categorias estiver na lista filtrada
- A comparação de categorias é **case-insensitive**
- Após o filtro, a ordenação é **decrescente por melhor pontuação** (`best_points = max(points, points_club)`)
- O filtro **NÃO** afeta o salvamento de dados (JSON/CSV mantêm todos os parceiros)

## 5. Notificação Telegram

- Envia ranking dos top parceiros filtrados, ordenados por **melhor pontuação** decrescente
- Exibe indicador visual `🏆 (Clube)` quando a pontuação do Clube é superior à normal/promoção
- Mensagem limitada a 4096 caracteres (limite da API Telegram)
- Retry com exponential backoff (até 3 tentativas)
- Se variáveis `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` não estiverem configuradas, a notificação é ignorada silenciosamente

## 6. Summary no Console

- Exibe ranking dos parceiros filtrados, ordenados por **melhor pontuação** decrescente
- Indicadores visuais:
  - `⭐` — parceiro em promoção
  - `🏆` — melhor pontuação vem do Clube Livelo

## 7. Agendamento

- Execução diária configurável (atualmente às 10:00 BRT)
- Timezone: America/Sao_Paulo

---

## Histórico de Atualizações

| Data | Feature | Descrição |
|------|---------|-----------|
| 2026-05-10 | filtro-categorias | Adição de filtro por categorias na notificação e summary |
| 2026-05-12 | clube-category | Consideração da pontuação Clube (`points_club`) na ordenação e exibição; indicador visual 🏆 (Clube) |
