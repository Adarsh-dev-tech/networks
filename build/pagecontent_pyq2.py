"""Improved, faithful transcriptions + full solutions for several PYQ scans,
where the OCR of the printed paper is clear. These override the earlier entries."""

PYQS = {}

PYQS[7] = dict(
 title="ca7 — Amdahl with communication overhead; cache optimisation; MIPS CPU time; snoopy vs directory",
 transcript="""1. When parallelising an application, the ideal speed-up is by the number of
   processors. This is limited by two things: the percentage of the application that
   can be parallelised and the cost of communication. Amdahl’s Law takes into account
   the former but not the latter.
   a) What is the speed-up with eight processors if, for every processor added, the
      communication overhead is 0.5% of the original execution time. [2]
   b) What is the speed-up with N processors if, for every time the number of
      processors is doubled, the communication overhead is increased by 0.5% of the
      original execution time? [2]
2. a) With an example, explain the cache optimisation technique to reduce the miss
      rate. [2]
   b) Can you think of a way to test some of the characteristics of an instruction
      cache — using a program? Hint: the compiler may generate a large number of
      non-obvious instructions. [2]
3. a) Consider an implementation of the MIPS ISA with a 500 MHz clock and
      — each ALU instruction takes 3 clock cycles,
      — each branch/jump instruction takes 2 clock cycles,
      — each sw instruction takes 4 clock cycles,
      — each lw instruction takes 5 clock cycles. [3]
      Also consider a program that during its execution executes:
      — x = 200 million ALU instructions
      — y = 55 million branch/jump instructions
      — z = 25 million sw instructions
      — w = 20 million lw instructions
      Find the CPU time. Assume a sequentially executing CPU.
   b) What is multiprocessor cache coherence? Differentiate between snoopy-based
      protocol and directory-based protocol with neat diagrams. [3]""",
 explain=r'''
    A(h3("1a — speed-up with 8 processors, 0.5% overhead per processor"))
    A(p("Each added processor brings 0.5% communication overhead measured against the original time. "
        "With 8 processors the total overhead is 8 × 0.5% = 4% of the original time."))
    A(formula("S = n / (1 + overhead_fraction) = 8 / (1 + 0.04) = 8/1.04 ≈ 7.69×"))
    A(h3("1b — speed-up with N processors, 0.5% added per doubling"))
    A(p("Each time the number of processors doubles, the overhead grows by another 0.5%. Writing "
        "N = 2^k, the overhead is 0.5%·k, so:"))
    A(formula("S(N) = N / (1 + 0.005·k)   where N = 2^k,  k = log₂N\n"
              "  e.g. N = 8 (k = 3):  S = 8 / (1 + 0.015) ≈ 7.88×\n"
              "       N = 16 (k = 4): S = 16 / (1 + 0.02) ≈ 15.7×"))
    A(h3("2a — reducing the miss rate (example)"))
    A(p("Example technique: <b>increase associativity</b>. Switching a direct-mapped cache to 2-way "
        "set associative removes conflict misses. With numbers: if the direct-mapped miss rate is 5% and "
        "2-way brings it to 3%, and the miss penalty is 50 cycles, then "
        "AMAT falls by (0.05 − 0.03) × 50 = 1 cycle."))
    A(formula("AMAT = hit time + miss rate × miss penalty\n"
              "  ΔAMAT = Δ(miss rate) × miss penalty = (0.05 − 0.03) × 50 = 1 cycle saved"))
    A(h3("2b — testing instruction-cache characteristics with a program"))
    A(p("Write a program whose instruction footprint can be varied systematically (e.g. a loop body "
        "repeated to a chosen size, or a loop unrolled to a chosen length) and measure the runtime as the "
        "footprint grows. When the footprint crosses the instruction-cache size the runtime jumps — that "
        "jump reveals the I-cache capacity. Varying the stride/alignment reveals the block size and "
        "associativity."))
    A(h3("3a — CPU time for the MIPS program"))
    A(formula("IC = 200M + 55M + 25M + 20M = 300 million instructions\n"
              "Total cycles = 200M×3 + 55M×2 + 25M×4 + 20M×5\n"
              "             = 600M + 110M + 100M + 100M = 910 million cycles\n"
              "CPU time = 910×10⁶ / 500×10⁶ Hz = 1.82 s\n"
              "Average CPI = 910/300 ≈ 3.03"))
    A(h3("3b — multiprocessor cache coherence; snoopy vs directory"))
    A(p("<b>Cache coherence</b> is the guarantee that every processor sees the latest value of every "
        "shared block, even though each has a private cache."))
    A(table(["","Snoopy-based","Directory-based"],
      [["Mechanism","All caches watch a shared bus","A directory records the sharers of each block"],
       ["Traffic","Broadcast to all caches","Point-to-point to the sharers only"],
       ["Scales to","Few processors (bus limit)","Many processors"],
       ["Hardware","Simple; needs a broadcast bus","Directory storage + extra messages"]],
      widths=[1.1,2.3,2.6]))
''')

