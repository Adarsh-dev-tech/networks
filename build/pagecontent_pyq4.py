"""Faithful transcriptions for the remaining scans (ca16, ca17, ca19, ca22, ca28, ca32)."""

PYQS = {}

PYQS[16] = dict(
 title="ca16 — For each sequence: must stall / forwarding / no stall",
 transcript="""2. For the code sequence below, state whether it must stall, can avoid stalls using
   only forwarding, or can execute without stalling or forwarding. (1)
   i.   lw   $t0, 0($t0)
        add  $t1, $t0, $t0
        addi $t3, $t0, 2
   ii.  add  $t1, $t0, $t0
        addi $t2, $t0, 5
        addi $t4, $t1, 5
   iii. addi $t1, $t0, 1
        addi $t2, $t0, 2
        addi $t3, $t0, 4
        addi $t5, $t0, 5""",
 explain=r'''
    A(h3("Classifying each sequence"))
    A(table(["Sequence","Verdict","Reason"],
      [["i. lw → add (use of $t0)","Must stall (1 cycle)","load-use: data ready only after MEM"],
       ["ii. add → addi (use of $t1)","Forwarding is enough (0 stalls)","ALU result forwarded EX/MEM→EX"],
       ["iii. independent addis","No stall, no forwarding needed","no dependences at all"]],
      widths=[1.9,1.6,2.3]))
    A(formula("Rules:\n"
              "  load → use         : 1 stall even with forwarding\n"
              "  ALU  → use         : 0 stalls with forwarding\n"
              "  independent        : 0 stalls, no forwarding needed"))
''')

PYQS[17] = dict(
 title="ca17 — Pipeline instruction mix: branch-adder use, data-memory use, speed-up",
 transcript="""b. Instructions executed by a pipelined processor are broken down as follows
   (ALU / Load / Store / Branch percentages given).
   i.  Assuming there are no stalls and that 60% of all conditional branches are taken,
       in what percentage of clock cycles does the branch adder in the EX stage generate
       a value that is actually used?
   ii. Assuming there are no stalls, how often (percentage of all cycles) do we use the
       data memory?
   iii. Each pipeline stage has some latency; pipelining introduces registers between
        stages, each adding latency. Assuming no stalls, what is the speed-up achieved by
        pipelining a single-cycle datapath?""",
 explain=r'''
    A(h3("i — branch adder utilisation"))
    A(formula("Branch adder produces a value only when a branch is taken (in EX):\n"
              "  utilisation = branch_fraction × taken_fraction × (cycles in EX)\n"
              "  = 0.30 × 0.60 × 1 = 0.18 = 18% of cycles."))
    A(h3("ii — data-memory utilisation"))
    A(formula("Data memory is used by loads and stores in MEM:\n"
              "  utilisation = (load_fraction + store_fraction) × 1 = 0.20 + 0.10 = 30%."))
    A(h3("iii — pipelining speed-up"))
    A(formula("S = (n · k) / (n + k − 1)  →  k  as n → ∞\n"
              "With register overhead, the clock period grows, so the realised speed-up\n"
              "  is slightly below k."))
''')

PYQS[19] = dict(
 title="ca19 — Performance (MIPS, CPU time) + pipelining speed-up (repeat of ca1 Q1)",
 transcript="""Q1. This scan repeats question 1 of ca1: compute the MIPS and the CPU time for the
    two machines (one with hardware FP, one emulating FP in software), and give the
    pipelining speed-up as a function of N.""",
 explain=r'''
    A(p("The solution is identical to ca1 Q1 (see the ca1 solution on the page where this guide "
        "covers performance). Because the question is a repeat, it is recorded here rather than "
        "duplicated in full:"))
    A(formula("CPI = Σ (share × CPI) ;  MIPS = f / (CPI × 10⁶)\n"
              "CPU time = IC × CPI / f\n"
              "Pipelining speed-up S(N) = N·A / (N + A − 1)"))
''')

