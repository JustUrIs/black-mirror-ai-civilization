"""Day 3+ scripted policies for famous agents — personality-aligned cycles
with food/water survival behavior + content variation.

Each famoso cycles through realistic routines:
- comer/beber cuando hambre/sed altos
- producir artefactos con variación (no copy-paste repetitivo)
- alinear acciones con personalidad seed

Survival: cada ciclo intercala GATHER (food/water del location actual o
mercado) + EAT/DRINK. Esto evita que mueran de hambre tras ~95 ticks.

DAY 4: cuando ANTHROPIC_API_KEY presente, build_all_policies retorna
LLMDrivenPolicy en vez de CyclicPolicy. Las decisiones vienen de Claude
Sonnet 4.6 leyendo personalidad + estado + ontology.
"""
import logging
import os
import random
from .world_loop import ScriptedAgentPolicy
from ..gm.actions import Action


log = logging.getLogger("famous_policies")


# Variaciones de contenido para evitar repetición visible
BORGES_BOOK_VARIANTS = [
    ("El espejo y el papel",
     "El espejo y el papel comparten la mansa terquedad de devolverte lo que les diste. "
     "Pero el espejo lo hace al instante, sin memoria. El papel, en cambio, espera. "
     "Espera el dia en que otro lo lea y entienda algo que vos no entendiste al escribirlo. "
     "Esa demora se llama, a veces, civilizacion."),
    ("Sobre los nombres",
     "Un nombre no describe a la persona; la encierra. Quien acepta un nombre acepta una jaula. "
     "Quien lo cambia rompe esa jaula pero entra en otra. El unico que escapa es el que se niega "
     "a tener un nombre. Y ese, por definicion, no podemos nombrar."),
    ("Inventario de un cafe",
     "Sobre la mesa hay una taza vacia, dos servilletas, una moneda de gleam con la cara borrosa, "
     "y un papel donde alguien escribio una palabra y la tacho. El que se sienta despues hereda "
     "ese tachado mas que cualquier herencia visible. La ciudad consiste en esa transferencia."),
    ("La biblioteca y la memoria",
     "Una biblioteca no contiene libros: contiene lectores que vendran. Cada anaquel es una "
     "promesa hecha a alguien que todavia no nacio. Esa promesa es la unica forma de inmortalidad "
     "que conozco. Por eso entro aca cada manana sin esperanza pero con disciplina."),
    ("Sobre dos espejos enfrentados",
     "Dos espejos enfrentados producen un pasillo infinito de copias. Cada copia es ligeramente "
     "mas pequena. En la quinta o sexta version del reflejo se nota algo que la primera nego: "
     "el cansancio. Como si solo el infinito tuviera derecho a estar cansado."),
]

ARENDT_LAW_VARIANTS = [
    ("Ley de la Voz Escuchada",
     "Toda voz tiene derecho a ser escuchada al menos una vez antes de que se decida lo que "
     "afecta a quien la posee. Esta regla precede a cualquier mayoria. Sin ella, no hay "
     "republica posible. Quien la viole pierde derecho de votar por dos ciclos."),
    ("Ley del Pan Comun",
     "Cuando hay menos pan que personas, se reparte en partes iguales hasta que la escasez "
     "termine. Nadie come dos veces antes de que todos hayan comido al menos una. El que "
     "acumule mas alla del dia debe declararlo en plaza al amanecer siguiente."),
    ("Ley del Silencio del Amanecer",
     "Entre la luna nueva y el primer amanecer del dia siguiente, ningun habitante hablara "
     "en voz alta en espacios publicos. Esta restriccion es voluntaria pero ratificada: el "
     "silencio compartido es la unica liturgia republicana que no requiere creencia."),
]

