# Leaky Abstractions vs. Type-Safe Abstractions in the Era of AI Coding Agents

Part 1 of The Open Ecosystem and the Future of Software Engineering

I am writing this as a doctoral researcher in hybrid program analysis and as an engineer who spends a large part of the day inside real tools. The technical shift is already visible in ordinary software work: agents are becoming active participants in repository state transitions, but the abstractions around them are still too informal.

The claim of this essay is simple:

```text
AI coding agents are exposing a missing layer between human intent
and executable side effects.
```

That missing layer is not one thing. It is a stack of specifications, policies, typed handoffs, runtime effects, compiler representations, and evidence. Some of those ideas come from formal methods. Some come from programming languages. Some come from editor and CLI design. Some come from open-source economics.

They now belong in the same conversation.

## 1. One window

My current development environment has collapsed into one working surface.

Zed is the editor. The CLI is the durable execution substrate. Codex, Claude Code, Cursor, and other agents enter through command-line workflows. Handoffs, review notes, diffs, tests, and evidence are coordinated around the repository rather than around one chat interface.

The significance is that editor, shell, agent, and evidence are converging at the point where repository state changes.

```text
                         one working surface

+------------------------------------------------------------------+
| Zed                                                              |
|                                                                  |
| source files | terminal | diffs | notes | logs | review context  |
+------------------------------+-----------------------------------+
                               |
                               v
                       CLI / ACP boundary
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v
        Codex             Claude Code             Cursor
          |                    |                    |
          +--------------------+--------------------+
                               |
                               v
                  handoffs / orchestration / evidence
```

The editor is no longer only a place where a human writes text. It is becoming the human control plane for agentic software engineering. The CLI matters because it remains the most stable way to bind an agent to a real repository, a real shell, real tests, and real failure modes.

The right endpoint is not one perfect agent UI. It is an environment where agents remain interchangeable because the surrounding workflow carries the constraints and evidence.

The unit that matters is not:

```text
agent UI
```

It is:

```text
workflow + constraints + evidence
```

Once the workflow is explicit enough, the particular model can change. A stronger model can replace a weaker one. A local model can take over a narrow task. A specialized reviewer can judge a patch. A theorem prover can check a formal obligation. A compiler can reject an invalid lowering. The engineering system should not collapse when one agent is swapped out.

That is the first technical reason open interfaces matter.

## 2. The current abstraction leaks

Today, much of agentic development still looks like this:

```text
prompt
  -> agent
  -> Markdown handoff
  -> another agent
  -> shell command
  -> filesystem mutation
  -> prose summary
```

This works often enough to be useful. It also leaks in exactly the places where software engineering needs precision.

The intent is informal. The permissions are often ambient. The tool boundary is weak. The file system is treated as a shared substrate rather than a typed resource. The test result is usually summarized in prose. The reviewer may receive a diff without a precise statement of the allowed effects. Completion is often defined socially rather than technically.

For a human, this informality can be manageable. Humans infer the boundary from culture, taste, experience, and consequences. If a maintainer says "refactor the parser," a good engineer usually understands that this does not include changing the public API, editing CI, adding a dependency, or accessing the network.

An agent should not have to infer those limits from implicit social cues.

The stronger abstraction is:

```text
intent
  -> candidate formal specification
  -> authorization policy
  -> semantic obligations
  -> typed handoff
  -> effect-aware execution
  -> evidence packet
  -> human acceptance
```

That does not mean every code change becomes fully formal. It means the system should reduce ambiguity as work moves from intent to side effect.

Compilers already do this.

Programs do not remain raw text all the way to execution. They pass through parse trees, type checks, semantic checks, intermediate representations, optimization passes, lowering stages, and target-specific code generation. The point of the compiler pipeline is not ceremony. It is progressive commitment: each stage makes some ambiguity impossible and some invariants checkable.

AI software engineering needs the same instinct above the code level.

## 3. The open agentic software stack

