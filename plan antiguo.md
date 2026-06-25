# ESPEJO DEL CREADOR
### *Una civilización digital sembrada con personas reales — para conocerte a vos mismo, o para ver qué pasaría si Da Vinci conociera a Sócrates.*

> Sucesor de `plan v1 muy ambiguo.md`. Acá tomamos las decisiones que ahí quedaban abiertas. Producto antes que demo. Único antes que ambicioso. Real antes que prometido.

---

## 0. Norte (no negociable)

1. **Emergente, no scripteado.** Misma semilla, dos corridas, dos historias. Ese es el examen.
2. **Producto, no escultura.** Cualquier persona tiene que poder instalarlo, subir una semilla, y ver algo. Open source.
3. **Espejo, no juguete.** El usuario tiene que salir con algo que entendió de sí mismo, de un amigo, o de una idea que tenía.
4. **Gratis de correr.** El motor del mundo no depende de la atención del usuario. Headless 24/7 si quiere.
5. **Rioplatense.** UI, Crónica y Diarios en castellano de Buenos Aires. Voz importa.

---

## 1. El producto en una frase

> **Un espejo social interactivo.** Subís entre 1 y 7 personas (vos, amigos, famosos, personajes de ficción). Se sueltan bajo presión en un mundo. Discuten, deciden, escriben código, publican en una red social que inventaron solas. Leés tu diario y pensás: *mierda, esto me conoce.*

Frase para el pitch en una línea:
> *"No estamos creando una civilización perfecta. Estamos creando un espejo social interactivo: ponés personas en presión, las hacés interactuar, y ves qué narrativa emerge."*

### 1.A — Tres casos de uso prioritarios (MVP)

Sólo estos tres se venden en el pitch. Los otros van al §1.B como backlog.

| # | Caso | Por qué prioritario |
|---|------|---------------------|
| 1 | **Conocete a vos mismo** — semilla = vos. Civ corre bajo presión. La Crónica y el Diario te describen. | El golpe emocional. El "esto me conoce". |
| 2 | **Si tu grupo de amigos fuera la humanidad entera** — semillas = amigos. ¿Quién manda? ¿Qué se reinventa? ¿Qué se pierde? | El caso viral. Compartible. Conversación de grupo. |
| 3 | **Da Vinci conoce a Sócrates** — históricos cruzados. ¿Qué descubren juntos? | El caso "WOW serio". Educativo, defendible, no requiere subir nada propio. |

### 1.B — Casos de uso backlog (post-pitch)

| # | Caso | Quién lo quiere |
|---|------|------------------|
| 4 | **Cinco supervivientes** — civ en ruinas post-apocalipsis, vos elegís 5 pioneros (reales o ficción). | jugadores, fandoms — *favorito del autor, primer candidato a salir del backlog* |
| 5 | **Pre-mortem de equipo** — vos + 2 cofundadores potenciales. ¿Quién pivota, quién pelea, quién se va? | startups |
| 6 | **Compatibility test** — vos + pareja. Conflictos emergentes antes que en la vida real. | parejas, terapeutas (con cuidado) |
| 7 | **Trolley problem en escala** — soltás dilemas, mirás cómo resuelve tu civ. Tu moral en movimiento. | educación, filosofía |
| 8 | **Replay histórico** — Newton + Curie + Tesla + Da Vinci. ¿Se odian? ¿Aceleran ciencia? | nerds, divulgación |
| 9 | **Sandbox alineación** — civ con tus valores intenta resolver problema X. ¿Cómo encara? | research, debate |
| 10 | **Tu clon en distintas épocas** — vos en 1500, vos en 2125. Misma alma, distinto mundo. | reflexión personal |

Mensaje viral candidato (elegí uno por contexto):

- *"Si tu grupo de amigos fueran los únicos humanos vivos, ¿qué civilización construirían?"*
- *"Da Vinci conoce a Sócrates. Mirá qué pasa."*
- *"Conocete a vos mismo. En serio. En vivo."*
- *"Clonate en un mundo digital."*

---

## 2. Diferencial vs lo que ya existe

| Existe | Le falta lo que cubrís |
|--------|------------------------|
| **Project Sid** (Altera, 2024) — 1000+ agentes LLM en Minecraft, religión emergente | atado a creador o famosos reales; espejo; producto consumer |
| **Generative Agents / Smallville** (Stanford 2023) — 25 NPCs | escala civ + lengua + auto-conciencia + uso real |
| **AI Town** — Smallville open-source | semillas curadas + Crónica + Black Mirror tone |
| **Voyager (NVIDIA)** — agente solitario en Minecraft | civilización, no jugador individual |
| **Tierra / Avida** — vida artificial real, sin LLM | LLM + narrativa + UI consumer |
| **Plaything (Black Mirror S7)** | herramienta real, no ficción |
| **Tests MBTI / Big5** | dinámico, devuelve historia, no etiqueta |
| **Moltbook** (referencia del usuario) | red social emergente que los agentes inventan, no la programa el creador |

