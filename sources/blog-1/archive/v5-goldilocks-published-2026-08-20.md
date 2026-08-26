<!-- Dates checked 2026-08-20: ChatGPT 2022-11-30; ChatGPT Pro 2024-12-05; open-weights coalition letter hosted by NVIDIA 2026-07-24; Amazon/Lean FRO 2026-07-26; Mojo 1.0 2026-08-11; Mojo OSS 2026-08-18; DeepSeek Harness developer preview checked 2026-08-20. -->

# The Goldilocks Zone of the Open AI Ecosystem

*Open and closed systems will coexist. The question is which layers must be open for software written by agents to be trusted.*

**AI coding agents have exposed a missing layer between human intent and executable side effects.** Nothing in today's stack carries what a task permits, what it must preserve, and what counts as done from the typed sentence to the written bytes.

Filling that layer is a calibration problem on two axes, and the right answer on both is a Goldilocks zone. On rigor, it sits between prompt-only intent with ambient permissions and a proof for every edit. On openness, it sits between one vendor owning model, harness, policy, compiler, and evidence, and a scatter of source that never composes.

Open and closed will coexist. The frontier models are closed and will remain so. **The connective layers must be open:** evidence formats, policy semantics, agent protocols (ACP, MCP), compiler IR and the analyzers that attach to it. They exist to connect independent systems; closing them destroys the reason they exist, and they are where inspection, replacement, and replay happen. **The leaves can be closed:** weights, hosted inference, enterprise control planes, proprietary data, the best client, as long as the layers around them emit portable evidence.

That boundary is the zone, and every serious vendor is choosing where it sits. Modular opened its compiler and closed compiler contributions. Amazon funds Lean outside Amazon. Zed opened its agent protocol while most agents stay closed. Cedar's semantics are open while the hosted service is paid. This essay maps the boundary and opens the first of three threads, each revisited quarterly.

| Thread | Parts |
|---|---|
| The Golden Era of the Open Ecosystem | 6: this essay · open models and model competition · open agent harnesses · open compilers and AI-native languages · open protocols and portable evidence · incentives and the open social contract |
| Hybrid Analysis | 3: static vs. dynamic analysis · verification vs. validation · static + dynamic, verification + validation |
| Future of Software Engineering | 3: IDEs, CLIs, and harnesses · language wars in the agent era · review, acceptance, and ownership |

## 1. Where the abstraction leaks

My working position is one window. Zed is the editor, the CLI is the execution substrate, and Codex, Claude Code, and Cursor enter through the shell or the Agent Client Protocol, ACP. The agents are interchangeable by design. I keep the workflow, the constraints, and the evidence; I swap the agent. When the workflow carries the constraints, a narrow task can go to a local model and an obligation to a prover, and nothing around the swap changes.

That position is a test, and the current abstraction fails it.

Intent is informal: "refactor the parser." Permissions are ambient: whatever the shell user can touch, the agent can touch. Handoffs are prose: one agent writes Markdown and another reads it. Effects are invisible: a dependency added, a CI file edited, a network call made. Completion is social: "done" is a sentence, and the evidence for it is a summary written by the party under review.

A human engineer reads "refactor the parser" and knows what it excludes: no public API change, no new dependency, no CI edit, no network. The boundary is real and was never written down.

> Humans infer the boundary from culture and consequence. Agents have to be told, and nothing tells them.

That is the law of leaky abstractions in the agent loop, and there is a datum for how leaky. The Cordis paper, whose runtime returns in §3, surveyed the top 100 VS Code extensions: 87 need a host restart to be removed, and cross-extension exports are typed `any` by default. Nothing was committed at load time, so nothing can be unwound at unload time. An agent harness is the same shape of platform, with a model at the keyboard.

![F1 — Leaky pipeline vs. typed pipeline](diagrams/F1-leaky-vs-typed.svg)
*F1 — One task through an untyped pipeline (left) and a checked one (right); every leak on the left has its check on the right.*

Every leak sits in connective tissue: between human and agent, agent and agent, agent and filesystem. That tissue has to be open for anyone to check it.

## 2. The type

Every abstraction leaks. Types never stopped leaks; they made them checked errors at explicit boundaries. So ask what type a task handed to an agent has. Mine is a six-tuple.

```text
Φ = ⟨Pre, Post, Inv, Cap, Effects, Evidence⟩

Pre       what holds before the task
Post      what must hold after it
Inv       what must never break along the way
Cap       the authority granted
Effects   side effects allowed and forbidden
Evidence  what must be produced for acceptance
```

**Φ is the type.** A model can draft it from a sentence; nothing admits it on the model's word. A handoff between agents is a signature in it rather than a paragraph, and everything downstream is one of four projections.

![F2 — Φ and its four projections](diagrams/F2-phi-projections.svg)
*F2 — Φ at the centre; everything downstream consumes one of its four projections.*

**Cap and Effects project to authorization.** "Refactor the parser, no network" becomes Cedar:

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