The stack I have in mind has three technical layers and one evidence layer.

```text
                     OPEN AGENTIC SOFTWARE STACK

Human intent
    |
    v
Autoformalization
    |
    v
+--------------------------------------------------+
| FORMAL INTENT / POLICY                           |
|                                                  |
| preconditions, postconditions, invariants         |
| capabilities and forbidden effects               |
| Cedar-style authorization policy                  |
| semantic obligations for verification/validation  |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
| AGENT HARNESS                                    |
|                                                  |
| ACP / CLI                                        |
| Codex / Claude Code / Cursor                     |
| DeepSeek Harness / Cordis                        |
| typed handoffs, reviewers, judges, event logs     |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
| COMPILER / LANGUAGE INFRASTRUCTURE               |
|                                                  |
| Mojo                                             |
| MLIR-based compiler practice                     |
| domain-specific dialects and lowering pipelines   |
| future verification and policy-aware dialects     |
+-------------------------+------------------------+
                          |
                          v
                  executable system
                          |
                          v
                  evidence / witness
```

The formal intent layer asks what the user meant, what the user allowed, and what the resulting program must preserve.

The agent harness layer asks how models become bounded actors with tools, events, effects, reviewer loops, and durable handoffs.

The compiler layer asks how source-level ambiguity becomes checked structure and executable behavior.

The evidence layer asks what remains after the system acts: tests, traces, proofs, logs, diffs, counterexamples, and human review decisions.

The layers should remain separable. If one closed system owns intent, policy, harness, compiler, and evidence, then the developer cannot inspect where authority ended and where behavior began. Open interfaces are not a moral ornament here. They are part of the engineering method.

## 4. The Goldilocks problem

The missing layer should not be understood as "add maximum formalism everywhere." That would be as wrong as leaving everything in prose.

The engineering problem is calibration. A trivial documentation edit should not require a proof assistant. A parser refactor should have stronger obligations than a spelling fix. A dependency update should have stronger policy and evidence requirements than a local comment change. A security-sensitive runtime change should carry still more structure.

The useful target is a Goldilocks zone: enough structure to constrain authority and preserve evidence, not so much structure that ordinary engineering becomes impossible.

```text
                Goldilocks zone for agentic software work

under-specified              calibrated                     over-specified
----------------             ----------------               ----------------
prompt-only intent           typed task intent              full proof for
ambient filesystem           bounded capabilities           every edit
prose handoffs               structured handoffs            brittle workflow
untyped tool calls           effect-aware tools             blocked iteration
summary-as-evidence          evidence packet                ceremony > signal

risk: silent side effects     target: inspectable work       risk: unusable
      false completion                bounded authority            process
      weak review                     proportional evidence        false rigor
```

There is a similar Goldilocks problem for openness.

```text
                 Goldilocks zone for open infrastructure

closed vertical              open common layer              fragmented openness
---------------              -----------------              -------------------
one vendor owns              shared semantics               source exists but
model + harness              stable interfaces              nothing composes
policy + evidence            portable evidence              dialect drift
compiler boundary            multiple implementations       fork-only adoption

risk: lock-in                target: interoperability       risk: incoherence
      weak inspection                independent review            no standards
      no replacement                 compounding adoption          no leverage
```

And there is a Goldilocks problem for evidence.

```text
                       Evidence proportional to risk

low-risk change           medium-risk change          high-risk change
---------------           ------------------          ----------------
formatting                parser/runtime logic        authorization,
comments                  dependency behavior         security,
local docs                compiler lowering           payments,
                           API compatibility          safety boundary

evidence:                 evidence:                   evidence:
diff review               tests + static checks       policy + tests +
basic tests               dynamic traces              static analysis +
                           compatibility checks       proof obligation or
                                                      explicit human signoff
```

The stack should therefore be risk-sensitive. The task representation should carry enough information to decide what evidence is required, which effects are allowed, and when a human must make the final acceptance decision.

