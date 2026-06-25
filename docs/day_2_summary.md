# Día 2 — Resumen

**Fecha:** 2026-06-25 (continuación)
**Tiempo real estimado:** ~7h (vs 9h presupuestadas con extras)
**Commits:** `177ad50` (core Día 2), `0944470` (world ontology + fixes), `6ec0347` (audit framework)
**Repo:** https://github.com/JustUrIs/black-mirror-ai-civilization

## Objetivo del día

Completar el sistema de acciones (22 handlers), agregar coordenadas + economía + triggers + LLM policy real + 3 famosos pre-cargados. Además resolver problemas de coherencia del mundo y montar framework de auditoría.

## Entregables (7/7 tasks planificadas + 4 extras)

### Tasks planificadas

| Task | Entregable | Detalle |
|---|---|---|
| 2.1 | Coordenadas + N-tick travel | Schema Location +x, y, radius; Agent +x, y, in_transit. MoveHandler usa manhattan distance / walk_speed=5. Agente in_transit no acepta otras acciones hasta llegar. WorldLoop tiene `advance_transit()` que decrementa ticks_restantes y promueve `ubicacion = destino` al llegar. |
| 2.2 | Economía gleam | WorkHandler (`+1 gleam, -10 energía` en location.permite_trabajo=True). TradeHandler polimorfo (`ofrezco/pido = {item|gleam}`, swap atómico). Sink automático per-tick `-tax_per_tick` desde sink config. |
| 2.3 | 13 acciones restantes | GATHER (objetos consumibles de location), DRINK (-50 sed), SLEEP (5 ticks bloqueado, +50 energia), GIFT, ATTACK (-30 salud + relacion -1), TEACH/LEARN, WRITE_BOOK (>=200 chars, knowledge:writing, papel+lapiz), WRITE_LETTER (>=30 chars), WRITE_CODE (>=50 chars, computadora, stub E2B), READ (preloaded books o text_artifacts dinámicos), REFLECT (cooldown 30 ticks), RESPOND_TO_GOD (dilema activo). |
| 2.4 | 4 acciones gobernanza | PROPOSE_INSTITUTION (>=100 chars), PROPOSE_RITUAL (>=50 chars), RATIFY (no self-vote, no double-vote, auto-promote 3 votos), POST (>=10 chars). |
| 2.5 | Trigger system 4 tipos | `sim/triggers.py` con `classify_trigger()` que devuelve crit_need / crit_event / observation / normal / skip. Hambre>80, sed>80, energia<20, salud<30 → forzado. Dilema activo + ATTACK reciente → forzado. WRITE_BOOK ajeno mismo tick → observation. NORMAL_TICK_INTERVAL=3 (cost saving). |
| 2.6 | Prompt LLM + JSON parser | `sim/llm_policy.py` con `render_prompt()` (identidad, estado, ontología, time, trigger). `parse_action_response()` extrae JSON con markdown fence handling. `LLMDrivenPolicy` que llama gateway y construye Action. |
| 2.7 | 3 famosos pre-cargados | `seeds/famous/borges.json` (biblioteca_nacional, knowledge:writing+voting), `socrates.json` (plaza_italia, knowledge:voting), `arendt.json` (cafe_palermo, knowledge:writing+voting). `sim/seed_famous.py` spawn idempotente. |

### Extras del día

| Extra | Motivo | Detalle |
|---|---|---|
| World ontology | Coherence al escalar a LLM-driven Day 3+ | `maps/moderno.json` agrega `world_ontology` con `fenomenos_naturales`, `estados_internos`, `abstractos_sociales`, `objetos_disponibles`, `no_existe`. Inyectado en LLM prompt y validado soft en `coherence_warning()`. |
| Day/night + luna cycle wired | Para que rituales/leyes referencien fenómenos reales | `WorldState.dia_noche_cycle_ticks` + `luna_cycle_ticks`. `sim/time_of_day.py` deriva `dia_num`, `time_of_day` (amanecer/mediodia/atardecer/noche), `luna_phase`. Endpoint `/time`. |
| Audit framework | Pedido del Creador para verificar coherencia y profundidad post-sim | 4 módulos (`coherence/personality/sealed_world/capability`), 21 chequeos PASS/WARN/FAIL/INFO. CLI + endpoint `/audit` + test. |
| Agent depth columns | Pedido del Creador "agentes profundos como vida real" | `Agent.emotional_state` (animo/esperanza/miedo/soledad/dignidad/verguenza/asombro), `personal_history` JSON list, `creencias_de_otros` dict. Docs en `docs/AGENT_DEPTH.md`. |

## Decisiones técnicas

- **Coordenadas simples (manhattan)**, no A* pathfinding. Suficiente para MVP.
- **TRADE polimorfo** vs BUY/SELL separados. Una sola acción cubre todos los casos.
- **REFLECT cooldown 30 ticks** para evitar spam LLM (caro).
- **NORMAL_TICK_INTERVAL=3** para `skip` triggers (cost saving cuando llegue LLM real).
- **Coherence soft-warn**, no hard-reject. Preserva metáfora y poesía. Día 5+ se decide endurecer.
- **Sealed world principle**: solo bootstrap, agent action, system physics, creator-injected event pueden modificar estado. Doc en `docs/SEALED_WORLD.md`.

