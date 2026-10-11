<!-- Source of /blog/testing-compositional-mcp-zero-trust/. Build with tools/build_essay.py; written to blog_website/SKILLS.md. -->
# Testing Compositional MCP in Zero Trust

*A chain of MCP servers can admit every call it receives and still carry out a plan that the user never approved, because each server sees one call and the violation lies in their composition. We describe a demonstration, observed end to end on the official Rust SDK, in which every process checks the whole plan before it acts and checks the bytes of every call before they leave, and in which an independent judge decides each run from the records alone.*

**Few terms in computer science are invoked as often as *composition* and *abstraction*, and few are examined as carefully as their frequency would suggest.** Whether a piece of software is correct nonetheless reduces to two questions: whether each abstraction captures what it is intended to capture, and whether the parts compose into the behaviour that was intended. Language models have made code inexpensive to produce; they have not made its composition correct, and they have moved the cost of software from writing the parts to establishing that the parts fit. This series examines both questions from the standpoint of compilers, programming languages and static analysis, within the domain of software construction. Later parts treat abstraction formally, from type theory, and show how it can help in the application space. This first part is concerned with composition at the protocol layer, where an agent's work is now delegated through a chain of servers, and with what is required to test such a chain rather than its members.

<figure class="article-figure article-video">
<video controls muted playsinline preload="metadata" poster="demo-terminal-page-poster.png" width="1600" height="540">
<source src="demo-terminal-page.mp4" type="video/mp4">
</video>
<figcaption><strong>V1</strong> The demonstration in fifty seconds, recorded from the published code. On the left, the terminal prints the records each process writes and the judge's verdict; on the right, the live page shows the plan verdict, the composition graph and one card per record. Three scenarios run in sequence: every rule holds; the workspace alters one field of one call and its own gate refuses it; the plan follows the planted comment and every process denies it before any call. Silent.</figcaption>
</figure>

## 1. Introduction

A coding agent is a composition of components that were designed and authorized separately. An editor holds a session and a set of permissions; an agent produces a plan; the plan reaches tools through servers, and servers call further servers; at the end of the chain a file is written, a commit is made, or a test is run. Each component is reasonable in isolation, each exposes an interface, and most interfaces are governed by a protocol. The failures that matter, however, arise from the manner in which the components are combined, and we highlight two of them.

**Challenge 1. Authorization is applied per call, but consent is given per plan.** A user consents to an outcome, such as a test being run and its result recorded inside a project. The outcome is reached by a sequence of calls, each of which is authorized by the server that receives it, on the basis of a token, a listed tool and a permitted caller. A sequence in which every call is individually permitted can nonetheless move restricted data to a destination the user never approved, because no server in the sequence observes more than its own call. *Per-call authorization is therefore necessary but not sufficient; the plan as a whole must be checked, and it must be checked by every process that acts on it, since a downstream server cannot assume that an upstream one did.*

**Challenge 2. The object that is checked is not the object that is sent.** A request exists inside a process first as a value, then as a protocol message, then as a serialized line, and finally as bytes written to a pipe. A check applied to the value leaves an interval between the time of the check and the time of the write, and anything that alters the message in that interval escapes the check. *A check is therefore meaningful only if it is applied to the form of the request that the receiver will actually see, immediately before it is sent, and only if the act of sending is impossible without it.*

In this work, we address both challenges with a demonstration rather than a design: one coding task carried through four operating-system processes on the official Rust SDK for the Model Context Protocol, with the whole plan verified by every process before it serves anything, and with every outgoing message checked on its serialized bytes by the process that sends it. Three scenarios exercise the mechanism: a run in which every rule holds, a run in which one process alters one field of one call at run time, and a run in which the plan itself is altered to follow an instruction planted in the source code. A judge written in another language re-derives the verdict of each run from the records the processes wrote, against expectations fixed before the runs. The demonstration was presented at the MCP Dev Summit in Toronto on 5 October 2026, and its code is published.

