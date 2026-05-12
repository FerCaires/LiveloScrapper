# Tarefas de Implementação: Clube Category

## Resumo
Ajuste dos módulos de notificação, filtro e summary para utilizarem a maior pontuação disponível entre `points` e `points_club` na ordenação e exibição, com indicador visual 🏆 quando a melhor pontuação provém do Clube Livelo.

## Tarefas Realizadas
- [x] Adicionar `@property best_points` e `@property is_club_best` em `src/models/parity.py`
- [x] Atualizar ordenação e exibição em `src/notifier.py` — usar `best_points` e tag `🏆 (Clube)`
- [x] Atualizar ordenação em `src/filters.py` — usar `best_points` e atualizar docstring
- [x] Atualizar ordenação e exibição em `src/scheduler.py` — usar `best_points` e tag `🏆`
- [x] Criar documentação de tarefas (`docs/clube-category/tasks-clube-category.md`)

## Arquivos Criados
| Arquivo | Descrição |
|---------|----------|
| `docs/clube-category/tasks-clube-category.md` | Registro de tarefas da implementação |

## Arquivos Modificados
| Arquivo | Mudança |
|---------|--------|
| `src/models/parity.py` | Adicionadas properties `best_points` (max entre points e points_club) e `is_club_best` (indica se a melhor pontuação vem do Clube) |
| `src/notifier.py` | Ordenação por `best_points`; exibição de `best_points` no ranking; tag `🏆 (Clube)` quando `is_club_best` |
| `src/filters.py` | Ordenação por `best_points` em vez de `points`; docstring atualizada |
| `src/scheduler.py` | Ordenação por `best_points`; exibição de `best_points` no ranking; tag `🏆` quando `is_club_best` |

## Dependências Adicionadas
- Nenhuma — apenas alterações em código existente

## Observações Técnicas
- `best_points` retorna `max(self.points, self.points_club)` — `points_base` NÃO participa do cálculo
- `is_club_best` usa comparação estrita (`>`): quando `points == points_club`, retorna `False` (sem tag)
- As properties não afetam `dataclasses.asdict()`, portanto a persistência JSON/CSV permanece intacta
- Tags ⭐ (promoção) e 🏆 (Clube) são independentes e podem coexistir no summary
