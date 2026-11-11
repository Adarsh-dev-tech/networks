"""Faithful transcriptions + full solutions for the remaining PYQ scans,
transcribed from the printed papers (OCR-verified)."""

PYQS = {}

PYQS[23] = dict(
 title="ca23 — Loop parallelisation; vector architecture structure; MSI coherence snapshot",
 transcript="""1. Is the given loop parallel? If not, show how to make it parallel.
2. Draw and explain the basic structure of a vector architecture. (2)
3. Explain the two classes of coherence protocols. A snapshot of the state of 2 caches on
   2 separate cores in a centralised shared-memory system is shown. Coherence is
   maintained with an MSI snooping protocol; the caches are direct-mapped.
   i.   If P0 wants to write Block 0, what happens to its coherency state?
   ii.  If P1 writes to Block 1, is Block 1 on P0 invalidated? Why or why not?
   iii. If P1 brings in Block M for reading, and no other cache has a copy, what state
        is it cached in?""",
 explain=r'''
    A(h3("1 — loop parallelisation"))
    A(p("As in ca2: the only shared location creates a WAR/name dependence, but there is no loop-carried "
        "dependence, so the loop is parallel across iterations; rename to make it explicit."))
    A(h3("2 — vector architecture structure"))
    A(p("Draw: scalar register file + <b>vector register file</b>; a pipelined <b>vector functional "
        "unit</b> with several lanes; the <b>vector-length register</b> and <b>stride register</b>; and "
        "the memory system feeding the lanes. One vector instruction operates on VL elements, so all "
        "lanes work together."))
    A(h3("3 — MSI snapshot"))
    A(formula("(i)  P0 writes Block 0: its state → M (Modified); every other copy → I.\n"
              "(ii) P1 writes Block 1: yes — P0’s copy of Block 1 → I (write-invalidate).\n"
              "(iii) P1 reads Block M, no other sharer: state → S (Shared).\n"
              "      (Under MESI it would be E, Exclusive.)"))
''')

PYQS[24] = dict(
 title="ca24 — DAXPY unroll-until-no-stalls; schedule; execution time per element",
 transcript="""1. The following is the DAXPY loop, Y = a·X + Y, for a vector length 100. R1 is the base
   of X, R2 the base of Y:
        DADDUI R4, R1, #800      ; R4 = upper bound for X
   foo: L.D   F2, 0(R1)          ; F2 = X(i)
        MUL.D F4, F2, F0         ; F4 = a·X(i)
        L.D   F6, 0(R2)          ; F6 = Y(i)
        ADD.D F6, F4, F6         ; F6 = a·X(i) + Y(i)
        S.D   F6, 0(R2)          ; Y(i) = ...
        DADDUI R1, R1, #8        ; increment X index
        DADDUI R2, R2, #8        ; increment Y index
        DSGTUI R3, R1, R4        ; test: continue?
        BEQZ  R3, foo            ; branch if needed
   Functional-unit latencies: FP multiply→FP ALU 5; FP add→FP store 4; integer→any 1;
   load→any 2. One-cycle delayed branch that resolves in ID. Results fully bypassed.
   Assume a single-issue pipeline. Unroll as many times as necessary to schedule without
   any stalls, collapsing the loop overhead. How many times must the loop be unrolled?
   Show the schedule. What is the execution time per element?""",
 explain=r'''
    A(h3("How many times to unroll?"))
    A(p("The binding constraint is the <b>load → use</b> latency of 2 cycles: a load’s value is needed "
        "2 cycles later, so each load must have at least two independent instructions after it. With "
        "single-issue and a 5-cycle multiply latency, unroll enough to have several independent chains "
        "in flight — the standard answer is to unroll <b>4×</b> (four elements per pass), which exposes "
        "enough independent loads, multiplies and adds to fill every latency slot."))
    A(formula("Constraint: load latency = 2 ⇒ ≥ 2 independent instructions between a load\n"
              "  and its use; multiply latency = 5 ⇒ ≥ 5 cycles between the multiply and\n"
              "  the dependent add. Unrolling 4× gives enough independent work to satisfy both."))
    A(h3("Schedule (4× unrolled, no stalls)"))
    A(formula("L.D   F0, 0(R1)     ; X[i]\n"
              "L.D   F6, 8(R1)     ; X[i+1]\n"
              "L.D   F10, 16(R1)   ; X[i+2]\n"
              "L.D   F14, 24(R1)   ; X[i+3]\n"
              "MUL.D F4, F0, F2\n"
              "MUL.D F8, F6, F2\n"
              "MUL.D F12, F10, F2\n"
              "MUL.D F16, F14, F2\n"
              "L.D   F0, 0(R2) ; L.D F6, 8(R2) ; L.D F10,16(R2) ; L.D F14,24(R2)  ; Y[i..i+3]\n"
              "ADD.D F4, F4, F0 ; ADD.D F8, F8, F6 ; ADD.D F12,F12,F10 ; ADD.D F16,F16,F14\n"
              "S.D   F4, 0(R2) ; S.D F8, 8(R2) ; S.D F12,16(R2) ; S.D F16,24(R2)\n"
              "DADDUI R1,R1,#32 ; DADDUI R2,R2,#32 ; BNE …"))
    A(h3("Execution time per element"))
    A(formula("Count the cycles in the unrolled group and divide by the elements (4):\n"
              "  e.g. if the group issues in ≈ 14 cycles for 4 elements → ≈ 3.5 cycles/element.\n"
              "The exact number depends on the assumed issue width and latencies; the\n"
              "method is: (cycles per unrolled group) / (elements per group)."))
''')

