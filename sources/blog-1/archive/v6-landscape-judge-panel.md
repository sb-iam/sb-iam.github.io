<!-- Dates checked 2026-08-21: "Open Weights and American AI Leadership" coalition letter hosted by NVIDIA 2026-07-24 (PDF revised 2026-07-29, 235 signatories); Amazon / Lean FRO 2026-07-26; Qualcomm closes Modular acquisition 2026-07-29; Mojo 1.0 2026-08-11; DeepSeek Harness created 2026-08-13 (179,486 stars on 2026-08-21); Mojo compiler open-sourced at ModCon 2026-08-18; GLM-5.2 2026-06-16; Kimi K3 full weights 2026-07-27; ICSE 2026 Apr 12–18 (Doctoral Symposium Apr 14, IDE 2026 Apr 18); The Verification Summit 2026-06-10. -->

# The Goldilocks Zone of the Open AI Ecosystem

*Open and closed systems will coexist. The question is which layers must be open for software written by agents to be trusted.*

**AI coding agents have exposed a missing layer between human intent and executable side effects.** A person types a sentence, an agent edits a repository, and nothing between the two carries what the task permitted, what it had to preserve, and what counted as done. The model was the product; everything around it was scaffolding.

The scaffolding is becoming the architecture, in public, one layer at a time. Within four weeks this summer an industry coalition published an open letter on open weights; Amazon made the largest gift in the Lean FRO's history, outside Amazon on purpose; DeepSeek shipped an MIT-licensed agent harness; Modular open-sourced the Mojo compiler.

My stance is neutral on open versus closed and exact about layers. Tan and colleagues argued at ICML 2026, in *If open source is to win, it must go public*, that "open source weights alone are inert" without the layers that activate them, what the paper calls the activation gap, and conceded that public AI "is not about replacing private labs." Their question is which layers must be public; mine is which must be open for an agent's work to be checked by someone who does not work for the vendor.

This essay maps those layers and opens the first of three threads, each revisited quarterly.

| Thread | Parts |
|---|---|
| The Golden Era of the Open Ecosystem | 6: this essay · from leaky abstractions to type-safe abstractions · languages, SDKs, and the holy wars · open models and environments · open harnesses, compilers, and protocols · incentives and the open social contract |
| Hybrid Analysis | 3: static vs. dynamic analysis · verification vs. validation · static + dynamic, verification + validation |
| Future of Software Engineering | 3: IDEs, CLIs, and harnesses · language wars in the agent era · review, acceptance, and ownership |

## 1. The Open AI Layer Cake

![F3 — The Open AI Layer Cake](diagrams/F3-layer-cake.svg)
*F3 — One row per layer: what it commits, its open reference in 2026, and whether it must be open, can be closed, or either.*

**The cake is the activation gap, drawn for one domain.** Six layers sit above a line, read top-down as progressive commitment: each commits what the layer above left informal, in a form the layer below can check, and each commitment is either open to inspection or sealed inside one vendor.

**Human intent** commits a goal and a person who accepts the risk. It arrives through whichever client that person types into, open or closed.

**Formal intent and policy** commits the task boundary: what the agent may touch, what it must preserve, what counts as done. Cedar is the open reference for authority; Lean and CSLib are where obligations land. This layer must be open: a policy semantics only one product understands is configuration, and a proof only one vendor can check is a claim. The type this layer commits is the next essay's subject.

**The agent harness** commits execution: which tool ran, under which capability, with what result, and whether the run can be replayed. Its interface must be open, meaning the protocol the editor speaks to the agent (ACP) and the log of what the model saw; the implementation can be anyone's. DeepSeek Harness on Cordis opened this layer in August.

**Compiler and language** commits meaning: typed structure, an IR that analyzers can attach to, and hooks for checks before lowering erases what they need. The IR and its analyzers must be open; the compiler that produces them can be either. Modular opened Mojo's at ModCon.

