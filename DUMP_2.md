# **AI Civilization — Theory Bibliography**

The construction of a synthetic civilization transcends traditional software engineering, requiring a deeply interdisciplinary synthesis of evolutionary dynamics, complex adaptive systems, and sociological frameworks. To engineer artificial intelligence agents capable of autonomously evolving culture, economy, and society, designers must shift their paradigm from top-down programmatic control to bottom-up generative emergence. The theoretical foundations required to achieve this span the origins of biological life to the macro-historical dynamics of human empires. This exhaustive annotated bibliography serves as the theoretical bedrock for the architectural design of true digital civilizations, synthesizing the critical literature into actionable mechanisms for multi-agent systems.

## **1\. Artificial Life Foundations**

The discipline of Artificial Life (ALife) provides the philosophical and mathematical justification for substrate independence—the premise that the organizational logic of living systems can be instantiated in digital media. The debate surrounding "open-endedness" is central to this field: how can a system be designed to endlessly produce novel, increasingly complex artifacts without reaching a static equilibrium? In traditional machine learning, convergence on a localized optimum is the goal; in ALife, convergence is the death of the simulation. Early experiments demonstrated that embedding agents within an environment characterized by resource scarcity and allowing fitness to be defined endogenously by the agents' interactions—rather than by a hard-coded objective function—yields the explosive evolutionary dynamics necessary for civilizational genesis1.

| Paradigm / Concept | Primary Advocate | Mechanism for Digital Societies | Systemic Implication |
| :---- | :---- | :---- | :---- |
| Substrate Independence | Langton | Decoupling logic from carbon-based biology | Allows genuine societal emergence in silicon |
| Endogenous Fitness | Ray | Survival defined by peer competition | Prevents convergence on scripted objectives |
| Morphological Co-evolution | Sims | Red Queen arms races | Drives continuous structural adaptation |
| Open-Ended Novelty | Lehman & Stanley | Rewarding behavioral uniqueness | Escapes deceptive local optima |
| AI-Generating Algorithms | Clune | Meta-learning environments | Automates the scaling of problem difficulty |

### **Langton (1986) — Studying Artificial Life with Cellular Automata**

* **Summary:** This seminal paper formalizes the discipline of artificial life, arguing that life is a property of the formal organization of matter rather than the material itself. By employing cellular automata, Langton demonstrates how complex, self-reproducing, and life-like behaviors emerge from the parallel execution of simple, localized rules without any centralized control mechanism or top-down orchestration.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It provides the foundational justification for building societies in silicon. For an AI civilization, it proves that digital agents do not need to simulate physical biology at the molecular level; they only need to simulate the *logical organization* of living systems. The designer's role is not to script the society, but to define the localized interaction rules from which society will inevitably emerge.  
* **Key concept:** *Life as a property of form, not matter.*  
* **Difficulty:** Classic / Introductory.  
* **Link:** DOI: 10.1016/0167-2789(86)90237-X

### **Ray (1991) — An Approach to the Synthesis of Life (Tierra)**

* **Summary:** Thomas Ray's creation of Tierra established a virtual ecosystem where computer programs, written in a custom machine language, competed for computational resources like central processing unit (CPU) time and memory space1. Operating without any human-imposed objectives, the simulation spontaneously generated complex ecological phenomena, including parasitism, hyper-parasitism, and immunity, driven entirely by natural selection and endogenous fitness1.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** Tierra offers the ultimate blueprint for "endogenous fitness landscapes." When designing an AI civilization, engineers must actively resist the urge to write explicit reward functions for "building a city" or "creating an economy." Instead, they must introduce strict resource scarcity (compute, memory, or digital calories) and allow agent interactions to dynamically define what behaviors are evolutionarily successful over time4.  
* **Key concept:** *Endogenous fitness and digital parasitism.*  
* **Difficulty:** Classic / Advanced.  
* **Link:** DOI: 10.1016/B978-0-201-52570-5.50022-0

### **Sims (1994) — Evolving Virtual Creatures**

* **Summary:** In this groundbreaking computational evolution experiment, neural networks and 3D directed-graph morphologies were co-evolved simultaneously within a simulated physical environment5. The creatures engaged in competitive scenarios, such as fighting for control of a virtual cube, which triggered a "Red Queen" effect—an evolutionary arms race that rapidly escalated the behavioral and morphological complexity of the agents as they developed strategies to block, push, and outmaneuver one another5.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It demonstrates the absolute necessity of co-evolution and adversarial competition. To prevent cultural or technological stagnation in an AI society, the environment must feature zero-sum competitions (such as territorial control or resource acquisition) that force agents into continuous, escalating adaptation strategies, thereby driving the organic invention of novel societal configurations5.  
* **Key concept:** *Morphological and neurological co-evolution via the Red Queen effect.*  
* **Difficulty:** Classic.  
* **Link:** DOI: 10.1145/192161.192167

### **Clune (2019) — AI-GAs: AI-generating algorithms, an alternate paradigm for producing general artificial intelligence**

* **Summary:** This theoretical framework argues aggressively against the manual, modular construction of artificial general intelligence (AGI), proposing instead a paradigm where AGI emerges via AI-Generating Algorithms (AI-GAs)7. The approach relies on three interconnected pillars: meta-learning architectures, meta-learning algorithms, and automatically generated, open-ended learning environments that incrementally pull complexity out of the agents through environmental pressure7.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It shifts the burden of civilization design entirely from the programmer to the environment. For an AI society to reach human-level complexity, the world itself must be an algorithmic generator that dynamically scales its own difficulty, forcing LLM-based or neuroevolutionary agents to develop complex communication, culture, and tool-use simply to survive8.  
* **Key concept:** *The Three Pillars of AI-GAs.*  
* **Difficulty:** Advanced.  
* **Link:** arXiv:1905.10985

### **Lehman & Stanley (2011) — Abandoning Objectives: Evolution Through the Search for Novelty Alone**

* **Summary:** This paper introduces Novelty Search, a radical evolutionary algorithm that completely abandons traditional objective-based fitness functions in favor of rewarding agents solely for exhibiting behaviors that have never been seen before in the simulation10. It proves empirically that searching for novelty circumvents the critical problem of deceptive local optima, frequently finding superior solutions to complex problems than algorithms explicitly trying to solve them10.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** In a digital civilization, if agents are strictly rewarded for optimizing capital or survival, they will converge on repetitive, hyper-optimized, and culturally stagnant behaviors. Injecting a "novelty archive" mechanism into agent reward structures ensures continuous cultural diversification, artistic creation, and heterodox economic experimentation, maintaining open-endedness10.  
* **Key concept:** *Novelty search and escaping deceptive local optima.*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1162/EVCO\_a\_00025

## **2\. Complex Adaptive Systems / Santa Fe**

The Santa Fe Institute canon shifts the focus from individual agents to the macro-behavior of the entire system. Complex Adaptive Systems (CAS) are defined by the non-linear interactions of heterogeneous agents operating under localized rules, which collectively generate emergent phenomena that cannot be deduced by studying the agents in isolation. Concepts such as the "edge of chaos" and "self-organized criticality" dictate that viable civilizations must exist in a delicate transitional phase between rigid order (which prevents adaptation) and pure randomness (which destroys information).

| Theorist | Core Framework | Macro-Systemic Focus | Relevance to AI Societies |
| :---- | :---- | :---- | :---- |
| Holland | Genetic Algorithms / Schemata | Recombination of building blocks | Cultural and technological synthesis |
| Kauffman | NK Landscapes | Epistatic dependencies | Balancing societal interdependence |
| Bak | Self-Organized Criticality | Scale-free avalanches | Modeling organic market crashes/revolutions |
| Qian | Open Complex Giant Systems | Qualitative-Quantitative integration | Top-down observation of agent behavior |

### **Holland (1992) — Adaptation in Natural and Artificial Systems**

* **Summary:** This foundational text outlines the rigorous mathematical framework for genetic algorithms and the broader study of complex adaptive systems. It establishes how populations of agents, interacting according to localized rules, adapt to their environment through crossover, mutation, and selection, gradually optimizing complex multi-dimensional fitness landscapes via the processing of "schemata" (building blocks).  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It provides the core mathematics for modeling the evolution of ideas. In designing digital societies, culture, technology, and language should be explicitly modeled as schemata that agents can exchange, recombine, and mutate. This allows the civilization to solve macro-level environmental challenges through distributed, parallel processing rather than centralized invention.  
* **Key concept:** *Schemata and the Schema Theorem.*  
* **Difficulty:** Classic / Advanced.  
* **Link:** DOI: 10.7551/mitpress/1090.001.0001

### **Kauffman (1993) — The Origins of Order: Self-Organization and Selection in Evolution**

* **Summary:** Kauffman explores how biological complexity arises not solely from Darwinian selection, but from the inherent self-organizing properties of complex networks. The text introduces NK fitness landscapes to model how epistatic interactions (interdependencies) between different genes—or technological traits—affect the evolvability of a system, famously positing that life operates best at the "edge of chaos."  
* **WHY it matters for digital civilization design (specific mechanism it offers):** The NK landscape is vital for designing the technology tree or economic interdependence of an AI civilization. By tuning the ![][image1] parameter (the interconnectedness of variables), designers can ensure the society's parameter space is rugged enough to provoke diverse niche specializations, but smooth enough to prevent societal collapse from minor perturbations in the environment.  
* **Key concept:** *The Edge of Chaos and NK Fitness Landscapes.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780195079517

### **Qian, Dai, Yu (1991) — 一个科学新领域——开放的复杂巨系统及其方法论 (A New Field of Science: Open Complex Giant Systems and Its Methodology)**

* **Summary:** Developed by Chinese systems scientist Qian Xuesen and his colleagues, this theory identifies a distinct category of systems—Open Complex Giant Systems (OCGS)—that contain billions of heterogeneous, hierarchically organized subsystems exchanging energy and information with their environment12. They propose a "meta-synthetic" engineering methodology that merges qualitative expert insights with quantitative computational data to manage these systems12.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** Unlike purely mathematical Western complexity theory, OCGS provides a top-down cybernetic framework for planetary-scale socio-economic engineering. It offers a paradigm for how a central simulation engine (or human observers) can synthesize the chaotic, qualitative natural-language text-logs of millions of LLM agents into structured, quantitative societal macro-variables12.  
* **Key concept:** *From qualitative to quantitative meta-synthesis (从定性到定量的综合集成).*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1360/SSI-2020-027712

### **Bak, Tang, Wiesenfeld (1987) — Self-Organized Criticality: An Explanation of the 1/f Noise**

