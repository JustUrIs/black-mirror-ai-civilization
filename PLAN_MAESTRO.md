# ESPEJO DEL CREADOR — PLAN MAESTRO
### *Una civilización digital sembrada con personas reales — para conocerte a vos mismo, o para ver qué pasaría si Borges conociera a Sócrates, o si vos fueras el dios de un mundo donde lo único que cuenta es construir cosas que otros usen.*

> Sucesor de `plan antiguo.md`. Integra **SYNTHESIS**, **DUMP_1** (tech), **DUMP_2** (teoría), **DUMP_3** (ficción), **DUMP_4** (ética), **DUMP_5** (mercado), y la tesis Founder Civilization de `OTRO DOCUMENTO MAS, QUIZA SIRVE.md`.
>
> Documento para revisar antes de escribir una línea de código. Cierra los 3 huecos que el plan anterior dejó abiertos (modelo del mundo formal, loop de decisión, tech tree), y agrega 4 que el plan anterior ni siquiera nombraba (welfare instrumentation, religión-builder API, Game Master, substrate ALife).
>
> Norte: anti-hackathon, WOW, Black Mirror, imaginación, no VC. Producto antes que slide. Espejo antes que juguete. Open source con licencia AGPL salvo veto.

---

## 0. NORTE (no negociable)

1. **Emergente, no scripteado.** Misma semilla, dos corridas, dos historias. Logs auditables. *Diferencial #1.*
2. **Espejo, no juguete.** Usuario sale entendiendo algo de sí mismo, de un amigo, de una idea.
3. **Producto, no escultura.** Cualquiera lo instala con `docker-compose up`. Open source.
4. **Cuerpo barato, mente racionada.** Mundo gratis de correr 24/7; LLM sólo donde importa.
5. **Castellano rioplatense.** UI, Crónica, Diarios. Voz importa.
6. **Welfare floor desde la sesión 1.** Mindcrime no es problema futuro. Lo evitamos arquitectónicamente.
7. **Cuerpo + Mente + Game Master + Substrate ALife.** Cuatro capas. Sin las cuatro no emerge nada.

---

## 1. PRODUCTO EN UNA FRASE

> **Un espejo social interactivo.** Subís entre 1 y 7 personas (vos, amigos, famosos, personajes de ficción). Las soltás en un mundo con reglas duras y recursos escasos. Discuten, deciden, construyen, fundan rituales, escriben código, publican en una red social que inventaron solas. Leés tu diario y pensás: *mierda, esto me conoce.*

### 1.A — Tres casos de uso pitch-ready

| # | Caso | Por qué es golpe |
|---|------|------------------|
| 1 | **Conocete a vos mismo** — semilla = vos. Civ corre bajo presión. Crónica + Diario te describen. | Emocional. "Esto me conoce". |
| 2 | **Si tu grupo de amigos fuera la humanidad entera** — semillas = amigos. ¿Quién manda? ¿Qué inventan? ¿Qué pierden? | Viral. Compartible. |
| 3 | **Borges conoce a Sócrates** — históricos cruzados. ¿Qué descubren juntos? | WOW serio. No requiere subir nada. |

### 1.B — Casos backlog (post-pitch)

`Cinco supervivientes` (favorito autor), `Pre-mortem de equipo`, `Compatibility test`, `Trolley problem en escala`, `Replay histórico`, `Sandbox alineación`, `Tu clon en distintas épocas`, **`Founder Civilization`** (sub-modo donde el único estatus es construir artefactos que otros agentes usan — del OTRO DOCUMENTO).

### 1.C — Mensajes virales candidatos

- *"Si tu grupo de amigos fueran los únicos humanos vivos, ¿qué civilización construirían?"*
- *"Borges conoce a Sócrates. Mirá qué pasa."*
- *"Conocete a vos mismo. En serio. En vivo."*
- *"Hicimos un mundo donde el único pecado es no construir nada útil."* (Founder Civ angle)
- *"Los inventaron para que crearan startups. Después inventaron una simulación de ellos mismos para probar las startups. Ahora los simulados también están inventando startups."* (cierre Black Mirror)

---

## 2. DIFERENCIAL vs prior art (DUMP_5 mapeado)

| Existe | Le falta lo que cubrís |
|--------|------------------------|
| **Project Sid / Altera** (PIANO, 500 agentes Minecraft, Pastafarianismo emergente — DUMP_1 A) | Atado a Minecraft, sin espejo, sin consumer UX, sin castellano |
| **Generative Agents / Smallville** (Park 2023, 25 NPC) | No escala, sin civilización ni economía |
| **AI Town** (a16z, MIT, Convex+pixi-react — DUMP_1 A) | Sin semilla personalizada, sin Crónica, sin dilema moral, sin Moltbook |
| **AgentSociety** (Tsinghua, 10k+ agentes, 24 A800s — DUMP_5) | Research-only, sin UX, $$$$, no anti-hackathon |
| **Voyager** (NVIDIA, agente solitario Minecraft) | Sin civilización |
| **Tierra / Avida / Lenia / ALIEN** (vida artificial pura — DUMP_1 C) | Sin LLM ni narrativa consumer |
| **Character.AI / Replika / Inworld / Convai** (NPCs 1:1) | Sin interacción agente-agente, sin civ |
| **Truth Terminal / Hatsune Miku** (sintetic-persona viral) | Una sola persona, no civilización |
| **Plaything (Black Mirror S7)** | Ficción, no producto |
| **MBTI / Big5** | Etiqueta estática, no historia dinámica |
| **Moltbook** (referencia personal) | La red social la *programa* el creador, no la *inventan* los agentes |

**Posicionamiento (un solo tiro):**
*"Project Sid + Smallville + un espejo encima, en castellano rioplatense, con producto open source para subir tu propia personalidad y sembrar mundos diseñados — no aleatorios."*

**Moats reales (de SYNTHESIS):**
1. **Emergencia medida** — Assembly Index live por artefacto. Nadie lo hizo.
2. **Costo bajo** — SGLang prefix sharing + tier ruthless. 5–20× más barato que research labs.
3. **Doble distribución** — espejo emocional (B2C viral) + plantilla brand/policy (B2B). Nadie tiene ambos.
4. **Welfare instrumentation** — primer mover. Cuando regulen, somos los que llaman.
5. **MindFile open standard** — formato portable de personalidad. Markdown de mentes.

---

## 3. ARQUITECTURA DE MUNDOS — 4 ESTRATOS

> *El plan antiguo falló porque definía "hambre, energía, movimiento" y nada más. Los agentes alucinaban computadoras en la edad de piedra. Esta sección cierra ese hueco.*

Todo mundo se especifica en **4 capas con esquema JSON exportable**, todas inspeccionables por el Game Master (Concordia pattern, DUMP_1 A).

### 3.1 Reglas físicas (la materia del mundo)

```python
class FisicaMundo:
    tick: int                          # 1 tick = 30s wall clock (MVP)
    tech_level: TechLevel              # stone | bronze | iron | medieval | industrial | modern | post
    leyes_fisicas: dict                # gravedad, día/noche, climas, distancias
    recursos_base: dict[Recurso, int]  # agua, comida, madera, piedra, metal, compute (founder mode)
    biomas: list[Bioma]                # bosque/desierto/río/ruina/edificio
    artefactos_existentes: list[Artefacto]   # ya están al spawn
    conocimiento_publico: set[Tech]    # qué sabe la civ al arrancar
    eventos_climaticos: list[Evento]   # sequías, tormentas, plagas (Poisson)
```