**The executable system** commits behavior: what runs, where, and the traces it throws off. It sits on either side of the line.

**Evidence and witness** commits the record: what was proved, refuted, tested, observed, judged, assumed, or never checked, in a format a second tool can read. It must be portable. Evidence legible only in one vendor's dashboard is a screenshot.

The weights are not a row of the cake. They are what the cake activates, and they can sit on either side: an open flagship lowers the cost floor and says nothing about whether the agent's software can be trusted. Below the cake sit cloud, chips, and energy, outside this series.

> The weights are the finished artifact. Everything that makes them trustworthy for software is the cake.

Goldilocks is the calibration on two axes. On rigor, the zone sits between prompt-only intent with ambient permissions and a proof for every edit, with evidence scaling to risk. On openness, it sits between one vendor owning every layer and a scatter of source that never composes, with connective layers open and leaves either way.

![F4 — The Goldilocks zone on two axes](diagrams/F4-goldilocks.svg)
*F4 — Rigor by openness, with the zone bounded on all four sides.*

## 2. AI-assisted software development, made verifiable

![F6 — The agentic SDLC inside a verifiable ecosystem](diagrams/F6-agentic-sdlc.svg)
*F6 — The loop (intent → plan → edit → build → test → review → merge → operate) with the cake wrapped around it: the spec before the first edit, the harness around execution, analyzers at build, evidence at merge.*

The loop has not changed, and everything in it moves faster: intent, plan, edit, build, test, review, merge, operate. SWE-agent and OpenHands run it at repository scale; the literature calls the result the agentic SDLC and records SWE-bench Verified rising from 1.96 to 78.4 percent between October 2023 and April 2026. A systematic review of 92 studies found the deciding factor: "output verifiability is the primary enabler of agentic adoption."

**A verifiable ecosystem lets agents build verified large-scale software by three principles the functional-programming and hardware communities already live by.**

**The formal spec is the contract.** RISC-V specifies its architecture twice: the ISA manual is the official prose, and the Sail model, chosen in 2019 over four rivals in Haskell or Coq, is the official formal specification. The Architectural Certification Tests compute expected results from Sail and gate the "RISC-V Compatible" mark, and their README insists they are not verification tests. The agentic analogue: intent lands in a spec that tools can execute, and the prose stays prose.

**Make illegal states unrepresentable.** Yaron Minsky's maxim is typed functional programming's working rule, and the verified canon runs on it: CompCert is written in Coq's functional language and extracted to OCaml; seL4's 8,700 lines of C were derived from a Haskell prototype and proved in roughly 200,000 lines of Isabelle; QuickCheck made properties executable tests. An agent that cannot express a forbidden state cannot reach it.

**Verification is sign-off, not afterthought.** Verification consumes 60 to 70 percent of engineering effort on a chip project; simulation still dominates, formal grows every year, and CIRCT is carrying MLIR into that world, experimentally. A 2025 formal check of the open CHERIoT-Ibex core against its Sail specification found around thirty bugs, four breaking CHERI's monotonicity property. Csmith spent six CPU-years failing to find a wrong-code bug in CompCert's verified middle-end and still concluded that "verification does not obviate testing, but rather complements it." Proofs and tests together, and neither merges on its own word.

> Hardware ships when verification signs off. Software written by agents should ship the same way.

Auto-research is out of scope; the loop being made trustworthy is the one that ships software.

## 3. 2026, layer by layer

### Compiler: Mojo goes open at ModCon

Mojo 1.0 shipped on August 11, a stability milestone: 1.x changes "primarily additive," source stable, ABI not. A week later at ModCon, Modular open-sourced the entire compiler and toolchain under Apache 2.0 with LLVM exceptions. MAX stays source-available, and Modular is now a Qualcomm company.

Modular's earlier docs called Mojo "the first major language designed expressly for MLIR"; the current vision doc says "built purely on top of MLIR Core," aiming at "a unified language for kernel development," with MAX's own kernels already written in it. My argument, which Modular does not make: an open, general-purpose compiler built directly on MLIR is the pattern book for DSLs on MLIR and for verification hooks inserted before lowering erases the structure they need. The Mojo 1.0 post covers the language itself.

