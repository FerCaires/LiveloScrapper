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

## 2. Regras Gerais

- A extração diária captura **todos** os parceiros da Livelo, sem exceção
- Os dados completos são sempre persistidos em JSON e CSV (sem filtro)
- O campo `categories` é uma string com categorias separadas por espaço

## 3. Filtro de Categorias (Notificação e Summary)

- **Onde se aplica:** Notificação Telegram e summary no console
- **Categorias filtradas:** `perfumariaecosmeticos`, `modaebeleza`, `modaeacessorios`, `calcados`
- Um parceiro é incluído se **qualquer uma** de suas categorias estiver na lista filtrada
- A comparação de categorias é **case-insensitive**
- Após o filtro, a ordenação é **decrescente por pontuação** (`parity.points`)
- O filtro **NÃO** afeta o salvamento de dados (JSON/CSV mantêm todos os parceiros)

## 4. Notificação Telegram

- Envia ranking dos top parceiros filtrados, ordenados por pontuação decrescente
- Mensagem limitada a 4096 caracteres (limite da API Telegram)
- Retry com exponential backoff (até 3 tentativas)
- Se variáveis `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` não estiverem configuradas, a notificação é ignorada silenciosamente

## 5. Agendamento

- Execução diária configurável (atualmente às 10:00 BRT)
- Timezone: America/Sao_Paulo
