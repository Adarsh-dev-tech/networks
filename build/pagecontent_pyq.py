"""Per-image previous-year-question transcriptions and full solutions (ca1..ca41)."""

PYQS = {}

PYQS[1] = dict(
 title="ca1 — Performance (MIPS, CPU time), pipelining speed-up, loop dependences",
 transcript="""Answer All Questions
1. a. We want to compare computers R1 and R2, which differ in that R1 has machine
      instructions for floating-point operations, while R2 does not (FP operations are
      implemented in software using several non-FP instructions). Both have a clock
      frequency of 400 MHz. In both we run the same program, which has the following
      instruction mix:  (2.5)
        Type            Dynamic share   Instruction duration (CPI)
                        (p_i)           R1      R2
        FP addition     16%             4       —
        FP multiplication 10%           6       —
        FP division      8%            10       —
        Non-FP instructions 66%         3       2
   (i)  Calculate the MIPS for R1 and R2.
   (ii) Calculate the CPU execution time on R1 and R2 if there are 12000 instructions.
   b. Assuming N instructions are executed and all are add instructions (taking A clock
      cycles), what is the speed-up of a pipelined implementation compared with a
      multi-cycle implementation? (function of N; clock cycle = 305 ps)  (2.5)
2. a. In the loop below find all true dependences, output dependences and
      anti-dependences. Eliminate the output and anti-dependences by renaming. (2.5)
        for (i=0; i<100; i++) {
            A[i] = A[i] * B[i];   /* S1 */
            B[i] = A[i] + c;      /* S2 */
            A[i] = C[i] * c;      /* S3 */
            C[i] = D[i] * A[i];   /* S4 */
        }""",
 explain=r'''
    A(h3("Part 1a — MIPS and CPU time"))
    A(p("Average CPI is the sum of (share × CPI) over the instruction classes. For R1 the FP "
        "classes exist; for R2 the FP work is done in software, so the shares differ. Using the printed "
        "figures (R1: FP add 16%·4, FP mul 10%·6, FP div 8%·10, non-FP 66%·3):"))
    A(formula("R1: CPI = 0.16×4 + 0.10×6 + 0.08×10 + 0.66×3\n"
              "       = 0.64 + 0.60 + 0.80 + 1.98 = 4.02\n"
              "MIPS = f / (CPI × 10⁶) = 400×10⁶ / (4.02×10⁶) ≈ 99.5 MIPS\n\n"
              "CPU time = IC × CPI / f = 12000 × 4.02 / 400×10⁶ = 4.824×10⁴ / 4×10⁸\n"
              "         = 1.206×10⁻⁴ s ≈ 120.6 µs"))
    A(p("For R2 the FP operations are emulated by many non-FP instructions, so the effective CPI is "
        "lower per instruction but many more instructions are executed. Substituting the printed R2 "
        "column gives the R2 CPI, then MIPS and CPU time by the same two formulas."))
    A(formula("R2: CPI ≈ 2 (non-FP column); MIPS = 400×10⁶/(2×10⁶) = 200 MIPS\n"
              "CPU time = IC × CPI / f  (IC larger because FP is expanded into several instructions)"))
    A(h3("Part 1b — pipelined vs multi-cycle speed-up"))
    A(formula("Multi-cycle time for N instructions, A cycles each:   T_mc = N · A · T\n"
              "Pipelined time (k = A stages):                        T_p  = (A + N − 1) · T\n"
              "Speed-up = T_mc / T_p = N·A / (N + A − 1)"))
    A(p("With clock cycle T = 305 ps the speed-up is an expression in N (the clock cancels): "
        "S(N) = N·A/(N + A − 1). As N → ∞ the speed-up approaches A (the number of stages)."))
    A(h3("Part 2a — dependences in the loop"))
    A(p("For each pair of statements sharing a location, classify the dependence:"))
    A(table(["Statements","Location","Dependence","Why"],
      [["S1 → S2","A[i]","RAW (true)","S2 reads A[i] written by S1"],
       ["S1 → S3","A[i]","WAW (output)","Both write A[i]"],
       ["S2 → S3","A[i]","WAR (anti)","S3 overwrites A[i] that S2 read"],
       ["S3 → S4","A[i]","RAW (true)","S4 reads A[i] written by S3"],
       ["S1 → S4","A[i]","WAR/WAW","overwritten by S3 before S4"]],
      widths=[1.1,0.9,1.2,2.6]))
    A(formula("Rename the registers holding A[i] to remove WAW and WAR:\n"
              "  A1 = A[i]*B[i];      /* S1 */\n"
              "  B[i] = A1 + c;       /* S2 */\n"
              "  A2 = C[i]*c;         /* S3 */\n"
              "  C[i] = D[i]*A2;      /* S4 */\n"
              "The true (RAW) dependences S1→S2 and S3→S4 remain; the false ones are gone."))
''')

PYQS[2] = dict(
 title="ca2 — Loop dependences / parallelisation; MSI cache-coherence snapshot",
 transcript="""b. Consider the loop:  (2.5)
     for (i=0; i<100; i++) {
        A[i] = A[i] + B[i];   /* S1 */
        B[i] = C[i] + D[i];   /* S2 */
     }
   Are there dependences between S1 and S2? Is this loop parallel? If not, show how
   to make it parallel.

2. Explain the two classes of coherence protocols. A snapshot of the state of 2 caches
   on 2 separate cores in a centralized shared-memory system is shown. Coherence is
   maintained with an MSI snooping protocol; caches are direct-mapped. (10)
     (Cache P0 and cache P1 tables with Tag / Data words / Coherency state)
     i.   If P0 wants to write Block 0, what happens to its coherency state?
     ii.  If P1 writes to Block 1, is Block 1 on P0 invalidated? Why?
     iii. If P1 brings in Block M for reading, and no other cache has a copy, what
          state is it cached in?""",
 explain=r'''
    A(h3("Part b — dependences in the two-statement loop"))
    A(p("S1 reads/writes A[i] and reads B[i]; S2 reads C[i], D[i] and writes B[i]. The only shared "
        "location is B[i]: S1 reads B[i] and S2 writes it — a <b>WAR (anti-dependence)</b>. Because "
        "different iterations touch different indices, there is no <i>loop-carried</i> dependence, so the "
        "iterations are independent and the loop <b>is parallel</b> across i."))
    A(formula("S1: A[i] = A[i] + B[i]     (reads B[i])\n"
              "S2: B[i] = C[i] + D[i]     (writes B[i])\n"
              "→ WAR on B[i] within one iteration, but no dependence between\n"
              "  different i, so iterations can run in parallel (rename B to be safe)."))
    A(h3("The two classes of coherence protocol"))
    A(bullets([
        "<b>Snooping</b> — every cache watches a shared bus; writes are broadcast and other copies are "
        "invalidated or updated. Simple, but needs a broadcast medium.",
        "<b>Directory-based</b> — a directory records which caches hold each block; messages go only to "
        "the sharers, so it scales to large systems.",
    ]))
    A(h3("The MSI snapshot"))
    A(formula("(i)  P0 writes Block 0:  its state goes S → M (or I → M if it missed);\n"
              "     every other copy of Block 0 is invalidated (→ I).\n"
              "(ii) P1 writes Block 1:  yes — P0’s copy of Block 1 is invalidated (→ I),\n"
              "     because the write-invalidate protocol keeps only the writer’s copy valid.\n"
              "(iii) P1 reads Block M with no other sharer:  it is cached in state\n"
              "     S (shared) under MSI; under MESI it would be E (exclusive)."))
''')

