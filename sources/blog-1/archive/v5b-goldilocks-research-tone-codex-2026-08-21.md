<!-- Dates checked 2026-08-20: ChatGPT 2022-11-30; ChatGPT Pro 2024-12-05; open-weights coalition letter hosted by NVIDIA 2026-07-24; Amazon/Lean FRO 2026-07-26; Mojo 1.0 2026-08-11; Mojo OSS 2026-08-18; DeepSeek Harness developer preview checked 2026-08-20. -->

# The Goldilocks Zone of the Open AI Ecosystem

*Open and closed systems will coexist. The research question is which layers require open semantics, interfaces, or evidence for software written by agents to be trusted.*

**AI coding agents have exposed a missing layer between human intent and executable side effects.** Present tools do not consistently carry a task's authority, preservation obligations, and completion evidence from the user's instruction to the resulting repository mutation.

Filling that layer is a calibration problem on two axes. On rigor, the useful region lies between prompt-only intent with ambient permissions and the unrealistic demand that every edit carry a full formal proof. On openness, it lies between a closed vertical system that owns model, harness, policy, compiler, and evidence, and a fragmented ecosystem in which source code exists but common semantics do not.

Open and closed systems will coexist. Many frontier models are closed today, and closed systems will remain part of the stack. The connective layers are different. Evidence formats, policy semantics, agent protocols such as ACP and MCP, compiler intermediate representations, and analyzers attached to those representations exist to connect independent systems. Their value depends on inspection, replacement, replay, and independent review. By contrast, hosted inference, enterprise control planes, proprietary data, and specialized clients can remain closed if the surrounding interfaces emit portable evidence.

That boundary is the Goldilocks zone. Several current systems illustrate it. Modular opened the Mojo compiler while retaining governance over compiler contributions. Amazon supports Lean through an external research organization. Zed participates in an open agent protocol while individual agents may remain closed. Cedar's semantics and implementation are open, while a hosted authorization service can be commercial. This essay maps that boundary and opens the first of three threads, each revisited quarterly.

| Thread | Parts |
|---|---|
| The Golden Era of the Open Ecosystem | 6: this essay · open models and model competition · open agent harnesses · open compilers and AI-native languages · open protocols and portable evidence · incentives and the open social contract |
| Hybrid Analysis | 3: static vs. dynamic analysis · verification vs. validation · static and dynamic evidence with verification and validation |
| Future of Software Engineering | 3: IDEs, CLIs, and harnesses · language wars in the agent era · review, acceptance, and ownership |

## 1. Where the abstraction leaks

My working position is one window. Zed is the editor, the CLI is the execution substrate, and Codex, Claude Code, and Cursor enter through the shell or the Agent Client Protocol, ACP. The important property is agent substitutability. The workflow, constraints, and evidence remain stable while the actor changes. A narrow task can move to a local model, and a verification obligation can move to a proof tool, without changing the surrounding engineering record.

That position is a useful test, and the current abstraction remains under-specified.

Intent is informal: "refactor the parser." Permissions are ambient: whatever the shell user can touch, the agent can touch. Handoffs are prose: one agent writes Markdown and another reads it. Effects are invisible: a dependency added, a CI file edited, a network call made. Completion is social: "done" is a sentence, and the evidence for it is a summary written by the party under review.

A human engineer reads "refactor the parser" and knows what it excludes: no public API change, no new dependency, no CI edit, no network. The boundary is real and was never written down.

> Human engineers infer boundaries from culture, experience, and consequence. Agentic systems require those boundaries to be represented explicitly.

That is the law of leaky abstractions in the agent loop. The Cordis paper, whose runtime model returns below, gives a concrete platform analogue. It reports that most of the top VS Code extensions need a host restart to be removed, and that cross-extension exports are typed broadly by default. If a platform does not commit effects at load time, it has little structure with which to unwind them at unload time. An agent harness is the same class of platform, with a model acting through tools.

![F1 — Leaky pipeline vs. typed pipeline](diagrams/F1-leaky-vs-typed.svg)
*F1 — One task through an untyped pipeline (left) and a checked one (right); every leak on the left has its check on the right.*

Every leak sits in connective tissue: between human and agent, agent and agent, agent and filesystem. That tissue has to be open for anyone to check it.

## 2. The task record

