# Archive: Draft 2 Before Research-Voice Rewrite (Preserved)

The draft below was the previous active version. It is preserved so earlier structure and wording remain available, but the publishable article now starts above this archive.

# Leaky Abstractions vs. Type-Safe Abstractions in the Era of AI Coding Agents

Part 1 of The Open Ecosystem and the Future of Software Engineering

Draft status: active Blog 1 draft.

This is personal technical thought leadership. I am writing as a researcher in hybrid program analysis, a systems/compiler engineer, a heavy user of coding agents, and an open-source builder trying to understand where software engineering is going.

## High-Level Contents

1. My development environment has collapsed to one window.

   Zed, ACP/CLI, Codex, Claude Code, Cursor, judge loops, handoffs, and deep work now sit in the same daily workflow. That is not just a productivity change. It exposes where the abstractions around agentic software work are still informal.

2. The model is becoming interchangeable.

   Once a developer uses several strong coding agents, loyalty to one interface matters less. The valuable object becomes:

   ```text
   workflow > agent UI

   eventually:

   specification + harness + evidence > particular model
   ```

3. The abstractions leak.

   Natural-language handoffs, implicit permissions, ambient filesystem access, unstructured judge output, context loss, and vague completion criteria are not small UX issues. They are signs that the programming abstraction for autonomous software engineering is still under-specified.

4. The stack needs typed boundaries.

   The loose loop:

   ```text
   prompt
     -> agent
     -> Markdown handoff
     -> agent
     -> tool
     -> side effects
   ```

   needs to evolve toward:

   ```text
   intent
     -> autoformalized specification
     -> typed policy
     -> typed agent handoffs
     -> typed/effect-aware execution
     -> compiler
     -> witness
   ```

5. Cedar matters, but Cedar is not the autoformalizer.

   Cedar answers an authorization question: may this principal perform this action on this resource in this context? It does not prove that the resulting program satisfied the user's semantic intent. That separation is essential.

6. Open source needs a sharper economic frame.

   The recurring framework for this series is:

   ```text
   Why Open?

   1. Common infrastructure
   2. Strategic collaboration
   3. Network effects
   ```

   These are not mutually exclusive. Internet standards, Linux, and LLVM each show different versions of shared infrastructure. LLVM also shows strategic collaboration and network effects at the compiler layer.

7. The series has three recurring threads.

   The writing program is not one flat list of posts. It has three threads that should be revisited quarterly: Open Ecosystem, Hybrid Analysis, and the Future of Software Engineering.

---

# Full Blog Draft

## 1. My development environment has collapsed to one window

My software development environment has collapsed to one window.

Not literally one process. Not one vendor. One working surface.

Zed is where I keep the code and the rhythm of editing. ACP and CLI workflows are where agents become operational instead of conversational. Codex, Claude Code, Cursor, and other coding agents are no longer separate curiosities. They are interchangeable participants in a single development loop. Around them are handoffs, review prompts, judge loops, repository state, tests, diffs, and the human decision to accept or reject a change.

That change is easy to describe as productivity. It is more useful to describe it as a pressure test on the abstractions of software engineering.

The old editor abstraction was simple enough:

```text
human edits file
human runs tool
human interprets result
human commits change
```

The new agentic abstraction is much messier:

```text
human states intent
agent reads repository
agent edits files
agent runs tools
agent interprets failures
agent summarizes evidence
another agent reviews the change
human accepts or rejects
```

That sounds like a workflow improvement until something goes wrong. Then the hidden questions appear:

- What did the agent believe it was allowed to do?
- Which files was it allowed to read?
- Which files was it allowed to write?
- Which tools could it run?
- Was network access part of the task or an ambient capability?
- What counts as completion?
- What is evidence, and who decides whether it is enough?
- If a second agent reviews the work, what exactly is it reviewing?

These are not chatbot questions. These are programming-language, operating-system, policy, compiler, and software-engineering questions appearing inside the daily developer workflow.

The point of this article is not that I have a finished answer. The point is that several developments that are usually discussed separately belong in the same conversation: agent harnesses, typed handoffs, autoformalization, Cedar policies, open compilers, MLIR-style intermediate representations, and evidence-bearing development workflows.

