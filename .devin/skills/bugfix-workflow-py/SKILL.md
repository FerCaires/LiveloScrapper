---
name: bugfix-workflow-py
description: Fluxo enxuto de correção de bugs para Python. Guia o operador (Devin principal ou usuário) a investigar, reproduzir, corrigir e validar regressões com o mínimo de sobrecarga burocrática. Nunca substitui o feature-workflow-py.
argument-hint: "[bug description or issue reference]"
subagent: false
triggers:
  - user
  - model
---

# 🐛 Bugfix Workflow Skill — Python

Correção de bugs exige **velocidade e precisão**, não especificação. Este fluxo elimina as fases de `spec`, `tech-plan` e `SDD` do feature-workflow-py, mantendo apenas o essencial: **reproduzir → corrigir → validar**.

> **Quando usar este fluxo:**
> - Regressões em código existente
> - `AttributeError`, `KeyError`, `TypeError`, `NoneType` em produção
> - Comportamento inesperado em regra já implementada
> - Fix de segurança ou performance pontual

> **Quando NÃO usar (escalar para feature-workflow-py):**
> - Bug é sintoma de redesign arquitetural
> - Correção exige nova dependência externa complexa
> - Bug envolve regra de negócio não documentada (precisa de spec)

---

## ⚡ Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: INVESTIGAÇÃO + REPRODUÇÃO                        │
│  • Analisar stacktrace / logs / relatório do usuário        │
│  • Isolar o mínimo código que reproduz o bug              │
│  • Escrever teste que falha (TDD reverso)                   │
│  • Confirmar falha ANTES de qualquer alteração              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 2: CORREÇÃO                                         │
│  • Implementar o fix mais simples possível                 │
│  • Garantir que o teste de reprodução passe               │
│  • Rodar suite completa para detectar regressões            │
│  • Adicionar teste de regressão se não existir              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: VALIDAÇÃO + PR                                   │
│  • Revisar diff (foco em edge cases e segurança)            │
│  • Rodar testes E2E / integração se disponíveis             │
│  • Criar PR com descrição do root cause                     │
└─────────────────────────────────────────────────────────────┘
```

---

## FASE 1: Investigação + Reprodução

### 1.1 Coletar evidências

```bash
# Logs recentes (ajustar caminho conforme projeto)
cat logs/*.log | grep -i error
cat logs/*.log | grep -i exception

# Git blame na linha do stacktrace
git blame -L {linha},{linha} {arquivo}

# Quando o código mudou pela últ vez?
git log --oneline -n 5 -- {arquivo}
```

**Checklist de investigação:**
- [ ] Stacktrace completo salvo (copiar para a sessão)
- [ ] Último commit que tocou no arquivo identificado
- [ ] Variáveis de ambiente / estado relevante documentado
- [ ] Input que causa o bug isolado (mínimo reprodutível)

### 1.2 Isolar reprodução

Crie um teste mínimo que **falha** com o bug atual. Não altere código de produção ainda.

```python
# Exemplo de teste de reprodução
import pytest


def test_bug_reproducao_descritivo():
    """Reproduz issue #123: KeyError quando campo 'bonus' está ausente."""
    input_bug = {"partner": "x", "points": 100}  # sem 'bonus'
    
    with pytest.raises(KeyError, match="bonus"):
        funcao_que_quebra(input_bug)
```

> **REGRA**: Se não conseguir reproduzir em teste, pare. Bugs não reproduzíveis não devem ser "consertados com palpite".

### 1.3 Escalar se necessário

| Bloqueio | Ação |
|----------|------|
| Bug vem de decisão arquitetural ruim (ex: acoplamento circular) | Invocar `tech-lead-py` para direcionamento antes de corrigir |
| Comportamento esperado é ambíguo (regra de negócio não clara) | Invocar `pm-analyst-py` para esclarecer |
| Bug envolve schema de DB / contrato de API quebrado | Invocar `tech-lead-py` para ADR de compatibilidade |

---

## FASE 2: Correção

### 2.1 Implementar fix cirúrgico

Princípio: **O menor diff que resolve o problema.**

```python
# ❌ Ruim — refatoração grande no meio do bugfix
# ❌ Ruim — adicionar camada de abstração para um simples None check

# ✅ Bom — fix direto no ponto da falha
bonus = data.get("bonus")  # ao invés de data["bonus"]
```

**Checklist de correção:**
- [ ] Fix é o menor possível (≤ 50 linhas de diff ideal)
- [ ] Não introduz novo comportamento (só corrige o bug)
- [ ] Não remove funcionalidade existente sem justificativa
- [ ] `None`, `[]`, `{}`, `''` tratados explicitamente se forem a causa
- [ ] Nenhum `except Exception: pass` genérico introduzido

### 2.2 Validação local obrigatória

```bash
# 1. Teste de reprodução agora passa?
pytest tests/path/to/test_reproducao.py -v

# 2. Suite completa passa? (regressão)
pytest

# 3. Lint limpo?
ruff check .

# 4. Type check (se o projeto usa)
mypy src/
```

**Se algum passo falhar:**
- `pytest` falha em teste antigo → seu fix quebrou algo; investigar
- `ruff check` falha → corrigir formatação antes de commit
- `mypy` falha → ajustar type hints

### 2.3 Documentar o Bug (Artefato Obrigatório)

Crie o artefato de bugfix em `docs/bugs/fix-{bugName}/bug-report.md` usando o template `docs/bugs/TEMPLATE.md`:

```bash
cp docs/bugs/TEMPLATE.md docs/bugs/fix-{bugName}/bug-report.md
```

**Preencher obrigatoriamente:**
- **Metadados**: identificador, data, autor, severidade, commit hash
- **Sintoma**: stacktrace ou descrição do comportamento incorreto
- **Causa Raiz**: explicação do POR QUÊ (não só o O QUÊ)
- **Reprodução**: input mínimo ou passos para reproduzir
- **Correção Aplicada**: diff/descrição textual da mudança
- **Validação**: checklist de qualidade + evidências de testes passando
- **Lições Aprendidas**: como prevenir recorrência

> **REGRA**: Bugfix sem artefato em `docs/bugs/` está incompleto. O artefato serve como histórico técnico e base para futuras investigações de regressão.

### 2.4 Commit

Máximo **1 commit** para a correção (o artefato pode estar no mesmo commit ou em commit separado de docs):

```bash
git commit -m "$(cat <<'EOF'
fix: tratar campo ausente em extracao de bonus

- Usa .get() ao inves de [] para evitar KeyError
- Adiciona teste de regressao para campo opcional
- Adiciona docs/bugs/fix-extracao-bonus/bug-report.md

Closes #123

Generated with [Devin](https://cli.devin.ai/docs)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
EOF
)"
```

---

## FASE 3: Validação + PR

### 3.1 Self-review do diff

Antes de chamar `qa-engineer-py` (ou antes de criar PR), faça uma revisão rápida:

```bash
git diff main...HEAD
```

**Checklist de self-review:**
- [ ] Diff contém APENAS código relacionado ao bug (sem alterações cosméticas)
- [ ] Nenhum `print()`, `console.log()`, `debugger` esquecido
- [ ] Nenhum secret ou credencial hardcoded
- [ ] Variáveis temporárias removidas
- [ ] Teste de reprodução/regressão está no commit
- [ ] Artefato `docs/bugs/fix-{bugName}/bug-report.md` criado e preenchido

### 3.2 Validar com testes de integração / E2E

Se o projeto tiver testes de integração ou E2E, rode-os:

```bash
# Testes E2E (se existirem)
pytest tests/e2e/

# Ou skill específica do projeto
skill({ name: "testing-livelo-scrapper" })
```

> **REGRA**: Bugfixes em scrapers, schedulers ou saída de dados devem sempre passar pelo teste E2E do projeto antes do PR.

### 3.3 Criar PR

Template simplificado para bugfix:

```markdown
## 🐛 Bug
[Descrição curta do problema — 1 parágrafo]

## 🔍 Root Cause
[O que causava o bug — 1-2 frases]

## ✅ Correção
[O que foi alterado — lista curta]

## 🧪 Como Testar
```bash
pytest tests/path/to/test_regressao.py
```

## 📋 Checklist
- [ ] Teste de reprodução incluído
- [ ] `pytest` passando
- [ ] `ruff check` limpo
- [ ] Sem regressões na suite completa
- [ ] Artefato `docs/bugs/fix-{bugName}/bug-report.md` incluído
```

---

## 🆘 Critérios de Escalação

| Situação | Skill a invocar | Momento |
|----------|-----------------|---------|
| Causa raiz é arquitetural (acoplamento, responsabilidade mal distribuída) | `tech-lead-py` | Fase 1, antes de qualquer código |
| Regra de negócio não está clara (comportamento esperado é subjetivo) | `pm-analyst-py` | Fase 1, antes de reproduzir |
| Fix exige mudança em contrato de API pública / schema de banco | `tech-lead-py` | Fase 1, antes de implementar |
| Bug reaparece frequentemente (indício de problema sistêmico) | `tech-lead-py` | Após Fase 3, para proposta de refatoração |
| Correção ficou > 150 linhas de diff | `tech-lead-py` | Fase 2, para validar se não deveria ser feature |

---

## 🚫 O QUE NÃO FAZER EM BUGFIX

- **Não escreva spec** — bugs já têm comportamento esperado implícito (o estado anterior funcional ou o stacktrace).
- **Não crie ADR/SDD** — a menos que o escalonamento para `tech-lead-py` determine.
- **Não refatore em massa** — bugfix não é o momento de renomear 10 variáveis ou extrair 3 classes.
- **Não adicione feature** — se o fix "aproveita" para adicionar funcionalidade nova, pare: isso é feature, não bugfix.
- **Não pule o teste de reprodução** — corrigir sem reproduzir primeiro é adivinhação.
- **Não ignore a suite completa** — rodar só o teste novo esconde regressões.

---

## 📝 Resumo Rápido (cheat sheet)

```
1. REPRODUZIR
   → Isolar input que quebra
   → Escrever teste que FALHA
   → Confirmar falha

2. CORRIGIR
   → Menor diff possível
   → Passar teste de reprodução
   → Rodar suite completa (regressão)
   → 1 commit

3. VALIDAR
   → Self-review do diff
   → E2E / integração (se existir)
   → PR com root cause descrito
   → Merge
```
