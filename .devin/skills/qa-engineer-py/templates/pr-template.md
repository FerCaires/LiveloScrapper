## 🎯 Contexto
[Resumo do problema e solução — 1 parágrafo]

## 📝 Mudanças
- [Mudança 1 — arquivo `.py` e o que mudou]
- [Mudança 2 — arquivo `.py` e o que mudou]
- [Mudança 3 — `pyproject.toml` se nova dependência]
- [Mudança 4 — `.env.example` se nova configuração]

## 🏗️ Arquitetura
- [Padrão usado: Feature-based | Monolithic | Clean Arch]
- [Camadas afetadas: Router → Service → Repository]
- [Nova integração: API externa | Message Broker]

## 🧪 Como Testar
```bash
# 1. Rodar testes unitários
pytest

# 2. Verificar cobertura
pytest --cov=src --cov-report=term

# 3. Rodar E2E (se aplicável)
pytest tests/e2e/

# 4. Rodar local (se aplicável)
uvicorn main:app --reload
# Testar: abrir http://localhost:8000/docs
```

## ✅ Critérios de Aceite
- [ ] [Critério 1 da spec]
- [ ] [Critério 2 da spec]

## 📋 Checklist de Qualidade
- [ ] `pytest` passando
- [ ] `ruff check` limpo
- [ ] `mypy` sem erros
- [ ] Sem `Any` sem justificativa
- [ ] Sem secrets expostos
- [ ] README atualizado (se necessário)
- [ ] `.env.example` atualizado (se necessário)