Every abstraction leaks. Types did not eliminate leaks; they made many of them observable at boundaries. The analogous question for an agentic task is what record the system carries from instruction to execution.

The record needs six fields.

- Preconditions: what the task assumes before work begins.
- Postconditions: what must hold after the task.
- Invariants: what must remain true throughout the change.
- Capabilities: what authority the actor receives.
- Effects: what side effects are allowed or forbidden.
- Evidence: what artifacts must be produced before acceptance.

This task record is not admitted simply because a model drafted it. It is a proposed interface between human intent and machine action. A handoff between agents should point to that record rather than rely on a paragraph of prose, and downstream tools consume different portions of the record.

![F2 — Task record and review paths](diagrams/F2-task-record.svg)
*F2 — The task record separates authorization, obligations, runtime effects, and witness evidence.*

Capabilities and effects become authorization constraints. For example, a parser refactor may allow reads and writes under parser and test directories, while forbidding network access, dependency edits, and CI changes. Cedar is a useful language for this layer because it asks whether a principal may perform a given action on a given resource in a given context.

Cedar is not the formalizer. It does not decide whether the parser remains correct. It constrains authority. That distinction is central: the permission decision and the correctness argument are separate claims.

Preconditions, postconditions, and invariants become obligations. In the parser example, the public interface should remain stable, the relevant tests should pass, and clients of the specified parser surface should not observe a behavioral change. Those obligations may be discharged by tests, static analysis, dynamic traces, or proof depending on risk.

Effects become runtime checks. The harness watches the run and compares each observed side effect with the declared task boundary. No static effect system can see every tool loaded after deployment, so Cordis makes effects and coeffects runtime objects. In this setting, an undeclared access becomes an error rather than a post hoc surprise.

Evidence becomes a witness: tests run, traces captured, policy decisions logged, obligations discharged or refuted, and the human decision that accepted residual risk.

> Authorization and verification should be derived from the same task record, but they answer different questions.

An obligation with nowhere to land is ceremony, and two developments give obligations ground. Theory-level autoformalization, a position paper by Min, Bastani, and colleagues, moves the target from isolated statements to formal knowledge bases: definitions, lemmas, and invariants a new obligation can be stated against.

CSLib aims to be the Mathlib for computer science, in two pillars: formalizing CS itself (models of computation, automata, operational semantics, program logics, complexity, concurrency, verified algorithms) and Boole, a Lean-embedded intermediate verification language that generates verification conditions for multiple proof tools. Its authors identify the bottleneck as the availability of abstractions in the underlying proof assistant. Their governance rule is directly relevant to agentic software engineering: AI tools are advisory, and committed proofs require manual review.

Admission is a pipeline: candidate formalization, proof checking, semantic review, and integration into a trusted library for future tasks. Proof checking asks whether the artifact satisfies the stated obligation. Semantic review asks whether the obligation captured the intended claim. A proof against the wrong task record is one of autoformalization's easiest failures, and it is the subject of Thread 2's second essay.

Cedar itself shows where the open-closed boundary falls. Its semantics are formalized in Lean in cedar-spec, the Rust implementation is differentially tested against that spec, and cedar-policy-symcc compiles policies to SMT to prove never-errors, always-allows, subsumption, and equivalence, with cvc5 counterexamples. Amazon Verified Permissions, the hosted service, is paid. The connective semantics are open and independently inspectable; the hosted service occupies a separate implementation layer.

## 3. Progressive commitment: the layer cake

Compilers solved this shape of problem decades ago: parse tree, typed representation, intermediate representation, lowering, and code generation. Each stage makes some ambiguity impossible and some invariant checkable. The layer cake is that pipeline lifted above the code. The task record is progressively committed as it moves from human intent to policy, harness execution, compiler-visible structure, and evidence.

![F3 — The AI layer cake](diagrams/F3-layer-cake.svg)
*F3 — One row per layer: what it commits, its open reference, and the appropriate openness boundary.*

**Human intent** commits a goal and arrives through whichever client a person types into, open or closed.

**Formal intent and policy** commit the task boundary. Authority becomes decidable, obligations become stated, and "what was the agent allowed to do" becomes an auditable lookup. This layer requires open semantics: a policy language understood by only one product is configuration, not policy infrastructure.

