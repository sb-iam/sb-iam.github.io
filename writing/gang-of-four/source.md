<!-- Source of /blog/gang-of-four/. Build with tools/build_essay.py; written to blog_website/SKILLS.md. Unpublished draft of Part 3, planned for Oct 18, 2026. Facts refreshed on 14 October 2026; the toolchains of the four-compiler study are listed under References. -->
# Gang of four: C++, Lean, Mojo and Rust

*C++, Lean, Mojo and Rust are the first-class languages of our research. All four let a compiler run part of a program before the program runs, and they differ in when they check generic code, what form of it they keep, and what their compile-time code may do. We examine each language, the interfaces that join them, and what each can establish about software that runs on a phone, a workstation and a cloud.*

**[Part 2](/blog/golden-era-open-ecosystem/) described Mojo's parameters as compile-time metaprogramming of the same kind as Rust's procedural macros; the description holds for the problem but not for the mechanism.** A procedural macro is a compiled Rust program that rewrites tokens before any type exists, whereas a Mojo parameter is a typed value that the compiler evaluates while it specializes generic code. Both let a compiler run part of a program before the program runs, a problem shared by the four languages that are first-class in our research: C++, Lean, Mojo and Rust. Their mechanisms differ, and the differences decide where an error appears, which representation an analysis must read, and what a tool can establish.

The rest of this essay is organized as follows. Section 1 defines the two classes of language, Section 2 examines the four in turn, and Section 3 compares their metaprogramming. Section 4 describes the connections among them, Section 5 their place in verification, validation and execution, and Section 6 what remains difficult.

## 1. First-class and second-class languages

The distinction describes the position of a language in our research, not its quality. A first-class language is one in which we write abstractions by hand and whose compiler holds the program in a representation that an analysis can read: C++ through Clang and LLVM, Rust through its mid-level intermediate representation (MIR), Mojo through MLIR, and Lean through the terms that its kernel checks. A second-class language, such as TypeScript, Python, Go, Kotlin or Java, is one in which we do not write the first layer of a system; its code is generated from definitions in the four. As such, an abstraction and its analysis reside in one place, and generated code inherits the structure of the abstraction but not its proofs, since a generator and a second compiler stand between them.

Most applications are written in the second-class languages, which offer the better developer experience, from TypeScript's checker in the editor to Python's libraries for machine learning. A higher-level language is not, however, easier to analyze. In one release of Facebook for Android, Jitana found 3,918 classes by static analysis and 23,621 once it had captured three files that the app loaded as it ran; ReHAna was built because reflection and dynamic code loading hide code from any analysis that assumes the program is complete. The problem is general: reflection could not be ignored in 78% of the Java projects that Landman, Serebrenik and Vinju studied, PyCG reports a recall of about 70% for its call graphs of Python programs, and TypeScript's designers chose not to "apply a sound or 'provably correct' type system". A higher-level language therefore moves the difficulty of analysis from memory to dynamism, from whether a pointer is valid to whether the code that runs is the code that was analyzed. Next, we examine the four first-class languages.

## 2. Four languages on their own terms

**C++.** C++ is the language in which compiler infrastructure is written. LLVM, Clang and MLIR are C++ libraries, and all four languages reach machine code through LLVM; the Mojo compiler is written in C++ on MLIR, and Lean's kernel and runtime are C++. An analysis of compiled code across the four therefore reads representations that C++ defines. C++ also has the longest history of compile-time computation, from templates and `constexpr` functions to the static reflection of C++26, whose technical work the committee completed in March 2026 and which GCC 16 implements but Clang does not yet. Its templates are checked late: the parts of a template that depend on a parameter are checked only when an instance is formed, and a concept constrains which instances may be formed without checking the body against the constraint.

