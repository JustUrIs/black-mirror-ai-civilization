"""FastAPI app entrypoint."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from ..db.session import init_db, get_session
from ..db.schema import WorldState, Agent, Location, ActionLog
from ..sim.bootstrap import bootstrap_world


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    bootstrap_world()
    yield


app = FastAPI(title="Eidolon backend", lifespan=lifespan)


@app.get("/")
def root():
    return {"name": "eidolon", "version": "0.1.0-day1"}


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
        }


@app.get("/agents")
def agents():
    with get_session() as s:
        rows = s.query(Agent).all()
        return [
            {
                "id": a.id, "nombre": a.nombre, "ubicacion": a.ubicacion,
                "salud": a.salud, "necesidades": a.necesidades,
                "alive": a.alive,
            }
            for a in rows
        ]


@app.get("/locations")
def locations():
    with get_session() as s:
        rows = s.query(Location).all()
        return [
            {
                "id": l.id, "nombre_display": l.nombre_display,
                "tipo": l.tipo, "objetos": l.objetos,
                "transitions": l.transitions,
            }
            for l in rows
        ]


@app.get("/log")
def log(limit: int = 100):
    with get_session() as s:
        rows = (
            s.query(ActionLog)
            .order_by(ActionLog.id.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "tick": r.tick, "agent_id": r.agent_id,
                "action_type": r.action_type, "params": r.params,
                "status": r.status, "error_nl": r.error_nl,
                "side_effect": r.side_effect_summary,
                "timestamp": r.timestamp.isoformat(),
            }
            for r in rows
        ]
