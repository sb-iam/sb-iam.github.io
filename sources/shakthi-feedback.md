# My Feedback


Three research threads on trustworthy -> verifiable agentic software: the open ecosystem around it, the hybrid methods that evaluate it, and the engineering stack that puts it into practice. The outlines are tentative and will evolve as the work develops. This is my personal blog, UNL, BMO or CFA


Open Compilers: Mojo, Rust, Modern C++, MLIR, LLVM, and the Pattern Book for DSLs and libraries to compose

Agent Harnesses, sandboxes and the safe deployment pipeline


Open Proofs: Lean, CSLib, and the Checker Nobody Owns-> Formal verification with Rust toolchain, the ecosystem the mojo needs to build on..

Open Weights, Models, and Environments: the Letter, the Activation Gap, and RL on Your Own Hardware -> remove activation gap, 

My research comes out of the Android lineage: Jitana's virtual graph loader built using C++ BGL, which loads dexcode into an analyzable graph on demand  instead of reconstructing a whole program, and ReHAna, which recovered the code that reflection/dynamic code hides. The same principles now apply across the AI stack: static analysis, dynamic analysis, compiler infrastructure, and runtime evidence, combined so that software changes are easier to inspect, test, explain, and review.

VerifyD is the platform direction, with interpretability and verification as first-class citizens: static checks, dynamic checks, compiler-aware evidence, provenance, record replay with graph substrates and human review for AI-assisted software engineering. The control plane is built on Rust and Data Plane is in Mojo, MLIR is sparsely used after Mojo compiler was releasted tooling, built on the same principles of virtual graph loader. Will be opensourced soon.



› Remove Witawas in this IAM: Interpretable AI with
  MLIR - A Compiler-Integrated Framework for
  Trustworthy Code Generation
  Shakthi Bachala, Witawas Srisa-an. ICSE 2026
  Doctoral Symposium.



Thread 2

Hybrid Analysis
Notes on static analysis, dynamic analysis, Android analysis, compiler IR, and runtime evidence. A Five-part opening series, revisited quarterly.

1. Static vs Dynamic Analysis -> Static  Dynamic
2. Verification vs Validation -> Verification + Validation
3. Program Synthesis vs LLMs -> Program Synthesis + LLMs
3. Applied Research Topics ->  MECH Interp + Influence Functions; Static Models vs continual learning
6. Unification substrate 


Thread 3

Future of Software Engineering
Notes on how software engineering changes when models, tools, and compilers work together: how devtools unify the personas of software engineer, AI engineer, and platform engineer, and whether generic or specialized, extensible tooling wins. A Five-part opening series, revisited quarterly.



Future of Software Engineering
1. IDEs, CLIs, Agent Harnesses, LLMs  the stack. 
2. High Performant but safe languages for Coding Agents 
3. Yet another Protocol - LSP, ACP, MCP, A2A.... -> 
4. Persona - Software Engineer, AI Engineer, Platform Engineer, Security Engineer, DevOps....
5. Unification with Composable Tooling  










Title of the series - Open ecosystem in the era of AI?
Mojo Compiler Released
DeepSeek's Impact on AI (Democratizing AI Compute, Part 1)


Note: There are

1. Start with AI evolution -> graph

  1. Nov 2022 - ChatGPT
  2. Fall 2024 - O3 Reasoning Models + Deep
  Seek Moment
  3. Fall 2025 - Coding Agents + Open Claw
  4. Summer 2026 - Openecosystem for AI

2. Real Jensen Huang AI Cake

3. In-Scope and Out-of-Scope of the thread
In-scope: Coding
Out-of-scope: ...


Future of Software Engineering	3: 
IDEs, CLIs, and harnesses · language wars in the agent era · review, acceptance, and ownership, sdlc, devops, pipeelinges and hyperscalers and neo clouds


SDK's are open but hte backend FFI's and the real would be opensourced which is the secret sauce