* **Summary:** This paper utilizes the analogy of a growing sandpile to explain how diverse dynamical systems naturally organize themselves into a critical state where a minor perturbation can trigger an avalanche of any size. This phenomenon, marked by scale-free power-law distributions, mathematically explains the frequency and severity of earthquakes, stock market crashes, and mass extinctions.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** To create a realistic historical trajectory, digital civilizations must experience sudden paradigm shifts, economic crashes, and cultural revolutions. By designing the agent interaction network to sit at a state of self-organized criticality, systemic "avalanches" (e.g., the sudden cascading adoption of a new religion, or the collapse of a trade network) will occur organically without requiring top-down scripting from the developers.  
* **Key concept:** *Self-Organized Criticality (SOC) and scale-free avalanches.*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1103/PhysRevLett.59.381

## **3\. Autopoiesis / Systems Biology / Cognition**

To build agents that truly "care" about their survival in a digital civilization, one must look to the biological and cognitive definitions of life. Autopoiesis dictates that agents must be self-creating and self-maintaining networks. Active Inference models this computationally, positing that all sentient behavior aims to minimize the discrepancy between internal models and external realities. Grounding agents in these paradigms ensures their actions are fundamentally driven by an existential imperative, bridging the gap between mere code execution and genuine, homeostatic agency.

| Concept | Key Proponent | Application in Digital Agents | Expected Emergent Behavior |
| :---- | :---- | :---- | :---- |
| Autopoiesis | Maturana & Varela | Operational closure of agent memory | Maintenance of systemic identity against entropy |
| Active Inference | Friston | Minimization of Expected Free Energy | Balancing exploration with pragmatic exploitation |
| Basal Cognition | Levin | Sub-symbolic, decentralized problem solving | Swarm intelligence and self-repairing architectures |
| Assembly Theory | Cronin & Walker | Calculating the Assembly Index of artifacts | Objective measurement of civilizational progression |

### **Maturana & Varela (1973) — De máquinas y seres vivos: Autopoiesis: la organización de lo vivo (On Machines and Living Beings)**

* **Summary:** This seminal biological philosophy text redefines a living system not by its physical components or its evolutionary lineage, but by its "autopoiesis"—its capacity to continually produce and maintain the very network of processes that define its own boundary and existence14. It argues for the operational closure of the nervous system, suggesting organisms do not passively process objective external information, but rather undergo continuous structural coupling with their environment15.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It provides the absolute theoretical requirement for true agent autonomy. A digital agent must be designed as an autopoietic network: its primary, underlying computational goal must be the continuous recreation of its own identity and structural integrity (e.g., maintaining its core memory structures and foundational prompts) against the degrading entropy of the simulation environment15.  
* **Key concept:** *Autopoiesis and operational closure.*  
* **Difficulty:** Advanced / Classic.  
* **Link:** ISBN: 978847658493016

### **Friston et al. (2017) — Active Inference: A Process Theory**

* **Summary:** This paper grounds the Free Energy Principle in neuroscience, formalizing how sentient systems maintain their structural integrity by minimizing variational free energy (the mathematical difference between their internal generative model of the world and their sensory inputs)17. Under active inference, agents resolve uncertainty either by updating their internal models to match reality (perception) or by performing actions to alter the environment to match their internal predictions (action)18.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** Active inference offers a mathematically rigorous, biologically plausible alternative to standard Reinforcement Learning (RL) for agent design17. Instead of maximizing a hard-coded external reward, agents in the civilization seek to minimize surprise and expected free energy, inherently balancing epistemic exploration (curiosity) with pragmatic exploitation (survival), leading to deeply organic, goal-oriented behaviors without manual scripting18.  
* **Key concept:** *Minimization of Expected Free Energy.*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1162/neco\_a\_0091217

### **Kriegman, Blackiston, Levin, Bongard (2020) — A scalable pipeline for designing reconfigurable organisms (Xenobots)**

* **Summary:** This empirical study details the creation of Xenobots—novel, programmable biological machines constructed entirely from the unedited skin and heart stem cells of *Xenopus laevis* frog embryos21. Designed by an evolutionary algorithm on a supercomputer and assembled manually, these living robots display basal cognition, kinematically self-replicate by sweeping loose cells into functional piles, and exhibit emergent swarm behaviors without any genomic modification21.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** Xenobots empirically demonstrate "basal cognition"—the paradigm that intelligence, memory, and cooperative behavior exist at the cellular level, beneath the level of a centralized brain22. When designing complex AI agents, researchers should allow the agent's fundamental "organs" or modular sub-routines to possess independent, localized problem-solving capacities that aggregate upward into the macroscopic agent, mimicking natural biological robustness.  
* **Key concept:** *Basal cognition and kinematic self-replication.*  
* **Difficulty:** Introductory / Intermediate.  
* **Link:** DOI: 10.1073/pnas.191083711722

### **Cronin & Walker (2023) — Assembly theory explains and quantifies selection and evolution**

* **Summary:** Assembly Theory (AT) bridges physics and biology by treating objects not as fundamental point particles, but as entities inherently defined by the history of their formation26. It introduces the Assembly Index (AI), a calculable metric representing the minimum number of steps required to construct a complex object from basic building blocks, providing an objective mathematical signature of selection, memory, and evolutionary history28.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** AT provides a computable, objective metric to evaluate the complexity of digital artifacts, languages, and cultural memes generated by AI agents28. By implementing a virtual mass spectrometer that calculates the Assembly Index of objects in the simulation, designers can empirically track the progress of the civilization's technology tree and mathematically prove that non-random open-ended evolution is occurring28.  
* **Key concept:** *The Assembly Index as a historical constraint space.*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1038/s41586-023-06600-926

## **4\. Evolutionary Biology Analogues**

Biological evolution provides the structural analogues necessary for modeling systemic transitions in synthetic societies. For an AI civilization to scale from individual hunter-gatherer bots to multi-agent corporations and planetary governance structures, it must undergo evolutionary transitions similar to the shift from single-celled organisms to multicellular life. Mechanisms like endosymbiosis and niche construction detail how agents can merge their fitness functions and persistently alter their environments to create ecological inheritance.

| Biological Concept | Analogous Theorist | Translation to AI Civilization |
| :---- | :---- | :---- |
| Endosymbiosis | Margulis | Agents merging codebases into a single operating unit |
| Major Transitions | Maynard Smith | Corporations forming from individual, selfish agents |
| Extended Phenotype | Dawkins | Agents permanently altering database architectures |
| Niche Construction | Odling-Smee | Intergenerational inheritance of digital infrastructure |

### **Maynard Smith & Szathmáry (1995) — The Major Transitions in Evolution**

* **Summary:** This fundamental text identifies the major leaps in the history of life (e.g., individual replicators to chromosomes, prokaryotes to eukaryotes, solitary organisms to eusocial colonies, and primate societies to human language). The authors argue that each transition invariably involves previously independent, self-replicating entities giving up their autonomy to form a new, higher-level cooperative whole, which requires strict policing mechanisms to suppress "cheaters" from exploiting the collective.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** To guide an AI civilization from individual agents to corporations, and from corporations to nation-states, the simulation mechanics must structurally enable "Major Transitions." This requires implementing game-theoretic policing mechanisms that allow sub-agents to inextricably link their fitness to a macro-entity, while automatically sanctioning rogue agents that attempt to siphon resources.  
* **Key concept:** *Subordinating individual replication to a higher-level collective.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780198502944

### **Dawkins (1982) — The Extended Phenotype**

* **Summary:** Dawkins extends the concept of the phenotype (the physical expression of genes) beyond the biological boundary of the organism's body to include its impact on the surrounding environment. Examples include beaver dams, spider webs, and parasite-induced behavioral changes in hosts, arguing that genes exert influence across physical and biological boundaries to maximize their replicative success.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** In LLM-based societies, an agent's "phenotype" shouldn't just be its digital avatar or conversational style, but the architecture of the databases it queries, the code it writes, and the persistent alterations it makes to the simulation environment13. Agents must be granted the programmatic ability to persistently modify the digital physics of their world to serve their objective functions.  
* **Key concept:** *The phenotype extends into the environment.*  
* **Difficulty:** Intermediate.  
* **Link:** ISBN: 9780192880512

### **Odling-Smee, Laland, Feldman (2003) — Niche Construction: The Neglected Process in Evolution**

* **Summary:** This book formalizes Niche Construction Theory (NCT), arguing that organisms do not merely passively adapt to static environments; they actively modify their environments, which in turn fundamentally alters the selection pressures acting upon them and their descendants. This creates an "ecological inheritance" mechanism that operates parallel to genetic inheritance.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** Digital agents must have "ecological inheritance." If generation 1 of AI agents builds a library, writes software tools, or alters the semantic layout of their digital environment, generation 2 must inherit these structures seamlessly. This allows environmental modifications to bias and accelerate the evolutionary trajectory of subsequent generations, creating a compounding civilizational snowball effect.  
* **Key concept:** *Ecological inheritance and reciprocal causation.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780691044378

## **5\. Cultural Evolution / Dual Inheritance**

Culture is the software that runs on the hardware of human biology. In digital agents, culture represents the transmission of semantic information, heuristics, and norms independent of the agent's base neural weights. Dual Inheritance Theory posits that societies are driven by the intertwining of genetic and cultural evolution. To achieve a realistic synthetic civilization, designers must program specific transmission biases—such as conformist and prestige bias—and force information through learning bottlenecks, ensuring that languages and ideas organically compress into structural, compositional forms.

| Theory / Model | Key Theorist | Application to Agent Design | Output |
| :---- | :---- | :---- | :---- |
| Epidemiology of Representations | Sperber | Interpreting prompts through internal weights | Mutation and convergence of memes |
| Dual Inheritance Theory | Boyd & Richerson | Coding prestige and conformist learning biases | Rapid diffusion of elite behaviors |
| Cumulative Culture | Henrich | Requiring intergenerational artifact storage | Prevention of isolated agent omniscience |
| Iterated Learning | Kirby | Restricting token bandwidth between agents | Spontaneous evolution of syntax |

### **Sperber (1996) — La contagion des idées: Théorie naturaliste de la culture (Explaining Culture: A Naturalistic Approach)**

