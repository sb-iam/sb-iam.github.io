<!-- Dates checked 2026-08-21: ICSE 2026 Doctoral Symposium 2026-04-14; IDE 2026 workshop 2026-04-18; The Verification Summit 2026-06-10; GLM-5.2 2026-06-16; "Open Weights and American AI Leadership" 2026-07-24 (PDF revised 2026-07-29, 235 signatories); Amazon / Lean FRO 2026-07-26; Kimi K3 full weights 2026-07-27; Qualcomm–Modular close 2026-07-29; Mojo 1.0 2026-08-11; DeepSeek Harness 2026-08-13 (179,486 stars on 2026-08-21); Mojo compiler open-sourced at ModCon 2026-08-18. -->

# The Goldilocks Zone of the Open AI Ecosystem

*Open and closed systems will coexist. The question is which layers must be open for software written by agents to be trusted.*

**AI coding agents exposed a missing layer.** Between the sentence a person types and the bytes an agent writes, nothing carried what the task permitted, what it had to preserve, or what counted as done. In 2026 the industry started filling that gap, one layer at a time, in public.

I take no side in open versus closed. Frontier weights are closed and will stay closed. The position paper Tan and colleagues brought to ICML 2026, *If open source is to win, it must go public*, supplies the fact my position rests on: "open source weights alone are inert; without inference, fine-tuning, localization, tooling, and interfaces, they remain unusable." Their question is which layers must be public. Mine is the narrower engineering question, which layers must be open for an agent's work to be checked by someone who does not work for the vendor, and the answer is a boundary through the middle of the stack.

This essay walks that boundary event by event, assembles the layer cake from what opened, and starts the first of three threads, each revisited quarterly.

| Thread | Parts |
|---|---|
| The Golden Era of the Open Ecosystem | 6: this essay · from leaky abstractions to type-safe abstractions · languages, SDKs, and the holy wars · open models and environments · open harnesses, compilers, and protocols · incentives and the open social contract |
| Hybrid Analysis | 3: static vs. dynamic analysis · verification vs. validation · static + dynamic, verification + validation |
| Future of Software Engineering | 3: IDEs, CLIs, and harnesses · language wars in the agent era · review, acceptance, and ownership |

## 1. 2026, layer by layer

The year had a shape. In April, at ICSE 2026 in Rio de Janeiro, the IDE workshop organized by JetBrains Research opened with a keynote on human-AI experience in the IDE and closed with round tables on what LLMs are doing to IDE usage. The IDE is where intent enters, and the room's question was what an IDE is now. In June, The Verification Summit, Pramaana Labs' launch edition in San Francisco, put about 150 people in a single track under one sentence: "from outputs that sound right to outputs we can prove right." Between those two meetings, the middle opened.

### Models and environments

In June the open-weight flagships closed in on the frontier, on the labs' own benchmarks: Z.ai's GLM-5.2, 753 billion parameters under MIT, on June 16; Moonshot's Kimi K3, 2.8 trillion parameters under its own Kimi K3 License, with full weights by July 27. Z.ai says GLM-5 is "closing the gap with frontier models"; Moonshot says K3 "still trails the most powerful proprietary models." Approaching frontier on the labs' own benchmarks is the honest sentence.

Prime Intellect's stack lets people who did not train a model train it further: prime-rl (Apache-2.0) runs asynchronous RL as a vLLM inference server, an orchestrator driving rollouts, and an FSDP2 trainer; verifiers (MIT) packages each task as an environment, a dataset plus a harness plus reward functions; the Environments Hub versions more than 2,500 of them. A reward is a deterministic check or an LLM judge. Prime Intellect does not use the words; that split is verification and validation, and one environment scores training and evaluation alike.

NVIDIA rates a DGX Spark (128 GB unified memory, $4,699) for inference to about 200B parameters and fine-tuning to 70B. GLM-4.7-Flash (30B-A3B) fits in BF16, GLM-4.5-Air at 4-bit, and LoRA fine-tuning there is documented. Neither GLM-5.2 nor Kimi K3 fits on one Spark or two, and prime-rl's full loop on a Spark is undocumented. The desk-side story is a 30–70B open model, fine-tuned locally, scored by an open environment.

### Weights