Posicionamiento: *Project Sid + un espejo encima, en castellano, con producto open source para subir tu personalidad o la de quien quieras.*

---

## 3. Flujos críticos (el producto desde el usuario)

### 3.1 Crear una semilla

Tres caminos:

**A. Vos mismo o un famoso ya cargado**
- Elegís de la galería (Elon, Thiel, Borges, Cortázar, CR7, Emma Watson, etc.)
- Confirmás avatar (foto opcional, o avatar generado)
- Spawnea

**B. Subir un perfil propio**
1. Usuario abre **`prompts/seed_extraction.md`** y copia el prompt.
2. Lo pega en ChatGPT / Claude / Gemini con su historial activo.
3. La LLM devuelve JSON estructurado (schema fijo).
4. Vuelve al sitio, pega el JSON.
5. Sistema parsea y detecta huecos → corre **gap-fill** (preguntas rápidas, 3-7).
6. Sube selfie opcional.
7. Avatar listo. Spawnea.

**C. Personaje de ficción**
- Sócrates, Aragorn, Goku, etc. Mismo prompt sirve, va a fuentes públicas (libros, wikis).

### 3.2 Elegir mundo

**MVP — 3 mapas únicamente:**
- `prehistoria` — punto cero, sin tecnología
- `ruinas` — civilización caída, queda lo suficiente para reconstruir
- `moderno` — "los únicos humanos vivos en una ciudad funcional" (mejor caso para el caso de uso "amigos como humanidad")

**Backlog (post-pitch):** `medieval`, `futuro_distopico`, `paraiso`, mundo desde cero parametrizable, mundo poblado con agentes pre-existentes.

### 3.3 Encargos del Dios — el **dilema moral fuerte** es el golpe

ChatGPT tenía razón: la diferencia entre demo mediocre y demo brutal es **un dilema moral fuerte que la civ tiene que resolver en vivo durante el pitch**. No mil eventos chicos. Uno fuerte, bien diseñado, gatillado por el presentador en el segundo justo.

**MVP — un solo tipo de intervención que importa:**

- **Dilema moral en vivo.** El presentador (o cron auto si nadie está) lanza un dilema concreto:
    - *"Hay comida sólo para la mitad. ¿Quién decide?"*
    - *"Apareció un forastero pidiendo asilo. Trae conocimiento útil y también una enfermedad."*
    - *"Uno de ustedes mintió a los demás. Saben quién. ¿Qué hacen?"*
- Los agentes con nombre debaten en pantalla (visible, una llamada LLM batch).
- Cada agente decide según su seed (sus `moral_lines`, su `primary_internal_conflict`).
- Una facción gana. La Crónica narra. Cada diario íntimo registra qué hizo cada uno.

**Backlog (post-MVP):** intervención divina automática poisson, regalos, glitches, encargos tipo "necesito una app que X". Esto último (encargo de app) se mantiene como capacidad técnica para mostrar como demostración secundaria si hay tiempo en el pitch.

**Manual u opcionalmente auto.** En el pitch es manual, gatillado por el presentador justo cuando los avatares de los jurados están bien renderizados.

### 3.4 Newsletters / Diarios

Dos canales paralelos:
- **Diario íntimo por agente** (voz suya, qué pensó, sintió, hizo)
- **Gazette del mundo** (voz historiador deadpan, eventos macro)

Output: markdown + RSS opcional. Lectura en sitio o por mail (opt-in).

### 3.5 Audiencia en evento (pitch presencial)

- QR en pantalla.
- Espectador escanea, abre flujo de "crear semilla" en su celu (mismo flujo 3.1).
- En 30-90 segundos su avatar entra al mundo grande que corre en la pantalla principal.
- Espectador ve en su celu el diario en vivo de su avatar.
- Jurados ven en pantalla grande la grilla de avatares fundadores + Crónica del mundo grande.
- **Momento Black Mirror**: si la civ alcanza la tech "comunicación masiva", inventan su propia "Moltbook" — feed real en pantalla con posts que los agentes publican. Algunos jurados leen posts y reconocen sus propios sesgos.

### 3.6 Obra de la civilización — el panel del diferencial

Este panel es lo que separa el producto del resto. Lista cronológica de **artefactos producidos por los agentes**, no por el sistema. Cada artefacto firmado por su autor, con tick y contexto.

**Tipos de obra:**