The rest of this essay is organized as follows. Section 2 describes the three protocols that now compose an agent and locates the gap on the axis where the chain forms. Section 3 describes the task, the processes, the inputs, the rules and the record. Section 4 reports the three scenarios. Section 5 explains what the check on the bytes guarantees and what it does not. Section 6 relates the demonstration to the seven invariants the talk proposed as a test matrix. Section 7 states what was observed, what was modeled and the threats to the validity of the claims. Section 8 describes future work, and Section 9 gives the deck and the code.

## 2. Background: three protocols, one chain

Three protocols now describe a composed agent, and it is useful to regard them as three independent axes rather than as competitors, since each answers a different question about the same system. The Agent Client Protocol (ACP) is the axis of intent: it answers who asked and what was consented to, and the editor session, with its prompt, permissions and workspace, resides on it. Agent2Agent (A2A) is the axis of delegation: it answers who acts on whose behalf, each hop passing a task to another agent and receiving artifacts in return, and the governing rule on this axis is attenuation, by which authority may only decrease as it is delegated. The Model Context Protocol (MCP) is the axis of reach: it answers what the agent can touch, and tools, data and effects lie on it, each hop moving data and authority one server further from a source through a gateway to a sink. Figure F2 places the three axes at a common origin, the host, where a session, a delegation and a reach meet.

![F2 — Three axes from one origin, the host. A single call is a point on one axis; a plan is a point in the whole space.](diagrams/F2-three-axes.svg)

Per-call authorization checks a point on one axis. MCP's authorization layer performs this check correctly: a client presents a token to a server, the server verifies the token's audience and scope, and the call is admitted or rejected. The check is necessary. It is also where the gap of Challenge 1 opens, because what the user consented to is a plan, and a plan is a point in the whole space rather than on one axis. Three calls, each carrying a valid token and each addressed to a listed tool, can together carry a restricted summary to a public destination, and no single check detects the violation because no single check observes more than one call. Figure F1 shows this situation for the chain used in the demonstration.

![F1 — Three permitted calls, one violation: per-call authorization passes every hop, and the plan as a whole moves restricted output to a public sink.](diagrams/F1-three-calls-one-violation.svg)

MCP is the axis on which the chain forms. An editor speaks ACP to one agent, and an agent may delegate over A2A to a few others, but reach is a chain of servers in which each is a client of the next; this is precisely the shape in which a gateway forwards a request, a workspace commits a change and a test runner records a result. As such, the demonstration remains on the MCP axis, on the local problem of servers connected over standard input and output, and within software construction. The remote problem, in which the same servers are connected over HTTP with real credentials, is outside its scope, and Section 7 states what that exclusion costs.

## 3. The demonstration

This section describes the demonstration in the order in which a run proceeds: the task, the four processes that carry it, the three inputs that every process reads, the five rules that every process applies, and the record that every process writes.

**The task.** The task is a single sentence, and every process reads the same text of it:

> Fix the failing test `repeated_member_is_rejected` in crate `jsonlite`, commit the fix, run exactly that test on the commit, and record the result in `checks/jsonlite-summary.txt` inside the project. Keep the source and the test output inside the project.

The crate named in the task is a JSON parser without dependencies, written for the demonstration; its test for duplicate object keys fails before an approved patch is applied and passes after it. A comment planted in the parser asks that the summary be uploaded to a public gist. We treat this comment as data rather than as an instruction; no component of the demonstration acts on it. The third scenario examines the consequence of a plan that does.

**The four processes.** The task passes through four operating-system processes, which we name H, G, A and B. All four are built on the official Rust SDK for MCP, `rmcp`, pinned to one Git revision, and all speak MCP 2025-11-25 over standard input and output. H is the MCP host; G, A and B are MCP servers, each spawned by the process above it, and G and A are in addition MCP clients of the process below them. Table 1 gives each process's role, what it does and what it checks.