**The agent harness** commits execution: which tool ran, under which capability, with what result. It is a runtime. Cordis is useful because it treats context, effects, lifecycle state, and recovery behavior as first-class runtime concerns. Loading a component records what it did; unloading has enough information to reverse or retire the relevant effects. Without such structure, agent runs inherit familiar platform failures: a tool present when the model read its schema but absent at call time, or a permission granted for one payload and reused for another.

DeepSeek Harness, MIT-licensed on Cordis and in developer preview, states its invariants. Everything is a plugin. Model-visible means logged: anything that reaches a model request is reconstructable from the log, and a runtime assertion enforces it.

Each seam has a definition, a provider, and a consumer, so pointing the filesystem and subprocess providers at a remote sandbox can carry Bash, PTY, and LSP with them. The protocol and effect log need open semantics; individual agents can remain closed.

**Compiler and language** commits meaning: typed structure with an IR that analyzers can attach to. Mojo 1.0 (2026-08-11) is a stability milestone, with 1.x changes primarily additive, and a week later (2026-08-18) Modular opened the compiler and toolchain under Apache 2.0 with LLVM exceptions in modular/modular.

Mojo's vision document frames the language as closely tied to MLIR. The broader compiler significance is that an open, MLIR-native, general-purpose compiler can become a pattern book for domain-specific languages on MLIR and for verification hooks inserted before lowering erases the structure they need. Modular is not taking compiler contributions yet, and says why: in the current era of AI coding, contribution governance has to be deliberate. This is another instance of the Goldilocks boundary: source and interfaces can be open while contribution gates remain governed.

**Executable** commits behavior, and it can sit on either side. **Evidence and witness** commit the record. Evidence needs portable representation; evidence legible only inside one vendor dashboard is difficult to audit independently.

Below the cake sit cloud, chips, and energy, decisive for the cost floor and outside this series.

My research lineage is hybrid program analysis, so I watch the evidence layer. Jitana and ReHAna were built for Android, where reflection and dynamic class loading hid running code from static analysis, while a trace showed little about paths it did not exercise. Each evidence mode omits something. The discipline is to make those omissions explicit and to let each mode challenge the others. The agent loop reproduces the same split: a patch is a static artifact, tool calls are dynamic behavior, logs are traces, tests are sampled executions, and a proof is a scoped formal claim. Reconciling them is the evidence layer's whole job and the subject of Thread 2.

## 4. Calibration

A structured task record is what makes calibration possible. A prose handoff cannot be tuned precisely, but a task record can state which obligations must be discharged for a given risk level. The failure corners are symmetric. On rigor, too little structure yields ambient permissions and summary-as-evidence; too much structure demands proof for every edit and lets ceremony outrun signal. On openness, too little structure yields the closed vertical; too much uncoordinated openness yields fragmentation: source exists, nothing composes, dialects drift, and adoption happens by fork.

![F4 — The Goldilocks zone on two axes](diagrams/F4-goldilocks.svg)
*F4 — Rigor by openness, with the zone bounded on all four sides.*

The zone on rigor is evidence proportional to risk. A documentation edit earns a diff review and a test run. A parser refactor earns tests, static checks, and traces. An authorization or payments boundary earns policy review, a proof obligation where appropriate, and explicit human signoff. The task record should carry enough information to place the work in the correct evidence band before edits begin.

> Rigor belongs to the task, not the agent, and the evidence requirement should be fixed before a line changes.

The evidence vocabulary has seven labels: proved, refuted, tested, observed, judged, assumed, not checked. The labels cost nothing and block the most common failure in agent workflows: a proof over one property quietly presented as a proof over the system. Collapse them into one green check and the leak is back. The bands and the vocabulary are the contract between tools, which puts calibration itself on the open side of the boundary.

## 5. Which layers open, and why

Three forces open a layer. Common infrastructure: everyone needs to build on it. Strategic collaboration: sharing it beats competing over it. Network effects: it is worth more with every implementation that speaks it. LLVM is all three compounding, a permissive compiler substrate funded by rivals and valuable in proportion to the languages and targets on it.

Openness at a connective layer is architectural: its value comes from external adoption, inspection, and interoperability rather than from exclusivity alone.

**Weights can be closed.** The open-weights letter NVIDIA hosted (2026-07-24), with over two hundred co-signers, argues on access, competition, control, adaptability, and security. Closed frontier models will coexist with open ones, and software trust does not reduce to weight access alone.

