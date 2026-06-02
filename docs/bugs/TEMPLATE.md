# Bug Report — fix-{bugName}

## Metadados

| Campo | Valor |
|-------|-------|
| **Identificador** | fix-{bugName} |
| **Data da Correção** | YYYY-MM-DD |
| **Autor** | @autor |
| **Issue/PR Relacionado** | #N |
| **Commit** | `abc1234` |
| **Severidade** | 🔴 Crítica / 🟠 Alta / 🟡 Média / 🟢 Baixa |
| **Ambiente** | Produção / Staging / Desenvolvimento |

---

## 1. Sintoma

[Descreva o que o usuário/sistema observou. Erro? Comportamento inesperado? Dados incorretos?]

### Stacktrace (se aplicável)
```
Traceback (most recent call last):
  File "...", line N, in ...
    ...
ExceptionType: mensagem
```

---

## 2. Causa Raiz (Root Cause)

[Explique POR QUE o bug acontecia. Qual invariante foi violada? Qual estado inesperado não era tratado?]

---

## 3. Reprodução

[Input mínimo ou passos para reproduzir o bug no estado anterior à correção.]

```python
# Exemplo de código/script de reprodução
input_bug = {...}
resultado = funcao_que_quebrava(input_bug)
# → lançava KeyError / retornava valor incorreto
```

---

## 4. Correção Aplicada

[O que foi alterado no código. Diff mínimo ou descrição textual clara.]

```python
# Antes
valor = data["campo"]  # → KeyError quando ausente

# Depois
valor = data.get("campo")  # → retorna None, tratado downstream
```

### Arquivos Alterados
- `src/...py` — descrição da mudança
- `tests/...py` — teste de regressão adicionado

---

## 5. Validação

### Checklist de Qualidade
- [ ] Teste de reprodução escrito e passando
- [ ] Suite completa (`pytest`) passando sem regressões
- [ ] `ruff check` limpo
- [ ] Testes E2E / integração passando (se aplicável)
- [ ] Revisão de código (self-review ou peer review)

### Evidências
```bash
$ pytest tests/... -v
============================= test session starts ==============================
...
PASSED
```

---

## 6. Lições Aprendidas / Prevenção

[O que poderia ter evitado esse bug? Falta de validação? Assunção incorreta sobre formato de dados? Documentar para prevenir recorrência.]

---

> Gerado durante o fluxo `bugfix-workflow-py`