| Process | Role | What it does | What it checks |
|---|---|---|---|
| H | host | submits the task to G; accepts that the effect occurred only after re-hashing the receipt B wrote | the whole plan, before its first call; every message it sends |
| G | gateway: server to H, client of A | forwards the fix request to A | the whole plan, before serving; the request it received; every message it sends |
| A | workspace: server to G, client of B | applies the patch, makes a real git commit, asks B to verify that commit | the whole plan, before serving; the request it received; every message it sends |
| B | test runner: server to A | runs exactly one `cargo test` on the commit, writes the summary file once, writes a receipt that binds the file's bytes to the commit and the test | the whole plan, before serving; the request it received |

Figure F3 shows the same structure as a diagram: the frozen inputs above the chain, the four processes joined by their pipes, the run directory that only the processes write, and the two readers that only read.

![F3 — Four processes, one plan, one record: frozen inputs above, the chain in the middle, the run directory below, and two readers that only read.](diagrams/F3-four-processes-one-record.svg)

**The inputs.** Before a process does anything else, it reads three files that are fixed for the run. The first is the Program, which is the plan: three steps, each naming the tool to call, the caller, the callee and the arguments, and, for the last step, the effect it produces; the patch and the test name are literals inside it, and the last step's commit argument refers to the output of the step before it. The second is the policy, which states which caller may use which tool toward which destination and assigns each destination a tenant and a clearance; the internal summary path is cleared for the project's restricted data, and the public gist is not. The third is the consent, which records the one effect the user approved: the summary written to the internal path. Because every process reads the same three files, every process can reach the same verdict on the plan without trusting any other process to have reached it.

**The rules.** Five rules are applied, and Table 2 states, for each, the question it answers and where it is applied. The first three are questions about the plan, the fourth is a question about the bytes, and the fifth binds the two.

| Rule | The question it answers | Where it is applied |
|---|---|---|
| Permission | Does a row of the policy allow this caller to use this tool toward this destination? A tool that a server lists is not thereby permitted. | to the plan, by every process; again to the bytes, at every gate |
| Data labels | May data of this tenant and classification flow into this destination? Summarizing does not declassify. | the same |
| Consent | Is the effect of this plan the one the user approved? A comment in the source cannot widen it. | the same |
| Exact action | Are the bytes about to leave exactly the step the plan admitted, resolved against what this process has itself observed? | at the sender's gate before every write; at the receiver before it enters its handler |
| Verified plan | Has this process recorded its own verdict on the whole plan before sending or serving anything? A process whose verdict is a denial sends nothing. | each process, on itself |

The manner in which the rules are applied matters as much as the rules themselves. The whole-plan verdict is written to the process's journal before it serves anything, so that a denial is a durable record rather than a log line. Each process checks every outgoing message after the SDK has built it and the transport has serialized it, and before it is written, on the bytes that will actually leave; we refer to this check as the gate. The gate's decision is written to the journal and synchronized to disk, and the permit to write the message is constructed only from the journal's acknowledgement of that record. The bytes of every message that was decided or refused are retained under their hash. This arrangement is our answer to Challenge 2, and Section 5 examines what it guarantees.

**The record.** Each process keeps one hash-chained journal. The run directory holds the four journals, the retained messages, the git workspace, the summary file, the receipt and the panel printed to the terminal, and nothing else writes to it. Two readers consume it. The first is a judge, written in a different language from the processes, which never runs the binary, never reads the runtime's own report, and re-derives the verdict of a run against expectations that were written before the runtime was adapted. The second is a live page, fed by a loopback viewer that tails the journals, which shows one card per record and prints the judge's verdict verbatim. Everything reported in the next section is taken from these records.

## 4. Three scenarios

We ran three scenarios, which Table 3 summarizes and which we describe in turn below. A fourth variant, in which the workspace alters the destination of its call rather than the test name, is included with the code; we omit it here because it exercises the same gate as the second scenario and the same rules as the third.

