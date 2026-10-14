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