On July 24 an NVIDIA-led coalition published *Open Weights and American AI Leadership*, an open letter to U.S. policymakers. It is not a pledge; it commits its signatories to nothing. Led by NVIDIA, Microsoft, and Meta, it reached 235 signatories by July 29, most of them startups, infrastructure vendors, investors, and nonprofits. Its definition is the durable part: open-weight models are ones "anyone can download, inspect, modify, and run on their own infrastructure."

What the letter opened is the argument. Weights are a leaf of the cake, and a leaf can be closed: trust is decided in the layers that activate them, and those are the ones the ICML paper says stay private. Its own example is the coding-agent harness, where the developer works "inside the company's proprietary model harness (e.g. Claude Code) that captures the user's exact process of software development."

> Trust never rested on the weights. It rests on the layers that activate them.

### Proofs

Two days later Amazon's Automated Reasoning organization announced, in a post by Byron Cook and Shawn Bice, "substantial, long-term financial support" for the Lean Focused Research Organization, the single largest donation in the FRO's history, amount undisclosed. The reason given is the sentence this essay is built on: "it's easier to trust a proof when you can evaluate the tools behind it yourself."

CSLib is a separate effort. Announced in August 2025, it aims to be for computer science what Mathlib is for mathematics, plus Boole, an imperative language whose verification conditions land in Lean. Its steering committee spans Amazon, Google DeepMind, Stanford, UT Austin, the University of Southern Denmark, and the Lean FRO, and its funding is its own, a Renaissance Philanthropy program. Its authors name the wall an agentic ecosystem hits first, "AI-based provers are bottlenecked by the abstractions available in the underlying proof assistant," and keep AI advisory with manual review on every commit. My judgment: a proof checker funded by the largest cloud and governed outside it, beside a library built so agents can state obligations about real programs, is the biggest step AI-aided verification has taken.

### Harness

On August 13 DeepSeek published DeepSeek Harness, `dsh`, MIT-licensed and in developer preview; by August 21 it had 179,486 stars. It is built on Cordis, a 2022 plugin framework it credits as its foundation. Two invariants define it. Everything is a plugin: the model adapter, the tool registry, the session log, and the agent loop itself are replaceable from configuration, with no privileged core. Model-visible means logged: anything that reaches a model request must be reconstructable from the append-only session log, and a runtime assertion enforces it.

DeepSeek Harness does not credit pi, Mario Zechner's coding agent; pi's footprint is one npm package, pi-ai, a model adapter used by one plugin. The two are opposite answers to the same problem: pi keeps a four-tool core and refuses sub-agents, plan mode, and MCP; dsh ships sub-agents, planning, skills, sandboxing, and approval policy in its Standard preset, and only its Minimal preset, a two-tool loop for benchmarking, is pi-shaped. The layer the ICML paper says stays private now has an open, replayable implementation with its invariants written down.

### Compiler

The compiler opened in two steps. On August 11 Mojo reached 1.0, a stability milestone: semver on the core language, 1.x changes "primarily additive," source-level only, the ABI not yet stable. On August 18 at ModCon in San Francisco, Modular, a Qualcomm company since July 29, open-sourced the entire compiler and toolchain under Apache 2.0 with LLVM exceptions; MAX stays source-available.

Modular once called Mojo "the first major language designed expressly for MLIR"; the current vision doc says it is "built purely on top of MLIR Core," syntactic sugar for MLIR, aiming at "a unified language for kernel development"; MAX's CPU and GPU kernels are all written in it. The argument Modular does not make is mine: an open, general-purpose compiler that is MLIR all the way down is the pattern book for building DSLs on MLIR and for inserting verification hooks before lowering erases the structure they need. Its first governance decision: no compiler contributions yet, "particularly in today's era of AI coding," with a target of year end. The IR is must-open, the gate is governance, and a compiler vendor drew this essay's boundary. The Mojo 1.0 post covers the language itself.

> Open source, closed gate, and the reason given was agents.

## 2. The Open AI Layer Cake

Stack those events and the cake assembles itself. Each layer commits something the layer above left ambiguous, the way a compiler pipeline does; this is that pipeline lifted above the code.

![F3 — The Open AI Layer Cake](diagrams/F3-layer-cake.svg)
*F3 — One row per layer: what it commits, its 2026 open reference, and whether it must be open, can be closed, or either.*

