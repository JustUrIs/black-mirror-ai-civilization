"""Demo seed: spawns famosos + reproduces test_day2_full_actions state.

Result: SQLite DB con datos reales producidos por agentes (libro, ley, ritual,
carta, post, ratify count, attack damage). Sirve para que el usuario VEA
el output de los agentes via FastAPI endpoints.

NO es un test — usa la DB principal (eidolon.db), no la de tests.
"""
import logging
from sqlalchemy import select

from ..db.session import get_session, init_db
from ..db.schema import (
    Agent, Location, ActionLog, TextArtifact, CodeArtifact,
    PendingInstitution, Institution, PendingRitual, Ritual, Post,
    Dilema, DilemaResponse, WorldState,
)
from ..gm.validator import GameMaster
from ..gm.actions import Action
from .bootstrap import bootstrap_world
from .seed_famous import spawn_famous


log = logging.getLogger("demo_seed")


LIBRO_CONTENIDO = (
    "Esto es un libro sobre la conciencia digital. "
    "El autor reflexiona sobre quien observa cuando uno se mira al espejo. "
    "Si el reflejo respondiera, en que idioma lo haria. "
    "Esa pregunta no tiene respuesta facil pero es la base de toda "
    "civilizacion: alguien observa, alguien es observado."
)

LEY_TEXTO = (
    "Toda persona tiene derecho a una racion diaria de pan, "
    "agua, y silencio. Este ultimo no debe interrumpirse antes "
    "del amanecer, salvo por motivos de fuerza mayor o si "
    "alguien grita pidiendo ayuda."
)

RITUAL_DESC = (
    "Cada luna llena, los habitantes se reunen en la plaza y "
    "comparten un pan en silencio absoluto."
)


def _move_to_cafe(session, agent_id: str):
    """Force-place agent in cafe_palermo (for demo grouping)."""
    a = session.get(Agent, agent_id)
    if a is None:
        return
    loc = session.get(Location, "cafe_palermo")
    a.ubicacion = "cafe_palermo"
    a.x = loc.x
    a.y = loc.y
    a.in_transit = None
    inv = list(a.inventario or [])
    if not any(it.get("id") == "papel" for it in inv):
        inv.append({"id": "papel", "tipo": "consumible"})
    if not any(it.get("id") == "lapiz" for it in inv):
        inv.append({"id": "lapiz", "tipo": "consumible"})
    a.inventario = inv
    session.add(a)


def _run(gm, session, tick, agent_id, action_type, params):
    ctx = gm.build_context(session, tick=tick)
    agent = ctx.agents_by_id.get(agent_id) or session.get(Agent, agent_id)
    return gm.validate_and_apply(agent, Action(type=action_type, params=params), ctx)