PYQS[8] = dict(
 title="ca8 — Branch-target-buffer penalty vs fixed penalty; write-miss stall with ownership and invalidates",
 transcript="""4. a) Suppose we have a deeply pipelined processor for which we implement a branch-target
      buffer for the conditional branches only. Assume that the misprediction penalty is
      always four cycles and the buffer-miss penalty is always three cycles. Assume a 90%
      hit rate, 90% accuracy and 18% branch frequency. How much faster is the processor
      with the branch-target buffer versus a processor that has a fixed two-cycle branch
      penalty? Assume a base CPI without branch stalls of one. [3]
   b) Suppose we have a processor where a write miss takes 50 cycles to establish
      ownership, 10 cycles to issue each invalidate after ownership is established, and
      80 cycles for an invalidate to complete and be acknowledged once it is issued.
      Assuming four other processors share a cache block, how long does a write miss
      stall the writing processor if the processor is sequentially consistent? Assume
      the invalidates must be explicitly acknowledged before the coherence controller
      knows they are completed. Suppose we could continue executing after obtaining
      ownership for the write miss without waiting for the invalidates; how long would
      the write take? [3]""",
 explain=r'''
    A(h3("4a — BTB versus a fixed 2-cycle branch penalty"))
    A(formula("BTB penalty per branch = buffer_miss_rate × miss_penalty\n"
              "                        + hit_rate × (1 − accuracy) × mispredict_penalty\n"
              "  = 0.10 × 3 + 0.90 × 0.10 × 4\n"
              "  = 0.30 + 0.36 = 0.66 cycles/branch\n\n"
              "With 18% branches:  extra CPI = 0.18 × 0.66 = 0.119\n"
              "  CPI_BTB = 1 + 0.119 = 1.119\n\n"
              "Fixed penalty:      extra CPI = 0.18 × 2 = 0.36\n"
              "  CPI_fixed = 1.36\n\n"
              "Speed-up = 1.36 / 1.119 ≈ 1.215×  (≈ 21% faster)"))
    A(h3("4b — write-miss stall with ownership + invalidates"))
    A(formula("Sequential consistency (invalidates acknowledged before proceeding):\n"
              "  stall = ownership + (issue each invalidate) + (last invalidate completes)\n"
              "  = 50 + 4×10 + 80 = 170 cycles\n\n"
              "If we may continue after ownership without waiting for invalidates:\n"
              "  write takes = 50 cycles  (the invalidations proceed in the background)"))
''')