The question is:

```text
What should the programming abstraction for autonomous software engineering be?
```

## 2. The model is becoming interchangeable

The first surprise of using several strong coding agents is that the model becomes less sacred.

That does not mean model quality stops mattering. It matters enormously. A weak model inside a strong harness is still weak. But after some threshold, the developer's attention shifts. I care less about which branded chat box is open and more about whether the system around the model can preserve intent, constrain effects, collect evidence, and recover from failure.

The useful comparison is:

```text
agent UI
  vs.
workflow
```

An isolated agent UI can feel impressive. It can answer a hard question, write code, summarize a codebase, and produce a plausible plan. But repository-level software engineering is not just answer production. It is state transition under constraints.

The stronger object is:

```text
specification + harness + evidence
```

That object can survive model substitution. If the workflow has explicit intent, typed permissions, durable events, replayable commands, structured test output, and reviewable evidence, then the model can improve, regress, or be swapped without destroying the surrounding engineering discipline.

This is why I deliberately want agents to become interchangeable. A future where every developer workflow is locked to one opaque model UI is weaker than a future where models plug into shared harnesses, shared policies, shared evidence formats, and shared review structures.

In that world, the model is still powerful, but it is not the whole system.

## 3. Where the current abstraction leaks

The current abstraction leaks everywhere.

The normal workflow often looks like this:

```text
prompt
  -> agent
  -> Markdown handoff
  -> agent
  -> tool
  -> side effects
```

This is useful, but it is not a strong programming model.

The handoff is often natural language. The permissions are often implicit. Filesystem access is often ambient. Tool output is summarized in prose. Judge output is unstructured. Context can be lost during long work. The definition of completion is often a sentence like "make it done" or "fix the issue," even when the actual requirements are much sharper.

The failure mode is not only that the model hallucinates. The deeper failure mode is that the system has no first-class representation of the task's authority, obligations, effects, and evidence.

For a human developer, some of this informality is tolerable because organizational context fills in the gaps. Humans know that "refactor the parser" usually does not mean "change CI configuration, add a new dependency, edit unrelated packages, and fetch random code from the network." Agents do not share that implicit social boundary unless the harness makes it explicit.

The future abstraction needs to look more like this:

```text
intent
  -> autoformalized specification
  -> typed policy
  -> typed agent handoffs
  -> typed/effect-aware execution
  -> compiler
  -> witness
```

This does not mean every task becomes a theorem proving exercise. It means the system should progressively reduce ambiguity as work moves from human intent to executable side effects.

That is exactly what the compiler world already understands.

## 4. The open agentic software stack

The emerging stack has three open layers that solve different problems.

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
| Specs + invariants + capabilities                |
| Cedar policy                                     |
| Rust-native Cedar                                |
| planned Cedar <-> Mojo-native path               |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
| AGENT HARNESS                                    |
|                                                  |
| ACP / CLI                                        |
| Codex / Claude Code / Cursor                     |
| DeepSeek Harness / Cordis                        |
| typed handoffs + judge/reviewer graphs           |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
| COMPILER                                         |
|                                                  |
| Mojo                                             |
| LIT -> KGEN -> LLVM                              |
| future verification / policy dialects            |
+-------------------------+------------------------+
                          |
                          v
                  Executable system
                          |
                          v
                  Evidence / witness
```

Each layer answers a different question.

The formal intent and policy layer asks: what is the user actually authorizing, requiring, and forbidding?

The agent harness layer asks: how do models become actors with bounded tools, durable events, typed handoffs, and reviewable execution?

The compiler layer asks: how does ambiguous source-level work become progressively structured, checked, lowered, optimized, and executed?

The witness layer asks: what evidence remains after the system acts?

The important thing is that these layers should not collapse into one opaque product. If a model, harness, policy system, compiler, and evidence store are all fused into a black box, then the developer cannot inspect the boundary between intent, authority, execution, and proof. Open interfaces matter because the boundaries are where trust is built.

## 5. Cedar is policy, not autoformalization

Cedar is important in this picture, but the distinction has to be precise.

Cedar is not the autoformalizer.

The LLM or agent can perform autoformalization:

```text
natural-language intent
  -> LLM / agent
  -> Phi