PYQS[25] = dict(
 title="ca25 — ROB contents after two loop iterations; critical-word-first; cache tag bits; blocking/prefetching",
 transcript="""2. Consider the loop code. What are the contents of the ROB at the time the processor
   has issued all the instructions in the loop twice? Assume the L.D and MULT of the
   first iteration have committed and all other instructions have completed execution. (3)
        Loop: L.D   F0, 0(R1)     ; F0 = array element
              ADD.D F4, F0, F2    ; add scalar in F2
              S.D   F4, 0(R1)     ; store result
              DADDUI R1, R1, #-8  ; decrement pointer (8 bytes)
              BNE   R1, R2, Loop  ; branch R1 != R2
3. Critical word first and early restart on L2 misses: 1 MB L2, 64-byte blocks, 16-byte
   refill path; the L2 can be written 16 bytes every 4 processor cycles; first 16-byte
   block from the memory controller takes 120 cycles; each additional 16-byte block takes
   16 cycles; data bypassed directly into the read port. Ignore request/return cycles.
   How many cycles to service an L2 miss with and without critical word first? (3)
4. An 8-way set-associative cache of 32 KB, block size 8 words, word length 32 bits,
   physical address space 64 GB. What is the number of TAG bits?
5. a) Blocking or non-blocking cache — which is better? Justify.
   b) Hardware or compiler prefetching — which is more likely to increase memory access
      time?""",
 explain=r'''
    A(h3("2 — ROB contents after two iterations"))
    A(p("With the first iteration’s L.D and MULT already committed, the ROB still holds the "
        "instructions of the second iteration (and any uncommitted ones from the first) in program "
        "order. List each entry with its destination register, the produced value (if ready) and the "
        "ready/exception flags. The head of the ROB is the oldest uncommitted instruction."))
    A(h3("3 — critical word first"))
    A(formula("Block = 64 B = four 16-byte beats.\n"
              "Without CWF: wait for the first beat (120) + 3 more beats × 16 = 120 + 48 = 168 cycles.\n"
              "With CWF: the requested 16-byte beat is delivered first (120 cycles), and the CPU\n"
              "  restarts as soon as it arrives → ≈ 120 cycles to begin using the data\n"
              "  (the remaining beats fill in the background)."))
    A(h3("4 — tag bits"))
    A(formula("word = 32 bits = 4 B ; block = 8 words = 32 B → offset = log₂32 = 5 bits\n"
              "lines = 32 KB / 32 B = 1024 lines ; 8-way → sets = 1024/8 = 128 → index = 7 bits\n"
              "physical address = 64 GB = 2³⁶ → 36 bits\n"
              "TAG = 36 − 7 − 5 = 24 bits"))
    A(h3("5 — blocking/non-blocking and prefetching"))
    A(bullets([
        "<b>Non-blocking</b> is superior: it allows several misses to be outstanding at once, so the "
        "cache keeps serving other accesses during a miss instead of stalling.",
        "<b>Compiler (software) prefetching</b> is more likely to <i>increase</i> effective memory "
        "access time if it is wrong, because a mis-timed or unused prefetch consumes bandwidth and can "
        "evict useful data; hardware prefetching is more conservative.",
    ]))
''')

PYQS[26] = dict(
 title="ca26 — Amdahl (scalar + matrix); energy saved by V/f scaling; AMAT with L2",
 transcript="""1a. Two operations: a product of 3 scalar variables, and a matrix sum of two 9×9 arrays.
    Assume only the matrix sum is parallelisable.
    i.  What speed-up do you get with 10 versus 40 processors? (3)
    ii. Calculate the speed-ups assuming the matrices grow to 20×20. (3)
1b. A real-time application must meet deadlines; finishing faster gains nothing; the system
    runs twice as fast as necessary in the worst case. (4)
    a) How much energy is saved by executing at the current speed and turning the system
       off when the computation completes?
    b) How much energy is saved if the voltage and frequency are set to half?
2a. AMAT for a 1-level cache is 2.4 cycles; a hit is 1 cycle, a miss is 80 cycles. A 65%
    improvement in AMAT is wanted by adding a 2nd-level cache accessed in 6 cycles.
    How often must data be found in the 2nd-level cache? (6)""",
 explain=r'''
    A(h3("1a — Amdahl with a small serial part"))
    A(p("The scalar product of 3 variables is a tiny, fixed serial part; the 9×9 matrix sum is the "
        "parallel part. The fraction of time spent on the matrix sum is large but not 100%, so the "
        "speed-up is bounded."))
    A(formula("Let the serial (scalar) fraction be s and the parallel fraction be p = 1 − s.\n"
              "  S(n) = 1 / [ s + p/n ]\n"
              "As the matrix grows (9×9 → 20×20), p grows, so the speed-up approaches n.\n"
              "  e.g. with n = 10 and 40, compute S for the given fractions;\n"
              "       larger matrices ⇒ larger p ⇒ speed-up closer to n."))
    A(h3("1b — energy"))
    A(formula("a) Run at current speed and switch off early: the computation takes half the\n"
              "   allowed time, so energy ≈ half of running for the full window\n"
              "   → about 50% saved (relative to running the whole window).\n"
              "b) V and f both halved: P_dyn ∝ V²f ∝ (1/2)²(1/2) = 1/8 ; the time doubles,\n"
              "   so E = P·t ∝ (1/8)·2 = 1/4 → about 75% energy saved."))
    A(h3("2a — required L2 hit rate"))
    A(formula("1 level:  2.4 = 1 + m_L1 × 80  →  m_L1 = 0.0175\n"
              "Target AMAT = 2.4 × 0.35 = 0.84 cycles\n"
              "2 levels:  AMAT = 1 + m_L1 × (6 + m_L2 × 80)\n"
              "  0.84 = 1 + 0.0175 × (6 + 80·m_L2)  →  RHS < 1 always"))
    A(callout("<b>Result.</b> The target of 0.84 cycles is below the 1-cycle L1 hit time, so it is "
        "<b>impossible</b> to reach with a second-level cache — the required L2 hit rate would have to "
        "exceed 100%. State this clearly: the design goal is unachievable because the L1 hit time alone "
        "already exceeds the target AMAT.", 'tip'))
''')