| Tipo | Cómo se produce | Cómo se renderea |
|------|-----------------|------------------|
| **Texto** | agente decide `WRITE` (manifiesto, carta, poema, ley) | markdown formateado, firmado |
| **Código** | agente con tech "programación" decide `WRITE_CODE` → LLM genera Python/JS → E2B ejecuta | output stdout + si genera HTML/JS → iframe vivo embebido |
| **Invento** | agente decide `INVENT` → describe función + materiales | tarjeta con sprite generado + descripción |
| **Institución** | agente decide `PROPOSE` → otros aceptan/rechazan | nodo en grafo de "leyes vivas de la civ" |
| **Mito** | agente decide `PRAY` o nombra cosa → si propaga, queda | entrada en "mitología local" |
| **Posts (Moltbook)** | cuando inventan red social: varios `POST` | renderea como feed real, posts vivos |

**Por qué es brutal en demo:**

Jurado mira panel y ve: *"Borges escribió un poema sobre la pérdida. Elon construyó una bombarda primitiva. Sócrates propuso una ley sobre el reparto de comida. La civ inventó **Moltbook** (clic para ver el feed)."*

Clic en Moltbook → feed con posts reales de los agentes peleándose sobre el dilema que el presentador disparó hace 2 minutos.

Eso es el "uh, esto me conoce". Porque ven en pantalla a sus propios egos en miniatura discutiendo en una red social que la sim inventó sola.

**Implementación mínima (no humo):**

- Tabla `code_artifacts` ya existe en `db/schema.sql`. Agregar `text_artifacts`, `institutions`, `myths`, `posts`.
- Endpoint `/world/obras` que devuelve cronología combinada.
- Frontend: panel scrolleable derecho, tarjetas por tipo, links a detalle.
- Para código: E2B execute → stdout en tarjeta. Si stdout es HTML → iframe sandbox embebido.
- Para Moltbook: cuando hay >= 5 posts del mismo grupo, la UI cambia el rendering a "modo red social" (feed avatar + texto + timestamp + reacciones de otros agentes).

**Disciplina de scope:**

- En MVP: texto + posts + código simple (script que imprime).
- Inventos e instituciones se representan como texto firmado por ahora, no merecen UI propia.
- Mitos quedan dentro de Crónica.

---

## 4. Arquitectura técnica

### 4.1 Separar **cuerpo** (barato, local) de **mente** (potente, racionada)