A request is allowed only if some permit matches and no forbid matches; an empty policy set denies everything. "No network" is a forbid, and no permit can reopen it. Cedar is a projection of Φ, not its formalizer. It answers whether this principal may take this action on this resource in this context, and says nothing about whether the parser still parses.

**Pre, Post, and Inv project to obligations**, discharged by tests, static analysis, or proof depending on risk:

```text
public_api(before) == public_api(after)
tests(after)       == PASS
behavior(before)   ≈  behavior(after)
```

Here ≈ is observational equivalence on the specified interface: no client of the parser's public surface can tell before from after. Defined that narrowly, it can be tested, approximated statically, or proved. Left undefined, it is the hand-wave this essay exists to end.

**Effects project to a runtime check.** The harness watches the run and checks each side effect against the declared set. No static effect system can see a tool loaded after deployment, so Cordis reifies effects and coeffects as runtime objects instead, and an undeclared access is an error rather than a surprise. Checked boundaries are static where possible and reified at runtime where not.

**Evidence projects to a witness:** tests run, traces captured, policy decisions logged, obligations discharged or refuted, and the human decision that accepted the residual risk.

> Authorization and verification are two projections of one typed object.

An obligation with nowhere to land is ceremony, and two developments give obligations ground. Theory-level autoformalization, a position paper by Min, Bastani, and colleagues, moves the target from isolated statements to formal knowledge bases: definitions, lemmas, and invariants a new obligation can be stated against.

CSLib aims to be the Mathlib for computer science, in two pillars: formalizing CS itself (models of computation, automata, operational semantics, program logics, complexity, concurrency, verified algorithms) and Boole, a Lean-embedded intermediate verification language that generates verification conditions for Grind, Lean-SMT, Hammer, or LLM provers. Its authors name the bottleneck: "AI-based provers are bottlenecked by the abstractions available in the underlying proof assistant." Their governance rule is this essay's creed: AI tools are advisory only, and every committed proof goes through manual review.

Admission is a pipeline: candidate formalization, then proof check, which is verification (does the artifact satisfy Φ), then semantic review, which is validation (was Φ what was meant), then integration into the trusted library for the next task to reuse. A proof that passes against the wrong Φ is autoformalization's easiest failure, and Thread 2's second essay.

Cedar itself shows where the open-closed boundary falls. Its semantics are formalized in Lean in cedar-spec, the Rust implementation is differentially tested against that spec, and cedar-policy-symcc compiles policies to SMT to prove never-errors, always-allows, subsumption, and equivalence, with cvc5 counterexamples. Amazon Verified Permissions, the hosted service, is paid. The semantics are connective, so they are open and verified all the way down; the service is a leaf.

## 3. Progressive commitment: the layer cake

Compilers solved this shape of problem decades ago: parse tree, typed representation, IR, lowering, codegen, and each stage makes some ambiguity impossible and some invariant checkable. The layer cake is that pipeline lifted above the code, with Φ as the object being lowered. Goldilocks decides how much each layer must commit; open-versus-closed decides who may inspect it.

![F3 — The AI layer cake](diagrams/F3-layer-cake.svg)
*F3 — One row per layer: what it commits, its open reference, and whether it must be open, can be closed, or either.*

**Human intent** commits a goal and arrives through whichever client a person types into, open or closed.

**Formal intent and policy** commits Φ. Authority becomes decidable, obligations become stated, and "what was the agent allowed to do" is a lookup. It must be open: a policy semantics that only one product understands is configuration, not policy.

**The agent harness** commits execution: which tool ran, under which capability, with what result. It is a runtime. In Cordis a component is a triple ⟨coeffect specification, provision, witnessed effect function⟩; loading runs the effect function and accumulates inverses, and unloading applies them LIFO, so removing a plugin removes what it did. Without inverses you get the failures agent runs are full of: a tool present when the model read its schema and gone at call time, a permission granted for one payload and reused for another.

DeepSeek Harness, MIT-licensed on Cordis and in developer preview, states its invariants. Everything is a plugin. Model-visible means logged: anything that reaches a model request is reconstructable from the log, and a runtime assertion enforces it.

Each seam has a definition, a provider, and a consumer, so pointing the filesystem and subprocess providers at a remote sandbox carries Bash, PTY, and LSP with them. The protocol and the effect log must be open; the best agent can be closed.

**Compiler and language** commits meaning: typed structure with an IR that analyzers can attach to. Mojo 1.0 (2026-08-11) is a stability milestone, with 1.x changes primarily additive, and a week later (2026-08-18) Modular opened the compiler and toolchain under Apache 2.0 with LLVM exceptions in modular/modular.

Mojo's vision doc calls the language syntactic sugar for MLIR, built purely on MLIR Core, and I will make the argument Modular does not: an open, MLIR-native, general-purpose compiler is the pattern book for DSLs on MLIR and for verification hooks inserted before lowering erases the structure they need. Modular is not taking compiler contributions yet, and says why: "in today's era of AI coding" it needs to be deliberate about how contributions are handled. Open source, closed gate, because of agents: the IR and its analyzers are must-open, the gate is governance rather than interface, and a compiler vendor has drawn this essay's boundary.

