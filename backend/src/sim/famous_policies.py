"""Day 3 scripted policies for famous agents — personality-aligned cycles.

Each famoso tiene una rutina ciclica de acciones consistente con su seed:
- Borges: biblioteca -> escribe/lee -> cafe -> habla -> reflexiona
- Sócrates: plaza -> habla con quien este -> mercado -> trabaja -> plaza
- Arendt: cafe -> escribe/propone ley -> plaza -> habla -> reflexiona

Cuando el queue se vacia, se rellena. Day 5+ LLM-driven reemplaza esto.
"""
import logging
from .world_loop import ScriptedAgentPolicy
from ..gm.actions import Action


log = logging.getLogger("famous_policies")


BORGES_LIBRO_CONTENIDO = (
    "El espejo y el papel comparten la mansa terquedad de devolverte lo que les diste. "
    "Pero el espejo lo hace al instante, sin memoria. El papel, en cambio, espera. "
    "Espera el dia en que otro lo lea y entienda algo que vos no entendiste al escribirlo. "
    "Esa demora se llama, a veces, civilizacion."
)

BORGES_LIBRO_2 = (
    "Sobre los nombres. Un nombre no describe a la persona; la encierra. "
    "Quien acepta un nombre acepta una jaula. Quien lo cambia rompe esa jaula "
    "pero entra en otra. El unico que escapa es el que se niega a tener un nombre. "
    "Y ese, por definicion, no podemos nombrar."
)

ARENDT_LEY_TEXTO = (
    "Toda voz tiene derecho a ser escuchada al menos una vez antes de que se decida "
    "lo que afecta a quien la posee. Esta regla precede a cualquier mayoria. Sin ella, "
    "no hay republica posible. Quien la viole pierde su derecho de votar por dos ciclos."
)

ARENDT_RITUAL_DESC = (
    "Una vez por mes, en el atardecer, los habitantes que escribieron ese mes "
    "leen en voz alta un fragmento de su obra en la plaza. El resto escucha en silencio."
)


def cycle_borges():
    """Ciclo: bibliotecaria -> escribir/leer -> cafe -> hablar -> reflexionar -> repetir"""
    return [
        Action(type="READ", params={"libro_id": "libro_borges_pre"}),
        Action(type="WORK", params={}),  # solo si en cafe; sino reject
        Action(type="WRITE_BOOK", params={
            "titulo": "El espejo y el papel",
            "contenido_full": BORGES_LIBRO_CONTENIDO,
        }),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="TALK", params={
            "agente": "socrates",
            "contenido": "Sócrates, escribi algo sobre el papel y el espejo.",
        }),
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
        Action(type="WORK", params={}),
        Action(type="WRITE_BOOK", params={
            "titulo": "Sobre los nombres",
            "contenido_full": BORGES_LIBRO_2,
        }),
        Action(type="REFLECT", params={
            "prompt_interno": "que escribi y por que. el papel sigue esperando.",
        }),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="MOVE", params={"destino": "biblioteca_nacional"}),
        Action(type="READ", params={"libro_id": "libro_platon_pre"}),
    ]


def cycle_socrates():
    """Ciclo: plaza -> hablar -> mercado -> trabajar -> plaza -> reflexionar"""
    return [
        Action(type="TALK", params={
            "agente": "arendt",
            "contenido": "Arendt, decime por que te molesta que la gente obedezca sin pensar.",
        }),
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
        Action(type="WORK", params={}),
        Action(type="TALK", params={
            "agente": "borges",
            "contenido": "Borges, escribir es huir de lo dicho o quedarse en lo escrito?",
        }),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="REFLECT", params={
            "prompt_interno": "que es lo que no se y deberia saber hoy.",
        }),
        Action(type="MOVE", params={"destino": "mercado_bonpland"}),
        Action(type="WORK", params={}),
        Action(type="WORK", params={}),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="MOVE", params={"destino": "parque_centenario"}),
    ]


def cycle_arendt():
    """Ciclo: cafe -> escribir/proponer -> plaza -> hablar -> ratificar -> repetir"""
    return [
        Action(type="WORK", params={}),
        Action(type="PROPOSE_INSTITUTION", params={
            "nombre": "Ley de la Voz Escuchada",
            "texto_ley": ARENDT_LEY_TEXTO,
        }),
        Action(type="PROPOSE_RITUAL", params={
            "nombre": "Lectura del Atardecer",
            "mci_concept": "leer en voz alta lo escrito",
            "frecuencia": "luna llena al atardecer",
            "descripcion": ARENDT_RITUAL_DESC,
        }),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="TALK", params={
            "agente": "borges",
            "contenido": "Borges, te invito a ratificar mi ley nueva. Es sobre la voz.",
        }),
        Action(type="MOVE", params={"destino": "biblioteca_nacional"}),
        Action(type="READ", params={"libro_id": "libro_borges_pre"}),
        Action(type="MOVE", params={"destino": "plaza_italia"}),
        Action(type="POST", params={
            "red": "default",
            "contenido": "Una republica empieza cuando alguien escucha a otro sin querer responderle todavia.",
        }),
        Action(type="REFLECT", params={
            "prompt_interno": "que escuche hoy y que no entendi.",
        }),
        Action(type="MOVE", params={"destino": "cafe_palermo"}),
    ]


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
    return {aid: CyclicPolicy(aid) for aid in CYCLES.keys()}