PYQS[3] = dict(
 title="ca3 — Architecture vs organization, Amdahl, caches, virtual memory, FPSQR design, power",
 transcript="""Date: 19.09.2022     Answer ALL Questions     Max Marks: 20
1. What is the difference between computer architecture and computer organization? (2)
2. Derive and explain Amdahl’s law. (3)
3. What are pros and cons of each cache organization? (3)
4. What is virtual memory? Explain the need for virtual memory. (2)
5. Measurements: FP frequency = 25%, average CPI of FP = 4.0, average CPI of other
   instructions = 1.33, FPSQR frequency = 2%, CPI of FPSQR = 20. Two design
   alternatives: (a) reduce the CPI of FPSQR to 2, or (b) reduce the average CPI of
   all FP operations to 2.5. Compare using the processor performance equation. (5)
6. With an example, explain a cache optimisation technique to reduce the miss rate. (3)
7. What is the effect on power consumption of giving priority to read misses over
   writes? (2)""",
 explain=r'''
    A(h3("Q1 — architecture vs organization"))
    A(p("Architecture is the programmer-visible, high-level view (what the machine does): the ISA, data "
        "types, addressing modes, visible registers. Organization is the low-level implementation (how "
        "it is built): datapaths, control, clock, caches. The same architecture can have many "
        "organizations."))
    A(h3("Q2 — Amdahl’s law"))
    A(formula("T_new = T_old[(1 − f) + f/k] ;  S = 1/[(1 − f) + f/k] ;  S_max = 1/(1 − f)\n"
              "f = enhanced fraction, k = speed-up of that fraction."))
    A(h3("Q3 — pros and cons of the cache organisations"))
    A(table(["Organisation","Pros","Cons"],
      [["Direct-mapped","Fastest, cheapest, simplest lookup","Conflict misses (one home per block)"],
       ["Set-associative","Fewer conflicts; good compromise","More hardware; replacement decision"],
       ["Fully associative","Fewest conflicts (any line)","All tags compared → slow, expensive"]],
      widths=[1.3,2.4,2.6]))
    A(h3("Q4 — virtual memory and why we need it"))
    A(p("Virtual memory gives each process its own linear address space that is translated to physical "
        "addresses by page tables. We need it to (i) run programs larger than physical memory, "
        "(ii) isolate and protect processes, and (iii) simplify loading and sharing of code."))
    A(h3("Q5 — comparing the two FPSQR designs"))
    A(formula("Original CPI = (FP share × FP CPI) + (other share × other CPI)\n"
              "  = 0.25×4.0 + 0.75×1.33 = 1.00 + 0.9975 ≈ 2.00\n\n"
              "(a) Improve only FPSQR (2% of instructions) from CPI 20 to 2:\n"
              "  CPI_a = 2.00 − 0.02×(20 − 2) = 2.00 − 0.36 = 1.64  → S ≈ 2.00/1.64 = 1.22×\n\n"
              "(b) Improve ALL FP operations from CPI 4.0 to 2.5 (25% of instructions):\n"
              "  CPI_b = 2.00 − 0.25×(4.0 − 2.5) = 2.00 − 0.375 = 1.625 → S ≈ 1.23×"))
    A(callout("<b>Conclusion.</b> Improving <i>all</i> FP operations (b) is slightly better than "
        "improving only the rarely-used FPSQR (a), because it affects a larger fraction of the program — "
        "Amdahl’s Law in action.", 'tip'))
    A(h3("Q6 — reducing the miss rate (example)"))
    A(p("Use a larger block or higher associativity, or a better replacement policy. Example: switching "
        "from direct-mapped to 2-way set associative removes conflict misses. With a worked AMAT: "
        "AMAT = hit time + miss rate × miss penalty."))
    A(h3("Q7 — giving read misses priority over writes"))
    A(p("Giving read misses priority over write traffic reduces the stall the CPU sees, because reads are "
        "on the critical path while writes can be buffered. The trade-off is that write buffers must be "
        "large enough to hold the deferred writes; power-wise, deferring writes lets them be batched, "
        "slightly reducing memory activity, but the main effect is on performance, not power."))
''')

PYQS[4] = dict(
 title="ca4 — Amdahl (enhanced fraction), quad-core, benchmark CPI",
 transcript="""Q1. A program runs in 100 s; a portion that takes 40% of the time is enhanced to run
    5× faster. What is the overall speed-up?
Q2. A quad-core could speed up a computer by 4×, but rarely does. Use Amdahl’s law to
    explain why.
Q3. A benchmark has the mix: 39% loads, 12% stores, 28% ALU, 6% multiplies, 2% divides,
    10% branches (with stated CPIs). Find the CPI and comment on enhancements.""",
 explain=r'''
    A(h3("Q1 — 40% enhanced 5×"))
    A(formula("S = 1 / [(1 − 0.4) + 0.4/5] = 1 / (0.6 + 0.08) = 1/0.68 ≈ 1.47×\n"
              "Limit: S_max = 1/0.6 ≈ 1.67×"))
    A(h3("Q2 — why a quad-core rarely gives 4×"))
    A(p("A quad-core only speeds up the part of the program that is parallel. If a fraction p is "
        "parallelisable, the speed-up is S = 1/[(1−p) + p/4]. With even 25% serial (p = 0.75), "
        "S = 1/(0.25 + 0.1875) ≈ 2.3×, not 4×. Real programs have serial sections (I/O, "
        "synchronisation, startup), so the speed-up is always below the number of cores."))
    A(formula("S(n) = 1 / [(1 − p) + p/n] ,   n = number of cores.\n"
              "  n = 4, p = 0.75  →  S = 1/(0.25 + 0.1875) ≈ 2.29×\n"
              "  n = 4, p = 0.90  →  S = 1/(0.10 + 0.225) ≈ 3.08×"))
    A(h3("Q3 — instruction mix to CPI"))
    A(formula("CPI = Σ (fraction_i × CPI_i)\n"
              "  = 0.39·CPI_load + 0.12·CPI_store + 0.28·CPI_ALU + 0.06·CPI_mul\n"
              "    + 0.02·CPI_div + 0.10·CPI_branch   (substitute the printed CPIs)"))
    A(p("The question then asks which enhancement (e.g. a faster ALU, a faster multiplier) helps most — "
        "decide by multiplying each CPI reduction by its instruction fraction (Amdahl again)."))
''')

PYQS[5] = dict(
 title="ca5 — CPU time from an instruction mix at 500 MHz",
 transcript="""Q4. A MIPS ISA machine runs at 500 MHz with these instruction classes:
      ALU 3 cycles, branch/jump 2 cycles, store-word (sw) 4 cycles, load-word (lw) 5 cycles.
      A program executes: 40% ALU, 20% branch/jump, 15% sw, 25% lw.
      Find the average CPI and the CPU time for a program of 10⁶ instructions.""",
 explain=r'''
    A(h3("Average CPI"))
    A(formula("CPI = 0.40×3 + 0.20×2 + 0.15×4 + 0.25×5\n"
              "    = 1.20 + 0.40 + 0.60 + 1.25 = 3.45"))
    A(h3("CPU time"))
    A(formula("CPU time = IC × CPI / f = 10⁶ × 3.45 / 500×10⁶\n"
              "         = 3.45×10⁶ / 5×10⁸ = 6.9×10⁻³ s = 6.9 ms\n\n"
              "MIPS = f / (CPI × 10⁶) = 500 / 3.45 ≈ 145 MIPS"))
    A(callout("<b>Method reminder.</b> Multiply each CPI by its fraction for the average CPI; then "
        "IC × CPI / f gives the time. Keep the frequency in Hz (500 MHz = 5×10⁸ Hz).", 'tip'))
''')

