<!-- Dates checked 2026-08-20: ChatGPT 2022-11-30; ChatGPT Pro 2024-12-05; NVIDIA open-weights pledge 2026-07-24; Amazon/Lean FRO 2026-07-26; Mojo 1.0 2026-08-11; Mojo OSS 2026-08-18; DeepSeek Harness developer preview checked 2026-08-20. -->

# The Goldilocks Zone of the Open AI Ecosystem

*Open and closed systems will coexist. The question is which layers must be open for software written by agents to be trusted.*

**AI coding agents have exposed a missing layer between human intent and executable side effects.** Nothing in today's stack carries what a task permits, what it must preserve, and what counts as done from the typed sentence to the written bytes.

Filling that layer is a calibration problem on two axes. On rigor, the zone sits between prompt-only intent with ambient permissions and a proof for every edit. On openness, it sits between one vendor owning model, harness, policy, compiler, and evidence, and a scatter of source that never composes. The right answer on both axes is a Goldilocks zone.

Open and closed will coexist. The frontier models are closed and will stay closed. **The connective layers must be open:** evidence formats, policy semantics, agent protocols, compiler IR and the analyzers that attach to it. They exist to connect independent systems; closing them destroys the reason they exist, and they are where inspection, replacement, and replay happen. **The leaves can be closed:** weights, hosted inference, enterprise control planes, proprietary data, the best client, as long as the layers around them emit portable evidence.

That boundary is the zone, and every serious vendor is choosing where it sits. Modular opened its compiler and closed contributions. Amazon funds Lean outside Amazon. Zed opened its agent protocol while the agents stay closed. Cedar's semantics are open while the hosted service is paid. This essay maps the boundary and opens the first of three threads.

| Thread | Opening series | Cadence |
|---|---|---|
| The Golden Era of the Open Ecosystem | 6 parts: this essay · open models and model competition · open agent harnesses · open compilers and AI-native languages · open protocols and portable evidence · incentives and the open social contract | Revisited quarterly |
| Hybrid Analysis | 3 parts: static vs. dynamic analysis · verification vs. validation · static + dynamic, verification + validation | Revisited quarterly |
| Future of Software Engineering | 3 parts: IDEs, CLIs, and harnesses · language wars in the agent era · review, acceptance, and ownership | Revisited quarterly |

## 1. Where the abstraction leaks

My working position is one window. Zed is the editor, the CLI is the execution substrate, and Codex, Claude Code, and Cursor enter through ACP and the shell. The agents are interchangeable by design. I keep the workflow, the constraints, and the evidence; I swap the agent. When the workflow carries the constraints, a narrow task can go to a local model and an obligation to a prover, and nothing around the swap changes.

That position is a test, and the current abstraction fails it. Intent is informal: "refactor the parser." Permissions are ambient: whatever the shell user can touch, the agent can touch. Handoffs are prose: one agent writes Markdown and another reads it. Effects are invisible: a dependency added, a CI file edited, a network call made. Completion is social: "done" is a sentence, and the evidence for it is a summary written by the party under review.

A human engineer reads "refactor the parser" and infers the boundary from culture and consequence. No public API change, no new dependency, no CI edit, no network. The boundary is real and was never written down.

> Humans infer the boundary from culture and consequence. Agents have to be told, and nothing tells them.

That is the law of leaky abstractions in the agent loop, and there is a datum for how leaky. The Cordis paper surveyed the top 100 VS Code extensions: 87 need a host restart to be removed, and cross-extension exports are typed `any` by default. Nothing was committed at load time, so nothing can be unwound at unload time. An agent harness is the same shape of platform, with a model at the keyboard.

![F1 — Leaky pipeline vs. typed pipeline](diagrams/F1-leaky-vs-typed.svg)
*F1 — The same task through an untyped pipeline (left) and a checked one (right). Each marker on the left is a leak; each marker on the right is the check that replaces it.*

Every leak sits in connective tissue: between human and agent, agent and agent, agent and filesystem. That tissue has to be open for anyone to check it. The model that fills it in can stay closed.

## 2. The type

Every abstraction leaks, and the historical fix has been types. So the question to ask of a task handed to an agent is what its type is. Mine is a six-tuple.

```text
Φ = ⟨Pre, Post, Inv, Cap, Effects, Evidence⟩

Pre       what holds before the task
Post      what must hold after it
Inv       what must never break along the way
Cap       the authority granted
Effects   side effects allowed and forbidden
Evidence  what must be produced for acceptance
```

