# Día 3 — Resumen

**Fecha:** 2026-06-25 (continuación)
**Tiempo real estimado:** ~6h (vs 8h presupuestadas)
**Commits:** `a2d5259` (frontend inicial), pending (fix sim vivo + drag-drop real)
**Repo:** https://github.com/JustUrIs/black-mirror-ai-civilization

## Objetivo del día

Frontend visual del mundo Eidolon. Ver agentes vivos, sus caritas con emoción, lo que producen, log de acciones live, audit health. Black Mirror dashboard vibe.

## Cambio de stack vs plan original

Plan original mencionaba Next.js + Phaser. **Pivot ejecutado** a HTML estático + SVG + JS vanilla por:
- Sin build step (refresh instantáneo)
- Control fino del Black Mirror look
- SVG mejor que canvas para 8 nodos + agentes (clickable nativo)
- Servir directo desde FastAPI (`/ui` mount)
- Sin lock-in framework

WebSocket realtime quedó **deferido a Día 4+**. Polling cada 2-5s suficiente para 3 agentes en MVP.

## Entregables (5/6 tasks completadas, 1 deferida)

| Task | Entregable | Detalle |
|---|---|---|
| 3.1 | Frontend scaffolding (HTML/CSS/JS) | `frontend/static/` con `index.html`, `style.css`, 6 módulos JS ES en `js/`. Sin node_modules, sin build step. |
| 3.2 | Mapa SVG con 8 locations CABA | `js/map.js`. 11 aristas, locations con colores por tipo (cyan público, ambar público+trabajo, gris privado), labels con manera dim uppercase. Hover tooltip con objetos. |
| 3.3 | Agentes con caritas + emoción + nombre | `js/faces.js` mapea `emotional_state + necesidades + alive` a emoji (🙂😐😟😨😴💀😌🥺 etc). Tinte de color por agente (Borges rojo, Sócrates verde, Arendt cyan). Nombre arriba. Hover tooltip con stats. Animación interpolada in-transit. |
| ~~3.4~~ | ~~WebSocket realtime~~ | **Deferido a Día 4.** Polling actual suficiente. |
| 3.5 | Side panels (agentes/obra/log) | `js/panels.js`. Panel agentes (cards con cara + ubicación + 3 barras de necesidades). Panel obra (4 tabs: LIB/LEY/POSTS/RIT). Panel log live (40 entradas, color por status). |
| 3.6 | Modal agente AI Town-style + audit dropdown | `js/modal.js`. Modal con 9 secciones: identidad, personalidad, pensamientos, emotional grid, relaciones, historial 40 acciones, interacciones filtradas, memoria reciente, artefactos propios, personal_history. Audit dropdown con 21 checks agrupados por categoría. |

## Extras del día

| Extra | Motivo | Detalle |
|---|---|---|
| Schema `WorldObject` | Pedido del Creador: spawn de piedra/árbol/pan al estilo Thronglets | Tabla nueva. Cada object tiene `created_by` (creator/agent) auditable. State active/consumed/destroyed. Metadata JSON. |
| Endpoint `POST /admin/spawn_object` | Creator inyecta objetos al mundo | Body: `{location_id, object_type, metadata?}`. Crea WorldObject + log entry `SPAWN_OBJECT` con agent_id="creator". Sealed-world compliant. |
| Creator panel UI | Botón en topbar | Dropdown con location selector + 5 botones objeto (🪨 piedra, 🌳 árbol, 🥖 pan, 💧 agua, 📕 libro extraño). Click → POST → object aparece en mapa con glow animation. |
| `/world_objects` GET endpoint | Render frontend | Lista objects activos con location, type, tick, created_by. |
| Time banner colorizado | Visual feedback del cycle | amanecer naranja, mediodia amarillo, atardecer rosa, noche azul. |

## Decisiones técnicas

- **Drop Next.js + Phaser** (eran ~250MB node_modules sin sumar valor real).
- **SVG inline** vs canvas Phaser. Más simple, eventos DOM nativos.
- **CSS variables + grid puro**, sin Tailwind (no build).
- **Polling > WebSocket para MVP**: latencia 2-5s aceptable con 3 agentes. WS Día 4 si escalamos a 10+.
- **Mount /ui**, no `/`, para que API endpoints no choquen.
- **Audit polling cada 15s** (caro de computar, no necesita ser instantáneo).
- **Modal carga al click**, no pre-fetch (evita 3× requests innecesarios).

## Issues encontrados y resueltos

| Issue | Fix |
|---|---|
| `parents[2]` apuntaba a `backend/` no a project root | `parents[3]` para llegar a `frontend/static/` |
| Test_audits.py output cortado en CI run | Re-corrido individual: PASS confirmado |

## Files nuevos creados

```
frontend/static/
├── index.html              (HTML estructura, 80 lineas)
├── style.css               (Black Mirror styles, 360 lineas)
└── js/
    ├── api.js              (fetch wrapper)
    ├── faces.js            (emoji mapping + colors)
    ├── map.js              (SVG render + agent positioning)
    ├── panels.js           (3 side panels)
    ├── modal.js            (agent detail modal)
    └── app.js              (orchestrator + polling)
```

Backend:
- `backend/src/db/schema.py` +1 tabla `WorldObject`
- `backend/src/api/main.py` +2 endpoints (`/world_objects`, `/admin/spawn_object`) + StaticFiles mount

## Aspecto visual logrado