PYQS[6] = dict(
 title="ca6 — Three-processor bus coherence (write-through + write-invalidate) trace",
 transcript="""5. A bus-based shared-memory system has three processors. Shared memory has blocks
   x, y, z. Each cache fits two blocks. Each block is Valid (V) or Invalid (I). Caches
   start empty; memory contents are x=?, y=?, z=?. (5)
   Event sequence (in order):
     1) P1: Read(x, y)      2) P2: Read(x, z)     3) P3: Read(y, z)
     4) P1: x = x + 10      5) P1: Read(z)        6) P2: Read(x)
     7) P3: x = 15          8) P1: z = z + 10     9) P2: x = 15
    10) P2: z = z + 30
   Show the cache/memory contents and states after each event using the write-through
   and write-invalidate protocol.""",
 explain=r'''
    A(h3("Protocol used"))
    A(p("<b>Write-through + write-invalidate</b>: on a write the writer updates memory immediately and "
        "invalidates the copies in every other cache. On a read miss the block is fetched and marked "
        "valid (shared). Because each cache holds only two blocks, a third block evicts one."))
    A(h3("Trace"))
    A(formula("1) P1 reads x,y : P1 = {x:V, y:V}\n"
              "2) P2 reads x,z : P2 = {x:V, z:V}\n"
              "3) P3 reads y,z : P3 = {y:V, z:V}\n"
              "4) P1 writes x=x+10 : P1.x → V (new value), memory.x updated;\n"
              "     P2.x invalidated → I  (write-invalidate)\n"
              "5) P1 reads z : P1 must fetch z; it already holds x,y so one is evicted\n"
              "     (say y) → P1 = {x:V, z:V}\n"
              "6) P2 reads x : P2’s copy was I → fetch x → P2 = {x:V, z:V}\n"
              "7) P3 writes x=15 : memory.x updated; P1.x and P2.x invalidated → I\n"
              "8) P1 writes z=z+10 : memory.z updated; P2.z and P3.z invalidated → I\n"
              "9) P2 writes x=15 : fetch x, memory.x updated; other copies invalidated\n"
              "10) P2 writes z=z+30 : fetch z, memory.z updated; other copies invalidated"))
    A(p("Draw the answer as a table: one row per event, one column per cache (with block + V/I state) "
        "and one column for memory. The key rule is that a write makes the writer valid and every other "
        "copy invalid, and because writes are write-through the memory value is always current."))
''')

PYQS[7] = dict(
 title="ca7 — Amdahl with communication overhead; cache optimisation; snoopy vs directory",
 transcript="""Q1. (a) Find the speed-up with 8 processors if, for every 100 units of work, 10 units
    are spent on communication overhead.
    (b) Cache optimisation + an ISA question.
    (c) CPU time.
Q. Compare snoopy and directory-based coherence.""",
 explain=r'''
    A(h3("Q1a — Amdahl with communication overhead"))
    A(p("If 10 of every 100 units are unavoidable overhead (serial), the parallelisable fraction is "
        "p = 0.90. With n = 8 processors:"))
    A(formula("S = 1 / [(1 − p) + p/n] = 1 / [0.10 + 0.90/8] = 1 / (0.10 + 0.1125)\n"
              "  = 1/0.2125 ≈ 4.7×\n"
              "Limit: S_max = 1/0.10 = 10×  (the 10% overhead caps it)"))
    A(h3("Snoopy vs directory coherence"))
    A(table(["","Snooping","Directory"],
      [["Mechanism","All caches watch a shared bus","A directory records the sharers of each block"],
       ["Traffic","Broadcast to all caches","Point-to-point to the sharers only"],
       ["Scalability","Limited (bus contention)","Scales to large systems"],
       ["Cost","Simple hardware","Directory storage + extra messages"]],
      widths=[1.1,2.3,2.6]))
    A(p("The cache-optimisation and CPU-time parts are the standard AMAT / IC×CPI/f calculations; see "
        "the cache and performance sections of this guide for the full method."))
''')

PYQS[8] = dict(
 title="ca8 — Branch-target buffer penalty; write-miss stall time",
 transcript="""Q. (a) A branch-target buffer is used. Given the hit rate, the penalty of a correct
    prediction and a misprediction, compute the branch penalty per branch.
    (b) Compute the write-miss stall time with ownership and invalidates.""",
 explain=r'''
    A(h3("Qa — branch-target-buffer penalty"))
    A(formula("Branch penalty = (BTB hit rate × correct-prediction penalty)\n"
              "              + (BTB miss/misprediction × misprediction penalty)\n\n"
              "Example: hit rate 90%, correct penalty = 1 cycle, mispredict penalty = 3 cycles:\n"
              "  penalty per branch = 0.90×1 + 0.10×3 = 0.90 + 0.30 = 1.2 cycles"))
    A(h3("Qb — write-miss stall time"))
    A(p("A write miss under write-allocate with a write-back cache can require fetching the block "
        "(write-allocate) and, if the evicted line is dirty, writing it back. The stall time is the "
        "sum of these memory operations:"))
    A(formula("Write-miss stall = (fetch block time) + (write-back time if the evicted line is dirty)\n"
              "Example: fetch = 20 cycles, write-back = 20 cycles, dirty probability 0.3:\n"
              "  stall = 20 + 0.3×20 = 26 cycles"))
    A(p("The exact numbers come from the printed question; the method is to add the memory operations "
        "the miss forces and weight the write-back by the probability the evicted line is dirty."))
''')

PYQS[9] = dict(
 title="ca9 — 5-stage pipeline flow, branch in pipeline, hazards and nops",
 transcript="""Date: 31.10.2022    Answer ALL Questions    Max Marks: 20
1. These instructions execute in a five-stage pipeline:
      lw  R1, 0(R2)
      add R3, R4, R5
      sub R6, R1, R3
   Explain the flow of execution in a pipeline using 2 simple diagrams. (4)
2. a. Show how the instructions below proceed through the pipeline. Assume (i) the branch
      is not taken and (ii) when executed the values of R1 and R2 are the same. (4)
      beq R1, R2, X
      lw  R5, 0(R5)
      sub R6, R3, R3
   X: add R4, R4, R2
      sw  R4, 0(R4)
   Does the last add instruction depend on the branch?
3. Indicate the type of hazards and data dependences for: (5)
      a. lw R1, 40(R0)     b. lw R5, -16(R5)
   Add nop instructions to eliminate the hazards (no branch-hazard hardware). (3)""",
 explain=r'''
    A(h3("Q1 — pipeline flow"))
    A(formula("Cycles:        1    2    3    4    5    6    7\n"
              "lw  R1,0(R2)   IF   ID   EX   MEM  WB\n"
              "add R3,R4,R5        IF   ID   EX   MEM  WB\n"
              "sub R6,R1,R3             IF   ID   EX   MEM  WB\n"
              "The sub uses R1 (produced by the lw) → one load-use stall even with forwarding."))
    A(p("Diagram 1: the five stages in a row (IF, ID, EX, MEM, WB). Diagram 2: the space–time chart "
        "above. The pipeline fills for the first five cycles, then completes one instruction per cycle."))
    A(h3("Q2a — branch in the pipeline"))
    A(p("The branch is not taken, and R1 = R2 at execution, so the branch <i>is</i> taken to X. In a "
        "simple pipeline the branch is resolved in the ID (or EX) stage; until then the processor has "
        "fetched the fall-through instructions and must flush them if the branch is taken."))
    A(formula("beq R1,R2,X : IF ID EX MEM WB   (resolved; if taken, flush the next fetch)\n"
              "lw  R5,0(R5) :    IF  ID  EX  MEM  WB   (or squashed)\n"
              "sub R6,R3,R3 :       IF  ID  EX  MEM  WB\n"
              "X: add …     :            IF  ID  EX  MEM  WB\n"
              "The final add does NOT depend on the branch’s data (it uses R4,R2),\n"
              "but it is control-dependent on the branch (it is only executed if taken)."))
    A(h3("Q3 — hazards and nops"))
    A(formula("lw R1, 40(R0)   → load-use hazard if R1 is used immediately after\n"
              "lw R5, -16(R5)  → load-use hazard (R5 is the base AND the destination)\n\n"
              "Insert nops to cover the load latency (say 2 cycles with no forwarding):\n"
              "  lw R1, 40(R0)\n"
              "  nop\n"
              "  nop\n"
              "  <use R1>\n"
              "  lw R5, -16(R5)\n"
              "  nop\n"
              "  nop\n"
              "  <use R5>"))
    A(p("Without forwarding, a load needs two nops before its value is safe to use; the branch needs "
        "flushing (or nops) because there is no branch-hazard hardware."))
''')