```

where:

```text
Phi = <Pre, Post, Inv, Cap, Effects, Evidence>
```

Part of that formalized object can project into Cedar authorization policy:

```text
Cap(Phi) -> Cedar policy
```

But the full specification is larger than authorization.

Consider an informal request:

```text
Refactor the parser.
You may modify parser source and tests,
but do not change public APIs,
dependencies,
CI configuration,
or access the network.
```

That should become two different kinds of constraints.

First, semantic obligations:

```text
public_api(before) == public_api(after)
tests(after) == PASS
behavior(before) ~= behavior(after)
```

Second, authorization policy:

```text
permit(agent, Read, parser/**)
permit(agent, Write, parser/**)
permit(agent, Write, tests/**)

forbid(agent, Write, Cargo.toml)
forbid(agent, Write, .github/**)
forbid(agent, Network, *)
```

Cedar answers a specific question:

```text
May this principal perform this action on this resource in this context?
```

It does not prove:

```text
Did the resulting program satisfy the specification?
```

You need both.

This separation is not academic. If an agent is allowed to edit `parser/**` and `tests/**`, Cedar-style authorization can prevent it from writing `.github/**` or adding dependencies. But authorization alone cannot prove that the refactor preserved parser behavior, public APIs, or performance properties. That requires semantic checks, tests, traces, static analysis, dynamic analysis, or formal verification depending on the task.

Authorization constrains what the actor may do. Verification and validation judge what the actor actually produced.

## 6. Harnesses are becoming runtimes

Agent harnesses are becoming runtimes for software work.

That is why projects like DeepSeek Harness and Cordis are interesting. The important idea is not only "run another model." The interesting idea is composable agent infrastructure: tools, effects, coeffects, plugins, durable events, structured handoffs, and judge or reviewer graphs.

Once agents act on real repositories, the harness has to care about things that ordinary chat interfaces could ignore:

- capability boundaries,
- tool schemas,
- side effects,
- event logs,
- retry behavior,
- reviewer routing,
- handoff formats,
- evidence collection,
- recovery after interruption.

This is where the future starts to resemble a runtime system.

In a programming language, the runtime is not just where code happens to execute. It defines memory behavior, scheduling behavior, error behavior, IO behavior, and sometimes security behavior. Agent harnesses are moving in the same direction for software work. They define what an agent can observe, what it can mutate, how it calls tools, how its actions are logged, and how another actor can judge the result.

The present state is still rough. Much of the agent world is held together by Markdown, shell commands, human trust, and post-hoc summaries. But the direction is visible. Agentic software engineering needs harnesses that behave less like chat wrappers and more like typed execution environments.

## 7. Compilers already know how to reduce ambiguity

Compiler people have lived with a version of this problem for decades.

Programs do not remain ambiguous blobs all the way to execution. They progressively acquire structure and lose ambiguity:

```text
Source
  -> parsed structure
  -> typed representation
  -> semantic checks
  -> intermediate representation
  -> optimization / transformation
  -> lower-level IR
  -> machine code
```

For Mojo, the public story around the opened compiler/toolchain is especially relevant because the structure is explicit:

```text
Source -> LIT -> KGEN -> LLVM -> Machine
```

The exact details will evolve, but the conceptual lesson is stable. A serious systems language cannot treat code as undifferentiated text until the last moment. It needs source-level representation, semantic and lifetime checking, parametric IR, elaboration, lowering, and eventual execution.

AI coding agents create pressure to apply a similar idea above the code level.

Human intent should not remain an ambiguous natural-language blob until it becomes filesystem mutation. It should progressively acquire structure:

```text
intent
  -> candidate specification
  -> capabilities
  -> semantic obligations
  -> effect constraints
  -> typed handoff
  -> execution trace
  -> evidence packet
```

That is why autoformalization, policy languages, harnesses, and compilers belong in the same article. They are all trying to move work from ambiguity toward checked structure.

## 8. Why open?

The word "open" is not decoration in this series.

The technical thesis is:

```text
AI coding agents expose the weakness of today's loosely specified abstraction boundaries.
```

The economic thesis is:

```text
The infrastructure enabling better boundaries will often become open,
not because every participant shares the same ideology,
but because interoperability itself creates value.
```

The framework I want to use across this writing program is:

```text
Why Open?

1. Common infrastructure
   "This should be something everyone can build on."

2. Strategic collaboration
   "We benefit more by sharing this layer
    than by competing over it."

3. Network effects
   "The technology becomes more valuable
    when everyone can participate."
```

These categories overlap. That is a feature, not a defect. The point is not to classify every project with one label. The point is to ask which force is doing the work.

### Common infrastructure

Sometimes the value of a technology comes precisely from being available as shared infrastructure rather than being captured by one vendor.

The Internet is the strongest example at the protocol level. TCP/IP, DNS, HTTP, and related standards formed an open standards and protocol ecosystem. The Internet is not one open-source project, so it is better to describe it as common protocol infrastructure.

Linux is the canonical software example. The kernel became shared infrastructure that individuals, universities, cloud companies, chip companies, device manufacturers, and competitors could all improve while building very different systems above and around it.

LLVM is especially relevant here because it shows the same pattern at the compiler layer. A reusable, permissively licensed compiler infrastructure allowed languages, research projects, hardware vendors, and commercial products to share a huge body of compiler engineering instead of rebuilding everything independently.

### Strategic collaboration

Sometimes a company or ecosystem opens infrastructure because owning that layer is not where it captures the most value.

The useful phrase is:

```text
Companies open the layer where ecosystem growth is more valuable
than exclusivity, and capture value somewhere adjacent to it.
```

That can happen because shared development lowers cost. It can happen because several actors are behind a stronger incumbent. It can happen because a layer is important but non-core. It can happen because openness recruits developers and weakens lock-in somewhere else.

The pattern often looks like this:

```text
Company / ecosystem

OPEN:
  language
  compiler
  protocol
  model
  runtime
  framework
  interchange format

CAPTURE:
  hardware
  cloud
  inference
  distribution
  enterprise platform
  proprietary data
  hosted service
```

That is a stronger claim than "open source is good." It says openness can be strategically rational even for private actors.

### Network effects

Some technologies become more useful as more people participate.

A programming language that nobody else writes is weak. A compiler that nobody targets has limited leverage. An IR that no other tool understands is isolated. An agent protocol supported by one agent is barely a protocol. A policy language understood by one product is just configuration.

A simple conceptual model is:

```text
V(open layer) = f(implementations, users, tools, integrations, contributors)
```

This is not an empirical equation. It is a way of thinking.

Programming languages, compilers, protocols, and intermediate representations often become substantially more valuable when they are open because their value compounds with adoption, tooling, integrations, targets, and contributors.

Sometimes openness is a feature of the architecture, not a licensing decision.

For interoperability layers, closing the layer can destroy precisely the externalities that make it valuable.

LLVM is a good example of the three forces reinforcing each other:

```text
                         LLVM
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
   COMMON GOOD      COLLABORATION       NETWORK
   compiler         Apple, Google,      languages,
   infrastructure   NVIDIA, AMD,        targets,
                    Intel, etc.         tooling
```

The thesis becomes:

```text
Open ecosystems emerge when private actors discover that there is
more value in sharing a foundational layer than owning it exclusively.
Sometimes that begins as a public good, sometimes as strategic necessity,
and sometimes because the technology cannot achieve its full value
without a network. Often, all three forces eventually reinforce one another.
```

The future-of-software-engineering question is not merely "what will be open sourced?" It is:

```text
Which layers of the emerging AI software stack become common infrastructure,
which remain competitive,
and what economic or technical force determines that boundary?
```

## 9. Cedar-Mojo as open exploration

Cedar-Mojo fits this series naturally, but only if it is framed correctly.

The framing is shared semantics and open infrastructure, not ownership of a proprietary representation.

The right framing is simpler:

```text
As part of exploring this idea,
I am working on a native Cedar-Mojo implementation
that I plan to open source.
```

That gives the writing some skin in the game without changing the article into an announcement. I am not only saying that open compiler ecosystems, policy semantics, and agent harnesses are interesting. I am testing the intersection:

```text
Cedar authorization semantics
        |
        +--> Rust implementation
        |
        +--> native Mojo exploration
                 |
                 v
          Mojo / MLIR ecosystem
```

The reason to open that kind of work is not charity alone. It is that policy semantics become more valuable when multiple systems can speak them. An authorization language that only one runtime understands is configuration. A policy language with shared semantics across agents, services, compilers, and developer tools can become infrastructure.

The strategic consequence is:

```text
Open the semantics you want to become a standard.
```

This does not mean every implementation detail of every system should be open. It means interoperability layers deserve special treatment: policy schemas, witness formats, verification interfaces, typed handoff contracts, and compiler-facing semantics are candidates where broad adoption can be more valuable than private control.

## 10. Series map

This writing program has three recurring threads. They are independent enough to read separately, but they converge around the same problem: how software engineering changes when agents can act, compilers expose more structure, and evidence becomes central.

### Thread 1: Open Ecosystem

A 6-part opening series:

1. Leaky Abstractions vs. Type-Safe Abstractions in the Era of AI Coding Agents
2. Open Models and Model Interchangeability
3. Open Agent Harnesses, ACP/CLI, and Durable Handoffs
4. Open Compilers, Mojo, MLIR, and the Return of Typed Infrastructure
5. Open Policy, Formal Intent, Cedar, and Evidence
6. Why Open? Common Infrastructure, Strategic Collaboration, and Network Effects

This thread asks why foundational layers become open, which layers need interoperability to create value, and where economic value migrates after a layer becomes common infrastructure.

### Thread 2: Hybrid Analysis

A 3-part opening series:

1. Static vs. Dynamic Analysis Is the Wrong Final Frame
2. Verification vs. Validation in AI Software Engineering
3. Static + Dynamic, Verification + Validation: Hybrid Analysis for Agentic Software

This thread connects older hybrid program analysis work to the new problem of agents, generated code, runtime traces, tool calls, policies, and evidence.

### Thread 3: Future of Software Engineering

A 3-part opening series:

1. IDEs as Human Control Planes, CLI as the Durable Base
2. Agent Protocols, Handoffs, and Code Review When Agents Produce Most of the Patch
3. Languages for Verifiable AI Infrastructure

This thread is a quarterly field report on how the daily practice of software engineering changes as agents become normal participants in the development loop.

## 11. What this article claims, and what it does not claim

This article does not claim that one policy language solves software correctness.

It does not claim that one harness solves trust.

It does not claim that one compiler solves agentic software engineering.

It does not claim that open source always wins or that closed systems have no role.

The claim is narrower and stronger:

```text
AI coding agents expose a missing abstraction layer between human intent
and executable side effects.
```

The systems that fill that layer will need formal intent, authorization policy, semantic obligations, typed handoffs, effect-aware execution, compiler structure, and evidence.

Many of those pieces are likely to become open because they are interoperability layers. They become more valuable when multiple actors can implement them, inspect them, target them, and build around them.

That is why the open ecosystem and the future of software engineering belong in the same title.

The most important question is no longer:

```text
Which model writes the best patch?
```

It is:

```text
What stack lets humans specify intent,
bound authority,
run agents,
inspect effects,
and trust evidence?
```

That is the programming abstraction I want this series to explore.

## Source Anchors To Resolve Before Publication

- DeepSeek Harness and Cordis documentation for the agent-harness/runtime discussion.
- Modular and Mojo compiler/toolchain materials for LIT, KGEN, MLIR, LLVM, and open compiler structure.
- Cedar documentation and the Cedar implementation for authorization-policy semantics.
- Internet protocol history, Linux, and LLVM materials for the common-infrastructure examples.
- ACP/CLI and coding-agent documentation for the developer-workflow examples.

---