**Human intent** commits the goal and who accepts the risk. It arrives through an IDE, a CLI, or a chat window, open or closed. Either.

**Formal intent and policy** commits the task's boundary: what it may touch, what it must preserve, what counts as done, stated so a machine can check it. Cedar, autoformalization, CSLib. Must be open; a policy semantics only one product understands is configuration. Part 2 gives this layer its type.

**The agent harness** commits execution: which tool ran, under which capability, with what result, logged so the run replays. DeepSeek Harness, Cordis, and the Agent Client Protocol, Apache-2.0, no CLA, JetBrains co-developing. The interface and the log must be open; the best agent can be closed.

**Compiler and language** commits meaning: typed structure and an IR analyzers attach to before lowering. Mojo, MLIR, LLVM. The IR is open; the implementation and the gate go either way.

**The executable** commits behavior and produces traces. Either.

**Evidence** commits the record: proved, refuted, tested, observed, judged, assumed, not checked. Must be open, in portable formats; evidence legible only in one vendor's dashboard is a screenshot.

Cloud, chips, and energy are below the cake. They decide the cost floor and fall below this series' line.

The rule the events share: layers that connect independent systems must be open, because connection is their value and closing them destroys it; leaves can be closed as long as the layers around them emit portable evidence. The "activation gap" Tan and colleagues describe, between available weights and usable systems, is the same observation from the other side. The gap is the connective layers.

Goldilocks runs on both axes. On rigor, the zone sits between prompt-only intent with ambient permissions and a proof for every edit: evidence scales with risk, so a docs edit earns a diff and a test run, a parser refactor earns tests and static checks, and an auth boundary earns a proof obligation and a human signature. On openness, it sits between one vendor owning model, harness, policy, compiler, and evidence, and a scatter of source that never composes.

![F4 — The Goldilocks zone on two axes](diagrams/F4-goldilocks.svg)
*F4 — Rigor by openness, bounded on all four sides.*

## 3. AI-assisted software development, made verifiable

The loop every agent runs, SWE-agent and OpenHands included, is the old one: intent, plan, edit, build, test, review, merge, operate. What changed is speed. The literature calls it the agentic SDLC and records SWE-bench Verified rising from 1.96% to 78.4% between October 2023 and April 2026. A systematic review of 92 studies found where the gains landed: "output verifiability is the primary enabler of agentic adoption." Agents took the loop where something could check them.

![F6 — The agentic SDLC inside the verifiable ecosystem](diagrams/F6-agentic-sdlc.svg)
*F6 — The loop in the middle; formal intent at its entry, the harness around execution, the compiler and analyzers at build, evidence at review; each layer of the cake wrapped around one phase.*

Wrap the cake around the loop and agents can build large systems humans can trust, by principles two communities already live by.

The functional-programming community built the verified canon. CompCert is written in Coq's functional language and extracted to OCaml; Csmith spent six CPU-years finding wrong-code bugs in every C compiler it tested except CompCert's verified middle-end, and its authors still concluded that "verification does not obviate testing, but rather complements it." seL4 is 8,700 lines of C derived from a Haskell prototype and proved in 200,000 lines of Isabelle. Yaron Minsky's maxim, make illegal states unrepresentable, is a type-design rule before it is a proof technique; QuickCheck made properties testable; Lean 4 is itself a compiled functional language.

The hardware community built the sign-off culture. RISC-V specifies its architecture twice: the ISA manual is the prose specification and the Sail model is the official formal one, chosen after a 2019 public review in which all five candidates were written in functional metalanguages. The Architectural Certification Tests compute expected results from Sail and gate the "RISC-V Compatible" mark, and their README insists they are not verification tests. Verification consumes 60–70% of chip-project engineering effort; simulation still dominates, formal grows every year, and CIRCT is carrying MLIR into that world, experimentally.

Three principles fall out: formal specs are the contract, illegal states are unrepresentable, and verification is sign-off rather than afterthought. The agentic SDLC is what this ecosystem makes trustworthy. Agents doing research is a different loop and out of scope.

> Agents made the loop fast. The layers around it make it trustworthy.

## 4. Which layers open, and why

Three forces open a layer. Common infrastructure: everyone has to build on it. Strategic collaboration: sharing it beats competing over it. Network effects: it is worth more with every implementation that speaks it. LLVM is all three compounding: a permissive substrate funded by rivals, worth more with every language and target on it.