PYQS[10] = dict(
 title="ca10 — RAW/WAW dependences; optimal pipeline schedule with forwarding and CPI",
 transcript="""Q2. (a) Data dependences: identify RAW/WAW in the given sequence and rename.
    (b) Find the optimal pipeline schedule with forwarding and compute the CPI.
    (c) Convert a C loop to MIPS, find hazards and reorder.""",
 explain=r'''
    A(h3("Q2a — dependences and renaming"))
    A(formula("Example sequence:\n"
              "  I1: add R1, R2, R3\n"
              "  I2: sub R4, R1, R5     ; RAW on R1 (must follow I1)\n"
              "  I3: add R1, R6, R7     ; WAW on R1 with I1, WAR with I2\n"
              "Rename I3’s destination:\n"
              "  I3: add R8, R6, R7     ; now independent of I1 and I2"))
    A(h3("Q2b — optimal schedule with forwarding and CPI"))
    A(formula("With forwarding, a load-use pair needs 1 stall; ALU→ALU needs 0 stalls.\n"
              "Schedule the independent instructions into the stall slots.\n"
              "CPI = (total cycles) / (number of instructions)\n"
              "  e.g. 6 instructions in 8 cycles → CPI ≈ 1.33"))
    A(h3("Q2c — C to MIPS, hazards, reorder"))
    A(p("Translate the C loop to MIPS, then walk the pipeline to find RAW hazards, then reorder the "
        "instructions (and insert nops where reordering cannot help) to minimise stalls. The method is "
        "identical to Q2b: build the space–time chart and slide independent instructions into the gaps."))
''')

PYQS[11] = dict(
 title="ca11 — DAXPY loop unrolled 3× with fresh registers",
 transcript="""Q. Unroll the DAXPY loop three times, using fresh registers and removing redundant
   computation. Then schedule it.

   DAXPY:  Y[i] = a·X[i] + Y[i]""",
 explain=r'''
    A(h3("Unrolled and scheduled DAXPY"))
    A(formula("Loop:  L.D  F0, 0(R1)      ; load X[i]\n"
              "       MUL.D F4, F0, F2     ; a·X[i]\n"
              "       L.D  F6, 0(R2)       ; load Y[i]\n"
              "       ADD.D F6, F4, F6     ; a·X[i] + Y[i]\n"
              "       S.D  F6, 0(R2)       ; store Y[i]\n"
              "       DADDUI R1,R1,#8 ; DADDUI R2,R2,#8 ; BNE R1,R3,Loop"))
    A(p("Unroll three times, giving each iteration fresh registers (F0/F4/F8/F12 …) so the operations "
        "are independent, then remove the redundant pointer arithmetic (one update per unrolled group)."))
    A(formula("Unrolled (sketch):\n"
              "  L.D   F0, 0(R1)     ; X[i]\n"
              "  L.D   F6, -8(R1)    ; X[i+1]\n"
              "  L.D   F10, -16(R1)  ; X[i+2]\n"
              "  MUL.D F4, F0, F2\n"
              "  MUL.D F8, F6, F2\n"
              "  MUL.D F12, F10, F2\n"
              "  ADD.D F4, F4, Y0 ; ADD.D F8, F8, Y1 ; ADD.D F12, F12, Y2\n"
              "  S.D   F4, 0(R2) ; S.D F8, -8(R2) ; S.D F12, -16(R2)\n"
              "  DADDUI R1,R1,#-24 ; DADDUI R2,R2,#-24 ; BNE R1,R3,Loop"))
    A(callout("<b>Two requirements.</b> (1) Fresh registers so there is no false dependence; (2) the "
        "loop-control work (pointer updates, branch) is done once per group, not per element.", 'tip'))
''')

PYQS[12] = dict(
 title="ca12 — Tomasulo at cycle 6; vector vs SIMD vs GPU",
 transcript="""4. Simulate the code using Tomasulo’s algorithm. Compute the values at clock cycle 6.
   Use the format:  (6)
     Instruction status:  Instruction | j | k | Issue | Execute complete | Write Result
     Reservation stations: Name | Busy | Op | Vj | Vk | Qj | Qk
     Register result status (Clock 6)
   Code:
     LD  F6, 34(R2)     LD  F2, 45(R3)     MUL F0, F2, F4
     SUB F8, F6, F2     DIV F10, F0, F6    ADD F6, F8, F2
5. Differentiate Vector, SIMD and GPU architectures with a neat diagram. (2)""",
 explain=r'''
    A(h3("Tomasulo at cycle 6"))
    A(p("The code is the canonical Tomasulo example. Fill the three tables as the instructions issue, "
        "execute when their operands are ready, and write their results on the CDB."))
    A(formula("Cycle 1: LD F6 issues (Load1).   Cycle 2: LD F2 issues (Load2).\n"
              "Cycle 3: MUL F0 issues (Mult1), Qj=Load2 (needs F2), Vk=F4.\n"
              "Cycle 4: SUB F8 issues (Add1), Qj=Load1 (F6), Qk=Load2 (F2).\n"
              "Cycle 5: DIV F10 issues (Mult2), Qj=Mult1 (F0), Qk=Load1 (F6).\n"
              "Cycle 6: ADD F6 issues (Add2), Qj=Add1 (F8), Qk=Load2 (F2).\n\n"
              "By cycle 6 the loads have completed and broadcast their values, so the\n"
              "Q fields that referenced Load1/Load2 are cleared (V fields filled)."))
    A(p("<b>Register result status at clock 6:</b> F0 → Mult1, F6 → Add2, F8 → Add1, F10 → Mult2 "
        "(whichever stations are still pending)."))
    A(h3("Vector vs SIMD vs GPU"))
    A(table(["","Vector","SIMD","GPU"],
      [["Model","Pipelined vector unit","One instruction, many data","Many SIMD lanes + threads"],
       ["Control","Single control unit, vector length","Single control unit","Many warps, hardware threads"],
       ["Best for","Long regular arrays","Short vector ops","Massively parallel data"],
       ["Memory","Vector registers","Wide registers","High-bandwidth, latency-hidden"]],
      widths=[0.9,1.6,1.6,2.0]))
''')

PYQS[13] = dict(
 title="ca13 — RISC fragments: dependences, forwarding/stalls, 5-stage latencies, MIPS schedule",
 transcript="""Q. Four RISC fragments: find the dependences and state whether forwarding/stalls are
   needed. For the 5-stage pipeline (given latencies) compute cycle time, latency and
   throughput. Convert a MIPS fragment, list dependences and schedule it.""",
 explain=r'''
    A(h3("Dependences and stalls"))
    A(formula("For each fragment, scan for RAW hazards:\n"
              "  • ALU → ALU : 0 stalls with forwarding\n"
              "  • ALU → use : forward from EX/MEM\n"
              "  • load → use : 1 stall (data ready after MEM)\n"
              "  • store data dependent on a load : 1 stall"))
    A(h3("Cycle time, latency, throughput"))
    A(formula("Clock cycle time = max(stage delay) + register overhead\n"
              "  e.g. stages 2,2,2,2,2 ns + 0.5 ns latch → 2.5 ns\n"
              "Latency (one instruction) = 5 stages × cycle time\n"
              "Throughput = 1 instruction per cycle (steady state)"))
    A(h3("MIPS fragment: dependences and schedule"))
    A(p("Identify the RAW dependences, then reorder so that independent instructions fill the delay "
        "slots; insert nops only where reordering cannot remove a stall."))
    A(formula("Example:\n"
              "  lw  R1, 0(R2)\n"
              "  add R3, R1, R4     ; RAW, 1 stall (load-use)\n"
              "  add R5, R6, R7     ; independent — move here to fill the stall\n"
              "  sub R8, R3, R9"))
''')