This is where hybrid program analysis becomes useful. Static checks, dynamic checks, formal obligations, policy decisions, and human review are not competing religions. They are instruments with different operating ranges.

## 5. Cedar is not autoformalization

Cedar is useful in this stack, but it should not be confused with autoformalization.

Cedar answers an authorization question:

```text
May this principal perform this action
on this resource
in this context?
```

Autoformalization asks a different question:

```text
Can an informal intent be translated into a structured formal object
that a machine can check, refine, or use?
```

A useful task representation might look like this:

```text
Phi = <Pre, Post, Inv, Cap, Effects, Evidence>
```

where:

```text
Pre       = assumptions before the task
Post      = required properties after the task
Inv       = invariants that must not be broken
Cap       = capabilities granted to the actor
Effects   = allowed and forbidden side effects
Evidence  = what must be produced for acceptance
```

Only part of that object projects into authorization policy:

```text
Cap(Phi) + Effects(Phi) -> Cedar-style policy
```

For example:

```text
Refactor the parser.
You may modify parser source and tests.
Do not change public APIs.
Do not add dependencies.
Do not edit CI.
Do not access the network.
```

This should split into two classes of constraints.

Authorization constraints:

```text
permit(agent, Read, parser/**)
permit(agent, Write, parser/**)
permit(agent, Write, tests/**)

forbid(agent, Write, Cargo.toml)
forbid(agent, Write, .github/**)
forbid(agent, Network, *)
```

Semantic obligations:

```text
public_api(before) == public_api(after)
tests(after) == PASS
behavior(before) ~= behavior(after)
```

The first class says what the agent may do. The second class says what the resulting program must satisfy.

This distinction matters because a policy engine can correctly prevent a forbidden write and still say nothing about whether the parser remains correct. Conversely, a test suite can pass while the agent used authority it should not have had. Authorization and verification are complementary. They are not substitutes.

## 6. Autoformalization is becoming a knowledge-base problem

The autoformalization literature is moving in exactly the direction this stack needs.

The important shift is from isolated statements to structured formal knowledge. Translating one theorem into Lean is useful, but real verification work usually depends on a library of definitions, lemmas, invariants, proof infrastructure, and naming conventions. A theorem rarely stands alone. It sits inside a theory.

That is why the theory-level autoformalization agenda is important. It reframes autoformalization as the construction of coherent formal libraries rather than one-off translations. In software terms, this is the difference between generating a single type signature and building the surrounding module system, dependency graph, invariants, and proofs needed for that signature to mean anything.

```text
isolated statement formalization

informal theorem
      |
      v
formal theorem


theory-level autoformalization

informal notes / papers / code comments / specs
      |
      v
definitions + axioms + lemmas + notations + tactics
      |
      v
structured formal library
      |
      v
target theorem / verification condition
```

CSLib is relevant for the same reason. The Lean ecosystem has Mathlib for mathematics. Computer science needs its own body of reusable formal infrastructure: automata, operational semantics, algorithms, complexity, program logics, compiler semantics, network models, and verification conditions. Without that substrate, "autoformalize this software claim" often has nowhere stable to land.

For AI coding agents, this becomes practical. If agents write more of the code, then the cost of checking the code has to fall. But checking cannot be only a bigger test run. Some claims need static analysis. Some need dynamic validation. Some need symbolic execution or SMT. Some need proof assistants. Some need a human to reject an invalid formalization even if it type-checks.

The research problem is not "let the model produce a proof and move on." The research problem is admission:

```text
candidate formalization
      |
      v
type check / proof check
      |
      v
semantic review
      |
      v
integration into a trusted library
      |
      v
reuse by future verification tasks
```

This is where hybrid program analysis enters the picture. Static evidence, dynamic evidence, formal evidence, and human evidence have different failure modes. A serious system needs to record which kind of claim each artifact supports.

## 7. Agent harnesses are becoming runtimes

Agent harnesses are not just wrappers around model calls. They are becoming runtimes for software work.

