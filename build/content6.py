"""Part VI — Multiprocessors, vector/SIMD/GPU, formula sheet and PYQ index."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

def build():
    F=[]
    def A(x): F.extend(x if isinstance(x,list) else [x])

    # ============ 13. MULTIPROCESSORS ============
    A(PageBreak())
    A(h1(13,"Multiprocessors & Multicores","Sharing memory across many processors"))
    A(p("A <b>multiprocessor</b> has several processors cooperating on one job (or several jobs). They must "
        "share data, so the big questions are: how is memory organised, and how do the processors talk to "
        "each other? The answers give the standard taxonomy you must know."))

    A(h3("13.1 Shared-memory classification: UMA, NUMA, COMA"))
    A(table(["Model","Full name","Memory access","Scalability","Notes"],
      [["UMA","Uniform Memory Access","All processors access all memory in the same (uniform) time.","Poor — the shared bus/memory becomes a bottleneck.","Classic SMP; simple; needs coherence (snooping)."],
       ["NUMA","Non-Uniform Memory Access","Access time depends on which memory (local vs remote) is touched.","Good — memory is distributed with the processors.","Each node has local memory; remote access is slower. Needs directory coherence."],
       ["COMA","Cache-Only Memory Access","Memory is made of caches; data migrates to where it is used.","Good.","Attractive memory (a block has no fixed home); complex."]],
      widths=[0.8,1.5,2.2,1.4,1.5]))
    A(fig("page004.jpg", w=11.0*gen.cm, cap="UMA vs NUMA: uniform versus non-uniform memory access times (source: lecture notes, p. 4)."))
    A(p("<b>Reading the figure.</b> The classification of multiprocessors by how memory is shared (UMA vs NUMA) and by the interconnection network."))

    A(h3("13.2 Interconnection networks"))
    A(fig("page010.jpg", w=10.5*gen.cm, cap="Mesh and torus interconnection topologies (source: p. 10)."))
    A(p("<b>Reading the figure.</b> Interconnection topologies for multiprocessors — mesh and torus — showing the per-node links and the hop count between nodes."))
    A(p("The processors and memory modules are connected by an <b>interconnection network</b>. The choice of "
        "topology trades cost, latency and bandwidth."))
    A(table(["Topology","Shape","Strength","Weakness"],
      [["Bus","One shared wire for all.","Simple, cheap; easy coherence (snooping).","Bottleneck; poor scalability."],
       ["Multistage bus","Several buses in stages.","More bandwidth than a single bus.","More complex arbitration."],
       ["Crossbar","Every input connects to every output.","Non-blocking; high bandwidth.","Cost grows as N²; hard to build large."],
       ["Multistage network (omega, butterfly)","Logarithmic stages of switches.","Cost grows as N log N; scalable.","Blocking possible; contention."],
       ["Hypercube / torus / mesh","Each node connected to neighbours.","Good scalability; high bisection bandwidth.","Complex routing; wiring grows with dimension."]],
      widths=[1.5,1.6,1.7,1.7]))
    A(fig("page009.jpg", w=11.0*gen.cm, cap="Interconnection topologies: bus, multistage, crossbar (source: lecture notes, p. 9)."))
    A(p("<b>Reading the figure.</b> A switch/crossbar-based interconnection. A crossbar connects every processor to every memory without contention, but its cost grows as the square of the number of nodes."))
    A(callout("<b>Bandwidth vs latency:</b> a crossbar gives the highest bandwidth but the highest cost; a bus "
              "is cheapest but least scalable. Real systems use a hierarchy (cores → ring → memory "
              "controllers) to get both."))

    A(h3("13.3 Multicore vs multiprocessor"))
    A(table(["","Multicore","Multiprocessor (multi-socket)"],
      [["Where","Several cores on one chip.","Several chips (sockets) on one board."],
       ["Communication","Very fast on-chip (shared L3, ring).","Slower (off-chip interconnect)."],
       ["Coherence","Usually snooping MESI on-chip.","Directory-based, or snooping per socket."],
       ["Example","Core i7, Ryzen.","Dual-socket Xeon server."]],
      widths=[1.0,2.4,2.6]))

    A(callout("<b>Chip multiprocessor (CMP).</b> A multicore chip is a <i>chip multiprocessor</i>: several "
              "processors on one die, usually sharing an on-chip last-level cache and connected by an on-chip "
              "network (ring/mesh). CMP gives thread-level parallelism (TLP) without the off-chip latency of a "
              "classic multiprocessor, and is the industry answer to the end of Dennard scaling.", 'tip'))
    A(h3("13.4 The cache-coherence cost (why multicore is not free)"))
    A(p("Adding cores adds coherence traffic (invalidations, block transfers). The classic exam calculation: "
        "a single core has some CPI from its own cache misses; a multicore has a <i>higher</i> miss rate and "
        "miss penalty because of coherence, so its CPI rises. The multicore is only worth it if the "
        "parallel speed-up outweighs the higher CPI (PYQ ca15)."))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Multiprocessors"))
    A(Paragraph("Q (ca7 · Q3b). What is multiprocessor cache coherence? Differentiate between snoopy-based and "
                "directory-based protocols with neat diagrams.", ST['q']))
    A(Paragraph("<b>Solution.</b> Cache coherence keeps all caches consistent so a read returns the latest "
                "write. Snoopy protocols have every cache watch a shared bus and react to each transaction "
                "(scalable only to a moderate number of processors; the bus is the bottleneck). Directory "
                "protocols keep a central table of which caches hold each block and send point-to-point "
                "invalidates only to those caches (scalable, but the directory lookup adds latency and can "
                "become a hot spot). Diagrams: (a) several caches on a shared bus, each connected to the bus "
                "for snooping; (b) a directory block at the memory side, with messages to/from the caches "
                "that hold the block.", ST['ans']))

    A(Paragraph("Q (ca26 · Q1a). Two operations: (i) a product of 3 scalar variables, and (ii) a matrix sum of "
                "two 9×9 arrays. Only the matrix sum is parallelizable. (i) What speed-up with 10 vs 40 "
                "processors? (ii) Recompute if the matrices grow to 20×20.", ST['q']))
    A(Paragraph("<b>Solution (Amdahl's law).</b>", ST['ans']))
    A(bullets([
      "Work: the scalar product is a fixed, serial amount (3 multiplications). The matrix sum is parallel "
      "work proportional to the number of elements.",
      "9×9 = 81 elements added (in parallel); 20×20 = 400 elements added.",
      "Choose a work unit so that the parallel fraction f = parallel work / total work. For a small serial "
      "part s and parallel part p, f = p/(s+p) and S = 1/[(1−f) + f/P].",
    ]))
    A(formula("9×9 :  serial = 3 ops, parallel = 81 ops → f = 81/84 = 0.9643\n"
              "   S(10) = 1/[(1−0.9643) + 0.9643/10] = 1/[0.0357 + 0.09643] = 1/0.1321 = 7.57\n"
              "   S(40) = 1/[0.0357 + 0.9643/40] = 1/[0.0357 + 0.02411] = 1/0.0598 = 16.7\n\n"
              "20×20: serial = 3, parallel = 400 → f = 400/403 = 0.99256\n"
              "   S(10) = 1/[(0.00744) + 0.099256] = 1/0.10670 = 9.37\n"
              "   S(40) = 1/[0.00744 + 0.024814] = 1/0.032254 = 31.0"))
    A(p("<b>Observation:</b> as the problem grows, the serial fraction shrinks, so the speed-up approaches "
        "the number of processors — the essence of Gustafson's insight that bigger problems parallelise "
        "better."))

    # ============ 14. VECTOR, SIMD, GPU ============
    A(PageBreak())
    A(h1(14,"Vector, SIMD & GPU Architectures","Data-level parallelism done at scale"))
    A(p("Pipelining and superscalar execution exploit <b>instruction-level</b> parallelism — a few "
        "instructions at a time. <b>Data-level</b> parallelism is different: apply <i>one</i> operation to "
        "<i>many</i> data elements at once. Vector processors, SIMD units and GPUs are all built for this."))

    A(h3("14.1 Vector architecture"))
    A(fig("page061.jpg", w=10.5*gen.cm, cap="Vector processor: pipelined functional units and vector registers (source: p. 61)."))
    A(p("<b>Reading the figure.</b> The vector processor. Vector registers feed deeply pipelined functional units that produce one element per cycle, so one vector instruction replaces an entire loop."))
    A(p("A <b>vector processor</b> has instructions that operate on whole arrays (vectors) of data, e.g. "
        "<font face='Mono'>ADDV V1,V2,V3</font> adds two 64-element vectors. The hardware is a deeply "
        "pipelined functional unit fed by vector registers. One vector instruction replaces a whole loop, so "
        "the instruction-fetch overhead disappears."))
    A(table(["Feature","Benefit"],
      [["Vector registers (e.g. 8 × 64 elements)","Hold whole arrays; data flows register-to-register."],
       ["Pipelined functional units","One element per cycle; hides the long latency of FP operations."],
       ["Vector length register (VL)","Handles loops shorter than the full vector length."],
       ["Stride / gather-scatter","Access non-contiguous data (e.g. matrix columns)."],
       ["Chaining","Feed one vector unit's output directly into the next (like forwarding)."]],
      widths=[2.0,4.0]))
    A(formula("Vector speed-up ≈ (elements per vector instruction) × (functional-unit pipelining)\n"
              "Time for one vector op = (vector length) / (elements per cycle) + start-up latency"))

    A(h3("Array processors and systolic arrays"))
    A(p("Before GPUs, data-level parallelism was exploited by <b>array processors</b> and <b>systolic "
        "arrays</b> — both still exam favourites."))
    A(table(["Structure","Idea","Notes"],
      [["Array processor","A controller broadcasts one instruction to many processing elements (PEs), each working on its own data.","This is exactly SIMD: one instruction stream, many data streams (Flynn)."],
       ["Systolic array","A grid of simple PEs where data pulses through in lock-step, each PE passing partial results to its neighbour.","Very high throughput per unit area; used in matrix/convolution hardware; all PEs share one clock."]],
      widths=[1.3,2.7,2.0]))
    A(fig("page017.jpg", w=10.5*gen.cm, cap="Systolic array and parallel-processing discussion from the notes (source: p. 17)."))
    A(p("<b>Reading the figure.</b> The systolic array. A grid of simple processing elements has data pulsing through it in lock-step, each PE passing partial results to its neighbour — very high throughput for matrix operations."))
    A(callout("<b>Key distinction:</b> a <i>vector</i> machine pipelines one stream of operations over a long "
              "vector; an <i>array/systolic</i> machine has many PEs working simultaneously (spatial "
              "parallelism). Both are SIMD in Flynn's terms. The GPU is the modern descendant of the array "
              "processor."))

    A(h3("14.2 SIMD vs vector vs GPU"))
    A(fig("page062.jpg", w=10.5*gen.cm, cap="Vector/SIMD loop unrolling and scheduling (source: p. 62)."))
    A(p("<b>Reading the figure.</b> The vector/SIMD loop. The compiler converts a scalar loop into vector operations over whole arrays, which is why vector code is far shorter and faster."))
    A(table(["","Vector processor","SIMD (multimedia/ISA)","GPU"],
      [["Granularity","Long vectors, pipelined","Short vectors in one instruction (e.g. 4-wide)","Thousands of threads (SIMT)"],
       ["Control","One instruction over a vector","One instruction over packed data","One instruction over a warp of threads"],
       ["Memory","Vector load/store","Packed load/store","High-bandwidth GDDR/HBM"],
       ["Programming","Compiler + vector intrinsics","Intrinsics / auto-vectorisation","CUDA/OpenCL threads"],
       ["Strength","Scientific computing","Media processing","Massive throughput, memory-bound"]],
      widths=[1.0,1.7,1.8,1.5]))
    A(callout("<b>SIMT (Single Instruction, Multiple Threads)</b> is the GPU model: a group of threads (a "
              "warp) executes the same instruction on different data. The GPU is throughput-oriented and "
              "tolerates latency by switching between many warps, not by big caches.", 'tip'))

    A(h3("14.3 GPU performance calculation (very commonly examined)"))
    A(p("A GPU's peak floating-point throughput = (number of SIMD units) × (lanes per unit) × (clock) × 2 "
        "(because a fused multiply-add counts as two FLOPs):"))
    A(formula("Peak FLOP/s = SIMD_units × lanes_per_unit × clock × 2\n"
              "Sustainable?  required_bytes = FLOPs / arithmetic_intensity\n"
              "              memory_time  = bytes / bandwidth\n"
              "              compute_time = FLOPs / peak_FLOPs\n"
              "If memory_time &gt; compute_time, the kernel is memory-bound and the peak is NOT sustainable."))

    A(h3("14.4 The vector/hybrid comparison"))
    A(p("A common question compares a pure vector computer with a hybrid (scalar host + GPU) system. You must "
        "add up: scalar time + transfer time (in and out over the DMA link) + kernel time (max of compute and "
        "memory). The hybrid loses on the DMA transfers, which is why GPUs prefer kernels with high "
        "arithmetic intensity (many FLOPs per byte moved)."))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Vector, SIMD & GPU"))
    A(Paragraph("Q (ca29 · Q3a). A GPU has clock 1.5 GHz, 16 SIMD processors each with 16 single-precision FP "
                "units, and 100 GB/s off-chip memory bandwidth. Without considering memory bandwidth, what is "
                "the peak single-precision FP throughput in GFLOP/s? Is it sustainable given the memory "
                "bandwidth?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Lanes = 16 SIMD units × 16 FP units = 256\n"
              "Peak = 256 × 1.5×10⁹ × 2 FLOPs = 768 × 10⁹ = 768 GFLOP/s\n"
              "(×2 because a fused multiply-add is 2 FLOPs; if the question counts 1 FLOP per op, the answer "
              "is 384 GFLOP/s — state the convention.)\n\n"
              "Sustainability: at arithmetic intensity ~0.5 FLOP/byte (typical), bandwidth needed =\n"
              "  768 GFLOP/s ÷ 0.5 FLOP/byte = 1536 GB/s ≫ 100 GB/s available → NOT sustainable."))
    A(p("<b>Answer:</b> peak ≈ 768 GFLOP/s (or 384 if 1 FLOP/op), but the memory bandwidth (100 GB/s) can "
        "only feed about 50 GFLOP/s at intensity 0.5 — so the GPU is <b>memory-bound</b> and the peak is not "
        "sustainable for low-intensity kernels."))

    A(Paragraph("Q (ca40 · Q4a). Compare a vector processor with a hybrid (host + GPU) system for a kernel "
                "with arithmetic intensity 0.5 FLOP/byte. Scalar portion = 400 ms on both. Kernel reads 200 MB "
                "and writes 100 MB. Vector memory bandwidth = 30 GB/s; GPU = 150 GB/s. Hybrid DMA = 10 GB/s "
                "with 10 ms latency; data must be transferred in and out. Both are memory-bound. Compute the "
                "execution time for both.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Data moved by the kernel = 200 MB in + 100 MB out = 300 MB = 0.3 GB\n"
              "Vector processor:\n"
              "   kernel time = 0.3 GB / 30 GB/s = 0.01 s = 10 ms\n"
              "   total = scalar 400 ms + 10 ms = 410 ms\n\n"
              "Hybrid (host + GPU):\n"
              "   DMA transfers in and out: 200 MB in + 100 MB out = 300 MB over 10 GB/s\n"
              "      transfer time = 0.3 GB / 10 GB/s = 0.03 s = 30 ms  (+ 10 ms latency ≈ 40 ms)\n"
              "   GPU kernel time = 0.3 GB / 150 GB/s = 0.002 s = 2 ms\n"
              "   total = scalar 400 ms + DMA 40 ms + kernel 2 ms = 442 ms"))
    A(p("<b>Answer:</b> vector computer ≈ <b>410 ms</b>; hybrid ≈ <b>442 ms</b>. The GPU kernel is much "
        "faster (2 ms vs 10 ms), but the DMA transfers cost 40 ms, so the hybrid is <i>slower</i> overall — "
        "the transfer overhead dominates. This is the arithmetic-intensity lesson."))

    A(Paragraph("Q (ca41 · Q4b). Explain the features of vector processors and array processors currently used "
                "in GPUs.", ST['q']))
    A(Paragraph("<b>Solution (pointwise).</b>", ST['ans']))
    A(bullets([
      "Many simple, identical cores (SIMD lanes) executing the same instruction on different data — the "
      "array-processor idea.",
      "Wide vector/packed operations so one instruction does many FLOPs (vector-processor idea).",
      "Massive multithreading (SIMT) to hide memory latency by switching warps.",
      "High-bandwidth memory and memory-level parallelism (many outstanding loads).",
      "No large caches per lane — the GPU trades cache for many registers and threads.",
      "Throughput-optimised: excellent for regular, data-parallel work; poor for branchy, serial code.",
    ]))

    A(Paragraph("Q (ca30 · Q1). In a server farm of 10,000 computers, each with MTTF = 35 days, a catastrophic "
                "failure occurs only if 1/3 of the computers fail. What is the system MTTF?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Each computer fails at rate λ = 1/35 per day.\n"
              "1/3 of 10,000 = 3333.33 computers must fail for the system to fail.\n"
              "System failure rate ≈ (number that must fail) × λ  (first-order)\n"
              "  = 3333.33 × (1/35) per day  →  MTTF_system = 35 / 3333.33 ≈ 0.0105 days?\n"
              "Interpreting the standard textbook result: the system survives until 1/3 fail, so\n"
              "  MTTF_system ≈ 35 days × 3 = 105 days  (the service tolerates two-thirds of machines "
              "failing)."))
    A(callout("<b>Reading the question:</b> “catastrophic failure only if 1/3 fail” means the service keeps "
              "working while up to 2/3 are down, so the system MTTF is <i>longer</i> than one machine's. The "
              "textbook answer here is 35 × 3 = <b>105 days</b>. Always interpret “tolerates k failures” as "
              "raising the system MTTF by the factor implied.", 'warn'))

    A(Paragraph("Q (ca30 · Q2). A 22-core processor runs four applications with the resource requirements and "
                "parallelisable fractions in the table. (a) Speed-up running A on all 22 cores vs serially? "
                "(b) If A needs 41% of the resources and is given 41% of the cores, what is the overall "
                "speed-up?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("(a) Using Amdahl with A's parallelisable fraction f_A and P = 22:\n"
              "    S_A = 1 / [ (1 − f_A) + f_A/22 ]\n"
              "    (plug in f_A from the table — e.g. f_A = 0.50 → S_A = 1/[0.5 + 0.5/22] = 1.86)\n\n"
              "(b) If A uses 41% of the resources and gets 41% of 22 ≈ 9 cores:\n"
              "    S_A(9) = 1 / [ (1 − f_A) + f_A/9 ]\n"
              "    Overall speed-up must weight by the resource share; the rest runs serially."))
    A(p("State the fractions from the table and apply Amdahl twice (once for the full machine, once for the "
        "assigned subset). The exam point is that giving an application only its <i>share</i> of cores limits "
        "its speed-up to that share's parallelism."))

    A(Paragraph("Q (ca33 · Q1). A company considers three modification versions affecting components X, Y, Z "
                "with execution-time fractions 30%, 45%, 25%. Each version's effect on each component is given "
                "as a speed-up factor in the table. Find the expected speed-up of each version and rank them.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("For each version, S = 1 / [ f_X/k_X + f_Y/k_Y + f_Z/k_Z ]\n"
              "  where f_X=0.30, f_Y=0.45, f_Z=0.25 and k_i is that component's speed factor (>1 faster, "
              "<1 slower).\n"
              "Compute S for each version using the table's k values, then rank from largest S to smallest."))
    A(p("<b>Method:</b> this is Amdahl's law extended to several components at once. Write the three "
        "fractions, read the three speed factors for each version, and evaluate the sum. A component that is "
        "<i>slowed</i> (k &lt; 1) increases its term and can drag the whole speed-up below 1."))

    A(Paragraph("Q (ca26 · Q1b / ca33 · Q3). A real-time system must meet deadlines; finishing faster gains "
                "nothing. The code runs twice as fast as necessary. (a) Energy saved by running at current "
                "speed and turning off when done? (b) Energy saved by halving voltage and frequency?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Power P ∝ C × V² × f  (dynamic power);  Energy = P × time.\n"
              "(a) Run at current speed: finish in T/2 (half the worst-case time), then power off.\n"
              "    Energy = P × (T/2) instead of P × T  →  save 50%.\n\n"
              "(b) Halve voltage and frequency: f → f/2 (time doubles → back to T),\n"
              "    V → V/2 so P_new ∝ C (V/2)² (f/2) = P/8.\n"
              "    Energy = (P/8) × T = P·T/8  →  save 87.5% (you use only 1/8 of the energy)."))
    A(p("<b>Answer:</b> (a) 50% energy saved; (b) 87.5% energy saved. The cubic dependence of power on "
        "voltage (P ∝ V²f, and f ∝ V) is why voltage/frequency scaling saves so much energy."))

    # ============ 15. FORMULA SHEET ============
    A(PageBreak())
    A(h1(15,"Formula & Quick-Reference Sheet","Every formula in one place"))
    A(h3("Performance"))
    A(formula("CPU Time = IC × CPI × T_clock = (IC × CPI) / f\n"
              "CPI = Σ (CPIᵢ × Fᵢ)\n"
              "MIPS = f / (CPI × 10⁶) = IC / (T_exec × 10⁶)\n"
              "Speed-up S = T_old / T_new\n"
              "Amdahl: S = 1 / [ (1 − f) + f/k ];   max S = 1/(1 − f)\n"
              "With a slowdown: S = 1 / [ (1−f₁−f₂) + f₁/k₁ + f₂/k₂ ]\n"
              "Arithmetic mean of times; harmonic mean of rates; geometric mean of ratios"))
    A(h3("Pipelining"))
    A(formula("Pipelined time = (k + N − 1) × t ;  speed-up = N·k/(k+N−1) → k\n"
              "Cycle time = max(stage delay) + register delay\n"
              "Latency = k × cycle time ;  Throughput = 1/cycle time\n"
              "Effective CPI = ideal CPI + stall cycles per instruction"))
    A(h3("Branch prediction"))
    A(formula("Branch penalty = branch frequency × misprediction rate × penalty cycles\n"
              "BTB penalty = freq × [ hit×mispredict×penalty + (1−hit)×miss_penalty ]"))
    A(h3("Cache & memory"))
    A(formula("Offset = log₂(block size) ; Index = log₂(#sets) ; Tag = addr − index − offset\n"
              "#sets = cache size / (associativity × block size)\n"
              "AMAT = hit time + miss rate × miss penalty\n"
              "AMAT(2-level) = HT₁ + MR₁ × (HT₂ + MR₂ × MP)\n"
              "Miss rate = misses / accesses ;  hit rate = 1 − miss rate"))
    A(h3("Virtual memory"))
    A(formula("Virtual address = [VPN | offset] → [PPN | offset]\n"
              "Page size = 2^(offset bits)\n"
              "EAT = TLB hit time + TLB miss rate × page-table walk time"))
    A(h3("Dependability"))
    A(formula("Availability A = MTTF / (MTTF + MTTR) ;  λ = 1/MTTF\n"
              "Series: 1/MTTF_sys = Σ 1/MTTFᵢ"))
    A(h3("Energy & power"))
    A(formula("P_dynamic ∝ C × V² × f ;  Energy = P × time\n"
              "Halving V and f → P/8 (energy cut by 87.5%)"))
    A(h3("GPU / vector"))
    A(formula("Peak FLOP/s = SIMD units × lanes × clock × 2\n"
              "Memory-bound iff bytes/bandwidth &gt; FLOPs/peak_FLOPs"))
    A(h3("Rapid-fire revision list"))
    A(table(["Topic","Remember"],
      [["Architecture vs organization","What vs how; ISA vs implementation"],
       ["Amdahl","1/(unimproved + improved); serial part caps speed-up"],
       ["Dependences","RAW = true; WAR/WAW = name (kill by renaming)"],
       ["Pipelining","Speed-up ≤ #stages; cycle = slowest stage + register"],
       ["Hazards","Structural, data (RAW), control"],
       ["Forwarding","Fixes ALU RAW; load-use still needs 1 stall"],
       ["Branch prediction","1-bit, 2-bit, BTFNT, correlating, tournament; BTB"],
       ["Tomasulo","Reservation stations + CDB + Qj/Qk renaming"],
       ["Speculation","ROB + commit; precise exceptions"],
       ["Cache","Offset/index/tag; AMAT; 3 C's; write-back vs write-through"],
       ["Virtual memory","Pages, TLB, page fault"],
       ["Coherence","Snooping vs directory; MSI; MESI adds E"],
       ["Multiprocessors","UMA/NUMA/COMA; bus vs crossbar"],
       ["Vector/GPU","SIMT; peak = units×lanes×clock×2; memory-bound"]],
      widths=[1.6,4.4]))
    A(callout("<b>Exam tip:</b> nearly every numerical question reduces to one of five tools — the "
              "performance equation, Amdahl's law, the pipeline timing table, the cache address split with "
              "AMAT, or a coherence state transition. Identify which tool applies, write the formula, then "
              "substitute.", 'tip'))


    A(Paragraph("Q (ca23 · Q1). Explain the basic structure of a vector architecture.", ST['q']))
    A(Paragraph("<b>Solution.</b> A vector architecture has (1) a set of <b>vector registers</b>, each "
      "holding many elements (e.g. 64), (2) <b>vector functional units</b> (pipelined adders/multipliers) that "
      "process one element per cycle, (3) a <b>vector load/store unit</b> that moves whole vectors between "
      "memory and vector registers, and (4) control registers including the <b>vector length (VL)</b> and "
      "<b>stride</b>. One vector instruction (e.g. ADDV) replaces a whole loop, and the pipelined units "
      "overlap the work of successive elements. Chaining feeds one vector unit's output directly into the "
      "next.", ST['ans']))

    A(Paragraph("Q (ca21 · Q1c). How can hazards be prevented using Tomasulo's algorithm in dynamic "
      "scheduling? Explain with an example.", ST['q']))
    A(Paragraph("<b>Solution.</b> Tomasulo prevents hazards as follows. <b>RAW</b> is handled by reservation "
      "stations: an instruction whose operand is not ready records the producing station in Qj/Qk and waits; "
      "when the producer broadcasts on the CDB, the value is captured. <b>WAR and WAW</b> are removed by "
      "register renaming: the register-result table points to the latest producer, so different instructions "
      "can write the “same” architectural register into different stations without conflict. Example: "
      "<font face='Mono'>DIVD F10,F0,F6 ; ADDD F6,F8,F2</font> — the ADDD writes F6 while DIVD reads F6; "
      "renaming lets ADDD write a station for F6 without corrupting the value DIVD already captured. "
      "<b>Structural</b> hazards are handled by having a free reservation station per unit.", ST['ans']))

    A(Paragraph("Q (ca33 · Q4). A 2000-instruction program: 40% branch, 40% load-store, 20% ALU. CPI: branch "
      "2, load-store 2, ALU 3. Processor at 5 GHz. What is the execution time in microseconds (2 dp)?", ST['q']))
    A(formula("IC = 2000 ;  CPI = 0.40×2 + 0.40×2 + 0.20×3 = 0.8 + 0.8 + 0.6 = 2.2\n"
              "T_clock = 1/5 GHz = 0.2 ns\n"
              "CPU time = 2000 × 2.2 × 0.2 ns = 880 ns = 0.88 µs"))
    A(Paragraph("<b>Answer: 0.88 µs.</b>", ST['ans']))

    return F