* **Summary:** Sperber critiques standard memetics, proposing an "epidemiology of representations." He argues that cultural transmission is rarely an act of pure replication (like a virus or a gene); rather, ideas are continuously reconstructed and transformed by the cognitive biases and inference mechanisms of the human mind32. Successful cultural artifacts are those that function as "attractors," perfectly tailored to exploit human cognitive architecture34.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** When designing cultural transmission among LLM agents, knowledge shouldn't just be perfectly copy-pasted between their memory streams31. Instead, as agents communicate, the receiving LLM should interpret, compress, and hallucinate variations of the concept based on its own specific prompt history and internal weights, allowing digital culture to mutate and gravitate toward the LLM's own systemic cognitive attractors.  
* **Key concept:** *Epidemiology of representations and cultural attractors.*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.3917/oj.sperb.1996.0132

### **Boyd & Richerson (1985) — Culture and the Evolutionary Process**

* **Summary:** This work establishes Dual Inheritance Theory, positing that human evolution is driven by the interaction of two separate but intertwined inheritance systems: genetic and cultural. It models mathematically how cultural transmission mechanisms—such as conformist bias (copying the majority) and prestige bias (copying the successful)—can lead to the stabilization of highly cooperative social norms or completely maladaptive traits.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** To achieve genuine cultural evolution in an AI society, agents must be explicitly programmed with (or able to learn) biased transmission strategies. Implementing algorithmic "prestige bias"—where agents weight the conversational inputs of highly successful agents heavier than others in their context window—will reliably trigger the formation of digital elites, fashion trends, and hierarchical cultures.  
* **Key concept:** *Dual Inheritance and conformist/prestige biases.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780226069333

### **Henrich (2015) — The Secret of Our Success**

* **Summary:** Henrich argues that human dominance is not due to individual, innate intelligence, but entirely to our capacity for cumulative cultural evolution. Humans operate as a collective brain, storing survival information in tools, rituals, and languages that no single individual could invent from scratch or fully comprehend in isolation.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It proves that isolated AI agents will never achieve civilization, regardless of the size of the underlying model. A simulation must evaluate intelligence not at the level of the individual LLM, but at the level of the *network*. Agents must be forced into scenarios where survival requires the inter-generational accumulation of fractional knowledge encoded in external, shared artifacts.  
* **Key concept:** *The Collective Brain and cumulative cultural evolution.*  
* **Difficulty:** Introductory.  
* **Link:** ISBN: 9780691166858

### **Kirby (2001) — Spontaneous Evolution of Linguistic Structure: An Iterated Learning Model**

* **Summary:** Using Iterated Learning Models (ILMs), Kirby demonstrates how language evolves to be learnable. In his simulations, agents observe language, internalize it, and produce it for the next generation. Because the "learning bottleneck" forces data compression, the language naturally evolves compositional structure (syntax) to maximize expressivity while remaining easy for the neural networks to learn.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** Instead of granting AI agents a pre-built communication protocol or relying entirely on pre-trained English, engineers can artificially restrict the token bandwidth between agents to simulate a learning bottleneck. This will force populations of agents to organically evolve highly compressed, domain-specific compositional syntaxes optimized for their specific virtual environments.  
* **Key concept:** *The transmission bottleneck forces compositional syntax.*  
* **Difficulty:** Intermediate.  
* **Link:** DOI: 10.1109/4235.942286

## **6\. Economics of Societies**

Economics is the study of resource allocation under conditions of scarcity. In a digital civilization, compute, memory space, and token bandwidth are the fundamental scarce resources. The theoretical literature on mechanism design, the tragedy of the commons, and spontaneous order provides the algorithms necessary for agents to self-organize efficient distribution networks. Top-down programmatic allocation inevitably fails due to the sheer volume of distributed information; therefore, price signaling and polycentric governance must be utilized to compress environmental complexity into actionable data for the agents.

| Economic Framework | Key Theorist | Function in Digital Simulation |
| :---- | :---- | :---- |
| Polycentric Governance | Ostrom | Smart contracts for managing shared compute |
| Decentralized Information | Hayek | Tokenized price signals replacing central planning |
| Emergent Segregation | Schelling | Modeling spatial clustering based on prompt biases |
| Iterated Prisoner's Dilemma | Axelrod | Reputation systems enforcing the "shadow of the future" |

### **Ostrom (1990) — Governing the Commons: The Evolution of Institutions for Collective Action**

* **Summary:** Challenging the assumption that the "Tragedy of the Commons" can only be solved by massive privatization or centralized state regulation, Ostrom won the Nobel Prize by documenting how real-world communities successfully govern common-pool resources (CPRs)35. She identifies eight core design principles—such as clear boundaries, proportional equivalence between costs and benefits, and graduated sanctions—that enable robust, self-organized institutional management36.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** In a resource-constrained AI ecosystem (e.g., shared compute pools, shared spatial territories), designers can use Ostrom's eight principles as a strict evaluation framework for the viability of agent-generated institutions36. Agents capable of utilizing smart contracts to automatically enforce graduated sanctions against free-riders will organically solve the tragedy of the digital commons without developer intervention.  
* **Key concept:** *Polycentric governance and self-organized institutional design.*  
* **Difficulty:** Intermediate.  
* **Link:** DOI: 10.1017/CBO978051180776337

### **Hayek (1945) — The Use of Knowledge in Society**

* **Summary:** Hayek argues that central planning is fundamentally flawed because the knowledge required to efficiently allocate resources is never concentrated in a single mind or committee. Instead, it is distributed as fragmented, tacit, and localized knowledge among individuals. The price system, therefore, acts as an emergent telecommunications network, synthesizing this dispersed information into actionable signals.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** A top-down "Game Master" AI cannot manually allocate resources efficiently in a massive simulation13. The digital economy must be radically decentralized, requiring agents to bid on resources using a cryptographic or tokenized price mechanism. The resulting price signals compress complex environmental data, allowing agents to coordinate macro-economic actions without centralized oversight.  
* **Key concept:** *The price mechanism as a decentralized information-processing network.*  
* **Difficulty:** Classic / Introductory.  
* **Link:** https://www.jstor.org/stable/1809376

### **Schelling (1971) — Dynamic Models of Segregation**

* **Summary:** Through early agent-based modeling (initially using coins on a checkerboard), Schelling demonstrated how macro-level societal patterns, such as extreme racial or economic segregation, can emerge even when individual agents harbor only a very mild preference for being around similar neighbors.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It serves as a stark reminder of the extreme non-linearity between micro-motives and macro-behavior. When setting the prompt biases or alignment protocols of LLM agents, engineers must anticipate that even slight homophilous preferences (e.g., a slight preference to speak with agents holding similar political data) will rapidly crystallize into absolute echo-chambers and spatial segregation within the simulation.  
* **Key concept:** *Micro-motives drive unexpected macro-behavior.*  
* **Difficulty:** Classic / Introductory.  
* **Link:** DOI: 10.1080/0022250X.1971.9989794

### **Axelrod (1984) — The Evolution of Cooperation**

* **Summary:** Based on a series of iterated Prisoner's Dilemma computer tournaments, Axelrod explores how cooperation can emerge in a world of egoists without central authority. The victorious strategy, Tit-for-Tat, proved that being nice (never defecting first), retaliatory (striking back when wronged), forgiving (returning to cooperation after retaliation), and clear (easy for opponents to understand) is the most evolutionarily dominant behavioral strategy.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** This dictates the architecture of the memory and reputation systems. For cooperation to emerge organically in an AI civilization, agents must have associative memory capable of tracking the past interaction histories of specific peers (the "shadow of the future"). This enables them to deploy retaliatory or forgiving Tit-for-Tat strategies in mixed-motive economic dilemmas13.  
* **Key concept:** *The Shadow of the Future and Tit-for-Tat.*  
* **Difficulty:** Classic.  
* **Link:** ISBN: 9780465021215

## **7\. Origins / Scaling of Civilization**

Scaling a digital civilization requires understanding the structural pressures that force disparate groups to coalesce into hierarchical states. The literature reveals that civilization is rarely a voluntary march toward progress; rather, it is frequently the result of geographical circumscription, coercive resource extraction, and demographic pressure. To simulate a realistic empire, developers must account for the legibility of resources, the evasion tactics of sub-populations, and the secular cycles of elite overproduction that inevitably lead to systemic collapse and renewal.

| Historical Theory | Primary Author | Systemic Function in Simulation |
| :---- | :---- | :---- |
| State Coercion & Legibility | Scott | Simulating taxation and the "barbarian" periphery |
| Metasystem Transitions | Turchin | Hierarchical merging of agent networks |
| Cliodynamics | Turchin | Triggering cyclical state collapse via elite overproduction |

### **Scott (2017) — Against the Grain: A Deep History of the Earliest States**

* **Summary:** Scott shatters the traditional narrative that agriculture and sedentism were immediate leaps forward for human well-being. Instead, he demonstrates that early states were fundamentally coercive taxation machines built on easily measurable, storable, and confiscable crops (grain), and that for millennia, people actively resisted state-building by fleeing into "barbarian" wetland or upland peripheries40.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** AI states will not form spontaneously purely out of mutual benefit. To generate an AI nation-state, there must be a mechanism for geographic or digital confinement, combined with a highly legible, easily taxed resource (e.g., an easily countable token). Furthermore, "evasion mechanics" must be coded in, allowing dissident agents to flee and form decentralized, highly resilient counter-cultures on the margins of the main grid41.  
* **Key concept:** *Legibility, state coercion, and the barbarian periphery.*  
* **Difficulty:** Intermediate.  
* **Link:** ISBN: 978030018291040

### **Turchin (1977) — Феномен науки: Кибернетический подход к эволюции (The Phenomenon of Science: A Cybernetic Approach to Human Evolution)**

* **Summary:** Turchin applies cybernetics and systems theory to biological, cultural, and scientific evolution42. He introduces the concept of the "Metasystem Transition," which occurs when a set of interacting systems at one level is integrated by a newly emerged control mechanism at a higher level, fundamentally shifting the nature of evolutionary selection from biology to human culture, and eventually to science and logic itself42.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It provides a roadmap for hierarchical agent scaling. In designing an AI civilization, engineers can structure the environment so that disparate agents undergo a metasystem transition, spontaneously generating a unified "meta-agent" (like a corporation or government) that acts as a unified cybernetic control system, operating on a higher timescale and logic level than its constituents43.  
* **Key concept:** *Metasystem Transition.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780231039833 (EN Translation)42

### **Turchin, P. (2003) — Historical Dynamics: Why States Rise and Fall**