Mojo:
1. First Lanugage on MLIR
2. First AI native mainstream AI language
3. Here Data Plane means -> Inference and training
4. Max - Graph Compiler... 
5. Unification of Inference and Training in one ecossytem
6. Broken training <-> inference, pytorch/jax/tensorflow <-> vllm, SGLang, TensorRT-LLM... 
7. But if both are on the same platform, with mojo a systems level language with performance of rust/c++ with zero abstraction(Ideally sometime -ve abstractions like c++)
8. Max inference <-> nabla training I am building nabla-mojo which will be open source soon it is not replacement for pytorch but only for trianing coding models, there are many other training 
9. https://github.com/ulmentflam/llm.mojo
10. https://github.com/nabla-ml/nabla

It is not just perf. if both are on the same platform the 50 years of program analysis easily applicablae that is possible is amazing as there is no cross language 

Devex of AI engineer
1. Training: Pytorch(10 years old), jax...
2. RL: Fireworks supports it too closed, open - Primeintellect, verl...
3. Inference: Fireworks, SGLang...
4. Orchestration Agents: Langchain, ...

Chris Lattner's LLVM is particularly relevant to your series because it demonstrates the same phenomenon at the compiler layer. A reusable, permissively licensed compiler infrastructure allowed languages, research projects, hardware vendors and commercial products to share an enormous body of compiler engineering rather than independently rebuilding it.

So I would sharpen your three incentives to:

Why Open?
	​

1. COMMON INFRASTRUCTURE
   "This should be something everyone can build on."


   Internet standards
   Linux
   LLVM




2. STRATEGIC COLLABORATION
   "We benefit more by sharing this layer
    than by competing over it."


   shared cost
   catch-up
   commoditize a non-core layer
   compete elsewhere




3. NETWORK EFFECTS
   "The technology becomes more valuable
    when everyone can participate."


   programming languages
   compilers / IRs
   protocols
   package ecosystems
   agent interfaces
   policy languages

And the interesting thing for the series is that these aren't mutually exclusive.

LLVM, for example, can simultaneously be understood as:

                  LLVM
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
  COMMON GOOD   COLLABORATION   NETWORK
  compiler      Apple, Google,  languages,
  infrastructure NVIDIA, AMD,   targets,
                Intel, etc.     tooling

That gives you a more sophisticated thesis than:

Companies open source because open source is good.

Your thesis becomes:

Open ecosystems emerge when private actors discover that there is more value in sharing a foundational layer than owning it exclusively. Sometimes that begins as a public good, sometimes as strategic necessity, and sometimes because the technology cannot achieve its full value without a network. Often, all three forces eventually reinforce one another.

That sentence could become one of the recurring ideas across all ten posts.

And it connects beautifully to the future of software engineering question. The interesting question isn't merely what will be open sourced? It is:

Which layers of the emerging AI software stack become common infrastructure, which remain competitive, and what economic or technical force determines that boundary?

That gives you room later to analyze Linux, LLVM/MLIR, Mojo, Rust, Cedar, ACP/MCP, agent harnesses, models, inference runtimes, and hardware without assuming they all have the same reason for being open.





Out of scope-of this series
1. Ethics of open vs closed source
2. Layer below ABI and physical hardware/robotics layer
3. Only focused on Software engineering

This is a culmination of my talking to more than 100's of researchers and attending these 3 conferences mainly modcon 2026(mojo compiler release), ICSE 2026(Doctoral Symposium -> IDE 2026 Workshop sponsored by Jet brains) and Verified Summit 2026 by Pramanna Lab

This also takees a neutral on open and closed both would exist but takes the learning from ICML paper on 


https://arxiv.org/pdf/2507.09296


But blog 1: needs to be:
1. Open AI Layer Cake - Explain that
  2. Although in the era ai, everything moves faster The combination of all the below - a diagram for ai asiisted software development(auto sdlc, auto research is out of scope but a verifiable ecosystem helps to create verified large scale software the principles that functional programming and RISC-V/hardware commmuntiy have)
    3. Modcon 2026: Mojo open COmpiler - First mainstream language on mlir, ai native language, unification of kernel development... point to mojo 1.0 for more 
      4. https://www.modular.com/blog/modcon-announcements


4. , Open Pledge by big tech 

5. Deep Seek Open Harness(inspired the phiosphy from pi but ground-up) 

7. CS Lib funding by AWS Reasoning group for Lean FRO -> This is a big leap for the community of auto formalization 