PYQS[10] = dict(
 title="ca10 — MIPS pipeline: data dependences, optimal schedule with forwarding, CPI; C-to-MIPS reordering",
 transcript="""Date: 03.11.2025     Answer ALL Questions     Max Marks: 20
1. The following MIPS program is to be run on a MIPS pipeline processor of form
   IF-ID-EX-MEM-WB. (3)
   a. Identify all data dependencies beside each instruction, in the form:
      <type> on <register> from <line-no> to <line-no>, e.g. WAW on $16 from L8 to L10.
        L1  lw   $t2, 60($t1)
        L2  lw   $t1, 40($t2)
        L3  slt  $t1, $t1, $t2
        L4  sw   $t1, 20($t2)
   b. Work out and diagram the optimal pipeline schedule using forwarding from EX or
      MEM stages to any other stage, then compute the pipeline CPI. (3)
        L1  lw   $t2, 60($t1)
        L2  lw   $t1, 40($t2)
        L3  slt  $t1, $t1, $t2
        L4  sw   $t1, 20($t2)
2. Convert the following C code to MIPS and find the hazards and reorder the
   instructions to avoid any stalls. (4)
        A = B + E;
        C = B - E;
        B = C + E;""",
 explain=r'''
    A(h3("1a — data dependences"))
    A(table(["Instruction","Dependence","Type and lines"],
      [["L2 lw $t1,40($t2)","reads $t2 written by L1","RAW on $t2 from L1 to L2"],
       ["L3 slt $t1,$t1,$t2","reads $t1 from L2 and $t2 from L1","RAW on $t1 L2→L3; RAW on $t2 L1→L3"],
       ["L3 slt $t1,…","writes $t1 also written by L2","WAW on $t1 from L2 to L3"],
       ["L4 sw $t1,20($t2)","reads $t1 from L3, $t2 from L1","RAW on $t1 L3→L4; RAW on $t2 L1→L4"]],
      widths=[1.5,2.0,2.5]))
    A(h3("1b — optimal schedule with forwarding and CPI"))
    A(formula("With forwarding EX/MEM→EX, an ALU result costs 0 stalls; a load-use\n"
              "pair costs 1 stall.\n\n"
              "Cycles:  1   2   3   4   5   6   7   8\n"
              "L1 lw    IF  ID  EX  MEM WB\n"
              "L2 lw        IF  ID  *   EX  MEM WB      (* = load-use stall: L2 uses $t2 from L1)\n"
              "L3 slt           IF  ID  EX  MEM WB      (reads $t1 from L2 → 1 stall, filled)\n"
              "L4 sw                IF  *   ID  EX  MEM WB\n\n"
              "Total = 4 instructions + 2 stall cycles; CPI = (4 + 2)/4 = 1.5"))
    A(h3("2 — C to MIPS, hazards, reorder"))
    A(formula("Assume B=$s1, E=$s2, A=$s0, C=$s3, and a temp $t0.\n"
              "  lw   $s1, B        ; B\n"
              "  lw   $s2, E        ; E\n"
              "  add  $s0, $s1, $s2 ; A = B + E\n"
              "  sub  $s3, $s1, $s2 ; C = B − E\n"
              "  add  $s1, $s3, $s2 ; B = C + E  (RAW on $s3 from the sub)\n\n"
              "Reordered to hide the load-use and ALU latencies:\n"
              "  lw   $s1, B\n"
              "  lw   $s2, E\n"
              "  sub  $s3, $s1, $s2 ; independent of the loads’ consumers ordering\n"
              "  add  $s0, $s1, $s2\n"
              "  add  $s1, $s3, $s2 ; last use of $s3, no stall"))
''')

PYQS[13] = dict(
 title="ca13 — Four RISC fragments (dependences, forwarding/stalls); 5-stage latencies; MIPS schedule and CPI",
 transcript="""1. Consider the following four RISC machine-code fragments, each with two instructions:
     i.   addi r1, r1, #4    ; load  r2, 7(r1)
     ii.  add  r3, r1, r2    ; store r2, 7(r1)
     iii. beq  r1, place     ; store r1, 7(r1)
     iv.  store r3, 17(r10)  ; load  r2, 12(r8)
   i.  For each fragment identify each dependence that exists or may exist. [1]
   ii. For each fragment, indicate whether data forwarding is sufficient or stall cycles
       are required; give the number of stall cycles. [1]
   b) The 5 stages of the processor have the following latencies:
        IF    ID    EX    MEM   WB
        300ps 400ps 350ps 550ps 100ps
   What is the cycle time? What is the latency of an instruction? What is the throughput?
   For a non-pipelined processor and a pipelined processor. [3]
2. The following MIPS program runs on a pipeline IF-ID-EX-MEM-WB:
        L1 lw  $t2, 60($t1)
        L2 lw  $t1, 40($t2)
        L3 slt $t1, $t1, $t2
        L4 sw  $t1, 20($t2)
   a) Identify all data dependencies as <type> on <register> from L_x to L_y. [3]
   b) Work out and diagram the optimal pipeline schedule with forwarding, then compute CPI. [2]""",
 explain=r'''
    A(h3("1a — dependences in the four fragments"))
    A(table(["Fragment","Dependence","Forwarding enough?"],
      [["i. addi r1→load r2,7(r1)","RAW on r1 (address)","Yes — 0 stalls"],
       ["ii. add r3→store r2,7(r1)","WAW on r2 (both touch r2)","Yes — 0 stalls"],
       ["iii. beq r1→store r1","control only; no register RAW","Yes — 0 stalls"],
       ["iv. store r3→load r2","possible memory dependence (may exist)","Yes — 0 stalls"]],
      widths=[2.1,1.9,1.6]))
    A(h3("1b — cycle time, latency, throughput"))
    A(formula("Non-pipelined: cycle time = sum of stages = 300+400+350+550+100 = 1700 ps\n"
              "  latency = 1700 ps ;  throughput = 1/1700 ps\n\n"
              "Pipelined: cycle time = slowest stage + register overhead\n"
              "  = 550 ps + (register delay, say r) ≈ 550 ps (ignoring r)\n"
              "  latency = 5 × 550 = 2750 ps (one instruction still traverses 5 stages)\n"
              "  throughput = 1 instruction / 550 ps"))
    A(h3("2a — dependences (same program as ca10)"))
    A(formula("RAW on $t2 from L1→L2 ;  RAW on $t1 L2→L3 ;  RAW on $t2 L1→L3 ;\n"
              "WAW on $t1 L2→L3 ;  RAW on $t1 L3→L4 ;  RAW on $t2 L1→L4"))
    A(h3("2b — optimal schedule and CPI"))
    A(formula("Same schedule as ca10: 2 load-use stalls over 4 instructions\n"
              "  CPI = (4 + 2)/4 = 1.5"))
''')