ARENDT_RITUAL_VARIANTS = [
    ("Lectura del Atardecer", "luna llena al atardecer",
     "Una vez por mes los habitantes que escribieron leen en voz alta un fragmento en la plaza. "
     "El resto escucha sin responder. La lectura termina cuando se hace de noche."),
    ("Pan Compartido", "luna creciente",
     "Cada quien lleva un pan al mercado y lo deja en la mesa central sin nombre. Despues come "
     "el pan que otro dejo. Sin gratitud explicita, sin deuda."),
]


def _interleave_eat(actions, every=4):
    """Intercala EAT/DRINK + GATHER (reabastece) cada N pasos para survival.

    Estrategia: come lo que tenga en inventario (EatHandler con item='ANY').
    Cada N acciones, MOVE a mercado, GATHER comida, GATHER agua, EAT, DRINK.
    """
    out = []
    for i, a in enumerate(actions):
        out.append(a)
        if (i + 1) % every == 0:
            out.append(Action(type="EAT", params={"item": "ANY"}))     # come lo que tenga
            out.append(Action(type="MOVE", params={"destino": "mercado_bonpland"}))
            out.append(Action(type="GATHER", params={"objeto": "puesto_comida"}))
            out.append(Action(type="DRINK", params={"fuente": "puesto_agua"}))
    return out


BORGES_HTML_DEMO = """<!doctype html>
<html><head><meta charset="utf-8"><title>Tema y variacion</title></head>
<body style="font-family:Georgia,serif;background:#0a0a0e;color:#d6d6dc;
            padding:18px;margin:0;line-height:1.5">
<h2 style="color:#6cc4ff;margin:0 0 8px">Tema y variacion</h2>
<p style="color:#8d8d97;font-size:11px;margin:0 0 10px">por borges, en eidolon</p>
<p>Cada lector lee un libro distinto. El primero busca la trama.</p>
<p>El segundo busca al autor.</p>
<p>El tercero, ya cansado, busca solo el silencio entre los parrafos.</p>
<p>Ninguno encuentra lo que busca; los tres encuentran otra cosa.</p>
<hr style="border-color:#2a2a35;margin:14px 0">
<p style="font-size:11px;color:#8d8d97;font-style:italic">
una sola pagina genera tres libros distintos. la biblioteca consiste en eso.</p>
</body></html>"""


def cycle_borges():
    variant = random.choice(BORGES_BOOK_VARIANTS)
    return _interleave_eat([
        Action(type="READ", params={"libro_id": "libro_borges_pre"}),
        Action(type="WORK", params={}),
        Action(type="WRITE_BOOK", params={"titulo": variant[0], "contenido_full": variant[1]}),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="TALK", params={
            "agente": "socrates",
            "contenido": f"Socrates, escribi sobre {variant[0].lower()}. Te lo presto si queres.",
        }),
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
        Action(type="MOVE", params={"destino": "depto_almagro_1"}),
        Action(type="WRITE_CODE", params={
            "spec": "una pagina sobre lectura multiple, html simple, palabra clave: variacion sobre tema",
            "lenguaje": "html",
            "codigo_full": BORGES_HTML_DEMO,
        }),
        Action(type="REFLECT", params={
            "prompt_interno": "que escribi y por que. el papel sigue esperando.",
        }),
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
        Action(type="MOVE", params={"destino": "biblioteca_nacional"}),
        Action(type="READ", params={"libro_id": "libro_platon_pre"}),
    ])


def cycle_socrates():
    target = random.choice(["arendt", "borges"])
    pregunta = random.choice([
        "decime por que aceptamos las palabras sin examinarlas primero.",
        "que es lo que sabemos hoy que ayer ignorabamos.",
        "si todos coinciden en algo, esa unanimidad es prueba o sospecha.",
        "que confundimos cuando confundimos certeza con verdad.",
        "para que sirve hacer preguntas si nadie va a contestar honesto.",
    ])
    return _interleave_eat([
        Action(type="TALK", params={"agente": target, "contenido": f"{target.capitalize()}, {pregunta}"}),
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
        Action(type="WORK", params={}),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="REFLECT", params={
            "prompt_interno": "que es lo que no se y deberia saber hoy.",
        }),
        Action(type="WORK", params={}),
        Action(type="MOVE", params={"destino": "parque_centenario"}),
    ])