8. Open Models + environments to build rl like prime intellect with GLM, Kimi which are on pair with frontier model, but smaller models that can run on dgx spark which we can finetune, apply rl(the whole framework by primeintellect here with both verification and validation)

An ecosystem is as good as its developer tooling, and in the next part of the series we will cover deep into each topics... starting with the holy wars of programming languages and their sdk's and where each language fits in the ecosystem of layer cake



Blog 2 can be the this with the title leaky abstraction to type safe abstractions in the era of open ecosystem



Mojo compiler is open source: As this is the first language on mlir ecosystem this provide the compiler industry the best practices of using and creating dsls for applications of  mlir-based compilers
https://www.modular.com/blog/mojo-open-source

Add references with classification:
Autoformalization and verification layer
1. Position: Theory-Level Autoformalization, From Isolated Statements to Unified Formal Knowledge Bases
https://openreview.net/pdf?id=BoteCHEFUr
2.  CSLib: The Lean Computer Science Library
3. https://arxiv.org/pdf/2602.04846
https://www.amazon.science/news/amazon-is-investing-in-the-lean-focused-research-organization



Agent Harnesses
1. https://github.com/deepseek-ai/deepseek-harness
2. https://github.com/cordiverse/paper/blob/main/paper.pdf especially the formalisms in page 55 for starters 

IDE: My current set-up of one window is zed integrated with codex, claude code and cursor through cli with one unification of handoffs, agent orchestration....
High-Performance in Rust 
https://github.com/zed-industries/zed

Open pledge: https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf









This is incorrect"
Series Map
The Golden Era of the Open Ecosystem
Open models, open harnesses, open compilers, open protocols, incentives, and why evidence must be portable.
Hybrid Analysis for AI Software Engineering
Static analysis, dynamic analysis, Jitana/ReHAna lineage, traces, symbolic methods, and why agents make hybrid analysis central again.
The Future of Software Engineering
IDEs as human control planes, CLI as the durable base, agent protocols, language wars, and code review when agents produce most of the patch.
Autoformalization and the Verification Layer
Candidate invariants, Lean/SMT/model checking, proof admission rules, counterexamples, and the difference between formalization and truth.
Languages for Verifiable AI Infrastructure
Rust, Mojo, modern C++, MLIR, typed IRs, ownership, effects, and why Python should not be the systems substrate.
The Social Contract of Open AI Software
Licensing, provenance, attribution, platform risk, and the new norms required when coding agents can read and reuse the open world." :
1. We would have 3 threads (all these thread this would be revisited every quarter for some forseeabel future))
2. 6 part series on open ecosystem
3. 3-part series on hybrid analysis including verification vs validation; static vs dynamic instead verson static + dynamic; verification + validation.....
4. 3-part series on future of software engineering(this would be revisited every quarter for some forseeabel future)



Completed 2026-08-21 (Claude, session ab064f46 — see blog-1/claude_review.md §8):
1. Blog 1 rebuilt as the landscape essay: Open AI Layer Cake explained (F3, with the 2026 open
   reference per layer); agentic-SDLC figure (F6) with the FP and RISC-V/hardware principles,
   auto-research out of scope; ModCon 2026 / Mojo 1.0 + open compiler; the open-weights letter;
   DeepSeek Harness on Cordis; Lean FRO gift + CSLib; Prime Intellect environments with GLM/Kimi and
   DGX Spark; "an ecosystem is as good as its developer tooling" close; languages/SDK holy wars in
   Part 3; scope exclusions; provenance note (ICSE 2026 -> The Verification Summit -> ModCon 2026).
   Neutral stance cited to Tan et al., "If open source is to win, it must go public", ICML 2026.
2. Blog 2 seeded at blog-2/blog-2.md with the Phi / type-safety essay and its figures, titled
   "From Leaky Abstractions to Type-Safe Abstractions in the Era of the Open Ecosystem".
