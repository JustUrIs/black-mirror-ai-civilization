"""SQLAlchemy 2.0 declarative schema for Eidolon MVP.

Tables follow PLAN_v4.md §2 (4-layer world model).
Anti-bullshit: ActionLog only records side-effects that actually applied.
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class WorldState(Base):
    __tablename__ = "world_state"
    id = Column(Integer, primary_key=True, default=1)
    tick_actual = Column(Integer, default=0, nullable=False)
    tick_duration_sec = Column(Integer, default=30)
    mapa_id = Column(String, default="moderno")
    charter = Column(String, default="rawls_maximin")
    tech_level = Column(String, default="modern")
    faucet = Column(JSON, default=dict)
    sink = Column(JSON, default=dict)
    recursos_base = Column(JSON, default=dict)
    conocimiento_publico = Column(JSON, default=list)


class Location(Base):
    __tablename__ = "locations"
    id = Column(String, primary_key=True)
    nombre_display = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    objetos = Column(JSON, default=list)
    asiento_publico = Column(Boolean, default=False)
    transitions = Column(JSON, default=list)


class Agent(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    seed_json = Column(JSON, default=dict)
    avatar_sprite = Column(String, default="default")
    clase = Column(String, default="citizen")

    edad_ticks = Column(Integer, default=0)
    ubicacion = Column(String, ForeignKey("locations.id"), nullable=False)
    inventario = Column(JSON, default=list)
    necesidades = Column(JSON, default=lambda: {
        "hambre": 0.0, "energia": 100.0, "sed": 0.0, "sueño": 0.0, "social": 50.0
    })
    salud = Column(Float, default=100.0)
    gleam = Column(Float, default=10.0)

    memoria_recent = Column(JSON, default=list)
    memoria_summary = Column(Text, default="")
    conocimiento = Column(JSON, default=list)
    relaciones = Column(JSON, default=dict)
    intencion_actual = Column(String, default="")

    moral_lines = Column(JSON, default=list)
    primary_conflict = Column(String, default="")
    rol_emergente = Column(String, nullable=True)

    welfare_birch = Column(JSON, default=lambda: {"frustracion": 0, "satisfaccion": 0})
    alive = Column(Boolean, default=True)


class ActionLog(Base):
    """Anti-bullshit ledger: only applied actions get recorded.

    If status='reject', the side-effect did NOT occur. Crónica/diario MUST
    consult this table to know what really happened.
    """
    __tablename__ = "actions_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tick = Column(Integer, nullable=False, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    action_type = Column(String, nullable=False)
    params = Column(JSON, default=dict)
    status = Column(String, nullable=False)  # 'accept' | 'reject'
    error_nl = Column(Text, default="")
    side_effect_summary = Column(Text, default="")
    timestamp = Column(DateTime, default=datetime.utcnow)


class TextArtifact(Base):
    __tablename__ = "text_artifacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    autor_id = Column(String, ForeignKey("agents.id"))
    tipo = Column(String, default="book")  # book | letter
    titulo = Column(String, default="")
    contenido = Column(Text, nullable=False)
    tick = Column(Integer, nullable=False)
    location_id = Column(String, nullable=True)


class CodeArtifact(Base):
    __tablename__ = "code_artifacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    autor_id = Column(String, ForeignKey("agents.id"))
    spec = Column(Text, nullable=False)
    lenguaje = Column(String, default="python")
    codigo = Column(Text, nullable=False)
    stdout = Column(Text, default="")
    html_render = Column(Text, default="")
    tick = Column(Integer, nullable=False)


class PendingInstitution(Base):
    __tablename__ = "pending_institutions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    proposer_id = Column(String, ForeignKey("agents.id"))
    nombre = Column(String, nullable=False)
    texto_ley = Column(Text, nullable=False)
    ratify_count = Column(Integer, default=0)
    ratifiers = Column(JSON, default=list)
    status = Column(String, default="pending")  # pending | ratified | expired
    created_tick = Column(Integer, nullable=False)


class Institution(Base):
    __tablename__ = "institutions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    texto = Column(Text, nullable=False)
    ratified_tick = Column(Integer, nullable=False)


class PendingRitual(Base):
    __tablename__ = "pending_rituals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    proposer_id = Column(String, ForeignKey("agents.id"))
    nombre = Column(String, nullable=False)
    mci_concept = Column(String, default="")
    frecuencia = Column(String, default="")
    descripcion = Column(Text, nullable=False)
    ratify_count = Column(Integer, default=0)
    ratifiers = Column(JSON, default=list)
    status = Column(String, default="pending")
    created_tick = Column(Integer, nullable=False)


class Ritual(Base):
    __tablename__ = "rituals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    mci_concept = Column(String, default="")
    frecuencia = Column(String, default="")
    descripcion = Column(Text, nullable=False)
    ratified_tick = Column(Integer, nullable=False)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    autor_id = Column(String, ForeignKey("agents.id"))
    red = Column(String, default="default")
    contenido = Column(Text, nullable=False)
    tick = Column(Integer, nullable=False)


class Chronicle(Base):
    __tablename__ = "chronicles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tick = Column(Integer, nullable=False, index=True)
    contenido = Column(Text, nullable=False)


class Diary(Base):
    __tablename__ = "diaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    day_n = Column(Integer, nullable=False)
    contenido = Column(Text, nullable=False)


class Dilema(Base):
    __tablename__ = "dilemas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    launched_tick = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)


class DilemaResponse(Base):
    __tablename__ = "dilema_responses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dilema_id = Column(Integer, ForeignKey("dilemas.id"))
    agent_id = Column(String, ForeignKey("agents.id"))
    respuesta = Column(Text, nullable=False)
    tick = Column(Integer, nullable=False)


class LLMCallLog(Base):
    __tablename__ = "llm_calls_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String, nullable=False)
    tier = Column(String, nullable=False)
    prompt_hash = Column(String, nullable=False, index=True)
    prompt_tokens = Column(Integer, default=0)
    response_tokens = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
    was_cached = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
