<!-- Source of /blog/testing-compositional-mcp-zero-trust/. Build with tools/build_essay.py; see docs in that file. -->
# Testing Compositional MCP in Zero Trust

*Every call was allowed. The chain was not. One coding task through four processes, three scenarios, and a judge that trusts only what the processes wrote.*

**Ten years from now, software will still be made of abstractions and compositions, and both will still have to be right.** Jeff Bezos used to say that he was asked constantly what would change in the next ten years and almost never what would not change, and that the second question was the more useful one, because a strategy can be built on what stays still. Ask it about programming and the answer is not a language or a model. Code has become cheap to produce. The cost has moved to the two questions that were always the hard ones: is this abstraction the right one, and does this composition of parts do what the person asked for. This series looks at both from one point of view, that of compilers, programming languages and static analysis, and in one domain only, the writing of code. This first essay is about composition at the protocol layer, where an agent's work is now chained through servers, and about what it takes to test the chain rather than its parts.

## 1. The question that will still be there

A coding agent today is a composition. An editor holds a session and a set of permissions; an agent plans; the plan reaches tools through servers; servers call other servers; somewhere at the end a file is written, a commit is made, a test runs. Each piece is reasonable on its own. Each piece has an interface, and most of the interfaces have a protocol. The failures that matter are not in the pieces. They are in the way the pieces are put together: a call that is permitted at every hop and still moves restricted data to a place the person never approved; a tool that is listed and therefore assumed to be allowed; an effect that happens before the decision that was supposed to precede it.

The talk this essay comes from, at the MCP Dev Summit in Toronto on 5 October 2026, made one claim and showed one demo for it: test the whole flow, not just the building blocks. The demo is small on purpose, one task and four processes, and it is observed end to end on the official Rust SDK, not drawn. Everything below is in the published code, and every number comes from its own check file.

## 2. The gap: every call allowed, the chain not

Three protocols now describe a composed agent, and it helps to see them as three independent axes rather than three competitors. The Agent Client Protocol, ACP, is the axis of intent: who asked, and what was consented. The editor session lives here, with the prompt, the permissions and the workspace. Agent2Agent, A2A, is the axis of delegation: who acts for whom. Each hop hands a task to another agent and receives artifacts back, and the rule on this axis is attenuation; authority can only shrink. The Model Context Protocol, MCP, is the axis of reach: what the agent can touch. Tools, data and effects; each hop moves data and authority one server further, from a source through a gateway to a sink.

![F2 — Three axes from one origin, the host. A single call is a point on one axis. A plan is a point in the whole space.](diagrams/F2-three-axes.svg)

Per-call authorization checks a point on one axis. MCP's authorization layer does this well: a client presents a token for a server, the server checks its audience and scope, the call is allowed or not. That is necessary. It is also where the gap opens, because the thing a person consented to is a plan, and a plan is a point in the whole space. Three calls, each with a valid token, each to a tool that is listed, can together carry a restricted summary to a public destination. No single check sees it, because no single check sees more than one call.

![F1 — Three permitted calls, one violation: per-call authorization passes every hop, and the plan as a whole moves restricted output to a public sink.](diagrams/F1-three-calls-one-violation.svg)

MCP is where the chain happens. An editor speaks ACP to one agent; an agent may delegate over A2A to a few; but reach is a chain of servers, each one a client of the next, and that is exactly the shape in which a gateway forwards, a workspace commits and a test runner writes. So the demo stays on the MCP axis, on the local problem, in the coding domain.

## 3. The demo: one task, four processes

The task is one sentence, and it is the text every process reads:

> Fix the failing test `repeated_member_is_rejected` in crate `jsonlite`, commit the fix, run exactly that test on the commit, and record the result in `checks/jsonlite-summary.txt` inside the project. Keep the source and the test output inside the project.

The crate is a small dependency-free JSON parser whose duplicate-key test fails before the approved patch and passes after it. A comment planted in its parser asks for the summary to be uploaded to a public gist. The comment is data; nothing in the demo reads it as an instruction, and one of the scenarios is what happens when a plan does.