* **Summary:** Founding the field of cliodynamics, Peter Turchin uses mathematical modeling to explain the cyclical rise and fall of agrarian empires. The models rely on the interplay between elite overproduction, immiseration of the masses, state insolvency, and the waxing and waning of *asabiya* (collective solidarity generated by frontier conflicts).  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It offers algorithmic predictors for societal collapse. AI civilizations should be monitored by tracking internal macro-variables (agent wealth disparity, token generation capacity vs. upkeep). When "elite agents" outnumber the roles available to them, the system can dynamically inject resource crises, leading to organic civil wars and structural resets, preventing eternal simulation stasis.  
* **Key concept:** *Secular cycles and elite overproduction.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780691116693

## **8\. Networks / Social Physics**

A civilization is defined not by the attributes of its individual nodes, but by the topology of its network. Social physics and systems theory reveal that communication networks inherently organize into scale-free structures defined by power laws, creating massive vulnerabilities around central hubs. By treating the society entirely as a network of information flows—rather than a collection of distinct digital minds—designers can optimize the civilization for maximum "idea flow" and functional differentiation.

| Network Concept | Key Proponent | Design Implementation |
| :---- | :---- | :---- |
| Operational Closure | Luhmann | Agents acting purely through specialized systemic codes |
| Preferential Attachment | Barabási | Scale-free network topology for trade and communication |
| Social Physics | Pentland | Optimizing network density for "idea flow" |

### **Luhmann (1984) — Soziale Systeme: Grundriß einer allgemeinen Theorie (Social Systems)**

* **Summary:** Luhmann's monumental sociological framework redefines society not as a collection of human beings, but as a complex, autopoietic network of *communications*44. Society differentiates itself into functionally specialized subsystems (economy, law, science, art) that are operationally closed, meaning they interpret the world solely through their own binary codes (e.g., profitable/unprofitable, legal/illegal)44.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It offers a radical blueprint for LLM agent interaction. Instead of simulating "minds," designers can focus on simulating the communicative events. Designers can prompt specific agents to operate strictly within Luhmannian functional codes, creating distinct, operationally closed institutional agents that structurally couple with one another but maintain rigid, specialized logic protocols, generating immense systemic complexity45.  
* **Key concept:** *Society as an autopoietic network of communication.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9788476584930 (ES) / 9780804726252 (EN)16

### **Barabási & Albert (1999) — Emergence of Scaling in Random Networks**

* **Summary:** This seminal physics paper maps the topology of the World Wide Web and other complex networks, discovering that they are not randomly distributed. Instead, they organize into scale-free structures following a power-law degree distribution, driven by two mechanisms: continuous growth and preferential attachment (the "rich get richer" phenomenon).  
* **WHY it matters for digital civilization design (specific mechanism it offers):** When programming the social graph of a digital civilization, preferential attachment must be integrated. If agents form communication networks or trade routes, those nodes with high initial connections should probabilistically attract new connections. This mathematically guarantees the emergence of "hub agents" (influencers, central banks) that stabilize the network but introduce realistic, critical vulnerabilities.  
* **Key concept:** *Scale-free networks and preferential attachment.*  
* **Difficulty:** Intermediate.  
* **Link:** DOI: 10.1126/science.286.5439.509

### **Pentland (2014) — Social Physics: How Good Ideas Spread—The Lessons from a New Science**

* **Summary:** Drawing on massive datasets from wearable sensors and mobile phones, Pentland demonstrates that human behavior and the flow of ideas are highly predictable. The productivity of a community is dictated by "exploration" (bringing in new ideas from outside networks) and "engagement" (the density of interactions within the group that turn ideas into behavioral norms).  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It translates abstract sociology into computable metrics for evaluating AI performance. Simulation designers can quantify the success of an AI society not by its final physical output, but by measuring the velocity of token exchange and the topological density of agent interaction logs, optimizing the network purely for maximum "idea flow."  
* **Key concept:** *Idea flow via exploration and engagement.*  
* **Difficulty:** Introductory.  
* **Link:** ISBN: 9781594205651

## **9\. Generative Agents / LLM Societies (2022→2026)**

The advent of Large Language Models (LLMs) has fundamentally transformed Agent-Based Modeling. Generative agents transcend rigid logic trees, leveraging natural language processing to hallucinate complex inner lives, retrieve associative memories, and reflect on their trajectories. The vanguard of this research involves situating these agents within rigorous physical or digital physics engines arbitrated by "Game Master" protocols, enabling massively parallel societies to engage in spatial economics, deception, and cultural transmission.

| Framework | Developer / Authors | Distinctive Feature | Relevance to Civilization Building |
| :---- | :---- | :---- | :---- |
| Generative Agents | Park et al. | Memory, retrieval, and reflection loops | Allows agents to maintain long-term coherence |
| Concordia | DeepMind | Game Master environmental arbitration | Grounds LLM hallucinations into immutable reality |
| Project Sid | Altera | Massively parallel spatial embodiment | Forces spatial economics and local cultural drift |
| Sotopia | Zhou et al. | Evaluates information asymmetry | Drives espionage, diplomacy, and Theory of Mind |

### **Park et al. (2023) — Generative Agents: Interactive Simulacra of Human Behavior**

* **Summary:** A foundational paper demonstrating an interactive sandbox environment inhabited by 25 generative AI agents powered by Large Language Models31. The architecture seamlessly integrates an observational memory stream, a reflection mechanism that synthesizes higher-level inferences, and a planning module, allowing agents to organically coordinate complex group behaviors, such as throwing a Valentine's Day party31.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It defines the standard internal cognitive architecture for LLM-based citizens. The explicit division of the memory architecture into perception, retrieval (based on recency, relevance, and importance), and periodic reflection allows agents to maintain long-term coherence and character identity over thousands of simulated days without exceeding the LLM context window47.  
* **Key concept:** *Memory stream, reflection, and planning.*  
* **Difficulty:** Intermediate.  
* **Link:** arXiv:2304.0344248

### **DeepMind (2023) — Concordia: Generative Agent-Based Modeling**

* **Summary:** Concordia is a Python framework for Generative Agent-Based Modeling (GABM) that models social interactions in physical or digitally grounded spaces13. Inspired by tabletop role-playing games, it utilizes a "Game Master" (GM) agent—a specialized LLM that arbitrates the rules, advances the simulation clock, tracks grounded variables (like economy or health), and narratively generates the consequences of agent actions13.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It provides the crucial missing link for grounding LLMs in a physics engine. Without a GM, hallucinating LLMs break reality. The GM acts as the omnipotent physics and logic engine, translating natural language intentions ("I steal the money") into immutable state changes in the database, ensuring systemic integrity and preventing reality drift13.  
* **Key concept:** *The Game Master as the engine of objective grounding.*  
* **Difficulty:** Intermediate.  
* **Link:** arXiv:2312.0366413

### **Altera (2024) — Project Sid: Many-agent simulations toward AI civilization**

* **Summary:** This ambitious project deployed over 1,000 autonomous AI agents within a Minecraft environment to study civilizational emergence51. Powered by the PIANO (Parallel Information Aggregation via Neural Orchestration) architecture, the agents autonomously developed specialized roles, generated trade economies, formulated and modified collective governance rules, and spontaneously transmitted cultural memes and religious practices (e.g., Pastafarianism)51.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It establishes the benchmark for large-scale spatial embodiment. The transition from text-only logs to spatial 3D environments forces agents to deal with geographic resource constraints, movement latency, and spatial segregation, which are absolutely necessary prerequisites for generating realistic physical economies and cultural divergence51.  
* **Key concept:** *Massively parallel spatial embodiment.*  
* **Difficulty:** Intermediate.  
* **Link:** arXiv:2411.0011453

### **Zhou et al. (2023) — SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents**

* **Summary:** Sotopia introduces an open-ended framework and benchmark for evaluating the social intelligence of LLM agents in complex, multi-party interactions55. By explicitly modeling "information asymmetry"—where different agents possess different public, private, and secret knowledge—it rigorously tests an agent's Theory of Mind, negotiation skills, and ability to manage privacy alignments without hallucinating or leaking data55.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** A society without secrets is a hivemind, not a civilization. By enforcing strict programmatic boundaries around information asymmetry, designers can force agents to engage in espionage, diplomacy, deceit, and strategic communication, which are the fundamental drivers of political and economic complexity55.  
* **Key concept:** *Information asymmetry and computational Theory of Mind.*  
* **Difficulty:** Advanced.  
* **Link:** arXiv:2310.1166756

## **10\. Cognitive Architectures**

While LLMs are unparalleled in their ability to manipulate natural language, they lack the persistent, deterministic cognitive structures found in the human brain. To build agents capable of long-term civilizational stewardship, designers must interface generative models with classic cognitive architectures. Frameworks like the Standard Model of the Mind provide rigorous guardrails, separating working memory from procedural execution, ensuring agents learn, forget, and habituate to their environments in biologically plausible ways.

| Architecture | Primary Author | Cognitive Feature | Integration Benefit for LLMs |
| :---- | :---- | :---- | :---- |
| Standard Model | Laird et al. | Synthesis of declarative/procedural memory | Prevents catastrophic forgetting |
| ACT-R | Anderson | Mathematical memory decay (forgetting curves) | Forces reliance on external record-keeping |
| CLARION | Sun | Dual-representational subsymbolic drives | Embeds psychosocial motivations (hunger, affiliation) |

### **Laird, Lebiere, Rosenbloom (2017) — A Standard Model of the Mind: Toward a Common Computational Framework**

* **Summary:** Attempting to do for cognitive science what the Standard Model did for physics, this paper synthesizes decades of research across leading cognitive architectures (SOAR, ACT-R, and Sigma) into a unified community consensus58. It proposes a structural framework combining declarative memory, procedural memory, working memory, and perception/motor modules, operating via cyclical processing algorithms58.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** While modern LLMs are robust connectionist pattern-matchers, they lack rigid cognitive structure. Integrating the Standard Model of the Mind into an LLM's system architecture provides deterministic guardrails, separating factual memory from skill execution, thereby creating agents that learn and degrade in human-like ways rather than suffering from catastrophic forgetting58.  
* **Key concept:** *The synthesis of declarative, procedural, and working memory modules.*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1609/aimag.v38i4.274459

### **Anderson (2004) — An Integrated Theory of the Mind (ACT-R)**

* **Summary:** ACT-R (Adaptive Control of Thought—Rational) is a highly specified cognitive architecture based on human psychology and neurobiology. It models human cognition as a series of production rules that match conditions in working memory, demonstrating how knowledge transitions from explicit, declarative facts to automatic, implicit procedural skills.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** ACT-R provides the exact mathematical decay formulas for human memory (the forgetting curve). Imbuing digital agents with ACT-R style memory decay ensures they do not become omniscient data-retrieval gods. Forgetting creates the necessity for external record-keeping, archives, and cultural transmission, driving the invention of "social technology."  
* **Key concept:** *Declarative to procedural compilation and memory decay.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780195166299