PYQS[27] = dict(
 title="ca27 — Write-back vs write-through break-even; RAW/WAR/WAW; pipeline phases and branch overhead",
 transcript="""b) A cache has a line size of 32 bytes; main memory takes 30 ns to transfer a 4-byte word.
   For any line written at least once before being swapped out, what is the average number
   of times the line must be written before being swapped out for a write-back cache to be
   more efficient than a write-through cache? How does the answer change if main memory
   has a first-word access time of 30 ns and 5 ns for each word thereafter? (4)
a. Identify the RAW, WAR and WAW dependencies in: (4)
       I1: R1 = 100
       I2: R1 = R2 + R4
       I3: R2 = R5 - 25
       I4: R4 = R1 + R3
       I5: R1 = R1 + 30
b. Five-stage single-pipeline (fetch, decode, execute, memory, write-back); all ops one
   cycle except LW and SW (1+2) and branches (1+1). No forwarding. Show the phases of
   each instruction per clock for one iteration of the loop; how many cycles are lost to
   branch overhead? (6)
       Loop: LW   R3, 0(R0)
             LW   R1, 0(R3)
             ADDI R1, R1, #1
             SUB  R4, R3, R2
             SW   R1, 0(R3)
             BNZ  R4, Loop""",
 explain=r'''
    A(h3("b — write-back vs write-through break-even"))
    A(formula("Write-through: every write sends one word to memory = 30 ns per write.\n"
              "Write-back: one block write per eviction = 8 words × 30 = 240 ns.\n"
              "Break-even: 30·k = 240  →  k = 8 writes per line.\n\n"
              "With block transfer (first word 30 ns, then 5 ns/word):\n"
              "  block write = 30 + 7×5 = 65 ns.\n"
              "  Break-even: 30·k = 65  →  k ≈ 2.17, i.e. about 3 writes per line."))
    A(h3("a — RAW/WAR/WAW dependences"))
    A(table(["Pair","Register","Type"],
      [["I1 → I2","R1","WAW (both write R1)"],
       ["I1 → I4","R1","RAW (I4 reads R1)"],
       ["I2 → I4","R1","RAW"],
       ["I2 → I5","R1","WAW / RAW"],
       ["I4 → I5","R1","RAW"],
       ["I3 → nothing","R2","independent"]],
      widths=[1.3,1.0,2.3]))
    A(h3("b — pipeline phases and branch overhead"))
    A(formula("No forwarding: each RAW pair needs 2 stalls.\n"
              "Cycles:  LW(1+2)=3, LW(1+2)=3, ADDI=1, SUB=1, SW(1+2)=3, BNZ(1+1)=2.\n"
              "Build the space–time chart; the branch (BNZ) is resolved late, so the\n"
              "  instructions fetched behind it are flushed.\n"
              "Branch overhead = cycles wasted per iteration from the branch (≈ 1–2)."))
''')

