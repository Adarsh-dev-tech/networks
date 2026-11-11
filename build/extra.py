"""New sections authored to match topics present in the handwritten notes
but missing / thin in the previous guide.  Each value is the exact source of
the A(...) statements for that section (already 4-space indented)."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

EXTRA = {}

EXTRA['cache_levels'] = r'''
    A(h3("Levels of cache (the memory hierarchy in practice)"))
    A(p("A modern CPU does not have one cache — it has a <b>hierarchy</b> of small, fast, expensive "
        "caches close to the core and larger, slower, cheaper caches further away. The whole hierarchy "
        "exists because of <b>locality</b>: a small memory near the core can serve most of the "
        "references most of the time."))
    A(fig("page003.jpg", w=11.0*gen.cm, cap="Levels of cache: L1 (split into instruction and data), L2, L3, then main memory (source: notes p. 3)."))
    A(p("<b>Reading the figure.</b> Notice the pyramid: registers at the top (smallest, fastest), then L1 split into I-cache and D-cache, then L2, L3 and finally main memory (DRAM) at the bottom (largest, slowest). Every level is a cache for the level below it, and a miss at one level sends the request down to the next. The split L1 removes the structural hazard between instruction fetch and data access."))
    A(bullets([
        "<b>L1</b> — smallest (typically 16–64 KB), fastest (1–3 cycles), built into the core.",
        "<b>L1 is split</b> into an <i>instruction</i> cache and a <i>data</i> cache so that the "
        "fetch stage and the memory stage can be accessed in the same cycle without fighting over one port.",
        "<b>L2</b> — larger (256 KB–1 MB), slower (≈10–20 cycles), usually private to a core.",
        "<b>L3</b> — largest on-chip cache (several MB), shared between cores, ≈30–50 cycles.",
        "<b>Main memory</b> (DRAM) — hundreds of cycles; if the data is not in any cache we must search "
        "the whole hierarchy (L1 → L2 → L3 → RAM) before it can be used.",
    ]))
    A(callout("<b>Advantage:</b> it improves the <i>average</i> access time, because most accesses hit "
        "in the small fast levels. <b>Disadvantage:</b> the design and control get complex — we must "
        "decide inclusion, replacement and coherence between the levels.", 'tip'))
    A(p("<b>Why split L1 into I-cache and D-cache?</b> The instruction fetch unit and the load/store unit "
        "issue requests in the same cycle. A single unified L1 would need two read ports, which is "
        "expensive and slow. Splitting gives each unit its own single-ported cache and removes the "
        "structural hazard."))
'''

EXTRA['parallelism_levels'] = r'''
    A(h3("Levels of parallelism"))
    A(p("Parallelism can be exploited at several levels. From the smallest grain to the largest:"))
    A(table(["Level","What is done in parallel","Example"],
      [["Bit level","Several bits of one word added at once","Carry-look-ahead adder, 64-bit ALU"],
       ["Instruction level","Several independent instructions overlap","Pipelining, superscalar, VLIW"],
       ["Data level","The same operation on many data items","SIMD / vector / GPU"],
       ["Task / thread level","Independent programs or threads","Multithreading, multicore, cluster"]],
      widths=[1.15,2.15,1.7]))
    A(p("The main hardware techniques that <b>increase instruction-level parallelism</b> are:"))
    A(bullets([
        "<b>Pipelining</b> — overlap the stages of different instructions; ideal CPI = 1.",
        "<b>Superscalar</b> — issue more than one instruction per cycle using several parallel pipes; "
        "CPI &lt; 1 is possible.",
        "<b>VLIW</b> — the compiler packs several independent operations into one very long instruction.",
        "<b>Out-of-order execution</b> — the hardware reorders instructions dynamically (scoreboard, Tomasulo).",
        "<b>Speculation</b> — guess the branch and execute ahead, then commit only if correct.",
        "<b>Multithreading</b> — several threads share one core and hide each other's stalls.",
    ]))
    A(callout("<b>Limit.</b> Parallelism is bounded by true (data and control) dependences. Amdahl's Law "
        "tells us that the serial part of the program sets a hard ceiling no matter how much parallel "
        "hardware we add.", 'tip'))
'''

EXTRA['parallel_arch_intro'] = r'''
    A(h3("Parallel computers — definition and why we build them"))
    A(p("A <b>parallel computer</b> is a computer in which several processors (processing elements, PE) "
        "cooperate to solve one problem faster. Every parallel computer is built from three ingredients:"))
    A(bullets([
        "1) <b>Processing elements</b> — the units that actually execute instructions.",
        "2) <b>Memory modules</b> — where instructions and data live (shared, distributed, or hybrid).",
        "3) <b>An interconnection network</b> — the communication path that lets the PEs talk to memory "
        "and to each other.",
    ]))
    A(p("<b>Why go parallel?</b> (i) The clock frequency can no longer be scaled freely — power and heat "
        "rise with frequency, so performance must come from parallelism; (ii) it is often cheaper to add "
        "many modest processors than to build one extremely fast processor; (iii) some problems "
        "(weather, graphics, simulation) are naturally parallel."))
    A(h3("How parallel computers are classified"))
    A(p("The notes list five different classification viewpoints. Any exam question on 'classification of "
        "parallel computers' can be answered from this list:"))
    A(bullets([
        "1) <b>Based on processing elements</b> — how many PEs and how they are organised.",
        "2) <b>Based on the interconnection network</b> — bus, crossbar, multistage, hypercube, mesh, …",
        "3) <b>Based on the memory arrangement</b> — shared memory, distributed memory, hybrid.",
        "4) <b>Based on granularity of processing</b> — fine-grained (many small tasks) vs coarse-grained "
        "(few large tasks).",
        "5) <b>Flynn's classification</b> — by instruction and data streams (SISD, SIMD, MISD, MIMD).",
    ]))
'''

EXTRA['simd_mimd'] = r'''
    A(h3("SIMD and MIMD machines in detail"))
    A(p("<b>SIMD (Single Instruction stream, Multiple Data stream).</b> One control unit broadcasts the "
        "same instruction to many processing elements, each working on a different data element. "
        "Example: add two arrays, c[i] = a[i] + b[i] for i = 0…n−1, in one (vectorised) operation:"))
    A(formula("for i in 0…n−1 :  c[i] = a[i] + b[i]\n"
              "One instruction (ADD) → n data elements processed together.\n"
              "Speed-up ≈ n compared with a scalar loop (ignoring overhead)."))
    A(fig("page006.jpg", w=11.0*gen.cm, cap="SIMD and MIMD organisations: one instruction stream to many PEs (SIMD) vs many independent instruction streams (MIMD) (source: notes p. 6)."))
    A(p("<b>Reading the figure.</b> Read the four quadrants. SIMD (one instruction, many data) is the vector/GPU idea — every PE gets the same opcode but its own data. MIMD (many instructions, many data) is the multicore idea — each processor runs its own program. SISD is the ordinary scalar CPU; MISD is only theoretical."))
    A(p("<b>MIMD (Multiple Instruction stream, Multiple Data stream).</b> Each processor runs its own "
        "instruction stream on its own data. MIMD machines split further by how memory is attached:"))
    A(table(["Model","Meaning","Communication"],
      [["Shared memory (UMA)","All PEs see one global address space","Loads/stores to shared RAM"],
       ["Distributed memory","Each PE has private memory","Message passing over the network"],
       ["Hybrid (NUMA)","Private memories, one global address space","Remote loads take longer than local"]],
      widths=[1.35,2.05,1.6]))
    A(callout("<b>Exam point.</b> SIMD requires all the data to be laid out regularly (a vector). MIMD is "
        "the general-purpose model used by multicore CPUs; it needs no such regularity but requires "
        "synchronisation and communication between the processors.", 'tip'))
'''

EXTRA['shared_dist_memory'] = r'''
    A(h3("Shared memory vs distributed memory"))
    A(p("The single most important structural distinction in multiprocessors is whether the memory is "
        "shared or distributed."))
    A(fig("page007.jpg", w=11.0*gen.cm, cap="Shared-memory and distributed-memory multiprocessors, and the UMA / NUMA / COMA sub-classification (source: notes p. 7)."))
    A(p("<b>Reading the figure.</b> Compare the two halves. On the left, shared memory: all processors reach one central RAM (UMA — uniform access time). On the right, distributed memory: each processor has its own RAM and they communicate by messages. NUMA and COMA are the hybrids — a single address space, but local memory is faster than remote."))
    A(bullets([
        "<b>Shared memory (UMA).</b> One physical memory accessed by every processor. Uniform access "
        "time. Programming is easy (ordinary loads and stores) but the bus/memory becomes the bottleneck.",
        "<b>Distributed memory.</b> Each processor has its own private memory; processors communicate "
        "by passing messages. It scales well, but the programmer must manage communication.",
        "<b>NUMA (Non-Uniform Memory Access).</b> A hybrid: a single global address space, but each "
        "processor has a local memory that is faster than remote memory. Performance depends on where "
        "the data lives.",
        "<b>COMA (Cache-Only Memory Architecture).</b> All main memory is treated as cache; data "
        "migrates to the node that is using it.",
    ]))
    A(formula("Access time (NUMA):  T = f · T_local + (1 − f) · T_remote ,   T_remote > T_local\n"
              "f = fraction of accesses served locally"))
'''

EXTRA['topologies'] = r'''
    A(h3("Interconnection networks and topologies"))
    A(p("The interconnection network decides how fast processors can exchange data, and it is one of the "
        "most heavily examined topics. Networks are first split into two families:"))
    A(bullets([
        "<b>Direct (static) network</b> — every node is both a processor and a switch; the topology is "
        "fixed (mesh, torus, hypercube, tree).",
        "<b>Indirect (dynamic) network</b> — separate switches connect the processors; the path can "
        "change from one transfer to the next (bus, crossbar, multistage network).",
    ]))
    A(h3("Bus-based networks"))
    A(p("A <b>bus</b> is a single shared communication path. It is simple and cheap, but only one "
        "transfer can happen at a time, so it does not scale."))
    A(fig("page008.jpg", w=11.0*gen.cm, cap="Bus-based multiprocessor: all processors share one communication path (source: notes p. 8)."))
    A(p("<b>Reading the figure.</b> All processors sit on one shared bus. It is cheap and simple, but only one transfer can happen at a time, so contention grows quickly with the number of processors — this is why a bus does not scale past a handful of cores."))
    A(p("A <b>multistage / multiple bus</b> uses several buses to reduce contention, at the cost of extra "
        "hardware. The classic indirect network is the <b>crossbar</b>:"))
    A(bullets([
        "<b>Crossbar</b> — every input can be connected to every output through a switch matrix. "
        "Non-blocking: all n processors can talk at once. Cost grows as O(n²) switches, so it is used "
        "only for small n.",
        "<b>Multistage (e.g. omega/butterfly)</b> — log₂n stages of small switches; cost O(n log n), "
        "between a bus and a crossbar.",
    ]))
    A(h3("Direct topologies"))
    A(fig("page011.jpg", w=11.0*gen.cm, cap="Hypercube and tree topologies with node addresses (source: notes p. 11)."))
    A(p("<b>Reading the figure.</b> Each hypercube node is labelled with a d-bit address; two nodes are neighbours when their addresses differ in exactly one bit, so the diameter is only log₂n. The tree is cheaper to build but its root becomes a bottleneck as traffic concentrates near the top."))
    A(table(["Topology","Degree","Diameter","Bisection width","Cost / comment"],
      [["Linear array","2","n − 1","1","cheapest, slowest"],
       ["Ring / torus","2 / 4","n/2 / n/2","2 / 2√n","wrap-around reduces diameter"],
       ["2-D mesh","4","2(√n − 1)","√n","simple to build, good locality"],
       ["Binary tree","3","2 log₂n","1","cheap, root is a bottleneck"],
       ["Hypercube (n = 2ᵈ)","d = log₂n","log₂n","n/2","excellent diameter, cost O(n log n)"],
       ["Crossbar","n","1","n","non-blocking, cost O(n²)"]],
      widths=[1.25,0.8,0.95,0.95,1.05]))
    A(p("The four numbers used to compare topologies are:"))
    A(bullets([
        "<b>Degree</b> — number of links per node (hardware cost).",
        "<b>Diameter</b> — maximum number of hops between any two nodes (worst-case latency).",
        "<b>Bisection width</b> — number of links that must be cut to split the network in half "
        "(bandwidth under worst-case traffic).",
        "<b>Cost</b> — total number of links/switches.",
    ]))
    A(formula("Hypercube with n = 2ᵈ nodes:  degree = d ,  diameter = d ,  links = n·d / 2\n"
              "Each node address is d bits; two nodes are neighbours if their addresses differ in 1 bit."))
'''

EXTRA['dvfs'] = r'''
    A(h3("Voltage, power and frequency scaling (DVFS)"))
    A(p("Why can we not simply raise the clock forever? Because dynamic power rises with both frequency "
        "and the square of the voltage:"))
    A(formula("P_dynamic = C · V² · f      (C = switched capacitance, V = supply voltage, f = frequency)\n"
              "P_total   = P_dynamic + P_static ,   P_static ∝ V · I_leak\n"
              "Energy    = P · t        (joules)"))
    A(p("<b>DVFS (Dynamic Voltage and Frequency Scaling)</b> lowers both V and f together to save energy "
        "with only a modest performance loss, because voltage and frequency can often be reduced by the "
        "same factor. Reducing V by 20% and f by 20% cuts dynamic power by ≈ 0.8² × 0.8 ≈ 51%."))
    A(callout("<b>Consequences (notes p. 23).</b> (1) We hit a <b>power wall</b>: heat cannot be removed "
        "fast enough, so the clock stopped scaling around 2004. (2) The industry moved from raising "
        "frequency to adding <b>more cores</b> (the multicore shift). (3) Cooling, packaging and battery "
        "life become first-class design constraints.", 'tip'))
'''

EXTRA['superscalar'] = r'''
    A(h3("Superscalar and deeper pipelines"))
    A(p("A <b>superscalar</b> processor fetches, decodes and issues several instructions per cycle using "
        "multiple parallel execution units. It is 'scalar' (each instruction works on one data item) but "
        "it can start more than one per cycle."))
    A(bullets([
        "<b>Superscalar</b> — hardware finds the independent instructions at run time; CPI can fall below 1.",
        "<b>VLIW</b> — the compiler packs independent operations into one long instruction word; "
        "simpler hardware, but the compiler does the scheduling and the code is not portable.",
        "<b>Deeper pipeline</b> — more stages give a shorter clock period but a larger penalty per "
        "mispredicted branch and more hazard-checking logic.",
    ]))
    A(formula("Superscalar of width m (ideal):  CPI = 1/m ,   speed-up ≤ m\n"
              "Real speed-up is lower because of dependences, hazards and limited issue width."))
    A(callout("<b>Trade-off.</b> Doubling the issue width does <i>not</i> double performance, because "
        "programs rarely contain enough independent instructions to keep all the pipes full. This is the "
        "same ILP limit that Amdahl's Law expresses at the program level.", 'tip'))
'''

EXTRA['cpu_time_metrics'] = r'''
    A(h3("CPU time, CPI, MIPS and benchmarks — the metric toolkit"))
    A(p("All performance numbers in this subject are built from one master equation. Learn it and every "
        "problem becomes substitution:"))
    A(formula("CPU time = Instruction count (IC) × CPI × Clock cycle time\n"
              "         = IC × CPI / Clock rate (f)\n"
              "CPI = Clock cycles per instruction = Σ (CPI_i × F_i),  F_i = fraction of instruction type i\n"
              "MIPS = IC / (Execution time × 10⁶) = Clock rate / (CPI × 10⁶)"))
    A(p("<b>Worked example (notes p. 28).</b> A program has instruction mix: ALU 40% (CPI 1), Load/Store "
        "20% (CPI 2), Control 30% (CPI 3), others 10% (CPI 4). Then"))
    A(formula("CPI = 0.4×1 + 0.2×2 + 0.3×3 + 0.1×4 = 0.4 + 0.4 + 0.9 + 0.4 = 2.1\n"
              "If clock = 2 GHz and IC = 10⁹:  CPU time = 10⁹ × 2.1 / 2×10⁹ = 1.05 s"))
    A(p("<b>Choosing a metric.</b> MIPS is only comparable between machines with the same ISA (it "
        "ignores the work done per instruction). For whole-program comparison use execution time; for "
        "benchmark suites use the <b>geometric mean</b> of the ratios."))
    A(table(["Mean","Formula","Used for"],
      [["Arithmetic mean","(1/n) Σ Tᵢ","Total time of fixed work"],
       ["Harmonic mean","n / Σ(1/Rᵢ)","Average rate (throughput, MIPS)"],
       ["Geometric mean","(Π Rᵢ)^(1/n)","Averaging normalised benchmark ratios"]],
      widths=[1.2,2.0,1.8]))
'''

EXTRA['tomasulo_worked'] = r'''
    A(h3("A full worked Tomasulo example (issue → execute → write result)"))
    A(p("The notes (pp. 56–60) trace the classic sequence below. Learn the <b>three steps</b> of every "
        "instruction and the three tables, and you can reproduce any exam example."))
    A(formula("L.D   F6, 32(R2)        ; load into F6\n"
              "L.D   F2, 44(R3)        ; load into F2\n"
              "MUL.D F0, F2, F4        ; F0 = F2 × F4   (multiply latency 10)\n"
              "SUB.D F8, F6, F2        ; F8 = F6 − F2   (add latency 2)\n"
              "DIV.D F10, F0, F6       ; F10 = F0 / F6  (divide latency 40)\n"
              "ADD.D F6, F8, F2        ; F6 = F8 + F2"))
    A(bullets([
        "<b>Issue.</b> If a free reservation station exists, send the op and the operands; rename the "
        "destination register to the station's tag. Otherwise <i>stall</i>.",
        "<b>Execute.</b> When both operands are ready (Vⱼ and Vₖ valid), start execution in a functional "
        "unit. If an operand is still pending, wait and snoop the CDB.",
        "<b>Write result.</b> Broadcast the result on the CDB; every station waiting for that tag grabs "
        "it, and the register file is updated.",
    ]))
    A(p("For the sequence above: MUL.D must wait for the second L.D (F2), and DIV.D must wait for MUL.D "
        "(F0) and the first L.D (F6). SUB.D can run as soon as F6 and F2 are loaded. The reservation "
        "stations hold the operands so that the CDB broadcasts only once per producing instruction."))
    A(fig("page057.jpg", w=11.0*gen.cm, cap="Tomasulo instruction-status and reservation-station tables for the worked example (source: notes p. 57)."))
    A(p("<b>Reading the figure.</b> Follow the two tables together. The left table lists each instruction with its Issue / Execute / Write-result cycles; the right table is the reservation stations. When an instruction writes its result, the CDB broadcast clears the Q (producer) field of every station waiting on that tag and fills in the value — that is how the data dependency resolves."))
    A(callout("<b>Marking scheme.</b> Draw the reservation stations with the columns Op, Qⱼ, Vⱼ, Qₖ, Vₖ, "
        "A (address). Use '–' when a value is already available and a tag (e.g. 'Mult1') when it is not. "
        "Tick the clock cycle in which each instruction issues, starts execution and writes its result.", 'tip'))
'''


EXTRA['fig_p4'] = r'''
    A(fig("page004.jpg", w=10.5*gen.cm, cap="Levels of parallelism, RISC/CISC and the UMA / NUMA / COMA classification (source: notes p. 4)."))
    A(p("<b>Reading the figure.</b> This page ties three ideas together: the levels of parallelism (bit → instruction → data → task), the RISC-versus-CISC contrast, and the UMA / NUMA / COMA memory models. Use it as the one-page map of the classification material."))
'''

# ---- coverage map + audit (data-driven) ----
PAGE_MAP = {
 1:"Cover page (GoodNotes template); no academic content",
 2:"§1 Architecture vs organization; stored-program model",
 3:"§1 Levels of cache (L1 split I/D, L2, L3, RAM); §12 cache search on a miss",
 4:"§1 Levels of parallelism; RISC vs CISC (first pass); UMA/NUMA/COMA",
 5:"§1 Parallel computers: definition, need, five classifications",
 6:"§1 SIMD and MIMD organisations; vector example c[i]=a[i]+b[i]",
 7:"§1/§10 Shared vs distributed memory; UMA/NUMA/COMA sub-classification",
 8:"§10 Bus-based multiprocessor",
 9:"§10 Multistage (multiple) bus; crossbar topology",
 10:"§10 Mesh, hypercube, tree, torus topologies",
 11:"§10 Hypercube and tree; §14 vector/array processor (first pass)",
 12:"§3 RISC vs CISC; classification based on the processor",
 13:"§2 RISC/CISC implications for pipelining and CPI; vector processor",
 14:"§5 Pipelining (5 stages); §1 levels of parallelism",
 15:"§3 IEEE-754 floating-point addition example",
 16:"§14 Superscalar; SIMD; systolic idea",
 17:"§14 Systolic arrays; §15 multicore thermal/power note",
 18:"§3 ISA; ARM example; RISC architecture",
 19:"§2 Speed-up and Amdahl's law (derivation, T=I×CPI×T_c)",
 20:"§2 Amdahl; integer vs floating-point instruction mix",
 21:"§2 Amdahl worked PYQ (enhance fraction)",
 22:"§2 Amdahl worked PYQ (continued)",
 23:"§2/§15 Voltage, power and frequency scaling (power wall)",
 24:"§4 Cost of an integrated circuit; MTTF, MTTR, availability",
 25:"§4 MTTF and failure rate; worked examples",
 26:"§4 Reliability PYQs (parallel server, disk failure)",
 27:"§4 Availability; §2 performance-metric bridge",
 28:"§2 CPU time = IC × CPI × clock; worked instruction-mix example",
 29:"§2 Components of CPU time (compiler, ISA, organisation, hardware)",
 30:"§2 CPU-time / MIPS PYQ (instruction classes)",
 31:"§2 CPU-time PYQ worked calculations",
 32:"§2 CPU-time PYQ (continued)",
 33:"§5 Characteristics of pipelining; speed-up; timing table",
 34:"§5 Pipeline stages; instruction fetch and PC update",
 35:"§5 Pipeline timing; load-use stall",
 36:"§5 Pipeline; forwarding; load vs store handling",
 37:"§7 Branch predictor (one-bit and two-bit)",
 38:"§7 Tournament (hybrid) branch predictor",
 39:"§7 One-bit predictor state machine",
 40:"§7 Two-bit saturating predictor state machine",
 41:"§7 Two-bit / correlating predictor",
 42:"§8 Register renaming with a reorder buffer",
 43:"§8 Reservation-station fields (Op, Vj, Vk, Qj, Qk, A)",
 44:"§8 Tomasulo reservation-station / register tables",
 45:"§7/§6 Branch prediction; parallelisation and CPI",
 46:"§6 Loop unrolling; WAR/WAW/RAW dependences",
 47:"§8 Tomasulo worked example (tables)",
 48:"§8 Tomasulo worked example (continued)",
 49:"§6 Loop unrolling and scheduling",
 50:"§6 Loop-unrolling worked example",
 51:"§6 Unroll-until-no-stalls schedule",
 52:"§6 Instruction scheduling rules",
 53:"§9 Precise exceptions; speculation (exceptions in flight)",
 54:"§8 Tomasulo hardware diagram (RS, load/store buffers, CDB)",
 55:"§9 Speculation: issue, execute, read, write, commit",
 56:"§8 Tomasulo instruction-status table",
 57:"§8 Tomasulo instruction-status and reservation-station tables",
 58:"§8 Tomasulo tables (continued)",
 59:"§8 Tomasulo tables (continued)",
 60:"§8 Tomasulo tables (continued)",
 61:"§14 Superscalar processors; vector/loop operations",
 62:"§14 Vector/loop example; loop scheduling",
 63:"§6/§9 Loop scheduling with speculation",
 64:"§6/§9 Loop scheduling with speculation (continued)",
 65:"§9 Speculation timing table (issue/execute/read/write/commit)",
 66:"§9 Speculation timing table (continued)",
 67:"Blank / illegible page (only a heading fragment visible)",
 68:"§10 UMA shared memory; multicore with private caches",
 69:"§11/§10 Cache and coherence block diagram",
 70:"§11 Cache basics; direct mapping (block = mod)",
 71:"§11 Replacement policies (intro); associativity",
 72:"§11 Set-associative cache organisation",
 73:"§11 Replacement policies: FIFO, LRU, optimal, random",
 74:"§11 Direct-mapped cache worked example (address split)",
 75:"§11 Cache address split (tag/index/offset) worked example",
 76:"§11 Write-through vs write-back; write-allocate",
 77:"§11 Write policies: write-through, write-back, write-allocate, no-write-allocate",
 78:"§11 Write-allocate / write-back combinations",
 79:"§11 Write policies summary; AMAT (hit time + miss rate × miss penalty)",
 80:"§11 Multi-level caches; inclusive/exclusive; local vs global miss rate",
 81:"§11 Prefetching (hardware and software)",
 82:"§12 Virtual memory: address translation, TLB, page faults",
 83:"§15 Summary of instruction-level optimisations (multicast, speculation, branch prediction, loop unroll, Tomasulo, caches)",
 84:"§13 Cache coherence; MSI/MESI; snooping vs directory",
 85:"§13 MSI example (shared bus, write-invalidate)",
 86:"§13 MSI example (continued); directory-based protocol",
 87:"§13 MSI example (continued); write policy for a shared block",
}

EXTRA['coverage_map'] = None  # built programmatically below

def build_coverage():
    rows=[]
    for pg in range(1,88):
        topic = PAGE_MAP.get(pg, "—")
        rows.append([str(pg), topic])
    return rows

def build_audit():
    return None