**Executable** commits behavior, and it can sit on either side. **Evidence and witness** commits the record. It must be open: evidence legible only in one vendor's dashboard is a screenshot.

Below the cake sit cloud, chips, and energy, decisive for the cost floor and outside this series.

My research lineage is hybrid program analysis, so I watch the evidence layer. Jitana and ReHAna were built for Android, where reflection and dynamic class loading hid the running code from static analysis while a trace showed nothing of the paths it skipped. Each side lies by omission; the discipline is making each side challenge the other. The agent loop reproduces that split: a patch is a static artifact, tool calls are dynamic behavior, logs are traces, tests are sampled executions, and a proof is a scoped formal claim. Reconciling them is the evidence layer's whole job and the subject of Thread 2.

## 4. Calibration

A typed object is what makes calibration possible. You cannot tune the rigor of a prose handoff, but you can decide how much of Φ a task must discharge. The failure corners are symmetric. On rigor, too little is ambient permissions and summary-as-evidence; too much is a proof for every edit and ceremony outrunning signal. On openness, too little is the closed vertical; too much is fragmentation: source exists, nothing composes, dialects drift, adoption happens by fork.

![F4 — The Goldilocks zone on two axes](diagrams/F4-goldilocks.svg)
*F4 — Rigor by openness, with the zone bounded on all four sides.*

The zone on rigor is evidence proportional to risk. A docs edit earns a diff review and a test run. A parser refactor earns tests, static checks, and traces. An auth or payments boundary earns policy, a proof obligation, and an explicit human signature. Φ carries enough to place the task in advance: Effects and Inv say which band it is in, and Evidence says what the band demands.

> Rigor belongs to the task, not the agent, and Φ fixes it before a line changes.

The evidence vocabulary has seven labels: proved, refuted, tested, observed, judged, assumed, not checked. The labels cost nothing and block the most common failure in agent workflows: a proof over one property quietly presented as a proof over the system. Collapse them into one green check and the leak is back. The bands and the vocabulary are the contract between tools, which puts calibration itself on the open side of the boundary.

## 5. Which layers open, and why

Three forces open a layer. Common infrastructure: everyone needs to build on it. Strategic collaboration: sharing it beats competing over it. Network effects: it is worth more with every implementation that speaks it. LLVM is all three compounding, a permissive compiler substrate funded by rivals and valuable in proportion to the languages and targets on it.

Openness at a connective layer is architectural: its value is its externalities, so I expect these layers to open whether or not anyone is virtuous.

**Weights can be closed.** The open-weights letter NVIDIA hosted (2026-07-24), with over two hundred co-signers, argues on access, competition, control, adaptability, and security. Closed frontier models will coexist with open ones regardless, and trust never hinged on the weights.

**The harness must be open.** DeepSeek Harness on Cordis is the existence proof.

**The compiler must be open; its gate can be closed.** Mojo's compiler is Apache 2.0 with LLVM exceptions; its contribution queue is shut, and no analyzer needs that queue.

**The protocol must be open; the editor and the agents can be either.** Zed is roughly 97% Rust on its own GPU framework, gpui, under GPL-3.0-or-later. ACP is Apache-2.0 with no CLA, JSON-RPC over stdio with a typed schema, SDKs in five languages, and JetBrains co-developing. Zed charges nothing for external agents, and Claude Code and Cursor stay closed products behind it.

**The proof tools must be open.** Amazon's donation to the Lean FRO (2026-07-26), the FRO's largest ever, went outside Amazon on purpose: "it's easier to trust a proof when you can evaluate the tools behind it yourself," so that customers, auditors, and regulators can inspect work done in community-governed tools. The compiler may keep its gate because its output is checked downstream, by tests and by analyzers on an open IR; the proof checker is the last check, so its governance has to sit outside any one vendor.

## 6. The creed

**A model may propose. Only a verifier admits.** The reason is structural: the approximate representation that makes a model a strong proposer disqualifies it as an admitter.

If the verifier refutes the claim, the counterexample becomes a regression fixture. If it cannot decide, the claim stays unadmitted. A model's output is advisory until a deterministic check, a proof, a policy decision, or a human promotes it, and the promotion is recorded in the witness with its evidence class attached.

![F5 — From intent to acceptance](diagrams/F5-central-graph.svg)
*F5 — Intent is formalized into policy and obligations, executed under a harness, checked by compiler and analyzers, and accepted on evidence.*

That rule is the Goldilocks boundary, applied. Commit enough at each layer that admission is decidable; open enough of each layer that admission can be inspected by someone who does not work for the vendor.

Compilers learned this decades ago; the stack above the code is learning it now, in public, and the series follows it from here.

> The proposer can be closed. The admitter must be open.

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
