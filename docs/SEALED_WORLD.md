# Sealed World — principio arquitectónico

> El mundo de Eidolon es **cerrado por default**. Agentes viven sin influencia
> externa salvo canales explícitos autorizados por el Creador.

## Por qué importa

Si cualquier proceso puede inyectar estado en el mundo (random events automáticos,
news feeds, llamadas a APIs externas), la civilización deja de ser **auditable**:
no se puede demostrar que lo que pasa es emergente de los agentes vs orquestado
por fuera. El log "no scripteado" del pitch (§14 plan v4) depende de este sello.

## Canales de entrada autorizados

Solo estos pueden modificar estado del mundo:

| Canal | Quién | Cuándo |
|---|---|---|
| **`bootstrap`** | sistema | una vez al spawn del mundo (locations + WorldState) |
| **agent action** | `validate_and_apply()` | cada tick, vía GM con prereqs |
| **tick decay / sink** | `world_loop.run_one_tick()` | sistema, física del mundo |
| **`Dilema` injection** | Creador, vía `/admin` POST | manual, audit-logged |
| **spawn agent (seed JSON upload)** | Creador, vía endpoint upload | explícito |
| **`AUTO_PROMOTE`** | sistema | cuando ratify_count >= 3 (registrado en ActionLog con agent_id="system") |

**Nada más.** No hay cron jobs random, no hay event hooks externos, no hay scraping
de web, no hay APIs de noticias.

## Canales de salida (lectura solamente)

| Canal | Propósito |
|---|---|
| `GET /world`, `/agents`, etc. | Inspección externa (read-only) |
| `GET /audit` | Verificación post-sim |
| Crónica + diarios (Day 5+) | Outputs narrativos del mundo |

## Auditoría automática (sealed_world checks)

`backend/src/audits/sealed_world.py` verifica continuamente:

1. **action_log_origins**: cada entrada de `ActionLog` debe tener `agent_id` =
   un agente real OR uno de `ALLOWED_SYSTEM_AGENTS` (`system`, `creator`,
   `bootstrap`).
2. **artifacts_have_authors**: text/code/post artifacts deben tener `autor_id`
   que apunte a un agente existente.
3. **dilemas_authorized**: cada `Dilema` debe tener `launched_tick >= 0`.
4. **dilema_responses_match_agents**: cada `DilemaResponse.agent_id` debe ser
   agente real.
5. **inventory_origin** (post-MVP): per-item provenance ledger.

Si cualquiera FAILea, hay un leak en el sello.

## Roadmap post-MVP

- Provenance ledger para inventario (cada item con `gathered_from`, `traded_from`, etc.)
- Welfare/ombuds canal de salida + entrada (Day 5+ si lo activamos)
- Sub-simulación (cap depth 2) — más entradas a auditar
- Founder mode "oráculos del afuera" — entrada legítima pero requiere
  explicit `creator` agent_id