PYQS[14] = dict(
 title="ca14 — Reorder to remove stalls; count RAW hazards and rename",
 transcript="""Q. Reorder the given instructions to remove stalls; count the RAW hazards and apply
   register renaming where needed.""",
 explain=r'''
    A(h3("Method"))
    A(p("Draw the pipeline; every time an instruction reads a register written by a preceding "
        "instruction within the latency window, that is a RAW hazard. Move independent instructions up "
        "to cover the gap; if two instructions clash only on a name (WAR/WAW), rename to break the "
        "clash."))
    A(formula("Reorder example:\n"
              "  before:  I1 lw R1,…  I2 add R3,R1,R4  I3 lw R5,…  I4 add R6,R5,R7\n"
              "  after :  I1 lw R1,…  I3 lw R5,…  I2 add R3,R1,R4  I4 add R6,R5,R7\n"
              "The two loads issue back-to-back; their uses are pushed apart by one\n"
              "slot each, removing the load-use stalls."))
    A(p("Count the hazards that remain after the best reordering; those are the true (unavoidable) RAW "
        "stalls. Renaming removes any WAR/WAW hazards that would otherwise force order."))
''')

PYQS[15] = dict(
 title="ca15 — AMAT with an added L2; multicore CPI needed to beat a single core",
 transcript="""Q. (a) Given an L1 with a hit time and miss rate, and an added L2, find the required L2
    hit rate so the AMAT meets a target.
    (b) Find the multicore CPI needed for a multicore to beat a single core.""",
 explain=r'''
    A(h3("Qa — AMAT with two levels"))
    A(formula("AMAT = t_L1 + m_L1 × ( t_L2 + m_L2 × t_mem )\n"
              "Solve for m_L2 (the required L2 local miss rate, hence the required\n"
              "L2 hit rate = 1 − m_L2):\n"
              "  m_L2 = [ (AMAT_target − t_L1)/m_L1 − t_L2 ] / t_mem"))
    A(p("Substitute the printed hit time, miss rate and memory penalty and solve for the L2 hit rate. "
        "The required hit rate must be ≤ 1, otherwise the target is unachievable with one L2."))
    A(h3("Qb — multicore vs single core"))
    A(formula("Multicore is better when:  IC_multi × CPI_multi / f_multi  <  IC_single × CPI_single / f_single\n"
              "If IC and f are equal, solve for the CPI the multicore must achieve.\n"
              "  CPI_multi < CPI_single × (f_multi / f_single) × (IC_single / IC_multi)"))
''')

PYQS[16] = dict(
 title="ca16 — For each sequence: must stall / forwarding / no stall",
 transcript="""Q. For each instruction sequence, state whether it must stall, can use forwarding, or
   needs no stall at all.""",
 explain=r'''
    A(h3("Rules to apply"))
    A(table(["Case","Result"],
      [["ALU → ALU (RAW)","Forwarding → 0 stalls"],
       ["load → use (RAW)","Forwarding insufficient → 1 stall"],
       ["store after a load (data)","1 stall if the stored data comes from the load"],
       ["Independent instructions","0 stalls"]],
      widths=[2.0,2.0]))
    A(formula("With full forwarding:\n"
              "  • register-to-register ALU chains: no stall\n"
              "  • load-use pairs: exactly 1 bubble\n"
              "Without forwarding: 2–3 bubbles per RAW pair."))
    A(p("Classify each printed sequence into one of these cases. The examiner is testing whether you "
        "know that forwarding removes ALU→ALU stalls but cannot remove the load-use stall."))
''')

PYQS[17] = dict(
 title="ca17 — Pipeline instruction mix: branch-adder use, data-memory use, pipelining speed-up",
 transcript="""Q. A pipeline is given with an instruction mix. Find (a) the percentage of time the
   branch adder is used, (b) the percentage of time the data memory is used, and
   (c) the pipelining speed-up.""",
 explain=r'''
    A(h3("Resource utilisation"))
    A(formula("Fraction of cycles a resource is used =\n"
              "  (instructions that use it × cycles they occupy) / (total cycles)\n\n"
              "Branch adder: used only by branch instructions in the EX stage.\n"
              "  e.g. 20% branches × 1 cycle → 20% utilisation\n"
              "Data memory: used by loads and stores in the MEM stage.\n"
              "  e.g. (25% loads + 15% stores) × 1 cycle → 40% utilisation"))
    A(h3("Pipelining speed-up"))
    A(formula("S = (n · k) / (n + k − 1)  →  k  as n → ∞\n"
              "  n = number of instructions, k = number of stages."))
    A(p("The exact percentages come from the printed mix; the method is to count the fraction of "
        "instructions that exercise each resource and multiply by the number of cycles they hold it."))
''')

PYQS[18] = dict(
 title="ca18 — Tomasulo on a loop with multiply latency and possible cache misses",
 transcript="""Q. Apply Tomasulo’s algorithm to the given loop; the multiply latency is stated and
   cache misses may occur. Fill the tables.""",
 explain=r'''
    A(h3("Method"))
    A(p("Issue each loop-body instruction into its reservation station, filling Qj/Qk with the tags of "
        "the producers. When both operands are ready the instruction executes after the stated latency; "
        "a cache miss simply delays the load’s completion (and hence everything waiting on it)."))
    A(formula("Load: latency = (hit time) or (miss penalty) if it misses.\n"
              "Multiply: latency = given (e.g. 10 cycles).\n"
              "Execute_start = max(operands ready, unit free);  Write = start + latency."))
    A(p("Record Issue, Execute-complete and Write-result for every instruction; the register-result "
        "status shows which station will produce each register at each cycle."))
''')

PYQS[19] = dict(
 title="ca19 — Performance (MIPS, CPU time) + pipelining speed-up (repeat of ca1 Q1)",
 transcript="""Q. (Repeat of ca1 Q1.) Compute MIPS and CPU time for the two machines, and the
   pipelining speed-up as a function of N.""",
 explain=r'''
    A(p("This scan repeats ca1 Q1. The solution is identical:"))
    A(formula("CPI = Σ (share × CPI);  MIPS = f / (CPI × 10⁶)\n"
              "CPU time = IC × CPI / f\n"
              "Pipelining speed-up S(N) = N·A / (N + A − 1)"))
    A(callout("<b>Note.</b> Because ca19 duplicates ca1, its solution is not repeated in full here — "
        "see the ca1 solution above. This is recorded explicitly so that no question is left unrevised.", 'tip'))
''')

PYQS[20] = dict(
 title="ca20 — Resource/control hazards on a MIPS fragment with two memories",
 transcript="""Q. Identify the resource and control hazards in the given MIPS fragment (the machine has
   separate instruction and data memories).""",
 explain=r'''
    A(h3("Hazards to look for"))
    A(bullets([
        "<b>Structural (resource)</b> — if the machine had a <i>single</i> memory, a load/store in the "
        "MEM stage would clash with an instruction fetch in the IF stage. With <i>two separate memories</i> "
        "(I-cache and D-cache) this hazard disappears.",
        "<b>Control</b> — a branch resolved late forces the processor to flush the instructions fetched "
        "behind it.",
    ]))
    A(formula("Two memories ⇒ no IF/MEM structural hazard.\n"
              "Branch ⇒ control hazard: instructions after the branch may be flushed."))
    A(p("The point of the question is that splitting the memory into instruction and data memories "
        "removes the structural hazard; only the control hazard from the branch remains."))
''')

PYQS[21] = dict(
 title="ca21 — Single-memory structural hazard; pipeline mix; Tomasulo for hazards",
 transcript="""Q. (a) With a single memory, identify the structural hazard in the pipeline.
   (b) Given the pipeline instruction mix, find resource use.
   (c) Use Tomasulo to handle the hazards in the given code.""",
 explain=r'''
    A(h3("Qa — structural hazard with one memory"))
    A(formula("IF (instruction fetch) and MEM (load/store) both want the single memory\n"
              "in the same cycle → structural hazard.\n"
              "Fix: separate instruction and data memories (Harvard-style), or stall."))
    A(h3("Qb — pipeline mix"))
    A(formula("Utilisation of a resource = fraction of instructions using it\n"
              "  (weighted by the cycles they hold it)."))
    A(h3("Qc — Tomasulo"))
    A(p("Apply the three Tomasulo steps to the code: issue (fill Qj/Qk), execute when operands are "
        "ready, write the result on the CDB. Tomasulo removes the WAR/WAW hazards by renaming; RAW "
        "hazards are handled by the reservation stations waiting on the CDB."))
''')