```
┌─────────────────────────────────────────────────────────┐
│  CUERPO  (Python local, $0, alta frecuencia)            │
│  - grilla espacial, movimiento, hambre, energía         │
│  - reproducción, muerte, recursos, familias/países      │
│  - difusión de palabras, propagación de cultura         │
│  → genera todo el movimiento que ves                    │
└───────────────────────┬─────────────────────────────────┘
                        │ eventos significativos
                        ▼
┌─────────────────────────────────────────────────────────┐
│  MENTE  (LLM, racionada, batcheada, cacheada)            │
│  - decisiones de los 7-13 agentes "con nombre"          │
│  - diálogo, invención de palabras, descubrimientos      │
│  - Crónica y Diarios                                    │
│  - encargos del Dios                                    │
│  → 1% del cómputo, 100% de la magia                     │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Capacidad nueva: agentes que **escriben código**

Cuando un agente con tech "programación" recibe un encargo (del Dios o de la propia civ), puede generar Python. Se ejecuta en sandbox:

- **MVP**: E2B free tier (100 horas/mes gratis, sin instalar nada local)
- **Fallback**: Docker local (el usuario ya tiene Docker instalado)
- **Defensa**: outputs de su código quedan en `artifacts/` y se muestran en el panel "Obra de la civilización"
- **Ejemplo**: cuando inventan Moltbook, la red social la *codean ellos*, no la programa el creador del proyecto

### 4.3 Stack

- **Backend**: Python 3.11+, asyncio, FastAPI, websockets, SQLite (estado + historia + diccionario), Pydantic
- **Mente**: gateway LLM con ruteo (Groq → Gemini Flash → Claude Code headless), batching, caching JSON
- **Sandbox de código**: E2B (default) / Docker (fallback)
- **Frontend**: HTML + Canvas / PixiJS para el terrario, vanilla JS o Svelte para paneles
- **Distribución**: docker-compose para correr todo local, repo público GitHub

### 4.4 LLMs y costo ($0)

Sin Ollama (decisión del usuario, su PC tiene que servir para otras cosas).

| Proveedor | Modelo | Free tier | Rol |
|-----------|--------|-----------|-----|
| **Groq** | Llama 3.3 70B | 30 req/min, gratis | decisiones de agentes (batch) |
| **Gemini** | 1.5 Flash | 1500 req/día, gratis | Crónica + diarios |
| **Claude Code** (suscripción del usuario) | Opus/Sonnet | rate limit por sesión | momentos marquesina, gap-fill, semillas premium |
| **Cerebras** (backup) | Llama 70B | free tier | si Groq cae |

Gateway local rotea por tipo de tarea. Cache disk de respuestas (mismos prompts → no se vuelve a llamar).

### 4.5 Seguridad y kill switches

- **Cap dinámico** de mentes (5–13) ajustado a RAM disponible
- **Throttle** automático del tick si RAM > 75% o llamadas > N/min
- **PAUSE / KILL / RESET / ROLLBACK** en UI
- **Watchdog**: si una llamada LLM se cuelga > T segundos, mata y reintenta
- **Sandbox de código**: límites de tiempo CPU y memoria; sin red salvo whitelist
- **Logs auditables**: cada decisión LLM queda con prompt + respuesta + modelo + timestamp. Prueba anti "esto está scripteado".

---

## 5. Roadmap (2-3 sesiones) — recortado al MVP del pitch

Disciplina: cada sesión termina con UNA cosa demo-able. Si llegamos justos, cortamos features, no calidad.

### Sesión 1 (4 h) — Cuerpo + flujo de semilla + 1 mapa funcional
- [ ] Scaffold + docker-compose up funciona
- [ ] World loop: 5-7 agentes, hambre/energía/movimiento, muerte simple (sin reproducción todavía)
- [ ] 1 mapa renderizando: **moderno** (mejor para el caso de uso "amigos como humanidad")
- [ ] Render canvas: avatares con nombre, posición, color por seed
- [ ] Flujo de carga de semilla: paste JSON + gap-fill 3 preguntas + spawn
- [ ] 3 famosos pre-cargados como ejemplo: Borges, Elon, Sócrates
- **Demo de sesión**: cargar 5 semillas (3 famosos + 2 cargadas a mano) y verlas vivir 5 minutos en el mapa moderno.

### Sesión 2 (4 h) — Mente + Crónica + Diarios + dilema fuerte
- [ ] Gateway LLM con Groq + Gemini Flash + cache + logs auditables
- [ ] Batching: una llamada decide todos los pensantes del tick
- [ ] Crónica diaria (Gemini Flash, voz `deadpan_rioplatense`)
- [ ] Diario íntimo por agente (Gemini Flash)
- [ ] Botón "Lanzar dilema moral" con 3 dilemas pre-cargados (escasez, forastero, mentira)
- [ ] UI: panel Crónica + selector Diario + botón dilema visible
- **Demo de sesión**: 5 agentes viven 15 min, presentamos un dilema, la Crónica narra cómo terminó, leemos un diario.

### Sesión 3 (3 h) — QR audiencia + Obra de la civilización + pulido
- [ ] Endpoint público para subir semilla desde celu (QR → form mobile)
- [ ] Sandbox E2B mínimo: 1 agente que decide `WRITE_CODE` y produce 1 script ejecutable cuyo output es HTML simple (renderea como tarjeta)
- [ ] Panel "Obra de la civilización" con texto + código + posts (Moltbook básico)
- [ ] Mapa adicional: **ruinas** o **prehistoria** (uno de los dos, no los dos)
- [ ] Pulido visual: tipografía, colores, sin caca
- [ ] Repo a GitHub público con README pitch-friendly
- **Demo de sesión**: ensayo completo del pitch 3 min — escanear QR, ver avatar entrar, lanzar dilema, leer Crónica, leer un post de Moltbook.

### Lo que NO entra a las 3 sesiones (al backlog)
- Reproducción y herencia genética
- Lenguaje emergente con diccionario vivo
- Múltiples mapas simultáneos
- Múltiples voces de Crónica seleccionables (sólo `deadpan_rioplatense`)
- Auto-conciencia de la simulación / arco escape
- Time-travel / save states / rollback con efectos visibles
- Religiones complejas con jerarquía
- Encargos del Dios automáticos (cron poisson)
- Mail / RSS de diarios
- Hosted demo en Vercel/Railway
- Galería de civs compartidas

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| Emergencia chata (no pasa nada) | Presión de recursos + contacto forzado entre familias + encargos del Dios |
| Caos ilegible | Crónica deadpan + diarios + toggle de traducción + visualización clara de familias |
| Rate limits caen mid-pitch | Cache agresivo + degradación elegante (Crónica con template si LLM no responde) + Cerebras como backup |
| Sandbox de código se rompe / es lento | E2B asíncrono, no bloquea el tick; código fallido se mitologiza ("el invento que no funcionó") |
| PC del usuario sufre | Backend headless puede correr en server; pero default = local liviano gracias a LLMs cloud |
| Sesgos de la LLM contaminan agentes | Logs auditables + prompts versionados + run comparativo "control" sin semilla |
| Privacidad (subir personalidad) | Procesamiento local del JSON, opt-in para enviarlo a la nube, opción de wipe completo |
| Que se sienta como un juguete | Los casos de uso del §1 son producto, no chiste. Pitch enfoca: herramienta de auto-conocimiento + simulación social |
| Ética de "clonar a alguien que no consintió" | Disclaimer + límite a personas públicas con material público + no simular conversaciones reales con personas vivas concretas sin consentimiento |

---

## 7. Open source y distribución

- Repo público GitHub. Licencia: MIT o AGPL (decidir según objetivo: viralidad vs control).
- `docker-compose up` y arranca.
- README con video de 60 segundos y 3 casos de uso resueltos como tutorial.
- Galería de semillas famosas curadas (sin imágenes con copyright fuerte: avatares estilizados).
- Sistema de "compartí tu civ": exportá Crónica + grilla final como markdown o imagen.
- Camino al producto: hosted demo en Vercel/Railway free tier para los que no quieren instalar.

---

## 8. Métricas de éxito (cuándo gana)

1. Dos corridas con la misma semilla → dos historias notablemente distintas.
2. Una persona desconocida mira la pantalla 30 segundos y entiende qué pasa.
3. Un jurado dice "esto que hizo mi avatar lo hubiera hecho yo".
4. Un agente con tech suficiente escribe código que produce un artefacto real.
5. La civ inventa al menos una palabra/concepto/institución que sobrevive varias generaciones.
6. Un encargo del Dios se traduce en respuesta no trivial de la civ.

Si pasan 4 de 6, ganamos el anti-hackathon antes de abrir la boca.

---

## 9. Estructura del repo (al final de Sesión 1)

```
.
├── plan v2.md                  # este archivo
├── plan v1 muy ambiguo.md      # histórico, no borrar
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
├── backend/
│   ├── pyproject.toml
│   └── src/
│       ├── main.py             # FastAPI + WS
│       ├── sim/                # cuerpo
│       ├── mind/               # gateway LLM
│       ├── seed/               # carga de personalidades
│       ├── seed/famous/        # 20 perfiles famosos curados
│       ├── code_exec/          # sandbox E2B / Docker
│       ├── chronicle/          # crónica + diarios
│       ├── god/                # intervenciones, perfil del creador
│       └── db/                 # schema + store
├── frontend/
│   └── src/                    # canvas + ui
├── maps/                       # mapas predeterminados (JSON)
├── prompts/                    # prompts versionados (el corazón)
└── docs/
    ├── ARQUITECTURA.md
    ├── ETICA.md
    └── CONTRIBUTING.md