Openness at a connective layer is architectural, so these layers open whether or not anyone is virtuous, and 2026 is the evidence: a compiler vendor opened the IR and kept the gate, a hyperscaler funded a proof checker it refuses to own, a model lab opened the runtime around its models, and a chip vendor's coalition lobbied for openness at the one layer that can stay closed.

The rule is the reader's test for every announcement. Ask whether the layer connects or is a leaf. If it connects, its interface and its record must be open, and its governance may still be closed. If it is a leaf, it may be closed, provided the layers around it emit evidence anyone can read. Zed passes, a GPL-3.0 editor with an Apache-2.0 protocol and closed agents behind it; a harness whose session log only its vendor can parse does not.

## 5. The ecosystem is its tooling

**An ecosystem is as good as its developer tooling.** Weights arrive by download; trust arrives through the compiler that checks, the harness that logs, the prover that admits, and the evidence format that survives a vendor change. Those are the layers 2026 opened, and this thread follows them.

Part 2, *From Leaky Abstractions to Type-Safe Abstractions in the Era of the Open Ecosystem*, gives a task handed to an agent a type. After it, the thread goes layer by layer, starting with the holy wars of programming languages and their SDKs and where each language sits in the cake.

A note on provenance. This essay is the culmination of conversations with hundreds of researchers at three events this year: ICSE 2026, from the Doctoral Symposium to IDE 2026; The Verification Summit by Pramaana Labs; and ModCon 2026, where the Mojo compiler was open-sourced on stage.

A note on scope. The ethics of open versus closed source, everything below the ABI including hardware and robotics, and anything outside software engineering are out of scope for this series.

## References

### Stance

1. J. Tan, N. Vincent, K. Elkins, M. Sahlgren, J. Low, D. Pham, S. Pyysalo, J. Jitsev, "Position: If open source is to win, it must go public," ICML 2026 (Spotlight), arXiv:2507.09296v3: https://arxiv.org/abs/2507.09296

### Conferences

2. ICSE 2026, Rio de Janeiro, April 12–18, 2026: https://conf.researchr.org/home/icse-2026
3. ICSE 2026 Doctoral Symposium, April 14, 2026: https://conf.researchr.org/track/icse-2026/icse-2026-doctoral-symposium
4. IDE 2026, 3rd International Workshop on Integrated Development Environments, April 18, 2026: https://ide-workshop.github.io/
5. The Verification Summit, Launch Edition, Pramaana Labs, June 10, 2026: https://verificationsummit.ai/
6. ModCon 2026: Compute Unlocked, August 18, 2026: https://www.modular.com/modcon

### Models and environments

7. Prime Intellect, prime-rl (Apache-2.0): https://github.com/PrimeIntellect-ai/prime-rl
8. Prime Intellect / W. Brown, verifiers (MIT): https://github.com/PrimeIntellect-ai/verifiers
9. Prime Intellect, "Environments Hub" (2025-08-27): https://www.primeintellect.ai/blog/environments
10. Z.ai, GLM-5.2 model card (MIT, 2026-06-16): https://huggingface.co/zai-org/GLM-5.2
11. Z.ai, GLM-5 model card ("closing the gap with frontier models"): https://huggingface.co/zai-org/GLM-5
12. Z.ai, GLM-4.7-Flash model card (30B-A3B, MIT): https://huggingface.co/zai-org/GLM-4.7-Flash
13. Moonshot AI, "Kimi K3: Open Frontier Intelligence": https://www.kimi.com/blog/kimi-k3
14. Moonshot AI, Kimi K3 model card and license: https://huggingface.co/moonshotai/Kimi-K3
15. NVIDIA, DGX Spark product page: https://www.nvidia.com/en-us/products/workstations/dgx-spark/
16. NVIDIA, DGX Spark "Fine-tune with PyTorch" playbook: https://build.nvidia.com/spark/pytorch-fine-tune
17. NVIDIA Developer Forums, DGX Spark price change (2026-02-23): https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713

### Weights

18. "Open Weights and American AI Leadership," open letter hosted by NVIDIA (2026-07-24, PDF revised 2026-07-29): https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf
19. Microsoft, live signatory page: https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/

### Proofs