The boundary: open in source, closed in governance. Modular is not taking compiler contributions yet, "particularly in today's era of AI coding," and aims to by year end. No analyzer needs that queue. The IR is must-open; the gate is can-close.

### Harness: DeepSeek Harness on Cordis

DeepSeek Harness, binary `dsh`, arrived on August 13 as an MIT-licensed developer preview and had 179,486 GitHub stars by August 21. It is built on Cordis, a 2022 plugin framework it credits as its foundation, with two invariants. Everything is a plugin: the model adapter, the tool registry, the session log, and the agent loop itself, with no privileged core. Model-visible means logged: anything that reaches a model request must be reconstructable from the append-only session log, and a runtime invariant asserts it.

DeepSeek Harness does not credit pi, Mario Zechner's coding agent; pi's footprint is one npm package, pi-ai, a model adapter used by one plugin. The two are opposite answers to the same problem: pi keeps a four-tool core and refuses sub-agents, plan mode, and MCP; `dsh` ships sub-agents, planning, skills, sandboxing, and approval policy in its Standard preset, and only its Minimal preset, a two-tool loop for benchmarking, is pi-shaped.

This is the layer the ICML paper says stays private, the harness that "captures the user's exact process of software development." The log and the plugin interface are must-open, the harness can be anyone's, and a model lab has opened it.

### Proofs: Amazon funds Lean outside Amazon; CSLib builds the library

On July 26 Amazon's Automated Reasoning organization made what the Lean FRO calls the single largest donation in its history, amount undisclosed, to a body it does not control. The reason given is the whole argument for open proof tools: "it's easier to trust a proof when you can evaluate the tools behind it yourself."

CSLib is a separate effort, announced in August 2025 with a white paper in February 2026: Mathlib for computer science, plus Boole, an imperative language that discharges into Lean verification conditions. Its own steering committee spans Amazon, Google DeepMind, Stanford, UT Austin, Southern Denmark, and the Lean FRO, and its funding runs through its own channel, a Renaissance Philanthropy program. Its authors name the bottleneck, "AI-based provers are bottlenecked by the abstractions available in the underlying proof assistant," and their governance rule is the right one: AI advisory only, every commit through manual review.

My judgment: an independently governed checker plus a shared library of abstractions is the biggest step AI-aided formal verification has taken toward agents writing proofs that humans can check. The proof checker is the last check, so its governance is must-open.

### Weights: the coalition letter

On July 24 NVIDIA hosted "Open Weights and American AI Leadership," an open letter to U.S. policymakers that grew from 25 launch signatories led by NVIDIA, Microsoft, and Meta to 235 in its July 29 revision; Google, OpenAI, and Amazon joined within the week, and most of the rest are startups, infrastructure vendors, and nonprofits. It is advocacy, not commitment. It argues on five heads, access, competition, control, adaptability, and security, with the last inverted from the usual framing: "Relying solely on closed models is not inherently safe."

The letter argues for the finished artifact; the ICML paper says the artifact is inert. Both are right: weights decide the cost floor, a leaf that can go either way, and the cake decides whether the output can be trusted.

### Models and environments: Prime Intellect, GLM, Kimi, and a desk-sized box

Prime Intellect's stack separates the trainer from the task. prime-rl (Apache-2.0) runs asynchronous RL as three processes, vLLM inference, an orchestrator, and an FSDP2 trainer; verifiers (MIT) packages a task as an environment, a dataset plus a harness plus reward functions; the Environments Hub versions more than 2,500 of them. The reward is a deterministic check or an LLM judge "where deterministic evaluation is impractical." Prime Intellect does not use these words; the mapping is mine: a deterministic reward is verification, a judged reward is validation, and one environment scores training and evaluation alike.