A model can draft Φ from a sentence; nothing downstream admits it on the model's word. **Φ is the type.** A handoff between agents is a signature in it rather than a paragraph, and everything downstream is one of four projections.

![F2 — Φ and its four projections](diagrams/F2-phi-projections.svg)
*F2 — Cap and Effects project to authorization; Pre, Post, and Inv to obligations; Effects to a runtime check; Evidence to a witness.*

**Cap and Effects project to authorization.** "Refactor the parser, no network" becomes real Cedar:

```cedar
permit (
  principal == Agent::"refactor-bot",
  action == Action::"Write",
  resource in Dir::"parser"
);
forbid (
  principal == Agent::"refactor-bot",
  action == Action::"Network",
  resource
);
```

A request is allowed only if some permit matches and no forbid matches: any forbid overrides every permit, and an empty policy set denies everything. "No network" is a forbid, and no later permit can reopen it. Cedar is a projection of Φ, not its formalizer. It answers whether this principal may take this action on this resource in this context, and says nothing about whether the parser still parses.

**Pre, Post, and Inv project to obligations**, discharged by tests, static analysis, or proof depending on risk:

```text
public_api(before) == public_api(after)
tests(after)       == PASS
behavior(before)   ≈  behavior(after)
```

Here ≈ is observational equivalence on the specified interface: no client of the parser's public surface can tell before from after. Defined that narrowly, it can be tested, approximated statically, or proved. Left undefined, it is the hand-wave this essay exists to end.

**Effects project to a runtime check.** The harness watches the run and compares each actual side effect against the declared set. Checking that statically would demand an effect system over every tool, so Cordis reifies effects and coeffects as runtime objects instead: the guarantees a static system would give are established dynamically, and an undeclared access is an error rather than a surprise. Checked boundaries are static where possible and reified at runtime where not.

**Evidence projects to a witness:** tests run, traces captured, policy decisions logged, obligations discharged or refuted, and the human decision that accepted the residual risk.

> Authorization and verification are two projections of one typed object.

An obligation with nowhere to land is ceremony, and two developments give obligations ground. Theory-level autoformalization (Min, He, Li, Yi, Malik, Gupta, Si, and Bastani, arXiv 2607.13292, a position paper) moves the target from isolated statements to formal knowledge bases: definitions, lemmas, and invariants a new obligation can be stated against.

CSLib is the Mathlib for computer science, in two pillars: formalizing CS itself (models of computation, automata, operational semantics, program logics, complexity, concurrency, verified algorithms) and Boole, a Lean-embedded intermediate verification language that generates verification conditions for Grind, Lean-SMT, Hammer, or LLM provers. The CSLib authors name the bottleneck: "AI-based provers are bottlenecked by the abstractions available in the underlying proof assistant." Their governance rule is this essay's creed: AI tools are advisory only, and every committed proof goes through manual review.

Admission is a pipeline: candidate formalization, then type and proof check, then semantic review, then integration into the trusted library, then reuse by the next task. Each gate is a commitment the previous one could not make.

The projection target is where the boundary shows. Cedar's semantics are formalized in Lean in cedar-spec, the Rust implementation is differentially tested against that spec, and cedar-policy-symcc compiles policies to SMT to prove never-errors, always-allows, subsumption, and equivalence, with counterexamples from cvc5. Amazon Verified Permissions, the hosted service, is paid. The semantics connect independent systems, so they are open and verified all the way down. The service is a leaf, and nobody's trust depends on it.

## 3. Progressive commitment: the layer cake

Compilers solved this shape of problem decades ago. Source passes through parse tree, typed representation, IR, lowering, and codegen, and each stage makes some ambiguity impossible and some invariant checkable. The layer cake is that pipeline lifted above the code level, with Φ as the object being lowered. Goldilocks decides how much each layer must commit. Open-versus-closed decides who may inspect the commitment.

![F3 — The AI layer cake](diagrams/F3-layer-cake.svg)
*F3 — Each layer commits something the layer above left ambiguous. Left gutter: the open reference. Right gutter: must-open, can-close, or either.*

**Human intent** commits a goal. Either: it reaches the stack through whichever client a person types it into.

**Formal intent and policy** commits Φ. Authority becomes decidable, obligations become stated, and "what was the agent allowed to do" is a lookup, never a reconstruction. Must be open. A policy semantics that only one product understands is configuration, not policy.