3. Wording corrected against sources before publishing: the NVIDIA-hosted document is an open
   letter (25 launch signatories, 235 by Jul 29), not a pledge; DeepSeek Harness does not credit pi
   (its Minimal mode is pi-shaped; pi is one npm dependency); GLM-5.2 (753B) and Kimi K3 (2.8T) do
   not run on a DGX Spark (30-70B models do); Amazon's gift went to the Lean FRO, CSLib is separately
   governed and funded; "The Verification Summit" by Pramaana Labs; IDE 2026 organized (not
   sponsored) by JetBrains Research; Mojo is "the first major language designed expressly for MLIR"
   (Modular's earlier wording), not "AI-native".
4. Series map: 3 threads, Open Ecosystem 6 parts, Hybrid Analysis 3, Future of SE 3, quarterly.
5. Register: the overnight "formal" pass is archived (blog-1/archive/v5b-...codex...), not used;
   the bold pitch register stands on the page.
6. (later on 2026-08-21) Cake first, then an explicit "What this series covers" section (in scope /
   out of scope); Open Ecosystem thread expanded to 10 parts; Future of SE row adds persona
   unification by devtools and generic vs specialized/extensible tooling; new figure F7 places the
   open-weights letter, the Lean FRO gift, DeepSeek Harness (type theory + category theory via
   Cordis: effects as monads, coeffects as comonads, tracked inverses), and Mojo's open compiler on
   their layers with the first principle each rests on.
7. Separate /blog/ page ("Blog" / "Threads") listing the three threads and their parts; nav Blog
   links point there; essay URL is now /blog/golden-era-open-ecosystem/ (redirect kept at
   /writing/...); homepage column relabelled Blog / Threads; CV PDF link in the site accent.
8. (afternoon 2026-08-21) F0 AI-evolution opener (ChatGPT; reasoning models + DeepSeek moment —
   dated winter 2024-25 since V3/R1 and the $589B day were Dec-Jan; coding agents + OpenClaw —
   OpenClaw is Steinberger's open personal agent, begun Nov 2025, named Jan 30 2026; open ecosystem
   for AI). F8 Jensen Huang's real five-layer cake with our six-layer cake inset (source: "AI Is a
   5-Layer Cake", NVIDIA Blog, 2026-03-10). In scope: coding. Mojo expanded: data plane = training +
   inference, the broken PyTorch/JAX <-> vLLM/SGLang/TensorRT-LLM split, MAX, llm.mojo, Nabla,
   nabla-mojo (yours, open source soon, coding models only), and the one-platform program-analysis
   argument. DevEx-of-the-AI-engineer table by plane (open vs closed). Why Open restated as the three
   incentives + LLVM three ways + the recurring thesis sentence + the boundary question; Lattner's
   Democratizing AI Compute Part 1 and the LLVM developer policy cited.


Completed
1. Change CV /Users/shakthibachala/Desktop/verifyd/unified-plane/verifyd_unified_devex/writing/impl-repo/sb-iam.github.io/docs/cv:
  2. Change the graduation to Dec-2026
  3. Change the title of dissertation to "Hybrid Program Analysis for Verifiable Software"  
    
  2. Professional Experience: Add the cv-pdf link for more details
  
  Professional Experience
  Engineering Leadership to Principal Cloud Engineer - AI (IC)
  Bank of Montreal (BMO) | Cloud & AI Infrastructure
  
  Led a team of 50+ cloud engineers in enterprise-scale transformations.
  Orchestrated 20+ PB data migration for the Bank of the West acquisition.
  Delivered an MLOps platform from sandbox to production in 15 business days on AWS.
  Pioneered GenAI infrastructure deployment for Azure in 2 weeks.
  Created Cloud Adoption Assist, reducing deployment time by 60%.
  Transitioned to Principal Cloud Engineer - AI to focus on hands-on AI and ML infrastructure work.

Completed:


Always make the format better

1. All the reserch publication should connect with a proper document of link of pdf or source code /Users/shakthibachala/Desktop/verifyd/unified-plane/verifyd_unified_devex/writing/impl-repo/sb-iam.github.io/docs 
/Users/shakthibachala/Desktop/verifyd/unified-plane/verifyd_unified_devex/writing/impl-repo/sb-iam.github.io/docs

For An Efficient, Robust, and Scalable Approach for Analyzing Interacting Android Apps -> put the link of jitana source code https://github.com/ytsutano/jitana.git