DeepSeek Harness is interesting because its public framing is plugin-oriented: an agent harness where tools and capabilities are part of the system structure. Cordis is interesting because it gives a formal vocabulary for composability, effects, coeffects, context, lifecycle, and implementation correspondence.

The Cordis paper's page 55 is a useful starting point for reading agent harnesses as runtimes: a table that maps theory-level objects to implementation objects. Symbols such as context, effects, fibers, lifecycle transitions, inverses, providers, and targets are put next to implementation constructs such as `ctx`, `ctx.effect`, `ctx.get`, `ctx.set`, `fiber`, `fiber.state`, and `fiber.dispose`.

That matters because agent systems are full of hidden state.

```text
agent run
  reads context
  calls tools
  changes files
  observes errors
  retries
  hands off
  gets reviewed
  resumes later
```

If the harness treats those steps as unstructured events, then the developer receives a story. If the harness treats them as typed effects with recoverable context, then the developer receives an inspectable execution.

The distinction is important:

```text
chat wrapper:
  model call + tool call + transcript

agent runtime:
  actor + capability + context + effect + inverse + event + evidence
```

The second form is closer to software engineering.

It lets a system ask better questions:

- Which capability authorized this tool call?
- Which context was visible?
- Which side effects occurred?
- Which effect has an inverse?
- Which reviewer judged the result?
- Which evidence was produced?
- Which state transition was accepted by the human?

Those questions are not decorative. They are the beginning of a programming model.

## 8. Mojo, MLIR, and open compiler practice

Mojo's compiler being open source is important beyond Mojo itself.

Modular's post says the Mojo language, compiler, tooling, and the source needed to build the language are available in the `modular` GitHub repository under Apache 2.0 with LLVM exceptions. That matters because Mojo is not only a language story. It is a compiler-infrastructure story.

The interesting possibility is that Mojo becomes one of the first broadly visible, implementation-serious, general-purpose languages whose open compiler makes the MLIR ecosystem legible to ordinary systems programmers.

MLIR has already mattered in compiler research and infrastructure. But many developers still experience MLIR as something behind the curtain: a framework used by compiler teams, accelerator stacks, tensor compilers, and DSL implementers. An open Mojo compiler gives the broader compiler industry a concrete reference point for how a modern language can be built around MLIR-based ideas.

The value is not only "you can read the code." The value is that the code can become a living pattern book for using and creating DSLs on top of MLIR-based compilers:

```text
application domain
      |
      v
language / DSL surface
      |
      v
typed semantic representation
      |
      v
MLIR dialects and transformations
      |
      v
lowering pipeline
      |
      v
LLVM / accelerator / runtime target
```

For DSL authors, this is the important lesson. MLIR is not merely a back-end detail. It can shape how a language exposes domain structure, how transformations are organized, how optimizations are staged, and how verification hooks can be inserted before lowering erases useful information.

That connects directly to AI software engineering.

If agent-generated code is going to be trusted in high-performance and high-assurance settings, then the compiler cannot be a black box that simply accepts text. It should expose intermediate structure where analysis can attach:

```text
agent intent
      |
      v
source patch
      |
      v
typed language representation
      |
      v
domain-specific IR
      |
      v
analysis / verification / validation hooks
      |
      v
lowered executable artifact
      |
      v
witness
```

The "witness" here does not have to be a full proof. It can be a typed trace, a test certificate, a static-analysis report, a verified lowering condition, a proof artifact, or a counterexample. The important point is that the compiler stack should preserve enough structure for evidence to be meaningful.

This is why open compilers matter in the agent era. They are not only places to generate faster code. They are places to define and inspect the meaning of generated code.

## 9. Zed and high-performance local control

The IDE layer matters because humans still accept risk.