Undefined behaviour leaves a program with no meaning in the standard, and C++'s tools therefore answer narrower questions: sanitizers report it on the executions that ran, the Clang Static Analyzer explores paths symbolically without a guarantee of completeness, bounded model checkers such as CBMC establish a property up to a bound, and Clang 23 adds an intra-procedural check for use after free. C++26 makes reads of uninitialized local variables erroneous rather than undefined and hardens its standard library, whereas the author of Safe C++, a proposal for a borrow-checked subset, stopped work on it after the committee's safety group chose to prioritize profiles. The guarantees for C++ code therefore come mostly from tools around the language rather than from the language itself.

**Rust.** Rust makes ownership a property that its compiler checks: each value has one owner, a reference is either shared or mutable but not both, and the borrow checker enforces these rules on MIR before code is generated. Its traits are coherent, so that a trait has at most one implementation for a given type across all crates. Rust also has the most mature ecosystem of the four, and the one from which the others have most to learn. Cargo builds, tests and publishes with one tool, crates.io held 351,992 crates on 14 October 2026, and verification tools attach to MIR: Miri interprets it to detect undefined behaviour on the executions it runs, Kani model-checks it, and Aeneas translates it into Lean, the route by which Microsoft has proved its Rust implementations of ML-KEM and SHA-3. In 2025, memory-safety vulnerabilities fell below 20% of Android's vulnerabilities for the first time, and the maintainers of the Linux kernel concluded that Rust is no longer an experiment there.

What remains difficult is equally concrete. About 4% of Android's Rust sits in `unsafe` blocks, which permit operations whose safety the compiler cannot establish; data structures with shared mutable references fit the ownership discipline poorly; and the GPU targets are at tier 2 for NVIDIA and tier 3 for AMD. Rust also has no direct route into MLIR, whose C interface, in the words of pliron's authors, "is designed to interact with the compiler, not to extend it". pliron is therefore a representation in the style of MLIR, written in Rust and separate from MLIR, and NVIDIA's cuda-oxide, at an alpha stage, uses it to compile Rust kernels from MIR through LLVM to PTX.

**Lean.** Lean is a programming language as well as a setting for stating and checking properties. A Lean program is compiled: the compiler specializes it, emits C and compiles the C with a bundled C compiler. Its metaprogramming extends the compiler from within, since a macro, a syntax extension or a tactic such as `grind` is a Lean program that the compiler compiles and then runs on the rest of the file. Every declaration is checked by the kernel, a small type checker, so that a tactic or a language model may propose a proof but only the kernel accepts it.

The kernel, however, checks the logical definition and not the code that runs. The compiler is not verified; `implemented_by` substitutes code that, in its documentation's words, "is not checked to be equivalent to the original definition"; and `native_decide` runs compiled code and records its result as an axiom, as even `bv_decide` does for its verified checker of a SAT solver's certificate. A theorem about a function therefore establishes a property of its logical definition, while its execution depends also on the compiler, every substitution and the C toolchain. The Lean Focused Research Organization treats this boundary as engineering: its roadmap states that external checking of proofs "must become a routine part of every Lean user's workflow", and release 4.35.0 of 12 October 2026 bundles external checkers for that purpose. Lean is also a setting for code written elsewhere: AWS releases Cedar, an authorization language implemented in Rust, only when its Lean model, its proofs and the differential tests of the implementation against that model are current.

**Mojo.** We characterize Mojo as the first real language on MLIR, and the characterization has a technical meaning. Other compilers translate into MLIR either a language designed before it, as Flang does for Fortran and ClangIR for C and C++, or a program captured from Python, as Triton and Torch-MLIR do. Mojo's compiler parses source directly into its own MLIR dialects; in its documentation's words, "Mojo doesn't have an AST". Three consequences follow. The primitives of the language are library code over MLIR: `Bool` and the SIMD vector, of which `Int` is the one-element case, are structs that wrap MLIR types. Parameters are typed values, including types and lists, evaluated by an interpreter inside the elaborator on the same IR, so that generic code is "represented before instantiation" and survives into a package as MLIR, to be specialized by its consumer. And the target is an attribute fixed during elaboration, so that one source becomes code for CPUs and for NVIDIA, AMD and Apple GPUs.