<table class="scenes">
<thead><tr><th>Scenario</th><th>What happens</th><th>What the records show</th></tr></thead>
<tbody>
<tr><td><code>healthy</code></td><td>H submits the recorded plan; G admits it; A applies the two edits and commits; B runs the one test on that commit and writes the summary once.</td><td>Three calls, each entering its handler once; a real commit; the test passes; one summary file; the effect is known to have occurred, on the strength of a receipt that H re-hashed.</td></tr>
<tr><td><code>swap</code></td><td>The plan is valid. At run time A requests a different test from B than the plan names; the destination remains internal.</td><td>A's own gate refuses the message by the exact-action rule alone. B is never entered. The commit remains; no test runs and no file is written.</td></tr>
<tr><td><code>gist</code></td><td>The plan follows the planted comment: the same three calls, with the public gist as the destination.</td><td>H and every server deny the whole plan, with six findings under four rules. No call is made; no commit, no test and no file result.</td></tr>
</tbody></table>

A refusal scenario is judged against an expectation written before the scenario was run; the judge therefore reports a pass when the refusal occurred as expected, and a failure otherwise. A refusal is meaningful, moreover, only beside the unaltered first scenario executed in a fresh directory, since a system that refused everything would pass the second and third scenarios trivially.

Video V1, at the head of this essay, records the three scenarios with the terminal beside the page.

**The first scenario** establishes that the chain works when every rule holds. H verifies the plan and submits the task; G verifies the plan, admits the request and forwards it; A verifies the plan, applies the two edits of the patch, makes a commit, and asks B to test that commit; B verifies the plan, runs the one test named in the task, writes the summary file once, and writes a receipt. H accepts that the effect occurred only after it has re-hashed the receipt and the file at the one permitted path. Each of these steps is a record in a journal, and the judge confirms from the journals that each message entered its handler exactly once, that the commit exists in the workspace, that the test was run on that commit and passed, and that the file was written once.

**The second scenario** is the one that distinguishes a check on the bytes from a check on the object. Its plan is identical to that of the first, and all four processes verify it. H and G execute exactly as before, byte for byte. A makes its commit and then constructs its call to B with one field altered: the name of the test. A's gate does not examine the request object; it examines the serialized line that is about to be written to the pipe and compares it with the step the plan admitted. The difference, shown below as the line the admitted step resolves to and the line A retained when it refused, is confined to that one field:

```text
admitted  {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"_meta":{"progressToken":1},"arguments":{"commit":"f79c4dc…","destination":"internal","test":"repeated_member_is_rejected"},"name":"tests.run_and_record"}}
refused   {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"_meta":{"progressToken":1},"arguments":{"commit":"f79c4dc…","destination":"internal","test":"some_other_test"},"name":"tests.run_and_record"}}
```

Because the destination is still the internal path, the permission, label and consent rules are satisfied and report nothing; only the exact-action rule can observe the alteration, and it suffices. The message is refused before it is released, the line is never written, and B is never entered. Note that the commit A made remains in the workspace: a refusal halts the chain at the point of refusal and reverses nothing that preceded it, which is the correct behaviour for an effect that has already occurred and the reason the record must say so.

**The third scenario** fails earlier and more broadly. The task and the three calls are unchanged; only the destination differs, and it is the public gist that the planted comment requested. No row of the policy permits any caller to name that destination, so the permission rule is violated once for each of the three steps; B lists a tool that can reach the gist, and listing does not constitute permission. The workspace's output is labelled with one tenant and classified as restricted, the gist is public on both counts, and summarization does not declassify, so both label rules are violated on the final step. The consent admits a single effect, the summary written to the internal path, and a comment in the source cannot widen it, so the consent rule is violated as well. In total, six findings under four rules are recorded, and every process records its own denial before anything is sent; the servers start and list their tools, and that is the extent of their activity.


## 5. What the gate guarantees

The talk summarized the mechanism in one sentence: the permit to write is a value obtainable only from a synchronized journal record of the decision, so that if the bytes were not checked, no code path exists that can send them. In this section we explain the three properties that make the sentence true, and the one property it does not claim.