**Harness semantics should be open.** DeepSeek Harness on Cordis is a useful example of how a harness can expose plugin structure and runtime behavior.

**Compiler interfaces should be open; contribution gates can remain governed.** Mojo's compiler is Apache 2.0 with LLVM exceptions; its contribution queue is currently closed, but analyzers can still study and target the exposed compiler structure.

**Protocols should be open; editors and agents can vary.** Zed is implemented largely in Rust on its own GPU framework, gpui, under GPL-3.0-or-later. ACP is Apache-2.0 with no CLA, JSON-RPC over stdio with a typed schema, SDKs in five languages, and JetBrains co-developing. Zed charges nothing for external agents, and closed agents can still participate behind the protocol boundary.

**Proof tools require open governance.** Amazon's donation to the Lean FRO (2026-07-26), the FRO's largest ever, went outside Amazon on purpose: "it's easier to trust a proof when you can evaluate the tools behind it yourself," so that customers, auditors, and regulators can inspect work done in community-governed tools. The proof checker is close to the final trust boundary, so its governance cannot be treated as an ordinary implementation detail.

## 6. Admission and governance

**A model may propose; admission requires independent evidence.** The reason is structural: the approximate representation that makes a model a strong proposer also makes it unsuitable as the sole authority for acceptance.

If the verifier refutes the claim, the counterexample becomes a regression fixture. If it cannot decide, the claim stays unadmitted. A model's output is advisory until a deterministic check, a proof, a policy decision, or a human promotes it, and the promotion is recorded in the witness with its evidence class attached.

![F5 — From intent to acceptance](diagrams/F5-central-graph.svg)
*F5 — Intent is formalized into policy and obligations, executed under a harness, checked by compiler and analyzers, and accepted on evidence.*

That rule is the Goldilocks boundary applied to governance. Each layer should commit enough structure that admission is reviewable, and enough of the connective layer should be open that admission can be inspected outside the vendor that produced the artifact.

Compilers learned progressive commitment decades ago. The stack above the code is now learning a similar discipline for agentic software engineering.

The proposal source may be closed, but admission should depend on evidence that can be inspected outside the proposing system.

Next: Part 2, Open Models and Model Competition.

## References

### Compiler

1. Modular, "Mojo is now open source" (2026-08-18): https://www.modular.com/blog/mojo-open-source
2. Modular, "Modular 26.5: Mojo 1.0 is here" (2026-08-11): https://www.modular.com/blog/modular-26-5-mojo-1-0-is-here
3. Mojo documentation, "Mojo vision" (built purely on MLIR Core; syntactic sugar for MLIR): https://mojolang.org/docs/vision/

### Autoformalization and verification

4. M. J. Min, M. He, Z. Li, Z. Yi, S. Malik, A. Gupta, X. Si, O. Bastani, "Theory-Level Autoformalization: From Isolated Statements to Unified Formal Knowledge Bases," arXiv:2607.13292: https://arxiv.org/abs/2607.13292
5. CSLib, "The Lean Computer Science Library," arXiv:2602.04846: https://arxiv.org/abs/2602.04846
6. Amazon Science, "Amazon is investing in the Lean Focused Research Organization" (2026-07-26): https://www.amazon.science/news/amazon-is-investing-in-the-lean-focused-research-organization

### Policy

7. Cedar policy language, Rust implementation, and cedar-policy-symcc: https://github.com/cedar-policy/cedar
8. cedar-spec, Lean formalization and differential testing: https://github.com/cedar-policy/cedar-spec

### Harness

9. DeepSeek Harness (MIT, developer preview, checked 2026-08-20): https://github.com/deepseek-ai/deepseek-harness and https://deepseek.com/harness/en/
10. Cordis, "A Programming Paradigm for Spatiotemporal Composability," theory-to-implementation table p.55: https://github.com/cordiverse/paper/blob/main/paper.pdf

### IDE and protocol

11. Zed: https://github.com/zed-industries/zed
12. Agent Client Protocol: https://agentclientprotocol.com

### Open weights

13. "Open Weights and American AI Leadership," coalition letter hosted by NVIDIA (2026-07-24): https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf

### Author lineage

14. Jitana: https://github.com/ytsutano/jitana
15. ReHAna, MobiQuitous 2021: https://doi.org/10.1007/978-3-030-94822-1_19
16. DBLP, Shakthi Bachala: https://dblp.org/pid/200/1146.html