The alternative shows what this removes. Triton parses a subset of Python, and its debugging interpreter does not support `bfloat16`, so that the semantics a developer debugs differ from those the compiler implements. Torch-MLIR requires value semantics and known ranks and types, whereas PyTorch tensors may alias and mutate. At each such boundary, the meaning of the host program and that of the captured program can diverge. Our earlier proposal, IAM, met this boundary, since its interpretability operations extended StableHLO, which a Python function reaches only after JAX has traced it. In Mojo nothing is captured, because the source and its MLIR are one program.

The ecosystem is young. Mojo 1.0, released on 11 August 2026, promises stability of source but not of its binary interface; the compiler, open since 18 August, accepts only bug fixes and refactors; and its dialects are declared internal. A package carries MLIR from before elaboration, so that an error in a library's compile-time values can appear first in a consumer's build. MAX records its graphs through a Python interface and does not yet train models, and Mojo has no verification tool. Mojo therefore removes the boundary between a language and the representation in which hardware is described, and leaves the others to be built.

## 3. One problem, four mechanisms

Consider a function that raises x to a power N, where N and the type of x are known at compile time. In each of the four languages, the compiler can perform the part of this program that is known before it runs and emit code for the rest. For N = 5 over double-precision numbers, the residual program in C++, Rust and Mojo is three multiplications, whereas Lean by default treats N as a run-time value and unfolds the recursion only when the function is marked for specialization. This is partial evaluation, and the generic machinery of each language, whether templates, traits, parameters or instances, is a discipline for deciding what is static. Figure F1 places the mechanisms of the four compilers side by side.

