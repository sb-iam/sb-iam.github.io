# Research Statement: archived figures

Archived from `research-statement/index.html` on 2026-10-13, when the second
figure of the page returned to the VerifyD architecture: the Rust control
plane, the Virtual Graph Loader and the Mojo data plane. Kept here to be
revisited. Each figure is as it last appeared on the page, and none of them
describes the current design; the Research Statement does. The ink and the
background of the page's light theme are set on the root element of each file
so that it can be opened by itself.

| File | Caption on the page | Replaced by |
|---|---|---|
| [f2-jitac-one-loader-four-kinds-of-unit.svg](f2-jitac-one-loader-four-kinds-of-unit.svg) | **F2** The design of JITAC. Static analysis and the running program both require units of code; the virtual incremental loader serves both, extends one graph, and loads four kinds of unit, one for each level above the ABI. The gold nodes of the graph are a unit added after analysis began. | the figure of the four languages and the FFI, below |
| [f3-four-first-class-languages.svg](f3-four-first-class-languages.svg) | **F3** The first-class languages of this research and the task of each with respect to an abstraction. | the same figure |
| [f2-jitac-four-languages-ffi.svg](f2-jitac-four-languages-ffi.svg) | **F2** The design of JITAC. Each language is loaded in units of its own kind. An edge stands for the foreign calls of one language, which the virtual incremental loader joins to their definitions in one graph. | the figure now on the page |

## 2026-10-13: proposed VerifyD system in Mojo

The Research Statement now presents the owner-approved broader VerifyD design
with JITAC and Nabla-Mojo. The earlier Rust-control/Mojo-data figure is preserved
below. The introduction and replacement descriptions above record the earlier
archiving event; the Research Statement remains the current design.

| File | Caption on the page | Replaced by |
|---|---|---|
| [f2-verifyd-rust-control-mojo-data.svg](f2-verifyd-rust-control-mojo-data.svg) | **F2** The VerifyD platform architecture. Rust controls, Mojo computes, and the Virtual Graph Loader connects them: it holds the typed program graph, binds evidence and identity to it, loads program context on demand, and seals the snapshot a change was evaluated against. It plays the role the System classloader plays in **F1**, one rung up. Evidence returns to the control plane; the authority to admit a change never leaves it. | the proposed VerifyD system in Mojo, with JITAC between developer tools and model computation |

## 2026-10-13: JITAC with a Rust control plane and a Mojo data plane

The second figure of the Research Statement now shows the architecture of JITAC
in the layout of the earlier VerifyD figure. The figure of the proposed VerifyD
system in Mojo is preserved below. The two sections above record the earlier
archiving events; the Research Statement remains the current design.

| File | Caption on the page | Replaced by |
|---|---|---|
| [f2-verifyd-proposed-system-in-mojo.svg](f2-verifyd-proposed-system-in-mojo.svg) | **F2** The proposed VerifyD architecture places JITAC’s incremental program representations between developer tools and model computation. Results and runtime observations inform subsequent analysis. | the architecture of JITAC: the Rust control plane, the virtual incremental graph loader and the Mojo data plane |