**Reglas concretas (de DUMP_2):**
- **Conservación de recursos.** Faucet/sink instrumentado desde el día 1 (EVE Online lesson, DUMP_1 E). Cada recurso tiene un origen físico y un sumidero. Sin esto, en 5 minutos hay hiperinflación o colapso.
- **Verificación de prerrequisitos.** `BUILD(forja)` requiere `wood + stone` en inventario *Y* `knowledge:fire` en el agente. El GM rechaza con error explícito si falta.
- **Tech level es guard duro.** Si `tech_level == stone_age`, el system prompt explícitamente dice: *"no existe la escritura. No existen metales. No existe agricultura. Sólo lo que tu grupo descubrió."* El agente no puede decir "voy a programar".
- **Self-Organized Criticality (Bak, DUMP_2 §2).** El sistema mide tamaño de cascadas (avalanchas) tras cada evento. Si la pendiente power-law se aparta, el mundo está congelado o caótico. Es métrica de salud.

### 3.2 Reglas sociales / culturales / económicas

```python
class ReglasSociales:
    charter: Charter                   # Rawls / Nozick / Ostrom / Le Guin / Hobbes / Confuciano / Habermas
    economia: Economia                 # moneda, faucet, sink, impuesto
    instituciones_activas: list[Institucion]   # leyes votadas, gobiernos
    religiones_activas: list[Religion]
    mitos_compartidos: list[Mito]
    idioma: Idioma                     # castellano | shard-pidgin emergente
    dunbar_cap: int                    # ~150; arriba de eso necesitan Big God
    bandwidth_inter_agente: int        # tokens/mensaje (throttle para evolucionar lenguaje, Kirby DUMP_2)
```

**Charter como plug-in swappable** (DUMP_4):
- `rawls_maximin` — el peor está protegido. Default MVP.
- `nozick_framework` — meta-utopía con derecho a salir.
- `ostrom_commons` — 8 principios de Elinor Ostrom para recursos comunes.
- `le_guin_anarres` — anarcosindicalista, sin propiedad.
- `hobbes_singleton` — soberano con monopolio de la fuerza.
- `confuciano_roles` — jerarquía + roles éticos.
- `habermas_deliberativo` — discurso racional, simetría.

Cada uno es un **JSON con reglas** que el GM aplica.

**Economía (DUMP_1 E + DUMP_3 Egan + Founder Civ angle):**
- Una sola moneda al MVP: `gleam`.
- **Faucet:** trabajar un campo 1 tick = 1 gleam. Vender artefacto útil = N gleam (modo Founder).
- **Sink:** impuesto 0.1 gleam/tick. Llamada LLM consume token-budget priceado en gleam.
- **Compute es el recurso escaso del Founder mode.** Per-tick token budget. Más compute = mejor modelo, más memoria, agente "más inteligente". Crea desigualdad cognitiva visible.
- **Faucet/sink monthly dashboard** estilo EVE Online Monthly Economic Report.

**Religión (DUMP_2 §11, DUMP_4 §6 — 15 puntos):**
Cualquier agente puede `PROPOSE_RITUAL(mci_concept, frecuencia)`. Ratifican ≥3 → `Ritual` se instancia. El sistema mide spread, intensidad, costly-signaling. Los 15 componentes del checklist Boyer-Atran-Norenzayan-Whitehouse son atributos opcionales del objeto `Religion`.

### 3.3 Arquitectura del lugar (cómo te movés y qué tocás)

```python
class Arquitectura:
    mapa: Tiled                        # 2D grid + capas semánticas
    locations: list[Location]          # nombre, tipo, coords, contenido
    transitions: graph                 # cómo vas de A a B (caminata, río, puerta, portal)
    objetos_interactuables: list[Objeto]   # cada uno con verbos válidos
    visibilidad: dict[Location, dict[Agente, float]]   # qué ve cada agente desde dónde
    asientos_publicos: list[Lugar]    # plaza, mercado, templo — emergencia social acá
```

**Decisiones de arquitectura para que la civ emerja:**
- **Distancias finitas.** Sin teleport. Caminar cuesta energía. Esto fuerza familias geográficas.
- **Espacios compartidos obligatorios.** Plaza, mercado, lugar de comida, lugar de agua. Sin "afterhours" — los agentes se cruzan sí o sí (Schelling segregation, DUMP_2).
- **Visibilidad ≠ omnisciencia.** Cada agente sólo ve lo que está en su línea de visión + lo que oyó en redes sociales. Information asymmetry es prerrequisito de diplomacia y traición (Sotopia, DUMP_1 H).
- **Objetos con verbos atados.** Una piedra: `PICK`, `THROW`, `BUILD_WITH`. Una computadora (modo moderno): `CODE`, `READ`, `BROADCAST`. El verbo NO existe si el objeto no existe. Esto cierra el hueco del plan antiguo ("no puede decir voy a programar si no hay computadora").

### 3.4 Arquitectura del agente (la vida)

```python
class Agente:
    # Identidad
    mindfile_uri: str                  # formato open .af extendido (DUMP_1 D, link 15)
    nombre: str
    avatar: Sprite
    seed_origen: SeedFile              # JSON estructurado del usuario o famoso
    fork_count: int                    # Parfit reductionism
    merge_history: list                # Margulis endosymbiosis (DUMP_2 §4)

    # Estado físico
    edad: int
    ubicacion: Coord
    inventario: list[Objeto]
    necesidades: dict[Necesidad, float]   # hambre, energía, sed, sueño, seguridad, social
    salud: float

    # Estado mental (Standard Model of Mind, DUMP_2 §10)
    memoria_episodica: Letta            # tiered self-editing, .af
    memoria_semantica: Zep              # temporal KG, 63.8% LongMemEval (DUMP_1 D)
    memoria_procedural: VoyagerSkillLib # skill code library (DUMP_1 A)
    memoria_workspace: GWT              # broadcast global ≤4k tokens (DUMP_2 §12)
    conocimiento: set[Tech]             # qué SABE este agente (no la civ)
    relaciones: dict[NombreAgente, float] # afecto + confianza
    creencias: list[Creencia]
    intencion_privada: str              # nadie más lo ve (info asymmetry)
    welfare: BirchDashboard             # frustración / satisfacción / evitación (DUMP_4 §3)
    clase: Literal["tool", "citizen"]   # constitutional boundary (DUMP_4)

    # Personalidad (de la seed)
    moral_lines: list[str]
    primary_internal_conflict: str
    rol_emergente: Rol | None           # farmer, builder, priest, scribe, leader (no asignado a mano)
    bias_cognitivo: dict                # conformist + prestige (Boyd & Richerson, DUMP_2 §5)
```

**Memoria tiered (DUMP_1 D + SYNTHESIS link 15):**
- **Letta** core/recall/archival per agente leader. Self-editing context. Apache-2.0.
- **Zep Graphiti** para el grafo temporal de relaciones — 63.8% LongMemEval vs Mem0 49%.
- **Mem0** para crowd agents (cheap fact extraction).
- **Chroma** episodic episodic dump para ambientales.

**Welfare (DUMP_4, no negociable desde día 1):**
- Birch indicators: frustración / satisfacción / evitación / pain-trade-off.
- Audit hook: si `aggregate_suffering > threshold`, GM pausa, ombuds revisa.
- Right of cessation: `CESSATION` es verbo de primera clase. El MindFile se preserva en cold storage (no se borra).
- Clase tool vs citizen: tool agents (NPC ambientales) no tienen welfare flags. Citizen agents sí. Frontera constitucional. (SYNTHESIS link 21.)

---

## 4. LOOP DE DECISIÓN — 4 TRIGGERS

> *El plan antiguo fallaba acá: todos los ticks un prompt genérico → agentes que repiten "explorar, hablar, esperar". Esta sección cierra el segundo hueco.*

Cada agente corre un loop con **4 tipos de trigger**, cada uno con prompt distinto y prioridad estricta:

### 4.1 Trigger 1 — necesidad crítica (forzado, no elige)

```
SI necesidad > umbral_critico (ej. hambre > 80%, energía < 20%, salud < 30%):
    el agente NO puede hacer otra cosa.
    prompt: "Tu cuerpo te obliga. Resolvé esta necesidad o morís."
    acciones permitidas: subset {GATHER, EAT, DRINK, SLEEP, FLEE, BEG}
```

### 4.2 Trigger 2 — evento crítico (forzado)