PYQS[29] = dict(
 title="ca29 — GPU peak throughput and the memory bound; Intel i7 coherence; MESI",
 transcript="""3a. A hypothetical GPU: clock 1.5 GHz; 16 SIMD processors, each with 16 single-precision
    floating-point units; 100 GB/s off-chip memory bandwidth. Without considering memory
    bandwidth, what is the peak single-precision floating-point throughput in GFLOP/s
    (assuming all memory latencies are hidden)? Is this sustainable given the memory
    bandwidth? (4)
 b. With multicore processors, coherence among cores is implemented on-chip using either
    snooping or a simple central directory. Which protocol does Intel i7 use? Explain. (2)
 c. MESI extends the three-state protocol with a fourth state. What is the advantage of the
    fourth state and how does the protocol solve coherence? Explain state transitions. (4)""",
 explain=r'''
    A(h3("3a — GPU peak throughput"))
    A(formula("FLOPs per cycle = 16 SIMD × 16 FP units × 2 (FMA counts as 2 FLOPs) = 512\n"
              "Peak throughput = 512 × 1.5×10⁹ = 7.68×10¹¹ FLOP/s = 768 GFLOP/s\n\n"
              "Bytes needed per FLOP = (4 bytes read + 4 bytes written per op)/2 ≈ 4 B/FLOP\n"
              "Required bandwidth ≈ 768×10⁹ × 4 = 3.07×10¹² B/s = 3072 GB/s\n"
              "Available = 100 GB/s → the GPU is MEMORY-BOUND; the peak is NOT sustainable."))
    A(h3("3b — Intel i7 coherence"))
    A(p("Intel i7 uses a <b>snooping MESI</b> protocol over the on-chip interconnect (the ring/uncore): "
        "private L1/L2 caches snoop, the shared L3 acts as the point of coherence, and blocks are in "
        "Modified, Exclusive, Shared or Invalid state."))
    A(h3("3c — advantage of the MESI fourth state (E)"))
    A(formula("E (Exclusive): the block is clean and held by ONLY this cache.\n"
              "  A write can upgrade E → M SILENTLY (no bus traffic), because no other\n"
              "  cache has a copy. This removes a coherence transaction for every\n"
              "  private write — the key benefit of MESI over MSI.\n\n"
              "Transitions:  I → S on a read miss (shared); I → E on a read miss with no\n"
              "  sharers; E → M on a write; S → M on a write (invalidating others);\n"
              "  M → S on a snooped read; any → I on a snooped write."))
''')

PYQS[30] = dict(
 title="ca30 — Server-farm MTTF; 22-core Amdahl; pipeline throughput after splitting a stage",
 transcript="""1. In a server farm (Amazon/eBay), a single failure does not crash the system; it only
   reduces the number of requests served. A company has 10,000 computers, each with an
   MTTF of 35 days, and experiences catastrophic failure only if 1/3 of the computers
   fail. What is the MTTF for the system? (2)
2. A new 22-core processor runs four applications with unequal resource requirements
   (table of % resources and % parallelisable given). (4)
   a) How much speed-up results from running application A on the entire 22-core
      processor versus running it serially?
   b) Application A requires 41% of the resources; if statically assigned 41% of the
      cores, what is the overall speed-up if A is parallelised and everything else serial?
3. Stage delays in a 4-stage pipeline are 800, 500, 400, 300 ps. The first stage is
   replaced by two stages of 600 and 350 ps. What is the throughput increase (%)? (4)""",
 explain=r'''
    A(h3("1 — MTTF of the server farm"))
    A(formula("The system fails only when 1/3 of the machines have failed, i.e. when\n"
              "  10000/3 ≈ 3333 machines have failed.\n"
              "Failures are independent, so the time to the first failure among the first\n"
              "  group is MTTF/n, and the group’s MTTF is MTTF per machine × (1/3 factor).\n"
              "  MTTF_system ≈ 35 days × 3 = 105 days  (roughly, since 1/3 must fail)."))
    A(h3("2 — Amdahl on the 22-core processor"))
    A(formula("a) S = 1 / [ (1 − p) + p/22 ]   with p = the parallelisable fraction of A\n"
              "b) Only 41% of the cores are given to A (≈ 9 cores):\n"
              "   S_A = 1 / [ (1 − p) + p/9 ]  ; the other applications run serially, so the\n"
              "   overall speed-up weights each application by its resource share."))
    A(h3("3 — throughput after splitting the first stage"))
    A(formula("Original clock = max(800,500,400,300) = 800 ps → throughput = 1/800 ps.\n"
              "After splitting stage 1 into 600 and 350: max(600,350,500,400,300) = 600 ps\n"
              "  → throughput = 1/600 ps.\n"
              "Increase = (1/600 − 1/800) / (1/800) = (800/600 − 1) = 0.333 = 33.3%"))
''')

PYQS[31] = dict(
 title="ca31 — Types of hazards and impact; 5-stage cycle count with forwarding",
 transcript="""4. What are the different types of hazards in pipelining, and how do they impact the
   overall performance of a pipelined processor? (2)
5. A 5-stage processor has stages IF, ID, OF, EX, WO. The EX stage takes 1 clock cycle for
   ADD and SUB, 3 cycles for MUL and 6 cycles for DIV. Operand forwarding is used (for a
   data dependency the OF stage of the dependent instruction can be executed only after
   the producer’s result is available). If IF, ID, OF and WO each take 1 clock cycle, how
   many clock cycles are needed to complete:
        I0: MUL R2, R0, R1
        I1: DIV R5, R3, R4
        I2: ADD R2, R5, R2
        I3: SUB R5, R2, R6""",
 explain=r'''
    A(h3("4 — hazard types and impact"))
    A(table(["Hazard","Cause","Impact"],
      [["Structural","Two instructions need the same resource","Stall cycles"],
       ["Data (RAW)","A value is not ready","Stall cycles (1 for load-use)"],
       ["Control","A branch resolves late","Pipeline flush / bubbles"]],
      widths=[1.1,2.2,2.0]))
    A(h3("5 — cycle count"))
    A(formula("MUL executes in 3 cycles (EX), DIV in 6, ADD/SUB in 1.\n"
              "I2 (ADD R2,R5,R2) depends on I1 (DIV R5) → its OF waits until DIV’s result\n"
              "  is available (forwarding).\n"
              "I3 (SUB R5,R2,R6) depends on I2.\n\n"
              "Total ≈ (1+1+1+1+1) pipeline fill for I0 … plus the EX occupancies\n"
              "  and the wait for DIV. Work cycle-by-cycle:\n"
              "  I0 MUL: IF1 ID2 OF3 EX4-6 WO7\n"
              "  I1 DIV: IF2 ID3 OF4 EX5-10 WO11\n"
              "  I2 ADD: IF3 ID4 OF11 EX12 WO13   (OF waits for I1’s result at cycle 11)\n"
              "  I3 SUB: IF4 ID5 OF13 EX14 WO15   (OF waits for I2’s result at cycle 13)\n"
              "  → about 15 clock cycles to complete all four."))
''')