- Paleta dark: `#0a0a0e` base, accents apagados (cyan/ambar/rojo apagado)
- Monospace única tipografía
- Scanlines sutiles overlay (efecto Black Mirror/Mr. Robot)
- Border-left de 3px en agent cards con color del agente
- Animación dash en líneas de viaje (in_transit)
- Glow animation al aparecer objetos nuevos
- Hover states con drop-shadow glow del color del agente

## Test state al cierre Día 3

```
test_day1_loop.py            PASSED
test_day2_economy.py         PASSED
test_day2_full_actions.py    PASSED
test_day2_triggers.py        PASSED
test_day2_famous_spawn.py    PASSED
test_audits.py               PASSED
```

**6/6 test suites passing.** Sin tests nuevos para frontend (visual smoke test manual).

## Cómo acceder

```
http://127.0.0.1:8000/ui/
```

Endpoints API standalone también activos (Día 2 dashboard sigue en `/dashboard`).

## Lo que se ve en el dashboard

- **Top bar**: EIDOLON · día N · time_of_day · luna_phase · tick · [CREATOR] [AUDIT]
- **Mapa central** (75%): 8 locations CABA con labels, líneas de transición, 3 agentes con caritas + nombres encima
- **Side panel** (380px): 3 cards de agentes (Borges/Sócrates/Arendt) con barras de necesidades, panel Obra con tabs (2 libros, 1 ley, 2 posts, 1 ritual pending), action log live
- **Click agente** (mapa o card) → modal con perfil completo AI Town-style
- **Creator panel** → spawn piedra/árbol/pan/agua/libro en location dropdown
- **Audit dropdown** → 21 chequeos con status PASS/WARN/FAIL/INFO

## Acceptance criteria

- ✅ Dashboard abre en `http://127.0.0.1:8000/ui/` sin scroll horizontal
- ✅ Mapa muestra 8 locations CABA con colores correctos
- ✅ 3 agentes visibles con caritas (😐) y nombres
- ✅ In-transit interpolación + línea naranja dashed
- ✅ Side panel agentes 3 cards con barras
- ✅ Tabs Obra muestran libros (2), leyes (1), posts (2), rituales (1 pending)
- ✅ Action log 17 accepts + 6 rejects coloreados
- ✅ Click agente → modal con 9 secciones de profundidad
- ✅ Audit badge cliqueable con dropdown 21 checks
- ✅ Creator panel spawn objetos → aparecen en mapa con glow

## Estado al cierre Día 3

- **Frontend completo** y funcional (visual)
- **Spawn de objetos** primer paso de interacción Thronglets-style
- **0 cambios estructurales** al backend (solo nuevas tablas + endpoints)
- **0 regresiones** en tests Día 1-2
- **Tiempo real:** ~5h / **margen acumulado:** +7h (vs ~49h budget total restante)

## Fix post-entrega (mismo día)

Reporte del Creador: "Drag-drop no funciona. Agentes estáticos."

**Diagnóstico:**
1. `world_loop` no estaba corriendo en FastAPI (demo_seed solo seedea 13 ticks y para)
2. Drag-drop no implementado Día 3 inicial — solo había click-to-spawn

**Fixes aplicados:**

| Fix | Archivo | Detalle |
|---|---|---|
| Background sim task | `api/main.py` lifespan | `asyncio.create_task(WorldLoop.run())` arranca al boot del server. Configurable via `LIVE_TICK_SEC` env var (default 3s). Cancelado al shutdown. |
| Policies cíclicas famosos | `sim/famous_policies.py` (nuevo) | `CyclicPolicy` extiende ScriptedAgentPolicy con `_refill()` automático. 3 ciclos personality-aligned: Borges (biblio→escribir→café→hablar→reflexionar), Sócrates (plaza→hablar→mercado→trabajar), Arendt (café→proponer ley→hablar→ratificar). Cuando queue vacío, rellena. |
| Drag-drop SVG | `frontend/static/js/map.js` | `makeDraggable()` con pointerdown/move/up. `svgPoint()` convierte coordenadas pantalla → SVG. `nearestLocation()` calcula closest. Highlight `drop-target` mientras drag. Drop dentro 100u → POST `/admin/move_object`. |
| Endpoint move_object | `api/main.py` | `POST /admin/move_object {id, location_id}`. Actualiza `WorldObject.location_id` + log entry `MOVE_OBJECT` con agent_id="creator". |
| Drop-target CSS | `style.css` | `.loc-circle.drop-target` con stroke-width 3 + drop-shadow para feedback visual |
| `LIVE_TICK_SEC` env | `.env.example` (implícito) | Configurable. Demo usable a 2-3s/tick. Default 3s. |

**Verificación end-to-end:**
- Tick avanza 450→452 en 4s confirmado.
- 3 agentes alternan entre acciones diversas (MOVE, WORK, WRITE_BOOK, PROPOSE_INSTITUTION, TALK, REFLECT, etc.) sin scripts terminales.
- spawn_object endpoint OK.
- move_object endpoint OK.
- 6/6 tests pasan sin regresión.

## Próximo paso (Día 4)

Foco original Día 4 del plan: anti-bullshit artefactos + Obra de civ + WRITE_CODE E2B integration.
Plus pedido del Creador (carry-over):
- Tirar piedra → física → impacto → muerte por trauma
- Cadáver permanece visible
- Agente reacción a eventos (observation trigger ya está, falta wirear LLM-driven)
- Árbol frutal que crece + agentes lo comen
- LLM-driven decision real (reemplaza ciclo scripted)