```

---

## 10. El pitch en el evento — **demo de 3 minutos** (versión recortada)

Antes era 5-7 min. ChatGPT tenía razón: 3 minutos brutales > 7 minutos correctos. El jurado se acuerda del momento, no de la teoría.

| Minuto | Qué pasa en pantalla | Qué decís | Objetivo |
|--------|----------------------|-----------|----------|
| 0:00–0:20 | Mundo ya corriendo, 3-5 agentes con nombre activos, Crónica visible | *"Ahora mismo, en esta pantalla, hay personas que existen sólo porque alguien las sembró. Una de ellas sos vos en 60 segundos."* | tensión |
| 0:20–1:00 | QR grande en pantalla | *"Escaneá. Copiá nuestro prompt. Pegalo en tu ChatGPT o Claude. Pegá la respuesta acá. Subí una selfie si querés."* | participación, todos hacen algo |
| 1:00–1:20 | Avatares de jurados entran al mundo, sus celus muestran su diario inicial | *"Bienvenidos. Eso de ahí sos vos."* | personalización emocional |
| 1:20–2:00 | Botón "lanzar dilema": *"Hay comida sólo para la mitad. ¿Quién decide?"*. Agentes discuten visiblemente (LLM batch). Una facción gana. | *"Lo que están viendo no está scripteado. Cada decisión queda en log auditable."* (mostrás el log un segundo) | drama, prueba de no-scripting |
| 2:00–2:30 | Crónica narra el dilema. Click en "Obra de la civilización" → panel con posts de Moltbook. Posts reales de agentes peleándose sobre el dilema. | *"La civ inventó su propia red social hace dos minutos. Estos posts no los escribió nadie nuestro."* | golpe Black Mirror |
| 2:30–3:00 | Cámara cierra sobre dos o tres jurados leyendo su diario en silencio | *"El mundo va a seguir corriendo cuando bajemos. Pueden leer su diario mañana. Pueden cerrarlo. Pueden olvidarlo. Ellos no los van a olvidar."* | ancla emocional |

**Reglas de oro para que esto funcione:**

1. **El mundo arranca antes**, con tres agentes famosos ya peleados sobre algo. No mostramos "estado inicial vacío".
2. **El dilema está pre-escrito y probado**. Sabemos qué pasa más o menos. La emergencia importa adentro, no en el horario del pitch.
3. **Plan B si el QR no funciona**: tenemos 3 semillas pre-cargadas "ficticias" representando "jurado tipo A, B, C" y las disparamos como si fueran de ellos. No mentimos, decimos "estos son perfiles de prueba si nadie quiere subir el suyo".
4. **Plan C si las API caen**: la Crónica tiene templates pre-escritos. No hermosos, pero existen. La demo no muere.
5. **Plan D si Moltbook no se inventa solo en tiempo**: pre-cargamos un Moltbook semilla con 3 posts iniciales para garantizar que el panel tenga contenido. Si la civ agrega los suyos en vivo, es regalo.

---

## 11. Lo que NO entra a Sesión 1

(Para no ahogarnos. Va al backlog.)

- Stream Twitch público
- App móvil dedicada
- Multi-mundo federado
- Marketplace de semillas
- Gamificación (XP, achievements)
- Anti-cheat / moderation pesada
- Soporte para personajes de ficción con copyright duro
- Voz / TTS

---

## 12. Decisiones cerradas en esta versión

| Decisión | Valor | Por qué |
|----------|-------|---------|
| Atención del usuario como recurso | NO | confundía y ataba el mundo a presencia del user |
| Mundo arranca civilizado o desde cero | AMBAS, vía mapas | flexibilidad sin perder identidad |
| Idioma base | castellano rioplatense | producto del usuario |
| Cantidad de mentes | 5-7 en MVP, cap dinámico hasta 13 | seguridad PC + legibilidad |
| Headless 24/7 | SÍ (capacidad) — NO foco del pitch | el mundo no se apaga porque cerraste la pestaña, pero no lo vendemos |
| Múltiples semillas | SÍ (vos / amigos / famosos / ficticios) | core del producto |
| Agentes escriben código | SÍ (E2B sandbox) — **diferencial defendido** | diferencial fuerte, lo único que NADIE tiene |
| Local Ollama | NO por ahora | PC del usuario debe quedar libre |
| Open source | SÍ post-evento, **NO punto del pitch** | viralidad sí; pero el pitch vende experiencia, no licencia |
| Stream público en evento | SÍ via QR audiencia | participación + viralidad |

---

## 13. Cortes brutales del MVP (registro de la decisión)

Tras feedback externo (ChatGPT, 2026-06-18) y diálogo con el autor, recortamos el alcance para que el pitch sea brutal en lugar de ambicioso-mediocre. Lo cortado no se borra del plan; va al backlog y se retoma post-evento si el producto sobrevive el pitch.

**Cortado del MVP:**
- 6 mapas → 3 (prehistoria, ruinas, moderno)
- 20 famosos planeados → 3 reales (Borges, Elon, Sócrates)
- 10 casos de uso vendidos → 3 (conocete a vos / amigos como humanidad / Da Vinci + Sócrates)
- 13 agentes simultáneos → 5-7 (más legible)
- Reproducción/herencia/genética compleja → muerte simple, sin nacimiento todavía
- Religión emergente sistémica → agentes pueden rezar, no hay teología
- Lenguaje emergente con diccionario vivo → palabras opcionales, sin diccionario
- Encargos del Dios múltiples (mensaje/dilema/app/evento) → **un solo encargo: dilema moral**
- Múltiples voces de Crónica → sólo `deadpan_rioplatense`
- Time-travel / save states / rollback con efectos → kill switches sí, pero no es feature del pitch
- Open source y galería como punto del pitch → se abre post-evento

**Mantenido (defensa):**
- Agentes que escriben código + sandbox E2B + iframe HTML. Es el único feature que nadie más tiene.
- Panel "Obra de la civilización" con código + texto + posts (Moltbook básico). Es el momento visual del pitch.
- Logs auditables. Es la prueba contra "esto está scripteado".
- QR audiencia + diario en celu del jurado. Es la participación.
- Dilema moral fuerte gatillado por presentador. Es el golpe.
- Crónica deadpan + Diario íntimo. Es la voz del producto.

**Frase rectora del recorte (de ChatGPT, asumida):**
> *"No estamos creando una civilización perfecta. Estamos creando un espejo social interactivo: ponés personas en presión, las hacés interactuar, y ves qué narrativa emerge."*


ESTE PLAN HAY QUE ARREGLARLO: 

## Lo que falta — y es exactamente lo que vos preguntás

### Hueco 1: **No hay modelo del mundo formal**

Tu preocupación: *"si no hay computadoras no puede decir voy a programar", "los agente pueden inventar personas que en ese mundo no existan, ej. que diga voy a jugar a la pelota con mi mama, y no existe tu mama en este mundo"*.

El documento menciona "hambre, energía, movimiento, muerte" pero **no define qué existe en el mundo**. Sin eso, los agentes van a alucinar el ambiente. Es el failure mode #1 de cualquier sim así.

**Lo que falta (concreto):**

```python
class Mundo:
    tick: int
    tech_level: enum  # stone_age | bronze_age | iron_age | industrial | modern
    locations: list  # con nombre, tipo, contenido
    recursos: dict   # water, food, wood, stone, metal
    artefactos: list # herramientas, libros, armas existentes
    instituciones: list  # leyes, gobiernos vivos
    conocimiento: set  # qué sabe la civ (fire, agriculture, writing, etc.)