PYQS[22] = dict(
 title="ca22 — Loop dependences and renaming (repeat of ca1 Q2a)",
 transcript="""Q. This scan repeats ca1 Q2a: find the true, output and anti-dependences in the loop
   and eliminate the false ones by renaming.""",
 explain=r'''
    A(p("The solution is identical to ca1 Q2a (see the ca1 solution on the performance page of this "
        "guide). Recorded here as a repeat rather than duplicated in full:"))
    A(formula("S1: A[i] = A[i]*B[i]\n"
              "S2: B[i] = A[i] + c\n"
              "S3: A[i] = C[i]*c\n"
              "S4: C[i] = D[i]*A[i]\n"
              "RAW: S1→S2, S3→S4 ;  WAW: S1→S3 ;  WAR: S2→S3\n"
              "Rename: A1 = A[i]*B[i]; B[i]=A1+c; A2=C[i]*c; C[i]=D[i]*A2;"))
''')

PYQS[28] = dict(
 title="ca28 — Static vs dynamic scheduling; control-hazard techniques; Tomasulo with speculation",
 transcript="""4. a. Distinguish between static scheduling and dynamic scheduling.
   b. Name three major techniques that can reduce control-hazard stalls. Explain.
   c. How is Tomasulo’s algorithm modified to include speculation? What additional
      hardware is required?""",
 explain=r'''
    A(h3("a — static vs dynamic scheduling"))
    A(table(["","Static","Dynamic"],
      [["When","Compile time","Run time"],
       ["Sees","Program text only","Actual conditions (cache misses)"],
       ["Examples","Unrolling, software pipelining","Scoreboard, Tomasulo, speculation"]],
      widths=[0.9,2.3,2.3]))
    A(h3("b — three control-hazard techniques"))
    A(bullets([
        "<b>1) Branch prediction</b> — guess the direction and fetch down the predicted path.",
        "<b>2) Delayed branch</b> — the compiler fills the branch-delay slot with a useful instruction.",
        "<b>3) Flush on misprediction</b> — squash the wrong-path instructions when the branch resolves.",
    ]))
    A(h3("c — Tomasulo with speculation"))
    A(p("Add a <b>reorder buffer</b> so results are held in program order and committed in order. Extra "
        "hardware: the ROB itself, a mechanism to assign ROB entries at issue, and the commit logic that "
        "writes the architectural state in order and discards speculative entries on a misprediction."))
''')

PYQS[32] = dict(
 title="ca32 — Four predictors; 5-stage vs 10-stage clock; speculation; cache optimisation; branch overhead",
 transcript="""1. What are the 4 different types of predictors? Elaborate on their performance in
   terms of average misprediction rate. (4)
2. In the 5-stage pipeline the longest stage requires 0.8 ns and the pipeline register
   delay is 0.1 ns. What is the clock cycle time of the 5-stage pipeline? If the 10-stage
   pipeline splits all stages in half, what is the cycle time of the 10-stage machine? (2)
3. What do you understand by hardware-based speculation? (2)
4. Discuss the cache-memory optimisation techniques with a view to reducing the access time.
5. Five-stage pipeline; all ops one cycle except LW/SW (1+2) and branches (1+1); no
   forwarding. Show the phases per clock for one loop iteration; how many cycles are lost
   to branch overhead? (5)""",
 explain=r'''
    A(h3("1 — four predictors"))
    A(table(["Predictor","Mispredicts when","Approx. rate"],
      [["Static (taken/not)","Pattern changes","worst"],
       ["1-bit","Direction changes","high"],
       ["2-bit saturating","Two changes in a row","moderate"],
       ["Correlating (2-level)","Unseen history pattern","lowest"]],
      widths=[1.4,2.3,1.3]))
    A(h3("2 — clock cycle time"))
    A(formula("5-stage: cycle time = longest stage + register delay = 0.8 + 0.1 = 0.9 ns\n"
              "10-stage (stages halved): longest stage = 0.4 ns, register delay = 0.1 ns\n"
              "  → cycle time = 0.4 + 0.1 = 0.5 ns"))
    A(h3("3 — hardware-based speculation"))
    A(p("The hardware executes instructions before it is certain they should execute (e.g. past a "
        "predicted branch), keeping the results in a reorder buffer and committing them in order; "
        "a wrong guess is squashed."))
    A(h3("4 — cache optimisation to reduce access time"))
    A(formula("AMAT = hit time + miss rate × miss penalty\n"
              "  reduce hit time: smaller/faster cache, simpler addressing, avoid TLB delay."))
    A(h3("5 — phases and branch overhead"))
    A(formula("No forwarding → 2 stalls per RAW pair; the branch resolves late so the\n"
              "  instructions fetched behind it are flushed (branch overhead ≈ 2 cycles)."))
''')
