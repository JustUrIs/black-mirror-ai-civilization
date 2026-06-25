# AI Civilization Tech Stack

**A runnable-stack technical survey for building digital civilizations of autonomous AI agents — emergent agents with memory, goals, social dynamics, economy, and evolution.** Current as of June 20, 2026. Where a specific datapoint (stars, last commit, exact license) could not be confirmed in-session, it is marked **"unknown — search [X]"** rather than guessed. GitHub star counts are volatile snapshots, not live figures.

## TL;DR
- **There is no single "civilization engine" — you assemble one from three layers: an agent-cognition framework (Generative Agents / AI Town / Concordia / PIANO), a world engine (AI Town's pixi+Convex, Minecraft+Mineflayer, Mesa, or a game engine), and an LLM-serving backend (vLLM or SGLang).** The best-proven, fastest-to-prototype combination is **AI Town (MIT) + Ollama/vLLM + local Qwen3/Llama**, runnable in a day; the highest-emergence published result is **Altera's Project Sid / PIANO architecture in Minecraft at 500 agents on GPT-4o-class models**.
- **The dominant constraint is LLM cost, not the world engine.** A 100-agent, 1,000-tick run with one frontier API call per agent per tick is roughly 150M tokens (~$750–2,250 at GPT-4-class prices); the field's answer is small local models served with prefix-sharing (SGLang's RadixAttention) so a shared world-prompt is computed once. Design for this from day one.
- **If you want true open-endedness without LLMs, the canonical path is a quality-diversity evolutionary stack** — Lenia/Flow Lenia or ALIEN as substrate, NEAT/HyperNEAT or QD (MAP-Elites/POET) for cognition, novelty search for divergence. These genuinely *invent* novelty but don't "reason"; LLM agents reason but mostly *imitate* human institutions rather than inventing them de novo (Project Sid's own stated limitation).