**The agent harness** commits execution: which tool ran, under which capability, with what result. It is a runtime. In Cordis a component is a triple ⟨coeffect specification, provision, witnessed effect function⟩; loading runs the effect function and accumulates inverses, and unloading applies them LIFO, so removing a plugin removes what it did.

DeepSeek Harness, built on Cordis and shipped source-included as a developer preview, states its invariants. Everything is a plugin. Model-visible means logged: anything that reaches a model request is reconstructable from the log, and a runtime assertion enforces it.

Seams split into definition, provider, and consumer, so swapping the filesystem provider for a remote sandbox carries Bash, PTY, and LSP with it. Must be open: the protocol and the effect log. Can be closed: the best agent.

**Compiler and language** commits meaning: typed structure with an IR that analyzers can attach to. Mojo 1.0 (2026-08-11) is a stability milestone: 1.x changes should be primarily additive. A week later (2026-08-18) Modular opened the compiler and toolchain under Apache 2.0 with LLVM exceptions in modular/modular.

The Mojo docs describe a language designed from the start on MLIR, and I will make the argument Modular does not: an open, MLIR-native, general-purpose compiler is the pattern book for building DSLs on MLIR and for inserting verification hooks before lowering erases the structure they need. Modular is not accepting contributions yet, and says why: "in today's era of AI coding" it needs to be deliberate about how contributions are handled. Open source, closed gate, because of agents. The IR and its analyzers are must-open, the contribution queue is a leaf, and a compiler vendor has drawn exactly this essay's boundary.

**Executable** commits behavior, and it can sit on either side. **Evidence and witness** commits the record. Must be open: evidence legible only in one vendor's dashboard is a screenshot.

Below the cake sit cloud, chips, and energy: decisive for the cost floor, and below this series' boundary.

My research lineage is hybrid program analysis, so the evidence layer is the one I watch. Jitana and ReHAna were built for Android, where reflection and dynamic class loading hid the running code from static analysis while a trace showed nothing of the paths it skipped. Each side lies by omission; the discipline is making each side challenge the other. The agent loop reproduces that split exactly: a patch is a static artifact, tool calls are dynamic behavior, logs are traces, tests are sampled executions, and a proof is a scoped formal claim. Reconciling them is the evidence layer's whole job and the subject of Thread 2.

## 4. Calibration

A typed object is what makes calibration possible. You cannot tune the rigor of a prose handoff, but you can decide how much of Φ a task must discharge. On rigor, too little is prompt-only intent, ambient permissions, prose handoffs, and summary-as-evidence; too much is a proof for every edit, ceremony outrunning signal, and blocked iteration. On openness, too little is the closed vertical; too much is fragmentation, where source exists, nothing composes, dialects drift, and adoption happens by fork.

![F4 — The Goldilocks zone on two axes](diagrams/F4-goldilocks.svg)
*F4 — Rigor by openness. The zone is bounded on all four sides; evidence required grows with risk along the rigor axis.*

The zone on rigor is evidence proportional to risk. A docs edit earns a diff review and a test run. A parser refactor earns tests, static checks, and traces. An auth or payments boundary earns policy, a proof obligation, and an explicit human signature. Φ carries enough to place the task before a line changes: Effects and Inv say which band it is in, and Evidence says what the band demands.

> A typo earns a diff. An auth boundary earns a proof and a signature.

The evidence vocabulary has seven words: proved, refuted, tested, observed, judged, assumed, not checked. The labels cost nothing and block the most common failure in agent workflows: a proof over one property quietly presented as a proof over the system. Collapse them into one green check and the leak is back. The bands and the vocabulary are the contract between tools, which puts calibration itself on the open side of the boundary.

## 5. Which layers open, and why

Three forces open a layer. Common infrastructure: everyone needs to build on it. Strategic collaboration: sharing it beats competing over it. Network effects: it is worth more with every implementation that speaks it. LLVM is all three compounding, a permissive compiler substrate funded by rivals and valuable in proportion to the languages and targets on it.

Openness there is a property of the architecture: a connective layer's value is its externalities, and closing it destroys them, so I expect these layers to open whether or not anyone is virtuous.

**Weights can be closed.** NVIDIA's pledge (2026-07-24) argues for open weights on access, competition, control, adaptability, and security. Closed frontier models coexist beside them, and the stack stays trustworthy because the layers around them emit portable evidence.

**The harness must be open.** DeepSeek Harness on Cordis is the existence proof: a source-included runtime whose effects have inverses and whose logs reconstruct every model request.

