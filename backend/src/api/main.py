"""FastAPI app entrypoint."""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from pathlib import Path
from fastapi.staticfiles import StaticFiles

from ..db.session import init_db, get_session
from ..db.schema import (
    WorldState, Agent, Location, ActionLog,
    TextArtifact, CodeArtifact, Institution, PendingInstitution,
    Ritual, PendingRitual, Post, Dilema, DilemaResponse, WorldObject,
)
from ..sim.bootstrap import bootstrap_world


log = logging.getLogger("api")


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    bootstrap_world()
    # Spawn famosos si no existen
    from ..sim.seed_famous import spawn_famous
    spawn_famous()

    # Background world loop (Día 3+: agentes vivos)
    sim_task = None
    if os.getenv("DISABLE_SIM", "0") != "1":
        from ..sim.world_loop import WorldLoop
        from ..sim.famous_policies import build_all_policies
        tick_dur = float(os.getenv("LIVE_TICK_SEC", "3.0"))
        policies = build_all_policies()
        loop = WorldLoop(policies=policies, tick_duration_sec=tick_dur)
        log.info("starting background WorldLoop, tick=%ss, agents=%s",
                 tick_dur, list(policies.keys()))
        sim_task = asyncio.create_task(loop.run())

    try:
        yield
    finally:
        if sim_task is not None:
            sim_task.cancel()
            try:
                await sim_task
            except (asyncio.CancelledError, Exception):
                pass


app = FastAPI(title="Eidolon backend", lifespan=lifespan)


