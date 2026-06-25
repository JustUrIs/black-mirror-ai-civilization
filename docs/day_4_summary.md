# Día 4 — Resumen

**Fecha:** 2026-06-25 (continuación)
**Tiempo real estimado:** ~6h (vs 7h presupuestadas)
**Commits:** pending (esta entrega)
**Repo:** https://github.com/JustUrIs/black-mirror-ai-civilization

## Objetivo del día

Mundo vivo y con consecuencias. Agentes pueden morir (física), árboles producen fruta, creator interviene con drag-throw, agentes reaccionan emocionalmente, LLM-driven policy disponible. Anti-bullshit artefactos: WRITE_CODE produce HTML real con iframe.

## Entregables (7/7 tasks completadas)

| Task | Entregable | Detalle |
|---|---|---|
| 4.1 | LLM-driven policy wire | `famous_policies.build_all_policies()` detecta `ANTHROPIC_API_KEY` + `USE_LLM_POLICY!=0`. Si presente → `LLMDrivenPolicy` reemplaza `CyclicPolicy`. Fallback graceful. |
| 4.2 | WRITE_CODE HTML render | Handler acepta `codigo_full` param (>=50 chars). Si lenguaje=html → store en `html_render`. Endpoint `GET /code/{id}/render` sirve como iframe. Stub mínimo si `codigo_full` ausente. Borges cycle incluye 1 demo HTML cada vuelta. |
| 4.3 | Agent observation de creator | `triggers.py` extiende observation a `SPAWN_OBJECT`, `MOVE_OBJECT`, `REVIVE` con filtro `same_location`. Events incluyen `from_creator: True`. |
| 4.4 | Physics: THROW + death | Nuevo handler `ThrowHandler` (THROW action #22). Damage tabla por `object_type` (piedra=40, libro_extraño=5, comida=0). Si salud→0 → `alive=False`. Endpoint `POST /admin/throw_object` para creator. WorldObject marcado `state='thrown'` + metadata. |
| 4.5 | Fruit tree life cycle | `world_dynamics.grow_fruit_trees(s, tick)` corre cada tick. Cada `arbol_frutal` produce 1 `fruta` cada 20 ticks, cap 3 por árbol. GATHER extends para `world_object_id` param → consume fruta + agrega a inventario con `es_comestible`. EAT con `item='ANY'` come fruta. `agent_id="nature"` registrado en log (sealed-world autorizado). |
| 4.6 | Agent reaction emocional | `sim/emotions.py` con `update_agent_emotions()`. Eventos → deltas: SPAWN_OBJECT creator → asombro +15, miedo +5. ATTACK observado → miedo +25, animo -10. REVIVE → asombro +20, animo +15. Decay natural toward defaults. Personal_history record significant events (`intervencion_divina`, `presencie_violencia`, `milagro`). |
| 4.7 | Tests + summary + commit | `test_day4_dynamics.py` con 5 sub-tests (THROW kills, fruit grow, GATHER world_object, WRITE_CODE html, emotions update). 7/7 test suites passing globalmente. |

## Decisiones técnicas

- **Physics simple, no real engine**: damage table fija por tipo. Trajectory not animated (post-MVP). Suficiente para drama.
- **Fruit `nature` actor**: nuevo `agent_id="nature"` en allowed system list. Auditable.
- **HTML render directo, no eval**: code lenguaje='html' se sirve raw en iframe. No execution risk.
- **Emotions deterministic, no LLM**: heuristica per tick. Funciona sin keys. LLM puede sobrescribir Day 5+.
- **Creator interactions tienen agent_id="creator"**: SPAWN_OBJECT, MOVE_OBJECT, THROW, REVIVE todos creator-actor. Sealed-world audit las acepta como autorizadas.

## Issues encontrados y resueltos

| Issue | Fix |
|---|---|
| Test fruit_grow asertía sobre metadata_json sin flush | `s.flush()` antes de leer (SQLAlchemy autoflush=False) |
| Test WRITE_CODE spec 48 chars (<50) | Extendido string a 70 chars |
| Test GATHER fruta state assertion sin commit | flush + re-get para forzar visibility |

## Anti-bullshit en Día 4

| Acción | Constraint | Resultado |
|---|---|---|
| THROW | objeto activo + target accesible + alive | rechaza fallidos correctamente |
| GATHER world_object_id | object active + same location | nuevo path testeado |
| WRITE_CODE | spec >=50 + knowledge:programming + computadora en location | acepta + renderiza HTML |
| GROW_FRUIT (nature) | tree active + interval cumplido + cap no excedido | spawn fruta con metadata coherente |

## Estado al cierre Día 4

- **22 + 1 = 23 action handlers** (THROW agregado)
- **22 + 4 = 26 endpoints API** (`/code/{id}/render`, `/admin/throw_object`, `/admin/move_object`, `/admin/revive`, `/world_objects`)
- **5 trigger types + observation extendido** a creator events
- **3 famosos** con cycles personality-aligned + supervivencia (EAT/DRINK intercalado)
- **Borges cycle incluye WRITE_CODE HTML** demo iframe
- **7/7 test suites passing** (1 nuevo Día 4)
- **Tiempo real:** ~6h / **margen acumulado:** +6h

## Nuevas capacidades visibles en `/ui/`

| Capacidad | Cómo |
|---|---|
| Tirar piedra a agente | Drag piedra del mapa SOBRE el agente (drop dentro 30u) → endpoint `POST /admin/throw_object` |
| Muerte por trauma | THROW reduce salud por damage. Salud=0 → 💀 emoji + alive=False persistente |
| Revivir muertos | Botón 💚 en creator panel |
| Árbol frutal | Spawn 🌳 árbol_frutal → cada 20 ticks aparece 🍎 fruta junto al árbol |
| Agente come fruta | Cycle EAT con 'ANY' consume cualquier comestible incluyendo fruta cosechada |
| HTML artifact iframe | Click tab CODE en panel Obra → iframe vivo con HTML del agente |
| Reaccion emocional | Cara del agente cambia: asombro 😲 cuando creator spawnea, miedo 😨 cuando observa ATTACK |
| LLM driver | Si `ANTHROPIC_API_KEY` seteado al boot, agentes usan Claude Sonnet en vez de ciclos scripted |

## Tests al cierre Día 4

```
test_day1_loop.py             PASSED
test_day2_economy.py          PASSED
test_day2_full_actions.py     PASSED
test_day2_triggers.py         PASSED
test_day2_famous_spawn.py     PASSED
test_audits.py                PASSED
test_day4_dynamics.py         PASSED (5 sub-tests)
```

**7/7 test suites passing.**

## Próximo paso (Día 5)

Plan v4 original Día 5: Crónica + Diarios + flujo upload semilla + dilema en vivo.

Plus carry-over si hay tiempo:
- LLM-driven test real con keys (requiere ANTHROPIC_API_KEY en env)
- Cadáver visual mejorado (sprite tumba persistente)
- Árbol que muere si no produce fruta tras N ticks
- Agente que pisa fruta caída la come automáticamente