## Key Findings
1. **The 2023 Generative Agents memory–reflection–planning loop is still the reference architecture** for emergent social towns, and AI Town is its production-grade, MIT-licensed, deployable reincarnation.
2. **Project Sid's PIANO architecture is the state of the art for many-agent civilization** (specialized roles, constitutional voting via Google Docs, meme/religion propagation, taxation), but 1,000+ agents exceeded Minecraft server limits; 500 was the stable analyzed scale, and real progress required GPT-4o.
3. **Memory is a stack, not a database.** Raw vector DBs (Chroma/Qdrant/Weaviate/LanceDB) are ANN stores that "know nothing of time, contradiction, or relevance"; purpose-built layers (Letta/MemGPT, Zep, Mem0) add episodic/semantic/procedural structure on top.
4. **Serving choice is a 10× lever.** vLLM and SGLang sustain 100% success at 128 concurrent requests; Ollama (great for dev) is ~10× slower and broke down at that concurrency — never ship a multi-agent civ on Ollama.
5. **MMO economy postmortems are the best design canon for agent economies** — EVE's faucet/sink balancing, OSRS gold sinks, Diablo III's failed Real-Money Auction House, and Ultima Online's player-destroyed ecology all teach the same lesson: any exploitable system *will* be exploited.
6. **Open-endedness has a mature toolbox** (MAP-Elites, POET, novelty search, NEAT, QD in JAX via QDax) plus a new LLM-guided frontier (OMNI, Sakana's ASAL and evolutionary model-merge).

## Details

## A. Agent Frameworks

### Generative Agents (Park et al., "Smallville")
- **Link:** github.com/joonspk-research/generative_agents; paper arXiv:2304.03442 (UIST 2023 Best Paper)
- **License / Cost:** Apache-2.0 on the research repo (unknown — search exact LICENSE file); cost is OpenAI API tokens. The repo authors note runs "could be somewhat costly" with GPT-3.5 as of early 2023 (no exact dollar figure published — unknown, search Park et al. cost appendix).
- **Primitive provided:** The canonical loop — a time-stamped **memory stream** scored by recency/importance/relevance; **reflection** (periodic synthesis of high-level insights); **planning** (decomposing days into actions). World represented as a tree (world → areas → objects).
- **Best for:** The reference design for any emergent social town — information diffusion, relationship formation, emergent coordination (the spontaneous Valentine's party).
- **Limits:** Research code, not a maintained library; tied to a fixed 25-agent Tiled map (adding agents means editing the map); expensive; no economy/evolution primitives; widely cited and foundational but breaks at scale.

### AI Town (a16z-infra)
- **Link:** github.com/a16z-infra/ai-town
- **License / Cost:** MIT. Free locally with Ollama (llama3 + mxbai-embed-large); or cloud LLM (OpenAI/Together) at API cost. Backend is Convex (shared global state, transactions, simulation engine); frontend is pixi-react with historical replay buffers.
- **Primitive provided:** Production-grade TS/JS reimplementation of the generative-agents loop with persistence and multiplayer capability.
- **Best for:** The fastest path to a deployable, hackable browser town; the default "minimum viable civ" substrate.
- **Limits:** Convex dependency is a design lock-in; tuned for a small town, not thousands of agents; no built-in economy/evolution.

### Project Sid / PIANO (Altera)
- **Link:** github.com/altera-al/project-sid; paper arXiv:2411.00114
- **License / Cost:** Repo is primarily the technical report (unknown — search whether full agent code/license is released). Founder Robert (Guangyu) Yang (ex-MIT). Altera raised **more than $11 million** (investors including a16z and Eric Schmidt's First Spark Ventures; seed co-led by First Spark and Patron, per TechCrunch/MIT Technology Review).
- **Primitive provided:** **PIANO (Parallel Information Aggregation via Neural Orchestration)** — concurrent modules (speaking, planning, social awareness, action) running in parallel through a coherence bottleneck, enabling real-time multi-stream behavior; civilizational benchmarks inspired by human history.
- **Best for:** The largest published demonstration — the paper states "10 – 1000+ AI agents" in Minecraft; emergent merchant hubs, constitutional voting, meme/religion (Pastafarianism) propagation, and taxation.
- **Limits:** 1,000+ agent runs exceeded Minecraft server constraints (agents went "sporadically unresponsive"); 500 was the analyzed stable scale. Agents lack vision/spatial reasoning and innate drives (survival, curiosity, community); because they inherit human priors from the base LM, they "cannot simulate de novo emergence" of democratic systems, fiat economies, or communication systems. Required GPT-4o.

### Voyager (MineDojo)
- **Link:** github.com/MineDojo/Voyager; paper arXiv:2305.16291; voyager.minedojo.org
- **License / Cost:** MIT. GPT-4 API (originally); requires a Minecraft instance + Fabric mods + Mineflayer.
- **Primitive provided:** **Lifelong skill learning** — an ever-growing, embedding-indexed library of executable code skills; automatic curriculum; iterative prompting with environment feedback + self-verification (a form of in-context novelty search).
- **Best for:** Single-agent embodied open-ended learning; the skill-library pattern transfers to any civ agent that must accumulate know-how. Reported 3.3× more unique items, 2.3× longer travel, and tech-tree milestones up to 15.3× faster than prior SOTA.
- **Limits:** Single-agent (no native society); GPT-4 dependent; Minecraft-specific harness.

### Concordia (Google DeepMind)
- **Link:** github.com/google-deepmind/concordia; paper Vezhnevets et al., 2023; ~1.3k stars
- **License / Cost:** Apache-2.0. Any LLM API + a text embedder; cost = tokens.
- **Primitive provided:** **Game-Master pattern from tabletop RPGs** — a GM entity grounds free-text agent actions into outcomes (physical-plausibility checks, API calls). Modular component architecture (memory, chains-of-thought); prefabs for agents/GMs; inventory/economy components exist; Schelling-diagram scoring built in.
- **Best for:** Grounded social-science / economics / AI-safety simulation without building a world engine; rigorous, reproducible measurement.
- **Limits:** Text-grounded, not a visual world; quality depends heavily on LLM role-play ability; not built for thousands of agents.

### CAMEL
- **Link:** github.com/camel-ai/camel; paper arXiv:2303.17760 (NeurIPS 2023)
- **License / Cost:** Apache-2.0. API or local-model cost.
- **Primitive provided:** **Role-playing / inception prompting** — complementary-role agents communicate to solve tasks; framework explicitly targets "scaling laws of agents" and claims a design for up to 1M agents, with memory and benchmarking modules.
- **Best for:** Communicative multi-agent collaboration; large-scale emergent-behavior and scaling-law studies; synthetic data generation.
- **Limits:** Originally task-solving oriented rather than persistent-world; the very-large-agent claims are aspirational (unknown — search verified max-agent runs).

### AutoGen / AG2 (Microsoft)
- **Link:** github.com/microsoft/autogen; ~58,700 stars; paper arXiv:2308.08155
- **License / Cost:** MIT (unknown — search exact for sub-packages). API/local cost. As of October 2025, merged with Semantic Kernel into the unified Microsoft Agent Framework; AutoGen itself is now in maintenance mode.
- **Primitive provided:** **Event-driven multi-agent conversation** — structured conversational orchestration, tool use, code execution.
- **Best for:** Task-solving agent teams; the "multi-agent communication" primitive.
- **Limits:** No inherent persistent world, memory stream, or spatial/social dynamics; conversation-centric; maintenance mode.

### CrewAI
- **Link:** github.com/crewAIInc/crewAI; ~52,800 stars
- **License / Cost:** MIT. API/local cost. Standalone (independent of LangChain).
- **Primitive provided:** **Role-based crews + event-driven flows** — agents with roles, goals, tools.
- **Best for:** Production task automation with defined roles; quick multi-agent prototyping.
- **Limits:** Production-automation focus, not emergent society; no memory-stream/world model.

### LangGraph (LangChain)
- **Link:** github.com/langchain-ai/langgraph
- **License / Cost:** MIT. API/local cost. (LangChain ecosystem reports ~34.5M monthly downloads.)
- **Primitive provided:** **Durable, stateful graph orchestration** — checkpointed execution, human-in-the-loop, persistence; low-level control of agent control-flow.
- **Best for:** The orchestration backbone wiring memory + tools + multi-step planning for each civ agent.
- **Limits:** Orchestration layer only — you bring the world, memory semantics, and social model.

### Letta / MemGPT
- **Link:** github.com/letta-ai/letta (formerly MemGPT); paper arXiv:2310.08560
- **License / Cost:** Apache-2.0. Self-host via Docker (Postgres-backed) free + model cost; Letta Cloud paid. Model-agnostic.
- **Primitive provided:** **Tiered, self-editing memory** — core (in-context, editable) / recall / archival; agents rewrite their own context; "sleep-time"/dreaming consolidation; agents persisted as services with an open `.af` agent-file format.
- **Best for:** Giving each agent persistent identity + long-horizon learning; the memory backbone for stateful citizens.
- **Limits:** Per-agent statefulness is heavier than a simple memory stream; designed for stateful assistants more than 1,000-agent swarms; newer V1 architecture dropped heartbeats/prompted reasoning.

### AgentVerse (OpenBMB)
- **Link:** github.com/OpenBMB/AgentVerse
- **License / Cost:** Apache-2.0. API or local (vLLM/FSChat) cost.
- **Primitive provided:** **Dual frameworks** — task-solving (multi-agent-as-system) and **simulation** (custom environments for emergent social behavior). Ships NLP Classroom, Prisoner's Dilemma, Pokémon H5 demos; Minecraft branch exists.
- **Best for:** Quick emergent-behavior experiments and social games.
- **Limits:** Under refactor (use release-0.1 for stable simulation); smaller community than AutoGen/CrewAI.

### Sotopia
- **Link:** github.com/sotopia-lab/sotopia; "SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents," ICLR 2024
- **License / Cost:** MIT (unknown — search exact). API/local cost.
- **Primitive provided:** **Social-intelligence evaluation** — goal-driven social scenarios with multi-dimensional scoring (goal completion, relationship, social rules, secret-keeping, financial benefit); SOTOPIA-Ω adds dynamic strategy injection.
- **Best for:** Benchmarking the social reasoning / cooperation / negotiation of your agents (the evaluation half of Section H).
- **Limits:** Evaluation harness, not a world engine; scenario-scoped.

### MetaGPT
- **Link:** github.com/FoundationAgents/MetaGPT; ~67.9k stars; paper arXiv:2308.00352 (ICLR 2024 oral)
- **License / Cost:** MIT. API/local cost.
- **Primitive provided:** **SOP-encoded role org** — "Code = SOP(Team)"; PM/architect/engineer roles communicate via **structured documents** rather than free chat.
- **Best for:** Simulating a structured organization/company; division of labor as a civ primitive.
- **Limits:** Rigid SOP pipeline; software-company focus; not open-ended society.

### ChatDev
- **Link:** github.com/OpenBMB/ChatDev; paper arXiv:2307.07924 (ACL 2024)
- **License / Cost:** Apache-2.0 (unknown — search exact). API/local cost.
- **Primitive provided:** **Virtual software company** — role agents collaborate via dialogue through a phased waterfall to produce code.
- **Best for:** Studying structured dialogic collaboration / org processes.
- **Limits:** Rigid, customization-limited, not production; narrow (software) domain.

## B. World / Simulation Engines

### Mesa (Python)
- **Link:** github.com/projectmesa/mesa
- **License / Cost:** Apache-2.0; free.
- **Tick model:** Discrete-step scheduler (random/simultaneous/staged activation). **Max agents:** tens of thousands (pure Python; slower than JVM/Julia). **Persistence:** DataCollector → pandas; checkpointing manual. **Viz:** browser-based + Jupyter.
- **Best for:** The Python-native ABM substrate for non-LLM or hybrid civ models; rapid prototyping of economic/spatial dynamics.
- **Limits:** Python performance ceiling; not LLM-native out of the box.

### NetLogo
- **Link:** ccl.northwestern.edu/netlogo
- **License / Cost:** GPL-2.0; free.
- **Tick model:** Synchronous tick-based (turtles on patches). **Max agents:** millions of simple turtles, but benchmarked ~53× slower than optimized frameworks in a forest-fire model. **Persistence:** BehaviorSpace/world export. **Viz:** best-in-class built-in 2D/3D.
- **Best for:** Teaching, rapid classic ABM (Schelling, Sugarscape, predator-prey).
- **Limits:** Bespoke Logo language; synchronous-only core; awkward Python ML integration.

### MASON (Java)
- **Link:** cs.gmu.edu/~eclab/projects/mason
- **License / Cost:** Academic Free License; free.
- **Tick model:** Discrete-event scheduler. **Max agents:** thousands–millions; strong continuous-space (flocking) efficiency at thousands of agents. **Persistence:** serializable state. **Viz:** separable 2D/3D layer.
- **Best for:** High-performance large simulations where Java is acceptable.
- **Limits:** Java expertise; weaker novice UX.

### Repast (Simphony / Repast4Py / Repast HPC)
- **Link:** repast.github.io
- **License / Cost:** BSD-style; free.
- **Tick model:** Discrete-event. **Max agents:** Repast HPC scales to clusters (millions over MPI). **Persistence:** built-in logging/checkpoint. **Viz:** Simphony GUI; HPC headless.
- **Best for:** HPC-scale non-LLM ABM beyond a single machine.
- **Limits:** Steep learning curve; fragmented Java/C++/Python variants.

### AgentPy (Python)
- **Link:** agentpy.readthedocs.io (JOSS)
- **License / Cost:** BSD-3; free.
- **Tick model:** Step-based; integrated parameter sweeps. **Max agents:** ~Mesa-class. **Persistence:** DataDict export. **Viz:** Jupyter; fewer LOC than Mesa for sweeps.
- **Best for:** Multi-run experiment design / sensitivity analysis in Python.
- **Limits:** Smaller community; Python perf ceiling.

### Agents.jl (Julia)
- **Link:** juliadynamics.github.io/Agents.jl
- **License / Cost:** MIT; free.
- **Tick model:** Step-based; the fastest ABM framework in its own published comparison (others normalized to its runtime). **Max agents:** millions; near-C. **Persistence:** native save/load. **Viz:** Makie interactive.
- **Best for:** Performance-critical pure-ABM civ models in a high-level language.
- **Limits:** Julia compile-time; fewer LLM integrations.

### Evennia (Python MUD/text-world)
- **Link:** evennia.com
- **License / Cost:** BSD; free.
- **Tick model:** Event/tick scripts (TickerHandler); Django + Twisted. **Max agents:** hundreds–thousands of connected entities. **Persistence:** Django ORM (the strongest persistence story here). **Viz:** text/web client.
- **Best for:** Persistent text-world civilizations; LLM NPCs as first-class persistent objects; cheap (text = far fewer tokens than visual worlds).
- **Limits:** No spatial/visual sim; you build game logic; real-time scale needs care.

### Hytopia
- **Link:** hytopia.com
- **License / Cost:** SDK free; proprietary platform (unknown — search exact license/cost). TypeScript.
- **Tick model:** Server-authoritative real-time loop. **Max agents:** unknown — search tested limits. **Persistence:** platform-managed. **Viz:** voxel 3D browser.
- **Best for:** Shippable, player-facing voxel multiplayer worlds with JS/TS LLM bridges.
- **Limits:** Young platform; vendor dependence; few public benchmarks.

### Roblox + LLM bridges
- **Link:** create.roblox.com (Luau); LLM via HTTPService/Open Cloud
- **License / Cost:** Free to build; Roblox revenue share + LLM API cost.
- **Tick model:** Heartbeat ~60Hz. **Max agents:** server cap ~700 players; NPC count script/perf-bound. **Persistence:** DataStore. **Viz:** full 3D, huge built-in audience.
- **Best for:** Reaching players at scale; player-facing AI NPCs.
- **Limits:** External LLM calls rate-limited/sandboxed; moderation; ToS constraints.

### Minecraft (Mineflayer / MineDojo / MineRL)
- **Link:** github.com/PrismarineJS/mineflayer; minedojo.org; minerl.io
- **License / Cost:** Mineflayer MIT; MineDojo/MineRL MIT (unknown — search exact); needs Minecraft license/Java server.
- **Tick model:** 20 ticks/sec. **Max agents:** Project Sid pushed ~1,000 (unstable); 500 stable. **Persistence:** world save. **Viz:** full 3D.
- **Best for:** Embodied open-ended civ (Voyager/Sid lineage); the crafting tech-tree as economic substrate.
- **Limits:** Server can't hold ~1,000 agents reliably; agents lack vision unless added; bot control brittle.

### Unity ML-Agents
- **Link:** github.com/Unity-Technologies/ml-agents
- **License / Cost:** Toolkit open-source (Apache-2.0 components); Unity licensing tiers.
- **Tick model:** Unity update loop + decision steps; PyTorch trainer. **Max agents:** hundreds–thousands (physics-bound). **Persistence:** Unity serialization. **Viz:** full 3D/2D. (Eco is built on Unity.)
- **Best for:** RL-based embodied agents, policy evolution, hybrid RL+LLM.
- **Limits:** RL-centric, not LLM-native; physics cost limits agent count.

### Godot + LLM bindings
- **Link:** godotengine.org; community GDScript/C# LLM plugins
- **License / Cost:** MIT (engine fully free, zero royalties) + LLM cost.
- **Tick model:** _process/_physics_process loop. **Max agents:** perf-bound (hundreds–thousands of light nodes). **Persistence:** custom (Resources/SQLite). **Viz:** full 2D/3D.
- **Best for:** Fully open-source shippable games with embedded agents; no vendor lock-in.
- **Limits:** You build the LLM bridge and persistence; smaller AI ecosystem than Unity.

### Custom PixiJS / Phaser 2D
- **Link:** pixijs.com; phaser.io
- **License / Cost:** MIT; free.
- **Tick model:** requestAnimationFrame. **Max agents:** thousands of sprites in-browser. **Persistence:** you build it. **Viz:** 2D WebGL. (The original Smallville used Phaser; AI Town uses pixi-react.)
- **Best for:** Lightweight browser civ visualizations (the Smallville/AI Town aesthetic).
- **Limits:** 2D only; you build all sim/persistence.

### Skyrim modding (Mantella)
- **Link:** github.com/art-from-the-machine/Mantella; nexusmods.com/skyrimspecialedition/mods/98631
- **License / Cost:** Open-source (uses CC-BY wiki text); free locally, or OpenRouter free tier (100 req/day) / paid APIs. Needs Skyrim/Fallout 4.
- **Tick model:** Real-time STT→LLM→TTS pipeline (Whisper/Moonshine → LLM → Piper/xVASynth/XTTS). **Max agents:** arbitrary-size group conversations; per-NPC memory persists across sessions. **Persistence:** per-NPC memory files. **Viz:** full Skyrim 3D.
- **Best for:** Player-facing voiced AI NPCs with memory, vision, and 20+ in-game actions — the most polished consumer AI-NPC experience.
- **Limits:** A mod, not a platform; single-player; latency-sensitive; tied to Bethesda games.

### VRChat AI NPCs
- **Link:** VRChat SDK (Udon) + community LLM bridges
- **License / Cost:** SDK free; LLM cost. (unknown — search current official AI-NPC support.)
- **Tick model:** Real-time social VR. **Max agents:** instance cap (tens of avatars). **Persistence:** limited (community solutions). **Viz:** full social VR.
- **Best for:** Embodied social VR agents alongside human players.
- **Limits:** Udon sandbox limits external calls; weak persistence; ToS constraints.

## C. Classic ALife / Evolutionary Substrates (the canon)

### Tierra (Tom Ray, 1991)
- **Link:** life.ou.edu (historical)
- **License / Cost:** Academic; free. **Maturity:** historical landmark.
- **What:** Self-replicating machine-code organisms compete for CPU + memory; spontaneous parasites/hyper-parasites; open-ended digital evolution.
- **Best for:** The conceptual foundation of code-as-organism.
- **Limits:** Non-local interactions hinder distribution; dated codebase.

### Avida (Michigan State / devolab)
- **Link:** github.com/devosoft/avida; avida.devosoft.org; Avida-ED at avida-ed.github.io
- **License / Cost:** GNU LGPL (newer code BSD-style MSU license); free.
- **What:** Each digital organism has protected memory + its own virtual CPU; Poisson mutations; intrinsic + extrinsic fitness. Produced the Lenski/Ofria/Pennock/Adami *Nature* 2003 result on the evolutionary origin of complex features. Avida-ED is a free browser educational version (2017 ISAL Education & Outreach Award).
- **Best for:** Rigorous, publishable digital-evolution experiments; teaching.
- **Limits:** Abstract (no rich world/economy/social layer); non-embodied.

### Polyworld (Larry Yaeger)
- **Link:** github.com/polyworld/polyworld
- **License / Cost:** Open-source; free.
- **What:** Embodied creatures with Hebbian neural-net brains in 2D; eat/mate/fight/evolve; uses Tononi–Sporns–Edelman complexity to measure neural integration.
- **Best for:** Neural-evolution + ecology studies; emergent r/K strategies.
- **Limits:** Dated; small community; build friction.

### Framsticks (Komosinski & Ulatowski)
- **Link:** framsticks.com
- **License / Cost:** Free for education/research/non-commercial under its own license (core NOT open-source; FRED editor is open Java). Evolved creatures usable commercially with credit. Current v5.2.
- **What:** 3D stick-and-joint creatures with neural brains; evolve morphology + control; Python/Java network APIs, client-server.
- **Best for:** Evolved virtual creatures (morphology+control) with scripting access.
- **Limits:** Proprietary core limits redistribution; devs note "not used in industry."

### OpenWorm
- **Link:** openworm.org; github.com/openworm
- **License / Cost:** MIT; free.
- **What:** Open-science whole-organism simulation of *C. elegans* (302 neurons): Sibernetic fluid sim + c302 neural model.
- **Best for:** Biologically grounded single-organism neural simulation.
- **Limits:** Not a civilization substrate; extremely narrow; long-running, incomplete.

### Lenia (Bert Wang-Chak Chan)
- **Link:** github.com/Chakazul/Lenia; arXiv:1812.05433, 2005.03742
- **License / Cost:** MIT (unknown — search exact); free.
- **What:** Continuous-space/time/state generalization of Game of Life; smooth self-organizing "lifeforms" with individuality, self-replication, division of labor ("virtual eukaryotes"). Won the 2018 Virtual Creatures Contest and ISAL Outstanding Publication 2019. Variants: **Flow Lenia** (mass conservation → virtual creatures) and **Particle Lenia** (Mordvintsev/Niklasson/Randazzo, energy-based).
- **Best for:** Pure no-LLM emergence/open-endedness; the modern ALife darling.
- **Limits:** No goals/economy/language; emergence is morphodynamic, not cognitive; measuring complexity is an open problem.

### Particle Lenia (Mordvintsev et al., Google)
- **Link:** google-research.github.io/self-organising-systems/particle-lenia
- **License / Cost:** Open demo/code; free.
- **What:** Particle-based, energy-minimizing Lenia variant; complex dynamics from particle-interaction rules.
- **Best for:** Lightweight interactive ALife with an energy-based formulation.
- **Limits:** Same as Lenia — no cognition.

### Neural Cellular Automata (Mordvintsev et al., Distill 2020)
- **Link:** distill.pub/2020/growing-ca ("Growing Neural Cellular Automata")
- **License / Cost:** Open; free.
- **What:** CA update rule parameterized by a small neural net; learns to grow/regenerate target patterns; self-repair.
- **Best for:** Morphogenesis, self-repair, generative substrate; pairs with ASAL search.
- **Limits:** Pattern-formation, not social agents.

### ALIEN (Artificial Life Environment, chrxh)
- **Link:** github.com/chrxh/alien; alien-project.org; chrxh.itch.io/alien
- **License / Cost:** BSD-3-Clause (current; older forks were GPLv3 — flag if it matters); free. CUDA/C++.
- **What:** GPU-accelerated 2D particle-physics ALife; cells form bodies with sensors, muscles, weapons, constructors run by neural nets; genomes inherited. Won the ALIFE 2024 Virtual Creatures Competition.
- **Best for:** Visually rich, GPU-scale ALife evolution with agent-like organisms.
- **Limits:** Windows-only installer; **requires an Nvidia GPU (CUDA ≥6.0, ~4GB VRAM)** — no AMD/Mac; single genome capped at 8 KB.

### The Bibites (Léo Caussan)
- **Link:** thebibites.com; thebibites.itch.io/the-bibites
- **License / Cost:** Free standalone (Win/Linux/Mac); paid Steam version adds Workshop/achievements. Closed-source.
- **What:** 2D creatures with evolving neural-net brains + genetic code; egg-based reproduction with mutation; food-web ecology.
- **Best for:** Accessible, watchable neural-creature evolution.
- **Limits:** No tutorial; closed-source limits research extension.

### Sodaplay / Sodaconstructor (Ed Burton)
- **Link:** historical (Wikipedia: Soda_Constructor)
- **License / Cost:** Was a free Java applet; **effectively defunct** (2014 reboot Kickstarter failed at £2,246/£25,000).
- **What:** Mass-spring physics construction toy; muscle-driven walking creatures; BAFTA 2001.
- **Best for:** Historical inspiration only.
- **Limits:** Java applets unsupported by modern browsers; only unofficial JS clones remain.

### Karl Sims — Evolved Virtual Creatures (1994)
- **Link:** karlsims.com/evolved-virtual-creatures.html
- **License / Cost:** Original ran on a Connection Machine CM-5. Modern reimplementations: jjuiddong/KarlSims (DX3D+PhysX), Taylor & Massey (2001, off-the-shelf physics). A canonical MuJoCo/Bullet port is unconfirmed — search.
- **What:** Directed-graph genotype encoding body + brain; GA-evolved for swimming/walking/jumping/competing for a cube.
- **Best for:** The foundational reference for co-evolving morphology + control.
- **Limits:** Original code not runnable today; reimplementations vary.

### Creatures (Steve Grand, 1996)
- **Link:** creaturesdockingstation.com; Steam App 1659050 (free); openc2e engine
- **License / Cost:** Docking Station is **free** (Win/Linux, also free on Steam); openc2e engine open-source.
- **What:** Norns with digital DNA, neural-net brains, and chemical metabolism; breed and learn.
- **Best for:** Classic creature-AI with biochemistry + learning; openc2e for hacking.
- **Limits:** Official online servers dead (community "Natsue" warp); aging engine.

### Black & White (Lionhead / Molyneux, 2001)
- **Link:** commercial (GOG/abandonware status unknown — search)
- **License / Cost:** Proprietary; no source.
- **What:** A Creature that learns by reinforcement + imitation (player feedback) — landmark learned-behavior game AI.
- **Best for:** Design inspiration for reinforcement/imitation-shaped agents.
- **Limits:** Closed; not a research tool.

### Spore (Maxis, 2008)
- **Link/License:** commercial, proprietary.
- **What:** Procedural creature/civ creation across scales; "evolution" is largely aesthetic/procedural rather than genuine selection.
- **Best for:** Inspiration for multi-scale civ progression and procedural generation.
- **Limits:** Evolution is cosmetic; not a simulation substrate.

### Dwarf Fortress (Bay 12)
- **Link/License:** bay12games.com; Steam; proprietary (paid Steam; classic free).
- **What:** Deep emergent simulation — geology, hydrology, history generation, psychology, economy, emergent narrative from systems depth.
- **Best for:** The gold standard of emergent simulation design; a reference for world/economy/history systems.
- **Limits:** Closed-source; not programmable as an agent platform.

### RimWorld (Ludeon)
- **Link/License:** rimworldgame.com; proprietary; very moddable (Harmony/C#).
- **What:** Colony sim with an **AI Storyteller** (director shaping events) plus needs/mood/relationship systems.
- **Best for:** The director/storyteller pattern; mod-driven LLM-NPC experiments.
- **Limits:** Closed core; not built for thousands of autonomous agents.

### Caves of Qud (Freehold Games)
- **Link/License:** cavesofqud.com; proprietary.
- **What:** Procedural world with deep historical/faction/relationship generation and emergent ecology.
- **Best for:** Inspiration for procedural history + faction systems.
- **Limits:** Closed; not a platform.

### Ultima Online (Origin / Garriott, 1997)
- **Link:** historical; commercial.
- **What:** Famous **virtual-ecology experiment** (a 3-year carnivore/herbivore/plant food chain) destroyed by players within days of launch; the code was removed. Garriott's lesson: "If you put it in a game, and we can kill it, then we will kill it because we will assume that there must be some reason for us to kill it."
- **Best for:** The cautionary postmortem for agent/ecological economies — emergent agents (like players) will exploit any exploitable system.
- **Limits:** Historical; the lesson outweighs the artifact.

### Eco (Strange Loop Games)
- **Link:** play.eco; Steam App 382310
- **License / Cost:** Commercial (paid); built in **Unity (C#)**; devs frame "the Eco engine" as a reusable platform.
- **What:** Multiplayer civ-survival where all resources come from a simulated ecosystem; player-built **economies (backed/fiat currencies), programmable laws, and government** — "Tragedy of the Commons: The Game." Originally an educational tool (over $1M from the US Dept. of Education; 2015 Kickstarter $200k+).
- **Best for:** A reference design for simulated economy + governance + ecological feedback; a possible host for AI players.
- **Limits:** Closed-source; performance/agent-count limits unknown — search.

### Equilinox (ThinMatrix)
- **Link/License:** equilinox.com; commercial (paid).
- **What:** Peaceful ecosystem-evolution sim; breed/evolve species across biomes.
- **Best for:** Lightweight ecosystem inspiration.
- **Limits:** Closed; shallow evolution; not a platform.

### Species: Artificial Life, Real Evolution (ALRE)
- **Link:** speciesgame.com; Steam App 774541
- **License / Cost:** **Paid** Steam Early Access (the many "free download" sites are piracy). "Mostly Positive" (~73% of 967 reviews).
- **What:** Scientifically-grounded emergent natural selection — creatures mutate, speciate, and form phylogenetic trees under selection pressures.
- **Best for:** Watching genuine open-ended speciation; teaching selection.
- **Limits:** Early Access (devs warn of bugs); closed-source.

## D. Memory / Knowledge Layer

### Chroma
- **Link:** github.com/chroma-core/chroma
- **License / Cost:** Apache-2.0; free (in-process or server).
- **What:** Simplest-API embedding store; embedded or server.
- **Best for:** Fast prototyping of episodic/semantic memory; the "minimum viable" vector store.
- **Limits:** Not billion-scale; a raw ANN store knows nothing of time/contradiction/relevance.

### Qdrant
- **Link:** github.com/qdrant/qdrant
- **License / Cost:** Apache-2.0; free self-host + paid cloud. Rust.
- **What:** High-performance vector DB with rich payload filtering + strong consistency; Mem0's default backend.
- **Best for:** Production agent memory with metadata filtering (per-agent/session scoping).
- **Limits:** Separate service to operate; still ANN-only semantics.

### Weaviate
- **Link:** github.com/weaviate/weaviate
- **License / Cost:** BSD-3; free self-host + cloud. GraphQL.
- **What:** Vector DB with hybrid search and built-in vectorization modules (insert text, get vectors).
- **Best for:** Knowledge-graph-flavored memory + hybrid search.
- **Limits:** Java runtime resource-heavy; GraphQL learning curve; modules add latency/cost.

### LanceDB
- **Link:** github.com/lancedb/lancedb
- **License / Cost:** Apache-2.0; free. Disk-based (Lance columnar format).
- **What:** Embedded, larger-than-memory vector store with disk-based indexing; a default Mem0 vector backend.
- **Best for:** Local-first, large on-disk agent memory without a server.
- **Limits:** Younger ecosystem; fewer managed options.

### Letta (as memory layer)
- **License / Cost:** Apache-2.0; self-host free + model cost.
- **What:** Tiered core/recall/archival memory with self-editing — MemGPT's OS-like context paging.
- **Best for:** Turnkey **procedural + episodic + semantic** memory per agent without hand-rolling schemes.
- **Limits:** Heavier per agent; opinionated architecture.

### Zep
- **Link:** github.com/getzep/zep
- **License / Cost:** Open-source core + paid cloud (advanced features gated).
- **What:** **Dual store (vector + temporal knowledge graph, "Graphiti")** — extracts atomic facts into a time-aware graph; temporal queries. Scored 63.8% on the LongMemEval temporal-retrieval sub-task (vs Mem0's 49.0%) in an independent eval.
- **Best for:** Agents needing temporal reasoning + entity relationships over long histories.
- **Limits:** Best graph features behind cloud tier; extraction quality varies.

### Mem0
- **Link:** github.com/mem0ai/mem0; docs.mem0.ai
- **License / Cost:** Apache-2.0 OSS; graph features ("Mem0g") require ~$249/mo Pro tier. Raised **$24M across a Seed (led by Kindred Ventures) and Series A (led by Basis Set Ventures), announced Oct 28, 2025**, with Peak XV, GitHub Fund, and Y Combinator. Defaults to SQLite + LanceDB + Kuzu, or Qdrant.
- **What:** Memory layer **on top of** a vector DB (+ optional graph) extracting atomic facts (subject-relation-object), scoped by user/session/agent.
- **Best for:** Drop-in long-term memory across sessions; multi-agent scoped recall.
- **Limits:** Graph behind paywall; extraction noise accumulates; **49.0% on the LongMemEval temporal-retrieval sub-task (GPT-4o)** in an independent eval — meaningfully below Zep's Graphiti at 63.8%.

### Hierarchical / cognitive-science memory schemes
- **What:** Mapping cognitive memory types onto agents: **episodic** (time-stamped events → memory stream), **semantic** (facts → KG/fact store), **procedural** (skills → Voyager's skill library or Letta's editable prompts/tools). Generative Agents' recency/importance/relevance scoring + reflection is the canonical hierarchical scheme; MemGPT adds OS-style paging; recent work argues raw ANN "storage ≠ memory" and favors retrieval-centered architectures (arXiv:2605.04897).
- **Best for:** Deciding which memory type each civ behavior needs — reflection for culture, skill library for economy.
- **Limits:** No consensus standard; the "right" consolidation/forgetting policy is an open problem.

## E. Economy / Governance Primitives (real & simulated)

### Ethereum
- **Link/License/Cost:** ethereum.org; open protocol; gas fees (real money) on mainnet; free on testnets/local (Hardhat/Foundry/Anvil).
- **What:** Turing-complete contracts (Solidity/Vyper) for tokens, markets, DAOs — reusable as an agent economic/governance substrate.
- **Best for:** Verifiable agent ownership, on-chain markets, DAO-style governance experiments.
- **Limits:** Gas cost + latency make per-tick agent transactions impractical on mainnet; use L2/local chains.

### Solana
- **Link/License/Cost:** solana.com; open; low fees; local validator free. Rust/Anchor.
- **What:** High-throughput L1 (sub-cent fees, fast finality) — better for high-frequency agent micro-transactions.
- **Best for:** Many small agent transactions/tick on a real chain.
- **Limits:** Still external dependency/cost; complexity vs an in-memory ledger.

### Hyperledger Fabric
- **Link/License/Cost:** hyperledger-fabric.readthedocs.io; Apache-2.0; free (permissioned, self-hosted).
- **What:** Permissioned enterprise blockchain; chaincode in Go/Java/JS.
- **Best for:** Private, controlled agent-economy ledgers with known validators.
- **Limits:** Heavy ops; overkill vs a simple database for most sims.

### Radix
- **Link:** radixdlt.com; github.com/radixdlt/radixdlt-scrypto
- **License / Cost:** Radix License v1.0 (modified Apache-2.0). Babylon (smart contracts) live Sept 28, 2023.
- **What:** L1 with **asset-oriented Scrypto** (Rust-based) where tokens are native FSM-governed "resources," plus Cerberus sharded consensus.
- **Best for:** Agent economies where value-transfer safety matters — assets behave like physical objects, reducing whole classes of exploit.
- **Limits:** Smaller ecosystem; a new paradigm/language to learn.

### Anoma
- **Link:** anoma.net
- **License / Cost:** Open (unknown — search exact license). **Mainnet targeted 2026 — not yet shipped (forward-looking).**
- **What:** **Intent-centric** architecture — agents sign *intents* (desired outcomes); solvers discover counterparties and settle atomically; Resource Machine state model; Juvix language.
- **Best for:** A native **marketplace for autonomous agents** — agents express goals, a solving layer clears them (directly analogous to agent-economy matchmaking).
- **Limits:** Pre-mainnet; experimental; conceptual maturity exceeds production readiness.

### Prediction markets / mechanism-design libraries
- **What:** LMSR (Hanson's logarithmic market scoring rule) and mechanism-design tooling for belief aggregation, auctions, and voting (VCG, quadratic voting); Gnosis/Polymarket contracts. LLM-agent social sims increasingly pair agents with internal prediction markets.
- **Best for:** Aggregating agent forecasts; auction/allocation primitives; emergent price discovery.
- **Limits:** Much is research code; tuning for stability is hard.

### MMO economy postmortems (the design canon)
- **EVE Online:** CCP hired **Dr. Eyjólfur "Eyjo" Guðmundsson in 2007** as lead economist (he described the role as "like a research scientist for a central bank"); CCP publishes **Monthly Economic Reports**; the economy is balanced via **ISK faucets (mainly bounties) vs sinks (NPC taxes, asset destruction)**; "Active ISK Delta" excludes 90-day-inactive accounts; PLEX has become a quasi-currency. Even CCP's own MERs have shipped with data errors (one chart off ~9%).
- **RuneScape / OSRS:** The Grand Exchange **1% sales tax was added 9 Dec 2021** (raised to **2% on 29 May 2025**), capped at 5M gp/item, with an **Item Sink** that buys and deletes oversupplied goods; Mod Ash noted "well over half the taxed coins are drained… rather than being re-injected." Pre-tax, an estimated ~2.7 trillion gp entered the game monthly.
- **Diablo III RMAH:** The Real-Money Auction House **opened June 12, 2012** and was **discontinued March 18, 2014**; production director John Hight stated it "ultimately undermines Diablo's core game play: kill monsters to get cool loot." Intended for ~10% of players, but "stingy" loot "shoved everyone into the auction house" (Josh Mosqueira).
- **Best for:** Hard-won lessons on inflation control (sinks/faucets), exploit-proofing, and not letting a meta-economy cannibalize core behavior — directly applicable to agent economies.
- **Limits:** Human-player lessons may not transfer 1:1 to LLM agents (different exploit-seeking).

## F. Evolution / Open-Endedness

### POET
- **Link:** arXiv:1901.01753 (Wang, Lehman, Clune, Stanley; GECCO 2019); Enhanced POET arXiv:2003.08536
- **License / Cost:** Apache-2.0 (unknown — search exact); free.
- **What:** **Paired Open-Ended Trailblazer** — co-evolves environments and agent solutions with MAP-Elites-style transfer + minimal-criterion coevolution; generates an endless curriculum.
- **Best for:** Auto-generating ever-harder civ challenges/environments with matched agents.
- **Limits:** Compute-heavy; environment encoding is domain-specific.

### MAP-Elites
- **Link:** arXiv:1504.04909 (Mouret & Clune)
- **License / Cost:** Algorithm (many MIT impls, e.g. QDax); free.
- **What:** **Illumination/quality-diversity** — keeps a grid archive of the best solution per behavioral niche; returns diverse high performers, not one optimum.
- **Best for:** Diverse agent behaviors/morphologies; behavioral repertoires; damage recovery (the "Robots that can adapt like animals" *Nature* result).
- **Limits:** Requires hand-chosen behavior descriptors (exceptions: AURORA auto-descriptors); grid-granularity vs cost tradeoff.

### Quality-Diversity (QD) family
- **Link:** QDax (github.com/adaptive-intelligent-robotics/QDax); pyribs (github.com/icaros-usc/pyribs)
- **License / Cost:** MIT/Apache; free; QDax is JAX-accelerated.
- **What:** Novelty search, NSLC, MAP-Elites, CMA-ME, MOME — balance novelty + quality to cover behavior space.
- **Best for:** GPU-scale QD for evolving diverse civ agents/content.
- **Limits:** Descriptor design; can be sample-hungry.

### OMNI
- **Link:** arXiv:2306.01711 (Zhang, Lehman, Stanley, Clune)
- **License / Cost:** Research code (unknown — search exact license); free.
- **What:** Uses a foundation model to judge which tasks are "interesting/learnable," steering an auto-curriculum — attacking the descriptor problem in open-endedness.
- **Best for:** LLM-guided curricula (what civ agents should learn next).
- **Limits:** New; depends on FM judgment quality.

### NEAT / HyperNEAT (Stanley & Miikkulainen)
- **Link:** NEAT (2002, ISAL Paper of the Decade 2002–2012); HyperNEAT (2009). Impls: neat-python (BSD), SharpNEAT, PyTorch-NEAT.
- **License / Cost:** Open; free.
- **What:** **NEAT** complexifies neural topologies from minimal, using historical markings + speciation; **HyperNEAT** uses CPPNs to indirectly encode large, geometrically regular nets.
- **Best for:** Evolving agent brains/controllers from scratch (the no-LLM cognition path).
- **Limits:** Scales worse than gradient methods for huge nets; HyperNEAT doesn't always beat NEAT.

### OpenAI Evolution Strategies
- **Link:** arXiv:1703.03864 ("Evolution Strategies as a Scalable Alternative to Reinforcement Learning")
- **License / Cost:** Open; free.
- **What:** Black-box, massively parallelizable ES for policy optimization — scales across many CPUs with minimal communication.
- **Best for:** Massively parallel policy evolution where gradients are awkward.
- **Limits:** Sample-inefficient vs gradient RL for some tasks.

### Sakana AI — Evolutionary Model Merge / ASAL
- **Link:** sakana.ai/evolutionary-model-merge (published in *Nature Machine Intelligence*); asal.sakana.ai (arXiv:2412.17799)
- **License / Cost:** Methods open; implemented in mergekit/Optuna. Free (compute aside).
- **What:** **Evo model-merging** discovers non-intuitive ways to combine model weights/layers to make new capable models; **ASAL** uses foundation models to automate the *search for artificial life* across Boids/Lenia/NCA/Game-of-Life and to quantify previously qualitative emergence.
- **Best for:** Cheaply generating specialized agent models (merge instead of train); FM-driven ALife discovery + emergence metrics.
- **Limits:** Merge quality unpredictable; ASAL emergence measures are new.

### Novelty Search (Lehman & Stanley)
- **Link:** "Abandoning Objectives" (2011); book *Why Greatness Cannot Be Planned*
- **License / Cost:** Algorithm; free.
- **What:** Reward behavioral novelty (distance to an archive) instead of an objective — escapes deception/local optima; maintains phenotypic diversity (vs NEAT's genotypic).
- **Best for:** Open-ended divergence; seeding cultural/behavioral variety.
- **Limits:** No quality guarantee alone (hence QD hybrids).

## G. Infra / Scaling

### vLLM
- **Link:** github.com/vllm-project/vllm
- **License / Cost:** Apache-2.0; free (self-host; GPU cost).
- **What:** **PagedAttention** + continuous batching; early benchmarks 14–24× HF Transformers throughput; OpenAI-compatible server; widest model/hardware support. Hit ~8,033 tok/s with NVFP4 on a Blackwell benchmark; **100% success at 128 concurrent requests**.
- **Best for:** The default for serving N agents from one GPU; high concurrency.
- **Limits:** GPU memory/ops to manage; benchmark leadership varies by hardware tier.

### SGLang (LMSYS)
- **Link:** github.com/sgl-project/sglang
- **License / Cost:** Apache-2.0; free.
- **What:** **RadixAttention** (prefix-cache reuse) — excels at shared-prefix agent loops and multi-turn; won 6/8 concurrency levels vs vLLM same-model in one test; ~648 TPS on A10 at batch 128.
- **Best for:** Many agents sharing a large common system/world prompt (huge token savings); agent loops/RAG.
- **Limits:** Some hardware (Blackwell SM-120) needs flags/patches; ecosystem younger than vLLM.

### Ollama
- **Link:** ollama.com
- **License / Cost:** MIT; free.
- **What:** One-command local model serving; excellent DX; automatic VRAM management.
- **Best for:** Local prototyping (AI Town/Mantella default), single-agent/dev.
- **Limits:** No real continuous batching — ~484 tok/s (≈10× slower than vLLM/SGLang) and **broke down at 128 concurrent requests**; not for multi-agent production load.

### Cost math (tokens × agents × ticks)
- **What:** Cost ≈ agents × (LLM calls/agent/tick) × (in+out tokens/call) × ticks × ($/token). Example: 100 agents × 1 call/tick × ~1.5k tokens × 1,000 ticks ≈ 150M tokens — at GPT-4-class API (~$5–15/M) ≈ $750–2,250 per run; the same on a local 8B at ~3–6k tok/s is hours of GPU time (an H100 at ~$2/hr ≈ single-digit dollars). This is why the field moved to small local models + SGLang prefix sharing.
- **Best for:** Budgeting before launch.
- **Limits:** Reflection/planning multiply calls/tick; long contexts blow up token counts.

### Local vs API tradeoff
- **What:** API = zero ops, fastest start, but per-token cost dominates at agent scale and data leaves your network. Local (vLLM/SGLang on rented/owned GPU) = high fixed cost, near-zero marginal token cost, full data control — wins once monthly API spend exceeds GPU rental.
- **Best for:** Choosing the crossover point for your scale.
- **Limits:** Local needs MLOps + GPU access.

### Small models for cheap NPCs
- **What:** **Qwen3** (dense + MoE, strong multilingual, Apache-2.0); **Llama** (Meta community license, restrictions at very large scale); **Phi-4** (Microsoft, MIT, strong reasoning-per-param); Gemma, Mistral/Ministral, gpt-oss (OpenAI open-weight). **Distillation / behavior cloning:** train a small model on a frontier model's agent trajectories to clone behavior cheaply. Tier your models — big brains for leaders, small for crowds.
- **Best for:** Running thousands of NPCs at fractions of a cent each. (Current SOTA small-model rankings: unknown — search latest open-LLM leaderboard.)
- **Limits:** Small models are weaker at long-horizon planning/theory-of-mind; Project Sid needed GPT-4o-class for real progress.

## H. Evaluation / Metrics for Emergent Civilization

- **Civilizational benchmarks (Project Sid, arXiv:2411.00114):** role-specialization counts, rule adherence/change, collective-action progress (Minecraft item/tech-tree progression across ~1,000 items), cultural-meme spread, religion conversion curves (Pastafarianism). *Best for:* end-to-end civ progress. *Limit:* Minecraft-specific.
- **Believability (Generative Agents):** human-rated believability (their agents rated more believable than humans role-playing agents); interview probes of memory/plans. *Limit:* subjective, costly.
- **Social intelligence (Sotopia, ICLR 2024):** multi-dimensional scores — goal completion, relationship maintenance, knowledge, secret-keeping, social-rule adherence, financial/material benefit.
- **Language drift / emergent communication:** **topographic similarity** (correlation of meaning-space and message-space distances), **Jaccard similarity** and unique-message counts, KL-based pairwise language distance *D* (arXiv:1904.09067), and **structural vs semantic drift** (Lazaridou et al. 2020; EcoLANG arXiv:2505.06904). *Best for:* measuring culture/language formation.
- **Cultural transmission:** "do two agents speak the same language in the same context?" as transmission evidence; iterated-learning compositionality under a transmission bottleneck (Kirby).
- **Economic complexity:** faucet/sink inflation balance (EVE-style), Gini coefficient of agent wealth, trade-network density/diversity, price stability/velocity, market depth. *Limit:* no standard agent-economy benchmark yet — search.
- **Cooperation/conflict:** payoffs in embedded social dilemmas (Prisoner's Dilemma, public-goods, Schelling diagrams in Concordia); conflict frequency; coalition formation. *Key suite:* **Melting Pot (DeepMind, arXiv:2107.06857)** — a dedicated multi-agent social-dilemma evaluation suite testing generalization to novel social partners.
- **Emergence quantification:** Granger-emergence toolboxes for ABM; ASAL's FM-based complexity/open-endedness measures; agent-drift indices (semantic/coordination/behavioral drift, arXiv:2601.04170). *Limit:* "emergence" remains contested and hard to quantify.

## Recommendations

**Stage 0 — Decide your axis first (this week).** Pick one of the four lanes below based on your goal. The single most consequential early choice is *LLM-driven society* vs *pure ALife evolution* — they share almost no tooling.

### Stack "Minimum viable civ" (cheapest)
- **Engine:** AI Town (MIT) on Convex + pixi.
- **Brains:** local **Qwen3-8B** (or Llama-class) via **Ollama** for the first day, then **switch to vLLM the moment you exceed ~10 agents**.
- **Memory:** AI Town built-in, or add Chroma for episodic recall.
- **Agents:** ~15–30 (matches Smallville's tested scale).
- **Cost:** ≈ **$0/month** fully local on one consumer GPU (electricity only); ≈ **$20–100/month** with a small hosted API for a town this size.
- **Why / when to graduate:** deployable in a day. **Move up** when agents per second stalls or you want economy/evolution primitives.

### Stack "Research grade" (best emergence, higher cost)
- **Engine:** Minecraft + Mineflayer (the Voyager/Sid lineage) for embodied civ, **or** Concordia (text-grounded GM pattern) for controlled, measurable studies.
- **Architecture:** PIANO-style parallel modules (Project Sid) or Concordia components; Voyager skill library for procedural memory.
- **Brains:** GPT-4o / Claude / frontier for leader agents (Sid needed GPT-4o-class), small local models for crowds; serve via **SGLang** to share the world prompt across all agents.
- **Memory:** Letta (tiered self-editing) or Zep (temporal KG) per agent.
- **Evolution:** MAP-Elites/POET via QDax (JAX) for environment/behavior diversity.
- **Metrics:** Project Sid civ benchmarks + Sotopia + Melting Pot + topographic-similarity language drift.
- **Agents:** **100–500** (500 is Sid's stable analyzed scale; expect instability past it).
- **Cost:** ≈ **$1k–5k+/month** (frontier API + GPU); a local-heavy variant is rented H100 time.

### Stack "Game-shippable" (player-facing, performant)
- **Engine:** Godot (MIT, zero royalties) or Unity (ML-Agents) for full control; **Skyrim + Mantella** to ship on an existing game today; Roblox/Hytopia to reach an audience.
- **Brains:** tiered — distilled small local model (Phi-4 / Qwen3-4B) for ambient NPCs, a mid model for key characters; **vLLM** backend; aggressive prompt caching.
- **Memory:** Mem0 or per-NPC memory files (the Mantella pattern).
- **Persistence:** game DB (DataStore / SQLite / Convex).
- **Agents:** dozens of visible NPCs (perf-bound), more off-screen.
- **Cost:** ≈ **$50–500/month** depending on player count and local vs API; Mantella can run **free** locally or via OpenRouter's free tier (100 req/day).

### Stack "Pure ALife / no LLM" (evolution from scratch)
- **Substrate:** Lenia / Flow Lenia / Particle Lenia, **or** ALIEN (GPU CUDA) for rich organisms, **or** Avida for rigorous digital evolution.
- **Cognition:** NEAT/HyperNEAT (neat-python) or QD (QDax); Karl-Sims-style morphology+control if embodied.
- **Search:** MAP-Elites + novelty search; ASAL (Sakana) for FM-guided discovery and emergence metrics.
- **Glue (if you need ABM):** Agents.jl (fastest) or Mesa (Python).
- **Cost:** ≈ **$0** (open-source) + one GPU (Nvidia required for ALIEN; JAX-friendly GPU for QDax).

### Thresholds that should change your decision
- **Concurrency > ~10 agents:** abandon Ollama for vLLM/SGLang immediately.
- **Shared world/system prompt > ~2k tokens reused across agents:** switch serving to SGLang (RadixAttention) — prefix caching is the biggest single cost win.
- **Monthly API spend > GPU rental (~$1.5–2k for an H100):** move to local serving.
- **Target > 500 concurrent embodied agents:** Minecraft will not hold; move to a custom lightweight engine (PixiJS/Convex) or a headless ABM (Repast HPC) and accept reduced embodiment.
- **You observe agents trivially exploiting your economy/ecology:** instrument faucet/sink balance and add sinks *before* scaling — the Ultima Online failure mode.

## Caveats
1. **Volatile metadata:** every star count, license, and "last commit" drifts; verify each repo's current state before committing. Items marked **"unknown — search [X]"** were not confirmable in-session and should not be treated as established.
2. **Cost, not the engine, is the wall.** Reflection and planning multiply LLM calls per tick; budget with the token math above and design for small local models + prefix sharing from the start.
3. **Foundation-model agents imitate, they don't invent institutions.** Project Sid's own authors note agents "cannot simulate de novo emergence" of democracy, fiat economies, or communication systems because they inherit human priors. Pure-ALife substrates do the opposite — they genuinely invent novelty but don't reason. Choose accordingly, or hybridize.
4. **"Emergence" is hard to measure and easy to over-claim.** Many sources (and marketing) describe agent societies in narrative, anthropomorphic terms; ground your claims in the Section H metrics (topographic similarity, Melting Pot scores, Gini, faucet/sink balance) rather than anecdotes like "they spontaneously formed a religion."
5. **Exploitation is the default, not the exception.** Ultima Online's three-year ecology was destroyed in days; sufficiently capable agents will do the same. Instrument emergent-exploit and economic-stability metrics from day one.
6. **Some "facts" here are vendor/blog framings.** EVE's "stagflation/decline" narratives come from community blogs, not CCP (which disputes them); Eco being "Unity" is well-reported but the devs emphasize their own engine layer; the Diablo III and Ultima Online quotes are from interviews/postmortems, accurate as design lessons but filtered through hindsight. Treat interpretive economic narratives as analysis, not measurement.