Zed is relevant not because every developer must use it, but because it represents a class of tool that should matter more: high-performance, local, programmable, and close to the repository. The Zed repository describes it as a high-performance multiplayer code editor from the creators of Atom and Tree-sitter. Its implementation in Rust is also relevant to the broader systems story: editor performance, concurrency, tree-sitter integration, and local responsiveness matter when the editor becomes a control plane for agents.

The useful interface is not a giant chat panel. It is a working surface where a human can inspect state:

```text
human control plane

code      -> what changed?
diff      -> where did it change?
tests     -> what ran?
trace     -> what happened?
policy    -> what was allowed?
handoff   -> what was delegated?
review    -> what was accepted or rejected?
```

The agent may write the patch. The harness may run the tools. The compiler may reject invalid structure. The proof assistant may check a theorem. But the human still needs a place to integrate the evidence.

That place should be fast, local, inspectable, and model-agnostic.

## 10. Open weights as part of the same ecosystem

The NVIDIA open-weights pledge belongs in this discussion because it shows that open models are no longer a fringe topic. Open weights are now argued for in terms of access, competition, control, adaptability, and security.

I do not need to endorse every policy claim in that document to treat it as evidence. The important point is that the industry argument for openness is becoming more explicit:

```text
open weights
  -> more access
  -> more local control
  -> more competition
  -> more specialized adaptation
  -> more independent evaluation
```

This does not make open weights automatically safe. Released weights can be misused, modified, or redistributed in ways the original developer cannot fully control. But closed models have their own risks: concentrated dependency, limited inspectability, narrow evaluation, and single points of failure.

For software engineering, the practical conclusion is modest:

```text
closed frontier models may remain important,
but open models keep the surrounding ecosystem honest.
```

They let researchers, small teams, universities, and infrastructure builders test workflows without asking permission from one model provider. They also make it easier to separate model capability from the rest of the stack: harness, policy, compiler, evidence, and review.

## 11. Why open?

The open ecosystem is not one argument. It is at least three.

```text
Why Open?

1. Common infrastructure
   Some layers should be shared because everyone needs to build on them.

2. Strategic collaboration
   Some layers are opened because cooperation is more useful than duplicated control.

3. Network effects
   Some layers become valuable only when many producers and consumers participate.
```

The Internet is common protocol infrastructure. Linux is shared operating-system infrastructure. LLVM is shared compiler infrastructure. They are not identical stories, but they show the same recurring pattern: a foundational layer becomes more valuable when many independent actors can build on it.

LLVM is especially instructive:

```text
                         LLVM
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
 common compiler     shared engineering   network effects
 infrastructure      across organizations languages, tools,
                                         targets, research
```

The lesson is not "open source wins because it is virtuous." That is too simple.

The better lesson is:

```text
Open ecosystems emerge when a foundational layer becomes more
valuable as shared infrastructure than as a private island.
```

Sometimes that begins as public infrastructure. Sometimes it begins as strategic collaboration. Sometimes the technology simply requires network effects. Often, all three forces reinforce each other over time.

Programming languages, compilers, protocols, intermediate representations, agent interfaces, policy languages, and formal libraries have this property. They gain value from tools, contributors, implementations, integrations, targets, and users.

For this series, that is the key idea:

```text
Sometimes openness is a feature of the architecture,
not only a license choice.
```

If a layer exists to connect independent systems, closing it can weaken the reason it exists.

## 12. From informal work to evidence-bearing execution

The central graph of this essay is this:

```text
human intent
    |
    v
natural language task
    |
    v
autoformalization
    |
    +------------------------------+
    |                              |
    v                              v
authorization policy          semantic obligations
who may do what               what must remain true
    |                              |
    +---------------+--------------+
                    |
                    v
              agent harness
       typed context + tools + effects
                    |
                    v
             repository mutation
                    |
                    v
          compiler / analyzer / tests
                    |
                    v
        proof, trace, counterexample,
        test result, or review packet
                    |
                    v
             human acceptance
```

This is the future abstraction this series investigates.