**The compiler must be open; its gate can be closed.** Mojo's compiler is Apache 2.0 with LLVM exceptions. Its contribution queue is shut "in today's era of AI coding."

**The protocol must be open; the editor and the agents can be either.** Zed is roughly 97% Rust on its own GPU framework, gpui, under GPL-3.0-or-later. ACP is Apache-2.0 with no CLA, JSON-RPC over stdio with a typed schema, SDKs in five languages, and JetBrains as co-host. Zed charges nothing for external agents, and Claude Code and Codex stay closed products behind it.

**The proof tools must be open.** Amazon's grant to the Lean FRO (2026-07-26), the largest in the organization's history, went outside Amazon on purpose: "it's easier to trust a proof when you can evaluate the tools behind it yourself," so that customers, auditors, and regulators can inspect work done in community-governed tools. Authority was placed beyond the company's reach, which is where authority has to live.

## 6. The creed

**A model may propose. Only a verifier admits.** If the verifier refutes the claim, the counterexample becomes a regression fixture. If it cannot decide, the claim stays unadmitted. A model's output is advisory until a deterministic check, a proof, a policy decision, or a human promotes it, and the promotion is recorded in the witness with its evidence class attached.

![F5 — From intent to acceptance](diagrams/F5-central-graph.svg)
*F5 — Intent is formalized into policy and obligations, executed under a harness, checked by compiler and analyzers, and accepted on evidence.*

That rule is the Goldilocks boundary, applied. Commit enough at each layer that admission is decidable; open enough of each layer that admission can be inspected by someone who does not work for the vendor.

Compilers learned this decades ago. The stack above the code is learning it now, in public. Modular, Amazon, Zed, and the Cedar team have each drawn the line in the same place, and the series follows it from here.

> The proposer can be closed. The admitter must be open.

Next: Part 2, Open Models and Model Competition.

## References

**Compiler**
1. Modular, "Mojo is now open source" (2026-08-18): https://www.modular.com/blog/mojo-open-source
2. Modular, "Modular 26.5: Mojo 1.0 is here" (2026-08-11): https://www.modular.com/blog/modular-26-5-mojo-1-0-is-here
3. Mojo documentation and FAQ, MLIR design: https://docs.modular.com/mojo/faq

**Autoformalization and verification**
4. M. J. Min, M. He, Z. Li, Z. Yi, S. Malik, A. Gupta, X. Si, O. Bastani, "Theory-Level Autoformalization: From Isolated Statements to Unified Formal Knowledge Bases," arXiv:2607.13292: https://arxiv.org/abs/2607.13292
5. CSLib, "The Lean Computer Science Library," arXiv:2602.04846: https://arxiv.org/abs/2602.04846
6. Amazon Science, "Amazon is investing in the Lean Focused Research Organization" (2026-07-26): https://www.amazon.science/news/amazon-is-investing-in-the-lean-focused-research-organization

**Policy**
7. Cedar policy language, Rust implementation, and cedar-policy-symcc: https://github.com/cedar-policy/cedar
8. cedar-spec, Lean formalization and differential testing: https://github.com/cedar-policy/cedar-spec

**Harness**
9. DeepSeek Harness (developer preview, checked 2026-08-20): https://github.com/deepseek-ai/deepseek-harness and https://deepseek.com/harness/en/
10. Cordis, "A Programming Paradigm for Spatiotemporal Composability," theory-to-implementation table p.55: https://github.com/cordiverse/paper/blob/main/paper.pdf

**IDE and protocol**
11. Zed: https://github.com/zed-industries/zed
12. Agent Client Protocol: https://agentclientprotocol.com

**Open weights**
13. NVIDIA, "Open Weights and American AI Leadership" (2026-07-24): https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf

**Author lineage**
14. Jitana: https://github.com/ytsutano/jitana
15. ReHAna, MobiQuitous 2021: https://doi.org/10.1007/978-3-030-94822-1_19
16. DBLP, Shakthi Bachala: https://dblp.org/pid/200/1146.html

---WORDCOUNT---
2320 prose words (body paragraphs only; excludes title, dek, headings, pull-quotes, figure captions, the series table, code fences, the Next line, and references). Per section: §0 ≈241, §1 ≈296, §2 ≈562, §3 ≈553, §4 ≈223, §5 ≈311, §6 ≈134. Fences: 3. Pull-quotes: 4 (17, 10, 14, 10 words). Figures: 5.