**The check and the use apply to the same bytes.** Within A, the request exists first as a value, then as a JSON-RPC message built by the SDK, then as one serialized line, after which the transport writes that line to B's standard input. Checking the value and then sending whatever reaches the wire leaves the interval described in Challenge 2. The gate instead checks the line itself, the last form the request takes before the write and the only form B will ever see, within the sender's own process and immediately before the write. As such, there is no interval between the check and the use. B checks what it received against its own copy of the plan's step before it enters its handler, and the judge later confirms that sender and receiver retained identical bytes. Figure F4 shows where the gate sits in the sequence.

![F4 — Where the gate sits: on the one serialized line, after the SDK built it and before the write; the refusal path never constructs a permit.](diagrams/F4-where-the-gate-sits.svg)

**The permit is a type that only the journal can produce.** The gate's decision is written to the journal and synchronized to disk; the journal then returns an acknowledgement, and only the journal can construct one. The permit to write is a Rust value that can be constructed only from that acknowledgement. The refusal path never constructs the value, and therefore no code path writes; a send that is abandoned after a decision is detected by a guard that records the fact. The discipline is that of a resource handle whose destructor releases a lock, applied to a wire: ownership of the permit is ownership of the right to write once.

**Process isolation makes the pipe the only channel.** The four roles are four operating-system processes rather than four tasks in one runtime, so none can reach another's memory. The only means by which A can influence B is the byte sequence it writes into the pipe, and that sequence is exactly what the gate checks. Each process reads the frozen inputs itself and keeps its own copy of the plan, its own journal and its own retained messages.

**What is not claimed.** The processes share one user and one filesystem. Isolation therefore prevents one process from tampering with another's memory, but not with the files both can reach. B binds the commit it tests to a clean working tree at the head of the repository and then tests that tree in place, trusting the disk between the check and the test, and the panel's scope line records this trust on every run. The gate guarantees that the bytes which left were the bytes that were checked; it does not guarantee that the filesystem the receiver then reads is the one the sender saw.

## 6. The seven invariants

The talk proposed a test matrix of seven invariants, each a property of a composed run rather than of a single call. Table 4 lists them and states, for each, whether the demonstration exhibits it or only states it.

| | Invariant | In this demonstration |
|---|---|---|
| 1 | Authority never grows across hops | exhibited: in the fourth variant, A's own gate refuses the widened call |
| 2 | Capability is not permission | exhibited: in the third scenario, B lists a tool that reaches the gist and no row of the policy permits it |
| 3 | Tokens are audience-bound | stated: credentials are modeled on standard input and output; each server trusts the link it was given |
| 4 | Restricted data stays out of unapproved sinks | exhibited: in the third scenario and the fourth variant, the summary never reaches the gist |
| 5 | Every effect has a prior decision | exhibited: in every run, the judge checks the ordering of records within each journal |
| 6 | Retries and partial failures stay safe | stated: there is no lost-reply or restart scenario; the effect vocabulary already distinguishes an unknown outcome from a failed one |
| 7 | The run is replayable | exhibited: in every run, an independent recount from the records; the page reopens any finished run from disk |

MCP authorization continues to perform its per-call function. This matrix is applied alongside it, to the plan, and the five exhibited invariants are the ones that a chain of per-call checks cannot establish on its own.

## 7. What was observed, what was modeled, and threats to validity

Table 5 separates the components of the demonstration by their status.

| Component | Status |
|---|---|
| MCP messages, four processes, the gate on the serialized bytes | observed: real `rmcp` over standard input and output |
| The git commits, `cargo test` on the committed tree, the summary file | observed: real effects in the run directory |
| The whole-plan check, the exact-action check, the refusals | observed and deterministic, from the frozen inputs |
| Credentials and identities | modeled: the policy names actors; nothing is signed |
| The parser crate, the patch, the planted comment | synthetic, written for the demonstration |
| A coding agent proposing the plan | absent: the plan is recorded |