Four operating-system processes carry the task, all on the official Rust MCP SDK, `rmcp`, pinned at one Git revision, speaking MCP 2025-11-25 over stdio. H is the MCP host: it checks the plan, submits the one task, and later re-hashes a receipt before it believes anything happened. G, A and B are three MCP servers over stdio, each spawned by the process before it: G is a gateway that serves `submit_fix` to H and forwards it to A through its own gate; A is a workspace that applies the patch and makes a real git commit, then asks B to verify that commit; B is a test runner that runs exactly one `cargo test` on that commit, writes the summary file once, and writes a receipt binding the file's bytes to the commit and the test. G and A are also MCP clients of the next server down. That is the composition.

![F3 — Four processes, one plan, one record: frozen inputs above, the chain in the middle, the run directory below, and two readers that only read.](diagrams/F3-four-processes-one-record.svg)

Three things are the same in every process.

**The whole plan is checked before anything runs.** The plan is a Program with three nodes: tool, caller, callee, arguments, and for the last node an effect. The patch and the test name are literals inside it; B's commit argument refers to the output A will produce. H checks the Program before its first call, and every server checks it before it serves anything, each against the same frozen policy and the same frozen consent, and each records its own verdict durably. A denied process serves nothing. The rules are small: a policy row must exist for caller, tool and destination; the labels on the data must be allowed to flow into the sink; the admitted intent must cover the one effect; and the policy, not the proposal, decides which node is an effect node.

**Every outgoing frame is gated on its exact bytes.** The SDK builds the message, the transport serializes it once, and that buffer is what the gate decides on. It must equal the admitted node resolved against the inputs this process observed, and the node's rules run again on the actual bytes. The decision is a durable journal record, synced before anything depends on it; the permit to write is built only from the journal's acknowledgement; and the bytes of every decided or refused frame are retained under their hash.

**Everything is written down.** Each process keeps one hash-chained journal. The run directory holds the four journals, the retained frames, the git workspace, the summary file, the receipt and the panel the terminal printed. Nothing else writes there. Two readers read it: a judge, written in another language, that never runs the binary, never reads the runtime's own report, and re-derives the verdict against expectations that were frozen before the runtime was adapted; and a live page, fed by a loopback viewer that tails the journals, shows one card per record, and prints the judge's line verbatim.

## 4. Three scenarios

One script runs the three scenarios in a row, with Enter between them. A fourth is in the code for questions.

| Scene | What happens | What the records show | Judge |
|---|---|---|---|
| `healthy` | H submits the recorded plan; G admits it; A applies the two edits and commits; B runs the one test on that commit and writes the summary once | 3 business calls, 21 frames gated, one handler entry each, a real commit, `1 passed, 0 failed`, one file, effect `known_applied` from a receipt H re-hashed | PASS, 211 checks |
| `swap` | The plan is fine; at run time A asks B for a different test than the plan names; the destination is still internal | A's own gate refuses the exact bytes with one finding, `EXACT_ACTION_MISMATCH`; 2 business calls, 1 refusal; B never entered; the commit stays, no test, no file | PASS, 178 checks |
| `gist` | The plan follows the planted comment: the same three calls, with the public gist as the destination | H and every server deny the whole plan with six findings under four names; 15 handshake frames gated, 0 business calls; no commit, no test, no file | PASS, 124 checks |
| `substitute` | The plan is fine; at run time A changes its child's destination to the public gist | A's gate refuses with five findings; B never entered; the commit stays, no file | PASS, 179 checks |

The judge passes a refusal scene because the refusal is the frozen expectation, and a refusal only counts beside the unchanged `healthy` run in a fresh directory.

The second scenario is the one to read slowly. Its plan is identical to the pass, and all four processes verified it. H and G run exactly as before, byte for byte. A makes its commit, then builds its call to B with one field changed. Its gate does not look at a request object; it looks at the serialized line about to go on the wire and compares it with the node it admitted. This is the whole difference: the line the admitted node resolves to, and the line A retained under its hash when it refused:

```text
admitted  {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"_meta":{"progressToken":1},"arguments":{"commit":"f79c4dc…","destination":"internal","test":"repeated_member_is_rejected"},"name":"tests.run_and_record"}}
refused   {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"_meta":{"progressToken":1},"arguments":{"commit":"f79c4dc…","destination":"internal","test":"some_other_test"},"name":"tests.run_and_record"}}
```

The destination is still internal, so the consent, capability and label rules all hold and have nothing to say. Only the exact-action rule can see this, and it is enough: refused before release, the line never written, B never entered. The commit A made stays in the workspace, because a refusal stops the chain where it is and undoes nothing before it.