The model is part of it, but not all of it. The editor is part of it, but not all of it. The compiler is part of it, but not all of it. The proof assistant is part of it, but not all of it.

The system only becomes software engineering when the pieces compose.

## 13. What this series will track

The writing program has three recurring threads.

Open Ecosystem:

```text
open models
open weights
open harnesses
open compilers
open policy semantics
open evidence formats
```

Hybrid Analysis:

```text
static analysis
dynamic analysis
verification
validation
runtime traces
compiler IR
agent side effects
```

Future of Software Engineering:

```text
IDE as human control plane
CLI as durable execution base
agent protocols
typed handoffs
reviewer and judge graphs
languages for verifiable AI infrastructure
```

These threads should be revisited quarterly because the stack is moving too quickly for a one-time map.

The question is not whether agents will write code. They already do.

The question is whether the surrounding engineering discipline becomes stronger or weaker as they do.

## References by Layer

### Open compiler and MLIR ecosystem

- Modular, "Mojo is now open source": https://www.modular.com/blog/mojo-open-source
  - Classification: open compiler infrastructure.
  - Why it matters here: the Mojo compiler and tooling being open source provides a concrete reference for language and DSL builders working in the MLIR ecosystem. For compiler engineers, this is a chance to study modern language implementation practice rather than only consume a finished binary.

### Autoformalization and verification layer

- Marcus J. Min, Mike He, Zhaoyu Li, Zixuan Yi, Sharad Malik, Aarti Gupta, Xujie Si, Osbert Bastani, "Theory-Level Autoformalization: From Isolated Statements to Unified Formal Knowledge Bases": https://openreview.net/forum?id=BoteCHEFUr
  - PDF / arXiv mirror: https://arxiv.org/abs/2607.13292
  - Classification: theory-level autoformalization.
  - Why it matters here: it moves the target from isolated statement translation to coherent formal knowledge bases with dependencies.

- CSLib, "The Lean Computer Science Library": https://arxiv.org/pdf/2602.04846
  - Classification: formal computer-science library.
  - Why it matters here: it argues for reusable Lean infrastructure for computer science, including models, logics, algorithms, semantics, and verification infrastructure.

- Amazon Science, "Amazon is investing in the Lean Focused Research Organization": https://www.amazon.science/news/amazon-is-investing-in-the-lean-focused-research-organization
  - Classification: proof-assistant ecosystem support.
  - Why it matters here: it frames Lean as infrastructure whose trustworthiness depends on independent validation, transparency, and external community development.

### Formal policy layer

- Cedar policy language: https://github.com/cedar-policy/cedar
  - Classification: authorization policy language and Rust implementation.
  - Why it matters here: Cedar separates authorization policy from application code and gives a concrete language for fine-grained permissions, validation, analysis, and audit.

### Agent harnesses

- DeepSeek Harness: https://github.com/deepseek-ai/deepseek-harness
  - Classification: open agent harness.
  - Why it matters here: it treats the harness as a plugin-oriented execution environment rather than only a model wrapper.

- Cordis, "A Programming Paradigm for Spatiotemporal Composability": https://github.com/cordiverse/paper/blob/main/paper.pdf
  - Classification: formal model for composable runtime structure.
  - Why it matters here: page 55 gives a theory-to-implementation correspondence table that maps formal constructs such as context, effects, fibers, lifecycle state, and inverses to concrete implementation objects.

### IDE and developer control plane

- Zed: https://github.com/zed-industries/zed
  - Classification: high-performance local editor infrastructure.
  - Why it matters here: my current setup uses Zed with Codex, Claude Code, and Cursor through CLI workflows, with handoffs and agent orchestration organized around the repository.

### Open weights and open AI infrastructure

- NVIDIA, "Open Weights and American AI Leadership": https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf
  - Classification: open-weights policy and ecosystem argument.
  - Why it matters here: it makes the industrial case for open weights in terms of access, competition, control, adaptability, and security, which belongs in the broader open ecosystem analysis.

---