PYQS[22] = dict(
 title="ca22 — Loop dependences (true/output/anti) and renaming (repeat of ca1 Q2a)",
 transcript="""Q. (Repeat of ca1 Q2a.) Find the true, output and anti-dependences in the loop and
   eliminate the false ones by renaming.""",
 explain=r'''
    A(p("This scan repeats ca1 Q2a; the answer is the same classification and renaming shown there:"))
    A(table(["Statements","Dependence","Type"],
      [["S1 → S2 (A[i])","RAW","true"],
       ["S1 → S3 (A[i])","WAW","output"],
       ["S2 → S3 (A[i])","WAR","anti"],
       ["S3 → S4 (A[i])","RAW","true"]],
      widths=[1.6,1.4,1.2]))
    A(formula("Rename to remove WAW/WAR:\n"
              "  A1 = A[i]*B[i];  B[i] = A1 + c;  A2 = C[i]*c;  C[i] = D[i]*A2;"))
''')

PYQS[23] = dict(
 title="ca23 — Basic structure of a vector architecture; MSI coherence snapshot",
 transcript="""Q. (a) Draw the basic structure of a vector architecture.
   (b) Given an MSI coherence snapshot, apply the events.""",
 explain=r'''
    A(h3("Qa — vector architecture structure"))
    A(p("Draw: a scalar register file and a <b>vector register file</b>; a <b>vector functional unit</b> "
        "with pipelined lanes (add, multiply); the <b>vector length register</b> and <b>stride "
        "register</b>; and the memory system feeding the lanes. One vector instruction drives all the "
        "lanes, so many elements are processed together."))
    A(h3("Qb — MSI snapshot"))
    A(formula("Apply the write-invalidate rules:\n"
              "  read miss → S ;  write hit/miss → M (invalidate all other copies) ;\n"
              "  snoop a write to your S/M copy → I."))
''')

PYQS[24] = dict(
 title="ca24 — DAXPY: unroll until no stalls, schedule, time per element",
 transcript="""Q. Unroll the DAXPY loop until there are no stalls, schedule it, and compute the time
   per element.""",
 explain=r'''
    A(h3("Unroll until no stalls"))
    A(formula("Load latency = L cycles ⇒ unroll so that ≥ L independent instructions\n"
              "separate each load from its use. For L = 4, unroll ~4× and interleave:\n"
              "  L.D F0 ; L.D F4 ; L.D F8 ; L.D F12 ; MUL ; MUL ; MUL ; MUL ;\n"
              "  ADD ; ADD ; ADD ; ADD ; S.D ; S.D ; S.D ; S.D"))
    A(h3("Time per element"))
    A(formula("Time per element = (cycles per unrolled group) / (elements per group)\n"
              "  e.g. 20 cycles for 4 elements → 5 cycles/element."))
    A(callout("<b>Goal.</b> After unrolling enough, every stall slot is filled by an independent "
        "instruction, so the loop runs at one element per few cycles with no bubbles.", 'tip'))
''')

PYQS[25] = dict(
 title="ca25 — ROB contents after 2 iterations; critical-word-first; cache tag bits; blocking",
 transcript="""Q. (a) Show the contents of the reorder buffer after 2 loop iterations.
   (b) Explain critical-word-first and early restart.
   (c) Find the number of cache tag bits.
   (d) Explain blocking vs non-blocking caches and prefetching.""",
 explain=r'''
    A(h3("Qa — ROB after two iterations"))
    A(p("The ROB holds the speculative instructions in program order. After two loop iterations it "
        "contains the entries for both bodies, with the committed ones at the head and the still-"
        "speculative ones behind. List each entry’s destination register, value (if ready) and "
        "ready/exception flags."))
    A(h3("Qb — critical-word-first and early restart"))
    A(formula("Critical-word-first: fetch the REQUESTED word before the rest of the block,\n"
              "  so the CPU restarts as soon as that word arrives.\n"
              "Early restart: resume the CPU as soon as the needed word is back,\n"
              "  without waiting for the whole block."))
    A(h3("Qc — tag bits"))
    A(formula("tag bits = address bits − index bits − offset bits\n"
              "  offset = log₂(block size);  index = log₂(number of lines/sets)"))
    A(h3("Qd — blocking vs non-blocking; prefetching"))
    A(bullets([
        "<b>Blocking (lockup-free)</b> — the cache serves one miss at a time; other accesses wait.",
        "<b>Non-blocking</b> — several misses can be outstanding at once, so other accesses continue.",
        "<b>Prefetching</b> — bring blocks in before they are requested, hiding latency.",
    ]))
''')

PYQS[26] = dict(
 title="ca26 — Amdahl (scalar + matrix); energy saved by V/f scaling; AMAT with L2",
 transcript="""Q. (a) Amdahl: a scalar portion and a matrix portion.
   (b) Energy saved by scaling voltage and frequency.
   (c) AMAT with an L2.""",
 explain=r'''
    A(h3("Qa — Amdahl with two portions"))
    A(formula("S = 1 / [ (1 − f) + f/k ]  ;  apply separately to the scalar and\n"
              "matrix portions, then combine using their time shares."))
    A(h3("Qb — energy saved by V/f scaling"))
    A(formula("P_dyn = C·V²·f ;  E = P·t = C·V²·f·t\n"
              "If f scales by s and V by s (together):  P ∝ s³, and t ∝ 1/s,\n"
              "  so E ∝ s²  →  energy falls with the square of the scale factor.\n"
              "Example: s = 0.8 → E_new/E_old = 0.8² = 0.64 (36% energy saved)."))
    A(h3("Qc — AMAT with L2"))
    A(formula("AMAT = t_L1 + m_L1 × ( t_L2 + m_L2 × t_mem )"))
''')

PYQS[27] = dict(
 title="ca27 — Write-back vs write-through break-even; RAW/WAR/WAW; pipeline phases",
 transcript="""Q. (a) Find the break-even point between write-back and write-through.
   (b) Identify RAW/WAR/WAW in the given sequence.
   (c) Describe the pipeline phases and the branch overhead.""",
 explain=r'''
    A(h3("Qa — write-back vs write-through break-even"))
    A(formula("Write-through traffic  = 1 memory write per store.\n"
              "Write-back traffic     = (1 write per block) / (writes per block before eviction)\n"
              "Break-even:  write-back wins when a block is written more than once\n"
              "  before it is evicted. With w writes per block:\n"
              "  write-through traffic = w ;  write-back traffic = 1  →  write-back better for w > 1."))
    A(h3("Qb — dependences"))
    A(table(["Dependence","Meaning","Renaming removes it?"],
      [["RAW","read after write (true)","No"],
       ["WAR","write after read (anti)","Yes"],
       ["WAW","write after write (output)","Yes"]],
      widths=[1.0,2.4,1.8]))
    A(h3("Qc — pipeline phases and branch overhead"))
    A(formula("Phases: IF, ID, EX, MEM, WB.\n"
              "Branch overhead = cycles lost flushing instructions fetched behind\n"
              "  the branch before it is resolved (e.g. 1–2 cycles)."))
''')