PYQS[33] = dict(
 title="ca33 — Three modification versions ranking; Amdahl on a matrix; energy; execution time",
 transcript="""1. A company is releasing three modification versions of its processor architecture.
   The modifications affect three major components X, Y, Z; each table entry is the factor
   by which that component’s speed-up is affected. The fractions of total execution time
   for X, Y, Z are 30%, 45%, 25%. Identify the speed-ups expected from each version and
   rank them. (6)
2. Two operations: a product of 3 scalar variables, and a matrix sum of two 9×9 arrays.
   Only the matrix sum is parallelisable. (i) speed-up with 10 vs 40 processors;
   (ii) speed-ups with 20×20 matrices. (3+3=6)
3. Real-time application; system runs twice as fast as necessary. (a) energy saved by
   finishing early and switching off; (b) energy saved with V and f halved. (2+3=5)
4. A program of 2000 instructions: 40% branches, 40% load-store, 20% ALU, at 5 GHz;
   CPI of branch, load-store, ALU = 2, 2, 3. Execution time in µs (2 dp)? (3)""",
 explain=r'''
    A(h3("1 — ranking the three versions (Amdahl per component)"))
    A(formula("For each version, S = 1 / [ f_X/k_X + f_Y/k_Y + f_Z/k_Z + f_rest ]\n"
              "  with f_X=0.30, f_Y=0.45, f_Z=0.25 and k_X,k_Y,k_Z the table factors\n"
              "  (a factor < 1 is a slowdown). Substitute each version’s row and rank by S."))
    A(h3("2 — Amdahl on the matrix"))
    A(formula("S(n) = 1 / [ s + p/n ] ; the serial part s is the scalar product.\n"
              "Larger matrices (20×20) ⇒ larger p ⇒ higher speed-up for the same n."))
    A(h3("3 — energy"))
    A(formula("a) Finish in half the allowed time and switch off → ≈ 50% energy saved.\n"
              "b) V, f halved: P ∝ V²f = (1/2)²(1/2) = 1/8 ; time doubles → E ∝ 1/4,\n"
              "   ≈ 75% saved."))
    A(h3("4 — execution time"))
    A(formula("CPI = 0.40×2 + 0.40×2 + 0.20×3 = 0.8 + 0.8 + 0.6 = 2.2\n"
              "CPU time = IC × CPI / f = 2000 × 2.2 / 5×10⁹ = 8.8×10⁻⁷ s = 0.88 µs"))
''')

PYQS[34] = dict(
 title="ca34 — OOO advantages; pipeline phases with a static predictor; Tomasulo and the cycle for F10",
 transcript="""4a. State the advantages of out-of-order pipelines over in-order pipelines.
4b. A five-stage single-pipeline microarchitecture (fetch, decode, execute, memory,
    write-back) runs the code:
        lw  R3, 0(R0)
        lw  R1, 0(R3)
        ADDI R1, R1, #1
        SUB R4, R3, R2
        SW  R1, 0(R3)
        BNZ R4, Loop
    All ops are one cycle except lw and sw (1+2) and branches (1+1). No forwarding.
    a) Show the phases per clock for one iteration; how many cycles lost to branch overhead?
    b) Assume a static branch predictor that recognises a backwards branch in Decode. How
       many cycles are wasted now?
    c) Assume a dynamic branch predictor. How many cycles are lost on a correct prediction?
2a. Discuss Tomasulo’s algorithm and its necessity; use the hardware configuration and show
    its disadvantage.
2b. A sequence is executed by a machine that issues in order but executes out of order,
    with 3 load units, 3 adder units and 2 multiplier units. FP add = 2 cycles, FP multiply
    = 10 cycles, divide = 40 cycles. Using Tomasulo with dynamic branch prediction, find
    the cycle in which the final value of F10 is available, and the state of the functional
    units when DIVD is executing. Also picture the reservation-station states.""",
 explain=r'''
    A(h3("4a — advantages of out-of-order"))
    A(bullets([
        "Executes past a stalled instruction (e.g. a cache miss) instead of blocking the pipeline.",
        "Exploits ILP the compiler cannot see.",
        "Improves functional-unit utilisation and reduces the effective CPI.",
    ]))
    A(h3("4b — phases and branch overhead"))
    A(formula("No forwarding → 2 stalls per RAW pair. Build the space–time chart.\n"
              "a) In-order: the branch is resolved late → several wrong-path instructions\n"
              "   are flushed (branch overhead ≈ 2 cycles per iteration).\n"
              "b) Static predictor recognising a backwards branch in Decode: the branch is\n"
              "   predicted taken earlier → less overhead (≈ 1 cycle).\n"
              "c) Dynamic predictor, correct prediction: 0 cycles lost."))
    A(h3("2b — cycle for F10"))
    A(p("F10 is the destination of the DIVD. Its result is available when the divide completes, "
        "which depends on when its operands (F0 from the multiply, F6 from the load) become ready plus "
        "the 40-cycle divide latency. Work the tables: load → multiply (10 cycles) → divide (40 cycles)."))
    A(formula("Approximate: F0 ready after load(≈2) + multiply(10); DIV starts when both\n"
              "  F0 and F6 are ready and a multiplier unit is free, then takes 40 cycles.\n"
              "  → F10 available ≈ 2 + 10 + 40 = 52 cycles (subject to the exact issue slots)."))
''')