Z.ai's GLM-5.2 (753B parameters, MIT) and Moonshot's Kimi K3 (2.8T, Kimi K3 License) approach frontier models on the labs' own benchmarks; Moonshot itself says K3 "still trails the most powerful proprietary models." Neither runs on a DGX Spark. NVIDIA rates the $4,699, 128 GB box for inference to 200B parameters and fine-tuning to 70B; what fits is GLM-4.7-Flash (30B-A3B, MIT) in BF16 or INTELLECT-3 (106B-A12B) at 4-bit, with LoRA fine-tuning documented by NVIDIA and prime-rl's RL loop not. Local is real at 30 to 70 billion parameters.

Models are leaves. Environments are evidence, and a reward nobody else can run is not a benchmark, so environments must be open.

## 4. Which layers open, and why

Three forces open a layer. Common infrastructure: everyone needs to build on it. Strategic collaboration: sharing it beats competing over it. Network effects: it is worth more with every implementation that speaks it. LLVM is all three compounding, a permissive substrate funded by rivals. Openness at a connective layer is architectural, so I expect these layers to open whether or not anyone is virtuous.

Tan and colleagues ask which layers must be public and answer with institutions; I ask which must be open and answer with a rule. **A layer that exists to connect independent systems must be open: policy semantics, agent protocols, effect logs, compiler IR and its analyzers, evidence formats, the proof checker.** A leaf can be closed, as long as the layers around it emit portable evidence: weights, hosted inference, the best client, a compiler's contribution queue.

> A layer that connects independent systems cannot be closed without destroying its reason to exist.

The reader's test for any layer: does its value come from connecting things that do not share an owner? Zed passes, a GPL-3.0 editor with an Apache-2.0 protocol and closed agents behind it; a harness whose session log only its vendor can parse does not.

## 5. The ecosystem is its tooling

**An ecosystem is as good as its developer tooling.** Weights without a harness are a download; proofs without an open checker are a vendor's assurance. Trust arrives through the compiler that checks, the harness that logs, the prover that admits, and the evidence format that survives a vendor change.

The series goes deep on each layer from here, beginning with the holy wars of programming languages and their SDKs and where each language sits in the cake. Next: Part 2, From Leaky Abstractions to Type-Safe Abstractions in the Era of the Open Ecosystem.

Out of scope: the ethics of open versus closed, everything below the ABI including hardware and robotics, and anything outside software engineering.

A note on provenance. This essay is the culmination of conversations with hundreds of researchers across three 2026 events: ICSE 2026 in Rio de Janeiro, from the Doctoral Symposium (April 14) to the IDE 2026 workshop organized by JetBrains Research (April 18); The Verification Summit by Pramaana Labs in San Francisco (June 10); and ModCon 2026 in San Francisco (August 18), where Mojo's compiler went open.

## References

### Stance

1. J. Tan, N. Vincent, K. Elkins, M. Sahlgren, J. Low, D. Pham, S. Pyysalo, J. Jitsev, "Position: If open source is to win, it must go public," ICML 2026 (Spotlight), arXiv:2507.09296v3: https://arxiv.org/abs/2507.09296

### Agentic SDLC and verified-software principles

