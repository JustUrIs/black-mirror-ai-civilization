# Día 1 — Resumen

**Fecha:** 2026-06-25
**Tiempo real estimado:** ~6h (vs 7h presupuestadas)
**Commits:** `a06a9c8` (scaffold), `b5c0a0a` (cleanup)
**Repo:** https://github.com/JustUrIs/black-mirror-ai-civilization

## Objetivo del día

Levantar scaffolding: backend FastAPI, SQLite schema, GM core con 3 handlers, LLM gateway stub, world loop async con 1 agente hardcoded.

## Entregables (6/6 tasks completadas)

| Task | Entregable | Detalle |
|---|---|---|
| 1.1 | Scaffold + FastAPI + SQLite | `backend/src/db/schema.py` con 16 tablas: WorldState, Location, Agent, ActionLog, TextArtifact, CodeArtifact, PendingInstitution, Institution, PendingRitual, Ritual, Post, Chronicle, Diary, Dilema, DilemaResponse, LLMCallLog. `backend/src/api/main.py` con endpoints `/`, `/world`, `/agents`, `/locations`, `/log`. Docker Compose + Dockerfile. |
| 1.2 | Mapa moderno CABA | `maps/moderno.json` con 8 locations: plaza_italia, cafe_palermo, biblioteca_nacional, depto_almagro_1/2/3, mercado_bonpland, parque_centenario. 11 aristas simétricas. Objetos con verbos atados (papel/lapiz/cama/computadora/heladera/comida/agua). |
| 1.3 | GM core + 3 handlers | `backend/src/gm/validator.py` con `GameMaster.validate_and_apply()`. `handlers.py` con MOVE (prereq: transition válida + energía>5), TALK (anti-bullshit: contenido >5 chars, no placeholder), EAT (item en inventario + comestible). `actions.py` con dataclass Action + Accept/Reject + WorldContext. |
| 1.4 | LLM gateway stub | `backend/src/mind/llm.py` con LLMGateway, soporte tier (leader/crowd/content/narrator/micro), cache disk (sha256 hash), audit log LLMCallLog, stub mode (sin keys retorna canned JSON). |
| 1.5 | World loop + 1 agente | `backend/src/sim/world_loop.py` async, decay needs por tick, ScriptedAgentPolicy con queue FIFO. `seed_day1.py` con `spawn_test_agent` + `build_test_policy`. |
| 1.6 | Test 10 ticks | `backend/tests/test_day1_loop.py` corre 10 ticks, valida 7 accepts + 3 rejects con error_nl correcto, agente movió + comió + inventario consumido. |

## Decisiones técnicas

- **No Convex (descartado AI Town fork).** FastAPI Python custom + Phaser/Next.js posterior (D2 confirmado).
- **No Concordia.** GM custom Python ~400 líneas alcanza.
- **Stub mode LLM por default** si no hay keys (Día 1 no necesita LLM real).
- **Anti-bullshit baked-in** desde Día 1: TALK rechaza contenido <=5 chars o placeholder; EAT rechaza item ya consumido.

## Issues encontrados y resueltos

| Issue | Fix |
|---|---|
| Unicode print Windows cp1252 falló con ✓ | Reemplazado por `[OK]` |
| `Action.agent_id` redundante (WorldLoop ya conoce agente) | Eliminado del dataclass, GM recibe `agent` + `action` |
| `memoria_recent` cap a 30 hardcoded | Configurable vía `MEMORIA_RECENT_CAP` env var en `config.py` |
| `sueño` key en JSON disparaba encoding issues en logs Windows | Renombrado a `sueno` (ASCII safe) |

## Estado al cierre Día 1

- **16 tablas SQLite** creadas
- **3 handlers** (MOVE, TALK, EAT) con anti-bullshit
- **1 mapa** modern (CABA), 8 locations, 11 edges
- **0 LLM calls reales** (stub mode)
- **1 test end-to-end** passing
- **Tiempo real:** ~6h / **margen restante:** +1h

## Test suite final

```
test_day1_loop.py ........ PASSED (7 accepts, 3 rejects)
```

## Próximo paso (Día 2)

Implementar 15 acciones restantes, sistema de triggers, prompt LLM real con JSON response schema, 3 famosos pre-cargados.