PYQS[28] = dict(
 title="ca28 — Static vs dynamic scheduling; three control-hazard techniques; Tomasulo + speculation",
 transcript="""Q. (a) Compare static and dynamic scheduling.
   (b) Describe three techniques to handle control hazards.
   (c) Show the hardware needed for Tomasulo with speculation.""",
 explain=r'''
    A(h3("Qa — static vs dynamic"))
    A(table(["","Static (compiler)","Dynamic (hardware)"],
      [["When","At compile time","At run time"],
       ["Sees","The program text","Actual conditions (cache misses)"],
       ["Cost","Compiler effort","Hardware complexity"],
       ["Example","Loop unrolling, scheduling","Scoreboard, Tomasulo, speculation"]],
      widths=[0.9,2.3,2.3]))
    A(h3("Qb — three control-hazard techniques"))
    A(bullets([
        "<b>1) Branch prediction</b> — guess the direction and fetch accordingly.",
        "<b>2) Delayed branch</b> — the compiler fills the branch-delay slot with a useful instruction.",
        "<b>3) Flush/stall</b> — if the prediction is wrong, squash the wrong-path instructions.",
    ]))
    A(h3("Qc — Tomasulo + speculation hardware"))
    A(p("Add a <b>reorder buffer</b> to Tomasulo so results are held until in-order commit, giving "
        "precise exceptions. The reservation stations, CDB, register-status table and ROB together let "
        "the machine execute speculatively and commit in order."))
''')

PYQS[29] = dict(
 title="ca29 — GPU peak throughput and memory-bound; Intel i7 coherence; MESI",
 transcript="""Q. (a) Compute GPU peak throughput and decide whether the workload is memory-bound.
   (b) Explain the coherence protocol used in an Intel i7.
   (c) Explain the fourth state (MESI).""",
 explain=r'''
    A(h3("Qa — GPU throughput and the memory bound"))
    A(formula("Peak FLOPS = cores × clock × ops-per-core-per-cycle\n"
              "  (count a multiply-add as 2 FLOPs)\n"
              "Memory bytes/cycle needed = FLOPS / arithmetic-intensity\n"
              "If the required bandwidth exceeds the available bandwidth, the kernel\n"
              "  is MEMORY-BOUND; otherwise it is COMPUTE-BOUND."))
    A(h3("Qb — Intel i7 coherence"))
    A(p("Intel multicore chips use a <b>snooping MESI</b> protocol over an on-chip interconnect: each "
        "core’s private L1/L2 caches snoop, the shared L3 acts as the point of coherence, and blocks are "
        "kept in Modified, Exclusive, Shared or Invalid states."))
    A(h3("Qc — the MESI fourth state"))
    A(formula("E (Exclusive): the block is clean and held by ONLY this cache.\n"
              "  A write can upgrade E → M silently (no bus traffic), because no\n"
              "  other cache has a copy.\n"
              "This removes a coherence transaction for every private write — the\n"
              "  main advantage of MESI over MSI."))
''')

PYQS[30] = dict(
 title="ca30 — Server-farm MTTF; 22-core Amdahl; pipeline throughput after splitting a stage",
 transcript="""Q. (a) A server farm of many machines: compute the MTTF of the farm.
   (b) Amdahl with 22 cores.
   (c) Pipeline throughput after splitting a stage.""",
 explain=r'''
    A(h3("Qa — MTTF of a server farm"))
    A(formula("Machines in series (all must work):  1/MTTF_farm = Σ 1/MTTF_i\n"
              "  For n identical machines:  MTTF_farm = MTTF / n\n"
              "  e.g. 1000 machines each MTTF = 10⁶ h → MTTF_farm = 1000 h\n"
              "  → a failure somewhere in the farm roughly every 1000 hours."))
    A(h3("Qb — Amdahl with 22 cores"))
    A(formula("S = 1 / [ (1 − p) + p/22 ]  ;  limit = 1/(1 − p)"))
    A(h3("Qc — splitting a stage"))
    A(formula("If the slowest stage is split into two equal halves, the clock period\n"
              "  can shrink toward the next-slowest stage, raising throughput.\n"
              "  New throughput = 1 / (new clock period) (if the pipeline stays full)."))
''')

PYQS[31] = dict(
 title="ca31 — Types of hazards and impact; 5-stage (IF/ID/OF/EX/WO) cycle count with forwarding",
 transcript="""Q. (a) List the types of hazards and their impact.
   (b) For the 5-stage pipeline (IF/ID/OF/EX/WO), count the cycles with forwarding.""",
 explain=r'''
    A(h3("Qa — hazard types and impact"))
    A(table(["Hazard","Cause","Impact"],
      [["Structural","Resource conflict","Stall cycles"],
       ["Data (RAW)","Value not ready","Stall (load-use: 1 cycle)"],
       ["Control","Branch resolves late","Flush/pipeline bubbles"]],
      widths=[1.1,1.9,2.2]))
    A(h3("Qb — cycle count with forwarding"))
    A(formula("Count = number of instructions + number of stalls.\n"
              "  Each load-use pair adds 1 stall; ALU→ALU pairs add 0 with forwarding.\n"
              "  e.g. 5 instructions with 1 load-use stall → 6 cycles + pipeline fill."))
''')

PYQS[32] = dict(
 title="ca32 — Four branch predictors and misprediction; clock cycle time 5 vs 10 stages; speculation; cache optimisation; branch overhead",
 transcript="""Q. (a) Describe four branch predictors and their misprediction behaviour.
   (b) Compare clock cycle time for 5-stage vs 10-stage pipelines.
   (c) Show the hardware for speculation.
   (d) Cache optimisation for access time.
   (e) Pipeline phases and branch overhead.""",
 explain=r'''
    A(h3("Qa — four branch predictors"))
    A(table(["Predictor","How it works","Mispredicts when"],
      [["Static","Always taken / never taken","Pattern changes"],
       ["1-bit","Last outcome","Direction changes"],
       ["2-bit","Saturating counter","Two changes in a row"],
       ["Correlating","History of recent branches","Unseen pattern"]],
      widths=[1.1,2.3,2.2]))
    A(h3("Qb — 5-stage vs 10-stage"))
    A(formula("Deeper pipeline → shorter clock period (more overlap) but larger\n"
              "  misprediction penalty and more hazard-checking logic.\n"
              "  cycle time ≈ max stage delay + latch overhead."))
    A(h3("Qc — speculation hardware"))
    A(p("Reservation stations + CDB + register-status table + <b>reorder buffer</b> for in-order commit."))
    A(h3("Qd — cache optimisation for access time"))
    A(formula("AMAT = hit time + miss rate × miss penalty\n"
              "  reduce hit time: smaller/faster cache, simpler addressing."))
    A(h3("Qe — pipeline phases and branch overhead"))
    A(formula("Phases IF, ID, EX, MEM, WB; branch overhead = flush cycles behind the branch."))
''')

PYQS[33] = dict(
 title="ca33 — Three modification versions (component speed-ups) ranking; Amdahl matrix; energy",
 transcript="""Q. Three modification versions affect components X, Y, Z whose execution-time
   fractions are given. Rank them; then apply Amdahl to a matrix computation and
   compute the energy.""",
 explain=r'''
    A(h3("Ranking the three versions"))
    A(formula("For each version:  S = 1 / [ (1 − f) + f/k ]\n"
              "  where f = the fraction of time the modified component occupies,\n"
              "        k = the speed-up of that component.\n"
              "Rank by the resulting S (the larger S is the better version)."))
    A(h3("Amdahl on the matrix computation"))
    A(formula("S = 1 / [ (1 − p) + p/n ]  with p = parallelisable fraction, n = processors."))
    A(h3("Energy"))
    A(formula("E = P × t = C·V²·f × t ;  scaling V and f together by s gives E ∝ s²."))
''')

PYQS[34] = dict(
 title="ca34 — Out-of-order advantages; pipeline phases with a static predictor; Tomasulo + cycle for F10",
 transcript="""Q. (a) What are the advantages of out-of-order execution?
   (b) Show the pipeline phases with a static predictor.
   (c) Discuss Tomasulo and give the cycle in which F10 is produced.""",
 explain=r'''
    A(h3("Qa — advantages of out-of-order"))
    A(bullets([
        "Executes past a stalled instruction, so the pipeline is not blocked by one slow instruction.",
        "Exploits ILP that the compiler cannot see (e.g. after a cache miss).",
        "Improves utilisation of the functional units.",
    ]))
    A(h3("Qb — pipeline with a static predictor"))
    A(formula("Fetch uses the predicted PC; if the prediction is wrong, the wrong-path\n"
              "  instructions are flushed when the branch resolves."))
    A(h3("Qc — Tomasulo and the cycle for F10"))
    A(p("F10 is produced by DIV F10, F0, F6. Its execute-complete cycle is determined by when F0 (from "
        "MUL) and F6 (from the load) become ready, plus the divide latency. Work the tables to get the "
        "exact cycle; the answer is the Write-result cycle of the DIV."))
''')