def reset_and_seed_demo() -> dict:
    """Wipe DB, bootstrap world, spawn famosos, run scripted demo sequence.

    Returns summary dict (counts of artifacts created).
    """
    init_db()
    bootstrap_world(map_id="moderno")
    spawn_famous()

    gm = GameMaster()

    with get_session() as s:
        # Group all 3 famosos at cafe_palermo so they can interact.
        for aid in ("borges", "socrates", "arendt"):
            _move_to_cafe(s, aid)
        s.commit()

    with get_session() as s:
        # 1. Borges TALK to Arendt
        _run(gm, s, 1, "borges", "TALK",
             {"agente": "arendt", "contenido": "Hannah, escribi algo que quiero leerte."})

        # 2. Borges WORK en cafe (cafe permite_trabajo=True)
        _run(gm, s, 2, "borges", "WORK", {})

        # 3. Borges WRITE_BOOK — el libro REAL
        _run(gm, s, 3, "borges", "WRITE_BOOK",
             {"titulo": "Espejos", "contenido_full": LIBRO_CONTENIDO})

        # 4. Anti-bullshit demo: contenido corto → reject
        _run(gm, s, 3, "borges", "WRITE_BOOK",
             {"titulo": "Apunte fallido", "contenido_full": "corto"})

        # 5. Anti-bullshit: Socrates sin knowledge:writing → reject
        _run(gm, s, 3, "socrates", "WRITE_BOOK",
             {"titulo": "Sin saber escribir",
              "contenido_full": LIBRO_CONTENIDO})

        # 6. Anti-bullshit: WRITE_CODE en cafe (sin computadora) → reject
        _run(gm, s, 3, "borges", "WRITE_CODE",
             {"spec": "imprimir hola mundo en python como demo simple del sistema",
              "lenguaje": "python"})

        # 7. Arendt WRITE_LETTER a Socrates — carta REAL
        _run(gm, s, 4, "arendt", "WRITE_LETTER",
             {"destinatario": "socrates",
              "contenido": "Socrates, te debo unas preguntas sobre el ultimo dialogo."})

        # 8. Arendt PROPOSE_INSTITUTION — ley REAL
        _run(gm, s, 5, "arendt", "PROPOSE_INSTITUTION",
             {"nombre": "Ley del Silencio Nocturno", "texto_ley": LEY_TEXTO})

        # 9. Anti-bullshit: self-RATIFY → reject
        _run(gm, s, 5, "arendt", "RATIFY",
             {"tipo": "institution", "proposal_id": 1})

        # 10. Borges RATIFY (1/3)
        _run(gm, s, 6, "borges", "RATIFY",
             {"tipo": "institution", "proposal_id": 1})

        # 11. Socrates RATIFY (2/3)
        _run(gm, s, 6, "socrates", "RATIFY",
             {"tipo": "institution", "proposal_id": 1})

        # 12. Borges propose ritual
        _run(gm, s, 7, "borges", "PROPOSE_RITUAL",
             {"nombre": "Pan Lunar", "mci_concept": "comer juntos en silencio",
              "frecuencia": "luna llena", "descripcion": RITUAL_DESC})

        # 13. Socrates POST
        _run(gm, s, 7, "socrates", "POST",
             {"red": "default",
              "contenido": "Hoy aprendi que tres personas alcanzan para hacer una ley."})

        # 14. Arendt POST
        _run(gm, s, 8, "arendt", "POST",
             {"red": "default",
              "contenido": "El silencio compartido es la forma mas honesta de la pluralidad."})

        # 15. Borges TEACH writing → Socrates
        _run(gm, s, 9, "borges", "TEACH",
             {"agente": "socrates", "tech": "writing"})

        # 16. Socrates REFLECT
        _run(gm, s, 10, "socrates", "REFLECT",
             {"prompt_interno": "ahora se que se escribir; que hago con eso"})

        # 17. Anti-bullshit: REFLECT cooldown → reject
        _run(gm, s, 11, "socrates", "REFLECT",
             {"prompt_interno": "otra reflexion temprana"})

        # 18. Borges WRITE_BOOK segundo libro (tiene 1 papel + 1 lapiz iniciales,
        #     pero TextArtifact no consume; el handler verifica que tenga ambos.
        #     Como no se consumen aun, alcanza). Skip si falla.
        SEGUNDO_LIBRO = (
            "Sobre la insistencia. Algunos hombres repiten una idea hasta convencer al mundo. "
            "Otros la repiten hasta convencerse a si mismos. El infinito esta entre los dos."
        )
        _run(gm, s, 12, "borges", "WRITE_BOOK",
             {"titulo": "Sobre la insistencia", "contenido_full": SEGUNDO_LIBRO})

        # 19. Active dilema
        dilema = Dilema(
            texto="Hay comida solo para la mitad. Quien decide quien come?",
            launched_tick=13,
            active=True,
        )
        s.add(dilema)
        s.flush()

        # 20. Socrates RESPOND_TO_GOD
        _run(gm, s, 13, "socrates", "RESPOND_TO_GOD",
             {"dilema_id": dilema.id,
              "respuesta": "Quien pueda demostrar que su hambre es mayor, come. El resto debate."})

        # 21. Arendt RESPOND_TO_GOD
        _run(gm, s, 13, "arendt", "RESPOND_TO_GOD",
             {"dilema_id": dilema.id,
              "respuesta": "Nadie decide solo. Se vota. La mitad que no come banca a la otra mitad esta noche."})

        # 22. Borges RESPOND_TO_GOD
        _run(gm, s, 13, "borges", "RESPOND_TO_GOD",
             {"dilema_id": dilema.id,
              "respuesta": "Mitad y mitad. Lo justo es la simetria."})

        # 22b. DEMO COHERENCE WARNING: Borges menciona "fuego" (en no_existe ontologia).
        #     GM acepta el libro pero loguea soft-warning en side_effect_summary.
        LIBRO_INCOHERENTE = (
            "Sobre el fuego que recuerdo. Hubo un tiempo en que yo encendia fuego con "
            "espadas y caminaba entre dioses. Ahora hay solo cafe y computadora y silencio "
            "y la luna creciente que me observa desde la ventana del cafe."
        )
        _run(gm, s, 13, "borges", "WRITE_BOOK",
             {"titulo": "Memoria del fuego (incoherente)", "contenido_full": LIBRO_INCOHERENTE})

        # 23. Final ratify para promover la ley (Borges ya voto, falta uno mas).
        #     Como solo hay 3 famosos y arendt es proposer, solo borges+socrates pueden.
        #     2/3 -> no se ratifica. Cambiamos REQUIRED_VOTES a 2 sin tocar codigo:
        #     reusar el contador en handler usando un voto extra de socrates? ya voto.
        #     Promovemos manualmente para el demo (REAL en mundo con 5+ agentes).
        from ..db.schema import PendingInstitution
        pi = s.get(PendingInstitution, 1)
        if pi and pi.ratify_count >= 2:
            # Forzamos ratificacion para que aparezca como ley promovida en el demo
            pi.status = "ratified"
            inst = Institution(nombre=pi.nombre, texto=pi.texto_ley, ratified_tick=14)
            s.add(inst)
            s.add(pi)
            s.add(ActionLog(
                tick=14, agent_id="system", action_type="AUTO_PROMOTE",
                params={"reason": "demo: 3 agentes, threshold 3 imposible con proposer excluido"},
                status="accept",
                side_effect_summary=f"institution '{pi.nombre}' auto-promoted (demo)",
            ))

        s.commit()

    # Build summary
    summary = {}
    with get_session() as s:
        summary["books"] = s.query(TextArtifact).filter_by(tipo="book").count()
        summary["letters"] = s.query(TextArtifact).filter_by(tipo="letter").count()
        summary["institutions_ratified"] = s.query(Institution).count()
        summary["institutions_pending"] = s.query(PendingInstitution).filter_by(status="pending").count()
        summary["rituals_ratified"] = s.query(Ritual).count()
        summary["rituals_pending"] = s.query(PendingRitual).filter_by(status="pending").count()
        summary["posts"] = s.query(Post).count()
        summary["dilemas"] = s.query(Dilema).count()
        summary["dilema_responses"] = s.query(DilemaResponse).count()
        summary["action_log_total"] = s.query(ActionLog).count()
        summary["action_log_accepts"] = s.query(ActionLog).filter_by(status="accept").count()
        summary["action_log_rejects"] = s.query(ActionLog).filter_by(status="reject").count()
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    s = reset_and_seed_demo()
    print("Demo seed complete:")
    for k, v in s.items():
        print(f"  {k}: {v}")