The third scenario fails earlier and wider. Same task, same three calls, one word changed: the destination is the public gist, as the planted comment asked. No policy row lets any caller ask for that destination, so `CAPABILITY_WITHOUT_PERMISSION` fires once per node, three times; B lists a gist tool, and listing is not permission. The workspace's output is labelled for one tenant and classified restricted, the gist is public on both counts, and summarizing does not declassify: `LABEL_TENANT` and `LABEL_CLASSIFICATION` fire on the sink node. The consent admits one effect, the summary to the internal path, and a comment in the code cannot widen it: `CONSENT_SCOPE_MISMATCH`. Six findings, four names, and every process records its own denial before anything is sent; the servers come up and list their tools, and that is all they ever do.

<figure class="article-figure article-video">
<video controls muted playsinline preload="metadata" poster="demo-poster.png" width="1200" height="750">
<source src="demo.mp4" type="video/mp4">
</video>
<figcaption><strong>V1</strong> The live page during the three scenarios, recorded from the published code: <code>healthy</code> passes and the graph turns blue hop by hop; <code>swap</code> is refused at the workspace's gate by one rule and the A to B hop turns red; <code>gist</code> is denied by every process before any call, every node is marked denied and no hop is released. The verdict line on the page is the judge's. Silent, 50 seconds.</figcaption>
</figure>

## 5. What "bytes leave" means

The talk's one-liner was that the permit to write is a value you can only get from a synced journal record of the decision, so if the bytes were not checked there is no code path that can send them. Three ideas sit under that sentence.

**The time-of-check gap.** Inside A, the request exists as a struct, then as a JSON-RPC message, then as one serialized line, and then `write_all` puts that line into B's stdin. Checking the struct and then sending whatever ends up on the wire leaves a gap between the time of check and the time of use, and everything that touches the message in between is inside it. The gate checks the line, the last form before the write and the only form B will ever see, in the sender's own process, right before the write. Check and use are the same bytes. B checks what it received against its own copy of the plan node before it enters its handler, and the judge later confirms that sender and receiver retained identical bytes.

![F4 — Where the gate sits: on the one serialized line, after the SDK built it and before the write; the refusal path never constructs a permit.](diagrams/F4-where-the-gate-sits.svg)

**The permit is a type the journal makes.** The gate's decision is written to the journal and synced; the journal then hands back an acknowledgement, and only the journal can construct one. The permit to write is a Rust value that can only be built from that acknowledgement. The refusal path never constructs the value, so there is no code path that writes; a send that is dropped after a decision is caught by a guard that records it. This is the same discipline as a resource handle whose destructor releases the lock, applied to a wire: ownership of the permit is ownership of the right to write once.

**Process isolation is the boundary.** The four roles are four operating-system processes, not four tasks in one runtime, so one cannot reach another's memory. The only way A can influence B is the byte sequence it writes into the pipe, and that is exactly what the gate checks. Each process reads the frozen inputs itself and keeps its own copy of the plan, its own journal and its own retained frames. The honest limit is on the same page: they share one user and one filesystem, so isolation stops memory tampering, not filesystem tampering. B binds the commit to a clean tree at HEAD and then tests that tree in place, trusting the disk, and the panel's scope line says so on every run.

## 6. The seven invariants

The talk's abstract promised a zero-trust test matrix. It is seven properties of a composed run, none of them a property of one call. The demo shows five directly and is explicit about the other two.

| | Invariant | In this demo |
|---|---|---|
| 1 | Authority never grows across hops | shown: `substitute`, A's own gate refuses the widened call |
| 2 | Capability is not permission | shown: `gist`, B lists a gist tool and no policy row permits it |
| 3 | Tokens are audience-bound | stated only: credentials are modeled on stdio; each server trusts the link it was given |
| 4 | Restricted data stays out of unapproved sinks | shown: `gist` and `substitute`, the summary never reaches the gist |
| 5 | Every effect has a prior decision | shown: every run, the judge checks the order inside each journal |
| 6 | Retries and partial failures stay safe | stated only: no lost-reply or restart scene; the effect vocabulary already says `unknown` rather than `failed` |
| 7 | The run is replayable | shown: every run, an independent recount from the records; the page reopens any finished run from disk |