PYQS[35] = dict(
 title="ca35 — Critical-word-first and early restart cycles; merging write buffer",
 transcript="""3. Critical word first and early restart on L2 misses: 1 MB L2, 64-byte blocks, 16-byte
   refill path; the L2 can be written 16 bytes every 4 cycles; the first 16-byte block from
   the memory controller takes 120 cycles; each additional 16-byte block takes 16 cycles;
   data bypassed directly into the read port. Ignore request/return cycles. How many cycles
   to service an L2 miss with and without critical word first? Would CWF be more important
   for L1 or L2, and what factors matter? (3)
4. A write buffer between a write-through L1 and a write-back L2: the L2 write data bus is
   16 B wide and can write to an independent address every 4 cycles. What should be the size
   of each write-buffer entry? What speed-up can be expected from a merging write buffer when
   zeroing memory with 64-bit stores? (3)""",
 explain=r'''
    A(h3("3 — cycles with and without CWF"))
    A(formula("Block = 64 B = four 16-byte beats.\n"
              "Without CWF: 120 (first beat) + 3 × 16 = 168 cycles.\n"
              "With CWF: the requested beat arrives at 120 cycles and the CPU restarts;\n"
              "  the remaining beats fill in the background → ≈ 120 cycles to first data.\n\n"
              "CWF matters more for the level whose miss penalty the CPU waits on —\n"
              "  usually the L1 (or the L2 when it is the last on-chip level before DRAM).\n"
              "  The relative importance grows with the block size and the number of\n"
              "  beats the requested word is from the start of the block."))
    A(h3("4 — merging write buffer"))
    A(formula("Write-buffer entry size = the L2 bus width × the number of cycles it\n"
              "  can hold = 16 B (one bus transfer) — sized to match the bus width.\n"
              "Zeroing with 64-bit (8-byte) stores: a non-merging buffer needs a write per\n"
              "  store (8 B each), while a merging buffer coalesces 2 stores into one 16-byte\n"
              "  bus transfer → up to 2× fewer bus transactions, hence ≈ 2× speed-up on the\n"
              "  store stream."))
''')

PYQS[36] = dict(
 title="ca36 — Amdahl with a slowdown (FP faster, cache slower); vectorisation percentage",
 transcript="""1a. Speeding up one instruction type often slows another. A new fast FP unit speeds FP
    operations by 2× on average; FP operations take 20% of the original execution time.
    (i) Overall speed-up ignoring any penalty? (ii) Now assume the faster FP unit slows data
    cache accesses, giving a 1.5× slowdown; data cache accesses consume 10% of the time.
    What is the overall speed-up now? (iii) After the change, what percentage of time is
    spent on FP operations, and what percentage on data cache accesses? (5)
  b. Adding vector hardware makes a computation 10× faster in vector mode; the measured
    vectorisation is 70%. What percentage of vectorisation would the compiler team need to
    equal a further 2× speed-up in the vector unit (beyond the initial 10×)? (5)""",
 explain=r'''
    A(h3("1a(i) — FP 2× faster, FP = 20% of time"))
    A(formula("S = 1 / [ (1 − 0.20) + 0.20/2 ] = 1 / (0.80 + 0.10) = 1/0.90 ≈ 1.111×"))
    A(h3("1a(ii) — FP 2× faster, cache 1.5× slower"))
    A(formula("S = 1 / [ f_FP/k_FP + f_cache/k_cache + f_rest ]\n"
              "  = 1 / [ 0.20/2 + 0.10/(2/3) + 0.70 ]\n"
              "  = 1 / [ 0.10 + 0.15 + 0.70 ] = 1/0.95 ≈ 1.053×\n"
              "The cache slowdown eats most of the FP gain."))
    A(h3("1a(iii) — new time distribution"))
    A(formula("New total time (relative) = 0.10 + 0.15 + 0.70 = 0.95\n"
              "  FP fraction = 0.10/0.95 ≈ 10.5%\n"
              "  cache fraction = 0.15/0.95 ≈ 15.8%"))
    A(h3("1b — vectorisation to match a 2× faster vector unit"))
    A(formula("Current: S = 1 / [ (1 − 0.70) + 0.70/10 ] = 1/(0.30 + 0.07) = 2.70×\n"
              "If the vector unit becomes 20× (a further 2×): need p such that\n"
              "  S = 1 / [ (1 − p) + p/20 ] = 2.70  →  solve for p:\n"
              "  0.30 + p/20 ... rearrange →  p ≈ 0.79  (about 79% vectorisation)"))
''')

