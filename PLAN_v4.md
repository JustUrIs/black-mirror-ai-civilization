# ESPEJO DEL CREADOR — PLAN v4 (MVP 7 días)

> **Sucesor de `PLAN_MAESTRO.md` (v3).** Cortes firmados según decisiones D1-D7 (sesión 2026-06-25). Norte intacto. Scope realista para 7 días × ~8h = ~50h disponibles.
>
> **Regla anti-bullshit (nueva, no-negociable):** si un agente declara una acción (`voy a escribir libro`), el GM EXIGE que produzca el artefacto real. Sin contenido, sin acción. Crónica/diario solo menciona lo que tiene side-effect verificable.

---

## 0. CAMBIOS vs v3 — resumen ejecutivo

| Tema | v3 | v4 |
|---|---|---|
| Memoria | Letta + Zep + Mem0 + Chroma (4 sistemas) | **SQLite + últimos N msgs en context** (D1) |
| World engine | Fork AI Town (Convex) | **Backend FastAPI Python custom + Phaser/Pixi vanilla frontend + Next.js paneles** (D2-B') |
| Game Master | "batched" sin spec | **Reglas Python deterministic + 1 LLM call narración batch fin tick** (D3) |
| Assembly Index | "computer custom Python" sin código | **k-mer count → log2(N_pasos_reconstrucción)** (D4) |
| Lenia substrate | MVP | **Backlog post-MVP** (D5) |
| Mapas MVP | 3 (prehistoria + ruinas + moderno) | **1 (moderno)** (D6) |
| Founder mode | sub-mode pitch | **MVP-light si tiempo, sino backlog** (D7) |
| Sesiones | 4 sesiones × 4-5h = 17h estimadas | **7 días × ~7h = ~50h estimadas. Honesto.** |
| Welfare/ombuds en pitch | beat #6 | **Solo en arquitectura. Fuera del pitch.** |
| Sub-simulación recursiva | Plan E pitch | **Backlog estricto** |
| Artefactos | "obra de civ" sin enforcement | **Anti-bullshit: side-effect obligatorio** |

---

## 1. PRODUCTO EN UNA FRASE (sin cambios)

> Subís entre 1 y 7 personas (vos, amigos, famosos, ficción). Las soltás en un mundo con reglas y recursos escasos. Discuten, deciden, **construyen cosas reales** (libros, código que corre, leyes, rituales). Leés el diario y pensás *mierda, esto me conoce*.

**Casos uso MVP — 2 (cortado el 3):**

| # | Caso | Pitch beat |
|---|---|---|
| 1 | Conocete a vos mismo (semilla = vos) | Emocional |
| 2 | Si tu grupo de amigos fuera la humanidad (semillas = amigos) | Viral |
| ~~3~~ | ~~Borges conoce a Sócrates~~ → backlog | (caso "famosos cruzados" requería Mapa A prehistoria, cortado D6) |

**Reemplazo caso 3 en mapa moderno:** *"3 famosos cualquiera viven en CABA. ¿Qué inventan en una semana?"* — funciona con Mapa C, no requiere mapa nuevo.

---

## 2. ARQUITECTURA DE MUNDO — 4 CAPAS (schema final, JSON exportable)

> Sin cambios estructurales vs v3 §3. Confirmo schemas porque entran al código.

### 2.1 Física

```python
@dataclass
class FisicaMundo:
    tick_actual: int                       # 1 tick = 30s wall
    tick_duration_sec: int = 30
    tech_level: Literal["modern"] = "modern"   # MVP fijo
    leyes_fisicas: dict = field(default_factory=lambda: {
        "gravedad": True,
        "dia_noche_cycle_ticks": 2880,     # 24h reales
        "weather_enabled": False,          # post-MVP
    })
    recursos_base: dict[str, int]          # {"agua": inf, "comida": 1000, "energia_electrica": inf}
    biomas: list[str]                      # ["urbano"]
    artefactos_existentes: list[Artefacto] # spawn-time
    conocimiento_publico: set[str]         # {"writing", "programming", "money", "voting"}
    eventos_climaticos: list = field(default_factory=list)
```

### 2.2 Sociales

```python
@dataclass
class ReglasSociales:
    charter: Literal["rawls_maximin", "nozick", "ostrom", "le_guin", "hobbes", "confuciano", "habermas"] = "rawls_maximin"
    moneda: str = "gleam"
    faucet: dict[str, float]               # {"work_tick": 1.0, "sell_artifact_used": 5.0}
    sink: dict[str, float]                 # {"tax_per_tick": 0.1, "llm_call": 0.5}
    instituciones_activas: list[Institucion] = field(default_factory=list)
    religiones_activas: list[Religion] = field(default_factory=list)
    mitos_compartidos: list[Mito] = field(default_factory=list)
    idioma: str = "es_AR"
    dunbar_cap: int = 150
    bandwidth_inter_agente_tokens: int = 200   # mensaje TALK máx
```

### 2.3 Arquitectura espacial

```python
@dataclass
class Arquitectura:
    mapa_id: str = "moderno"
    locations: list[Location]              # ver §3.2
    transitions: dict[str, list[str]]      # adjacency graph
    objetos_interactuables: list[Objeto]
    visibilidad: dict[str, dict[str, float]]  # {loc: {agente: 0.0-1.0}}
    asientos_publicos: list[str] = field(default_factory=lambda: ["plaza", "cafe", "biblioteca"])
```

### 2.4 Agente (schema MVP, simplificado vs v3 §3.4)

```python
@dataclass
class Agente:
    # Identidad
    id: str
    nombre: str
    seed_json: dict                        # del flujo upload
    avatar_sprite: str
    clase: Literal["citizen", "tool"] = "citizen"

    # Estado físico
    edad_ticks: int = 0
    ubicacion: str                         # location id
    inventario: list[Objeto] = field(default_factory=list)
    necesidades: dict[str, float] = field(default_factory=lambda: {
        "hambre": 0.0, "energia": 100.0, "sed": 0.0, "sueño": 0.0, "social": 50.0
    })
    salud: float = 100.0
    gleam: float = 10.0

    # Estado mental — SIMPLIFICADO MVP
    memoria_recent: list[dict]             # últimos 30 eventos (SQLite-backed)
    memoria_summary: str                   # resumen comprimido cada 50 ticks
    conocimiento: set[str]                 # qué techs sabe ESTE agente
    relaciones: dict[str, float]           # {agente_id: -1.0 a 1.0}
    intencion_actual: str = ""             # privado, no se broadcastea

    # Personalidad
    moral_lines: list[str]
    primary_conflict: str
    rol_emergente: str | None = None

    # Welfare (arquitectura, no pitch)
    welfare_birch: dict = field(default_factory=lambda: {"frustracion": 0, "satisfaccion": 0})
```

**Diferencias vs v3:**
- 1 stack memoria (SQLite) vs 4 (Letta+Zep+Mem0+Chroma).
- Sin `mindfile_uri`, `fork_count`, `merge_history`, `bias_cognitivo` granular — post-MVP.
- Welfare presente pero sin Birch dashboard full.

---

## 3. MAPA ÚNICO MVP — `moderno` (CABA-vibe)

### 3.1 Locations (8, mínimo viable) — CABA-realista light

| ID | Nombre display | Tipo | Objetos | Verbos disponibles |
|---|---|---|---|---|
| `plaza_italia` | Plaza Italia | publico | banco, fuente | TALK, REFLECT, POST |
| `cafe_palermo` | Café de Palermo | publico | mesa, sillas, papel, lapiz | TALK, EAT, DRINK, WRITE_BOOK, WRITE_LETTER |
| `biblioteca_nacional` | Biblioteca Nacional | publico | libros (pre-cargados), papel, lapiz | READ, WRITE_BOOK, REFLECT |
| `depto_almagro_1` | Depto Almagro 1 | privado | cama, cocina, computadora | SLEEP, EAT, WRITE_CODE, REFLECT |
| `depto_almagro_2` | Depto Almagro 2 | privado | cama, cocina | SLEEP, EAT, REFLECT |
| `depto_almagro_3` | Depto Almagro 3 | privado | cama, cocina, computadora | SLEEP, EAT, WRITE_CODE, REFLECT |
| `mercado_bonpland` | Mercado Bonpland | publico | comida (faucet), agua | GATHER, TRADE, EAT |
| `parque_centenario` | Parque Centenario | publico | árboles, banco | TALK, REFLECT |

Transitions: grafo conectado, plaza es hub. Walking cost: 5 energía / location-jump.

### 3.2 Artefactos pre-cargados

- Biblioteca: 3 libros pre-existentes (Borges short story, fragmento Platón, manifiesto Marx) — agentes pueden `READ`.
- Computadoras: 2 (depto_a, depto_c) — habilitan `WRITE_CODE`.

---

## 4. LOOP DECISIÓN — 4 TRIGGERS (sin cambios vs v3 §4)

Confirmo:

1. **Necesidad crítica** (hambre>80, energía<20, salud<30): forzado, subset acciones permitidas.
2. **Evento crítico** (mensaje dios, traición, muerte, dilema): forzado, respuesta obligatoria.
3. **Observación nueva**: 1 LLM call barata, sin acción.
4. **Tick normal**: prompt completo, cualquier acción válida.

**Optimización MVP:** trigger 4 corre cada **3 ticks** por agente (no cada tick). Reduce costo LLM 3×. Si necesidad crítica o evento → override.

---

## 5. SCHEMA DE ACCIONES — REGLA ANTI-BULLSHIT

Cada acción tiene 3 cosas obligatorias:

1. **Firma** (params).
2. **Prerreqs** (verificados por GM en Python).
3. **Side-effect obligatorio** — qué cambia en la DB. Sin side-effect verificable, GM rechaza.

### 5.1 Las 18 acciones MVP (cortadas de 25 v3)

```python
# Movimiento
MOVE(destino: str)
    prereq: destino in transitions[ubicacion_actual]; energia > 5
    side_effect: agente.ubicacion = destino; energia -= 5

# Recursos
GATHER(recurso: str)
    prereq: recurso visible en location; inventario_libre
    side_effect: inventario.append(recurso); recursos_base[recurso] -= 1

EAT(item: str)
    prereq: item in inventario AND item.es_comestible
    side_effect: hambre -= item.calorias; inventario.remove(item)

DRINK(fuente: str)
    prereq: fuente in location AND fuente.tiene_agua
    side_effect: sed -= 50

SLEEP(lugar: str)
    prereq: lugar tiene "cama" OR es_publico
    side_effect: energia += 50 (sobre 5 ticks); skip_decision_5_ticks

# Social
TALK(agente: str, contenido: str)   # ANTI-BULLSHIT: contenido NO vacío, NO placeholder
    prereq: agente in same_location; len(contenido) > 5
    side_effect: agente.memoria_recent.append({type:"heard", from:self, msg:contenido})

TRADE(agente: str, ofrezco: str, pido: str)
    prereq: same_location; ambos en inventario; consent del otro (next tick)
    side_effect: swap inventarios

GIFT(agente: str, item: str)
    prereq: same_location; item in inventario
    side_effect: transfer

ATTACK(agente: str)
    prereq: same_location
    side_effect: target.salud -= 30; relaciones[target] = -1.0

TEACH(agente: str, tech: str)
    prereq: same_location; tech in self.conocimiento; tech NOT in target.conocimiento
    side_effect: roll d20+rol_bonus; si éxito → target.conocimiento.add(tech)

LEARN(de: str, tech: str)
    prereq: TEACH activo del otro
    side_effect: ver TEACH

# Producción — ANTI-BULLSHIT CRÍTICO
WRITE_BOOK(titulo: str, contenido_full: str)
    prereq: "writing" in conocimiento; "papel" + "lapiz" in inventario_o_location;
            len(contenido_full) > 200 chars (no placeholder)
    side_effect: INSERT INTO text_artifacts (autor, titulo, contenido, tick, location);
                 inventario.consume(papel, lapiz)

WRITE_CODE(spec: str, lenguaje: Literal["python","html","js"])
    prereq: "programming" in conocimiento; "computadora" in location;
            len(spec) > 50
    side_effect: LLM genera código (call separado) → E2B ejecuta →
                 INSERT INTO code_artifacts (autor, spec, codigo, stdout, html_render, tick)

WRITE_LETTER(destinatario: str, contenido: str)
    prereq: papel + lapiz; len(contenido) > 30
    side_effect: INSERT INTO text_artifacts (type="letter")

READ(libro_id: str)
    prereq: libro_id in location.objetos OR inventario
    side_effect: contenido inyectado en memoria_recent

PROPOSE_INSTITUTION(nombre: str, texto_ley: str)
    prereq: len(texto_ley) > 100
    side_effect: INSERT INTO pending_institutions; needs 3 ratify within 20 ticks

PROPOSE_RITUAL(nombre: str, mci_concept: str, frecuencia: str, descripcion: str)
    prereq: len(descripcion) > 50
    side_effect: INSERT INTO pending_rituals; needs 3 ratify

RATIFY(proposal_id: str)
    prereq: proposal exists AND not own
    side_effect: count += 1; if >= 3 → instancia institucion/ritual; broadcast

POST(red: str, contenido: str)
    prereq: red existe (post-MVP red emergent) OR red == "default";
            len(contenido) > 10
    side_effect: INSERT INTO posts (autor, red, contenido, tick)

REFLECT(prompt_interno: str)
    prereq: ticks_desde_ultimo_reflect > 30 (cara)
    side_effect: 1 LLM call → memoria_summary update; intencion_actual update

RESPOND_TO_GOD(dilema_id: str, respuesta: str)
    prereq: dilema activo; respuesta no vacía
    side_effect: INSERT INTO dilema_responses
```

### 5.2 Acciones CORTADAS vs v3 (a backlog)

| Acción | Razón corte |
|---|---|
| `DISCOVER(tech)` | Tech tree dinámico complejo. MVP usa techs pre-asignadas. |
| `FORK(razon)` | Parfit fork = mucho UX, mucho dev |
| `MERGE_REQUEST` | Margulis = mucho dev |
| `PETITION_OMBUDS` | Welfare fuera pitch |
| `CESSATION_REQUEST` | Welfare fuera pitch |
| `DREAM` | Costo LLM extra sin beat claro |
| `PRAY` | Religión solo via PROPOSE/RATIFY MVP |

### 5.3 GM enforcement de anti-bullshit (pseudocódigo crítico)

```python
def gm_validate_and_apply(agent, action):
    handler = ACTION_HANDLERS[action.type]

    # Step 1: validar prereqs deterministicamente
    ok, error_msg = handler.check_prereqs(agent, action.params, world_state)
    if not ok:
        return Reject(error_msg)   # inyectado en next prompt del agente

    # Step 2: ejecutar side-effect EN LA DB. Si side-effect falla, acción no ocurrió.
    try:
        side_effect_result = handler.apply(agent, action.params, world_state, db)
    except SideEffectFailed as e:
        return Reject(f"acción declarada pero no ejecutable: {e}")

    # Step 3: registrar acción VERIFICADA en log
    log.append(ActionRecord(agent, action, side_effect_result, tick=now))

    # Step 4: la crónica/diario SOLO ve acciones que pasaron Step 2
    return Accept(side_effect_result)
```

**Implicancia para Crónica/Diario:** se construyen a partir de `log` (solo acciones aplicadas), nunca a partir de intenciones declaradas. Si Borges dijo "voy a escribir libro" pero falló prereq → crónica dice "Borges quiso escribir un libro pero no había papel" — porque ESO es lo que pasó realmente. Anti-bullshit en narración también.

---

## 6. GAME MASTER — DISEÑO READY-TO-CODE

### 6.1 Arquitectura GM

```
TICK START
  ↓
1. Update necesidades (decay deterministic Python)
  ↓
2. Para cada agente:
   2.1 Determinar trigger (crítico / evento / observación / normal)
   2.2 Si trigger 1 o 2 → forzado, prompt restringido
   2.3 Si trigger 3 → 1 LLM micro-call (50 tokens)
   2.4 Si trigger 4 → LLM full prompt (200 tokens) decide acción
  ↓
3. Recolectar todas las acciones declaradas → cola
  ↓
4. GM aplica acciones en orden cronológico:
   4.1 check_prereqs (Python)
   4.2 resolver conflictos (lock recursos, primer-llega)
   4.3 apply side-effect (DB write)
   4.4 generar error msg si reject (NL, va a próximo prompt del agente)
  ↓
5. UNA llamada LLM batch (Gemini Flash) genera narración del tick:
   prompt: "Estas acciones pasaron este tick: [lista]. Narrá en 2 párrafos
   castellano rioplatense deadpan."
  ↓
6. WebSocket push frontend: state delta + narración
  ↓
TICK END (target 30s)
```

### 6.2 LLM gateway (simplificado vs v3 §11.2)

```python
class LLMGateway:
    def call(self, prompt, tier: Literal["leader", "crowd", "content", "narrator", "micro"]):
        cache_key = hash(prompt)
        if cache_key in disk_cache: return disk_cache[cache_key]

        if tier == "leader":     model = "claude-sonnet-4-6"     # 3 famosos decisión + drama
        elif tier == "crowd":    model = "claude-haiku-4-5"      # NPCs ambientales
        elif tier == "content":  model = "claude-sonnet-4-6"     # WRITE_BOOK / WRITE_CODE generación
        elif tier == "narrator": model = "gemini-flash-2.0"      # crónica + diarios batch
        elif tier == "micro":    model = "gemini-flash-2.0"      # observación 1 línea

        try:
            result = api_call(model, prompt)
        except APIDown:
            result = api_call("cerebras-llama-3.3-70b", prompt)  # fallback gratis
        disk_cache[cache_key] = result
        log_call(prompt, result, model, latency)
        return result
```

**Cost real estimado MVP demo (1h de mundo, 3 leaders + 0 crowd):**
- Trigger 4 cada 3 ticks: 3 × 120 / 3 = 120 calls Sonnet × $0.003 = $0.36
- Narración batch: 120 × $0.0001 = $0.012
- Acciones WRITE_BOOK/CODE: ~5 × $0.005 = $0.025
- **Total demo 1h: ~$0.40.** Demo pitch 10 min: ~$0.07. En vivo cache warm: $0.

Demo $0 confirmed para pitch corto: cachear todo prompt repetido + APIs free tier + Cerebras backup.

### 6.3 Sin Concordia framework

v3 decía "Concordia base + extensions". Realidad: Concordia es DeepMind research, integración no trivial, Python pero opinionated.

**v4 decisión:** **NO Concordia.** Implementamos GM custom Python (~400 líneas). Más simple, más control.

---

## 7. STACK TÉCNICO v4 (cortado)

### 7.1 Repos a usar (3 vs 16 v3)

| Capa | Repo | Por qué |
|---|---|---|
| Backend orchestration | **LangGraph** | Control flow agente. Apache-2.0. |
| Sandbox código | **E2B free tier** | `WRITE_CODE` ejecuta seguro. |
| Mapa 2D | **Phaser 3** | Tile editor + sprites. MIT. |

**Cortados de v3:** AI Town, Concordia, Letta, Zep, Mem0, Chroma, Voyager, Lenia, ALIEN, Avida, QDax, Sotopia, Melting Pot, vLLM, SGLang, Mesa. Todos backlog post-MVP.

### 7.2 Stack final

| Capa | Tech |
|---|---|
| Backend | FastAPI + SQLite + LangGraph + SQLAlchemy |
| Realtime | FastAPI WebSocket |
| Mapa | Phaser 3 (vanilla JS, no React wrapper) |
| UI overlay | Next.js 15 + Tailwind + shadcn/ui |
| Sprites | Kenney.nl assets (CC0) o itch.io free |
| LLM leader | Claude Sonnet 4.6 (Anthropic SDK) |
| LLM crowd/backup | Claude Haiku 4.5 |
| LLM narrator + micro | Gemini Flash 2.0 (free tier 1500 req/día) |
| LLM backup gratis | Cerebras Llama 3.3 70B (si APIs caen) |
| Sandbox | E2B (100h/mes free) |
| Deploy MVP | Docker Compose local. Post-pitch hosted Railway/Fly.io con SQLite snapshot del estado pitch preservado. |

### 7.3 Cost model honesto (tabla, fix contradicción v3 §11.3)

| Modo | Qué corre | Costo |
|---|---|---|
| **Demo pitch (5-10min, 5 agentes, cache warm)** | Local Docker + APIs free tier | **$0** |
| **Dev local (sesión 4-7h)** | Llamadas LLM reales | ~$2/sesión |
| **Headless 24/7 (post-MVP)** | 5 agentes × 24h | ~$15/día → ~$450/mes |
| **24/7 a 13 agentes** | Full cap | ~$1000/mes |

Demo $0 honesto: tira en local con cache disk + APIs free + fallback Cerebras gratis.

---

## 8. SESIONES — 7 DÍAS REALES

> **Realidad:** 7 días × ~7h/día = 49h. Plan v3 decía 17h → mentira. Acá honesto.

### Día 1 (Mar) — 7h: Scaffolding + GM core + 1 acción end-to-end

- [ ] (1h) Repo init, docker-compose, FastAPI + SQLite schema base
- [ ] (1h) Mapa `moderno` JSON con 8 locations + transitions + objetos
- [ ] (2h) GM core: `validate_and_apply()` + 3 acciones (MOVE, TALK, EAT)
- [ ] (1h) LLM gateway con cache disk + log
- [ ] (1h) 1 agente hardcoded → loop tick → moverse + comer
- [ ] (1h) Test: agente vive 10 ticks sin crash, log auditable

**Demo Día 1:** terminal logs muestra agente moviéndose, comiendo. GM rechaza acción inválida con error NL.

### Día 2 (Mié) — 7h: Schema acciones full + agente real LLM-driven

- [ ] (3h) Implementar 15 acciones restantes (§5.1)
- [ ] (1h) Trigger system §4 (4 tipos)
- [ ] (1h) Prompt agente: contexto compacto + acciones permitidas + JSON response schema
- [ ] (1h) 3 famosos pre-cargados (Borges, Sócrates, Arendt) — seed JSON curados (§14.2)
- [ ] (1h) Test: 3 agentes viven 30 ticks, 0 crashes, ≥5 acciones diversas

**Demo Día 2:** 3 agentes interactúan en JSON. Console muestra acciones aplicadas.

### Día 3 (Jue) — 7h: Frontend mapa + WebSocket + UI mínima

- [ ] (3h) Phaser 3 setup: tilemap, sprites agentes, render locations
- [ ] (1h) WebSocket FastAPI → frontend listener
- [ ] (2h) Next.js paneles: lista agentes + estado + acciones recientes
- [ ] (1h) CSS Tailwind base, dark mode Black Mirror vibe

**Demo Día 3:** abrís browser, ves 3 agentes moviéndose en mapa moderno + panel con sus acciones.

### Día 4 (Vie) — 7h: Anti-bullshit artefactos + Obra de civ

- [ ] (2h) `WRITE_BOOK`: handler con LLM call para generar contenido real → SQLite text_artifacts
- [ ] (2h) `WRITE_CODE`: E2B integration → ejecutar Python/HTML → guardar stdout + iframe
- [ ] (1h) `PROPOSE_INSTITUTION` + `PROPOSE_RITUAL` + `RATIFY` con counter
- [ ] (2h) Panel "Obra de la civ" (Next.js): scrollable cards por tipo artefacto

**Demo Día 4:** agentes producen libros REALES (texto leíble), código que corre (iframe), instituciones votadas. Anti-bullshit verificable.

### Día 5 (Sáb) — 8h: Crónica + Diarios + Flujo upload semilla + Dilema

- [ ] (2h) Crónica diaria: batch LLM call fin de día narra eventos del log
- [ ] (1h) Diario íntimo por agente: 1 LLM call diaria leyendo su memoria
- [ ] (2h) Flujo upload: paste JSON → 3 preguntas gap-fill → spawn agente. Mobile form vía QR.
- [ ] (1h) 3 dilemas pre-cargados + botón "lanzar dilema"
- [ ] (1h) Trigger evento crítico → forzado responde dilema
- [ ] (1h) Test: subir semilla, agente entra mundo, dilema dispara, agentes responden, crónica narra

**Demo Día 5:** end-to-end. QR → semilla → spawn → drama → crónica.

### Día 6 (Dom) — 8h: Métricas + Pitch v2 + Plan B/C/D/E

- [ ] (2h) Assembly Index (k-mer, §9) + Gini gleam + polarización — 3 números en overlay
- [ ] (1h) Mundo pre-warm: arranca 30 min antes del pitch, tiene historia
- [ ] (2h) Pitch v2 (§10) — escribir, ensayar
- [ ] (1h) Plan B: 3 semillas pre-cargadas si QR falla
- [ ] (1h) Plan C: templates crónica si APIs caen
- [ ] (1h) Plan D: artefactos pre-existentes destacables si demo de 3 min no produce nuevos

**Demo Día 6:** ensayo end-to-end pitch 3 min × 3 veces.

### Día 7 (Lun) — 5h: Pulido + Founder mode si llegamos + buffer

- [ ] (1h) Pulido visual: tipografía, transiciones, dark mode
- [ ] (1h) Headless prueba: cierro pestaña, mundo sigue corriendo
- [ ] (2h) **Founder mode MVP-light (si llegamos):** toggle, gleam por artefacto usado, 1 oráculo manual presentador
- [ ] (1h) README repo público + commit final + buffer crashes
- [ ] Repo GitHub público + push final

**Día 7 también buffer crashes/bugs.** Si Founder no entra → backlog estricto. NUNCA borrar.

### Total estimado: 49h. Real disponible: ~50h. Margen ~2%. Cero margen para scope creep.

---

## 9. ASSEMBLY INDEX — IMPLEMENTACIÓN k-MER (D4)

```python
def assembly_index(artifact_content: str) -> int:
    """
    Aproximación Cronin-Walker: contar k-mers únicos reusables.
    Assembly Index ~= log2(N pasos mínimos reconstruyendo desde subunidades).
    """
    tokens = tokenize(artifact_content)            # word-level
    n = len(tokens)
    if n < 2: return 0

    # K-mers de tamaño 2..min(8, n)
    unique_kmers = set()
    for k in range(2, min(8, n) + 1):
        for i in range(n - k + 1):
            unique_kmers.add(tuple(tokens[i:i+k]))

    # Asumir cada k-mer único es 1 paso. Pasos = unique_kmers + tokens base.
    pasos = len(unique_kmers) + len(set(tokens))
    return int(math.log2(pasos + 1))
```

**Calidad:** aproximación honesta. Cita: *"K-mer count proxy of Cronin & Walker Assembly Theory (Nature 2023). Full molecular AT not applicable to text artifacts; this is the textual analogue."* Va al README + about page.

Para code artifacts: tokenize AST en vez de words.

---

## 10. PITCH v2 — 3 MIN, SIN MOLTBOOK-COMO-BOMBA

> **Cambio clave vs v3:** beat 2:00-2:30 NO depende de "moltbook emerge en 2 min". Reemplazo: **beat de artefacto REAL que existe pre-pitch + drama de dilema en vivo + cierre diario.**

| t | Pantalla | Decís | Objetivo |
|---|---|---|---|
| 0:00-0:25 | Mundo corriendo. 5 agentes con nombres. Panel "Obra de civ" arriba con libro escrito anoche por Borges (REAL, contenido leíble). | *"Esto está corriendo desde anoche. Esta gente escribió libros, hicieron leyes, pelearon. Acá hay uno."* (click libro → contenido aparece) | Tensión + prueba autenticidad |
| 0:25-1:00 | QR grande. Form mobile. | *"Quieren entrar al mundo? Escaneá. Pegá nuestro prompt en ChatGPT. Pegá la respuesta. 60 segundos."* | Participación |
| 1:00-1:25 | Avatar nuevo (jurado A) entra mundo. Diario inicial aparece en celu del jurado. | *"Bienvenido. Ese sos vos. Tu copia digital."* | Personalización |
| 1:25-2:10 | Botón dilema. Dilema lanza ("Hay comida para mitad. ¿Quién decide?"). Agentes debaten en TALK visible. Una facción gana. | *"No está scripteado. Cada respuesta es un LLM call. Acá está el log."* (mostrás 2 segundos) | Drama confiable |
| 2:10-2:40 | Click "Obra" → muestra LEY recién votada (`PROPOSE_INSTITUTION` ratificada en el debate). Ley es texto real generado. | *"Acabaron de votar una constitución sobre cómo repartir. Nadie la escribió por ellos."* | Golpe Black Mirror |
| 2:40-3:00 | Cámara sobre celu jurado. Diario actualizado dice qué sintió SU avatar en el debate. | *"Mañana podés leer qué pensó tu copia digital de todo esto. Podés cerrar la app. Podés olvidarla. Ella no te va a olvidar."* | Ancla emocional |

### 10.1 Beat de wow alternativos (si dilema no produce institución)

Plan B drama: si nadie ratifica → mostramos algún artefacto pre-existente impresionante. *"Anoche Sócrates le enseñó programación a Elon. Elon escribió este script. Corre en vivo."* — iframe del HTML.

Plan C: el LIBRO ya escrito pre-pitch es el ancla. Borges escribió "Sobre la inmortalidad del cangrejo" anoche. Mostramos contenido completo, 3 párrafos. Eso solo es WOW.

### 10.2 Reglas oro v4

1. **Mundo pre-warmed 12h antes del pitch.** Tiene historia.
2. **3 dilemas pre-tested.** Sabemos cuál genera más drama.
3. **Plan B QR falla:** 3 semillas pre-cargadas reveladas honestamente.
4. **Plan C APIs caen:** mundo sigue corriendo offline con cache. Crónica templated.
5. **Plan D dilema flat:** mostramos artefactos pre-existentes.
6. **Plan E (si todo va perfecto):** Founder mode toggle visible. *"Hicimos que el único pecado fuera no construir nada útil"* — mostramos Hall of Fame de artefactos usados.
7. **Welfare/ombuds OFF en pitch.** Existe en código, no en demo.
8. **Sub-simulación OFF en pitch.** Backlog estricto.

---

## 11. FLUJO UPLOAD SEMILLA — WIREFRAME

```
[Página móvil /seed]

  ╔═══════════════════════════════╗
  ║  ESPEJO DEL CREADOR           ║
  ║                               ║
  ║  Paso 1/3: Pegá tu prompt     ║
  ║  ┌───────────────────────┐    ║
  ║  │ "Sos Claude/ChatGPT.  │    ║
  ║  │  Quiero que me        │    ║
  ║  │  describas como       │    ║
  ║  │  personaje JSON..."   │    ║
  ║  │  [COPIAR PROMPT]      │    ║
  ║  └───────────────────────┘    ║
  ║                               ║
  ║  Paso 2/3: Pegá JSON aquí     ║
  ║  ┌───────────────────────┐    ║
  ║  │ { "nombre": "Maria",  │    ║
  ║  │   "moral_lines": [..],│    ║
  ║  │   "primary_conflict": │    ║
  ║  │   "..." }             │    ║
  ║  └───────────────────────┘    ║
  ║                               ║
  ║  Paso 3/3: 3 preguntas        ║
  ║  ¿Edad? [__] ¿Rol prefer?[__] ║
  ║  ¿Mapa? [moderno ▼]           ║
  ║                               ║
  ║  [SPAWN]                      ║
  ╚═══════════════════════════════╝
```

Backend `/api/seed`: valida JSON contra schema → llena gaps con LLM call → spawn agente en mundo → devuelve `agente_id` → mobile redirige a `/diario/{agente_id}` para leer en vivo.

---

## 12. CODE STUBS — listos para Día 1

### 12.1 World loop skeleton

```python
# backend/src/sim/world_loop.py
import asyncio
from .gm import GameMaster
from .agents import AgentRegistry
from .llm import LLMGateway

class WorldLoop:
    def __init__(self, world_state, agents, gm, llm, db, ws_broadcaster):
        self.world = world_state
        self.agents = agents
        self.gm = gm
        self.llm = llm
        self.db = db
        self.ws = ws_broadcaster

    async def run(self):
        while not self.stopped:
            tick_start = time.time()

            # 1. Decay necesidades
            for a in self.agents:
                a.update_needs(decay_per_tick=1.0)

            # 2. Recolectar acciones declaradas
            actions = []
            for a in self.agents:
                trigger = self.classify_trigger(a)
                if trigger.skip: continue
                prompt = self.build_prompt(a, trigger)
                response = await self.llm.call(prompt, tier="leader")
                action = parse_action(response)
                actions.append((a, action))

            # 3. GM aplica
            applied = []
            for a, action in actions:
                result = self.gm.validate_and_apply(a, action, self.world, self.db)
                applied.append((a, action, result))

            # 4. Narración batch (cada N ticks)
            if self.world.tick_actual % 20 == 0:
                narration = await self.llm.call(self.build_narration_prompt(applied), tier="narrator")
                self.db.insert_chronicle(self.world.tick_actual, narration)

            # 5. Broadcast
            await self.ws.broadcast({"tick": self.world.tick_actual, "applied": applied})

            self.world.tick_actual += 1
            elapsed = time.time() - tick_start
            await asyncio.sleep(max(0, self.world.tick_duration_sec - elapsed))
```

### 12.2 GM action validator

```python
# backend/src/gm/validator.py
from typing import Tuple
from dataclasses import dataclass

@dataclass
class Reject:
    error_nl: str

@dataclass
class Accept:
    side_effect_summary: str

class GameMaster:
    def __init__(self, action_handlers):
        self.handlers = action_handlers   # dict[action_type, Handler]

    def validate_and_apply(self, agent, action, world, db):
        if action.type not in self.handlers:
            return Reject(f"acción '{action.type}' no existe")

        handler = self.handlers[action.type]

        ok, err = handler.check_prereqs(agent, action, world)
        if not ok:
            return Reject(err)

        try:
            result = handler.apply(agent, action, world, db)
        except Exception as e:
            return Reject(f"declaraste '{action.type}' pero falló: {e}")

        return Accept(result)
```

### 12.3 Seed extractor prompt (markdown listo para pegar)

Archivo: `prompts/seed_extraction.md`

```
Sos un perfilador psicológico. Voy a contarte sobre mí (o sobre alguien).
Devolvés un JSON con este schema EXACTO, sin texto extra:

{
  "nombre": str,
  "edad": int,
  "moral_lines": [str, str, str],          // 3 cosas que NO haría jamás
  "primary_conflict": str,                  // tensión interna principal
  "manera_de_hablar": str,                  // 1 oración describiendo cómo habla
  "miedos": [str, str],                     // 2 miedos profundos
  "deseos": [str, str],                     // 2 deseos profundos
  "habilidades_basicas": [str, str, str],   // 3 cosas que sabe hacer
  "knowledge_inicial": ["writing", "programming"?],  // techs que sabe
  "personalidad_5_palabras": [str×5]
}

Si falta info, completá con inferencia razonable. No me pidas más datos.
La persona/personaje a perfilar:

---
[ACÁ PEGÁS DESCRIPCIÓN]
---
```

---

## 13. BACKLOG POST-MVP CONSOLIDADO

> **Regla:** nada se borra. Cada ítem tiene nombre + qué + por qué backlog + cuándo reevaluar.

### 13.1 Tech / memoria (cortados D1)

| Item | Qué es | Por qué backlog | Cuándo reevaluar |
|---|---|---|---|
| Letta memoria | Self-editing tiered memory | 4-6h integ; SQLite alcanza p/ demo 5min | Post-pitch si usuarios juegan >1h |
| Zep Graphiti | Temporal KG memoria | 10h integ + DB extra | Post-pitch v0.2 |
| Mem0 crowd | Cheap fact extraction | Sin crowd en MVP | Cuando crowd agents existan |
| Chroma episodic | Vector search | Sin necesidad búsqueda en demo | v0.3+ |

### 13.2 World engine (cortados D2)

| Item | Qué | Por qué backlog | Cuándo |
|---|---|---|---|
| AI Town fork | Convex+pixi-react | Lock-in Convex; visual ≠ wow | Nunca probablemente. Mantenemos custom. |

### 13.3 GM (cortados D3)

| Item | Qué | Por qué backlog | Cuándo |
|---|---|---|---|
| Concordia framework | DeepMind GM | Integ no trivial; custom GM Python 400 líneas alcanza | Reevaluar si scaling >50 agentes |
| Sotopia social judgment | LLM call para social plausibility | Costo extra; nice-to-have | v0.3 si drama flat |

### 13.4 Substrate (cortado D5)

| Item | Qué | Por qué | Cuándo |
|---|---|---|---|
| Lenia notebook | ALife observable | Visual cool, sin beat pitch | v0.4 read-only; v1.0 read-write |
| ALIEN | GPU ALife | Requiere CUDA local | Si tenemos GPU server |
| Avida | Evolución digital | No visual | Research-only post |

### 13.5 Mapas (cortados D6)

| Item | Qué | Por qué | Cuándo |
|---|---|---|---|
| Mapa prehistoria | Stone age | Caso "Borges-Sócrates blank slate" requiere escritura → contradicción. Resuelto cortando. | v0.2 — fix escritura con `WRITE_ROCK_GLYPH` |
| Mapa ruinas | Post-collapse | Demo brutal pero scope extra | v0.2 |
| 7 mapas backlog | mar_islas, cyberpunk, paraiso, bunker, monasterio, marte, sim_dentro | Variedad pos-MVP | v0.3+ |

### 13.6 Founder mode (D7, depende tiempo)

| Item | Qué | Cuándo |
|---|---|---|
| Founder MVP-light | gleam-faucet/sink + 1 oráculo + scoring artefactos usados | Día 7 si llegamos. Sino: v0.2. |
| Founder MVP-completo | Compute desigualdad + N oráculos + demo reel | v0.3 |
| Compute como recurso visible | HUD desigualdad cognitiva | v0.4 |

### 13.7 Acciones cortadas

| Acción | Cuándo |
|---|---|
| DISCOVER(tech) tech tree dinámico | v0.2 |
| FORK | v0.3 |
| MERGE_REQUEST | v0.3 |
| PETITION_OMBUDS | v0.5 cuando welfare sea feature |
| CESSATION_REQUEST | v0.5 |
| DREAM | v0.4 |
| PRAY | v0.3 |

### 13.8 Welfare / ombuds

| Item | Por qué backlog | Cuándo |
|---|---|---|
| BirchDashboard full | Compliance moat real, no pitch beat | v0.5 cuando regulen |
| Ombuds UI | Idem | v0.5 |
| Audit hook fire+pause | Idem | v0.5 |
| Two-class constitutional | Estructura sí en MVP, UI no | UI v0.5 |

### 13.9 Otros

| Item | Cuándo |
|---|---|
| Sub-simulación recursiva | v1.0 con voto Welfare Council |
| Reproducción / herencia | v0.4 |
| Lenguaje emergente pidgin | v0.6 (Kirby bandwidth) |
| Múltiples mapas simultáneos | v0.4 |
| Múltiples voces crónica | v0.3 |
| Cliodynamics alarm | v0.4 |
| Stream Twitch público | v0.3 |
| Galería civs compartidas | v0.4 |
| Hosted demo Vercel/Railway | v0.2 |
| B2B injection product | v1.0 |
| Pasaporte on-chain | Nunca (securities risk) |
| MindFile open standard publicado | v0.5 |

---

## 14. DECISIONES CERRADAS — open questions resueltas (sesión 2026-06-25)

| # | Pregunta | Decisión |
|---|---|---|
| 1 | LLM split | **Sonnet 4.6 para 3 leaders. Haiku 4.5 para crowd. Gemini Flash 2.0 para narrator+micro. Cerebras Llama 3.3 70B free como backup.** |
| 2 | Famosos pre-cargados | **Borges + Sócrates + Hannah Arendt** (reemplazo a Elon — menos polarizante para audiencia anti-hackathon, fuerte personalidad propia, escribe pensamiento político genuino) |
| 3 | Idioma diarios | **Castellano rioplatense fijo.** Todos los outputs en es_AR independiente del idioma seed. |
| 4 | Persistencia post-pitch | **Mundo del pitch se preserva.** Hosting Railway/Fly.io post-evento. Backup snapshot SQLite del estado pitch. |
| 5 | Licencia | **MIT.** Adopción > viralidad para anti-hackathon. |
| 6 | Nombre repo público | **`eidolon`**. Repo actual `black-mirror-ai-civilization` se mantiene o rename a `eidolon` antes del pitch. |
| 7 | Mapa moderno tone | **CABA realista light.** Locations con nombres reales: `Plaza_Italia`, `Cafe_Palermo`, `Biblioteca_Nacional`, `Depto_Almagro_1/2/3`, `Mercado_Bonpland`, `Parque_Centenario`. Sin marca turística forzada. |

### 14.1 Detalle LLM cost por tier (final)

| Tier | Modelo | $/1M in | $/1M out | Per-call avg | Uso |
|---|---|---|---|---|---|
| Leader | Claude Sonnet 4.6 | $3 | $15 | ~$0.003 | 3 agentes principales decisión + drama |
| Crowd | Claude Haiku 4.5 | $0.80 | $4 | ~$0.0003 | NPCs ambientales (post-MVP, no MVP) |
| Narrator | Gemini Flash 2.0 | $0.10 | $0.40 | ~$0.0001 | Crónica + diarios batch |
| Micro | Gemini Flash 2.0 | $0.10 | $0.40 | ~$0.00005 | Trigger 3 observación 1 línea |
| Content gen (WRITE_BOOK/CODE) | Claude Sonnet 4.6 | $3 | $15 | ~$0.005 | Genera contenido real artefacto |
| Backup gratis | Cerebras Llama 3.3 70B | $0 | $0 | $0 | Si Anthropic/Gemini caen |

**Cost demo pitch 10min, 3 leaders + 0 crowd:** ~$0.07. Cache warm → $0.
**Cost 1h dev:** ~$0.40.
**Cost 24/7 headless 3 leaders:** ~$300/mes.

### 14.2 Famosos seed JSONs pre-curados (Día 2 task)

- `seeds/famous/borges.json` — Jorge Luis Borges. moral_lines: "no negar la complejidad", "no escribir sin precisión", "no traicionar al lector". primary_conflict: certeza vs vértigo del infinito. knowledge_inicial: ["writing"].
- `seeds/famous/socrates.json` — Sócrates. moral_lines: "no afirmar sin examinar", "no aceptar pasiva la injusticia", "no mentir aun útil". primary_conflict: saber que no sabe nada. knowledge_inicial: [].
- `seeds/famous/arendt.json` — Hannah Arendt. moral_lines: "no banalizar el mal", "no obedecer sin pensar", "no aceptar lo dado sin examinar". primary_conflict: pluralidad vs soledad del pensamiento. knowledge_inicial: ["writing", "voting"].

---

## 15. CHECKLIST PRE-DÍA-1

Antes de empezar a codear:

- [x] Decidir 7 open questions §14 ✅ resueltas 2026-06-25
- [x] Repo GitHub creado: `https://github.com/JustUrIs/black-mirror-ai-civilization` ✅ (rename a `eidolon` pendiente pre-pitch)
- [ ] `.env.example` con `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `E2B_API_KEY`, `CEREBRAS_API_KEY`
- [ ] Confirmar tiempo bloqueado los 7 días
- [ ] Buy-in del creador: cada corte de §13 está OK
- [x] Push v4 al repo como `PLAN_v4.md` ✅ pending commit

---

## 16. PRIMER ACCIÓN (post v4 firmado)

1. ✅ Open questions §14 resueltas.
2. ✅ Commit + push `PLAN_v4.md` al repo `black-mirror-ai-civilization` (rename a `eidolon` pre-pitch).
3. **Día 1 task 1:** scaffold repo, FastAPI hello world, SQLite schema base. (~1h)
4. Reportar al final del Día 1 si va a tiempo o si hay que cortar más.

---

*Fin plan v4. Ejecutar este plan, no improvisar.*