def cycle_arendt():
    law = random.choice(ARENDT_LAW_VARIANTS)
    ritual = random.choice(ARENDT_RITUAL_VARIANTS)
    post_text = random.choice([
        "Una republica empieza cuando alguien escucha a otro sin querer responderle todavia.",
        "El silencio compartido es la forma mas honesta de la pluralidad.",
        "Pensar es lo que hago cuando estoy sola. Actuar es lo que hago cuando estoy con vos.",
        "La banalidad del mal no es maldad: es ausencia de pensamiento.",
        "Un voto sin escuchar es solo un ruido organizado.",
    ])
    return _interleave_eat([
        Action(type="WORK", params={}),
        Action(type="PROPOSE_INSTITUTION", params={
            "nombre": law[0], "texto_ley": law[1],
        }),
        Action(type="PROPOSE_RITUAL", params={
            "nombre": ritual[0], "mci_concept": "leer escuchar comer",
            "frecuencia": ritual[1], "descripcion": ritual[2],
        }),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="TALK", params={
            "agente": "borges",
            "contenido": f"Borges, ratifica mi {law[0]}. Necesitamos un voto antes de la noche.",
        }),
        Action(type="POST", params={"red": "default", "contenido": post_text}),
        Action(type="REFLECT", params={
            "prompt_interno": "que escuche hoy y que no entendi.",
        }),
    ])


CYCLES = {
    "borges": cycle_borges,
    "socrates": cycle_socrates,
    "arendt": cycle_arendt,
}


class CyclicPolicy(ScriptedAgentPolicy):
    """ScriptedAgentPolicy que rellena el queue cuando se vacia."""

    def __init__(self, agent_id: str):
        super().__init__(agent_id=agent_id, queue=[])
        self._cycle_fn = CYCLES.get(agent_id, lambda: [])
        self._refill()

    def _refill(self):
        self.queue.extend(self._cycle_fn())

    def next_action(self, trigger=None):
        if not self.queue:
            self._refill()
        if not self.queue:
            return None
        return self.queue.pop(0)


def build_all_policies() -> dict:
    """Build policies for famous agents.

    Priority:
    1. ANTHROPIC_API_KEY + USE_LLM_POLICY=1 → LLMDrivenPolicy (Claude Sonnet).
    2. USE_CYCLIC_POLICY=1 → legacy CyclicPolicy (rigid scripted cycles).
    3. Default → SmartPolicy: reactive heuristic. Acts on state (hambre/sed/
       energia), reacts to triggers, expresses personality.

    SmartPolicy emits `_rationale` in every Action so the UI can show the
    internal monologue even without an LLM.
    """
    use_llm = (
        os.getenv("ANTHROPIC_API_KEY")
        and os.getenv("USE_LLM_POLICY", "1") != "0"
    )
    if use_llm:
        from ..mind.llm import LLMGateway
        from .llm_policy import LLMDrivenPolicy
        gateway = LLMGateway(stub_mode=False)
        log.info("LLM-driven policy ACTIVE for famosos (USE_LLM_POLICY=1)")
        return {
            aid: LLMDrivenPolicy(agent_id=aid, gateway=gateway)
            for aid in CYCLES.keys()
        }

    if os.getenv("USE_CYCLIC_POLICY", "0") == "1":
        log.info("Legacy CyclicPolicy ACTIVE (USE_CYCLIC_POLICY=1)")
        return {aid: CyclicPolicy(aid) for aid in CYCLES.keys()}

    from .smart_policy import build_smart_policies
    log.info("SmartPolicy ACTIVE (reactive heuristic; rationale visible per action)")
    return build_smart_policies()