PYQS[14] = dict(
 title="ca14 — Hazards and reordering; register renaming with P-registers; RAW hazards",
 transcript="""a. Find the hazards in the code below and reorder the instructions to avoid any
   stalls. [5]
        lw   $t1, 0($t0)
        lw   $t2, 4($t0)
        add  $t3, $t1, $t2
        sw   $t3, 12($t0)
        lw   $t4, 8($t0)
        add  $t5, $t1, $t4
        sw   $t5, 16($t0)
b. Consider the following code. Assume an architecture with a unified register file
   that both floating-point and integer ISA registers map to. [5]
        loop: (1) faddi f1, f5, 5
              (2) sub   x6, x5, x4
              (3) flw   f1, 0(x6)
              (4) fmul  f3, f1, f4
              (5) fmul  f9, f9, f8
              (6) fadd  f1, f2, f3
              (7) fcvt  x6, f3
              (8) fsw   f4, 0(x6)
              (9) bne   x7, x0, loop
              (10) faddi f4, f4, 8
              (11) faddi f6, f6, 8
   a) How many RAW hazards are there? Write them as (I → J) where J reads what I writes.
   b) Show register renaming to minimise stalls (P1, P2, …). What hazards does renaming help?""",
 explain=r'''
    A(h3("a — hazards and reordering"))
    A(formula("RAW on $t1: lw→add($t3) and lw→add($t5)\n"
              "RAW on $t2: lw→add($t3)\n"
              "RAW on $t3: add→sw\n"
              "RAW on $t4: lw→add($t5)\n"
              "RAW on $t5: add→sw\n\n"
              "Reordered (independent loads hoisted to cover load-use latency):\n"
              "  lw  $t1, 0($t0)\n"
              "  lw  $t2, 4($t0)\n"
              "  lw  $t4, 8($t0)\n"
              "  add $t3, $t1, $t2\n"
              "  add $t5, $t1, $t4\n"
              "  sw  $t3, 12($t0)\n"
              "  sw  $t5, 16($t0)"))
    A(h3("b — RAW hazards in the loop"))
    A(formula("(1) faddi f1 → (3) flw f1? (3 writes f1, so WAW/WAR; (1)→(4) f1 used? \n"
              "(4) reads f1 written by (3) : (3 → 4)\n"
              "(3) flw f1 → (6) fadd reads f3 written by (4): (4 → 6)\n"
              "(2) sub x6 → (3) flw uses x6 as base: (2 → 3)\n"
              "(4) fmul f3 → (6) fadd and (7) fcvt x6: (4 → 6), (4 → 7)\n"
              "Count the true (RAW) pairs as listed."))
    A(p("Renaming gives each new value a fresh physical register (P1, P2, …), removing WAW and WAR "
        "(name) dependences — e.g. the f1 written by (1) and the f1 loaded by (3) get different physical "
        "registers, so (4) no longer waits for (1). RAW dependences remain."))
''')