2. H. Bhati, "Agentic AI in the Software Development Lifecycle," arXiv:2604.26275 (2026-04-29): https://arxiv.org/abs/2604.26275
3. J. Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," NeurIPS 2024, arXiv:2405.15793: https://arxiv.org/abs/2405.15793
4. X. Wang et al., "OpenHands: An Open Platform for AI Software Developers as Generalist Agents," ICLR 2025, arXiv:2407.16741: https://arxiv.org/abs/2407.16741
5. S. A. Apostolou, J. Bosch, H. Holmström Olsson, "Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle," arXiv:2605.15245 (2026-05-14): https://arxiv.org/abs/2605.15245
6. riscv/sail-riscv, formal specification of the RISC-V ISA: https://github.com/riscv/sail-riscv
7. RISC-V ISA Formal Spec Public Review (2019; Sail selected over Forvis, GRIFT, riscv-plv, Kami): https://github.com/riscvarchive/ISA_Formal_Spec_Public_Review
8. riscv/riscv-arch-test, Architectural Certification Tests (Sail as reference model; "not verification tests"): https://github.com/riscv/riscv-arch-test
9. H. Foster, 2024 Siemens EDA / Wilson Research Group IC/ASIC Functional Verification Trend Report: https://verificationacademy.com/topics/planning-measurement-and-analysis/wrg-industry-data-and-trends/2024-siemens-eda-and-wilson-research-group-ic-asic-functional-verification-trend-report/
10. CIRCT, Circuit IR Compilers and Tools (self-described experimental): https://circt.llvm.org/
11. L. Ploix et al., "Comprehensive Formal Verification of Observational Correctness for the CHERIoT-Ibex Processor," arXiv:2502.04738: https://arxiv.org/abs/2502.04738
12. X. Leroy, "Formal verification of a realistic compiler," CACM 52(7), 2009: https://xavierleroy.org/publi/compcert-CACM.pdf
13. X. Yang, Y. Chen, E. Eide, J. Regehr, "Finding and Understanding Bugs in C Compilers," PLDI 2011: https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf
14. G. Klein et al., "seL4: Formal Verification of an OS Kernel," SOSP 2009: https://dl.acm.org/doi/10.1145/1629575.1629596
15. Y. Minsky, "Effective ML Revisited," Jane Street (2011-03-09): https://blog.janestreet.com/effective-ml-revisited/
16. K. Claessen, J. Hughes, "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs," ICFP 2000: https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf

### Compiler

17. Modular, "Modular 26.5: Mojo 1.0 is here!" (2026-08-11): https://www.modular.com/blog/modular-26-5-mojo-1-0-is-here
18. Mojo documentation, "Mojo stability guarantees" (source-level; ABI not stable): https://mojolang.org/docs/api-docs/stability/
19. Modular, "Mojo is now open source!" (2026-08-18; Apache 2.0 with LLVM exceptions; compiler contributions not yet accepted): https://www.modular.com/blog/mojo-open-source
20. Modular, "ModCon 2026: Open source, open cloud, open silicon" (2026-08-18): https://www.modular.com/blog/modcon-announcements
21. Qualcomm / Modular, "Qualcomm Completes Acquisition of Modular" (2026-07-29): https://www.modular.com/blog/qualcomm-completes-acquisition-of-modular
22. Modular, "Why Mojo" (archived 2024-06-05; "the first major language designed expressly for MLIR"; page since redirected): https://web.archive.org/web/20240605012702/https://docs.modular.com/mojo/why-mojo
23. Mojo documentation, "Mojo vision" ("built purely on top of MLIR Core"; "a unified language for kernel development"): https://mojolang.org/docs/vision/

### Harness

24. DeepSeek AI, DeepSeek Harness (MIT, developer preview; repo created 2026-08-13; 179,486 stars on 2026-08-21): https://github.com/deepseek-ai/deepseek-harness
25. DeepSeek AI, "DeepSeek Harness Architecture" (everything is a plugin; model-visible means logged): https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md
26. DeepSeek AI, DeepSeek Harness product site (Standard, Code, Minimal, Creator modes): https://deepseek.com/harness/en/
27. cordiverse/cordis, meta-framework of spatiotemporal composability (MIT, 2022): https://github.com/cordiverse/cordis
28. Y. Shi, W. Zhang, T. Cui, "A Programming Paradigm for Spatiotemporal Composability" (Cordis paper): https://github.com/cordiverse/paper
29. M. Zechner et al., pi coding agent, philosophy (four tools; no sub-agents, plan mode, or MCP): https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md
30. Agent Client Protocol (Apache-2.0): https://agentclientprotocol.com
31. Zed (GPL-3.0-or-later): https://github.com/zed-industries/zed