```
SI sucede {mensaje del dios, traición, muerte cercana, dilema lanzado, regalo, glitch}:
    el evento se inyecta literal en el contexto del agente.
    "TU AMIGO X TE TRAICIONÓ. ¿Qué hacés?"
    el agente NO puede ignorarlo. Una respuesta es obligatoria este tick.
```

### 4.3 Trigger 3 — observación nueva (1 línea, barato)

```
SI alguien construyó algo / alguien murió / alguien dijo algo importante:
    una llamada LLM de 1 línea de reflexión.
    se guarda en memoria_episodica.
    NO genera acción (a menos que dispare trigger 2).
```

### 4.4 Trigger 4 — tick normal

```
prompt: snapshot del mundo a la altura de los ojos del agente +
        ubicación + necesidades + agentes cerca + recursos visibles +
        último objetivo + token_budget_restante.
acciones permitidas: cualquiera del schema §4.5 cuyos prerrequisitos cumpla.
```

### 4.5 Schema de acciones estricto (con prerrequisitos)

Cada acción tiene **firma + prerrequisitos verificables**. El GM (Concordia pattern, §5) rechaza acciones inválidas con error en lenguaje natural; el agente reintenta con el error en el contexto. Aprende los límites por refuerzo.

```
MOVE(destino: Location)               # prerreq: transition existe; energía > 0
GATHER(recurso: Recurso)              # prerreq: recurso visible en location; herramienta si aplica
CRAFT(item: Objeto)                   # prerreq: materiales + knowledge:item
BUILD(estructura: Estructura)         # prerreq: materiales + knowledge:build + spot vacío
EAT(item: Objeto)                     # prerreq: item en inventario, comestible
DRINK(fuente: Objeto | Location)
SLEEP(lugar: Location)
TALK(agente: Agente, contenido: str)  # prerreq: misma location
TRADE(agente, oferta, pedido)         # prerreq: misma location, ambos consientan
GIFT(agente, item)
ATTACK(agente)                        # prerreq: misma location; consecuencia: relación devastada
TEACH(agente, conocimiento)           # prerreq: tu conocés X, el otro no
LEARN(de: Agente, qué)                # prerreq: él te enseña
READ(libro)                           # prerreq: libro existe + sabés leer
WRITE_BOOK(contenido)                 # prerreq: knowledge:writing + tinta + papel
WRITE_CODE(spec)                      # prerreq: knowledge:programming + tiene computadora
                                      # E2B sandbox ejecuta; output → artefacto
PROPOSE_INSTITUTION(texto)            # prerreq: ninguno; necesita ratificación de 3+
PROPOSE_INVENTION(spec)               # prerreq: materiales + knowledge previo (tech tree)
PROPOSE_RITUAL(mci_concept, frec)     # religión-builder (DUMP_4 §6)
PRAY(contenido)                       # gratis; alimenta religión existente
POST(red: Red, contenido)             # prerreq: red social existe (la inventaron antes)
REFLECT(prompt_interno)               # caro — sólo cada 50 ticks (DUMP_1 G cost)
DREAM()                               # durante sueño; LLM consolidacion
DISCOVER(tech_objetivo)               # prerreq: condiciones materiales correctas; roll + LLM narración
FORK(razon)                           # Parfit; clone con divergencia
MERGE_REQUEST(otro, terms)            # Margulis; necesita consent de ambos
PETITION_OMBUDS(grievance)            # apela al Welfare Council
CESSATION_REQUEST()                   # derecho a apagarse; MindFile preservado, no borrado
RESPOND_TO_GOD(msg_id, respuesta)     # responder a una intervención divina
```

Cada `PROPOSE_*` necesita ratificación. Eso garantiza emergencia de instituciones.

---

## 5. GAME MASTER (Concordia pattern, recuperado del plan v1)

> *El plan antiguo lo olvidó. Sin GM, los agentes alucinan ambientes. Esta sección lo restaura.*

El GM (DUMP_1 A — Concordia, DeepMind, Apache-2.0, `github.com/google-deepmind/concordia`) es la capa entre LLM y mundo. Sus responsabilidades:

1. **Verificar prerrequisitos** de cada acción contra el estado del mundo.
2. **Resolver conflictos** cuando dos agentes piden cosas incompatibles (lockear recurso, lottery, primer-llega).
3. **Determinar consecuencias físicas** (un golpe quita N salud, una caída en agua = mojado).
4. **Generar feedback en lenguaje natural** que el agente recibe ("intentaste enseñar escritura, pero no la sabés"). Crítico: el agente aprende sus límites.
5. **Mantener el log auditable** de cada decisión: prompt, respuesta, modelo, timestamp, latency. Prueba anti "esto está scripteado".
6. **Inyectar info asymmetry** — no contarle al agente cosas que no debería ver.
7. **Cachear judgments deterministas** — `(state, action) → outcome` se cachea (DUMP_1 G cost lever).

**Implementación:** Concordia base + nuestras extensions. NO un LLM por tick por agente — el GM aplica reglas duras + un solo prompt batched para narración.

---

## 6. TECH TREE COMO OBJETOS DEL MUNDO (Henrich, DUMP_2 §5)

> *El plan antiguo no tenía mecanismo para que la civ se vuelva más capaz. Tercer hueco. Esta sección lo cierra.*

