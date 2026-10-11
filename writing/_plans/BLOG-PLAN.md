# Blog plan

Written 2026-10-11. The release order below is the owner's; the five-thread
roadmap at the bottom is a copy of what `blog/index.html` shows on that date.

## Series: Compositions and Abstractions for Software

Point of view: compilers, programming languages and static analysis. Domain:
software construction. Ten parts planned; the first three are set.

| Part | Essay | Status | Release |
|---|---|---|---|
| 1 | Testing Compositional MCP in Zero Trust: the Toronto demo, the deck, the code | live: `blog/testing-compositional-mcp-zero-trust/` | Oct 11, 2026 |
| 2 | Summer 2026: the Mojo compiler, the Lean FRO, the DeepSeek harness, and Nvidia's acquisition of Hugging Face | written, dormant until release; the Aug 21 page stays as it is until then | Oct 15, 2026 |
| 3 | The gang of four: Rust, Mojo, C++ and Lean | not written | Oct 18, 2026 |

Conventions: each essay has its Markdown source under `writing/<slug>/source.md`
with figures in `diagrams/` beside it, is built by `tools/build_essay.py` into
`blog/<slug>/`, and gets a redirect at `writing/<slug>/index.html`. The hero
carries the series navigation (`--prev`, `--next`; a label without a URL is
text until the neighbour exists). The deck downloads live in `docs/`.

## Roadmap as published on blog/index.html (copied 2026-10-11)

This fall, the series explores AI engineering through five interconnected
threads that bring together mathematics, systems engineering, and economics.

### Thread 1 / 10 posts: Goldilocks Zone

Compilers, protocols, open weights, proof infrastructure, policy semantics,
interoperability, portable evidence, and their assembly into an AI-native stack.

1. Summer 2026: Mojo 1.0, DeepSeek Harness, Lean FRO, and the Open-Weights Letter (Aug 21, 2026)
2. From ModCon to One Language, Many IRs: Mojo 1.0, MLIR, LLVM, and the DSL Threshold (planned)
3. Inside Mojo's Compiler: From LIT and KGEN to LLVM IR (planned)
4. Auditing Mojo's Open Compiler: Reproducible Lowering and External Verification (planned)
5. The Goldilocks Boundary: Open Connective Layers, Closed Competitive Leaves (planned)
6. The Protocol Fabric: LSP, ACP, MCP, and A2A Without Vendor Lock-In (planned)
7. The Activation Stack: What Open Weights Need Beyond Model Files (planned)
8. Portable Evidence: Moving Proofs, Tests, Traces, and Receipts Between Tools (planned)
9. Policy and Proof as Open Semantics: Cedar, Lean, and Independently Checkable Semantics (planned)
10. Conclusion: The AI-Native Stack of the Open Ecosystem (planned)

### Thread 2 / 10 posts: AI Supercycle

Economics only: capital intensity, scarcity rents, complements, market
structure, standards, network effects, ownership, and value migration.

1. The AI Supercycle: Capital, Compute, and the New Industrial Flywheel
2. Five Layers of Capital: Energy, Chips, Infrastructure, Models, and Applications
3. Scarcity Rents: Power, Silicon, Data Centers, and the Price of Intelligence
4. The Invisible Hand of Commoditization: When Foundational Layers Become Shared
5. Open Source as Strategy: Common Goods, Catch-Up, and Competitive Complements
6. Models, Tools, and Complements: Where Value Accrues in the Agent Economy
7. Hyperscalers, Neoclouds, and AI Factories: The New Market Structure
8. The Economics of Agentic Labor: Productivity, Marginal Cost, and Ownership
9. Standards as Markets: Network Effects, Switching Costs, and Protocol Adoption
10. After the Gold Rush: Where Durable Value Remains in the AI Supercycle

### Thread 3 / 10 posts: Hybrid Analysis

Analysis methodology only: static reasoning, runtime observation, symbolic
execution, concolic testing, verification, validation, synthesis, model
behavior, drift, evidence graphs, and operational neuro-symbolic compilation.

1. From Static Theory to the Dynamic World: Why One View Is Never Enough
2. Before Execution: Abstract Interpretation, Dataflow, and the Shape of Possibility
3. After Execution: Traces, Profiles, and the Facts Programs Reveal
4. Joining the Views: Sound Over-Approximation Meets Runtime Evidence
5. Paths Under Constraint: Symbolic Execution, Concolic Testing, and Solver-Guided Exploration
6. Verification Is Not Validation: Proving the System and Testing the Claim
7. Synthesis in the Loop: Counterexamples, Constraints, and Language Models
8. Inside the Model: Mechanistic Interpretability and Influence Functions
9. A Moving Target: Continual Learning, Drift, and Time-Indexed Evidence
10. The UNIVERSAL VIRTUAL GRAPH: Unification with Neuro-Symbolic Compilation

### Thread 4 / 10 posts: Software 4.0

Systems engineering only: generic programming, language design, negative-cost
abstractions, typed agent work, engineering environments, roles, lifecycle
ownership, and measured costs.

1. Software 4.0: From Mathematics to Systems Engineering
2. From Algebra to Architecture: Generic Programming as an Engineering Method
3. The Language Wars After Code Generation: What Still Matters When Agents Program
4. Negative-Cost Abstractions: When Stronger Invariants Reduce Total Cost
5. Systems Languages in the AI Era: Mojo, Rust, and the Search for a Unified Stack
6. A Type System for Agent Work: Intent, Capabilities, Effects, and Evidence
7. DeepSeek Harness and the Typed Agent Runtime
8. The New Engineering Workbench: IDEs, CLIs, Sandboxes, and Agent Teams
9. The Five-Persona System: Software, AI, Platform, Security, and DevOps
10. Engineering Beyond Code: Review, Acceptance, Ownership, and the Software 4.0 SDLC

### Thread 5 / 10 posts: The Holy Grails

Mechanistic interpretability plus program analysis: decidability and
complexity, finite abstraction, fixpoint semantics, neural IRs, neural
verification, guided program synthesis, and neuro-symbolic compilation.

1. The Holy Grails: Mechanistic Interpretability Meets Program Analysis
2. P vs. NP: Scaling Verification Through Bounded Approximation
3. The Verification Space: Programs, Models, Properties, Environments, and Time
4. Finite Answers to Infinite State Spaces: Abstraction, Widening, and Bounded Unrolling
5. Fixpoints Are Not All the Same: Lattices, Recurrence, and Equilibrium Models
6. What Is a Neural IR? Features, Circuits, and Causal Abstractions
7. Compile, Then Decompile: RASP, Tracr, and Ground-Truth Circuits
8. Verifying Neural Networks: Abstract Domains, SMT, and Branch-and-Bound
9. Gradient Descent Meets Symbolic Descent: Ndea and Guided Program Synthesis
10. Neuro-Symbolic Compilation: Mapping the Verification Space