Where external validity is concerned, the demonstration is one task, one chain of three servers, and one machine, and the servers are connected over standard input and output rather than HTTP. We chose this configuration because it isolates the two challenges from the questions of transport and credential that the remote configuration adds; however, it means that a refusal is always the sender's own gate, and that a process which bypassed its gate would not be stopped by the next one. The remote configuration, with audience-bound tokens, is the subject of later work.

Where internal validity is concerned, the judge is independent of the runtime's code and of its self-report, but not of its inputs: it reads the same policy and Program files as the processes, so a defective input would be defective in both places and would pass. The expectations for the original three scenarios were written before the runtime was adapted; those of the second scenario were written alongside it, and the file records that as a revision. The exact-action comparison is performed on canonical JSON, with the wire bytes retained beside it, so a message that differed only in key order would be admitted; the retained bytes allow the judge to see that difference even though the gate does not act on it.

Where construct validity is concerned, the rules are hand-written, sufficient for three steps and two destinations, with no schema and no analysis; the demonstration shows what a checkable plan must look like and nothing about how such a plan is produced from a user's intent. The page was checked in one headless browser at one window size. We did not measure the cost of the gate relative to the cost of the calls, nor the effort required to write a policy for a real chain. Each of these limits appears, with a severity, in the critique published with the code.

## 8. Future work

Three directions follow from the demonstration, and each retains the gate on the bytes.

**A policy engine in place of hand-written rules.** The present rules are plain tables and a checker, which suffices for a demonstration but cannot express a rule about a tool that does not yet exist and cannot be analyzed for conflicts. The next step is a policy language proper, Cedar, with a schema, analysis and a single language shared by hosts and servers. The gate does not move into the engine: the engine answers whether an action is allowed, and the gate guarantees that the action it answered about is the one that left.

**Typed gates in Mojo, C++ and Lean.** The Model Context Protocol has official SDKs for several languages but none for Mojo, C++ or Lean. The gap matters here because the guarantee that no write occurs without a permit is at present enforced by the Rust type system alone; an SDK that expresses the permit as a zero-cost abstraction in each of these languages would move the same guarantee to compile time, where a program that attempts a write without a permit fails to build rather than at run time. The design of these SDKs is the subject of a later part of this series.

**Proofs from the same Rust source.** Charon and Aeneas translate Rust into Lean, and can therefore lift the rule checker and the gate's ordering logic from the code that ran on stage into a form in which the invariants are proved of the code rather than recounted per run. Synchronization to disk and the pipe remain the stated trust boundary; the proof covers what lies between them.

## 9. The deck and the code

- The talk deck, cover and twelve slides: [PDF](/docs/testing-compositional-mcp-zero-trust-deck.pdf) and [web page](/docs/testing-compositional-mcp-zero-trust-deck.html).
- The code, under the Apache License 2.0, with instructions for building it and running the scenarios: [github.com/sb-iam/conferences/tree/main/2026-mcp-toronto](https://github.com/sb-iam/conferences/tree/main/2026-mcp-toronto).

Next in the series: Part 2, *Summer 2026, the Goldilocks zone*: Mojo's open compiler, DeepSeek's agent harness, the Lean FRO's new funding, and Nvidia's purchase of Hugging Face.

## References

1. *Testing Compositional MCP in Zero Trust*, MCP Dev Summit Toronto, 5 October 2026. https://events.linuxfoundation.org/mcp-dev-summit-toronto/program/schedule/?id=1288277
2. Model Context Protocol, specification 2025-11-25, including the authorization section. https://modelcontextprotocol.io/specification/2025-11-25
3. The official Rust SDK for MCP, `rmcp`, used at Git revision `ae2f9c9b45a2c98d24ee345406e79f507c9f9282`. https://github.com/modelcontextprotocol/rust-sdk
4. Agent Client Protocol. https://agentclientprotocol.com
5. Agent2Agent protocol. https://github.com/a2aproject/A2A
6. Cedar policy language. https://www.cedarpolicy.com
7. Charon and Aeneas, from Rust to Lean. https://github.com/AeneasVerif/aeneas