PYQS[15] = dict(
 title="ca15 — AMAT with a second-level cache; multicore CPI to beat a single core",
 transcript="""1a. The average memory access time for a microprocessor with one level of cache is
    2.4 clock cycles. If data is present and valid it is found in 1 clock cycle. If it is
    not found, 80 clock cycles are needed from off-chip memory. Designers want a 65%
    improvement in AMAT and are considering a second-level cache on-chip that is
    accessed in 6 clock cycles (the addition does not affect the L1 access pattern or
    hit time; off-chip accesses still require 80 extra cycles). To obtain the desired
    speed-up, how often must data be found in the second-level cache? (5)
  b. The base CPI for a pipelined single-core system is 1 (excluding cache misses).
    For every 10,000,000 accesses there are 308,752 L1 misses; a hit costs 1 cycle, a
    miss 10 cycles. Now consider a multi-core chip with equivalent L1 caches, shared
    centralised memory, snooping MSI coherence, where misses rise to 452,977 per
    10,000,000 accesses and a miss now costs 14 cycles. What must the CPI of the
    multi-core system be for it to be worthwhile to abandon the single core? (5)""",
 explain=r'''
    A(h3("1a — required second-level hit rate"))
    A(formula("Single level:  AMAT = 2.4 cycles\n"
              "  AMAT = hit_time + miss_rate × miss_penalty\n"
              "  2.4 = 1 + m_L1 × 80  →  m_L1 = 1.4/80 = 0.0175  (L1 miss rate)\n\n"
              "Target AMAT = 2.4 × (1 − 0.65) = 0.84 cycles  (a 65% improvement)\n"
              "With L2:  AMAT = 1 + m_L1 × (6 + m_L2 × 80)\n"
              "  0.84 = 1 + 0.0175 × (6 + m_L2 × 80)  →  0.0175×(6 + 80·m_L2) = −0.16"))
    A(callout("<b>Note the impossibility.</b> The target of 0.84 cycles is <i>below</i> the 1-cycle L1 "
        "hit time, so no second-level cache can reach it — the required L2 hit rate would have to exceed "
        "100%. The correct exam answer is to show this: the goal is unachievable because the L1 hit time "
        "already exceeds the target AMAT.", 'tip'))
    A(h3("1b — required multicore CPI"))
    A(formula("Single core:  L1 miss rate = 308752 / 10⁷ = 0.0308752\n"
              "  CPI = 1 + 0.0308752 × 10 = 1 + 0.308752 ≈ 1.309\n\n"
              "Multicore:    miss rate = 452977 / 10⁷ = 0.0452977\n"
              "  CPI_multi = 1 + 0.0452977 × 14 = 1 + 0.634 ≈ 1.634\n\n"
              "The multicore is worthwhile only if its CPI is BELOW the single-core CPI\n"
              "  (≈ 1.309) once its extra parallelism is counted; on raw memory CPI the\n"
              "  multicore is worse (1.634 > 1.309), so the extra cores must more than\n"
              "  make up the difference."))
''')

PYQS[18] = dict(
 title="ca18 — Tomasulo on a loop with multiply latency and cache misses",
 transcript="""3. Implement the following code using Tomasulo’s algorithm. Assume multiply takes
   4 clocks and loads may have cache misses. Use the format given below: (10)
        LD   F0, 0(R1)      ; iteration 1
        MULT F4, F0, F2
        SD   F4, 0(R1)
        LD   F0, 0(R1)      ; iteration 2
        MULT F4, F0, F2
        SD   F4, 0(R1)
   Instruction status:  Instruction | j | k | iteration | Issue | Execute complete | Write result
   Reservation stations: Name | Busy | Op | Vj | Vk | Qj | Qk | A
   Register result status: Clock | R1 | F0 | F2 | F4 | F6 …""",
 explain=r'''
    A(h3("Filling the tables"))
    A(formula("Iteration 1:\n"
              "  LD   F0,0(R1)  → Load1 (address = 0+R1)\n"
              "  MULT F4,F0,F2  → Mult1 (Qj = Load1, Vk = F2)\n"
              "  SD   F4,0(R1)  → Store1 (Qk = Mult1, address 0+R1)\n"
              "Iteration 2 (independent of iteration 1 except for R1):\n"
              "  LD   F0,0(R1)  → Load2\n"
              "  MULT F4,F0,F2  → Mult2 (Qj = Load2, Vk = F2)\n"
              "  SD   F4,0(R1)  → Store2 (Qk = Mult2)"))
    A(bullets([
        "Multiply latency = 4 cycles; a load’s completion is delayed if it misses in the cache.",
        "The two iterations use the <b>same register names</b> (F0, F4), so renaming via the reservation "
        "stations is what lets them overlap: Load2 writes F0 while Load1’s value is still needed by "
        "Mult1.",
        "Record Issue, Execute-complete and Write-result for each instruction; the register-result-status "
        "table shows which station will produce F0 and F4 at each cycle.",
    ]))
''')

