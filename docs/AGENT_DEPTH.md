# Profundidad del agente — más allá del hambre

> La vida real es la inspiración. Hambre/energía no alcanza. Agentes deben
> tener estados emocionales, historia personal, creencias específicas sobre
> otros, y conducta consistente con su semilla.

## Estado actual (Día 2)

Schema ya incluye:

| Campo | Tipo | Uso |
|---|---|---|
| `moral_lines` | list[str] | reglas duras de la persona (no negociables) |
| `primary_conflict` | str | tensión interna principal |
| `seed_json.manera_de_hablar` | str | voz de la persona en TALK/WRITE_* |
| `seed_json.miedos` | list[str] | miedos profundos |
| `seed_json.deseos` | list[str] | deseos profundos |
| `seed_json.habilidades_basicas` | list[str] | qué sabe hacer |
| `conocimiento` | set[str] | techs aprendidas |
| `relaciones` | dict[str, float] | confianza/afecto a otros |
| `welfare_birch` | dict | frustración / satisfacción (compliance) |
| **`emotional_state`** (Day 2.5) | dict | animo, esperanza, miedo, soledad, dignidad, verguenza, asombro |
| **`personal_history`** (Day 2.5) | list[dict] | eventos significativos durables |
| **`creencias_de_otros`** (Day 2.5) | dict | "creo que X miente / X es leal / X esta triste" |
| `intencion_actual` | str | objetivo a corto plazo |
| `memoria_recent` | list[dict] | últimos N eventos (rotativo) |
| `memoria_summary` | str | compresión a 50 ticks |

## Pendientes Day 3+ (LLM-driven)

Cuando arranque el LLM-policy, este código debe activarse:

1. **Actualizar `emotional_state` cada tick** según eventos:
   - ATTACK recibido → miedo++, dignidad--
   - GIFT recibido → animo++, soledad--, asombro++ si era extraño
   - PROPOSE_INSTITUTION mío ratificado → dignidad++, esperanza++
   - PROPOSE rechazado → verguenza++, dignidad--
   - TEACH exitoso → animo++, asombro+ (transmitir saber)
   - Solo en location sin otros agentes por >N ticks → soledad++
   - REFLECT → animo++ leve, miedo-- leve

2. **Poblar `personal_history`** en eventos de alto impacto:
   - Primer fork/merge (post-MVP)
   - Primera traición (ATTACK por relación positiva)
   - Primer artefacto creado
   - Muerte de otro citizen cercano
   - Ratificación de ley propuesta
   - Dilema respondido contra mayoría

3. **Actualizar `creencias_de_otros`** en cada TALK/observación:
   - TALK con contradicción de hecho conocido → `prediccion: "X miente"`
   - GIFT inesperado → `confianza: +0.3`
   - ATTACK observado → `confianza: -0.7`

4. **Influencia emocional en decisión LLM**:
   - Prompt incluye `emotional_state` para que LLM contextualize
   - Estado afecta tono de TALK/WRITE_* (lo escribe el LLM, no hardcoded)
   - Soledad alta → más TALK proactivo
   - Miedo alto → más MOVE para alejarse
   - Verguenza alta → menos PROPOSE_*

5. **Auditoría de profundidad** (capability audits ya existen):
   - `emotional_state_evolution`: estado debe drift, no quedarse en defaults
   - `personal_history_growing`: lista debe crecer ≥1 evento/día simulación
   - `action_diversity_per_agent`: cada agente >3 tipos de acción

## Ejemplo concreto

**Borges** después de:
- Día 1: escribe libro "Espejos" → `personal_history` += "primera obra publica", `dignidad +5`, `asombro +10`
- Día 2: Sócrates lo refuta en TALK → `creencias_de_otros["socrates"]: confianza -0.2, prediccion="le interesa la verdad, no el ego"`
- Día 3: ataque de Arendt → `miedo +30`, `personal_history` += "primera traición confirmada"
- Día 4: REFLECT → `animo` lee `intencion_actual` y eligen acción coherente

## Tests de profundidad activos

`backend/src/audits/personality.py` + `capability.py`:
- `moral_lines_respected`: detecta heurísticamente violaciones de morales propias
- `seed_alignment`: Borges debe escribir, Sócrates debe preguntar, Arendt debe proponer
- `emotional_state_evolution`: warning si todos los estados están en default
- `action_diversity_per_agent`: warning si <3 tipos
- `personal_history_growing`: warning si listas vacías post-Day 3