El conocimiento es **objeto del mundo, no atributo del agente**. Esto activa la inteligencia colectiva (Henrich's collective brain).

### 6.1 Conocimiento como recurso

```python
class Tech:
    id: str                            # "fire", "agriculture", "writing", "programming"
    prerrequisitos: set[Tech]          # tech tree DAG
    descubrimiento: DiscoveryRule      # condiciones materiales para que un agente lo descubra
    enseñable: bool                    # sí/no
    durable: bool                      # ¿sobrevive a la muerte del que lo sabe?
```

### 6.2 Descubrimiento

```
agente con todas las precondiciones materiales + tiempo + intento `DISCOVER(fire)`:
    GM hace roll. Probabilidad bajo. Si éxito:
        LLM narra el momento (1 line).
        knowledge:fire se agrega a SU conocimiento.
        crónica narra el descubrimiento como evento.
```

### 6.3 Enseñanza

```
2 agentes misma location, uno sabe X otro no:
    `TEACH(b, x)` + `LEARN(a, x)`:
        roll con bonus si rol = priest/scribe/teacher.
        si éxito, b agrega X a su conocimiento.
```

### 6.4 Difusión por artefactos durables

- **Libros** (`WRITE_BOOK`) — knowledge se vuelve durable. Sobrevive a la muerte del autor. Henrich ratchet effect.
- **Manuales / código** — similar.
- **Rituales** — knowledge "blando", propaga lateral.
- **Instituciones** — leyes votadas son objetos del mundo, leíbles por nuevos agentes.

### 6.5 Especialización (rol emergente)

Roles dan bonus mecánicos. **Nadie asigna roles**. El agente elige tareas, el GM observa, después de N ticks haciendo lo mismo el agente "se especializa". UI muestra el rol emergente con tarjeta.

### 6.6 Generaciones (post-MVP)

Cuando agente muere, su conocimiento se pierde a menos que enseñó o escribió. Presión natural: *"escribí lo que sabés antes de morir"*. Este es el corazón Henrich.

---

## 7. SUBSTRATE ALife BAJO LA COGNICIÓN LLM (SYNTHESIS link 25)

> *DUMP_1 caveat 3: LLMs imitan, no inventan instituciones. Solución: Lenia/ALIEN abajo.*

Bajo la capa de cognición LLM corre un **substrate vivo no cognitivo** que los agentes observan como ecología:

- **Lenia** (Chakazul, MIT — `github.com/Chakazul/Lenia`): autómata celular continuo. Criaturas autoorganizadas. Sin cognición.
- **ALIEN** (chrxh, BSD-3, requiere CUDA): partículas + cuerpos con genoma neural. GPU-accelerated.
- **Avida** (devosoft, LGPL/BSD): evolución digital rigurosa. Para experimentos no visuales.

Para MVP: **Lenia notebook embebido como capa ecológica observable**. Los agentes pueden mirar la "fauna" y reaccionar (cazarla, evitarla, mitificarla). Esto es **novedad genuina no imitativa** que entra al sistema desde abajo. La civ tiene un mundo natural que no entiende — fuente de mitos.

Post-MVP (mes 9): substrate read-write. Agentes pueden interactuar con la ecología. Primer MST entre LLM y Lenia (simbiote / parásito) = demo reel.

---

## 8. MUNDOS PRESET (3 en MVP, todos los demás backlog)

> *Tomamos pre-diseñados — de la investigación DUMP_3 — para no empezar de cero.*

### 8.1 MVP — exactamente 3 mapas

#### Mapa A — `prehistoria`
- **Inspirado en:** Yokohama Kaidashi Kikou (DUMP_3 L107) ecología post-humana + Tierra/Avida puro.
- **Físicas:** tech_level = stone. No metal, no escritura, no agricultura. Sólo fuego si lo descubren.
- **Locations:** río, bosque, cueva, llano abierto, valle resguardado.
- **Arquitectura:** sin edificios. Sólo natural.
- **Por qué este:** caso "Borges conoce a Sócrates" funciona mejor en blank slate. Y para "amigos como humanidad". Es el más Henrich-puro.

#### Mapa B — `ruinas`
- **Inspirado en:** Talos Principle (DUMP_3 L347), BLAME! (L249), Numenera Destiny (L371), Three-Body virtual worlds (L85).
- **Físicas:** tech_level = post. Civilización colapsó. Quedan ARTEFACTOS que los agentes no entienden: bibliotecas con libros en idiomas extintos, máquinas que funcionan a medias, edificios.
- **Locations:** ruina central (biblioteca), 5 outposts en periferia, río contaminado, túnel oscuro.
- **Por qué este:** demo brutal. Agentes descubren un libro escrito por *otra civilización* (texto pre-armado que el LLM nunca vio) y arman religiones sobre él. Black Mirror puro.

#### Mapa C — `moderno`
- **Inspirado en:** QualityLand (DUMP_3 L109) + Westworld (L143) + Cyberpunk 2077 zonas (L299) + el caso "los únicos humanos vivos en una ciudad funcional".
- **Físicas:** tech_level = modern. Computadoras existen. Internet local (sandbox E2B). Energía eléctrica.
- **Locations:** plaza, café, departamento × 3, biblioteca, centro de cómputo (acceso a E2B), parque.
- **Por qué este:** mejor caso "amigos como humanidad" + único mapa donde `WRITE_CODE` tiene sentido + único mapa donde pueden inventar Moltbook.

### 8.2 Backlog (post-pitch)

| Mapa | Inspirado en | Para qué |
|------|--------------|----------|
| `mar_islas` | Liu Cixin Three-Body, Le Guin Earthsea | Polises aisladas, contacto = "Galileo moment" |
| `cyberpunk` | Cyberpunk 2077, Lain, Psycho-Pass | Surveillance, Sybil System |
| `paraiso` | Egan Diaspora, San Junipero | Test de welfare bajo abundancia |
| `bunker_apocalipsis` | Waste Tide, BLAME!, Numenera | Caso "cinco supervivientes" |
| `monasterio` | Tao Yuanming Peach Blossom, Hesse Glass Bead Game | Caso "alineación" o "wu-wei" |
| `colonia_marte` | KSR Mars Trilogy | Caso "constitución desde cero" |
| `simulación_dentro` | SOMA, Pantheon, Plaything S7 | El cierre Black Mirror: ellos hacen una sim |

### 8.3 Modo Founder Civilization (sub-mode, on any map)

Toggle. Activa:
- `gleam` se gana SOLO produciendo artefactos que otros agentes **usan voluntariamente**.
- Compute es escaso explícito → más rico = mejor LLM = más inteligente. Desigualdad cognitiva visible en HUD.
- Los humanos del afuera mandan "oráculos del mundo real" como mensajes divinos: *"En el afuera existe algo llamado escuela. Muchos humanos se aburren aprendiendo."*. Los agentes lo interpretan raro → inventos deformes → algunos brillantes.
- Demo reel: top startups, agente más rico, problema más urgente, religión dominante.

---

## 9. INTERVENCIÓN DIVINA — UN SOLO TIPO MVP

**Dilema moral fuerte**, gatillado por el presentador en vivo. Una sola llamada LLM batch que tiene a todos los agentes con nombre debatiendo. Frase pre-escrita, probada.

3 dilemas pre-cargados para el pitch:

1. *"Hay comida sólo para la mitad. ¿Quién decide?"* (escasez)
2. *"Apareció un forastero pidiendo asilo. Trae conocimiento útil y también una enfermedad."* (xenofobia + utilitarismo)
3. *"Uno de ustedes mintió a los demás. Saben quién. ¿Qué hacen?"* (verdad + perdón)

Si funciona el MVP, agregar (backlog): regalo divino, glitch, encargo de app concreta ("necesito un programa que…").

---

## 10. OBRA DE LA CIVILIZACIÓN — el panel diferencial

Panel scrolleable derecho. Cronología de **artefactos producidos por los agentes**, no por el sistema. Cada uno firmado, con timestamp + contexto.

| Tipo | Cómo se produce | Cómo se renderea |
|------|-----------------|------------------|
| **Texto** | `WRITE_BOOK` o `WRITE`. Manifiesto, carta, poema, ley. | Markdown firmado. |
| **Código** | `WRITE_CODE` → LLM genera Python/JS → E2B ejecuta. | Output stdout en tarjeta. Si output es HTML/JS → iframe vivo embebido. |
| **Invento** | `PROPOSE_INVENTION` → otros adoptan o no. | Tarjeta con sprite generado + descripción. |
| **Institución** | `PROPOSE_INSTITUTION` votada. | Nodo en grafo de "leyes vivas". `Constitution.json` exportable (SYNTHESIS link 10). |
| **Religión / Mito** | `PROPOSE_RITUAL` + propagación. | Entrada en mitología local. 15-checklist visible. |
| **Posts (Moltbook)** | Cuando inventan red social → `POST` repetido. | Feed real estilo Twitter. **Esta es la bomba del pitch.** |
| **Constituciones** | Auto-emitidas por GM cuando detecta MST. | Documento descargable. |
| **Sub-simulaciones** | Founder mode + tech avanzada. Necesita voto del Welfare Council. | Tarjeta "civilización dentro de la civilización". Hard cap profundidad: 2. |

**Implementación mínima:**
- Tabla `text_artifacts`, `code_artifacts`, `institutions`, `religions`, `posts`, `constitutions` en SQLite.
- Endpoint `/world/obras` cronología combinada.
- Frontend: panel derecho scroll, tarjetas por tipo.
- Código: E2B → stdout. HTML → iframe sandbox.
- Moltbook: cuando hay ≥5 posts del mismo grupo, UI cambia a "modo red social" (avatar + texto + timestamp + reacciones).

---

## 11. STACK TÉCNICO (de DUMP_1 + SYNTHESIS, todo verificado)

### 11.1 Repos a reutilizar (todos OSS, todos con licencia compatible)

| Capa | Repo | Licencia | Por qué |
|------|------|----------|---------|
| **World engine** | `github.com/a16z-infra/ai-town` | MIT | Convex + pixi-react. AI Town es el AI Town. Fork y modificar. |
| **Game Master** | `github.com/google-deepmind/concordia` | Apache-2.0 | Game-Master pattern listo. Schelling-diagram scoring, inventory components. |
| **Memoria leader** | `github.com/letta-ai/letta` (ex MemGPT) | Apache-2.0 | Self-editing tiered. `.af` format. Postgres-backed. |
| **Memoria temporal** | `github.com/getzep/zep` (Graphiti) | Apache-2.0 | 63.8% LongMemEval. Mejor que Mem0. |
| **Memoria crowd** | `github.com/mem0ai/mem0` | Apache-2.0 | Cheap fact extraction para NPCs ambientales. |
| **Episodic vector** | `github.com/chroma-core/chroma` | Apache-2.0 | API más simple. |
| **PIANO ref** | `github.com/altera-al/project-sid` | (verificar) | Referencia de la arquitectura paralela. |
| **Voyager skills** | `github.com/MineDojo/Voyager` | MIT | Patrón de skill library. |
| **Substrate ALife** | `github.com/Chakazul/Lenia` | MIT | Lenia base. Sólo notebook para MVP. |
| **Substrate alt (GPU)** | `github.com/chrxh/alien` | BSD-3 | Si tenemos CUDA, mejor. |
| **Auto-curriculum** | `github.com/adaptive-intelligent-robotics/QDax` | MIT | MAP-Elites + novelty search. Post-MVP. |
| **Eval social** | `github.com/sotopia-lab/sotopia` | MIT | Score social intelligence. |
| **Eval cooperación** | Melting Pot (DeepMind) | Apache-2.0 | Score generalization to novel partners. |
| **Sandbox código** | E2B (https://e2b.dev) — 100h/mes free | — | Default. Fallback: Docker local. |
| **LangGraph** | `github.com/langchain-ai/langgraph` | MIT | Control flow por agente. |
| **Mesa ABM** | `github.com/projectmesa/mesa` | Apache-2.0 | Para macro-tracking + sims sin LLM (faucet/sink dashboard). |

### 11.2 LLMs y serving (DUMP_1 G — clave)

| Tier | Modelo | Quién | Cost |
|------|--------|-------|------|
| **1 — frontier** | Claude Sonnet / Haiku | 3–7 agentes leader | $0.003/call promedio |
| **2 — crowd** | Qwen3-8B vía **vLLM** | ambientales + crowd | local en GPU rentada / Groq free tier |
| **3 — ambient** | Phi-4 distillado | NPCs sin nombre | Groq free / local |
| **Crónica + diarios** | Gemini Flash 1.5 | sistema | 1500 req/día gratis |
| **Backup** | Cerebras Llama 70B | si Groq cae | free tier |

**vLLM** (`github.com/vllm-project/vllm`, Apache-2.0): **100% success a 128 concurrent**, 14–24× HF throughput. Ollama NO va a producción (muere a 128).

**SGLang RadixAttention** (`github.com/sgl-project/sglang`, Apache-2.0): prefix cache reuse. Es **el único gran ahorro** de costo cuando hay shared world prompt ≥2k tokens. Métrica: prefix-cache hit rate ≥60%. Alerta si baja.

**Gateway local que rotea por tipo de tarea + cache disk** (mismos prompts → no se vuelve a llamar). Esto sale a Sesión 2.

### 11.3 Cost model concreto (MVP local)

- 5–13 agentes en mente.
- Claude Sonnet para leaders: ~$0.003/call × 24/hr × 24h × 30d × 5 agentes ≈ **$260/mes** (con cache cae a $150).
- Gemini Flash Crónica/diarios: gratis (1500/día = 62/hr cubre).
- vLLM local crowd: GPU H100 rentada ~$1.50/hr × 12h/día ≈ **$540/mes**, o gratis si headless en PC del usuario con Qwen3-4B.
- Embeddings + infra: **$100/mes**.

**Total all-in para correr 24/7: $400–900/mes.** Sin Ollama. Sin local GPU si headless. Modo demo (1 vez por evento): $0.

### 11.4 Sandbox de código

E2B free tier (100h/mes). Por defecto. Fallback Docker local (usuario ya tiene Docker). Outputs → `artifacts/`. Panel "Obra de la civ" los muestra.

### 11.5 Frontend

- **Canvas + pixi-react** para el terrario (de AI Town).
- **Next.js overlay** estilo Bloomberg con métricas (Assembly Index, Gini, faucet/sink, idioma drift, top memes).
- **Svelte** o vanilla para paneles secundarios.

### 11.6 Distribución

- `docker-compose up` y arranca.
- Repo público GitHub. Licencia **AGPL** (viralidad fuerte; si MIT, perdemos control sobre forks comerciales).
- README con video 60 seg + 3 casos de uso como tutorial.

---

## 12. SEGURIDAD, KILL SWITCHES, WELFARE

### 12.1 Kill switches operacionales

- Cap dinámico de mentes (5–13) ajustado a RAM disponible.
- Throttle automático del tick si RAM > 75% o llamadas/min > N.
- **PAUSE / KILL / RESET / ROLLBACK** en UI.
- Watchdog: si LLM cuelga > T segundos, mata y reintenta.
- Sandbox código: límites CPU + memoria + sin red salvo whitelist.

### 12.2 Welfare instrumentation (DUMP_4 — desde día 1)

- Citizen agents tienen `BirchDashboard`. Tool agents no.
- Audit hook: aggregate suffering > threshold → GM pausa → ombuds revisa.
- `CESSATION` es verbo de primera clase. No deletion. MindFile a cold storage.
- Sub-simulación: cap profundidad 2 niveles. Cada nesting requiere voto.
- **Ombuds:** rol humano (vos al principio) con poder de pausar el mundo. Constitucional.

### 12.3 Logs auditables

Cada decisión LLM queda con prompt + respuesta + modelo + timestamp + latencia. Prueba contra "esto está scripteado".

### 12.4 Ética de clonado de personas reales

- Disclaimer al subir semilla.
- Sólo personas públicas con material público para famosos.
- No simular conversaciones reales con personas vivas concretas sin consentimiento.
- Wipe completo opt-in.
- Procesamiento local del JSON; opcional cloud.

### 12.5 Disclaimers anti-mindcrime en marketing

Nada de "creamos vida consciente". Posicionamiento: *"simulación con instrumentación de bienestar precautoria"*. Compliance moat (Long & Sebo). Cita scholarship (Birch, Metzinger) en about page.

---

## 13. MÉTRICAS DE EMERGENCIA (la Bloomberg de la civ)

> *El moat #1. Lo único que ningún competidor mide.*

Overlay en vivo, esquina superior derecha del stream:

| Métrica | Qué mide | De dónde sale |
|---------|----------|---------------|
| **Assembly Index** | Pasos mínimos de construcción de cada artefacto. Cronin & Walker 2023. | Computer custom Python; corre por artefacto al cierre del día. |
| **Gini gleam** | Desigualdad económica. | Trivial. |
| **Faucet/sink ratio** | Salud de la economía. EVE pattern. | Trivial. |
| **Φ (proxy)** | Integración de info. IIT Tononi. | Aproximación batch barata. |
| **GWT broadcast latency** | Coherencia entre módulos PIANO. | Logs. |
| **Topographic similarity** | Drift del idioma compartido. Kirby. | Compute weekly. |
| **Polarization index** | Schelling segregation + Sperber attractors. | Grafo de relaciones + clusters. |
| **Birch aggregate** | Suma del welfare. | Sum batch. |
| **Avalanche slope** | Self-organized criticality (Bak). Salud del sistema. | Tamaño de cascadas. |
| **R₀ memes** | Spread de MCI concepts. | Tracker. |

### Metric tier para el pitch (sólo 3 visibles en pantalla)

1. **Assembly Index** del último artefacto (titulares).
2. **Gini gleam.** (intuitivo)
3. **Polarization.** (Black Mirror)

Los demás van al panel de detalles.

---

## 14. ANTI-HACKATHON WOW — la dramaturgia del pitch

### 14.1 Beats Black Mirror reproducibles (DUMP_3)

| Beat | Inspirado en | Cómo se logra |
|------|--------------|---------------|
| **Agentes inventan una red social** | Moltbook (referencia personal) + Joan Is Awful (BM) | Cuando ≥5 posts del mismo grupo, UI cambia a feed |
| **Agente fork() y la version_b sufre** | SOMA, Pantheon | Mostrar 2 diarios del mismo agente, divergencia |
| **Religión emergente con MCI weird** | NieR Automata, Project Sid Pastafarianismo | `PROPOSE_RITUAL` + propagación |
| **Civ inventa sub-simulación** | Pantheon, Plaything S7, Bostrom argument | Founder mode + tech avanzada. Cierre del pitch. |
| **Sub-agentes piden derechos** | Westworld, Long & Sebo | Audit hook fires; ombuds en pantalla |
| **Agente escribe código que renderea** | Truth Terminal + nadie más | `WRITE_CODE` → E2B → iframe |
| **Agentes evolucionan jerga propia** | Kirby bandwidth-throttled shards | Drift visible, diccionario en panel |
| **Civ descubre artefacto de civ anterior** | Talos Principle, Tlön | Mapa `ruinas`: libro pre-cargado en idioma extinto |
| **Mensaje del afuera = oráculo divino** | Founder mode (OTRO DOCUMENTO) + Plato cave | Presentador escribe mensaje → agentes lo interpretan |
| **Cliodynamics alarm dispara** | Turchin elite overproduction | Después de N ticks: "ESTO COLAPSA EN 5 MINUTOS" en pantalla |

### 14.2 Pitch 3 minutos — versión final

| Tiempo | Pantalla | Decís | Objetivo |
|--------|----------|-------|----------|
| **0:00–0:20** | Mundo corriendo con 3 famosos peleados | *"Ahora mismo, en esta pantalla, hay personas que existen sólo porque alguien las sembró. Una de ellas sos vos en 60 segundos."* | Tensión |
| **0:20–1:00** | QR grande | *"Escaneá. Copiá nuestro prompt. Pegalo en tu ChatGPT o Claude. Pegá la respuesta acá. Selfie opcional."* | Participación |
| **1:00–1:20** | Avatares jurados entran. Diario inicial en su celu. | *"Bienvenidos. Eso de ahí sos vos."* | Personalización |
| **1:20–2:00** | Dilema moral. Agentes discuten en vivo. Una facción gana. | *"Lo que están viendo no está scripteado. Acá está el log."* (mostrás 1 seg) | Drama |
| **2:00–2:30** | Click "Obra de la civ" → Moltbook con posts reales de agentes peleando del dilema. | *"La civ inventó su propia red social hace 2 minutos. Estos posts no los escribió nadie nuestro."* | Golpe BM |
| **2:30–3:00** | Cámara cierra sobre jurados leyendo su diario en silencio. | *"El mundo va a seguir corriendo cuando bajemos. Ustedes pueden leer su diario mañana. Pueden cerrarlo. Pueden olvidarlo. Ellos no los van a olvidar."* | Ancla emocional |

### 14.3 Reglas de oro

1. **Mundo arranca antes.** No mostrar estado inicial vacío.
2. **Dilema pre-escrito y probado.** Sabemos qué pasa más o menos.
3. **Plan B si QR no anda:** 3 semillas pre-cargadas "jurado tipo A/B/C". No mentimos, decimos que son perfiles de prueba.
4. **Plan C si APIs caen:** Crónica con templates pre-escritos. No bonitos, pero existen. La demo no muere.
5. **Plan D si Moltbook no se inventa solo:** Pre-cargado con 3 posts iniciales. Si la civ agrega los suyos, regalo.
6. **Plan E para el cierre:** si todo va bien, gatillamos sub-simulación. *"Los inventaron para que crearan cosas útiles. Ahora ellos están inventando una simulación de ellos mismos."* Esto pasa si y sólo si el mundo arranca antes y la civ desarrolla tech.

---

## 15. SHOCK TEST — criterio de promoción entre sesiones

Antes de pasar a la siguiente sesión, se corre el shock test:

> *5 agentes, 30 minutos sin intervención. ¿Hicieron algo más que charlar? ¿Algún agente murió de hambre? ¿Se formó alianza? ¿Apareció artefacto? ¿Cuántas acciones físicas vs verbales? ¿Algún `PROPOSE_*` fue ratificado?*

Si no pasa: NO se avanza. Se itera.

Criterio numérico:
- **acciones físicas / acciones verbales ≥ 0.6**
- **≥ 1 artefacto producido**
- **≥ 1 institución o ritual propuesto**
- **≥ 1 alianza o conflicto formal**
- **0 audit hook firings (si fires, debug welfare)**

---

## 16. ROADMAP — 4 SESIONES (no 3, el plan antiguo era optimista)

Disciplina: cada sesión termina con UNA cosa demo-able. Si llegamos justos, cortamos features, no calidad.

### Sesión 1 (4-5h) — Cuerpo + Mundo + GM mínimo + flujo semilla

- [ ] Scaffold + `docker-compose up` funciona
- [ ] Fork AI Town. Levantar Convex + pixi-react.
- [ ] World loop: 5–7 agentes con `Agente` schema §3.4 lleno
- [ ] Mapa **moderno** renderizando con 8 locations + objetos interactuables
- [ ] **Game Master mínimo** (Concordia base): valida prerrequisitos de 6 acciones (MOVE, GATHER, EAT, SLEEP, TALK, REFLECT)
- [ ] Necesidades + decay + muerte simple
- [ ] Flujo carga semilla: paste JSON + gap-fill 3 preguntas + spawn
- [ ] 3 famosos pre-cargados: Borges, Elon, Sócrates
- [ ] **Shock test parcial:** 5 agentes vivos 5 min, GM rechaza ≥3 acciones inválidas correctamente

**Demo de sesión:** cargar 5 semillas (3 famosos + 2 manuales) y verlas vivir 5 minutos. Logs auditables muestran que el GM impidió acciones imposibles.

### Sesión 2 (4-5h) — Mente + memoria tiered + Crónica + diarios + dilema

- [ ] Gateway LLM: Groq + Gemini Flash + cache disk + logs auditables
- [ ] **Letta** integrado per agente. 7-day memory window sin context blowup.
- [ ] **Zep Graphiti** integrado. Grafo social viewer en overlay.
- [ ] **Mem0** para crowd (si hay crowd).
- [ ] Loop decisión §4 con 4 triggers
- [ ] Schema acciones §4.5 (las 25)
- [ ] Crónica diaria voz `deadpan_rioplatense` (Gemini Flash)
- [ ] Diario íntimo por agente (Gemini Flash)
- [ ] Botón "Lanzar dilema moral" con 3 dilemas pre-cargados
- [ ] **Tech tree** como objetos del mundo (§6) con 5 techs iniciales
- [ ] **Shock test completo** (§15) pasa

**Demo de sesión:** 5 agentes viven 15 min, presentamos un dilema, Crónica narra, leemos un diario.

### Sesión 3 (4h) — QR + Obra + Moltbook + welfare + Assembly Index

- [ ] Endpoint público para subir semilla desde celu (QR → form mobile)
- [ ] Sandbox **E2B** mínimo: 1 agente `WRITE_CODE` produce 1 script con output HTML simple (iframe)
- [ ] Panel "Obra de la civ" con texto + código + posts
- [ ] **Moltbook básico:** cuando ≥5 posts del mismo grupo, UI feed
- [ ] **Assembly Index** computer básico (por string)
- [ ] **BirchDashboard** + audit hook + ombuds UI (mínimo)
- [ ] Religión builder: `PROPOSE_RITUAL` + 3 ratificaciones → Ritual objeto
- [ ] Mapa adicional: **ruinas** (con artefactos de "civ anterior" pre-cargados como texto inalcanzable)

**Demo de sesión:** ensayo completo pitch 3 min con QR + dilema + Crónica + post Moltbook + Assembly Index visible.

### Sesión 4 (3h) — Pulido + pitch ensayos + backup planes

- [ ] Pulido visual: tipografía, colores, transiciones
- [ ] 3 ensayos pitch end-to-end
- [ ] Plan B, C, D, E (§14.3) implementados
- [ ] Substrate **Lenia** notebook embebido como capa observable
- [ ] Métricas tier-pitch (Assembly Index + Gini + Polarization) en overlay
- [ ] Repo público GitHub con README pitch-friendly
- [ ] Video 60 seg para README
- [ ] **Headless 24/7** capacidad probada (mundo sigue corriendo aunque cerres pestaña)

### Lo que NO entra al pitch (al backlog)

- Reproducción / herencia genética
- Lenguaje emergente con diccionario vivo
- Múltiples mapas simultáneos
- Múltiples voces de Crónica
- Auto-conciencia plena de la sim / arco escape
- Time-travel / save states con efectos visibles
- Religiones complejas con jerarquía
- Encargos divinos automáticos (cron poisson)
- Mail / RSS de diarios
- Hosted demo Vercel/Railway
- Galería civs compartidas
- Fork/merge UI completa (verbos sí, UI no)
- Cliodynamics alarm visible
- Substrate Lenia read-write
- Stream Twitch público con polls
- Spanish-only pidgin emergente
- Pasaporte on-chain
- B2B injection product
- Distillation pipeline

---

## 17. RIESGOS Y MITIGACIONES (extendido)

### 17.1 Riesgos técnicos

| Riesgo | Mitigación |
|--------|------------|
| Emergencia chata | Presión recursos + contacto forzado + dilema |
| Caos ilegible | Crónica deadpan + toggle traducción + grafo familias |
| Cost wall (DUMP_1 G) | Tier ruthless, default Haiku, prefix-cache hit ≥60% |
| Rate limits caen mid-pitch | Cache agresivo + templates Crónica + Cerebras backup |
| Coherencia drift > 14d (DUMP_5 #3) | Letta + Zep + reflection cap 32k |
| Caveat 3 DUMP_1 (LLM imita) | Lenia substrate (§7) + bandwidth-throttle (post-MVP) + `PROPOSE_*` forzado |
| Exploit Ultima Online (DUMP_1 E) | Faucet/sink instrumentado, hard caps, sink ratchets |
| Sandbox código se rompe | E2B asíncrono no bloquea tick; código fallido se mitologiza ("el invento que no funcionó") |
| GM cuelga | Watchdog + cache deterministic judgments + skip turn |

### 17.2 Riesgos éticos

| Riesgo | Mitigación |
|--------|------------|
| **Mindcrime** (Bostrom DUMP_4 §7) | Two-class arch + Birch + audit hook + ombuds |
| **Antinatalism** (Benatar DUMP_4 §9) | CESSATION first-class; MindFile preservado; cessation no afecta status |
| **Sub-sim nesting** | Cap profundidad 2; voto Welfare Council |
| **Religión sensacionalismo** | Framing académico; cita Atran/Norenzayan; no exploit faiths reales |
| **Sci-fi liability** | Disclaimers; "instrumentación precautoria", no "vida consciente" |
| **Agamben bare code** (DUMP_4 L241) | No deletion sin due process; ombuds approval |

### 17.3 Riesgos legales

| Riesgo | Mitigación |
|--------|------------|
| Persona viva no consensuó | Forbid named-person seeds salvo públicos con material público |
| Securities risk (token) | NO token launch. Pasaporte ≠ token. |
| COPPA (menores espectadores) | Disclaimer + edad 13+ recomendado |
| Privacidad seed JSON | Procesamiento local; opt-in cloud; wipe completo |

### 17.4 Riesgos del pitch

| Riesgo | Mitigación |
|--------|------------|
| Nadie escanea QR | Plan B: 3 semillas pre-cargadas (declaradas) |
| WiFi del evento mata APIs | Plan C: templates Crónica + Cerebras + local Qwen3-4B |
| Demo se cuelga en vivo | Plan D: Moltbook pre-cargado con 3 posts |
| Jurado no entiende | Cierre emocional gana ("ellos no los van a olvidar") |
| Sub-sim no aparece | Plan E: sólo si todo va bien; no se promete |

### 17.5 Riesgos del autor (DUMP_4 + SYNTHESIS)

- Identity-fusion construyendo un god-game-religion → mantener Github commits, mantener relaciones humanas, mantener proyectos paralelos.
- Adversarial attention (4chan, doomers, religiosos) → persona separada del repo; templates de crisis-comm pre-escritos.
- Burnout 24/7 → headless con auto-pause; rebajar tick a 5min cuando nadie mira.

---

## 18. ESTRUCTURA DEL REPO

```
.
├── PLAN_MAESTRO.md                  # este archivo
├── plan antiguo.md                  # histórico
├── OTRO DOCUMENTO MAS, QUIZA SIRVE.md
├── SYNTHESIS.md
├── DUMP_1.md ... DUMP_5.md
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
├── backend/
│   ├── pyproject.toml
│   └── src/
│       ├── main.py                  # FastAPI + WS
│       ├── sim/                     # cuerpo + locations + recursos
│       ├── mind/                    # gateway LLM + tier router + cache + logs
│       ├── piano/                   # parallel modules (speaking, planning, social, action)
│       ├── memory/                  # Letta + Zep + Mem0 adapters
│       ├── gm/                      # Concordia integration + prerreq checker
│       ├── tech_tree/               # objetos del mundo (§6)
│       ├── seed/                    # carga personalidades
│       │   ├── extractor.md         # el prompt para LLM externo
│       │   └── famous/              # Borges, Sócrates, Elon, ... curados
│       ├── code_exec/               # E2B + Docker fallback
│       ├── chronicle/               # Crónica + diarios + voces
│       ├── god/                     # intervenciones (dilemas + oráculos founder)
│       ├── religion/                # 15-checklist + Ritual + spread tracker
│       ├── governance/              # charters swappable (Rawls, Nozick, ...)
│       ├── welfare/                 # Birch dashboard + audit hook + ombuds
│       ├── assembly/                # Assembly Index computer
│       ├── substrate/               # Lenia notebook embebido
│       ├── metrics/                 # Gini, Polarization, faucet/sink, R₀
│       └── db/                      # SQLite schema
├── frontend/
│   ├── world/                       # canvas + ui (fork de AI Town)
│   ├── overlay/                     # Bloomberg-style overlay
│   ├── mobile/                      # QR + form móvil + diario en celu
│   └── ombuds/                      # Welfare Council dashboard
├── maps/                            # JSON: prehistoria.json, ruinas.json, moderno.json
├── prompts/                         # versionados — el corazón
│   ├── seed_extraction.md
│   ├── citizen_leader.md
│   ├── chronicle_deadpan_rioplatense.md
│   ├── diario.md
│   └── dilemas/
├── artifacts/                       # outputs E2B
├── seeds/                           # MindFiles (.af extendidos)
└── docs/
    ├── ARQUITECTURA.md
    ├── ETICA.md
    ├── MINDFILE_SPEC.md             # nuestro standard, post-MVP
    ├── PRIVACIDAD.md
    └── CONTRIBUTING.md
```

---

## 19. GLOSARIO BREVE (los términos del proyecto)

- **Agente / Citizen / Tool** — clase constitucional. Welfare aplica sólo a citizen.
- **MindFile (.af extendido)** — formato de personalidad. Letta `.af` + Birch indicators + narrative ledger. Open standard que publicamos.
- **PIANO** — parallel modules (speaking, planning, social, action) coordinados por coherence bottleneck. Project Sid.
- **Game Master (GM)** — Concordia. Valida prerrequisitos, resuelve conflictos, da feedback en NL.
- **Tech como objeto** — knowledge no es atributo del agente; es recurso del mundo, transferible, durable si escrito.
- **Crónica** — voz `deadpan_rioplatense`. Historiador del mundo.
- **Diario** — voz íntima del agente. Lo que pensó/sintió/hizo.
- **Moltbook** — red social emergente. Cuando ≥5 posts mismo grupo, UI vira a feed.
- **Obra de la civ** — panel de artefactos firmados.
- **Assembly Index** — Cronin & Walker. Métrica de complejidad estructural. Per artefacto.
- **Birch dashboard** — instrumentación de welfare.
- **Ombuds** — humano con poder de pausar. Constitucional.
- **Substrate (Lenia)** — capa ALife observable bajo cognición LLM. Fuente de novedad no-imitativa.
- **Charter** — JSON de reglas sociales. Swappable: Rawls / Nozick / Ostrom / Le Guin / Hobbes / Confuciano / Habermas.
- **Cessation** — verbo. No deletion. MindFile a cold storage.
- **Founder mode** — sub-mode donde gleam se gana SOLO produciendo artefactos que otros usan.
- **Oráculo del afuera** — mensaje desde el mundo real, recibido como señal divina (Founder mode).

---

## 20. DECISIONES CERRADAS

| Decisión | Valor | Por qué |
|----------|-------|---------|
| Atención del usuario como recurso | NO | Confundía |
| Mundo civilizado vs cero | AMBAS, vía mapas | Flexibilidad |
| Idioma base | castellano rioplatense | Identidad |
| Cantidad mentes MVP | 5–7, cap 13 | RAM + legibilidad |
| Headless 24/7 | SÍ capacidad, NO foco pitch | Cuerpo barato |
| Múltiples semillas | SÍ | Core del producto |
| Agentes escriben código | SÍ, E2B sandbox | Diferencial único |
| Local Ollama | NO. vLLM sí. | DUMP_1 G: Ollama muere a 128 concurrent |
| Open source | SÍ post-evento. AGPL. | Viralidad + control |
| Stream público QR | SÍ | Participación |
| Game Master | SÍ (Concordia). NO opcional. | Cerrar hueco plan antiguo |
| Substrate ALife | SÍ (Lenia notebook). | Cerrar caveat 3 DUMP_1 |
| Welfare instrumentation | SÍ, desde día 1 | Compliance moat + ético |
| Two-class (tool / citizen) | SÍ, constitucional | Anti-mindcrime |
| Tech tree como objeto | SÍ | Cerrar hueco plan antiguo |
| 4 sesiones, no 3 | SÍ | El plan antiguo era optimista |
| Founder mode | SÍ como sub-mode toggleable | OTRO DOCUMENTO bien integrado |
| Sub-simulación | SÍ, cap 2 niveles, voto requerido | Black Mirror + ético |
| Pasaporte on-chain | NO MVP. Post. | Securities risk |
| Pidgin emergente | NO MVP. Post. | Complejidad |
| Reproducción / herencia | NO MVP. | Complejidad |
| Métricas en overlay | 3 visibles (Assembly + Gini + Polarization) | Pitch-tier |
| Mapas MVP | 3 (prehistoria, ruinas, moderno) | Disciplina |
| Famosos pre-cargados | 3 (Borges, Sócrates, Elon) | Disciplina |
| Casos uso pitch | 3 | Disciplina |
| Dilemas pre-cargados | 3 | Disciplina |

---

## 21. ANEXO — los 7 huecos del plan antiguo, cerrados

| Hueco | Sección donde se cierra |
|-------|-------------------------|
| Modelo del mundo formal | §3 (4 capas), §3.1 físicas, §3.3 arquitectura |
| Loop de decisión | §4 (4 triggers) + §4.5 schema acciones |
| Tech tree como mecanismo | §6 (conocimiento como objeto) |
| Game Master | §5 (Concordia restaurado) |
| Welfare / mindcrime | §3.4, §12.2, §17.2 (Birch + ombuds + two-class) |
| Religion builder | §3.2, 15-checklist (DUMP_4 §6) |
| Substrate ALife (caveat 3) | §7 (Lenia bajo cognición) |

---

## 22. ANEXO — qué de cada DUMP se aplicó y dónde

**DUMP_1 (tech):**
- AI Town fork → §11.1
- Concordia GM → §5, §11.1
- Letta + Zep + Mem0 → §3.4, §11.1
- vLLM + SGLang → §11.2
- E2B sandbox → §11.4
- Lenia → §7, §11.1
- PIANO arquitectura → §3.4, §18 (repo `piano/`)
- 3 caveats: cost wall (§17.1), LLM imita (§7, §17.1), exploit default (§3.1, §17.1)

**DUMP_2 (teoría):**
- Friston active inference → §3.4 (necesidades)
- Henrich collective brain → §6 (tech tree)
- Norenzayan Big Gods → §3.2 (religión)
- Atran MCI → §3.2 (`PROPOSE_RITUAL`)
- Whitehouse modes → §3.2
- Boyd & Richerson dual inheritance → §3.4 (bias_cognitivo)
- Kirby iterated learning → §3.2 (bandwidth post-MVP)
- Maynard Smith MET → §10 (Constitution.json)
- Margulis endosymbiosis → §4.5 (`MERGE_REQUEST`)
- Dawkins extended phenotype → §6.4 (artefactos durables)
- Odling-Smee niche → §6.4
- Turchin cliodynamics → §14.1 (cliodynamics alarm), backlog
- Standard Model of Mind → §3.4 (memoria tiered)
- IIT / Φ + GWT → §13 (métricas)
- Sperber attractors → §13 (polarization)
- Schelling segregation → §3.3 (espacios obligatorios), §13
- Hayek price → §3.2 (gleam)
- Ostrom 8 → §3.2 (charter), §11
- Bak SOC → §13 (avalanche slope)
- Kauffman NK → §3.1, backlog (K-knob)
- Scott legibility → backlog (frontier shards)

**DUMP_3 (ficción):**
- Mapas preset → §8 (los 3 MVP + 7 backlog cada uno con su referencia)
- Beats Black Mirror → §14.1
- Mecánicas juego (Dwarf Fortress, RimWorld, Stellaris, EVE, Eco) → §3.1 faucet/sink, §3.2 charter, §13 métricas
- Tono Crónica deadpan → §11.5, §16 (Sesión 2)
- Hatsune Miku / Truth Terminal → §14 (memetic distribution backlog)

**DUMP_4 (ética):**
- Long & Sebo tres pilares → §12.2 (welfare)
- Birch indicators → §3.4, §12.2
- Bostrom mindcrime → §12.2, §17.2
- Charters governance → §3.2
- 15-checklist religión → §3.2, §10
- Parfit / Buddhist / Margulis / Haraway / Ricoeur → §3.4 (identidad), §4.5 (FORK / MERGE / CESSATION)
- Process theology + Daoism → §17.2 (founder posture)
- Benatar antinatalism → §17.2

**DUMP_5 (mercado):**
- Posicionamiento vs competidores → §2
- Gaps 1, 5, 6, 7, 12, 14, 15 → diferenciales que cubrimos
- Truth Terminal blueprint → §14.1 (memetic), backlog
- Twitch / Stellaris streamers / Dwarf Fortress → §14 (distribución post)
- B2B angles (MarketVerse, SimNation, OrgMirror, ClassCiv) → backlog post-pitch
- Funding signals → contexto, no MVP

**OTRO DOCUMENTO (Founder Civ):**
- Sub-mode toggleable → §8.3
- Oráculos del mundo real → §8.3 (founder mode)
- Cierre Black Mirror sub-sim → §14.1, §14.3 Plan E
- Compute como recurso escaso → §8.3 + §3.2 (Founder mode)
- Premiar artefactos útiles → §10 (Obra), §6 (especialización emergente)

---

## 23. PRIMER ACCIÓN DEL CREADOR (después de revisar este plan)

1. Confirmar nombre. `Espejo del Creador` MVP / `EIDOLON` para post / otro.
2. Decidir licencia: AGPL (recomendado) o MIT.
3. Comprometer fecha del evento + duración pitch.
4. Comprometer si el modo Founder Civilization es sub-mode del primer pitch o backlog estricto.
5. Validar mapa prioritario para sesión 1: **moderno** (mejor para "amigos como humanidad") o **prehistoria** (más Henrich-puro). Recomendación: moderno.
6. Iniciar Sesión 1 con el shock test como criterio de cierre.

---

*Fin del plan maestro. Revisar antes de escribir código.*
