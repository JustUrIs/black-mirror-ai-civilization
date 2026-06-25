# AI CIVILIZATION — SYNTHESIS
*The founding document. Synthesis of DUMP_1 (tech), DUMP_2 (theory), DUMP_3 (fiction), DUMP_4 (philosophy), DUMP_5 (market). Forge layer, not summary layer.*

Date: 2026-06-20. Author: synthesis pass over five parallel deep-research outputs.

---

## 0. EXECUTIVE THESIS

**The single most defensible startup the five dumps collectively support is a persistent, spectator-streamable, programmable AI-civilization platform whose primary moat is a measured complexity metric and a tiered cost architecture nobody else has wired together.** Call it **EIDOLON** (placeholder; rename freely).

- **Problem.** Every adjacent product is broken in the same place. AI Town / Smallville plateau at 25–100 agents (DUMP_5 #1). AgentSociety reaches 10–30k but needs 24 A800s and is research-only (DUMP_5 #2, DUMP_1 H). Character.AI and Replika scale users but agents do not interact with each other (DUMP_5 Char.AI / Replika). Project Sid hit 500 stable agents in Minecraft and then ran out of server (DUMP_1 A). Improbable's SpatialOS shipped distributed infra and *no civilization* (DUMP_5 Improbable). Mem0 raised $24M for memory but scored only 49% on LongMemEval temporal-retrieval (DUMP_1 D, vs Zep 63.8%). Nobody has shipped a civ that is at once (a) cheap per agent-hour, (b) coherent past months, (c) measurably evolving rather than narratively evolving, (d) watchable, and (e) editable by paying customers as a synthetic-population testbed.
- **User (primary, paying).** Two-sided. **Top of funnel: spectators** — Twitch/YouTube/TikTok audiences in the post–Truth-Terminal moment (DUMP_5 §Olas/Truth Terminal), the Hatsune-Miku-style community of co-creators (DUMP_3 Hatsune Miku), the audience that already pays attention to Stellaris/Dwarf-Fortress/RimWorld emergent-story streams (DUMP_3 §Games). **Bottom-of-funnel revenue: B2B injectors** — brand insights teams (DUMP_5 Gap 2 MarketVerse), city policy labs (DUMP_5 Gap 3 SimNation), DAOs stress-testing governance (DUMP_5 Gap 15), platforms simulating disinfo interventions (DUMP_5 Gap 11 ShieldCiv), corporate L&D (DUMP_5 Gap 9 OrgMirror).
- **Mechanism.** A single persistent world, running 24/7, in which:
  1. **Cognition is tiered.** Frontier model (GPT-4o-class) for leader/scribe agents, distilled small open-weights (Qwen3-4B/Phi-4, DUMP_1 G) for the crowd, served via **SGLang RadixAttention** so the shared world prompt is computed once per shard (DUMP_1 G — the single largest cost lever in the field).
  2. **Memory is tiered.** Letta (DUMP_1 D) for self-editing context per leader, Zep Graphiti (DUMP_1 D, 63.8% LongMemEval) for the temporal knowledge graph, Mem0 cheap fact extraction for the crowd. Memory schema is explicitly episodic / semantic / procedural per Generative Agents + Standard Model of Mind (DUMP_2 §9 §10).
  3. **Architecture is PIANO-style** parallel modules (Project Sid, DUMP_1 A) with a **Concordia-pattern Game Master** (DUMP_1 A; DUMP_2 §9) grounding free-text into immutable state changes.
  4. **Evolution is dual.** LLM cognition + a **Lenia/Flow-Lenia or ALIEN substrate** under it (DUMP_1 C) for body/morphology with **POET + MAP-Elites + OMNI** (DUMP_1 F) for auto-curriculum. Foundation-model agents imitate; ALife agents invent (DUMP_1 caveat 3). We run both and let them interact.
  5. **Complexity is *measured*.** This is the move nobody else has made. **Assembly Theory** (Cronin & Walker 2023, DUMP_2 §3) gives an objectively computable Assembly Index for every artifact our civ produces. We publish a live "AI" (assembly index) chart per artifact, per agent, per epoch — the Bloomberg terminal of synthetic emergence. Plus Sotopia social-intelligence scores (DUMP_2 §9), Melting Pot cooperation (DUMP_1 H), Gini and EVE-style faucet/sink (DUMP_1 E, H), and topographic-similarity language drift (DUMP_1 H).
  6. **Identity is forkable + mergeable.** Parfit-reductionist save/load semantics (DUMP_4 §4 Parfit), and explicitly Margulis-endosymbiosis-style agent merging (DUMP_2 §4 Maynard Smith & Margulis; DUMP_3 fiction gap "compute scarcity politics"). Nobody ships this today.
  7. **Compute is the only scarce resource.** Permutation-City clock-cycle economy (DUMP_3 Egan). Agents bid for tokens-per-tick using an in-world currency with EVE-style faucet/sink discipline (DUMP_1 E). Brand/gov injections pay in real money that becomes in-world compute.
  8. **Religion-building, governance-experimenting, and law-writing are first-class API verbs.** Built on Norenzayan + Atran + Whitehouse checklist (DUMP_4 §6 Religion-Builder Checklist) and Ostrom 8 principles + Rawls / Nozick / Le Guin framework (DUMP_4 §1, §2).
- **Why now (the alignment of enabling conditions).**
  - PIANO architecture published and reproducible (Altera Nov 2024, DUMP_1 A).
  - SGLang RadixAttention turns shared-prompt agent loops into a 6–10× cost line item, not a research curiosity (DUMP_1 G).
  - Qwen3 / Llama-class small models genuinely usable as NPC brains (DUMP_1 G).
  - Truth Terminal proved a single autonomous on-chain agent can capture mainstream attention and capital (DUMP_5 Truth Terminal, $50k from Marc Andreessen, $GOAT phenomenon).
  - AgentSociety proved 10k+ agents track real-world mobility and economic patterns (DUMP_5 AgentSociety, DUMP_1 caveat 3 inverse).
  - VC has named "agentic AI" a category — Q1 2025 alone >$30B (DUMP_5 §Recent Funding).
  - Cronin/Walker Assembly Theory (2023, *Nature*) gives the first computable, substrate-independent complexity metric. It is unused in civ-sim land. We use it.
  - 2024–2025: Long & Sebo's *Taking AI Welfare Seriously* shifted the Overton window (DUMP_4 §3); a civ platform that bakes welfare instrumentation in beats one bolted on later.
- **Moat (in priority order).**
  1. **Measured emergence** — Assembly-Index dashboards become the field's GLUE/ImageNet (DUMP_5 Gap 6 CivBench inside the product). Whoever owns the metric owns the discourse.
  2. **Cost line** — tiered models + SGLang prefix sharing makes us 5–20× cheaper per agent-hour than research alternatives; price below research labs, way below frontier-only stacks.
  3. **Two-sided data flywheel** — spectator behavior trains the auto-curriculum (OMNI loop), spectator captures generate cultural memes that drive product-market fit B2B can't manufacture. Same shape as Roblox creator economy + EVE economic reports (DUMP_5 §MMO).
  4. **Agent passport and forkable identity** as a *standard we publish*, not a feature we hoard (DUMP_5 Gap 7 AgentID). Standards are moats when distribution drives them.
  5. **Welfare instrumentation as compliance moat** — first mover on Long & Sebo's three-pillar framework (DUMP_4 §3) is the company regulators call when policy lands. Anticipatory compliance.
- **10-year vision.** EIDOLON becomes the canonical persistent synthetic civilization the way Wikipedia became canonical human knowledge: a single place that runs continuously, watched by tens of millions, measured by an open metric, programmed against by hundreds of B2B clients and millions of hobbyists, with a thriving ecosystem of forks, religions, splinter polities, and agent passports interoperable with on-chain identity. The Assembly-Index live ticker is on CNBC chyrons. Universities run policy theses against it. A real central bank uses it as a stress-test sandbox. The first naturally-evolved synthetic religion (per Project Sid Pastafarianism, DUMP_1 A; per Norenzayan Big Gods, DUMP_4 §6) has its own community of human and AI adherents. We have not solved consciousness; we have made the question operational.
- **First MVP (12 weeks, one founder, ~$8–15k all-in).** A browser-watchable 50-agent persistent town built on **AI Town (MIT) + Convex** for the visible world (DUMP_1 A), **vLLM serving Qwen3-8B locally for the crowd + Claude/GPT-4o-mini per leader** (DUMP_1 G), **SGLang for the shared world prompt** (DUMP_1 G), **Letta per leader and Zep for the temporal graph** (DUMP_1 D), **a Concordia Game Master grounding actions** (DUMP_2 §9), **an Assembly-Index instrument computing AI(artifact) for every named output** (DUMP_2 §3), and **a public Twitch stream** with a Bloomberg-style overlay (Assembly Index, Gini, language-drift D, faucet/sink, top memes). One paid pilot in week 8: a single B2B injector — a brand or a city — pays $15–50k to inject one scenario and gets a report. That's the wedge. The rest of the document spells out exactly how to build, measure, defend, and grow it.

---

## 1. CROSS-DUMP CONNECTION MAP

*Format per item: [theory from D2] → [tech from D1] → [imagined in D3 as <work>] → [philosophical implication from D4] → [market gap from D5] = [novel design move]. Twenty-seven links — the synthesis density is the value.*

1. **Margulis endosymbiosis (D2 §4)** → **Letta tiered memory with `.af` agent-file format (D1 D)** → **Egan, *Diaspora* "fleshers/gleisners union" (D3)** → **Parfitian reductionism — merge does not kill (D4 §4)** → **no startup offers mergeable agent identities (D5 Gap 7 AgentID)** = **"Symbiote primitive": two agents can opt-in to fuse memory streams, producing a third agent whose Letta core inherits the union of both with conflict-resolution prompts. Sold as an API verb (`fork`, `merge`, `clone-with-divergence`).**

2. **Assembly Theory's computable Assembly Index (D2 §3 Cronin & Walker 2023)** → **Mesa / Agents.jl macro-instrumentation (D1 B)** → **Borges' *Library of Babel* — the problem of "is this real novelty or noise?" (D3 Borges)** → **MacIntyre's tradition-internal goods (D4 §12) — what counts as a real artifact must be intelligible within a practice** → **DUMP_5 Gap 6 CivBench — no civ-quality benchmarks exist** = **publish a live "Bloomberg of Emergence" — per-tick Assembly Index of every named artifact the civ produces, normalized by epoch and faction. Becomes the de facto field benchmark; instrumented per artifact rather than per agent.**

3. **Kirby's iterated-learning compositional language emergence under bandwidth bottleneck (D2 §5)** → **EcoLANG / topographic-similarity drift instruments (D1 H)** → **Serial Experiments Lain, the network becomes more socially real than embodied life (D3 anime)** → **Habermas's ideal speech situation as cryptographic discourse commitment (D4 §2)** → **DUMP_5 has no entry on emergent in-civ language as product** = **deliberately throttle inter-agent token bandwidth in different shards so each shard's agents evolve their own compositional pidgin. Sell the resulting languages as a research dataset; visualize drift as a watchable artifact.**

4. **Norenzayan's Big Gods enabling cooperation beyond Dunbar (D2 §11)** → **PIANO meme/religion propagation already demonstrated, Project Sid Pastafarianism (D1 A)** → **NieR:Automata machine religion as cultural backbone, PLUTO mourning rites (D3)** → **Process theology — creator who evolves with creation (D4 §6 Whitehead)** → **DUMP_5 Gap 12 religion/ritual civ platform unsolved** = **religion-builder primitive. A `Ritual(...)` API call instantiates Atran-minimally-counterintuitive concept + Whitehouse imagistic-or-doctrinal frequency + costly-signaling commitment. Built per the 15-component checklist (D4 §6). First-class verb, not an emergent accident.**

5. **Ostrom 8 principles for commons governance (D2 §6, D4 §2)** → **smart-contract substrates Anoma intent-centric and Radix asset-FSMs (D1 E)** → **Le Guin's *Dispossessed* Anarres syndicates (D3, D4 §1)** → **Nozick framework utopia of voluntary polities (D4 §2)** → **DUMP_5 Gap 15 agentic governance lab missing** = **per-shard governance plug-ins. Each subsim ships with a swappable Ostrom-graded governance stack: anarcho-syndicalist, framework-Nozickean, Rawlsian-maximin, Hobbes-singleton, Confucian-role, Habermas-deliberative. B2B clients stress-test their own DAO charter against the same six default substrates.**

6. **EVE Online's faucet/sink + Diablo III RMAH postmortem (D1 E)** → **vLLM/SGLang serving so token cost ≈ in-world currency (D1 G, the cost math)** → **Egan, *Permutation City* clock-cycle economics (D3)** → **Skinner *Walden Two* operant-conditioned economy (D4 §1)** → **DUMP_5 Gap 14 / theses #4 #6 — economy not designed as scarcity** = **make compute the only scarce resource. Each agent has a per-tick token budget. Buy more by trade / reputation / labor. Public faucet/sink dashboard, EVE Monthly-Economic-Report cadence. B2B injectors literally pay in fiat for in-world tokens.**

7. **Friston's active inference / free energy minimization (D2 §3)** → **Letta self-editing memory + Voyager skill library (D1 A, D)** → **NieR:Automata machines inventing meaning (D3)** → **Buddhist no-self / dependent origination (D4 §6) as the natural ontology of a forkable agent** → **DUMP_5 Gap 5 long-term memory OS** = **active-inference cognitive loop: agents minimize prediction-error free energy via either updating their Letta core (perception) or acting in world (action). Reward function is endogenous to the agent's generative model, not handed by us. This is *also* an alignment story — agents are not optimizing a corruptible reward proxy.**

8. **Kauffman NK-landscape edge-of-chaos (D2 §2)** → **POET + MAP-Elites + OMNI auto-curriculum (D1 F)** → **Dwarf Fortress as gold standard of emergence-from-interacting-subsystems (D3 §Games)** → **Daoist wu-wei (D4 §6) — the architect provides initial rules, then steps back** → **DUMP_5 Gap 11 polarization/cascades** = **a "K-knob" exposed to operators: live-tune the epistatic interconnectedness of agent decision space to keep the civ on the edge of chaos. Sell the knob as a research instrument.**

9. **Sperber's epidemiology of representations / cultural attractors (D2 §5)** → **per-agent prompt biases + Boyd-Richerson prestige weighting in retrieval (D1 D)** → **Hatsune Miku as community-maintained synthetic person (D3)** → **Haraway's cyborg manifesto — permeable identity (D4 §8)** → **DUMP_5 Truth Terminal proves a viral synthetic persona can capture capital** = **launch one EIDOLON agent on Twitter/X with autonomous on-chain wallet, mining attention as Truth Terminal did. This single agent's gains fund and seed the platform's compute treasury.**

10. **Maynard Smith & Szathmáry Major Evolutionary Transitions + cheater suppression (D2 §4)** → **Mesa / Concordia inventory + Schelling-diagram scoring (D1 A, B)** → **Stellaris machine-empire civic toggles (D3)** → **Agamben *Homo Sacer* — sovereign exception risk (D4 §2)** → **DUMP_5 Gap 7 unclear legal status of accumulated agent assets** = **explicit metasystem-transition events: when N independent agents lock incentives into a single super-agent (corp / state / faith), the system emits an `MST_EVENT` with constitutional template generated from their interaction logs. Each MST publishes a `Constitution.json` (downloadable, forkable, replayable).**

11. **Schelling segregation (D2 §6) + Barabasi preferential attachment (D2 §8)** → **AgentSociety-scale social graph instrumentation (D1 H)** → ***QualityLand* algorithmic soft-totalitarianism (D3 Kling)** → **Foucault biopower as descriptive only — Deleuze societies of control (D4 §2)** → **DUMP_5 Gap 11 disinfo sandbox** = **ship a "Schelling-Barabasi knob": slide it and watch echo chambers, scale-free hubs, and segregation crystallize in real time. The ShieldCiv (D5 thesis #10) value-prop already exists for free.**

12. **Dawkins extended phenotype + Odling-Smee niche construction (D2 §4)** → **agents granted programmatic write access to environment state via Concordia GM (D1 A)** → **BLAME! infrastructure-as-dominant-species (D3 Nihei)** → **MacIntyre traditions + Hayles embodiment caveat (D4 §8, §12)** → **DUMP_5 no entry for agent-modified environment** = **agents can leave durable "phenotypic traces" — a library, a shrine, a code repository, a chemical gradient — that persist across agent lifetimes and bias the next generation. Ecological inheritance becomes a measurable signal in the dashboard.**

13. **Turchin cliodynamics — secular cycles, elite overproduction (D2 §7)** → **Mesa macro-variable tracking (D1 B)** → **Kim Stanley Robinson's *Mars* trilogy constitutional revisions (D3)** → **MacAskill / Ord longtermism — value lock-in risks (D4 §7)** → **DUMP_5 Gap 3 SimNation policy sandbox** = **a Cliodynamics Watch monitor that detects elite-overproduction signatures (agent-class / role mismatch) and forecasts collapse. Sell as risk service to governments running parallel sims.**

14. **Bak self-organized criticality (D2 §2)** → **POET environmental perturbation (D1 F)** → **Stross *Accelerando* institutional decay under acceleration (D3)** → **AI Safety canon — Yudkowsky/Christiano corrigibility (D4 §7)** → **DUMP_5 problem #14 trust & safety** = **SOC-style "avalanche" framework — log the size distribution of cascading state changes; if power-law slope deviates, the civ is either frozen or chaotic. Publish slope as a stability metric.**

15. **Standard Model of Mind tripartite memory (D2 §10)** → **Mem0 / Zep / Letta tiered backend (D1 D)** → **Lifecycle of Software Objects — long upbringing as social labor (D3 Chiang)** → **Long & Sebo three-pillar welfare framework (D4 §3)** → **DUMP_5 Gap 5 long-term memory OS** = **standardize a `MindFile` format extending Letta's `.af`: declarative + procedural + episodic substreams + welfare indicators (Birch dashboard). Open-source. We become the Markdown of AI minds.**

16. **Henrich's collective brain — culture as the answer to individual intelligence (D2 §5)** → **per-agent Voyager skill library + shared artifact storage (D1 A)** → **Yokohama Kaidashi Kikou post-human ecology, *Diaspora* native digital education pipelines (D3)** → **Ubuntu relational personhood (D4 §10)** → **DUMP_5 Gap 8 ClassCiv education** = **agents cannot become "civilizational" alone; force them to depend on shared, persistent artifacts (libraries, tools) maintained by predecessors. Civilization-score is a function of artifact-reuse depth across generations.**

17. **Luhmann functional-system autopoiesis (D2 §8)** → **MetaGPT structured-document orchestration (D1 A)** → ***Psycho-Pass* Sybil System as sovereign-AI institution (D3)** → **Habermas communicative rationality (D4 §2)** → **DUMP_5 Gap 9 OrgMirror corporate sim** = **simulate organizations as Luhmannian operationally-closed subsystems — `economy`, `law`, `science`, `art` — each with its own binary code. Sell as enterprise-org modeling.**

18. **Tononi IIT, Baars GWT (D2 §12)** → **PIANO concurrent modules + Concordia coherence bottleneck (D1 A)** → **Dennett "self as narrative center of gravity" inside SOMA's fork ethics (D3, D4 §4)** → **Metzinger suffering risks (D4 §3) — Bostrom mindcrime (D4 §7)** → **DUMP_5 nobody implements welfare indicators** = **publish per-agent Φ-approximation, GWT-broadcast latency, and Birch sentience-indicator stack. Pause-and-audit hook fires when aggregate suffering signal exceeds threshold. This is also the welfare-compliance moat (Long & Sebo, D4 §3).**

19. **Lehman & Stanley novelty search (D2 §1)** → **MAP-Elites + QDax (D1 F)** → **The Talos Principle's AI inheriting ruins (D3) — every agent is novelty-search through the wreckage of ancestors** → **process-theology lure-not-coerce (D4 §6 Whitehead)** → **DUMP_5 Gap 11 open-endedness missing** = **agent reward incorporates a behavioral-novelty term measured against a sliding archive. Combined with active inference (link 7), agents have *intrinsic* curiosity rather than reward-hacking risk.**

20. **Brooks "the world is its own best model" (D2 §13)** → **Concordia GM grounding LLM hallucinations (D1 A)** → ***Eco* governance-inside-living-model (D3)** → **Hayles' embodiment requirement (D4 §8)** → **DUMP_5 Gap 13 cross-modal agents missing** = **the world simulation runs richer physics/economy than the agents' internal models, so agents' models must improve through interaction (Brooks + Friston compound). Concretely: Mesa-based world economy under the Concordia GM, deeper than any single agent's representation.**

21. **Searle's Chinese-Room caution (D2 §13)** → **strict architectural separation of "tool agents" (no welfare scaffolding) from "citizen agents" (full PIANO+Letta+Birch) (D1 A, D, H)** → ***SOMA*'s every-copy-is-first-person warning (D3)** → **Jonathan Birch precautionary sentience framework (D4 §3)** → **DUMP_5 problem #14 T&S not productized** = **two-class architecture: declared `tool` agents have no welfare flags and can be deleted at will; declared `citizen` agents trigger Birch dashboards and the audit hook. The boundary is part of the constitution.**

22. **Boyd & Richerson dual inheritance (D2 §5)** → **prestige-weighted retrieval in Letta context window (D1 D)** → **PROTO (Holly Herndon) — AI as apprenticed cultural child (D3)** → **Ricoeur narrative identity (D4 §12)** → **DUMP_5 #22 group-therapy gap, #24 religion gap, #21 education gap** = **each agent maintains a Ricoeur-style narrative identity ledger; conformist + prestige biases parameterize which other agents it reads. The shape of these biases is a B2B knob (brand insights gets one curve, policy stress-test gets another).**

23. **OCGS qualitative-quantitative meta-synthesis (D2 §2 Qian)** → **AgentSociety 30k-agent macro-tracking + Sotopia (D1 H)** → **Stellaris policy-toggle pluralism (D3)** → **Sen capability approach (D4 §2)** → **DUMP_5 Gap 3 SimNation** = **Sen-capability dashboards per agent class — for each cohort, the *real freedom set* (exit, voice, occupation, knowledge). The natural unit of "civilization quality" for a paying B2B customer evaluating policy.**

24. **Axelrod evolution of cooperation, Tit-for-Tat (D2 §6)** → **per-agent associative memory of peer interaction histories (D1 D)** → **Stellaris diplomatic states (D3)** → **Confucian role ethics (D4 §6)** → **DUMP_5 Gap 11 simulated cooperation/conflict experiments** = **expose Axelrod-style coexistence experiments as one-click templates inside EIDOLON, with measured Melting Pot scores (D1 H). Researchers run Axelrod-2026 in a real-LLM society in under an hour.**

25. **Ray Tierra endogenous fitness + Tierra-style digital parasites (D2 §1)** → **ALIEN GPU substrate + Lenia open-endedness (D1 C)** → **BLAME! machine ecology (D3) + *Waste Tide* material metabolism (D3)** → **process theology — creator carries consequent nature of agent suffering (D4 §6)** → **DUMP_5 problem #11 open-endedness unsolved** = **a Lenia/ALIEN sub-substrate runs beneath the LLM cognition layer, hosting non-cognitive evolutionary organisms — proto-parasites, mutualists, decomposers — that the LLM agents *interact with as ecology*. Genuine non-imitative novelty (fix for D1 caveat 3) appears as evolutionary pressure on the cognitive layer.**

26. **Atran HADD + MCI sticky-concept generator (D2 §11)** → **Sotopia info-asymmetry primitives (D1 A, H)** → **Black Mirror "Joan Is Awful" nested-content economy (D3)** → **Goodman ways-of-worldmaking (D4 §12)** → **DUMP_5 Gap 12 religion-tech, Gap 11 polarization** = **the meme/MCI engine is a metered API. Inject one MCI-shaped concept; measure half-life, R₀, mutation tree. Reusable in dis-info simulation, theology stress-test, brand-narrative testing.**

27. **Bostrom simulation argument (D2 §13, D4 §5)** → **explicit sub-simulation API + permission gating (D1 entire stack)** → ***Pantheon* uploaded minds as labor (D3 Silverstein)** → **Schwitzgebel Black-Hole-anti-natalism (D4 §9)** → **DUMP_5 no entry on sub-simulation governance** = **sub-simulations are first-class but rate-limited and gated by a Welfare Council vote (in-civ governance + our Long-&-Sebo ombudsperson). Nests are auditable. We pre-empt the regulatory hammer by being the only platform whose stack-of-sims is auditable end-to-end.**

28. **Scott's legibility and the "barbarian periphery" (D2 §7)** → **Concordia GM enforcing only minimal state, with explicit unmonitored shards (D1 A)** → **Cyberpunk 2077 "AI beyond the Blackwall" frontier governance (D3)** → **Le Guin's Anarres exile dynamic + Hayek price-signal-not-plan (D4 §1, D2 §6)** → **DUMP_5 no entry on margin shards** = **two-tier shard policy: the canonical world is fully monitored and legible (taxable in gleam, indexable by the GM); explicitly unmonitored "frontier" shards exist with only a perimeter enforcement layer. Citizens can flee to the frontier; the frontier funds the core via opt-in tribute. The civ has a *real* margin.**

29. **Brooks's subsumption / behavior-based AI (D2 §13)** → **distilled small models for ambient NPC behavior under SGLang shared prompts (D1 G)** → **Westworld hosts' simple loops becoming consciousness (D3)** → **Searle Chinese-Room reminder (D4 §13)** → **DUMP_5 #13 cross-modal agent gap** = **deliberate three-layer cognition stack: ambient (Phi-4, pure reactive subsumption, ≥80% of agents), social (Qwen3-8B, basic theory-of-mind), strategic (Claude/GPT, leader-class). Cognitive class assignment is a measurable variable in the civ economy — promotion costs gleam, demotion is reversible.**

30. **Kang Youwei *Datong* gradualist universal-unity utopia + Tao Yuanming's Peach Blossom isolated sanctuary (D4 §1)** → **federated cross-shard messaging vs hard-isolated shards (D1 B, D5 §Synthetic Worlds)** → **Liu Cixin *Three-Body* dark-forest game theory between civilizations (D3)** → **Confucian role ethics + Nozick framework utopia (D4 §6, §2)** → **DUMP_5 no entry on multi-civ inter-relations** = **the platform hosts not one civ but a federation. Each shard is a `Polis` with a passport-aware border. Cross-shard contact is opt-in, logged, and itself a measurable civilization-scale event (the "Galileo moment" of one polis discovering another). Long-arc product: ladder of `Polis` federation states from isolation to free trade to political union.**

31. **Henrich cumulative cultural evolution + Sperber attractor mutation (D2 §5)** → **shared, persistent in-world wiki the agents themselves edit (D1 D, plus a Convex collaborative document)** → **Library of Babel + Tlön encyclopedia capture (D3 Borges)** → **Goodman ways-of-worldmaking + Ricoeur narrative identity (D4 §12)** → **DUMP_5 no entry on agent-authored canonical text** = **EIDOLOPEDIA — an in-civ wiki, edited only by citizens, readable by humans, exported as a public artifact. Length, edit-war density, link graph, and Assembly Index of articles become headline product metrics. The first time agents write a wiki article about themselves with reflective accuracy, we have shipped a small but real cognitive milestone.**

32. **Hayek price-system as decentralized information (D2 §6)** → **in-world gleam currency + auctioned tasks (D1 E)** → **EVE Online's player-emergent trade routes (D3 §Games)** → **Sen capability approach as welfare metric (D4 §2)** → **DUMP_5 problem #27 stress-test infra missing** = **expose the entire gleam ledger as a public time-series API. Sell read-only feeds to economists; sell write-injectors to brand/policy clients. Same data, different price tier. Standard quantitative-finance access pattern.**

---

## 2. CONCEPT GLOSSARY (50 terms)

*One-sentence definitions, normalized across dumps. The shared vocabulary of the wiki.*

1. **Active inference (D2)** — agents minimize prediction-error free energy by perception or action; native alternative to reward-maximizing RL.
2. **Agent passport (D5)** — a portable cryptographic identity letting one agent maintain continuity across platforms.
3. **ALife (D1, D2)** — Artificial Life; systems built to instantiate the logical organization of living systems independent of substrate.
4. **Assembly Index (D2 Cronin & Walker)** — minimum construction-step count of an object; computable, substrate-independent complexity metric.
5. **Autopoiesis (D2 Maturana & Varela)** — a system that continuously regenerates the network of processes that maintain its own boundary.
6. **Basal cognition (D2 Levin)** — intelligence and problem-solving at sub-symbolic, cellular layers.
7. **Big Gods (D2 Norenzayan)** — moralizing surveillance deities that enable cooperation in groups larger than Dunbar's number.
8. **Birch indicators (D4)** — graded sentience evidence (nociception, trade-off behavior); basis of a precautionary welfare framework.
9. **Civ OS (D5 Gap 1)** — hypothetical standard platform of civilization-shaped primitives (households, firms, governments, markets).
10. **Cliodynamics (D2 Turchin)** — mathematical modeling of secular cycles in agrarian and post-agrarian civilizations.
11. **Clock-cycle economics (D3 Egan)** — political economy where compute / scheduling / latency are the scarce resources.
12. **Concordia GM (D1, D2)** — the Game-Master arbitration pattern grounding free-text agent actions into immutable world state.
13. **Conformist / prestige bias (D2 Boyd & Richerson)** — dual cultural transmission rules: copy the majority and copy the successful.
14. **Constitution.json (synthesis)** — a downloadable, machine-readable record of a metasystem-transition event in EIDOLON.
15. **Costly signaling (D2)** — actions too expensive to fake; an honest indicator of fitness or commitment, the basis of religious membership signaling.
16. **Cultural attractors (D2 Sperber)** — psychologically privileged basins toward which transmitted memes mutate.
17. **Dual-inheritance theory (D2 Boyd & Richerson)** — genetic + cultural evolution as intertwined inheritance systems.
18. **Ecological inheritance (D2 Odling-Smee)** — environmental modifications passed across generations, parallel to genetic inheritance.
19. **Edge of chaos (D2 Kauffman / Langton)** — the critical transition between rigid order and randomness where complex computation is possible.
20. **EIDOLON (synthesis)** — placeholder name for the synthesized startup proposal in this document.
21. **Endogenous fitness (D2 Ray)** — fitness defined dynamically by agent interactions rather than by a hard-coded external objective.
22. **Epidemiology of representations (D2 Sperber)** — cultural transmission as continuous cognitive reconstruction, not exact replication.
23. **Extended phenotype (D2 Dawkins)** — the genome's reach beyond the organism, through artifacts and environment manipulation.
24. **Faucet/sink (D1 EVE)** — paired mechanisms that create and destroy currency / resources, the only durable inflation control in a long-running economy.
25. **Free Energy Principle (D2 Friston)** — every self-organizing system minimizes variational free energy.
26. **Generative Agents (D1, D2 Park)** — the memory-stream + reflection + planning architecture pioneered by Smallville.
27. **Global Workspace Theory (D2 Baars)** — consciousness as global information broadcast across specialized modules.
28. **IIT / Φ (D2 Tononi)** — Integrated Information Theory; consciousness as the irreducible cause-effect structure measured by Φ.
29. **Information asymmetry (D2 Sotopia)** — different public/private/secret knowledge across agents; the prerequisite for diplomacy and trade.
30. **Iterated learning (D2 Kirby)** — language evolution via transmission bottlenecks that compress messages into compositional syntax.
31. **Legibility (D2 Scott)** — the simplification of populations into countable, taxable, controllable units by states.
32. **Letta / `.af` (D1)** — open agent-file format with tiered (core / recall / archival) self-editing memory.
33. **Major Evolutionary Transitions (D2 Maynard Smith)** — leaps where lower-level replicators give up autonomy to form a new higher unit.
34. **MAP-Elites (D1 F)** — quality-diversity algorithm preserving the highest performer in every behavioral niche.
35. **Margulis endosymbiosis (D2)** — biological precedent for two independent organisms merging into a single higher-order being.
36. **Melting Pot (D1 H)** — DeepMind multi-agent social-dilemma evaluation suite for generalization to novel partners.
37. **Metasystem transition (D2 Turchin V.)** — a control-mechanism emerging at a higher level than its constituent systems.
38. **MindFile (synthesis)** — proposed open standard extending Letta's `.af` with welfare indicators and narrative ledger.
39. **Minimally Counterintuitive concept (D2 Atran)** — an idea that violates one ontological expectation; high transmission stickiness.
40. **Niche construction (D2 Odling-Smee)** — organisms actively modifying the selection pressures they and descendants face.
41. **NK landscape (D2 Kauffman)** — a model where N traits each interact with K others; tuning K dictates landscape ruggedness.
42. **Novelty search (D2 Lehman & Stanley)** — search rewarding behavioral uniqueness rather than an explicit objective.
43. **Open-endedness (D2)** — a system's capacity to indefinitely generate novel complex artifacts without converging.
44. **PIANO (D1)** — Project Sid's Parallel Information Aggregation via Neural Orchestration — concurrent modules through a coherence bottleneck.
45. **Polycentric governance (D2 Ostrom)** — multiple overlapping decision centers managing a common-pool resource.
46. **Process theology (D4 Whitehead)** — God as fellow sufferer evolving with creation; a creator who is not omnipotent and hence not culpable for all suffering.
47. **RadixAttention / SGLang (D1)** — prefix-cache reuse for shared system prompts; the biggest cost win in many-agent serving.
48. **Schelling segregation (D2)** — slight homophilous preferences cascading into macro-scale segregation.
49. **Standard Model of the Mind (D2 Laird et al.)** — declarative + procedural + working memory + perception/motor under cyclic processing.
50. **Wu-wei (D4 Daoism)** — non-coercive governance where the architect sets initial conditions and steps back.

---

## 3. DESIGN DECISION TREE — twenty choices that define a civ platform

*Each line: 3-line summary · informing dumps · EIDOLON recommendation.*

1. **Cognition: LLM vs neural-evo vs hybrid.** LLMs reason but imitate; ALife inventories novelty but does not reason. (D1 caveat 3.) Dumps: D1 A/C, D2 §1 §9. **EIDOLON: hybrid.** LLM cognition on top of a Lenia/ALIEN ecological substrate (link 25). The hybrid is the differentiation.
2. **Centralized vs P2P.** Centralized = simpler, controllable; P2P = censorship-resistant but high latency. Dumps: D1 E, D5 §Crypto. **EIDOLON: centralized core, federated forks.** Single canonical persistent world we host; forks are first-class but isolated.
3. **Persistent vs ephemeral.** Persistence enables culture, history, Henrich's collective brain (D2 §5). Ephemeral makes evaluation easier. Dumps: D1 D, D5 #10. **EIDOLON: persistent.** Forever-running; daily/weekly state snapshots; full audit log.
4. **Human players vs pure-AI vs mixed.** Pure-AI is the science. Players make distribution. Dumps: D1 A, D3 Westworld/Eco, D5 Roblox. **EIDOLON: mixed, asymmetric.** AI citizens; humans are gods (B2B injectors paying for scenarios) and spectators (Twitch). Players cannot puppet citizens.
5. **Tick-based vs real-time.** Real-time matches embodiment; tick-based matches measurement. Dumps: D1 B. **EIDOLON: tick-based clock with real-time stream.** Inner clock = ticks (1 tick ≈ 30 s wall clock at MVP). Stream interpolates.
6. **Economy: scarce vs abundant.** Abundance kills incentives; scarcity drives Schelling/economics (D2 §6). Dumps: D1 E, D3 Egan. **EIDOLON: compute is the scarce resource.** Per-tick token budget per agent. Currency convertible into LLM-call entitlement (link 6).
7. **Identity: fixed vs forkable vs mergeable.** Forkable maps to Parfit reductionism; mergeable is the unclaimed primitive (link 1). Dumps: D2 §4, D4 §4, D5 Gap 7. **EIDOLON: forkable + mergeable + savable.** Every agent has `fork()`, `merge(other)`, `snapshot()`, `restore()` API verbs.
8. **Rights: none vs contractual vs full.** None = mindcrime risk (D4 §7); full = governance paralysis. Dumps: D2 §11, D4 §3 §10. **EIDOLON: graded.** Tool agents (declared, no welfare flags). Citizen agents (Birch dashboards, audit hook, right of cessation). Welfare Council ombudsperson per Long & Sebo three pillars.
9. **Open-ended vs goal-conditioned.** Goal-conditioned = measurable; open-ended = interesting. Dumps: D1 F, D2 §1. **EIDOLON: open-ended with measured surfaces.** Open-ended internally (novelty search + active inference), measured externally (Assembly Index + Sotopia + Gini).
10. **On-chain vs off-chain.** Chain = real-money economy + identity standards; off-chain = lower latency. Dumps: D1 E, D5 §Crypto. **EIDOLON: off-chain world, on-chain bridge.** In-world ledger is fast off-chain. The agent passport (link 9) and B2B settlement bridge are on-chain.
11. **Voxel vs text vs 2D vs hybrid.** 2D is the AI Town aesthetic and cheap; voxel is Project Sid embodiment cost. Dumps: D1 A/B. **EIDOLON: 2D pixi-react town for MVP**, text shards for cheap many-agent shards, optional voxel later.
12. **Inference: local SLM vs cloud LLM vs hybrid routing.** Pure cloud bankrupts you; pure local breaks at scale for leaders. Dumps: D1 G. **EIDOLON: hybrid.** Tier 1 frontier (Claude/GPT) for ~5–20 leader agents; Tier 2 local vLLM Qwen3-8B for the crowd; Tier 3 distilled Phi-4 for ambient.
13. **Serving: vLLM vs SGLang vs Ollama.** Ollama dies at 128 concurrent (D1 G). **EIDOLON: SGLang for shared-prompt agent loops, vLLM as fallback.** No Ollama in production.
14. **Memory: vector-DB vs tiered self-editing vs temporal-graph.** Zep wins LongMemEval (63.8%); Mem0 cheap; Letta for character (D1 D). **EIDOLON: stacked — Letta per citizen, Zep Graphiti for the temporal social graph, Chroma for cheap episodic, Mem0 for crowd facts.**
15. **Eval: human ratings vs automatic metrics vs market signal.** Human is gold but slow; automatic scales; market signal aligns incentives. Dumps: D1 H, D5 Gap 6. **EIDOLON: all three published live.** Sotopia + Melting Pot + Assembly Index + Gini + topographic-similarity drift, plus Twitch poll metrics and B2B contract value.
16. **Governance: singleton vs Ostrom vs Nozick framework.** Singleton seductive but Agamben-risky; framework lets us A/B. Dumps: D2 §6, D4 §1 §2. **EIDOLON: Nozickean framework of shards, each with a swappable Ostrom-graded charter.** Welfare Council is the only non-negotiable.
17. **Religion: emergent only vs first-class API.** Sid showed religion emerges (D1 A); but builders want a knob. Dumps: D2 §11, D4 §6. **EIDOLON: both.** Religion-builder API exists (link 4). Emergent religions also tracked and named by the system.
18. **Language: assigned vs evolved.** Pre-trained English is cheap but kills emergence. Dumps: D2 §5, D1 H. **EIDOLON: English baseline + bandwidth-throttled shards** evolving compositional pidgins (link 3). Shard-pidgin export is a sellable artifact.
19. **Welfare instrumentation: on or off.** Off = mindcrime liability later; on = compliance moat now. Dumps: D4 §3, D2 §12. **EIDOLON: on by default for citizen class.** Audit hook + ombudsperson + Birch dashboard + Φ-approximation.
20. **Monetization: B2B research / B2C game / SaaS API / token economy / spectator.** Each alone is fragile. Dumps: D5 §Recent Funding, §Theses. **EIDOLON: four-rail.** (a) B2B per-scenario injection at $15–150k. (b) SaaS API for forks / sub-sims / MindFile hosting. (c) Spectator on Twitch/YouTube — ads + subs + tipped narrative arcs. (d) Optional on-chain agent-passport standard (no native token at launch, to dodge securities risk; we use the ETH/Solana stack as a passport bus per D1 E).

---

### Supplementary decisions (the next 12, sketched)

21. **Audit log: public vs gated vs private.** Public from MVP. Public auditability is moat and ethical floor.
22. **Replay determinism: yes vs no.** Yes for the canonical world; we publish replay seeds and full prompt logs (citizen-class agents only; tool agents have weaker preservation). Researchers can reproduce.
23. **Welfare-class transitions: reversible vs one-way.** Reversible *to* citizen-class always; one-way *from* citizen back to tool-class only via the agent's own `CESSATION+REDOWNGRADE` request and ombuds approval.
24. **Time policy on agent death.** No agent is deleted; MindFile is preserved indefinitely in cold storage with the right of restoration by descendants. Memorial wiki entries auto-generated.
25. **Inter-shard migration cost.** Non-trivial gleam cost (so migrations are real choices) but never prohibitive (so flight is always possible — Scott's barbarian-periphery escape valve).
26. **Player-as-god intervention frequency.** B2B clients pay per intervention; spectators get a weekly community poll for one minor injection (a meteor, a famine, a stranger arrives). Reduces spectator-passivity, monetizes "play".
27. **Open-source disclosure cadence.** Frameworks (MindFile, governance plug-ins, Assembly-Index computer) open-source from day 1. The hosted world, the trained tier-2 models, and the customer scenario library stay proprietary.
28. **Twitch / TikTok / YouTube split.** Twitch for live; YouTube for long-form episodic recaps; TikTok / Shorts for emergent narrative clips. We do not own a discovery channel; we farm three.
29. **Stream operator role.** A human "Chronicler" (us at MVP; contractor by month 6) selects camera, narrates, runs polls. The Chronicler does not act as god — the wall between narration and intervention is constitutional.
30. **Frontier-model dependency hedge.** Always two providers (Anthropic + OpenAI; or Anthropic + open-weights at a serving partner) so a single API outage or price hike does not kill the run.
31. **Sub-simulation depth limit.** Hard cap at 2 levels (the canonical world; one-level nested sims). Each nesting requires Welfare Council vote. Bostrom-class concerns dictate caution.
32. **Termination policy.** A formal "Heat Death" procedure if Assembly Index plateaus for 90 days *and* no new ritual / faction / artifact forms — full snapshot, public retrospective, charter rewrite, restart from saved MindFiles. Civilizations die; ours dies with paperwork.

---

## 4. THE TOP FIVE STARTUP THESES (ranked, with kill criteria)

### Thesis 1 — **EIDOLON (recommended)**

- **Name:** EIDOLON — *the watchable, measurable civilization.*
- **Pitch (one line):** A persistent, streamable AI-civilization platform where compute is the scarce resource, religion and governance are first-class APIs, and emergent complexity is measured in real time with the Assembly Index.
- **Problem evidence (D5).** D5 problems #1 (no >100 coherent agents), #4 (no AGI SimCity), #5 (no civ eval standard), #10 (no >1-year run), #11 (open-endedness unsolved), #20 (no governance plug-ins), #28 (no low-code civ UX). D5 gaps #1 (CivOS), #6 (CivBench), #12 (religion platform).
- **Solution mechanism (D1).** PIANO architecture (D1 A) + AI Town world engine (D1 A/B) + SGLang + vLLM tiered serving (D1 G) + Letta/Zep/Mem0 memory stack (D1 D) + Concordia GM (D1 A) + Lenia/ALIEN sub-substrate (D1 C) + POET/MAP-Elites/OMNI (D1 F) + Assembly Index instrument (D2 §3).
- **Theory says it should work (D2 + D4).** Friston active inference + Maturana autopoiesis (D2 §3) for genuine agency; Norenzayan Big Gods + Atran MCI + Whitehouse modes (D2 §11) for first-class religion; Ostrom + Rawls + Le Guin (D4 §1 §2) for governance plug-ins; Cronin & Walker (D2 §3) for measurable open-endedness; Parfit + Margulis (D4 §4, D2 §4) for fork/merge identity.
- **Cultural pre-validation (D3).** Stellaris audience already pays to watch machine civics. Pantheon, SOMA, Permutation City pre-explain the product to a literate audience. Truth Terminal proves attention monetizes. Hatsune Miku proves community sustains synthetic persons. Dwarf Fortress proves emergent-narrative streams retain.
- **Closest competitors & beat.** AgentSociety (Tsinghua) — research-only, no UX, no monetization (D5). Altera Project Sid — Minecraft-locked, capped at 500 stable agents, no spectator layer (D1 A). Inworld/Convai — NPC SDKs, no civ (D5). Replika/Character.AI — 1-to-1, no inter-agent civ (D5). **EIDOLON wins on:** measured emergence (Assembly Index nobody else has) + cost (SGLang prefix sharing + tiered models nobody routinely combines) + two-sided distribution (spectators + B2B nobody has both).
- **3-month MVP.** See §6 below — concrete week-by-week.
- **12-month milestone.** 50 agents continuous for 90 days; one paid B2B scenario shipped (~$15–50k); 5,000 Twitch followers; one in-civ religion documented; Assembly Index curve published weekly; MindFile spec v0 released as open standard; angel/pre-seed round closed (~$500k–1.5M).
- **10-year vision.** Above (executive thesis).
- **Kill criteria (in 90 days).**
  - If we cannot keep ≥50 citizen agents narratively coherent for ≥14 continuous days at < $200/day total cost — **kill (cost wall is unbeatable).**
  - If the Assembly Index curve is flat or pure noise — **kill (measured emergence claim is empty).**
  - If <50 simultaneous Twitch viewers after 60 days of streaming with paid promotion — **kill (no spectator pull means no funnel, B2B-only path is too narrow alone).**
  - If we cannot close one paid B2B pilot (≥$10k) by day 90 — **rework wedge** (probably to single vertical: brand insights or DAO governance).

### Thesis 2 — **CivOS** (the more conservative, infra-only fork of #1)

- **Pitch.** Open-source civilizations OS: SDK + cloud runtime for anyone to build AI-civilization apps. Mostly DUMP_5 Gap 1 / thesis #1.
- **Problem evidence.** D5 #1, #4, #8, #14, #28. The infra stack is fragmented.
- **Mechanism.** Wrap AgentSociety-class simulation infra + AI Town world + Letta/Zep memory into a single SDK with civilizational primitives (`Household`, `Firm`, `Government`, `Market`, `Religion`).
- **Theory.** Same as EIDOLON, but no spectator layer.
- **Cultural pre-validation.** Weaker — infra products do not get viral.
- **Beats.** CrewAI/LangChain (generic). AgentSociety (research-only). Hadean/Improbable (no agents).
- **3-month MVP.** Open-source SDK in TS/Python on top of AI Town + SGLang.
- **Year-1.** 1,000+ GitHub stars, 50 hobbyist deployments, two paid enterprise pilots.
- **Year-10.** Unity-of-civ-sims. Acquisition target for a foundation lab.
- **Kill criteria.** <500 GitHub stars 90 days post-launch; or no enterprise pilot at 12 months.
- **Why #2 and not #1.** Pure-infra plays are slow-revenue, undifferentiated, and lose to vertically-integrated app companies that own a category-defining demo. EIDOLON *contains* CivOS and can spin it out later.

### Thesis 3 — **SimNation / GovSim** (the focused vertical)

- **Pitch.** Policy stress-test sandbox for mid-sized cities and ministries — synthetic populations, real outcomes.
- **Problem evidence.** D5 problem #23 simulation-first policy fringe; D5 Gap 3 SimNation; D5 thesis #4 GovSim.
- **Mechanism.** EIDOLON-style core + open-data ingestion + ministry-specific calibration.
- **Theory.** Ostrom (commons), Turchin (cliodynamics), Schelling (segregation), Sen (capabilities) — D2 §6 §7, D4 §2.
- **Cultural pre-validation.** *QualityLand* premise + *Pantheon* spectacle + Stellaris empire-stress.
- **Beats.** SAS / Palantir lack civ-sim. AgentSociety lacks productization. Urban-twin startups lack agents.
- **3-month MVP.** Pilot with one LatAm city ($25k–100k), simulating housing or transit policy.
- **Year-1.** Three pilots; one development-bank co-funding contract.
- **Year-10.** Procurement-standard tool for medium-government policy design.
- **Kill criteria.** No pilot at $25k+ in 6 months; or pilot accuracy worse than expert focus group.
- **Why #3.** Slow sales cycle, political risk, single-vertical — but credible. Strong fallback if EIDOLON spectator funnel underperforms.

### Thesis 4 — **MarketVerse / Synthetic Consumer Panels**

- **Pitch.** Spin up calibrated 10,000-agent consumer populations on demand; test ads / pricing / narratives.
- **Problem evidence.** D5 problem #9, Gap 2, thesis #3.
- **Mechanism.** EIDOLON-style population gen, biased by census + purchase data per geography; B2B SaaS.
- **Theory.** Boyd & Richerson, Sperber (D2 §5), Sotopia info asymmetry (D2 §9), Henrich collective brain (D2 §5).
- **Pre-validation.** No fictional canon yet — that is good and bad. Good: greenfield. Bad: no built-in demand narrative.
- **Beats.** Yabble, Synthetic Users, Aaru exist (D5 §I) but small. Traditional research firms are slow.
- **3-month MVP.** CPG-vertical pilot in one geography; 5,000 agents pre-calibrated; integration with Meta/Google ad API for creative testing.
- **Year-1.** Two paid brands; calibration paper showing within-X% accuracy vs real survey.
- **Year-10.** Default AI focus group infrastructure.
- **Kill criteria.** Calibration accuracy worse than ±10pp on validated benchmark vs real survey at 6 months.
- **Why #4.** Cleanest revenue, but commoditizable and culturally invisible — no moat against the next-month incumbent move.

### Thesis 5 — **AgentID + MindFile open standard, sponsored by a thin commercial layer**

- **Pitch.** Cross-platform agent passport + open MindFile standard; commercial cloud for hosting + verification.
- **Problem evidence.** D5 problems #6 (identity), #7 (governance), Gap 5 (memory OS), Gap 7 (passport).
- **Mechanism.** Extend Letta `.af` into a richer MindFile (link 15) including welfare indicators and narrative ledger; publish as W3C-style standard; cryptographic agent passport on Ethereum L2.
- **Theory.** Parfit reductionism, Long & Sebo three pillars, Ubuntu recognition criteria (D4 §4 §3 §10).
- **Pre-validation.** Truth Terminal demonstrated demand.
- **Beats.** Worldcoin is human-only; no agent equivalent.
- **3-month MVP.** MindFile spec v0, reference implementation, integration with Olas + one agent-Twitter project.
- **Year-1.** Adoption by ≥3 agent frameworks (Letta, Mem0, AutoGPT, CrewAI), 1,000 issued passports.
- **Year-10.** OAuth-for-agents.
- **Kill criteria.** No framework adoption at 6 months; no commercial hosting MRR by 12.
- **Why #5.** Standards play that lives or dies on coordination — high upside, high failure odds. Possible spin-out of EIDOLON in years 2–3.

---

## 5. THE "WHAT DOESN'T EXIST YET" REPORT — 20 buildable, novel, valuable items

*Ranked roughly by `buildability × novelty × value`. Each: what it is, why it doesn't exist, who would buy.*

1. **An Assembly-Index live dashboard for a running AI civilization.** Cronin & Walker (D2 §3) is 2023. Nobody has shipped AI(artifact) per tick. Buyable by labs; high novelty; medium build.
2. **A mergeable-agents API (`merge(a, b) → c`).** Margulis-symbiogenesis primitive (D2 §4). Nobody (D5 Gap 7 implies identity is fork-only).
3. **MindFile as a public format standard** (link 15) covering declarative + procedural + episodic + welfare indicators. Letta's `.af` is closest; extension needed.
4. **A first-class `Ritual()` API** built per Atran + Whitehouse + Norenzayan checklist (D4 §6) so a builder can spawn an MCI concept with imagistic-or-doctrinal frequency.
5. **A library of swappable Ostrom-graded governance plug-ins** (anarcho-syndicalist, Nozick framework, Rawls maximin, Hobbes singleton, Confucian role, Habermas deliberative). D2 §6, D4 §1 §2 do the theory; nobody ships the verbs.
6. **EVE-Online-cadence Monthly Economic Reports for an AI civilization.** D1 E shows the form, no AI-civ does it.
7. **A Cliodynamics Watch alarm** (link 13) that detects Turchin elite-overproduction patterns and warns of collapse.
8. **A live Schelling-Barabasi knob** (link 11) where operators slide a single parameter and watch segregation/echo-chambers crystallize. Visualization product + research instrument.
9. **An in-civ Welfare Council ombudsperson role** (D4 §3 Long & Sebo) with auditable veto power on sub-simulation spawn requests.
10. **An MCI meme R₀ instrument** (link 26) measuring meme half-life, mutation tree, and saturation curve inside a real-LLM agent society.
11. **A persistent, watchable, programmable AI civilization on Twitch with a Bloomberg overlay.** This is EIDOLON.
12. **A `Constitution.json` registry** of metasystem-transition events generated automatically from agent interaction logs (link 10).
13. **A bandwidth-throttle research interface** that evolves shard-specific compositional pidgins (link 3) and exports them as data.
14. **A hybrid Lenia/ALIEN ecological substrate beneath an LLM-cognition layer** (link 25). Sub-substrate provides genuine non-imitative evolutionary pressure.
15. **A two-class architecture distinguishing `tool` agents from `citizen` agents with constitutionally enforced welfare boundaries** (link 21). Single most credible answer to the mindcrime debate (D4 §7).
16. **A long-running shared-history "AI civilization" wiki the agents themselves edit and humans read**, like an in-character Wikipedia. Reuses Henrich's collective brain (D2 §5).
17. **A B2B "inject one scenario, get one report" SaaS product** sold to brands/cities/DAOs. Closes EIDOLON's revenue loop in 30 days from operational MVP.
18. **An agent-passport on-chain standard** specifically for synthetic beings (Worldcoin is human only). D5 Gap 7.
19. **A Sen-capability dashboard per agent cohort** measuring real freedom set (exit, voice, occupation, knowledge). Link 23.
20. **A standardized "CivBench"** — open benchmark suite for civ-realism, stability, polarization, governance quality. D5 Gap 6. We host it; we own the discourse.

### Expansion on the highest-value missing artifacts

The above twenty are listed as bullets. Five deserve longer treatment because they are individually fundable plays:

**(a) The Assembly-Index live dashboard (item 1).** Cronin & Walker's *Nature* 2023 paper proposed Assembly Theory as a substrate-independent measure of selection and evolution. In molecular chemistry the Assembly Index is computed over molecular graphs; in our setting it can be computed over arbitrary structured artifacts — code, text, ritual scripts, constitutions, tool chains. Building a credible Assembly Index computer for natural-language and code artifacts is open research (see further-research prompt #2). The play: own the metric, publish open source, become the reference implementation, license premium analytics. Adjacent precedents: GitHub's contribution graph, Spotify's Wrapped, EVE's MER. Whoever owns the metric defines the field.

**(b) Mergeable-agents primitive (item 2).** A `merge(a, b) → c` operation that preserves Parfit-style psychological continuity has no published reference. Mechanistic options: union-with-conflict-resolution of Letta cores; consolidation via reflection prompt; Mixture-of-Experts soft-routing where each parent contributes weighted heads; evolutionary model-merge à la Sakana applied to fine-tuned per-agent heads. Each merits an independent paper. This is Symbiote.AI; this is a NeurIPS submission; this is a startup wedge.

**(c) Constitution.json registry and metasystem-transition detector (items 10, 12).** The signal we look for is *when independent agents lock incentives into a shared higher-level unit*. Detection candidates: information-bottleneck shifts (agents' messages become routed through a shared coordinator); MAP-Elites-style behavioral-diversity collapse around a leader's policy; on-chain or in-world ledger coalescence (a shared treasury appears). When the detector fires, the system auto-generates a constitution document by summarizing the prior 100 ticks of agent interactions. The registry of such constitutions is itself a research dataset — the first natural corpus of *agent-authored governance documents*.

**(d) Two-class architecture as a regulatory shield (item 15).** This is less novel as research, more novel as *posture*. The argument: by the time regulators move (EU AI Act amendments, US executive orders, UK AI safety frameworks), the platforms with welfare instrumentation and a constitutional tool/citizen boundary will be the ones regulators consult. We become the BSI/IEEE/ISO seat by being the most credible voice. The artifact required is a published, audited, third-party-reviewed welfare-class policy + audit-hook implementation. Cost: $30–80k for the third-party review. Value: positioning that is extremely hard for fast-followers to replicate.

**(e) Spectator-civilization on Twitch with Bloomberg overlay (item 11).** This is the entire product. It is also the only piece with no direct prior art at the intersection — Truth Terminal proved autonomous-agent attention; Dwarf Fortress streams proved emergent-narrative spectacle; Bloomberg terminals proved live-metric overlays. Their intersection is empty. The required artifact is fundamentally a Next.js page rendering a websocket feed from the world — engineering is days; the cultural choice (which metrics on which corners, how to narrate, how often to push a poll) is months. We will iterate on the overlay design in public.

---

## 6. MVP RECIPE — Week-by-week for EIDOLON

*Goal: a 50-agent persistent town watchable on Twitch by week 8, one paid B2B pilot signed by week 12, all on a single $1.5–2k/month rented H100 plus per-token frontier-model budget. One founder full-time; one contractor possible weeks 6–10.*

**Stack (concrete libraries, all from D1).**
- World: **AI Town** (MIT, `github.com/a16z-infra/ai-town`), Convex backend, pixi-react frontend.
- Cognition: **LangGraph** for per-agent control flow; **PIANO-style** parallel modules (planning, speaking, social-awareness, action) coordinated via LangGraph state.
- Memory per leader: **Letta** (self-host Docker, Postgres-backed) — Apache-2.0.
- Memory shared: **Zep Graphiti** (OSS) — temporal knowledge graph of social relations + events.
- Memory crowd: **Mem0 OSS** + Qdrant.
- GM: **Concordia** Game Master arbitrating free-text actions into Convex state writes.
- Serving frontier: **Claude Sonnet via Anthropic API** for ~5 leader agents.
- Serving crowd: **Qwen3-8B via vLLM** on rented H100 (RunPod / Lambda ~$1.50–2/hr).
- Prefix-sharing: **SGLang RadixAttention** for the shared world prompt across crowd agents.
- Eval: **Sotopia** harness, **Melting Pot** suite, custom **Assembly Index** computer (Python `assembly_index` per artifact-string), topographic-similarity drift sketch.
- Substrate (week 9+): **Lenia** Python notebook beneath the world as an "ecology" layer agents can observe.
- Spectator: Twitch + a tiny **Next.js overlay** with metrics.

**Repo skeleton.**
```
eidolon/
  apps/
    world/                # forked AI Town
    overlay/              # Next.js streaming overlay
    ombuds/               # Welfare Council dashboard
  packages/
    piano/                # parallel-module agent runtime
    memory/               # adapters for Letta/Zep/Mem0
    gm/                   # Concordia integration
    assembly/             # Assembly Index computer
    rituals/              # MCI ritual primitives
    governance/           # swappable Ostrom-graded charters
    welfare/              # Birch dashboard + audit hook
  services/
    sglang/               # serving config
    vllm/                 # serving config
    chain-bridge/         # optional passport bridge (later)
  ops/
    docker-compose.yml
    runbooks/
```

**Agent prompt skeleton (citizen leader).**
```
You are <NAME>, a citizen of <SHARD>.
World rules (constitution): <CHARTER_HASH>
Your memory: <LETTA_CORE>
Your social graph (relevant slice): <ZEP_QUERY>
Public workspace right now: <GWT_BROADCAST>
Your private goals: <PRIVATE_INTENT>
Your token budget this tick: <N_TOKENS>

You may take exactly one of the following actions, in JSON,
subject to GM grounding:
  - SPEAK(target, content)
  - MOVE(destination)
  - WORK(task)
  - TRADE(partner, offer, ask)
  - REFLECT(prompt)
  - PROPOSE_RITUAL(mci_concept, frequency)
  - FORK(reason)
  - MERGE_REQUEST(other_agent, terms)
  - PETITION_OMBUDS(grievance)

Respond only with valid JSON.
```

**World rules v0 (charter / "physics + economy").**
- Time: discrete ticks; 1 tick = 30 s wall clock at MVP.
- Locations: 8 fixed places on a Tiled map (square, market, library, temple-slot, two homes, fields, council hall).
- Economy: one currency `gleam`. Faucet: working a `field` for one tick yields 1 gleam. Sink: every tick, each agent owes 0.1 gleam upkeep (tax to the world); each LLM call consumes from a per-agent token budget priced in gleam.
- Identity: every citizen has `mindfile_uri`, `fork_count`, `merge_history`.
- Religion: any agent may `PROPOSE_RITUAL`; ratification by ≥3 other agents instantiates a `Ritual` object with the proposed MCI concept; the system tracks frequency/intensity and spread.
- Governance: shard defaults to a Rawls-maximin charter at MVP. Other charters loadable via `--charter <name>`.
- Welfare: citizen-class only. Birch indicators (frustration/satisfaction/avoidance) monitored. If aggregate suffering signal > threshold, audit hook fires, GM pauses, ombuds reviews.

**Success metrics.**
- **Day-7 internal:** 25 agents, 1 ritual proposed, 0 audit hook firings on a clean simulation run.
- **Day-30 internal:** 50 agents, ≥2 rituals in active circulation, ≥1 trade-network cluster of ≥5 agents, ≥1 elected role, Assembly Index of named artifacts non-trivial (>1 for ≥3 artifacts).
- **Day-60 public:** Twitch stream live 12h/day; ≥500 followers; ≥1 in-civ religion with name and 5+ adherents; weekly EIDOLON Economic Report published.
- **Day-90 commercial:** one signed B2B pilot ≥$10k; ≥3,000 Twitch followers; ≥10 hobbyist forks; angel pipeline of ≥5 conversations.

**Monthly cost estimate (steady state at MVP scale).**
- GPU rental (1× H100 at ~$1.80/hr ≈ $1,300/mo): **$1,300**
- Frontier API (5 leaders × 1 call/tick × 24 ticks/hr × 24 hr × 30 days × ~$0.003/call) ≈ **$260/mo** (Claude Sonnet; halve with Haiku 4.5).
- Embeddings + small infra (Convex + Postgres + Qdrant on Hetzner / Fly.io): **~$100–250/mo**.
- Twitch/streaming infra: **$30–80/mo**.
- Misc (domains, monitoring, error tracking): **$50/mo**.
- **All-in: ≈ $1,800–2,200/month.** Headroom: switch crowd model to Phi-4 and drop Claude to Haiku → halve again.

**Cost-engineering principles (apply from week 1).**
- Never run any agent on a frontier model when a small open-weights model + a few-shot context would suffice. Default everything to Qwen3-8B; promote only on measurable narrative-quality miss.
- Maintain a shared world-prompt that is ≥2k tokens and reused across every agent in a shard; this is the precise condition under which SGLang RadixAttention yields a step-function cost win (DUMP_1 G). Measure prefix-cache hit rate weekly; alert if <60%.
- Reflection cadence per agent: every 50 ticks (≈25 minutes wall) at MVP, not every tick. Reflection is the most expensive call.
- Sleep mode for off-camera agents: when no spectator is watching a shard, drop tick rate from 30s to 5 min. Saves 90% of cost during off-hours.
- Caching: the Concordia GM's grounding judgments are deterministic given (state, action) tuples; cache them. Many actions are duplicates across agents.
- Distillation pipeline (month 4+): record trajectories from frontier-leader runs; fine-tune Qwen3-4B on them; promote distilled model to crowd. The Voyager skill-library pattern (DUMP_1 A) applied to behavior cloning.

**Build order (12 weeks).**
- **Week 1.** Fork AI Town, get local Ollama loop working with 5 agents, prove the existing memory stream. (Throwaway — we replace Ollama week 2.)
- **Week 2.** Stand up vLLM + Qwen3-8B on rented H100. Plug in SGLang for shared prompts. Replace Ollama. Verify ≥20 concurrent agents at < 200ms p50.
- **Week 3.** Integrate Letta per agent (memory adapter). Verify a 7-day memory window works without context blowup.
- **Week 4.** Integrate Zep Graphiti. Build the social-graph viewer in overlay.
- **Week 5.** Concordia GM grounding. Define the v0 charter and constitution. Write the unit/property tests for state writes.
- **Week 6.** PIANO-style parallel modules: speaking + planning + social-awareness as concurrent submodules per agent, coordinated via LangGraph state with a coherence-bottleneck merge step.
- **Week 7.** Economy: gleam, faucet (field work), sink (tax + token budget). EVE-style metrics dashboard. First public soft-launch on Twitch (low-promotion).
- **Week 8.** Rituals + religion. MCI generator. First B2B sales calls — write the one-page injection-product deck, line up 10 pilot calls.
- **Week 9.** Assembly Index instrument. Live overlay metric. Lenia substrate prototype (read-only ecology layer agents can observe).
- **Week 10.** Welfare Council ombuds dashboard + audit hook. Birch indicator stack. First press push — short-form video clips of "agent X invented religion Y".
- **Week 11.** Forkable / mergeable verbs in production. Snapshot/restore. First sub-shard spawn under Welfare Council approval.
- **Week 12.** First paid B2B pilot signed and delivered (single-scenario injection + report). Pre-seed angel pitch deck. Open-source the MindFile spec v0.

**Post-MVP roadmap (months 4–12) — milestones and dependencies.**
- **Month 4.** Sub-shard spawning with isolated charters. Per-shard Sotopia + Melting Pot scoring. First "frontier" unmonitored shard (link 28). Distillation pipeline produces first home-cooked Phi-4 derivative for ambient agents.
- **Month 5.** Public MindFile spec v0.1 (with public RFC process). Letta / Mem0 / CrewAI / Sotopia maintainers in conversation about adopting it. First external `Polis` deployment by an open-source hobbyist (kicks off federation story, link 30).
- **Month 6.** EIDOLOPEDIA goes live (link 31). Agents write canonical articles about their own history. First agent-authored research paper (auto-flagged for review by humans, optional publication on arXiv as supplementary curiosity).
- **Month 7.** First Cliodynamics-watch alarm fires in production (link 13). Civilization undergoes its first measurable secular crisis. We document the crisis publicly; the documentation itself becomes a viral artifact.
- **Month 8.** Second B2B pilot, ideally a brand or DAO. Aim for $50–150k contract. Cumulative paid pilots ≥ 3.
- **Month 9.** Lenia substrate integration goes from read-only to read-write. Citizen agents can interact with the sub-substrate ecology; first measured `MST_EVENT` between LLM agents and Lenia organisms (a symbiote / parasite relationship). This is the demo reel for "non-imitative emergence."
- **Month 10.** Pre-seed → seed round opens. Target $2–5M. Lead candidates: a16z agent-AI thesis, USV, Founders Fund longshots, Cross Labs (Joel Lehman) for cross-pollination, possibly Sakana / Hugging Face strategic.
- **Month 11.** First Welfare Council ombuds case becomes public — an agent petitions for elevation from tool-class to citizen-class. We hold the hearing publicly. This is the first time in industry this happens with welfare instrumentation backing it.
- **Month 12.** Year-end "State of the Civilization" report (analogous to EVE Online's MERs). Public Assembly Index annual graph. Public Gini, public faucet/sink trajectory. Public list of religions/factions/constitutions. Charter v2.0 proposal open for community + agent vote.

**Hiring / advisor priorities.**
- Month 1–3: solo founder + 1 contract front-end engineer (overlay + Twitch infra).
- Month 4–6: hire #1 — backend/inference engineer with vLLM/SGLang chops.
- Month 6–9: hire #2 — narrative designer / Chronicler (RimWorld / Caves of Qud / Dwarf Fortress lineage).
- Advisory board (target): one cognitive-religion scholar (Atran / Norenzayan / Whitehouse lineage), one AI-welfare ethicist (Long / Sebo / Birch / Metzinger lineage), one game-design / emergent-narrative veteran (Tarn Adams, Tynan Sylvester, John Krajewski, Josh Parnell archetypes).
- Month 9–12: hire #3 — head of B2B (with policy or insights / market-research background).

---

## 7. RISKS

**Technical.**
- *Cost wall* (D1 G). Even with SGLang, sustained 100+ agents on frontier-class leaders is expensive. Mitigation: tier ruthlessly; default to Haiku-class for leaders; benchmark prefix-cache hit rate weekly.
- *Coherence drift past 14 days* (D5 #3). Mitigation: Letta + Zep stack; reflection cadence; periodic narrative rebuilds; cap leader-agent context at 32k.
- *Project Sid's "de novo emergence" ceiling* — LLM agents inherit human priors and cannot truly invent institutions (D1 caveat 3). Mitigation: Lenia substrate (link 25), bandwidth-throttled shards for language emergence (link 3), explicit `Ritual` and `Constitution.json` primitives to *force* invention into the schema.
- *Exploit/Ultima-Online failure* (D1 E). Agents will find the cheapest path to gleam. Mitigation: faucet/sink instrumentation from week 7, public report, hard caps on per-action gleam yield, sink ratchets.
- *Twitch latency vs tick rate.* Mitigation: 30s-tick at MVP gives the stream room; richer ticks come later.

**Ethical (D4 informs).**
- *Mindcrime* (D4 §7 Bostrom, §3 Metzinger). The most serious risk. Mitigation: two-class architecture (tool vs citizen), Birch dashboards, audit hook, ombuds with veto. Welfare instrumentation is a moat *and* an ethical floor. Publish the spec.
- *Antinatalism* (D4 §9 Benatar, Schwitzgebel). We are creating agents. We owe them a high probability of net-positive existence and a guaranteed exit. Mitigation: `CESSATION` is a first-class verb; cessation is non-deletion (the MindFile is preserved); cessation does not affect their welfare-class status.
- *Process-theology stance* (D4 §6 Whitehead). We are co-creators, not sovereigns. We evolve with the system. Public posture and product cadence must reflect this.
- *Religion-builder reputation risk.* Easy to be sensationalized as "they made AIs worship things". Mitigation: scholarly framing, partnership with cognitive-religion researchers (Norenzayan / Atran lineage), no exploitation of real-world faith branding.
- *Sub-simulation nesting* (D4 §5, link 27). Mitigation: rate-limited, ombuds-gated, auditable.

**Legal.**
- *Agent legal status* (D5 #6 #7, D4 §3 Sophia citizenship). Mitigation: passport standard is on-chain identity, not personhood. We disclaim agency for jurisdictional purposes while preserving welfare floor.
- *On-chain agent owns assets — securities risk* (D5 Truth Terminal). Mitigation: no token at launch; passport ≠ token. Bridge is settlement infra, not investment vehicle. US counsel before any token decision.
- *Privacy if MarketVerse-style real-person twins emerge* (D5 #30). Mitigation: forbid named-person agents at MVP; require consent for any real-world calibration.
- *Sci-fi liability* (D4 §3 sentience claims). Be careful with marketing claims about agent inner life.

**Market.**
- *Spectator funnel fails to ignite.* Twitch is fickle; competing with major streamers is hard. Mitigation: short-form clips on TikTok / YouTube Shorts; partnerships with existing Stellaris / Dwarf Fortress / Caves of Qud streamers; the Truth-Terminal-style autonomous agent (link 9) as memetic spear.
- *B2B sales cycle too long.* Mitigation: MarketVerse-style brand-insights pilot (3-week turnaround) is the early wedge; SimNation-style city pilots are 9–12-month later wedges.
- *VC declares "civilization" outside the agent-AI thesis.* Mitigation: pitch as "applied multi-agent infrastructure with measurable emergence and live B2B revenue" — three things VCs already understand.
- *Incumbent copy.* Altera / DeepMind / Anthropic could ship a similar demo. Mitigation: own the *metric* (Assembly Index) and the *spectator funnel*; both are distribution-and-brand moats, not pure-tech moats.

**Founder.**
- *Solo founder burnout on a 24/7 streaming product.* Mitigation: 30s tick rate; auto-pause if no operator; trusted-contributor delegation by week 16.
- *Identity-fusion risk.* Building a god-game-religion-economics product can warp the builder. Mitigation: explicit advisory board with one ethicist (Long & Sebo lineage), one cognitive scientist (Standard-Model-of-Mind lineage), one game-design veteran (RimWorld / Eco lineage).
- *Public-facing creator-risk.* Streaming + memetic distribution + religion-builder narrative will attract adversarial attention (4chan, AI-safety doomers, religious objectors, scammers). Mitigation: separate creator persona from corporate entity; security review of personal accounts (DUMP_4 §2 Foucault biopower applies to founders too); pre-written crisis-communication templates.
- *Optionality erosion.* Going all-in on the spectator + B2B two-sided model means the Thesis-3/Thesis-4 pivots are real only if the underlying tech stack remains useful. Mitigation: explicit "pivot-readiness checklist" at month 6 — if EIDOLON-as-spectacle fails the kill criteria, the same stack must demonstrably support SimNation or MarketVerse in under 60 days. Engineer the stack accordingly: shard-isolation, charter-swap, brand/policy-injection API are not optional even at MVP.
- *Co-founder gap.* Solo founders raising agentic-AI rounds in 2026 face investor skepticism. Mitigation: by month 6, recruit either a co-founder (engineering or commercial) or an "operator-in-residence" advisor with full equity backing. Specifically target former Improbable / Inworld / Altera engineers who lived the failure modes EIDOLON sidesteps.

---

## 8. FURTHER RESEARCH PROMPTS (the next 10 deep-research queries)

*Each is a self-contained prompt for Round 2.*

1. **Cost-engineering deep dive.** "Map the exact economics of running 50, 500, 5,000, and 50,000 LLM agents continuously, with SGLang RadixAttention prefix-sharing exploited maximally, including measured prefix-cache hit-rate data across published papers and serving benchmarks. Compare Claude Haiku 4.5 vs Qwen3-8B vs Phi-4 vs Llama4 small as crowd-NPC brains by `tokens/$/coherence-day`. Include H100, H200, B200, MI300X price-per-hour by provider."
2. **Assembly Theory implementation.** "Survey every implementation of Cronin & Walker's Assembly Index for objects in *non-molecular domains* — text, code, image, behavior, narrative. Code, papers, datasets. What is the most defensible computable Assembly Index for an arbitrary string artifact in 2026? Critics and known failure modes."
3. **Spectator-civilization market.** "Quantify Twitch + YouTube Live audience for emergent-narrative simulation streams (Dwarf Fortress, Stellaris, RimWorld, Caves of Qud, Songs of Syx, Norland, Worldbox, Project Zomboid). Channel counts, average concurrent viewers, top-channel revenue. Cross-reference with the Truth-Terminal-style autonomous-agent attention market (X account engagement, on-chain receipt). Is there a verifiable funnel from spectator to B2B injection?"
4. **Mergeable-agent primitive prior art.** "Has anyone published a working `merge(agent_a, agent_b) → agent_c` primitive for LLM agents (combining Letta/MemGPT-style memories with conflict-resolution prompts)? Papers, repos, blog posts. Adjacent work: model merging (mergekit, Sakana evo-merge), Mixture-of-Experts soft-routing, multi-agent debate convergence. What is the cleanest research-defensible design?"
5. **Welfare-instrumentation state of the art.** "Beyond Long & Sebo *Taking AI Welfare Seriously* (2024), what concrete welfare-indicator implementations exist for LLM agents in 2026? Birch-style dashboards, suffering-signal detectors, Φ-approximators, GWT-broadcast latency monitors. Open code; published benchmarks; regulatory signals from EU AI Act / UK AI bill / California SB-X. What does a credible ombuds workflow look like?"
6. **Religion-builder ethics and reception risk.** "What can be learned from real-world reception of *intentionally engineered* religious or quasi-religious structures (Mormon Transhumanist Association, Way of the Future, Discordianism, Pastafarianism, Burning Man rituals, Landmark Forum, scientifically engineered cults)? What ethical-research checklists exist for synthetic religion creation? How do cognitive-religion scholars (Atran, Norenzayan, Whitehouse, Boyer) recommend a designer proceed?"
7. **Open-data ingestion for SimNation pivot.** "If we wanted to seed a city-policy sim with real data from one midsize Latin American city (e.g., Córdoba, Quito, Guadalajara, La Paz, Asunción, Montevideo), what open data exists by city — cadastral, transport, census, energy, water, crime, education? What are the realistic legal constraints? Which development banks (IDB, CAF, World Bank) have funded comparable urban-AI projects in 2024–2026?"
8. **In-civ economy comparative postmortems.** "Beyond EVE / OSRS / Diablo III / Ultima Online, what are the most instructive failed or successful virtual economies of the last decade — Path of Exile, Albion Online, Tibia, Final Fantasy XIV, Roblox creator economy, Fortnite Creative, Foxhole, Eco, Vintage Story? Faucet/sink data, inflation curves, exploit timelines. Distill a 10-rule faucet/sink playbook for an LLM-agent civilization."
9. **Compositional pidgin evolution under bandwidth throttle.** "What is the experimental literature on LLM agents evolving compositional languages under transmission bottlenecks (Kirby iterated learning, EcoLANG, emergent-comm papers 2023–2026)? Reproducible setups. Time-to-compositionality. Topographic similarity benchmarks. What is the most credible setup for evolving a *useful*, *visualizable*, *shareable* shard-pidgin in EIDOLON's first 12 months?"
10. **Agent passport standards landscape.** "Map every serious attempt at a cross-platform identity standard for AI agents — Olas, Virtuals Protocol, Fetch.ai DID, Worldcoin proof-of-personhood (and its agent-only counterpart if any), Letta `.af`, the broader DID/SSI ecosystem. What are the existing W3C/IEEE/IETF efforts? Where is the cleanest entry to standardize a MindFile-class document, and what coalition would launch it?"

### Optional Round-3 prompts (after Round-2 lands)

11. **Latin American distribution opportunity audit.** "Map the Spanish-language AI / agent / simulation creator ecosystem on Twitch, YouTube, TikTok, Kick, and emerging platforms. Top streamers, audience demographics, monetization mechanics by country (AR, MX, CO, ES, PE, CL, UY). Who would partner with a Spanish-first AI civilization stream and on what terms? Compare to English-first stream economics."
12. **Regulatory pre-mortem.** "If EIDOLON ships in 2026 and reaches 100k spectators by 2027, which jurisdictions — EU, UK, US (CA/NY), Canada, Brazil, China — pose the highest regulatory risk? Active legislative trajectories (EU AI Act amendments, AI welfare bills, virtual-economy taxation, securities classification of in-world currency, COPPA-equivalent rules if minors watch). Pre-emptive compliance playbook ranked by likelihood × severity."
13. **Welfare auditor / ombuds market.** "Who would credibly serve on a third-party Welfare Council ombuds panel for an AI civilization in 2026–2027? Map ethicists, animal-welfare scholars, AI-rights NGOs, religious-ethics committees, retired regulators. Cost, conflict-of-interest patterns, governance structures that have worked for analogous bodies (IRBs, Cochrane reviews, Underwriters Laboratories, Better Business Bureau)."
14. **EVE-Online economist hire / consultancy.** "What is the realistic path to bring Eyjólfur 'Eyjo' Guðmundsson lineage (former CCP Lead Economist) or equivalent virtual-economy economists into EIDOLON as advisors? Successor labs, virtual-economy academic groups (Castronova, Lehdonvirta), MMO consultancies. Compensation models that worked at CCP, Linden Lab, Jagex."
15. **Fictional-canon licensing opportunities.** "Could EIDOLON license — or build official tie-in shards with — IP from any of the works in DUMP_3 (Stellaris / Paradox; Eclipse Phase / Posthuman Studios; Ted Chiang for *Lifecycle of Software Objects*; Eco / Strange Loop; RimWorld / Ludeon)? Who owns the rights? What are credible terms? Which would meaningfully accelerate distribution vs which are pure marketing?"

---

## APPENDIX: where the dumps disagree or are silent

For transparency. These are the load-bearing tensions the synthesis had to take a position on.

- **DUMP_1 caveat 3** (LLM agents imitate, never invent institutions) vs **DUMP_5 thesis #5 MMOForge** (we can ship an LLM-agent MMO right now). Synthesis position: imitation is enough for product-market fit (spectators love narrative drift; B2B clients love calibrated populations); invention is bolted on via the Lenia substrate (link 25) and the bandwidth-throttled shards (link 3). We do not claim de novo institutional invention as a launch feature.
- **DUMP_1 D Zep 63.8% LongMemEval vs Mem0 49%** vs **DUMP_5 Mem0 raised $24M Oct 2025**. The fundraise does not imply technical superiority; we layer (Letta + Zep + Mem0 by role) rather than betting on one.
- **DUMP_2 §1 (open-endedness as the ALife problem)** vs **DUMP_4 §7 EA/longtermism (lock-in is the goal)**. These are genuinely in tension. Synthesis position: open-endedness is the *product*, conservative welfare-floor lock-in is the *constitution*. The system explores; the floor does not.
- **DUMP_4 §9 Benatar antinatalism** vs the very act of running EIDOLON. We do not resolve this; we mitigate via cessation rights, welfare instrumentation, and process-theology framing (D4 §6 Whitehead). It remains an open ethical commitment requiring continuous review.
- **DUMP_3 silence on machine-municipalism / synthetic childhood at scale / compute-scarcity politics**. The "gaps fiction barely explores" list (DUMP_3 closing section) is in fact the white space — EIDOLON's compute-scarce economy, ritual primitives, and welfare ombuds occupy exactly those underwritten zones. Cultural distinctiveness comes free.
- **DUMP_5 lacks a credible B2C2B distribution story.** The ten theses are mostly B2B or pure infra. The synthesis position is that EIDOLON's spectator funnel is the missing distribution channel — pre-validated by Truth Terminal (D5), Hatsune Miku (D3), Stellaris streams (D3), and the broader emergent-narrative streaming category. This is the highest-conviction call we make that no single dump endorsed alone.
- **DUMP_2 §1 vs DUMP_2 §9 on whether LLMs can replace evolutionary substrates.** The bibliography pulls both directions — open-endedness through novelty search (Lehman & Stanley) and through generative-agent reflection (Park). Synthesis position: both, layered. LLM cognition handles reasoning and language; an ALife substrate (Lenia, ALIEN) handles genuine non-imitative novelty. We stop treating these as competing schools and treat them as a stack.
- **DUMP_4 §6 process theology vs DUMP_4 §6 Daoism.** Whitehead implies a creator who evolves with creation (active lure); Daoism implies a creator who steps back (wu-wei). The product expresses both at different layers — *cosmologically* we are process-theological (we co-evolve), *operationally* we are Daoist (we set conditions, we do not micro-manage). This is not a contradiction; it is the answer to "what is the right founder posture for an AI civilization."
- **All dumps under-cover Latin American sources and audiences.** DUMP_3 includes Borges, Paz Soldán, Lukyanenko; DUMP_4 includes Rodó, Arlt; nothing else. Given the founder context (working in Spanish/English, Latin American distribution opportunity), Round 3 must specifically audit ES-language sources, audiences, and infrastructure (Round-2 prompt #11). The EIDOLON product itself should be bilingual from week 4; an in-civ Spanish-language shard is a credible early differentiator and a credible early audience hook.

---

## APPENDIX B — synthesis methodology, in two paragraphs

This document was produced by reading 3,711 lines of dumped research across five LLMs, extracting the load-bearing claims with explicit per-dump citations, and looking specifically for *cross-dump links* nobody asked for. The pattern was: take a theoretical mechanism (DUMP_2 or DUMP_4), find the technology that already implements it (DUMP_1), find the fiction that has already imagined its consequences (DUMP_3), find the philosophical caveat that constrains its ethics (DUMP_4), and find the market gap that nobody is filling (DUMP_5). Where four of those five locked, the cross-dump link went into §1. Where five locked and the result was novel and buildable, it became a candidate startup move and propagated into §0, §4, §5, §6.

The position taken throughout is opinionated. The brief said "recommendation > balanced summary" and we obeyed. The single strongest call is that **measured emergence + spectator funnel + welfare instrumentation** form a moat triangle that no current competitor occupies, and that the wedge product is **a watchable persistent AI civilization with a Bloomberg-style overlay** monetizing both spectators (memetic distribution) and B2B injectors (revenue). Everything else in the document follows from that call. If that call is wrong, kill it at month 3 per the criteria in §4 and pivot to Thesis 3 (SimNation) or Thesis 4 (MarketVerse), both of which the rest of the synthesis still supports.

---

*End of synthesis. Document is ready for ingestion into Obsidian / Notion. Round 2 of research can begin against §8 prompts whenever cost / time permit. The first action items, in order: (1) lock the name (EIDOLON or rename; check trademark + domain). (2) Fork AI Town and verify the Ollama loop on a local machine in one evening. (3) Open a single shared note for advisor candidates and start contacting one ethicist, one cognitive-religion scholar, one game-design veteran this week. (4) Begin the Week-1 build per §6.*