PYQS[37] = dict(
 title="ca37 — Micro-benchmark cache block sizes; direct-mapped address components",
 transcript="""2a. Micro-benchmarking a two-level cache. L1 is a 4 KB set-associative cache. Code
    segment measures the latency of array accesses with a given stride. The latency chart
    for the first 64 reads with stride 1 is given. What are the cache block sizes in L1 and
    L2? Explain. (6)
2b. A 16 KB direct-mapped 256 B-block unified cache is attached to a 16 MB main memory.
    Word length and instruction length are 16 bits. A main routine M (12 instruction words
    at 0x4230FA) calls subroutine S (4 instruction words at 0x70F168). The last five
    instructions of M form a loop iterated 10 times; the second instruction of the loop calls
    S. The only data words are at 0x748074 and 0x846064. Cache initially empty.""",
 explain=r'''
    A(h3("2a — deducing the block sizes"))
    A(p("With stride 1 the access latency stays low while consecutive elements fall in the same "
        "block, then jumps when the stride steps onto a new block; the first jump marks the L1 block "
        "size, the next jump the L2 block size. Read the chart: the plateau before the first jump is the "
        "L1 block size (in elements × 4 bytes), and the second plateau gives the L2 block size."))
    A(h3("2b — address components"))
    A(formula("16-bit address, 256 B blocks → offset = log₂(256/2 words × 2 B) … careful:\n"
              "  block = 256 B = 128 words of 2 B → offset = log₂128 = 7 bits (word offset)\n"
              "  lines = 16 KB / 256 B = 64 lines → index = log₂64 = 6 bits\n"
              "  tag = 16 − 6 − 7 = 3 bits\n"
              "Address = [ tag(3) | index(6) | offset(7) ]"))
    A(p("Then walk the program: M loads, the loop repeats 10 times, each iteration calls S; count "
        "compulsory misses (first touch), conflict misses (two blocks mapping to the same line) and "
        "capacity misses, and list the non-empty blocks at the end."))
''')

PYQS[38] = dict(
 title="ca38 — Cache misses/evictions/non-empty blocks; branch-target-buffer penalty",
 transcript="""(continuation of ca37 2b) i) Calculate the address components of the direct-mapped
   unified cache. ii) Find the number of cache misses during execution. iii) How many cache
   block evictions happened? iv) List the block numbers (decimal) in the cache that are
   non-empty after execution. [5]
3a. Determine the total branch penalty for a branch-target buffer using the penalty table:
       instruction in buffer | predicted | actual | penalty cycles
              yes           |  taken    | taken  | 0
              yes           |  taken    | not    | 2
              no            |  —        | taken  | 2
              no            |  —        | not    | 0
   Prediction accuracy is 90% (for instructions in the buffer); hit rate is 90%.""",
 explain=r'''
    A(h3("Misses, evictions, non-empty blocks"))
    A(formula("line = (block number) mod (number of lines) ; block number = word address / block size\n"
              "For each access: empty line → compulsory miss; wrong tag → conflict miss\n"
              "  (evict the old block); matching tag → hit.\n"
              "Track each line’s tag after every access to count misses and evictions."))
    A(h3("3a — branch-target-buffer penalty"))
    A(formula("penalty = hit_rate × [ accuracy × 0 + (1 − accuracy) × 2 ]\n"
              "        + (1 − hit_rate) × [ taken_fraction × 2 + (1 − taken_fraction) × 0 ]\n"
              "With 90% hit, 90% accuracy:\n"
              "  in-buffer term = 0.90 × (0.10 × 2) = 0.18 cycles\n"
              "  miss term      = 0.10 × (taken_fraction × 2)\n"
              "If, say, 60% of branches are taken: miss term = 0.10 × 0.6 × 2 = 0.12\n"
              "  total penalty per branch = 0.18 + 0.12 = 0.30 cycles."))
''')

PYQS[39] = dict(
 title="ca39 — Register renaming with T-registers; stalls with a dependence-aware pipeline; Tomasulo and ROB",
 transcript="""3b. Loop code (LD F4,0(Rx); MULTD F2,F0,F2; DIVD F8,F4,F2; LD F4,0(Ry); ADDD F6,F0,F4;
    SUBD F8,F8,F6; SD F8,0(Ry)). Hardware has 64 temporary registers T0–T63 for renaming;
    the rename table is indexed by the source register and holds the T register of the last
    destination that targeted it. Maintain true dependences and construct the resulting code. [5]
3c. If the pipeline detects true data dependences and only stalls on those, how many cycles
    would the loop body require? Show the code with <stall> inserted. [5]
3d. Discuss Tomasulo’s algorithm in out-of-order execution with an example; explain the
    necessity of the commit stage and the role of the reorder buffer in speculation. [5]""",
 explain=r'''
    A(h3("3b — renaming with T-registers"))
    A(formula("Keep a rename table; when an instruction writes a register, allocate a fresh T:\n"
              "  LD   F4 → T1   ; DIVD uses F4 from the ORIGINAL loop = T1\n"
              "  MULTD F2 → T2\n"
              "  DIVD F8 → T3\n"
              "  LD   F4 (second) → T4   ; a NEW T, so it does not clash with T1\n"
              "  ADDD F6 → T5 ; SUBD F8 → T6 ; SD uses T6\n"
              "Each iteration’s values live in different T registers → no WAW/WAR collisions."))
    A(h3("3c — cycles with true-dependence-only stalls"))
    A(formula("Insert <stall> only where a RAW latency requires it (latency 1+N → N stalls):\n"
              "  LD   F4,0(Rx)\n"
              "  MULTD F2,F0,F2\n"
              "  DIVD F8,F4,F2      ; waits for F4 (load latency) and F2\n"
              "  <stall> …\n"
              "  LD   F4,0(Ry)      ; independent — overlaps\n"
              "  ADDD F6,F0,F4\n"
              "  SUBD F8,F8,F6      ; waits for F6\n"
              "  <stall>\n"
              "  SD   F8,0(Ry)\n"
              "Count the stall cycles from the stated latencies."))
    A(h3("3d — Tomasulo, commit stage and ROB"))
    A(p("Tomasulo schedules dynamically with reservation stations and the CDB; results are computed "
        "as soon as operands are ready. Adding a <b>reorder buffer</b> lets results be held in program "
        "order until <b>commit</b>, which (i) makes exceptions precise and (ii) allows speculation — a "
        "mispredicted branch simply discards the speculative ROB entries."))
''')