@app.get("/")
def root():
    return {"name": "eidolon", "version": "0.2.0-day2"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """Plain HTML dashboard: lista de endpoints + JSON pretty-printed con fetch."""
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Eidolon — Day 2 dashboard</title>
<style>
  body { font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
         background: #0c0c10; color: #d6d6dc; margin: 0; padding: 24px;
         line-height: 1.5; }
  h1 { color: #fff; }
  h2 { color: #6cc4ff; border-bottom: 1px solid #333; padding-bottom: 4px;
       margin-top: 32px; }
  a { color: #ffba6c; text-decoration: none; }
  a:hover { text-decoration: underline; }
  .grid { display: grid; grid-template-columns: 240px 1fr; gap: 32px; }
  .card { background: #16161c; border: 1px solid #2a2a32; padding: 12px 16px;
          margin-bottom: 12px; border-radius: 6px; }
  pre { background: #0a0a0e; padding: 12px; border-radius: 6px; overflow: auto;
        font-size: 12px; max-height: 50vh; }
  ul { list-style: none; padding: 0; }
  ul li { padding: 4px 0; }
  .badge-accept { color: #6fdc8c; }
  .badge-reject { color: #ff8389; }
  .small { color: #8d8d97; font-size: 12px; }
</style>
</head>
<body>
<h1>Eidolon — Day 2 dashboard</h1>
<p class="small">Refresh page after running <code>python -m src.sim.demo_seed</code> from <code>backend/</code> to populate the world.</p>

<div class="grid">
  <nav>
    <ul>
      <li><a href="#summary">Resumen</a></li>
      <li><a href="#time">/time (when)</a></li>
      <li><a href="#ontology">/ontology (what exists)</a></li>
      <li><a href="#world">/world</a></li>
      <li><a href="#agents">/agents</a></li>
      <li><a href="#books">/books</a></li>
      <li><a href="#letters">/letters</a></li>
      <li><a href="#institutions">/institutions</a></li>
      <li><a href="#rituals">/rituals</a></li>
      <li><a href="#posts">/posts</a></li>
      <li><a href="#dilemas">/dilemas</a></li>
      <li><a href="#log">/log</a></li>
      <li><a href="#log-rejects">/log?status=reject</a></li>
      <li><a href="#log-accepts">/log?status=accept</a></li>
      <li><a href="#audit"><b>/audit (21 chequeos)</b></a></li>
    </ul>
    <p class="small">JSON puro:<br>
      <a href="/agents">/agents</a><br>
      <a href="/books">/books</a><br>
      <a href="/institutions">/institutions</a><br>
      <a href="/log">/log</a> (todos)<br>
      <a href="/log?status=reject">/log?status=reject</a><br>
      <a href="/docs">/docs (Swagger UI)</a><br>
    </p>
  </nav>
  <main>
    <section id="summary"><h2>Resumen</h2><pre id="d-summary">cargando...</pre></section>
    <section id="time"><h2>Cuando estan viviendo</h2><pre id="d-time">cargando...</pre></section>
    <section id="ontology"><h2>Que existe en este mundo (ontologia)</h2><p class="small">Si agentes mencionan algo de <code>no_existe</code> el log marca soft-warning. WRITE_* no se rechaza, pero queda visible en el side_effect_summary.</p><pre id="d-ontology">cargando...</pre></section>
    <section id="world"><h2>Estado del mundo</h2><pre id="d-world">cargando...</pre></section>
    <section id="agents"><h2>Agentes</h2><pre id="d-agents">cargando...</pre></section>
    <section id="books"><h2>Libros (texto real)</h2><pre id="d-books">cargando...</pre></section>
    <section id="letters"><h2>Cartas</h2><pre id="d-letters">cargando...</pre></section>
    <section id="institutions"><h2>Instituciones — ratificadas + pendientes</h2><pre id="d-institutions">cargando...</pre></section>
    <section id="rituals"><h2>Rituales — ratificados + pendientes</h2><pre id="d-rituals">cargando...</pre></section>
    <section id="posts"><h2>Posts</h2><pre id="d-posts">cargando...</pre></section>
    <section id="dilemas"><h2>Dilemas + respuestas</h2><pre id="d-dilemas">cargando...</pre></section>
    <section id="log"><h2>Action log (los 30 mas recientes)</h2><pre id="d-log">cargando...</pre></section>
    <section id="log-rejects"><h2>Action log — rejects (anti-bullshit en accion)</h2><p class="small">Cada reject es el GM impidiendo una accion bullshit (sin contenido, sin prereq, etc). Eso es lo que QUEREMOS ver.</p><pre id="d-log-rejects">cargando...</pre></section>
    <section id="log-accepts"><h2>Action log — accepts (acciones reales aplicadas)</h2><pre id="d-log-accepts">cargando...</pre></section>
    <section id="audit"><h2>Audit report (4 categorias)</h2><p class="small">Coherence (artefactos vs ontologia), Personality (conducta vs seed), Sealed_world (sin influencia externa no autorizada), Capability (profundidad + diversidad). Status: PASS/WARN/FAIL/INFO.</p><pre id="d-audit">cargando...</pre></section>
  </main>
</div>

<script>
async function load(id, url) {
  try {
    const r = await fetch(url);
    document.getElementById(id).textContent = JSON.stringify(await r.json(), null, 2);
  } catch (e) {
    document.getElementById(id).textContent = "ERROR " + e;
  }
}
load("d-summary", "/summary");
load("d-time", "/time");
load("d-ontology", "/ontology");
load("d-world", "/world");
load("d-agents", "/agents");
load("d-books", "/books");
load("d-letters", "/letters");
load("d-institutions", "/institutions/all");
load("d-rituals", "/rituals/all");
load("d-posts", "/posts");
load("d-dilemas", "/dilemas");
load("d-log", "/log?limit=30");
load("d-log-rejects", "/log?status=reject&limit=100");
load("d-log-accepts", "/log?status=accept&limit=100");
load("d-audit", "/audit");
</script>
</body>
</html>"""


@app.get("/summary")
def summary():
    with get_session() as s:
        ws = s.get(WorldState, 1)
        return {
            "tick_actual": ws.tick_actual if ws else 0,
            "agents_alive": s.query(Agent).filter_by(alive=True).count(),
            "agents_total": s.query(Agent).count(),
            "books": s.query(TextArtifact).filter_by(tipo="book").count(),
            "letters": s.query(TextArtifact).filter_by(tipo="letter").count(),
            "code_artifacts": s.query(CodeArtifact).count(),
            "institutions_ratified": s.query(Institution).count(),
            "institutions_pending": s.query(PendingInstitution).filter_by(status="pending").count(),
            "rituals_ratified": s.query(Ritual).count(),
            "rituals_pending": s.query(PendingRitual).filter_by(status="pending").count(),
            "posts": s.query(Post).count(),
            "dilemas_active": s.query(Dilema).filter_by(active=True).count(),
            "dilemas_total": s.query(Dilema).count(),
            "dilema_responses": s.query(DilemaResponse).count(),
            "action_log_total": s.query(ActionLog).count(),
            "action_log_accepts": s.query(ActionLog).filter_by(status="accept").count(),
            "action_log_rejects": s.query(ActionLog).filter_by(status="reject").count(),
        }


@app.get("/world")
def world():
    with get_session() as s:
        ws = s.get(WorldState, 1)
        if ws is None:
            return {"error": "world not initialized"}
        return {
            "tick_actual": ws.tick_actual,
            "mapa_id": ws.mapa_id,
            "charter": ws.charter,
            "tech_level": ws.tech_level,
            "faucet": ws.faucet,
            "sink": ws.sink,
            "conocimiento_publico": ws.conocimiento_publico,
        }


@app.get("/agents")
def agents():
    with get_session() as s:
        rows = s.query(Agent).all()
        return [
            {
                "id": a.id, "nombre": a.nombre,
                "ubicacion": a.ubicacion, "x": a.x, "y": a.y,
                "in_transit": a.in_transit,
                "salud": a.salud, "gleam": a.gleam,
                "necesidades": a.necesidades,
                "conocimiento": a.conocimiento,
                "inventario": a.inventario,
                "moral_lines": a.moral_lines,
                "primary_conflict": a.primary_conflict,
                "relaciones": a.relaciones,
                "memoria_recent": a.memoria_recent,
                "alive": a.alive,
            }
            for a in rows
        ]


@app.get("/agents/{agent_id}")
def agent_detail(agent_id: str):
    with get_session() as s:
        a = s.get(Agent, agent_id)
        if a is None:
            return {"error": f"agent '{agent_id}' not found"}
        return {
            "id": a.id, "nombre": a.nombre,
            "seed_json": a.seed_json,
            "ubicacion": a.ubicacion, "x": a.x, "y": a.y,
            "in_transit": a.in_transit,
            "salud": a.salud, "gleam": a.gleam,
            "necesidades": a.necesidades,
            "conocimiento": a.conocimiento,
            "inventario": a.inventario,
            "moral_lines": a.moral_lines,
            "primary_conflict": a.primary_conflict,
            "relaciones": a.relaciones,
            "memoria_recent": a.memoria_recent,
            "memoria_summary": a.memoria_summary,
            "intencion_actual": a.intencion_actual,
            "welfare_birch": a.welfare_birch,
            "alive": a.alive,
        }


@app.get("/locations")
def locations():
    with get_session() as s:
        rows = s.query(Location).all()
        return [
            {
                "id": l.id, "nombre_display": l.nombre_display,
                "tipo": l.tipo, "x": l.x, "y": l.y, "radius": l.radius,
                "permite_trabajo": l.permite_trabajo,
                "objetos": l.objetos,
                "transitions": l.transitions,
            }
            for l in rows
        ]


@app.get("/books")
def books():
    with get_session() as s:
        rows = s.query(TextArtifact).filter_by(tipo="book").order_by(TextArtifact.tick).all()
        return [
            {
                "id": r.id, "autor_id": r.autor_id, "titulo": r.titulo,
                "contenido": r.contenido, "tick": r.tick,
                "location_id": r.location_id, "longitud_chars": len(r.contenido),
            } for r in rows
        ]


@app.get("/letters")
def letters():
    with get_session() as s:
        rows = s.query(TextArtifact).filter_by(tipo="letter").order_by(TextArtifact.tick).all()
        return [
            {
                "id": r.id, "autor_id": r.autor_id, "destinatario": r.titulo,
                "contenido": r.contenido, "tick": r.tick,
                "location_id": r.location_id,
            } for r in rows
        ]


@app.get("/code")
def code_artifacts():
    with get_session() as s:
        rows = s.query(CodeArtifact).order_by(CodeArtifact.tick).all()
        return [
            {
                "id": r.id, "autor_id": r.autor_id, "lenguaje": r.lenguaje,
                "spec": r.spec, "codigo": r.codigo, "stdout": r.stdout,
                "has_html_render": bool(r.html_render),
                "tick": r.tick,
            } for r in rows
        ]


@app.get("/code/{code_id}/render", response_class=HTMLResponse)
def code_render(code_id: int):
    """Serve HTML artifact as iframe-able page. ONLY html lenguaje."""
    with get_session() as s:
        a = s.get(CodeArtifact, code_id)
        if a is None:
            return HTMLResponse("<p>not found</p>", status_code=404)
        if a.lenguaje != "html" or not a.html_render:
            return HTMLResponse(
                f"<p style='font-family:monospace;color:#888'>"
                f"code #{code_id} ({a.lenguaje}) — sin HTML render</p>"
            )
        return HTMLResponse(a.html_render)


@app.get("/institutions")
def institutions_ratified():
    with get_session() as s:
        rows = s.query(Institution).order_by(Institution.ratified_tick).all()
        return [
            {"id": r.id, "nombre": r.nombre, "texto": r.texto, "ratified_tick": r.ratified_tick}
            for r in rows
        ]


@app.get("/institutions/pending")
def institutions_pending():
    with get_session() as s:
        rows = (
            s.query(PendingInstitution)
            .filter(PendingInstitution.status == "pending")
            .order_by(PendingInstitution.created_tick)
            .all()
        )
        return [
            {
                "id": r.id, "proposer_id": r.proposer_id, "nombre": r.nombre,
                "texto_ley": r.texto_ley, "ratify_count": r.ratify_count,
                "ratifiers": r.ratifiers, "status": r.status,
                "created_tick": r.created_tick,
            } for r in rows
        ]


@app.get("/institutions/all")
def institutions_all():
    return {"ratified": institutions_ratified(), "pending": institutions_pending()}


@app.get("/rituals")
def rituals_ratified():
    with get_session() as s:
        rows = s.query(Ritual).order_by(Ritual.ratified_tick).all()
        return [
            {
                "id": r.id, "nombre": r.nombre, "mci_concept": r.mci_concept,
                "frecuencia": r.frecuencia, "descripcion": r.descripcion,
                "ratified_tick": r.ratified_tick,
            } for r in rows
        ]


@app.get("/rituals/pending")
def rituals_pending():
    with get_session() as s:
        rows = (
            s.query(PendingRitual)
            .filter(PendingRitual.status == "pending")
            .order_by(PendingRitual.created_tick)
            .all()
        )
        return [
            {
                "id": r.id, "proposer_id": r.proposer_id, "nombre": r.nombre,
                "mci_concept": r.mci_concept, "frecuencia": r.frecuencia,
                "descripcion": r.descripcion, "ratify_count": r.ratify_count,
                "ratifiers": r.ratifiers, "status": r.status,
                "created_tick": r.created_tick,
            } for r in rows
        ]


@app.get("/rituals/all")
def rituals_all():
    return {"ratified": rituals_ratified(), "pending": rituals_pending()}


@app.get("/posts")
def posts():
    with get_session() as s:
        rows = s.query(Post).order_by(Post.tick).all()
        return [
            {"id": r.id, "autor_id": r.autor_id, "red": r.red,
             "contenido": r.contenido, "tick": r.tick}
            for r in rows
        ]


@app.get("/dilemas")
def dilemas():
    with get_session() as s:
        ds = s.query(Dilema).all()
        out = []
        for d in ds:
            responses = s.query(DilemaResponse).filter_by(dilema_id=d.id).all()
            out.append({
                "id": d.id, "texto": d.texto, "active": d.active,
                "launched_tick": d.launched_tick,
                "responses": [
                    {"agent_id": r.agent_id, "respuesta": r.respuesta, "tick": r.tick}
                    for r in responses
                ],
            })
        return out


@app.get("/log")
def log_endpoint(
    limit: int = 100,
    status: str | None = None,
    agent_id: str | None = None,
    action_type: str | None = None,
):
    with get_session() as s:
        q = s.query(ActionLog).order_by(ActionLog.id.desc())
        if status:
            q = q.filter(ActionLog.status == status)
        if agent_id:
            q = q.filter(ActionLog.agent_id == agent_id)
        if action_type:
            q = q.filter(ActionLog.action_type == action_type)
        rows = q.limit(limit).all()
        return [
            {
                "id": r.id, "tick": r.tick, "agent_id": r.agent_id,
                "action_type": r.action_type, "params": r.params,
                "status": r.status, "error_nl": r.error_nl,
                "side_effect_summary": r.side_effect_summary,
                "timestamp": r.timestamp.isoformat(),
            }
            for r in rows
        ]


@app.get("/time")
def time_now():
    from ..sim.time_of_day import from_world_state
    with get_session() as s:
        ws = s.get(WorldState, 1)
        if ws is None:
            return {"error": "world not initialized"}
        wt = from_world_state(ws)
        return {
            "tick": wt.tick,
            "dia_num": wt.dia_num,
            "time_of_day": wt.time_of_day,
            "luna_phase": wt.luna_phase,
            "is_night": wt.is_night,
            "dia_cycle_ticks": wt.dia_cycle,
            "luna_cycle_ticks": wt.luna_cycle,
            "describe": wt.describe(),
        }


@app.get("/ontology")
def ontology():
    with get_session() as s:
        ws = s.get(WorldState, 1)
        if ws is None:
            return {"error": "world not initialized"}
        return ws.world_ontology or {}


@app.post("/admin/reseed-demo")
def admin_reseed_demo():
    """DEV-ONLY: wipe DB + reseed via demo_seed.reset_and_seed_demo()."""
    from ..sim.demo_seed import reset_and_seed_demo
    return reset_and_seed_demo()


@app.get("/audit")
def audit():
    from ..audits.runner import run_all_audits
    return run_all_audits().to_dict()


@app.get("/world_objects")
def world_objects():
    with get_session() as s:
        rows = (
            s.query(WorldObject)
            .filter(WorldObject.state == "active")
            .order_by(WorldObject.created_tick.desc())
            .all()
        )
        return [
            {
                "id": w.id, "location_id": w.location_id,
                "object_type": w.object_type, "created_by": w.created_by,
                "created_tick": w.created_tick, "state": w.state,
                "metadata": w.metadata_json,
            } for w in rows
        ]


@app.post("/admin/revive")
def admin_revive(payload: dict):
    """Creator revive dead agent(s). Restore salud + reset needs + alive=True.

    Body: {"agent_id"?: str}  // si None: revive todos los muertos
    """
    agent_id = payload.get("agent_id")
    revived = []
    with get_session() as s:
        q = s.query(Agent)
        if agent_id:
            q = q.filter(Agent.id == agent_id)
        else:
            q = q.filter(Agent.alive == False)  # noqa: E712
        ws = s.get(WorldState, 1)
        tick = (ws.tick_actual or 0) if ws else 0
        for a in q.all():
            a.alive = True
            a.salud = 100.0
            a.necesidades = {
                "hambre": 20.0, "energia": 80.0, "sed": 10.0,
                "sueno": 5.0, "social": 50.0,
            }
            a.sleeping_until_tick = 0
            a.in_transit = None
            # Restore food in inventory
            inv = list(a.inventario or [])
            inv.append({"id": f"medialuna_revive_{a.id}", "es_comestible": True, "calorias": 30})
            inv.append({"id": f"agua_revive_{a.id}", "es_bebible": True})
            a.inventario = inv
            s.add(a)
            s.add(ActionLog(
                tick=tick, agent_id="creator", action_type="REVIVE",
                params={"target": a.id}, status="accept",
                side_effect_summary=f"creator revivió a {a.id} (+comida +agua)",
            ))
            revived.append(a.id)
        s.commit()
    return {"revived": revived}


@app.post("/admin/throw_object")
def admin_throw_object(payload: dict):
    """Creator launches object at target agent. Damage by object_type."""
    obj_id = payload.get("id")
    target_id = payload.get("agent_id")
    if not obj_id or not target_id:
        return {"error": "id + agent_id required"}
    with get_session() as s:
        wo = s.get(WorldObject, int(obj_id))
        if wo is None:
            return {"error": f"object {obj_id} no existe"}
        target = s.get(Agent, target_id)
        if target is None or not target.alive:
            return {"error": f"target '{target_id}' invalido o muerto"}
        from ..gm.handlers import THROW_DAMAGE_BY_TYPE
        damage = THROW_DAMAGE_BY_TYPE.get(wo.object_type, 10.0)
        ws = s.get(WorldState, 1)
        tick = (ws.tick_actual or 0) if ws else 0
        target.salud = max(0.0, target.salud - damage)
        died = False
        if target.salud <= 0:
            target.alive = False
            died = True
        wo.state = "thrown"
        wo.location_id = target.ubicacion  # objeto cae en location del target
        wo.metadata_json = dict(wo.metadata_json or {})
        wo.metadata_json.update({
            "thrown_by": "creator",
            "thrown_at_tick": tick,
            "target": target.id,
        })
        s.add(target)
        s.add(wo)
        s.add(ActionLog(
            tick=tick, agent_id="creator", action_type="THROW",
            params={"objeto_id": obj_id, "agente": target_id,
                    "object_type": wo.object_type},
            status="accept",
            side_effect_summary=(
                f"creator lanzo '{wo.object_type}' contra {target_id} "
                f"(-{damage} salud{', MURIO' if died else ''})"
            ),
        ))
        s.commit()
        return {
            "object_id": obj_id, "target": target_id,
            "damage": damage, "salud_restante": target.salud,
            "died": died,
        }


@app.post("/admin/move_object")
def admin_move_object(payload: dict):
    """Creator drag-drop: move existing WorldObject to another location."""
    obj_id = payload.get("id")
    new_loc = payload.get("location_id")
    if not obj_id or not new_loc:
        return {"error": "id + location_id required"}
    with get_session() as s:
        wo = s.get(WorldObject, int(obj_id))
        if wo is None:
            return {"error": f"object {obj_id} no existe"}
        loc = s.get(Location, new_loc)
        if loc is None:
            return {"error": f"location '{new_loc}' no existe"}
        old_loc = wo.location_id
        wo.location_id = new_loc
        ws = s.get(WorldState, 1)
        tick = (ws.tick_actual or 0) if ws else 0
        s.add(ActionLog(
            tick=tick, agent_id="creator", action_type="MOVE_OBJECT",
            params={"id": obj_id, "from": old_loc, "to": new_loc,
                    "object_type": wo.object_type},
            status="accept",
            side_effect_summary=f"creator movio '{wo.object_type}' de {old_loc} a {new_loc}",
        ))
        s.commit()
        return {"id": wo.id, "location_id": wo.location_id,
                "object_type": wo.object_type}


@app.post("/admin/spawn_object")
def admin_spawn_object(payload: dict):
    """Creator-injected world object (rocks, trees, food).

    Body: {"location_id": str, "object_type": str, "metadata"?: dict}
    Auditable: created_by="creator", action_log entry SPAWN_OBJECT.
    """
    location_id = payload.get("location_id")
    object_type = payload.get("object_type")
    metadata = payload.get("metadata") or {}
    if not location_id or not object_type:
        return {"error": "location_id + object_type required"}
    with get_session() as s:
        loc = s.get(Location, location_id)
        if loc is None:
            return {"error": f"location '{location_id}' no existe"}
        ws = s.get(WorldState, 1)
        tick = (ws.tick_actual or 0) if ws else 0
        wo = WorldObject(
            location_id=location_id,
            object_type=object_type,
            created_by="creator",
            created_tick=tick,
            state="active",
            metadata_json=metadata,
        )
        s.add(wo)
        s.add(ActionLog(
            tick=tick, agent_id="creator", action_type="SPAWN_OBJECT",
            params={"location_id": location_id, "object_type": object_type,
                    "metadata": metadata},
            status="accept",
            side_effect_summary=f"creator inyecto '{object_type}' en {location_id}",
        ))
        s.commit()
        s.refresh(wo)
        return {
            "id": wo.id, "location_id": wo.location_id,
            "object_type": wo.object_type, "created_tick": wo.created_tick,
            "created_by": wo.created_by,
        }


# Static frontend mount (must be LAST so it doesn't shadow other routes)
STATIC_DIR = Path(__file__).resolve().parents[3] / "frontend" / "static"
if STATIC_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(STATIC_DIR), html=True), name="ui")