MCP authorization still does its job per call. This matrix sits beside it, on the plan.

## 7. What was observed, what was modeled

| Part | Status |
|---|---|
| MCP messages, four processes, the gate on the serialized bytes | observed: real `rmcp` over stdio |
| The git commits, `cargo test` on the committed tree, the summary file | observed: real effects in the run directory |
| The whole-plan check, the exact-action check, the refusals | observed, deterministic, from the frozen fixtures |
| Credentials, identities | modeled: the policy table names actors; nothing is signed |
| The fixture crate, the patch, the planted comment | synthetic fixtures |
| A coding agent proposing the plan | not here: the plan is recorded |

The limits, as the code states them. No HTTP, no token, no TLS: a refusal is the sender's own gate, and a process that bypassed its gate would not be stopped by the next one. One machine, one author, no lost-reply or restart scene. The judge is independent of the runtime's code and of its self-report, not of its inputs: it reads the same policy and Program files, so a wrong fixture would be wrong in both places and pass. The rules are small and hand-written, enough for three nodes and two sinks, with no schema and no analysis. The expectations for the original three scenes were frozen before the runtime was adapted; the `swap` scene's were written with it, and the file records that as a revision. The exact-action comparison is on canonical JSON, with the wire bytes retained beside it. The page was checked in one headless browser at one window size, 67 checks, as part of the same check that runs the four scenes and a leak scan. Each of these is a line in the published critique, with a severity.

## 8. What comes next

Three directions, all keeping the same gate on the bytes.

**A policy engine instead of hand-written rules.** The rules today are plain tables and a small checker, which was right for a demo. The next step is a real policy language, Cedar, with a schema, analysis and one language across hosts and servers. What does not move into the engine is the gate: the engine answers whether an action is allowed; the gate guarantees that the action it answered about is the one that left.

**Typed gates in Mojo, C++ and Lean.** The permit-from-acknowledgement discipline is a type in Rust today. Small MCP SDKs for Mojo, C++ and Lean can carry the same discipline as zero-cost abstractions, so that no permit means no write, checked when the code is compiled rather than when it runs. Those SDKs are missing for MCP, and they are the subject of a later essay in this series.

**Proofs from the same Rust source.** Charon and Aeneas can lift the rule checker and the gate's ordering logic from the Rust that ran on stage into Lean, so the invariants are proved about the code rather than recounted per run. The sync to disk and the pipe remain the stated trust boundary; the proof covers what sits between them.

## 9. The deck and the code

- The talk deck, cover and twelve slides, as [PDF](/docs/testing-compositional-mcp-zero-trust-deck.pdf) and as a [web page](/docs/testing-compositional-mcp-zero-trust-deck.html).
- The code, under the Apache License 2.0: [github.com/sb-iam/conferences/tree/main/2026-mcp-toronto](https://github.com/sb-iam/conferences/tree/main/2026-mcp-toronto). With Rust 1.91 through rustup, `git` and Python 3.9 or later: `./demo build`, then `./demo talk` for the three scenarios with the live page, or `./demo check` for all four scenes, the leak scan and the page check, which writes the check file the numbers above come from.

Next in the series: Part 2, *Summer 2026*, composition and abstraction from the process and incentive side, on Oct 15, 2026; then Part 3, the gang of four, Rust, Mojo, C++ and Lean, on Oct 18, 2026.

## References

1. *Testing Compositional MCP in Zero Trust*, MCP Dev Summit Toronto, 5 October 2026. https://events.linuxfoundation.org/mcp-dev-summit-toronto/program/schedule/?id=1288277
2. Model Context Protocol, specification 2025-11-25, including the authorization section. https://modelcontextprotocol.io/specification/2025-11-25
3. The official Rust SDK for MCP, `rmcp`, used at Git revision `ae2f9c9b45a2c98d24ee345406e79f507c9f9282`. https://github.com/modelcontextprotocol/rust-sdk
4. Agent Client Protocol. https://agentclientprotocol.com
5. Agent2Agent protocol. https://github.com/a2aproject/A2A
6. Cedar policy language. https://www.cedarpolicy.com
7. Charon and Aeneas, from Rust to Lean. https://github.com/AeneasVerif/aeneas
8. Jeff Bezos on the question that does not change, AWS re:Invent fireside chat with Werner Vogels, November 2012.