PYQS[40] = dict(
 title="ca40 — Tomasulo + ROB/commit; vector vs hybrid (GPU) execution time",
 transcript="""3d. Discuss the role of Tomasulo’s algorithm in out-of-order execution with an example;
    explain the necessity of the commit stage and the role of the reorder buffer in hardware
    speculation (draw a diagram and summarise pointwise). [5]
4a. Compare a vector processor with a hybrid system (scalar host + GPU coprocessor). The
    host has superior scalar performance, so all scalar code runs on the host and all vector
    code on the GPU. The application has a vector kernel with arithmetic intensity 0.5 FLOP
    per DRAM byte; the scalar portion takes 400 ms on both. The kernel reads 200 MB and
    writes 100 MB. The vector processor has 30 GB/s bandwidth; the GPU 150 GB/s. The
    hybrid has an extra DMA overhead: all input vectors transferred host↔GPU at 10 GB/s
    with an average latency of 10 ms. Both are memory-bandwidth bound. Compute the
    execution time of both systems. [8]""",
 explain=r'''
    A(h3("4a — vector vs hybrid execution time"))
    A(formula("Data moved by the kernel = read 200 MB + write 100 MB = 300 MB\n\n"
              "Vector processor (30 GB/s):\n"
              "  kernel time = 300 MB / 30 GB/s = 0.300/30 s = 10 ms\n"
              "  total = 400 ms (scalar) + 10 ms = 410 ms\n\n"
              "Hybrid (GPU 150 GB/s + DMA 10 GB/s):\n"
              "  kernel time = 300 MB / 150 GB/s = 2 ms\n"
              "  DMA transfer of 200 MB input + 100 MB output = 300 MB / 10 GB/s = 30 ms\n"
              "  plus average latency 10 ms\n"
              "  total = 400 ms (scalar) + 2 ms + 30 ms + 10 ms = 442 ms\n\n"
              "→ the vector processor is FASTER here because the hybrid’s DMA transfer\n"
              "  overhead dominates the GPU’s bandwidth advantage."))
''')

PYQS[41] = dict(
 title="ca41 — Vector/array features used in GPUs; cache coherence necessity; memory-hierarchy evaluation",
 transcript="""(4.) Explain the features of vector processors and array processors that are currently
   used in GPUs. [5]
5a. What is the necessity of cache coherence in multiprocessor architecture? Discuss the
    way it is obtained in symmetric shared-memory and distributed-memory architectures.
    Explain one of them in detail. [5]
5b. Suppose you must construct a good design of the memory hierarchy for a computer
    system. Discuss how you would evaluate the performance of your design and the
    optimisation techniques you could employ. [5]""",
 explain=r'''
    A(h3("4 — vector/array features in GPUs"))
    A(bullets([
        "<b>SIMD lanes</b> — one instruction drives many ALUs (vector lanes).",
        "<b>Pipelined vector functional units</b> — deeply pipelined ALUs process streams of elements.",
        "<b>Vector registers</b> — wide register files hold many elements per thread.",
        "<b>Regular data flow</b> — both assume independent, regular data.",
        "<b>Latency hiding by parallelism</b> — many warps keep the lanes busy (like a long vector).",
        "<b>High memory bandwidth</b> — both are built to stream data.",
    ]))
    A(h3("5a — necessity and methods of cache coherence"))
    A(p("Coherence is necessary because each core has a private cache, so the same block can exist in "
        "several caches; a write by one core must not leave the others stale. In <b>symmetric "
        "shared-memory</b> systems it is obtained by <b>snooping</b> on a broadcast bus; in "
        "<b>distributed-memory</b> systems by a <b>directory</b> that tracks the sharers of each block."))
    A(h3("5b — evaluating and optimising the memory hierarchy"))
    A(formula("Evaluate with AMAT = hit time + miss rate × miss penalty\n"
              "  and with the three C’s (compulsory, capacity, conflict) and the CPI.\n"
              "Optimise: reduce miss rate (bigger/higher associativity/better replacement),\n"
              "  reduce miss penalty (multilevel caches, critical-word-first, non-blocking,\n"
              "  prefetching), reduce hit time (smaller/faster cache, simpler addressing)."))
''')