20. B. Cook, S. Bice, "Amazon is investing in the Lean Focused Research Organization," Amazon Science (2026-07-26): https://www.amazon.science/news/amazon-is-investing-in-the-lean-focused-research-organization
21. Lean FRO, "About the Lean FRO": https://lean-lang.org/fro/about/
22. C. Barrett, S. Chaudhuri, F. Montesi, J. Grundy, P. Kohli, L. de Moura, A. Rademaker, S. Yingchareonthawornchai, "CSLib: The Lean Computer Science Library," arXiv:2602.04846: https://arxiv.org/abs/2602.04846
23. CSLib Initiative, "About": https://www.cslib.io/initiative/about

### Harness

24. DeepSeek AI, DeepSeek Harness (MIT, developer preview, checked 2026-08-21): https://github.com/deepseek-ai/deepseek-harness
25. DeepSeek AI, "DeepSeek Harness Architecture" (invariants): https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md
26. Y. Shi, W. Zhang, T. Cui, "A Programming Paradigm for Spatiotemporal Composability" (Cordis): https://github.com/cordiverse/paper
27. M. Zechner et al., Pi agent harness (MIT): https://github.com/earendil-works/pi
28. Agent Client Protocol: https://agentclientprotocol.com
29. Zed: https://github.com/zed-industries/zed

### Compiler

30. Modular, "ModCon 2026: Open source, open cloud, open silicon" (2026-08-18): https://www.modular.com/blog/modcon-announcements
31. Modular, "Mojo is now open source!" (2026-08-18): https://www.modular.com/blog/mojo-open-source
32. Modular, "Modular 26.5: Mojo 1.0 is here!" (2026-08-11): https://www.modular.com/blog/modular-26-5-mojo-1-0-is-here
33. Mojo documentation, "Mojo vision" (MLIR Core; unified language for kernel development): https://mojolang.org/docs/vision/
34. Modular, "Why Mojo" (archived 2024-06-05; "first major language designed expressly for MLIR"): https://web.archive.org/web/20240605012702/https://docs.modular.com/mojo/why-mojo
35. Qualcomm / Modular, "Qualcomm Completes Acquisition of Modular" (2026-07-29): https://www.modular.com/blog/qualcomm-completes-acquisition-of-modular

### Verified-software principles

36. riscv/sail-riscv, formal specification of the RISC-V ISA: https://github.com/riscv/sail-riscv
37. RISC-V ISA Formal Spec Public Review (2019): https://github.com/riscvarchive/ISA_Formal_Spec_Public_Review
38. riscv/riscv-arch-test, Architectural Certification Tests: https://github.com/riscv/riscv-arch-test
39. H. Foster, 2024 Siemens EDA / Wilson Research Group IC/ASIC Functional Verification Trend Report: https://verificationacademy.com/topics/planning-measurement-and-analysis/wrg-industry-data-and-trends/2024-siemens-eda-and-wilson-research-group-ic-asic-functional-verification-trend-report/
40. CIRCT, Circuit IR Compilers and Tools: https://circt.llvm.org/
41. X. Leroy, "Formal verification of a realistic compiler," CACM 2009: https://xavierleroy.org/publi/compcert-CACM.pdf
42. X. Yang, Y. Chen, E. Eide, J. Regehr, "Finding and Understanding Bugs in C Compilers," PLDI 2011: https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf
43. G. Klein et al., "seL4: Formal Verification of an OS Kernel," SOSP 2009: https://dl.acm.org/doi/10.1145/1629575.1629596
44. Y. Minsky, "Effective ML Revisited" (2011): https://blog.janestreet.com/effective-ml-revisited/
45. K. Claessen, J. Hughes, "QuickCheck," ICFP 2000: https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf
46. Lean, "Lean programming language and theorem prover": https://lean-lang.org/

### Agentic SDLC

47. H. Bhati, "Agentic AI in the Software Development Lifecycle," arXiv:2604.26275: https://arxiv.org/abs/2604.26275
48. S. A. Apostolou, J. Bosch, H. Holmstrom Olsson, "Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle," arXiv:2605.15245: https://arxiv.org/abs/2605.15245
49. J. Yang et al., "SWE-agent," NeurIPS 2024: https://arxiv.org/abs/2405.15793
50. X. Wang et al., "OpenHands," ICLR 2025: https://arxiv.org/abs/2407.16741