PYQS[20] = dict(
 title="ca20 — Resource and control hazards in a MIPS fragment (two memories)",
 transcript="""2a. In this exercise we examine how resource hazards, control hazards and ISA design
    affect pipelined execution. Refer to the following fragment of MIPS code: (5)
        lw   $1, 40($6)
        beq  $2, $0, Label        ; assume $2 = $0 (branch taken)
        sw   $6, 50($2)
    Label: add  $2, $3, $4
        sw   $3, 50($4)
        lw   $5, -16($5)
        sw   $4, -16($4)
        lw   $3, -20($4)
        beq  $2, $0, Label        ; assume $2 != $0 (not taken)
        add  $5, $1, $4""",
 explain=r'''
    A(h3("Hazards in the fragment"))
    A(table(["Hazard","Where","Explanation"],
      [["Control","beq $2,$0,Label","Branch resolves late; instructions fetched behind it must be flushed if taken"],
       ["Data (RAW)","lw $5,-16($5)","the load’s base and destination are the same register → load-use handling"],
       ["Data (RAW)","lw $3,-20($4) then uses","load-use stall"],
       ["Resource","lw/sw vs fetch","only if a single memory is used"]],
      widths=[1.2,1.7,3.1]))
    A(formula("With TWO memories (separate instruction and data memories) the\n"
              "  IF-vs-MEM resource hazard does NOT occur; only control and data hazards remain.\n"
              "Branch penalty: with the first branch taken, the instructions fetched behind\n"
              "  it are flushed; with the second not taken, no flush."))
    A(p("The point of the question is that splitting the memory removes the structural hazard, while the "
        "branch (control hazard) and the load-use pairs (data hazards) are unaffected by the ISA choice "
        "except through the pipeline depth."))
''')

PYQS[21] = dict(
 title="ca21 — Single-memory structural hazard; pipeline mix; dynamic scheduling with Tomasulo",
 transcript="""Assume all branches are perfectly predicted (no control hazards). Assume there is one
memory (for both instructions and data), so there is a structural hazard every time we
need to fetch an instruction in the same cycle in which another instruction accesses
data. What is the total execution time of this instruction sequence in the five-stage
pipeline that has only one memory? We have seen that data hazards can be eliminated by
adding nops to the code — can you do the same with this structural hazard? Why?
Also: instructions executed by a pipelined processor are broken down as (ALU 40%,
Load 20%, Store 10%, Branch 30% …). (a) Assuming no stalls and 60% of conditional
branches taken, in what percentage of cycles does the branch adder in EX generate a
value that is actually used? (b) How often do we use the data memory?
(c) How to handle hazards in dynamic scheduling? Explain with an example.""",
 explain=r'''
    A(h3("Single-memory structural hazard"))
    A(formula("With one memory, a load/store in MEM and a fetch in IF conflict → the\n"
              "  fetch stalls one cycle whenever an instruction accesses data.\n"
              "  Total time = (number of instructions) + (pipeline fill) + (data-access stalls)."))
    A(p("<b>Can nops fix it?</b> No. Nops remove <i>data</i> hazards by giving the producer time, but "
        "the structural hazard is a <i>resource</i> conflict: the two instructions genuinely want the "
        "same memory in the same cycle. Adding nops would add more fetches, not fewer. The real fixes are "
        "separate instruction and data memories (Harvard style) or a memory that supports two accesses "
        "per cycle."))
    A(h3("Resource-utilisation percentages"))
    A(formula("(a) Branch adder used only when a branch is taken and in EX:\n"
              "      branch fraction × taken fraction = 0.30 × 0.60 = 18% of cycles\n"
              "    (if measured over all instructions, ≈ 0.30 × 0.60 × 1 cycle).\n"
              "(b) Data memory used by loads and stores in MEM:\n"
              "      load 20% + store 10% = 30% of cycles"))
    A(h3("Dynamic scheduling (Tomasulo)"))
    A(p("Handle hazards with reservation stations: issue an instruction into a free station (filling Qj/Qk "
        "with producer tags), execute when both operands are ready, and broadcast the result on the CDB. "
        "This removes WAR/WAW hazards by renaming and lets RAW-dependent instructions wait without "
        "blocking independent ones."))
''')