![F1 — The compiler's view. Each lane follows one compiler from left to right through five stages; an arrow means that the program passes to the next stage. "Optional" marks a route that exists and is not the default. In Lean, the kernel checks each declaration and emits no code, and compilation starts from the same definitions without being checked by the kernel.](diagrams/F1-compilers-view.svg)

The mechanisms differ along four dimensions. The first, when a generic body is checked, matters to anyone writing code. C++ checks the parts of a template that depend on a parameter only when an instance is formed; Rust and Mojo check generic bodies once against their bounds but evaluate constants that depend on parameters only when an instance is generated; Lean elaborates once and has the kernel check the result. In our study of the four compilers, a violated constraint on a compile-time value was reported by Lean during elaboration, where the value was supplied; by C++ at instantiation; by Rust in `cargo build` but not in `cargo check`; and by Mojo only when a consumer's build reached the value, not when the library was precompiled. For an engineer, or for a coding agent that generates, compiles and repairs code in a loop, a fast check that accepts what a full build rejects is an oracle that errs in one direction.

The second, the form of generic code that survives into a library, matters to anyone analyzing code. A C++ library ships templates as source, so that an analysis of LLVM IR sees only the instances that some translation unit formed. A Rust crate ships generic MIR, one body for all instances, which is why Miri, Kani and Charon, the front end of Aeneas, read MIR. A Mojo package ships MLIR whose parameters are still symbolic, so that an analysis built on Mojo's compiler could reason about every instance at once, in the representation that the compiler itself specializes; at the revision we studied, upstream MLIR tools could not read it. A Lean library ships its checked terms.

The third is what compile-time code may do: C++ constant evaluation may allocate only memory that it frees before it finishes, stable Rust may not allocate on the heap, a Mojo parameter may be a list built on the heap or a computed type, and a Lean metaprogram may add declarations and perform input and output. The fourth is what a metaprogram acts on: tokens for C++ and Rust macros, typed values for Mojo parameters, and the elaborator itself for Lean. Procedural macros, as Rust's reference states, "have the same resources that the compiler has", and so do Lean metaprograms; an account of what a build does must include the code that runs inside it.

Zig sharpens the comparison. Its `comptime`, like Mojo's parameters, uses one language at both stages and treats types as values, but its documentation calls the result "compile-time duck typing": a generic function is checked when it is called with particular types, as a C++ template is. One language for both stages does not by itself determine when an error is found. Next, we turn to what connects the four.

## 4. How the four connect

The four are joined by infrastructure and by calls, and Figure F2 separates the connections that exist from those that we propose. LLVM and MLIR, both written in C++, carry the code of all four toward machine code. Calls between the languages cross the C application binary interface (ABI): Rust and C++ declare `extern "C"` functions, Mojo calls external functions and opens dynamic libraries, and Lean binds C functions with `@[extern]`. The ABI carries data and not guarantees. A Rust lifetime, a Mojo origin and a Lean theorem all stop at the boundary, and Mojo's documentation states the consequence: "Nothing validates your arguments or return type against the C declaration."

![F2 — The four languages, the infrastructure they share and the interfaces between them. Arrows are routes of code toward machine code; solid lines are relationships that exist today; dashed lines, each labeled, are mappings that we propose and that do not exist. MLIR and LLVM are drawn in the color of C++, the language in which they are written.](diagrams/F2-four-languages.svg)

Several connections to Lean exist today. Aeneas translates safe Rust into Lean, and Cedar tests its Rust implementation against a Lean model. Between Lean and MLIR, the research project Lean-MLIR formalizes intermediate representations in static single assignment form and verifies peephole rewrites over them, and an earlier experiment gave Lean a back end in MLIR. Our proposals go further, and neither exists. The first maps Lean to MLIR: the semantics of a dialect is stated in Lean, so that a lowering between dialects can be checked against it. The second maps Lean abstractions to Mojo's parametric code, so that a Lean statement about every value of a parameter becomes a property of each instance that Mojo's elaborator produces. JITAC is designed with a control plane in Rust and a data plane in Mojo, as the [Research Statement](/research-statement/) describes, and the direction of the work is a data plane derived from abstractions stated in Lean and compiled through infrastructure written in C++.

OCaml and Zig show why these four, and not others, hold this position. OCaml has long been the language of verification tools: Rocq, Why3, Frama-C and Infer are written in it, and CompCert is extracted to it from proofs. Developer tools, however, are moving to Rust: Meta's Flow is now written in Rust, Pyre has been replaced by Pyrefly in Rust, and Bun moved from Zig to Rust in August 2026. Jane Street's OxCaml approaches Rust from the other side, adding modes that track locality, uniqueness and sharing between threads, with a core calculus proved free of data races; and Lean offers in one language what OCaml and a separate prover offered in two. Zig, finally, makes its own x86-64 back end the default for debug builds and plans to call Clang as a separate process instead of linking LLVM, the opposite of Mojo's commitment to MLIR and LLVM; the two choices differ in who owns the representation between source and machine code.

## 5. Verification, validation and three sites

Verification asks whether a program was built right, against its specification; validation asks whether the right program was built, for the purpose and setting in which it runs. Neither is a synonym for a kind of analysis. A proof establishes a property for every input, relative to a model of the language and a trusted checker; static analysis approximates every execution under assumptions about the program and its environment; a test verifies the executions it runs against an oracle; a measurement establishes performance on one configuration; and an operational observation establishes what ran, where and with what result. Each rests on assumptions that only another technique can check: that the code analyzed is the code that ran, that the compiler preserved its meaning, and that the target behaves as modeled. We therefore verify a property statically where static analysis suffices, and validate it, with the assumptions beneath it, on observed executions where it does not.

These questions arise in the work of three kinds of engineer, and one language can matter to all three. An AI engineer expresses a model or a kernel and selects its targets; Mojo specializes one source for several processors, and a measurement on one GPU establishes performance there and nowhere else. A software engineer integrates components across the C ABI and checks their properties, and every guarantee ends at the boundary between languages. A DevOps engineer builds for each target, deploys and examines what ran, and therefore needs to know which artifact, built by which compiler, executed on which device. Figure F3 shows, for each of the four, the sites on which its toolchain supports execution today.

![F3 — Heterogeneous computation across an Android device, a desktop workstation and a cloud. Each cell states what the toolchain of a language supports on that site today; a cell without a border means that no toolchain is supported there, and italics mark targets that a vendor has announced but not shipped. Solid arrows are transfers that exist; the dashed arrow is the proposed role of JITAC.](diagrams/F3-three-sites.svg)

The figure shows an asymmetry that all three roles meet. C++ and Rust reach every site, including the Android platform. Mojo reaches Apple silicon, Linux and the cloud, and Windows only through its Linux subsystem, but not Android, although Modular has announced a back end for the Hexagon processor in Qualcomm's chips. Lean's kernel runs wherever proofs are checked, and its programs run on desktop and server systems. A property proved on a workstation therefore reaches a phone only through an artifact compiled for the phone, and whether that artifact is the one that was analyzed is a question for observation. JITAC is designed to answer it, by deciding at run time what to load, how to specialize it and where to run it, and by recording each decision so that another party can check it; the dashed arrow marks this role as a design and not an implementation.

## 6. What remains difficult

At the time of writing, no compiler on the routes of Figure F1 is verified, so a property proved about source reaches machine code only through compilers that are tested. Mojo has neither a verification tool nor an Android target, and Boole, the route in CSLib from code to Lean goals, does not accept it. The C ABI carries no ownership, lifetime or proof between the four; C++26 reflection awaits Clang, and Rust's GPU targets remain below tier 1; and the mappings from Lean to MLIR and from Lean to Mojo are proposals.

In summary, the four languages share the problem of running part of a program before it runs and differ in when they check generic code, what they keep and what compile-time code may do; these differences decide what a writer sees, what an analyst reads and what a tool can establish. Each guarantee that one language provides stops at its boundary with the next, and carrying a guarantee across that boundary is the problem that the proposed mappings address.

Next in the series: Part 4.

## References

### This series and our work

1. [*Summer 2026: Mojo and MAX, the DeepSeek Harness, Lean, and NVIDIA*](/blog/golden-era-open-ecosystem/), Part 2 of this series.
2. [Research Statement](/research-statement/), *Just-in-Time Abstractions for Software Using Hybrid Program Analysis*.
3. Y. Tsutano, S. Bachala, W. Srisa-an, G. Rothermel and J. Dinh, "Jitana: A Modern Hybrid Program Analysis Framework for Android Platforms", *Journal of Computer Languages* 52:55–71, 2019. [PDF](/docs/Jitana-Journal.pdf)
4. S. Bachala, Y. Tsutano, W. Srisa-an, G. Rothermel, J. Dinh and Y. Hu, "ReHAna: An Efficient Program Analysis Framework to Uncover Reflective Code in Android", MobiQuitous 2021. [PDF](/docs/rehana.pdf)
5. S. Bachala, "Interpretable AI with MLIR (IAM): A Unified Framework for Neural Network Transparency", ICSE 2026 Doctoral Symposium. [PDF](/docs/shakthi_bachala_research_statement_icse.pdf)

### C++

6. H. Sutter, "C++26 is done! Trip report: March 2026 ISO C++ standards meeting (London Croydon, UK)", 29 March 2026. https://herbsutter.com/2026/03/29/c26-is-done-trip-report-march-2026-iso-c-standards-meeting-london-croydon-uk/
7. GCC 16 Release Series, Changes. https://gcc.gnu.org/gcc-16/changes.html; Clang, C++ Support in Clang. https://clang.llvm.org/cxx_status.html
8. LLVM Coding Standards. https://llvm.org/docs/CodingStandards.html
9. Clang 23.1.0 Release Notes. https://releases.llvm.org/23.1.0/tools/clang/docs/ReleaseNotes.html
10. S. Baxter and C. Mazakas, "Safe C++", P3390R0. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3390r0.html; The Register, "Safe C++ proposal ditched", 16 September 2025. https://www.theregister.com/2025/09/16/safe_c_proposal_ditched/
11. CBMC. https://github.com/diffblue/cbmc; ESBMC. https://github.com/esbmc/esbmc; Clang Static Analyzer. https://clang-analyzer.llvm.org

### Rust

12. Rust Compiler Development Guide, "Overview of the compiler". https://rustc-dev-guide.rust-lang.org/overview.html
13. The Rust Reference, "Procedural macros". https://doc.rust-lang.org/reference/procedural-macros.html
14. crates.io, summary statistics, retrieved 14 October 2026. https://crates.io/api/v1/summary
15. The Rust Project, "Adopting the FLS", 26 March 2025. https://blog.rust-lang.org/2025/03/26/adopting-the-fls/
16. Miri. https://github.com/rust-lang/miri; Kani. https://github.com/model-checking/kani; Verus. https://github.com/verus-lang/verus; Aeneas. https://github.com/AeneasVerif/aeneas
17. Microsoft Research, "Verifying Rust cryptography in SymCrypt: from standards to code", 13 July 2026. https://www.microsoft.com/en-us/research/blog/verifying-rust-cryptography-in-symcrypt-from-standards-to-code/
18. J. Vander Stoep, "Rust in Android: move fast and fix things", Google, 13 November 2025. https://blog.google/security/rust-in-android-move-fast-fix-things/
19. J. Corbet, "The state of the kernel Rust experiment", LWN, December 2025. https://lwn.net/Articles/1049831/
20. rustc, "Platform Support". https://doc.rust-lang.org/nightly/rustc/platform-support.html
21. pliron. https://github.com/pliron-org/pliron; pliron wiki, "Introduction". https://github.com/pliron-org/pliron/wiki/Introduction; NVIDIA, cuda-oxide. https://github.com/NVIDIA/cuda-rust

### Lean

22. Lean Language Reference, "Elaboration and Compilation". https://lean-lang.org/doc/reference/latest/Elaboration-and-Compilation/
23. Lean API documentation, `implemented_by`. https://lean-lang.org/doc/api/Lean/Compiler/ImplementedByAttr.html
24. Lean 4.29.0 and 4.35.0 release notes. https://lean-lang.org/doc/reference/latest/releases/v4.29.0/; https://lean-lang.org/doc/reference/latest/releases/v4.35.0/
25. Lean FRO, Roadmap, Year 4, Part 1. https://lean-lang.org/fro/roadmap/y4-1/
26. Lean Language Reference, "Supported Platforms". https://lean-lang.org/doc/reference/latest/platforms/
27. H. Böving, S. Bhat et al., "Interactive Bitvector Reasoning using Verified Bit-Blasting", *PACMPL* 9(OOPSLA2), 2025. https://doi.org/10.1145/3763167
28. Cedar specification and Lean formalization. https://github.com/cedar-policy/cedar-spec; AWS, "Lean Into Verified Software Development", 8 April 2024. https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/
29. nanoda. https://github.com/ammkrn/nanoda_lib
30. S. Bhat, A. Keizer, C. Hughes, A. Goens and T. Grosser, "Verifying Peephole Rewriting In SSA Compiler IRs", ITP 2024. https://arxiv.org/abs/2407.03685; Lean-MLIR. https://github.com/opencompl/lean-mlir
31. S. Bhat and T. Grosser, "Lambda the Ultimate SSA: Optimizing Functional Programs in SSA", CGO 2022. https://arxiv.org/abs/2201.07272

### Mojo, MLIR and the Python-embedded stacks

32. Mojo documentation, "Mojo vision". https://mojolang.org/docs/vision/
33. Modular, Mojo compiler manual, "Passes and IR". https://github.com/modular/modular/blob/main/Mojo/docs/compiler/manual/PassesAndIR.md
34. Mojo documentation, "Inline MLIR". https://mojolang.org/docs/reference/inline-mlir/; "Parameterization". https://mojolang.org/docs/manual/parameters/
35. Mojo documentation, "Mojo stability guarantees". https://mojolang.org/docs/api-docs/stability/; Mojo 1.1.0 release notes. https://mojolang.org/releases/v1.1.0/
36. Modular, "Mojo is now open source!", 18 August 2026. https://www.modular.com/blog/mojo-open-source; contribution areas. https://github.com/modular/modular/blob/main/Mojo/docs/contributing/contribution-areas.md
37. Mojo documentation, "System requirements". https://mojolang.org/docs/requirements/; Modular, "ModCon 2026: Open source, open cloud, open silicon". https://www.modular.com/blog/modcon-announcements; Modular, ModCon and Qualcomm. https://www.modular.com/blog/modcon-qualcomm
38. Mojo documentation, "Calling C". https://mojolang.org/docs/manual/c-ffi/
39. C. Lattner et al., "MLIR: Scaling Compiler Infrastructure for Domain Specific Computation", CGO 2021. https://arxiv.org/abs/2002.11054
40. Flang, "Fortran IR (FIR)". https://flang.llvm.org/docs/FortranIR.html; ClangIR. https://llvm.github.io/clangir/
41. Triton. https://github.com/triton-lang/triton; P. Tillet, H. T. Kung and D. Cox, "Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations", MAPL 2019. https://doi.org/10.1145/3315508.3329973
42. Torch-MLIR, architecture. https://github.com/llvm/torch-mlir/blob/main/docs/architecture.md

### Other languages

43. TypeScript Design Goals. https://github.com/microsoft/TypeScript/wiki/TypeScript-Design-Goals
44. V. Salis, T. Sotiropoulos, P. Louridas, D. Spinellis and D. Mitropoulos, "PyCG: Practical Call Graph Generation in Python", ICSE 2021. https://arxiv.org/abs/2103.00587
45. D. Landman, A. Serebrenik and J. J. Vinju, "Challenges for Static Analysis of Java Reflection – Literature Review and Empirical Study", ICSE 2017. https://doi.org/10.1109/ICSE.2017.53
46. Android Developers, "Android's Kotlin-first approach". https://developer.android.com/kotlin/first
47. Zig 0.17.0 Release Notes. https://ziglang.org/download/0.17.0/release-notes.html; Zig Language Reference, "comptime". https://ziglang.org/documentation/0.17.0/#comptime
48. L. White, "Introducing OxCaml", Jane Street, June 2025. https://blog.janestreet.com/introducing-oxcaml/; A. L. Georges et al., "Data Race Freedom à la Mode", POPL 2025. https://doi.org/10.1145/3704859
49. X. Leroy, "Formal verification of a realistic compiler", *Communications of the ACM* 52(7):107–115, 2009. https://doi.org/10.1145/1538788.1538814
50. Flow. https://github.com/facebook/flow; Pyrefly. https://github.com/facebook/pyrefly; J. Sumner, "Rewriting Bun in Rust", July 2026. https://bun.com/blog/bun-in-rust

### Method

51. B. W. Boehm, "Verifying and Validating Software Requirements and Design Specifications", *IEEE Software* 1(1):75–88, 1984. https://doi.org/10.1109/MS.1984.233702
52. N. D. Jones, C. K. Gomard and P. Sestoft, *Partial Evaluation and Automatic Program Generation*, Prentice Hall, 1993.
53. The four-compiler study of Section 3 ran its programs with Clang 22.1.8, rustc 1.97.1, a Mojo build of September 2026 and Lean 4.35.0-nightly-2026-09-12, and read the sources of each compiler at pinned revisions of the same month. Mojo 1.1 renamed several forms of syntax afterward; the mechanisms described here are those of the compiler, not of its spelling.