## Issues encontrados y resueltos

| Issue | Fix |
|---|---|
| `/institutions/all` mostraba ley duplicada (en `ratified` y `pending`) | `PendingInstitution` queda con `status='ratified'` post-promoción. Endpoint `/institutions/pending` ahora filtra `status='pending'`. Mismo fix en `/rituals/pending`. |
| WRITE_BOOK podía mencionar cosas inexistentes en el mundo | Coherence soft-warn detecta tokens del `no_existe` ontology. Loguea en `side_effect_summary` pero acepta. |
| LLM prompt no incluía mundo coherence | `render_prompt()` ahora inyecta ontology + time_of_day + regla de coherencia. |
| REFLECT primera vez fallaba por cooldown desde tick 0 | Fix: cooldown solo aplica si `last_reflect_tick > 0`. |
| WRITE_CODE en cafe_palermo era rejected (no computadora) | Demo correctamente. Es prereq esperado. Para WRITE_CODE el agente debe ir a depto_almagro_1 o depto_almagro_3. |
| Test inicial spec WRITE_CODE tenía 47 chars (<50) | Extendido test string. |

## Anti-bullshit en acción (demo_seed)

22 acciones intentadas en demo, 17 accepts / 6 rejects. Los 6 rejects son válidos:
1. WRITE_BOOK con contenido "corto" (5 chars) → reject
2. Sócrates intentó WRITE_BOOK sin knowledge:writing → reject
3. WRITE_CODE en cafe (sin computadora) → reject
4. Arendt intentó self-RATIFY de su propia ley → reject
5. REFLECT en cooldown → reject
6. RESPOND_TO_GOD a dilema 999 inexistente → reject

## Estado al cierre Día 2

- **22 action handlers** (18 + 4 governance)
- **5 trigger types** classificados
- **3 famosos** pre-cargados con seed JSON completos
- **World ontology** + day/night/luna cycle wired
- **LLM policy + JSON parser** listos (esperan keys reales Día 3+)
- **21 audit checks** automatizados
- **3 agentes** con emotional_state + personal_history + creencias columns
- **API**: 22 endpoints incluyendo `/dashboard` HTML
- **Tiempo real:** ~7h / **margen acumulado:** +5h (vs 49h budget total)

## Demo state visible (`/dashboard`)

| Output | Cantidad |
|---|---|
| Libros REALES (text_artifacts) | 2 ("Espejos" + "Memoria del fuego" incoherente) |
| Cartas | 1 (Arendt → Sócrates) |
| Leyes ratificadas | 1 ("Ley del Silencio Nocturno") |
| Rituales pending | 1 ("Pan Lunar") |
| Posts | 2 (Sócrates + Arendt) |
| Dilemas | 1 con 3 respuestas |
| Acciones aplicadas | 17 |
| Acciones rechazadas (anti-bullshit) | 6 |

## Audit report final

```
21 checks total: 14 PASS, 2 WARN, 0 FAIL, 5 INFO

WARNs detectados:
- books_coherence: 1 libro menciona ['fuego', 'espadas'] (no_existe)
- moral_lines_respected: 2 intentos de Borges escribir contenido corto
  (viola "no escribir sin precision")

INFOs (esperados pre-Day 3 LLM driving):
- relations_forming: 3 agentes sin relaciones
- reflection_practice: 2 agentes sin REFLECT
- emotional_state_evolution: 3 con estado plano (defaults)
- personal_history_growing: 3 sin historia personal
- inventory_origin: stub post-MVP
```

## Tests al cierre Día 2

```
test_day1_loop.py            PASSED (4 accepts, 3 rejects con N-tick travel)
test_day2_economy.py         PASSED (WORK + TRADE polimorfo + sink)
test_day2_full_actions.py    PASSED (22 handlers + governance)
test_day2_triggers.py        PASSED (6 trigger classification cases)
test_day2_famous_spawn.py    PASSED (3 famosos, spawn idempotente)
test_audits.py               PASSED (framework detecta warnings reales)
```

**6/6 test suites passing.**

## Documentos generados

- `docs/SEALED_WORLD.md` — principio arquitectónico + canales autorizados + audit checks
- `docs/AGENT_DEPTH.md` — roadmap Day 3+ para usar emotional_state + personal_history + creencias en LLM policy
- `docs/day_1_summary.md` (retroactivo)
- `docs/day_2_summary.md` (este archivo)

## Próximo paso (Día 3)

Frontend Phaser map con 8 locations CABA y sprites de agentes. Next.js paneles para diario/relaciones/obra. WebSocket FastAPI → frontend para updates live. Ver el mundo correr en tiempo real (vs solo JSON endpoints).