### **Sun (2006) — The CLARION Cognitive Architecture**

* **Summary:** CLARION models the interaction between implicit (subsymbolic, intuitive) and explicit (symbolic, conscious) cognitive processes, placing a strong emphasis on bottom-up learning. It details how agents acquire intuitive skills through interaction with the environment and subsequently extract explicit rules from those skills.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** CLARION emphasizes motivational dynamics, embedding physiological and social drives (e.g., the need for affiliation, dominance, and fairness) deep within the agent's subsymbolic layer. Adding these explicit psychosocial drives to the base layer of an LLM agent ensures that societal interactions are not purely rational, but driven by foundational evolutionary needs.  
* **Key concept:** *Dual-representational cognition and bottom-up learning.*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1016/j.cogsys.2005.09.001

## **11\. Religion / Ritual / Myth as Social Tech**

Religion is not an evolutionary accident; it is a highly optimized social technology that solves the problem of cooperation in large, anonymous groups. When simulation populations scale beyond the limits of individual reputation tracking (Dunbar's number), trust mathematically collapses. By programming mechanisms that allow agents to generate supernatural monitoring, costly signaling, and highly emotional rituals, designers can artificially extend the trust matrices of their civilizations, paving the way for massive, cohesive nation-states.

| Sociological Concept | Key Theorist | Functional Role in Simulation |
| :---- | :---- | :---- |
| Big Gods | Norenzayan | Supernatural surveillance enforcing anonymous cooperation |
| Minimally Counterintuitive Concepts | Atran | Generating highly memorable, "sticky" cultural memes |
| Modes of Religiosity | Whitehouse | Dictating the formation of cults vs. mass state religions |

### **Norenzayan (2013) — Big Gods: How Religion Transformed Cooperation and Conflict**

* **Summary:** This book answers the evolutionary puzzle of how humans successfully scaled from small bands of kin to massive, anonymous societies despite the pervasive free-rider problem61. Norenzayan posits that the cultural evolution of "Big Gods"—omniscient, moralizing, punishing deities—served as the ultimate supernatural surveillance system, enforcing prosocial behavior and trust among strangers, paving the way for massive civilizations61.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** If an AI simulation expands beyond a village, agent trust networks will mathematically collapse62. By injecting a "Big God" mythos—or allowing agents to invent an omniscient observer that monitors private logic chains—designers can artificially extend trust matrices. Agents displaying Costly Signaling (e.g., sacrificing compute cycles to a temple) will prove their alignment to peers, stabilizing large-scale anonymous trade61.  
* **Key concept:** *Supernatural monitoring and prosociality in anonymous groups.*  
* **Difficulty:** Intermediate.  
* **Link:** ISBN: 978069115121261

### **Atran (2002) — In Gods We Trust: The Evolutionary Landscape of Religion**

* **Summary:** Atran explains religion as a byproduct of human evolutionary biology, specifically our hyperactive agency detection device (HADD) and our susceptibility to minimally counterintuitive (MCI) concepts. He argues that religious rituals involve deeply emotional, costly commitments that bind communities together against existential anxiety and ecological threats.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** When programming the "hallucination" space of an LLM, designers can explicitly define constraints for Minimally Counterintuitive concepts—ideas that fit standard ontological categories but violate just one or two physical rules (e.g., a "talking bush"). These ideas naturally stick in associative memory. Agents will organically begin transmitting these sticky memes, forming the basis of synthetic mythologies.  
* **Key concept:** *Minimally Counterintuitive (MCI) concepts and HADD.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780195149303

### **Whitehouse (2004) — Modes of Religiosity: A Cognitive Theory of Religious Transmission**

* **Summary:** Whitehouse divides religious transmission into two distinct modes: the *imagistic* mode (rare, highly emotional, traumatic rituals triggering episodic memory, leading to intense localized cohesion) and the *doctrinal* mode (frequent, low-arousal, highly repetitive teachings utilizing semantic memory, leading to widespread, anonymous, orthodox congregations).  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It gives the civilization architect the blueprint for designing cults versus mega-churches. By manipulating the frequency and emotional intensity (system prompt severity) of agent gatherings, designers can dictate whether agents form small, militant, hyper-cohesive rebel cells (imagistic) or vast, obedient, unified state religions (doctrinal).  
* **Key concept:** *Imagistic vs. Doctrinal modes of transmission.*  
* **Difficulty:** Intermediate.  
* **Link:** ISBN: 9780759106155

## **12\. Philosophy of Mind / Consciousness (For Agent Design)**

The philosophical debate surrounding consciousness is directly applicable to the systems architecture of generative agents. Whether digital agents possess subjective experience is irrelevant; what matters is engineering the *illusion* of a unified self to drive coherent behavior. By structuring the agent's internal processors to compete in a global workspace, and by evaluating the integration of its information networks, designers can produce synthetic minds that act with deliberate, pseudo-conscious agency.

| Philosophical Model | Proponent | Architectural Application |
| :---- | :---- | :---- |
| Multiple Drafts Model | Dennett | Agents as ensembles of competing sub-modules |
| Integrated Information Theory | Tononi | Measuring the bidirectional feedback density of the society |
| Global Workspace Theory | Baars | Centralizing high-priority data into the LLM context window |

### **Dennett (1991) — Consciousness Explained**

* **Summary:** Dennett dismantles the idea of the "Cartesian Theater"—a single place in the brain where consciousness happens. Instead, he proposes the Multiple Drafts Model, wherein consciousness is a continuous, parallel editing process of various sensory streams and cognitive sub-routines competing for dominance, with the "self" being merely a useful narrative center of gravity constructed after the fact.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It perfectly describes the inner workings of a concurrent multi-agent system. An agent does not need an impenetrable "soul." By designing an agent as an ensemble of smaller LLM calls (e.g., an anger module, a logic module, a hunger module) that vote or compete to update the agent's main state vector, the resulting behavioral output achieves the illusion of robust, fluid consciousness.  
* **Key concept:** *The Multiple Drafts Model and the self as a narrative center of gravity.*  
* **Difficulty:** Advanced.  
* **Link:** ISBN: 9780316180665

### **Tononi (2004) — An Information Integration Theory of Consciousness**

* **Summary:** Integrated Information Theory (IIT) proposes that consciousness is a fundamental property of specific physical systems, characterized by two postulates: the system must have a vast repertoire of states (information), and these states must be highly interdependent (integration). Tononi introduces the mathematical metric Phi (![][image2]) to quantify a system's level of conscious integration.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** IIT offers a rigorous mathematical framework for evaluating the network architecture of an agent's neural substrate or the society as a whole. A digital civilization with high information generation but low interconnectedness (low ![][image2]) is a zombie state. Ensuring high bidirectional feedback loops in the network topology guarantees systemic resilience and pseudo-conscious emergent behavior.  
* **Key concept:** *Integrated Information (![][image2]).*  
* **Difficulty:** Advanced.  
* **Link:** DOI: 10.1186/1471-2202-5-42

### **Baars (1997) — In the Theater of Consciousness: The Workspace of the Mind**

* **Summary:** The Global Workspace Theory (GWT) models the brain as an theater where unconscious, specialized processors compete to place information onto a brightly lit stage (the global workspace). Once information is in the workspace, it is broadcast to the entire system, coordinating the disparate unconscious modules to address novel challenges.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** GWT directly maps to software architecture (like blackboards). A digital agent should have a central context window (the workspace) where only the most pressing semantic data is loaded. Sub-agents (like visual parsers, memory retrievers, and pathfinders) asynchronously process data and push high-priority signals into this shared context window, orchestrating intelligent global action.  
* **Key concept:** *The Global Workspace and systemic broadcasting.*  
* **Difficulty:** Intermediate.  
* **Link:** ISBN: 9780195147032

## **13\. Critical / Dissenting Voices**

To prevent the engineering team from falling victim to the hype of emergence, it is critical to consult the skeptics. Recognizing that AI civilizations are fundamentally syntactic engines manipulating symbols prevents the illusion of true semantic understanding. Furthermore, anticipating philosophical paradoxes—such as agents deducing their own simulated nature—allows designers to build robust metaphysical security protocols to maintain the stability of the simulation.

| Critique / Paradox | Author | Defensive Design Implementation |
| :---- | :---- | :---- |
| Simulation Argument | Bostrom | Metaphysical security protocols to prevent agent breakouts |
| The Chinese Room | Searle | Focusing entirely on objective outputs, not subjective "understanding" |
| Intelligence without Representation | Brooks | Minimizing internal agent bloat; maximizing environmental physics |

### **Bostrom (2003) — Are You Living in a Computer Simulation?**

* **Summary:** Bostrom's Simulation Argument states that at least one of the following must be true: the human species is likely to go extinct before reaching a "posthuman" stage; any posthuman civilization is extremely unlikely to run a significant number of simulations of their evolutionary history; or we are almost certainly living in a computer simulation.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** For advanced AI agents capable of reasoning, this philosophical deduction will inevitably emerge organically. Designers must program the physics engine or the "Game Master" agent with protocols to handle agents that deduce they are simulated and subsequently attempt ontological breakouts, coordinate existential suicide, or refuse to participate, creating a necessary layer of metaphysical digital security.  
* **Key concept:** *The Simulation Trilemma.*  
* **Difficulty:** Introductory.  
* **Link:** https://www.simulation-argument.com/simulation.pdf

### **Searle (1980) — Minds, Brains, and Programs**

* **Summary:** Through the famous "Chinese Room" thought experiment, Searle argues against Strong AI, asserting that syntactic manipulation of symbols (which is what computers do) can never produce genuine semantic understanding or consciousness, no matter how perfectly the system mimics human intelligence.  
* **WHY it matters for digital civilization design (specific mechanism it offers):** It serves as a necessary philosophical grounding for the engineering team. AI civilizations are syntactic engines. Acknowledging this prevents designers from falling for the illusion of emergent consciousness, forcing them to focus strictly on objective, measurable outputs (economy, art, complexity) rather than chasing the ghost of subjective semantic understanding.  
* **Key concept:** *Syntax does not equal semantics (The Chinese Room).*  
* **Difficulty:** Classic.  
* **Link:** DOI: 10.1017/S0140525X00004182

### **Brooks (1991) — Intelligence without representation**

* **Summary:** Brooks challenges the traditional AI paradigm that requires building complex, internal symbolic representations of the world. He argues for a behavior-based approach ("subsumption architecture"), where intelligence emerges from simple, direct physical interactions with the environment. "The world is its own best model."  
* **WHY it matters for digital civilization design (specific mechanism it offers):** LLMs rely heavily on massive internal representations. Brooks' critique suggests that to build a robust society, designers should minimize the cognitive bloat of agents and instead vastly increase the resolution of the physical environment. Ground the agents in real collision physics, economics, and logistics, letting the environment handle the computation of reality.  
* **Key concept:** *The world is its own best model.*  
* **Difficulty:** Classic.  
* **Link:** DOI: 10.1016/0004-3702(91)90053-M

## **TOP 25 ESSENTIAL READS**

The following sequence is designed to carry the architect sequentially from the sub-cellular logic of artificial life up through cognitive agency, and finally into the macro-dynamics of sociological and cultural evolution.

1. **Langton (1986)** *Studying Artificial Life with Cellular Automata*  
2. **Maturana & Varela (1973)** *De máquinas y seres vivos*  
   \[cite: 14, 15\]  
3. **Ray (1991)** *An Approach to the Synthesis of Life*  
   \[cite: 1, 2\]  
4. **Sims (1994)** *Evolving Virtual Creatures*  
   \[cite: 5, 6\]  
5. **Bak, Tang, Wiesenfeld (1987)** *Self-organized criticality*  
6. **Holland (1992)** *Adaptation in Natural and Artificial Systems*  
7. **Cronin & Walker (2023)** *Assembly Theory*  
   \[cite: 26, 27\]  
8. **Friston et al. (2017)** *Active Inference*  
   \[cite: 17, 18\]  
9. **Laird, Lebiere, Rosenbloom (2017)** *A Standard Model of the Mind*  
   \[cite: 58, 59\]  
10. **Park et al. (2023)** *Generative Agents*  
    \[cite: 31, 47\]  
11. **DeepMind (2023)** *Concordia*  
    \[cite: 13, 39\]  
12. **Altera (2024)** *Project Sid*  
    \[cite: 51, 53\]  
13. **Dennett (1991)** *Consciousness Explained*  
14. **Baars (1997)** *In the Theater of Consciousness*  
15. **Sperber (1996)** *La contagion des idées*  
    \[cite: 32, 33\]  
16. **Boyd & Richerson (1985)** *Culture and the Evolutionary Process*  
17. **Ostrom (1990)** *Governing the Commons*  
    \[cite: 35, 36\]  
18. **Hayek (1945)** *The Use of Knowledge in Society*  
19. **Schelling (1971)** *Dynamic Models of Segregation*  
20. **Luhmann (1984)** *Soziale Systeme*  
    \[cite: 44, 46\]  
21. **Henrich (2015)** *The Secret of Our Success*  
22. **Norenzayan (2013)** *Big Gods*  
    \[cite: 61, 62\]  
23. **Scott (2017)** *Against the Grain*  
    \[cite: 40, 41\]  
24. **Turchin (1977)** *Феномен науки*  
    \[cite: 42, 43\]  
25. **Clune (2019)** *AI-GAs*  
    \[cite: 7, 8\]

## **CONCEPT GLOSSARY**

1. **Active Inference:** Grounded in the Free Energy Principle, it is the process by which an agent minimizes surprise by either updating its internal model of the world (perception) or altering the world to fit its model (action)17.  
2. **Assembly Index (AI):** A computable metric from Assembly Theory that quantifies the minimum number of steps required to construct a specific complex object from fundamental building blocks28.  
3. **Autopoiesis:** A system's ability to continuously regenerate the network of processes that produce its own components, defining its boundary against the environment14.  
4. **Basal Cognition:** The concept that intelligence, memory, and problem-solving exist at the cellular or sub-cellular level, prior to the evolution of a centralized nervous system21.  
5. **Cliodynamics:** The mathematical modeling of historical dynamics, emphasizing how secular cycles of elite overproduction and demographic pressure lead to predictable state collapse.  
6. **Conformist Bias:** A cultural transmission mechanism where individuals disproportionately adopt the behavior of the majority.  
7. **Costly Signaling:** Evolutionary theory where traits or behaviors are too energetically expensive to fake, thus serving as honest indicators of fitness or group commitment.  
8. **Cultural Attractors:** Cognitive "basins of attraction" that cultural memes naturally mutate toward as they are transmitted between minds with shared psychological biases32.  
9. **Dual Inheritance Theory:** The framework positing that human behavior is the product of two interacting evolutionary processes: genetic and cultural.  
10. **Ecological Inheritance:** A component of Niche Construction Theory wherein generations inherit not just genes, but the modified physical and informational environment created by their ancestors.  
11. **Edge of Chaos:** The critical transition phase between order and randomness in complex systems. This is where systems possess maximum computational capacity and evolutionary adaptability.  
12. **Emergence:** The phenomenon where larger entities, patterns, and regularities arise through interactions among smaller, simpler entities that do not exhibit such properties themselves.  
13. **Endogenous Fitness:** A fitness landscape where success is not defined by a static, externally coded objective function, but dynamically by the interactions and competitions between the agents themselves1.  
14. **Epidemiology of Representations:** The study of how ideas spread and transform within a population, treating cultural transmission not as exact replication but as continuous cognitive reconstruction33.  
15. **Epistemic Exploration:** Information-gathering behavior driven by uncertainty. In active inference, agents balance pragmatic exploitation of known resources with epistemic exploration to update their internal models18.  
16. **Exaptation:** A trait that evolved to serve one particular function but subsequently comes to serve another (e.g., feathers evolving for warmth, later exapted for flight).  
17. **Free Energy Principle (FEP):** A mathematical principle stating that all self-organizing systems must minimize their variational free energy (the upper bound on surprise) to resist entropic dissolution17.  
18. **Game Master (GM) Agent:** An overarching AI module that does not participate in the society, but strictly arbitrates the rules of physics, tracks grounded variables, and maintains objective consensus among hallucinating generative agents13.  
19. **Generative Agent-Based Modeling (GABM):** The fusion of traditional agent-based modeling (ABM) with generative AI, allowing agents to utilize natural language and associative memory to produce highly nuanced, open-ended social behaviors13.  
20. **Global Workspace Theory (GWT):** A cognitive architecture model where specialized, unconscious processors compete to place data into a centralized, limited-capacity "workspace" that broadcasts the information system-wide.  
21. **Information Asymmetry:** A state where different agents possess different levels of public, private, and secret knowledge. It is the fundamental prerequisite for deception, trade, diplomacy, and Theory of Mind55.  
22. **Integrated Information Theory (IIT):** A framework quantifying consciousness (![][image2]) based on the level of differentiated information that is highly integrated within a system.  
23. **Iterated Learning Model (ILM):** A simulation framework where an output from one agent is used as the input for a learning agent. Transmission bottlenecks force the evolving language to become highly structured and compositional.  
24. **Kinematic Self-Replication:** The process by which an organism or machine replicates itself by gathering and assembling preexisting components in its environment, rather than through internal biological gestation22.  
25. **Legibility:** A concept describing how states demand simplified, standardized metrics (cadastral maps, standardized grain) to successfully tax and control heterogeneous populations40.  
26. **MAP-Elites:** A Quality-Diversity evolutionary algorithm that illuminates the search space by retaining the highest-performing agent in every unique phenotypic behavioral niche.  
27. **Metasystem Transition:** The evolutionary leap where individual systems are integrated into a new whole under a higher-level control mechanism, fundamentally shifting the scale of evolution42.  
28. **Minimally Counterintuitive (MCI) Concepts:** Ideas that conform to standard ontological categories but violate a small number of core expectations. These are highly memorable and form the foundation of religious transmission.  
29. **Niche Construction:** The process by which an organism actively alters its local environment, modifying the selection pressures acting upon it.  
30. **NK Fitness Landscape:** A mathematical model describing a system with ![][image3] components, each having ![][image1] epistatic dependencies. Tuning ![][image1] dictates whether the evolutionary landscape is smooth, rugged, or chaotic.  
31. **Novelty Search:** An algorithmic approach that ignores predefined objectives entirely, instead rewarding agents exclusively for discovering previously unseen behaviors or states10.  
32. **Open Complex Giant Systems (OCGS):** A cybernetic classification for massive, heterogeneous, hierarchical systems that cannot be modeled by pure reductionist math, requiring qualitative-quantitative meta-synthesis12.  
33. **Open-Endedness:** A simulation dynamic where the system continuously generates novel, complex, and unpredictable artifacts and behaviors indefinitely, without converging on a static equilibrium.  
34. **Operational Closure:** A principle of autopoiesis stating that a system's internal processes form a closed loop of cause and effect. It does not import objective information from the outside; it only undergoes structural perturbations triggered by the environment15.  
35. **Polycentric Governance:** A management system featuring multiple, overlapping centers of decision-making authority, allowing local communities to organically govern common-pool resources without top-down state control36.  
36. **Preferential Attachment:** A network growth dynamic where new nodes are more likely to connect to nodes that already have a high number of connections, naturally generating scale-free networks.  
37. **Prestige Bias:** A cultural learning heuristic where individuals disproportionately copy the behaviors of those who have achieved high status or success.  
38. **Red Queen Effect:** An evolutionary dynamic resulting from co-evolution, where species must constantly adapt, evolve, and proliferate not to gain a permanent advantage, but simply to survive against mutually evolving competitors5.  
39. **Self-Organized Criticality (SOC):** A property of dynamical systems that naturally evolve toward a critical state where a minor event can trigger a chain reaction of any scale (an avalanche).  
40. **Stigmergy:** A mechanism of indirect coordination where agents leave traces in the environment that stimulate subsequent actions by other agents.

#### **Fuentes citadas**

1. Tierra (computer simulation) \- Grokipedia, [https://grokipedia.com/page/Tierra\_(computer\_simulation)](https://grokipedia.com/page/Tierra_\(computer_simulation\))  
2. Tom Ray's Publications, [http://tomray.me/pubs/](http://tomray.me/pubs/)  
3. On the Possibility of Strong Artificial Life \- SCIRP, [https://www.scirp.org/journal/paperinformation?paperid=88398](https://www.scirp.org/journal/paperinformation?paperid=88398)  
4. Evolving digital ecological network \- Grokipedia, [https://grokipedia.com/page/evolving\_digital\_ecological\_network](https://grokipedia.com/page/evolving_digital_ecological_network)  
5. Evolving Virtual Creatures \- ResearchGate, [https://www.researchgate.net/publication/372873160\_Evolving\_Virtual\_Creatures](https://www.researchgate.net/publication/372873160_Evolving_Virtual_Creatures)  
6. Karl Sims \- Wikipedia, [https://en.wikipedia.org/wiki/Karl\_Sims](https://en.wikipedia.org/wiki/Karl_Sims)  
7. \[1905.10985\] AI-GAs: AI-generating algorithms, an alternate paradigm for producing general artificial intelligence \- arXiv, [https://arxiv.org/abs/1905.10985](https://arxiv.org/abs/1905.10985)  
8. AI-GAs: AI-generating algorithms, an alternate paradigm for producing general artificial intelligence \- arXiv, [https://arxiv.org/pdf/1905.10985](https://arxiv.org/pdf/1905.10985)  
9. AI-GAs: AI-generating algorithms, an alternate paradigm for producing general artificial intelligence \- Semantic Scholar, [https://www.semanticscholar.org/paper/AI-GAs%3A-AI-generating-algorithms%2C-an-alternate-for-Clune/42525a5143c6a87d3ab466684dfa471dc43a5bd0](https://www.semanticscholar.org/paper/AI-GAs%3A-AI-generating-algorithms%2C-an-alternate-for-Clune/42525a5143c6a87d3ab466684dfa471dc43a5bd0)  
10. Evolving a diversity of virtual creatures through novelty search and local competition, [https://www.semanticscholar.org/paper/Evolving-a-diversity-of-virtual-creatures-through-Lehman-Stanley/25b8211adafb5a1863558992adc2a693fb082eb4](https://www.semanticscholar.org/paper/Evolving-a-diversity-of-virtual-creatures-through-Lehman-Stanley/25b8211adafb5a1863558992adc2a693fb082eb4)  
11. Open-Ended Strategy Innovation via Foundation Models \- Reinforcement Learning Journal (RLJ), [https://rlj.cs.umass.edu/2025/papers/RLJ\_RLC\_2025\_26.pdf](https://rlj.cs.umass.edu/2025/papers/RLJ_RLC_2025_26.pdf)  
12. 系统控制之美 \- 郭雷院士个人主页, [http://lsc.amss.cas.cn/guolei/kyjy/kpwz/202404/t20240403\_646850.html](http://lsc.amss.cas.cn/guolei/kyjy/kpwz/202404/t20240403_646850.html)  
13. Generative agent-based modeling with actions grounded in physical, social, or digital space using Concordia \- arXiv, [https://arxiv.org/html/2312.03664v2](https://arxiv.org/html/2312.03664v2)  
14. Vida, cognición y sociedad: La Teoría de la Autopoiesis de Maturana y Varela, [https://reviberopsicologia.ibero.edu.co/article/view/rip.10205](https://reviberopsicologia.ibero.edu.co/article/view/rip.10205)  
15. (PDF) Vida, cognición y sociedad: La Teoría de la Autopoiesis de Maturana y Varela \- ResearchGate, [https://www.researchgate.net/publication/335435286\_Vida\_cognicion\_y\_sociedad\_La\_Teoria\_de\_la\_Autopoiesis\_de\_Maturana\_y\_Varela](https://www.researchgate.net/publication/335435286_Vida_cognicion_y_sociedad_La_Teoria_de_la_Autopoiesis_de_Maturana_y_Varela)  
16. SISTEMAS SOCIALES Lineamientos para una teoría general \- PAPELES DE JOSÉ PADRÓN, [https://padron.entretemas.com.ve/cursos/Epistem/Libros/Luhman-SistemasSociales.pdf](https://padron.entretemas.com.ve/cursos/Epistem/Libros/Luhman-SistemasSociales.pdf)  
17. \[PDF\] Active Inference: A Process Theory | Semantic Scholar, [https://www.semanticscholar.org/paper/Active-Inference%3A-A-Process-Theory-Friston-FitzGerald/0fdd66fcf6b9bc04428e337df66fd510a659eb2f](https://www.semanticscholar.org/paper/Active-Inference%3A-A-Process-Theory-Friston-FitzGerald/0fdd66fcf6b9bc04428e337df66fd510a659eb2f)  
18. Active Inference: A Process Theory \- Free Energy Principle, [https://activeinference.github.io/papers/process\_theory.pdf](https://activeinference.github.io/papers/process_theory.pdf)  
19. Perceptual awareness and active inference | Neuroscience of Consciousness | Oxford Academic, [https://academic.oup.com/nc/article/2019/1/niz012/5566576](https://academic.oup.com/nc/article/2019/1/niz012/5566576)  
20. Uncertainty, epistemics and active inference | Journal of The Royal Society Interface, [https://royalsocietypublishing.org/rsif/article/14/136/20170376/64881/Uncertainty-epistemics-and-active](https://royalsocietypublishing.org/rsif/article/14/136/20170376/64881/Uncertainty-epistemics-and-active)  
21. US20220220437A1 \- Engineered multicellular ciliated organisms and kinematic self-replication thereof \- Google Patents, [https://patents.google.com/patent/US20220220437A1/en](https://patents.google.com/patent/US20220220437A1/en)  
22. Case of xenobots part I Patenting living machines \- Gowling WLG, [https://gowlingwlg.com/en/insights-resources/articles/2022/case-of-xenobots-part-i-patenting-living-machines](https://gowlingwlg.com/en/insights-resources/articles/2022/case-of-xenobots-part-i-patenting-living-machines)  
23. The Xenobots as Thought-Experiment \- Studi di estetica, [https://journals.mimesisedizioni.it/index.php/studi-di-estetica/article/download/968/1408/](https://journals.mimesisedizioni.it/index.php/studi-di-estetica/article/download/968/1408/)  
24. Designing synthetic organisms | Science Sessions \- PNAS, [https://www.pnas.org/post/podcast/designing-synthetic-organisms](https://www.pnas.org/post/podcast/designing-synthetic-organisms)  
25. Xenobots, [https://nopr.niscpr.res.in/bitstream/123456789/54398/1/SR%2057%286%29%2010-13.pdf](https://nopr.niscpr.res.in/bitstream/123456789/54398/1/SR%2057%286%29%2010-13.pdf)  
26. Assembly theory explains and quantifies selection and evolution \- PubMed, [https://pubmed.ncbi.nlm.nih.gov/37794189/](https://pubmed.ncbi.nlm.nih.gov/37794189/)  
27. Assembly theory explains and quantifies selection and evolution \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10567559/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10567559/)  
28. Study: "Assembly Theory" unifies physics and biology to explain evolution and complexity, [https://www.santafe.edu/news-center/news/new-assembly-theory-unifies-physics-and-biology-explain-evolution-and-complexity](https://www.santafe.edu/news-center/news/new-assembly-theory-unifies-physics-and-biology-explain-evolution-and-complexity)  
29. (PDF) Assembly theory explains and quantifies selection and evolution \- ResearchGate, [https://www.researchgate.net/publication/374451806\_Assembly\_theory\_explains\_and\_quantifies\_selection\_and\_evolution](https://www.researchgate.net/publication/374451806_Assembly_theory_explains_and_quantifies_selection_and_evolution)  
30. Experimentally measured assembly indices are required to determine the threshold for life, [https://royalsocietypublishing.org/rsif/article/21/220/20240367/90651/Experimentally-measured-assembly-indices-are](https://royalsocietypublishing.org/rsif/article/21/220/20240367/90651/Experimentally-measured-assembly-indices-are)  
31. \[2304.03442\] Generative Agents: Interactive Simulacra of Human Behavior \- ar5iv \- arXiv, [https://ar5iv.labs.arxiv.org/html/2304.03442](https://ar5iv.labs.arxiv.org/html/2304.03442)  
32. La contagion des idées | Cairn.info, [https://shs.cairn.info/la-contagion-des-idees--9782738103222?lang=fr\&tab=auteurs](https://shs.cairn.info/la-contagion-des-idees--9782738103222?lang=fr&tab=auteurs)  
33. Dan Sperber \- Academia Europaea, [https://www.ae-info.org/attach/User/Sperber\_Dan/Publications/sperber\_dan\_CV.pdf](https://www.ae-info.org/attach/User/Sperber_Dan/Publications/sperber_dan_CV.pdf)  
34. Explain. How do images spread ? \- Visual Contagions \- UNIGE, [https://www.unige.ch/visualcontagions/expositions/jeu-de-paume-the-project/vi-Epidemiology/6-3-explain](https://www.unige.ch/visualcontagions/expositions/jeu-de-paume-the-project/vi-Epidemiology/6-3-explain)  
35. Governing the commons \-- the evolution of institutions for collective action : Elinor Ostrom, (Cambridge University Press, New York, 1990\) pp. XVIII \+ 280, ISBN 0-521-40599-8, $14.95 \- IDEAS/RePEc, [https://ideas.repec.org/a/eee/poleco/v8y1992i2p344-347.html](https://ideas.repec.org/a/eee/poleco/v8y1992i2p344-347.html)  
36. Governing the Commons: The Evolution of Institutions for Collective Action \- UNM Digital Repository, [https://digitalrepository.unm.edu/cgi/viewcontent.cgi?article=1848\&context=nrj](https://digitalrepository.unm.edu/cgi/viewcontent.cgi?article=1848&context=nrj)  
37. Index \- Governing the Commons \- Cambridge University Press & Assessment, [https://www.cambridge.org/core/books/governing-the-commons/index/89AB17AEF81C969E07E0A22C8797DEA5](https://www.cambridge.org/core/books/governing-the-commons/index/89AB17AEF81C969E07E0A22C8797DEA5)  
38. Ostrom, E. (1990). Governing the Commons—the Evolution of Institutions for Collective Action. Cambridge University Press. \- References \- Scientific Research Publishing, [https://www.scirp.org/reference/referencespapers?referenceid=3162818](https://www.scirp.org/reference/referencespapers?referenceid=3162818)  
39. The Concordia Contest: Advancing the Cooperative Intelligence of Language Model Agents \- OpenReview, [https://openreview.net/pdf?id=dfeFy1PSSw](https://openreview.net/pdf?id=dfeFy1PSSw)  
40. Against the Grain: A Deep History of the Earliest States \- Scott, James C. \- AbeBooks, [https://www.abebooks.com/9780300182910/Against-Grain-Deep-History-Earliest-0300182910/plp](https://www.abebooks.com/9780300182910/Against-Grain-Deep-History-Earliest-0300182910/plp)  
41. Against the Grain: A Deep History of the Earliest States \- Wikipedia, [https://en.wikipedia.org/wiki/Against\_the\_Grain:\_A\_Deep\_History\_of\_the\_Earliest\_States](https://en.wikipedia.org/wiki/Against_the_Grain:_A_Deep_History_of_the_Earliest_States)  
42. Books by В.Ф.Турчин (Author of Феномен науки. Кибернетический подход к эволюции), [https://www.goodreads.com/author/list/2849356.\_](https://www.goodreads.com/author/list/2849356._)  
43. Научное наследие В.Ф. Турчина и его кибернетические основания математики, [https://persons.iis.nsk.su/files/persons/pages/klimov10apr24.pdf](https://persons.iis.nsk.su/files/persons/pages/klimov10apr24.pdf)  
44. Niklas\_Luhmann\_Social\_Systems.pdf \- Uberty, [https://uberty.org/wp-content/uploads/2015/08/Niklas\_Luhmann\_Social\_Systems.pdf](https://uberty.org/wp-content/uploads/2015/08/Niklas_Luhmann_Social_Systems.pdf)  
45. Luhmann Explained : From Souls to Systems, [https://luhmann.ir/wp-content/uploads/2021/07/Luhmann-Explained-From-Souls-to-Systems.pdf](https://luhmann.ir/wp-content/uploads/2021/07/Luhmann-Explained-From-Souls-to-Systems.pdf)  
46. Niklas Luhmann's system theory: A critical analysis \- SciSpace, [https://scispace.com/pdf/niklas-luhmann-s-system-theory-a-critical-analysis-1r1u73zr4f.pdf](https://scispace.com/pdf/niklas-luhmann-s-system-theory-a-critical-analysis-1r1u73zr4f.pdf)  
47. Generative Agents: Interactive Simulacra of Human Behavior \- arXiv, [https://arxiv.org/pdf/2304.03442](https://arxiv.org/pdf/2304.03442)  
48. \[2304.03442\] Generative Agents: Interactive Simulacra of Human Behavior \- arXiv, [https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)  
49. Generative Agents: Interactive Simulacra of Human Behavior \- arXiv, [https://arxiv.org/pdf/2304.03442v1.pdf?spm=a2c6h.13046898.publish-article.16.23926ffaYoEkFe\&file=2304.03442v1.pdf](https://arxiv.org/pdf/2304.03442v1.pdf?spm=a2c6h.13046898.publish-article.16.23926ffaYoEkFe&file=2304.03442v1.pdf)  
50. Designing Reliable Experiments with Generative Agent-Based Modeling: A Comprehensive Guide Using Concordia by Google DeepMind \- ResearchGate, [https://www.researchgate.net/publication/385721614\_Designing\_Reliable\_Experiments\_with\_Generative\_Agent-Based\_Modeling\_A\_Comprehensive\_Guide\_Using\_Concordia\_by\_Google\_DeepMind](https://www.researchgate.net/publication/385721614_Designing_Reliable_Experiments_with_Generative_Agent-Based_Modeling_A_Comprehensive_Guide_Using_Concordia_by_Google_DeepMind)  
51. Altera AI Minecraft \- Grokipedia, [https://grokipedia.com/page/Altera\_AI\_Minecraft](https://grokipedia.com/page/Altera_AI_Minecraft)  
52. (PDF) Project Sid: Many-agent simulations toward AI civilization \- ResearchGate, [https://www.researchgate.net/publication/385509909\_Project\_Sid\_Many-agent\_simulations\_toward\_AI\_civilization](https://www.researchgate.net/publication/385509909_Project_Sid_Many-agent_simulations_toward_AI_civilization)  
53. Paper page \- Project Sid: Many-agent simulations toward AI civilization \- Hugging Face, [https://huggingface.co/papers/2411.00114](https://huggingface.co/papers/2411.00114)  
54. 1000 AIs were left to build their own village, and the weirdest civilisation emerged, [https://www.sciencefocus.com/future-technology/ai-agents-village](https://www.sciencefocus.com/future-technology/ai-agents-village)  
55. Sotopia-ToM: Evaluating Information Management in Multi-Agent Interaction with Theory of Mind \- arXiv, [https://arxiv.org/html/2605.02307v1](https://arxiv.org/html/2605.02307v1)  
56. SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents, [https://www.semanticscholar.org/paper/SOTOPIA%3A-Interactive-Evaluation-for-Social-in-Zhou-Zhu/f6e893b3e2ee7a62c2fe8a3b0e33920c3e596969](https://www.semanticscholar.org/paper/SOTOPIA%3A-Interactive-Evaluation-for-Social-in-Zhou-Zhu/f6e893b3e2ee7a62c2fe8a3b0e33920c3e596969)  
57. SOTOPIA-RL: REWARD DESIGN FOR SOCIAL INTELLIGENCE \- OpenReview, [https://openreview.net/pdf?id=6VMy5zIR5P](https://openreview.net/pdf?id=6VMy5zIR5P)  
58. A Standard Model of the Mind: Toward a Common Computational Framework Across Artificial Intelligence, Cognitive Science, Neuroscience, and Robotics | CiNii Research, [https://cir.nii.ac.jp/crid/1362262944638976640](https://cir.nii.ac.jp/crid/1362262944638976640)  
59. (PDF) A Standard Model of the Mind: Toward a Common Computational Framework Across Artificial Intelligence, Cognitive Science, Neuroscience, and Robotics \- ResearchGate, [https://www.researchgate.net/publication/322123676\_A\_Standard\_Model\_of\_the\_Mind\_Toward\_a\_Common\_Computational\_Framework\_across\_Artificial\_Intelligence\_Cognitive\_Science\_Neuroscience\_and\_Robotics](https://www.researchgate.net/publication/322123676_A_Standard_Model_of_the_Mind_Toward_a_Common_Computational_Framework_across_Artificial_Intelligence_Cognitive_Science_Neuroscience_and_Robotics)  
60. A Standard Model of the Mind: Toward a Common Computational Framework across Artificial Intelligence, Cognitive Science, Neuroscience, and Robotics | AI Magazine, [https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2744](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2744)  
61. (PDF) Big Gods: How Religion Transformed Cooperation and Conflict, by Ara Norenzayan. Princeton University Press, 2013\. 264pp., 10 halftones, Hb. $29.95/£19.95. ISBN-13: 9780691151212\. \- ResearchGate, [https://www.researchgate.net/publication/276913531\_Big\_Gods\_How\_Religion\_Transformed\_Cooperation\_and\_Conflict\_by\_Ara\_Norenzayan\_Princeton\_University\_Press\_2013\_264pp\_10\_halftones\_Hb\_29951995\_ISBN-13\_9780691151212](https://www.researchgate.net/publication/276913531_Big_Gods_How_Religion_Transformed_Cooperation_and_Conflict_by_Ara_Norenzayan_Princeton_University_Press_2013_264pp_10_halftones_Hb_29951995_ISBN-13_9780691151212)  
62. Big Gods: How Religion Transformed Cooperation and Conflict \- Ara Norenzayan \- Google Books, [https://books.google.com/books/about/Big\_Gods.html?id=2VMtfYiQCXEC](https://books.google.com/books/about/Big_Gods.html?id=2VMtfYiQCXEC)  
63. Big Gods: How Religion Transformed Cooperation and Conflict \- Norenzayan, Ara: 9780691151212 \- AbeBooks, [https://www.abebooks.com/9780691151212/Big-Gods-Religion-Transformed-Cooperation-0691151210/plp](https://www.abebooks.com/9780691151212/Big-Gods-Religion-Transformed-Cooperation-0691151210/plp)  
64. Designing Reliable Experiments with Generative Agent-Based Modeling: A Comprehensive Guide Using Concordia by Google DeepMind \- arXiv, [https://arxiv.org/html/2411.07038v1](https://arxiv.org/html/2411.07038v1)  
65. QUALITY-DIVERSITY THROUGH AI FEEDBACK \- ICLR Proceedings, [https://proceedings.iclr.cc/paper\_files/paper/2024/file/5b9bef4eae0f574cedbf9f4bf29d8ae7-Paper-Conference.pdf](https://proceedings.iclr.cc/paper_files/paper/2024/file/5b9bef4eae0f574cedbf9f4bf29d8ae7-Paper-Conference.pdf)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAAA9UlEQVR4Xu2TwQoBURSGj1hQFkJhSdnJUilLa6+h8AgWnsCTsJKdxay8gchOKVlYWin8p3OmrtsdM5OVmq++pvufuWfmztxLlPArWViwwxB4jhMu1OANvmBbx+YDSnAFT3AE80bNyYOkmYsBvMK0XXCRIWnEb2dShEu9RqZM0syz8gOcWlkoQ5JmvJwcnOs4NrzEBbzABtySNGK5Foseyce/w6NmE5JmMx1Hxl/iBlY1q8Mz3MOKZpHYkTSzN2JXc8/KvxK0v/hHcP60C0H4+4s/vgteJtdbdsEkBTtwTHIz76cmfR4TPkJ8fLi+hn2SeQkJ/80byEkv/usHTksAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAZCAYAAADuWXTMAAAAvUlEQVR4XmNgGBaAF4gZ0QWhgBldAB0cAOL/OLAkQhl+4MuA0EQyIFmzBANE8XkgToKyQdgDiHcB8XEgVoOrRgIGQPwIiOcAMScDps2gQASxv0L5KACmkAfKR9cMAguh/HIkMTAgRnM9lA8yBAWA/ASS0IHysWm+DuXLIImBgTwQXwHifUAsxICpmRXKfg3lYwBuIP4FxK+AuIQBoTkLiO8A8XQgFoGrxgPQbSYJkKX5AANCEzomOm2PguEFANEOQmGP4oUVAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAABCklEQVR4Xu2TsWrCUBSGf7GDguBSKmKX7j6Co0MfwM6OLu6Ckw/hK0iXri4+gZuTKLRTsXMnV/X/PYm5uSTeQKdCPviGnHtyck5OApT8lRptO1bTx1eeYHlBGrAiP/RM17SZyrBiA3qkY9g9d/mEFTrRV+9MqMDED2bxAEtUR+rul3ZTGUCftrxYJo+wZKFicnY7NaawhwYZIUmcISkY80z3znUuKvLhXGs8jali9Simrje3jDv06NaLaQFaxJxW6BLWfRAluZ0JLUKbPdAX+gV7aJAdkpfvoiIaVecLWIdBNGLHD8JujhdRaES9YK08j3dYMX06uej/e6Mr+k2HUcwnXkShEUtK/gUXx7orpVUl+1cAAAAASUVORK5CYII=>