### Proofs and policy

32. B. Cook, S. Bice, "Amazon is investing in the Lean Focused Research Organization," Amazon Science (2026-07-26): https://www.amazon.science/news/amazon-is-investing-in-the-lean-focused-research-organization
33. Lean FRO, "About the Lean FRO" (timeline; Amazon Automated Reasoning donation): https://lean-lang.org/fro/about/
34. C. Barrett, S. Chaudhuri, F. Montesi, J. Grundy, P. Kohli, L. de Moura, A. Rademaker, S. Yingchareonthawornchai, "CSLib: The Lean Computer Science Library," arXiv:2602.04846 (2026-02-04): https://arxiv.org/abs/2602.04846
35. CSLib Initiative (Renaissance Philanthropy), "About": https://www.cslib.io/initiative/about
36. cedar-spec, Lean formalization and differential testing of Cedar: https://github.com/cedar-policy/cedar-spec

### Weights

37. NVIDIA et al., "Open Weights and American AI Leadership," open letter (2026-07-24; PDF revised 2026-07-29, 235 signatories): https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf
38. Microsoft, live signatory page (270+ organizations as of 2026-08-03): https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/
39. Security Boulevard, "Nvidia Rallied the Industry Behind Open Weights. Then OpenAI Joined Anyway." (August 2026): https://securityboulevard.com/2026/08/nvidia-rallied-the-industry-behind-open-weights-then-openai-joined-anyway/

### Models and environments

40. Prime Intellect, prime-rl (Apache-2.0; vLLM inference, orchestrator, FSDP2 trainer): https://github.com/PrimeIntellect-ai/prime-rl
41. Prime Intellect / W. Brown, verifiers (MIT; environments, rubrics, LLM judges): https://github.com/PrimeIntellect-ai/verifiers
42. Prime Intellect, "Environments Hub" (2025-08-27): https://www.primeintellect.ai/blog/environments
43. Prime Intellect, "INTELLECT-3" (2025-11-26; 106B-A12B on GLM-4.5-Air base): https://www.primeintellect.ai/blog/intellect-3
44. Z.ai, GLM-5.2 model card (753B, MIT, 2026-06-16): https://huggingface.co/zai-org/GLM-5.2
45. Z.ai, GLM-4.7-Flash model card (30B-A3B, MIT): https://huggingface.co/zai-org/GLM-4.7-Flash
46. Moonshot AI, "Kimi K3: Open Frontier Intelligence" ("still trails the most powerful proprietary models"): https://www.kimi.com/blog/kimi-k3
47. Moonshot AI, Kimi K3 model card and license (2.8T, Kimi K3 License): https://huggingface.co/moonshotai/Kimi-K3
48. NVIDIA, DGX Spark product page (128 GB unified memory; 200B inference; 70B fine-tuning): https://www.nvidia.com/en-us/products/workstations/dgx-spark/
49. NVIDIA Developer Forums, DGX Spark price change to $4,699 (2026-02-23): https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713
50. NVIDIA, DGX Spark "Fine-tune with PyTorch" playbook (1–70B; SFT, LoRA, QLoRA): https://build.nvidia.com/spark/pytorch-fine-tune

### Conferences

51. ICSE 2026, Rio de Janeiro (April 12–18): https://conf.researchr.org/home/icse-2026
52. ICSE 2026 Doctoral Symposium (April 14): https://conf.researchr.org/track/icse-2026/icse-2026-doctoral-symposium
53. IDE 2026, 3rd International Workshop on Integrated Development Environments, co-located with ICSE 2026 (April 18; general chair Y. Golubev, JetBrains Research): https://ide-workshop.github.io/
54. The Verification Summit, Launch Edition, Pramaana Labs, San Francisco (2026-06-10): https://verificationsummit.ai/
55. ModCon 2026: Compute Unlocked, Grand Hyatt San Francisco (2026-08-18): https://www.modular.com/modcon
