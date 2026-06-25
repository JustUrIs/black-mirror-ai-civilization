# Eidolon — Espejo del Creador

Simulador de civilización digital sembrada con personas reales. Agentes LLM viven en CABA, escriben libros, votan leyes, pelean. Output verificable, no scripted.

> **Estado:** Día 1 de 7 (MVP en construcción). Ver `PLAN_v4.md` para roadmap.

## Stack

- **Backend:** FastAPI + SQLAlchemy + SQLite + LangGraph
- **LLM:** Claude Sonnet 4.6 (leaders) + Haiku 4.5 (crowd) + Gemini Flash 2.0 (narrator) + Cerebras Llama 3.3 70B (backup gratis)
- **Sandbox código:** E2B free tier
- **Frontend (Día 3+):** Phaser 3 + Next.js + Tailwind
- **Licencia:** MIT

## Anti-bullshit principle

Si un agente declara una acción (`WRITE_BOOK`), el Game Master EXIGE que produzca el artefacto real en la DB. Sin contenido verificable, GM rechaza. Crónica/diario solo narra acciones aplicadas — nunca intenciones que no produjeron side-effect.

## Run local

```bash
cp .env.example .env
# editar .env con keys
docker compose up --build
```

Endpoints (Día 1):
- `GET /` — info
- `GET /world` — estado mundo
- `GET /agents` — lista agentes
- `GET /locations` — locations del mapa moderno
- `GET /log?limit=100` — action log auditable

## Documentos

- `PLAN_v4.md` — plan MVP firmado, 7 días
- `PLAN_MAESTRO.md` — plan v3 (referencia, no ejecutar)
- `SYNTHESIS.md`, `DUMP_1.md`..`DUMP_5.md` — investigación de fondo