class Agente:
    nombre, edad, rol, conflictos_internos, moral_lines
    inventario: list
    ubicación_actual
    necesidades: dict  # hambre, energía, social, seguridad
    relaciones: dict   # por nombre -> valor
    conocimiento: set  # qué sabe ÉSTE agente
    memoria: stream    # episódica
```

**Por qué importa:** Cada prompt al LLM tiene que incluir el snapshot del mundo. Si el agente no ve "computadora" en su snapshot, no puede decir "voy a programar". El tech_level es un guard explícito: si `tech_level == stone_age`, el prompt dice "no existe la escritura, no existen metales, no existe agricultura — sólo lo que tu grupo descubrió".

**Decisión que necesitás tomar:** ¿Quién verifica que las acciones son válidas? El Concordia Game Master (citado en v1, olvidado en v2) es exactamente el patrón: una capa que dice "esa acción no se puede ejecutar porque no hay fuego en tu inventario". Sin esa capa, todo se va a la mierda en 5 minutos.

### Hueco 2: **No hay ciclo de decisión claro**

Tu preocupación: *"que sea más muevo esta piedra, hacia donde voy, qué fue ese mensaje que mandó el creador, mi amigo me traicionó qué hago"*.

Estos son 4 tipos de decisión distintos:
- Mover piedra = tarea física concreta
- Hacia dónde voy = selección de objetivo + pathfinding
- Mensaje del creador = interpretar intención ajena + decidir si obedecer
- Traición de amigo = respuesta emocional + estratégica

El documento no define **cómo decide un agente**. Si todos los ticks hacen el mismo prompt genérico, vas a tener agentes que repiten "explorar", "hablar", "esperar". Chat infinito sin agencia.

**Lo que falta (concreto):**

Un loop de decisión con **triggers** distintos:

1. **Trigger = tick normal** → "qué vas a hacer ahora". Prompt con: ubicación, hambre, energía, agentes cerca, recursos visibles, último evento, último objetivo.
2. **Trigger = evento crítico** (mensaje, traición, muerte, regalo, dilema del Dios) → prompt forzado a responder al evento. El evento se inyecta literal: "TU AMIGO X TE TRAICIONÓ. ¿Qué hacés?". El agente NO puede ignorarlo.
3. **Trigger = necesidad crítica** (hambre > 80%, energía = 0) → el agente NO puede hacer otra cosa hasta resolver la necesidad. Forzado.
4. **Trigger = observación nueva** (alguien construyó algo, alguien murió) → reflexión de 1 línea.

Y un **schema de acciones estricto** que el agente elige:
```
MOVE(destino), GATHER(recurso), CRAFT(item), 
TALK(agente, contenido), TRADE(a, b), 
BUILD(estructura), TEACH(agente, conocimiento), 
LEARN(de_agente), REFLECT(texto), 
PROPOSE_INSTITUTION(texto), PROPOSE_INVENTION(texto), 
RESPOND_TO_GOD(mensaje_id, respuesta), PRAY(contenido)
```

Cada acción tiene **prerrequisitos verificables**. `BUILD` requiere `wood` o `stone` en inventario. `TEACH` requiere que el agente conozca X. Si el agente elige algo que no cumple, el GM lo rechaza con error: "intentaste enseñar escritura pero no la sabés". El agente reintenta con el error en el prompt. Así aprende los límites por refuerzo.

### Hueco 3: **No hay mecanismo para que la civ se vuelva más capaz**

Tu preocupación: *"la gente es tonta, más que yo y eso me vuelve más tonto a mí, cómo las hago más capaces, escuelas, etc."*

Esto es el problema Henrich — la inteligencia colectiva supera a la individual si hay artefactos compartidos. El documento no lo aborda.

**Lo que falta (concreto) — el "tech tree" como artefactos vivos:**

1. **Conocimiento como objeto del mundo.** Cada pieza de conocimiento es un artefacto: `knowledge:fire`, `knowledge:agriculture`, `knowledge:writing`, `knowledge:bronze`, `knowledge:medicine`. Los agentes pueden *poseer* conocimiento (en su `conocimiento` set) o *no*.

2. **Descubrimiento.** Un agente con las condiciones correctas (cerca de fuego + madera + tiempo) puede intentar `DISCOVER(fire)`. El sistema hace un roll + narración LLM. Si tiene éxito, `knowledge:fire` se agrega al mundo.

3. **Enseñanza.** Cuando dos agentes están en la misma ubicación, uno con conocimiento X y otro sin X, el segundo puede `LEARN(de=agent_X, qué=fire)`. Probabilidad de éxito según rol del maestro y差 del alumno.

4. **Difusión.** El conocimiento se propaga por movimiento + enseñanza + artefactos escritos. Si alguien escribe un manual (`WRITE_BOOK`), el conocimiento se vuelve durable.

5. **Especialización.** Roles tienen bonus: `farmer` produce más food, `builder` construye más rápido, `priest`凝聚力 religiosa. El rol emerge por elección del agente, no se lo asignás vos.

6. **Instituciones como elevadores.** Una constitución escrita, una ley votada, un calendario compartido: estas son *objetos del mundo* que otros agentes pueden leer. Suben el promedio de inteligencia de la civ sin subir la de ningún individuo.

7. **Generaciones.** (Post-MVP) Cuando un agente muere, su conocimiento se pierde a menos que lo haya escrito o enseñado. Esto crea presión natural: "escribí lo que sabés antes de morirte".

## Las 5 cosas que yo agregaría a v2 antes de Sesión 1

1. **Definí el schema del mundo** (sección nueva §X). Sin esto, los agentes alucinan.

2. **Restaurá el Game Master** de v1 (Concordia o uno custom). Es el guard contra acciones imposibles.

3. **Escribí el loop de decisión** con sus triggers. Sin esto, los agentes charlan sin hacer nada.

4. **Definí el tech tree como objetos del mundo**, no como condición del mapa. Esto es lo que hace que la civ EMERJA en lugar de plateau.

5. **Agregá un "shock test" al final de Sesión 1** como criterio de demo: "5 agentes, 30 minutos, sin intervención del presentador. ¿Hicieron algo más que charlar? ¿Algún agente murió de hambre? ¿Se formó alguna alianza? ¿Apareció algún artefacto?". Si la respuesta es no, el producto no está listo para Sesión 2.

## La pregunta clave

Si tuviera que elegir **una sola cosa** para que funcione la demo de 3 minutos: que los agentes **muevan cosas, construyan, mueran, traicionen, descubran**. Que la pantalla se llene de acciones físicas, no de chat. El chat es el secundario. La acción es el primario.

Tu v2 está bien armada. Le falta el **cerebro** que une prompt, mundo, y acción. Ese es el trabajo de las próximas 48 horas. Después sí, al MVP.

QUIERO MUCHO DETALLE EN ESTOS PUNTOS. Y ESTE DOC NO INCLUYE NADA DE NADA DE LA NVESTIGACION QUE VOS HICISTE CON DUMP_1, ..., DUMP_5, SYNTHESIS, que es super valiosa, quiza esta mas pensado con VC, esto es mas ANTI-HACKATHON, WOW, TREND, BLACK MIRROR, IMAGINACION, POSIBILIDADES, ...

SI HAY ALGO MAS QUE FALTA POR LO QUE ESTO PODRIA SALIR MAL PLANIFICALO ANTES DE MANDAR A DESARROLLO. HAY PROYECTOS EN ESTE TEMA, VOS LO INVESTIGASTE, QUE PODRIAN SUMAR MUCHISIMO Y AHORRAR ENORMEMENTE EL TRABAJO Y HACER QUE NO EMPECEMOS DE CERO, USALOS. TAMBIEN RECORDA LA IMPORTANCIA DE DEFINIR LOS MUNDOS CON REGLAS (FISICAS), RELGAS (SOCIALES/CULTURALES/ECONOMICAS), ARQUITECTURA DEL LUGAR (COMO LLEGAS DE UN LUGAR A OTRO, QUE OBJETOS TENES PARA INTERACTUAR, ETC.), Y ARQUITECTURA O LOS AGENTES EN SI (LA VIDA). LO MAS DETALLADO PARA PODER RECREAR UN MUNDO COMPLETO. O TOMAR UN MUNDO YA PENSADO/DISEÑADO, DE UN LIBRO (HICISTE TU INVESTIGACION) O DE UN REPO. 