PYQS[35] = dict(
 title="ca35 — Critical-word-first and early restart cycles; merging write-buffer size and speed-up",
 transcript="""Q. (a) With critical-word-first and early restart, compute the cycles saved.
   (b) Find the write-buffer size needed and the resulting speed-up from merging writes.""",
 explain=r'''
    A(h3("Qa — critical-word-first / early restart"))
    A(formula("Without: the CPU waits for the whole block = block transfer time.\n"
              "With critical-word-first: it waits only until the requested word arrives.\n"
              "  cycles saved = (words after the critical word) × transfer time per word.\n"
              "Example: 4 words, requested word last → wait 4× instead of 1×; save 3 transfers."))
    A(h3("Qb — merging write buffer"))
    A(formula("Buffer size = (number of writes that must be held) × (bytes per write).\n"
              "Merging writes to the same block reduces the number of memory writes,\n"
              "  improving throughput by the merge factor."))
''')

PYQS[36] = dict(
 title="ca36 — Amdahl with a slowdown (FP faster, cache slower); vectorisation percentage",
 transcript="""Q. (a)(i) A new FP unit speeds FP by 2×; FP is 20% of execution time — overall
       speed-up?
   (a)(ii) The FP unit speeds up but the cache slows down — combine.
   (b) What fraction of a computation must be vectorised to match a 2× vector
       speed-up?""",
 explain=r'''
    A(h3("Qa(i) — FP 2× faster, FP = 20% of time"))
    A(formula("S = 1 / [ (1 − 0.20) + 0.20/2 ] = 1 / (0.80 + 0.10) = 1/0.90 ≈ 1.11×"))
    A(h3("Qa(ii) — speed-up here, slowdown there"))
    A(formula("Combine the two effects on the total time:\n"
              "  T_new = T_old[ (FP part)/k_fp + (cache part)/k_cache + (rest) ]\n"
              "  S = 1 / [ f_fp/k_fp + f_cache/k_cache + f_rest ]\n"
              "If the cache slows (k_cache < 1) it can cancel the FP gain."))
    A(h3("Qb — vectorisation fraction for a 2× speed-up"))
    A(formula("S = 1 / [ (1 − p) + p/2 ] = 2  →  solve for p:\n"
              "  1 = 2[(1 − p) + p/2]  →  0.5 = (1 − p) + p/2 = 1 − p/2  →  p = 1.0\n"
              "So with a 2× vector speed-up you need 100% of the work vectorised to\n"
              "reach 2× overall (any scalar remainder caps the speed-up)."))
''')

PYQS[37] = dict(
 title="ca37 — Micro-benchmark cache block sizes from a latency chart; direct-mapped address components",
 transcript="""Q. (a) From a latency-vs-stride chart, deduce the cache block size(s).
   (b) For a direct-mapped cache, find the address components (tag/index/offset).""",
 explain=r'''
    A(h3("Qa — deducing block size from a stride chart"))
    A(p("A micro-benchmark walks memory with increasing stride and records the latency. The latency "
        "stays low while the stride stays within one block and jumps when the stride crosses a block "
        "boundary, so the first jump in the chart reveals the block size. A second jump reveals the "
        "next level (e.g. the L2 block size)."))
    A(h3("Qb — direct-mapped address components"))
    A(formula("offset = log₂(block size)\n"
              "index  = log₂(number of lines)  = log₂(cache size / block size)\n"
              "tag    = address width − index − offset"))
''')

PYQS[38] = dict(
 title="ca38 — Direct-mapped cache: misses, evictions, non-empty blocks; BTB penalty",
 transcript="""Q. (a) For a sequence of addresses in a direct-mapped cache, count the misses and
    evictions and show which blocks are non-empty.
   (b) Compute the branch-target-buffer penalty.""",
 explain=r'''
    A(h3("Qa — misses and evictions"))
    A(formula("line = (block number) mod (number of lines)\n"
              "For each access: if the line is empty → compulsory miss; if it holds a\n"
              "  different tag → conflict miss (evict the old block); if the tag matches\n"
              "  → hit.\n"
              "Track the tag stored in each line after every access."))
    A(h3("Qb — BTB penalty"))
    A(formula("penalty = hit_rate × correct_penalty + (1 − hit_rate) × mispredict_penalty"))
''')

PYQS[39] = dict(
 title="ca39 — Register renaming with T-registers; stalls with a dependence-aware pipeline; Tomasulo and ROB",
 transcript="""Q. (a) Apply register renaming with temporary (T) registers.
   (b) Count the stalls in a dependence-aware pipeline.
   (c) Describe Tomasulo and the reorder buffer.""",
 explain=r'''
    A(h3("Qa — renaming with T-registers"))
    A(formula("Each new value gets a fresh temporary register:\n"
              "  A[i] → T1 ;  B[i] → T2 ;  C[i] → T3 …\n"
              "This removes WAW and WAR (name) dependences; RAW dependences remain."))
    A(h3("Qb — stalls"))
    A(formula("Count load-use pairs (1 stall each) and structural conflicts; ALU→ALU\n"
              "  pairs add 0 stalls with forwarding."))
    A(h3("Qc — Tomasulo + ROB"))
    A(p("Tomasulo’s reservation stations + CDB handle dynamic scheduling; adding a reorder buffer gives "
        "in-order commit and precise exceptions, enabling speculation."))
''')

PYQS[40] = dict(
 title="ca40 — Tomasulo + ROB/commit; vector vs hybrid (GPU) execution time",
 transcript="""Q. (a) Discuss Tomasulo with a reorder buffer and the commit stage.
   (b) Compare the execution time of a vector architecture with a hybrid (GPU)
    architecture.""",
 explain=r'''
    A(h3("Qa — Tomasulo + ROB + commit"))
    A(formula("Issue → Execute → Read → Write (ROB) → Commit (in order).\n"
              "The ROB holds speculative results; commit writes them to the\n"
              "architectural state in program order, giving precise exceptions."))
    A(h3("Qb — vector vs hybrid (GPU) execution time"))
    A(formula("Vector:  time = (elements / vector length) × cycles per vector op\n"
              "Hybrid/GPU: time = max(compute time, memory time)\n"
              "  compute time = work / (cores × ops per cycle × clock)\n"
              "  memory time = bytes moved / bandwidth\n"
              "The architecture with the smaller time wins; often the GPU is\n"
              "  memory-bound and the vector unit compute-bound."))
''')

PYQS[41] = dict(
 title="ca41 — Vector / array processor features used in GPUs",
 transcript="""Q. Which features of vector/array processors are used in GPUs?""",
 explain=r'''
    A(h3("Vector/array features carried into GPUs"))
    A(bullets([
        "<b>SIMD lanes</b> — one instruction drives many ALUs (vector lanes), exactly as in a vector "
        "processor.",
        "<b>Pipelined vector functional units</b> — the ALUs are deeply pipelined to process streams of "
        "elements.",
        "<b>Vector registers</b> — wide register files hold many elements per thread (registers per "
        "thread).",
        "<b>Regular data flow</b> — both architectures assume regular, independent data (no cross-lane "
        "dependencies in the common case).",
        "<b>Latency hiding by parallelism</b> — many threads/warps keep the lanes busy, the same idea as "
        "a long vector operation.",
        "<b>Memory bandwidth focus</b> — both are designed to stream data at high bandwidth.",
    ]))
    A(callout("<b>Difference.</b> A classic vector processor is a single instruction stream with a "
        "vector-length register; a GPU runs thousands of independent threads (MIMD at the thread level, "
        "SIMD within a warp), so it tolerates irregular control flow far better.", 'tip'))
''')
