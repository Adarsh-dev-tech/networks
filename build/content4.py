"""Part IV — ILP, branch prediction, dynamic scheduling and speculation."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

def build():
    F=[]
    def A(x): F.extend(x if isinstance(x,list) else [x])

    # ============ 6. ILP / LOOP UNROLLING / STATIC SCHEDULING ============
    A(PageBreak())
    A(h1(6,"Exploiting ILP: Loop Unrolling & Scheduling","Turning dependences into parallel work"))
    A(p("Dependences limit parallelism. Two ways to get past them: <b>rename</b> away the false ones "
        "(Topics 3, 8) and <b>replicate</b> the loop body so more independent work is visible at once. "
        "This second idea is <b>loop unrolling</b>, and it is one of the most examined topics."))

    A(h3("6.1 Why unroll?"))
    A(bullets([
      "Overlapping loop iterations exposes ILP that the loop control hides.",
      "It removes the loop-overhead instructions (branch + counter increment) — fewer instructions overall.",
      "It lets the scheduler move independent instructions into the slots where a dependent one would stall.",
    ]))
    A(callout("<b>Cost of unrolling:</b> more registers needed (each unrolled copy may want fresh names), "
              "bigger code (more I-cache pressure), and the tail iteration must be handled separately if the "
              "trip count is not a multiple of the unroll factor."))

    A(h3("6.2 The DAXPY loop — the classic example"))
    A(p("DAXPY computes Y = a·X + Y for vectors. It is the heart of Gaussian elimination. The MIPS code:"))
    A(formula("      DADDIU R4, R1, 1600   ; R4 = address of X[100] (end)\n"
              "Loop: L.D    F2, 0(R1)      ; F2 = X[i]\n"
              "      MUL.D  F4, F2, F0     ; F4 = a * X[i]\n"
              "      L.D    F6, 0(R2)      ; F6 = Y[i]\n"
              "      ADD.D  F6, F4, F6     ; F6 = a*X[i] + Y[i]\n"
              "      S.D    F6, 0(R2)      ; Y[i] = result\n"
              "      DADDIU R1, R1, #8     ; advance X index\n"
              "      DADDIU R2, R2, #8     ; advance Y index\n"
              "      DSGTUI R3, R1, R4     ; R3 = (R1 > end)?\n"
              "      BEQZ   R3, Loop       ; if not, repeat"))
    A(p("Each iteration uses F2, F4, F6. If we unroll, each copy must use <i>different</i> registers "
        "(F2/F4/F6, then F8/F10/F12, …) so the copies are independent — this is renaming by the compiler."))

    A(h3("6.3 Latency, stalls and scheduling"))
    A(fig("page051.jpg", w=10.5*gen.cm, cap="Loop unrolled and scheduled with no stalls (source: p. 51)."))
    A(p("<b>Reading the figure.</b> The DAXPY loop after unrolling and scheduling. The independent iterations are interleaved so that no stall slot is left empty — this is the goal of software scheduling."))
    A(p("Every functional unit has a <b>latency</b> — the number of cycles before its result is ready. If the "
        "next instruction needs that result too soon, the pipeline stalls. Scheduling means moving independent "
        "instructions into the stall slots."))
    A(table(["Producer → consumer","Typical latency (cycles)","Stall if not scheduled"],
      [["FP multiply → FP ALU op","5","4"],
       ["FP add → FP ALU op","3","2"],
       ["FP add → FP store","3","2"],
       ["Integer op → any","0-1","0-1"],
       ["Load → use","1-2","1-2"]],
      widths=[2.0,2.0,2.0]))
    A(p("A single-issue pipeline with <i>no</i> forwarding can hide these only by scheduling independent "
        "instructions between producer and consumer. Unrolling gives us enough independent instructions to "
        "fill every slot. We keep unrolling until there are enough independent instructions to cover the "
        "longest latency — then every cycle issues something useful."))
    A(formula("Execution time per element = (total cycles) / (number of elements computed)\n"
              "Speed-up from unrolling ≈ (un-optimised cycles) / (optimised cycles)"))
    A(h3("6.4 Static vs dynamic scheduling"))
    A(table(["","Static scheduling","Dynamic scheduling"],
      [["Who decides the order?","The compiler (at compile time)","The hardware (at run time)"],
       ["When?","Before execution; fixed order","During execution; may reorder"],
       ["Strength","No extra hardware; predictable","Handles dependences the compiler cannot see (e.g. cache misses); adapts to actual latencies"],
       ["Weakness","Cannot know run-time events (misses, latency variation)","Extra hardware: reservation stations, issue logic"],
       ["Examples","Loop unrolling, software pipelining, VLIW","Scoreboarding, Tomasulo's algorithm, out-of-order cores"]],
      widths=[1.5,2.2,2.3]))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Loop unrolling & scheduling"))
    A(Paragraph("Q (ca11 · Q3). Convert the loop below to a DAXPY implementation, unroll it three times, use "
                "different registers in each version, and eliminate redundant computations. Assume: integer "
                "ops 1 cycle; no memory delays; no branch delay; FP add 2, FP mul 5, FP div 19 cycles.", ST['q']))
    A(formula("for i := 1 to 100\n    Y[i] = a * X[i] + Y[i];"))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "The three unrolled bodies compute Y[i], Y[i+1], Y[i+2]. Use F0 = a (loop-invariant, loaded once).",
      "Register sets per copy: copy 1 → F2,F4,F6; copy 2 → F8,F10,F12; copy 3 → F14,F16,F18.",
      "Use displacement addressing (0(R1), 8(R1), 16(R1)) instead of incrementing R1 three times — this "
      "removes two redundant DADDIU per group.",
    ]))
    A(formula("Loop:  L.D   F2, 0(R1)      ; X[i]\n"
              "       L.D   F8, 8(R1)      ; X[i+1]\n"
              "       L.D   F14,16(R1)     ; X[i+2]\n"
              "       MUL.D F4, F2, F0     ; a*X[i]\n"
              "       MUL.D F10,F8, F0     ; a*X[i+1]\n"
              "       MUL.D F16,F14,F0     ; a*X[i+2]\n"
              "       L.D   F6, 0(R2)      ; Y[i]\n"
              "       L.D   F12,8(R2)      ; Y[i+1]\n"
              "       L.D   F18,16(R2)     ; Y[i+2]\n"
              "       ADD.D F6, F4, F6\n"
              "       ADD.D F12,F10,F12\n"
              "       ADD.D F18,F16,F18\n"
              "       S.D   F6, 0(R2)\n"
              "       S.D   F12,8(R2)\n"
              "       S.D   F18,16(R2)\n"
              "       DADDIU R1,R1,#24\n"
              "       DADDIU R2,R2,#24\n"
              "       DSGTUI R3,R1,R4\n"
              "       BEQZ  R3, Loop"))
    A(p("Only <b>two</b> index-increments and <b>one</b> branch per three elements remain, versus three of "
        "each before — that is the redundant computation eliminated. The three MUL/ADD chains are mutually "
        "independent, so the 5-cycle multiply latency and 2-cycle add latency can overlap across the three "
        "copies."))

    A(Paragraph("Q (ca24 · Q1). The DAXPY loop (Y = aX + Y, length 100) is given with a one-cycle delayed "
                "branch resolved in ID, full bypassing, and the latencies in the table (FP mul→ALU 5, FP "
                "add→ALU 3, FP add→store 3, integer 1). Single-issue. Unroll as many times as necessary to "
                "schedule it without any stalls, collapsing loop overhead. How many times must it be unrolled? "
                "Show the schedule. What is the execution time per element?", ST['q']))
    A(formula("      DADDIU R4,R1,#1600\n"
              "Loop: L.D    F2,0(R1)\n      MUL.D  F4,F2,F0\n      L.D    F6,0(R2)\n"
              "      ADD.D  F6,F4,F6\n      S.D    F6,0(R2)\n      DADDIU R1,R1,#8\n"
              "      DADDIU R2,R2,#8\n      DSGTUI R3,R1,R4\n      BEQZ   R3,Loop"))
    A(Paragraph("<b>Solution.</b> The longest dependence chain per element is load → multiply(5) → add(3) → "
                "store, i.e. about 5+3 = 8 cycles of latency that must be covered by other work. Unrolling "
                "so that several independent elements are in flight lets us hide this. With the loop overhead "
                "collapsed, unroll the body so that the independent elements fill the latency slots — "
                "the standard answer for these latencies is to unroll until at least 4 independent chains "
                "are available.", ST['ans']))
    A(p("<b>Schedule (unrolled ×4, one column per issue cycle; '-' = another element's slot):</b>"))
    A(table(["Cycle","Instruction","Why it is safe now"],
      [["1","L.D F2,0(R1)","first load of element k"],
       ["2","L.D F8,8(R1)","load of k+1 (independent)"],
       ["3","MUL.D F4,F2,F0","uses F2 (5 cycles available)"],
       ["4","L.D F10,16(R1)","load of k+2"],
       ["5","MUL.D F12,F8,F0","independent of F4"],
       ["6","L.D F6,0(R2)","Y[k] load"],
       ["7","ADD.D F6,F4,F6","F4 ready after 5 → no stall"],
       ["8","MUL.D F16,F14,F0","independent"],
       ["9","S.D F6,0(R2)","store, add→store latency covered"],
       ["10","ADD.D F12,F10,F12","F10 ready"],
       ["11","S.D F12,8(R2)",""],
       ["12","ADD.D F18,F16,F18",""],
       ["13","S.D F18,16(R2)",""],
       ["14","DADDIU R1,R1,#32","one increment for 4 elements"],
       ["15","DADDIU R2,R2,#32",""],
       ["16","DSGTUI R3,R1,R4",""],
       ["17","BEQZ R3,Loop","delayed branch slot filled"]],
      widths=[0.7,2.4,3.1]))
    A(p("<b>How many times unrolled?</b> Enough independent chains to cover the 8-cycle FP latency. Because "
        "the branch is delayed and resolves in ID, the loop overhead is essentially free, so the answer is "
        "the smallest unroll factor that keeps every issue slot busy — <b>4 times</b> for these latencies. "
        "<b>Execution time per element ≈ 17 cycles / 4 elements ≈ 4.25 cycles/element</b> (about 4 cycles per "
        "element, versus ~10+ unoptimised)."))

    # ============ 7. BRANCH PREDICTION ============
    A(PageBreak())
    A(h1(7,"Branch Prediction & Control Hazards","Guessing the future to keep the pipeline full"))
    A(p("Branches are the biggest source of stalls, because until a branch resolves you do not know which "
        "instruction to fetch. Rather than always wait, the processor <b>predicts</b> the outcome and "
        "speculatively fetches down the guessed path. If the guess is right, no time is lost; if wrong, the "
        "speculative instructions are flushed and the correct path is fetched — paying a <b>misprediction "
        "penalty</b>."))

    A(h3("7.1 Static vs dynamic prediction"))
    A(table(["","Static prediction","Dynamic prediction"],
      [["When decided","At compile time / fixed rule","At run time, from history"],
       ["Uses","The branch's direction or position in code","A table of past outcomes (hardware)"],
       ["Adapts?","No","Yes — improves as the program runs"],
       ["Examples","Always-taken, always-not-taken, BTFNT, delayed branch","1-bit, 2-bit saturating, correlating, tournament"]],
      widths=[1.2,2.4,2.4]))
    A(h4("The four classic predictors (exam favourite)"))
    A(table(["Predictor","How it works","Typical misprediction rate"],
      [["Always taken","Predict every branch taken.","≈ 30-40% (bad for loops that exit often)"],
       ["Always not taken","Predict every branch not taken.","≈ 30-40%"],
       ["Backward-Taken, Forward-Not-Taken (BTFNT)","Backward branches (loops) are taken; forward branches (if) not.","≈ 20-25%"],
       ["2-bit saturating counter","A small counter per branch; needs two wrong guesses in a row to flip.","≈ 10-15%"],
       ["Correlating (2-level)","Uses the outcome of recent branches to predict the next.","≈ 5-10%"],
       ["Tournament / hybrid","Combines two predictors with a chooser.","≈ 3-5%"]],
      widths=[1.5,2.8,1.7]))
    A(h3("7.2 The 2-bit saturating counter (state machine)"))
    A(fig("page039.jpg", w=10.0*gen.cm, cap="One-bit predictor state machine (source: p. 39)."))
    A(p("<b>Reading the figure.</b> The branch-predictor state machine. A saturating counter moves toward “taken” on a taken outcome and toward “not taken” otherwise; two consecutive wrong predictions are needed to flip a 2-bit predictor."))
    A(p("Each branch has a 2-bit state. It only changes its prediction after <b>two</b> consecutive opposite "
        "outcomes, which filters out one-off anomalies. The four states:"))
    A(formula("11 = Strongly Taken      10 = Weakly Taken\n"
              "01 = Weakly Not Taken    00 = Strongly Not Taken\n"
              "Predict Taken from {11,10};  Predict Not Taken from {01,00}."))
    A(fig("page037.jpg", w=11.0*gen.cm, cap="One-bit and two-bit branch predictors (source: lecture notes, p. 37)."))
    A(p("<b>Reading the figure.</b> The predictor table. Each branch has its own counter, updated after every execution, so the predictor learns the behaviour of individual branches."))
    A(p("Why 2 bits beat 1 bit: a loop that is taken 9 times then exits once would mispredict <i>twice</i> "
        "per exit with a 1-bit predictor (once at the exit, once at re-entry) but only <i>once</i> with a "
        "2-bit predictor, because a single anomaly does not flip the prediction."))
    A(h3("7.3 Branch Target Buffer (BTB)"))
    A(fig("page041.jpg", w=10.5*gen.cm, cap="Two-bit / correlating predictor state diagram (source: p. 41)."))
    A(p("<b>Reading the figure.</b> The correlating (two-level) predictor. A global branch-history register indexes a table of counters, so the prediction depends on the pattern of recent branches (e.g. TTNT), not just this branch."))
    A(p("Even a correctly predicted <i>direction</i> is useless without the <i>target address</i>. A "
        "<b>Branch Target Buffer</b> is a small cache, indexed by the branch's address, that stores the "
        "predicted target and (usually) the predicted direction. It lets the fetch unit start fetching the "
        "target in the very next cycle — <i>before</i> decoding the branch — so a correctly predicted branch "
        "costs <b>zero</b> penalty."))
    A(formula("Effective branch penalty (cycles/instr) = branch frequency × [ hit_rate×mispredict×penalty\n"
              "                                                   + (1−hit_rate)×buffer_miss_penalty ]"))
    A(callout("<b>Reading the formula:</b> if the branch is in the BTB (hit rate h) and we mispredict, we pay "
              "the misprediction penalty; if it is <i>not</i> in the BTB, we pay the buffer-miss penalty. "
              "Add the two and multiply by how often branches occur. (See PYQ ca8/ca38.)", 'tip'))

    A(h3("7.4 Correlating and tournament predictors"))
    A(fig("page038.jpg", w=10.5*gen.cm, cap="Two-level (correlating) and tournament branch predictors (source: p. 38)."))
    A(p("<b>Reading the figure.</b> Two-level (correlating) and tournament predictors. The tournament predictor keeps both a local and a global predictor and uses a chooser to pick whichever has been more accurate."))
    A(p("Branch behaviour often depends on other branches (e.g. <font face='Mono'>if(a==0) … if(a==0) …</font>). "
        "A <b>correlating</b> (two-level) predictor uses a global history register — the outcomes of the last "
        "<i>k</i> branches — together with the branch address to index the predictor table, capturing such "
        "patterns. A <b>tournament (hybrid)</b> predictor runs two predictors and uses a chooser (itself a "
        "2-bit counter per branch) to pick whichever has been more accurate."))

    A(h3("7.5 Control-hazard reduction techniques"))
    A(table(["Technique","How it works","Cost"],
      [["Stall","Wait for the branch to resolve.","Certain penalty = cycles to resolution"],
       ["Predict + flush","Guess; flush only when wrong.","Penalty × misprediction rate"],
       ["Delayed branch","Compiler fills the branch-delay slot with useful work.","Requires a free instruction"],
       ["Branch Target Buffer","Cache target + direction; zero penalty on a hit.","Extra cache hardware"],
       ["Speculation (ROB)","Execute the predicted path; commit only when the branch is confirmed.","Reorder buffer, more hardware"]],
      widths=[1.4,3.4,1.6]))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Branch prediction"))
    A(Paragraph("Q (ca8 · Q4a). A deeply pipelined processor uses a branch-target buffer for conditional "
                "branches. Misprediction penalty = 4 cycles, buffer-miss penalty = 3 cycles, hit rate = 90%, "
                "accuracy = 90%, branch frequency = 18%. Base CPI (no branch stalls) = 1. How much faster is "
                "the processor with the BTB versus one with a fixed 2-cycle branch penalty?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("With BTB:\n"
              "  stall per branch = hit×mispredict×penalty + miss×miss_penalty\n"
              "                   = 0.90×0.10×4 + 0.10×3 = 0.36 + 0.30 = 0.66 cycles\n"
              "  CPI_BTB = 1 + 0.18×0.66 = 1 + 0.1188 = 1.1188\n\n"
              "With fixed 2-cycle penalty:\n"
              "  CPI_fixed = 1 + 0.18×2 = 1.36\n\n"
              "Speed-up = 1.36 / 1.1188 = 1.216  →  about 1.22× faster"))
    A(p("<b>Answer: ≈ 1.22× faster with the branch-target buffer.</b> Note how the accuracy applies only on "
        "a BTB hit; a BTB miss always costs the buffer-miss penalty regardless of direction."))

    A(Paragraph("Q (ca38 · Q3a). Determine the total branch penalty for a branch target buffer given the "
                "penalty cycles below. Prediction accuracy = 90% (for buffered branches), hit rate = 90%.", ST['q']))
    A(table(["In buffer?","Branch","Penalty cycles"],
      [["Yes","Taken","0"],
       ["Yes","Not taken","2"],
       ["No","—","(buffer miss, from the problem's table)"]],
      widths=[1.5,1.5,2.0]))
    A(Paragraph("<b>Solution.</b> Using the same structure: buffered correct = 0; buffered mispredict = 2; "
                "unbuffered = buffer-miss penalty. Total penalty = 0.9×0.1×2 + 0.1×(miss penalty). If the "
                "problem's miss penalty is 2, then penalty = 0.18 + 0.2 = 0.38 cycles/branch; multiply by "
                "branch frequency for CPI contribution.", ST['ans']))
    A(callout("<b>Pattern for all BTB questions:</b> (1) hit-rate × misprediction-rate × mispredict-penalty; "
              "(2) + (1 − hit-rate) × miss-penalty; (3) × branch frequency; (4) add to base CPI; (5) compare "
              "as a ratio of CPIs (or execution times).", 'tip'))

    A(Paragraph("Q (ca17 · Q1 / ca21 · Q2b). Given the instruction mix (loads 25%, stores 15%, branches 10%, "
                "ALU 50% — as per the slide) and 60% of conditional branches taken, answer: (i) in what % of "
                "cycles does the branch adder in EX generate a used value? (ii) how often is data memory "
                "used? (iii) speed-up from pipelining a single-cycle datapath?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "<b>(i)</b> The branch adder computes a target only for <i>taken</i> branches that reach EX. Fraction "
      "of cycles the adder's value is used = (branch fraction) × (taken fraction) = 10% × 60% = <b>6%</b>.",
      "<b>(ii)</b> Data memory is used by loads and stores only = 25% + 15% = <b>40%</b> of cycles.",
      "<b>(iii)</b> If the single-cycle datapath's critical path is the sum of stage delays, pipelining lets "
      "the clock run at the slowest stage instead of the sum. Speed-up ≈ (sum of stage delays) / (slowest "
      "stage delay + register delay). With the latencies given in the problem, compute "
      "Σtᵢ / (max tᵢ + t_reg).",
    ]))
    A(formula("Speed-up(pipelining) = Σ(stage logic delays) / [ max(stage delay) + register delay ]"))

    # ============ 8. DYNAMIC SCHEDULING ============
    A(PageBreak())
    A(h1(8,"Dynamic Scheduling: Scoreboarding & Tomasulo's Algorithm","Letting hardware reorder work at run time"))
    A(p("A static schedule is fixed at compile time and cannot know about a cache miss that suddenly makes a "
        "load take 50 cycles. <b>Dynamic scheduling</b> lets the hardware reorder instructions at run time so "
        "the pipeline keeps issuing useful work even when one instruction stalls. The two landmark techniques "
        "are the <b>scoreboard</b> and <b>Tomasulo's algorithm</b>."))

    A(h3("8.1 Scoreboarding"))
    A(p("The scoreboard is a centralized control unit that decides when an instruction may issue, read its "
        "operands, execute and write back. It allows out-of-order execution but <b>in-order issue</b> and "
        "<b>in-order write-back</b>. It tracks, for each instruction, four stages:"))
    A(table(["Stage","Meaning","Blocked by"],
      [["Issue","Decode and send to a functional unit.","Structural hazard (unit busy) or WAW (no scoreboard entry)"],
       ["Read operands","Wait until both operands are available.","RAW — producer has not written yet"],
       ["Execute","Run in the functional unit.","Functional-unit latency"],
       ["Write result","Write back to the register file.","WAR — an earlier instruction has not read the old value"]],
      widths=[1.2,2.4,2.4]))
    A(callout("<b>Scoreboard limits:</b> it cannot do register renaming, so it stalls on WAW at issue and WAR "
              "at write-back, and it has a single register file with no forwarding of values to waiting "
              "instructions. Tomasulo fixes all three.", 'warn'))

    A(h3("8.2 Tomasulo's algorithm — the big idea"))
    A(p("Tomasulo introduced three mechanisms that together allow aggressive out-of-order execution:"))
    A(table(["Mechanism","What it does"],
      [["Reservation stations","Buffers next to each functional unit that hold an instruction and its operands "
        "until the unit is free and the operands are ready. Each has fields Op, Vj, Vk (values), Qj, Qk (the "
        "reservation station that will produce the missing operand)."],
       ["Register renaming via Qj/Qk","Instead of a value, a station can hold the <i>name</i> (Q) of the "
        "station that will produce it. This renames registers and removes WAR and WAW hazards."],
       ["Common Data Bus (CDB)","Results are broadcast on the CDB. Every station waiting on that result grabs "
        "it at the same time — this is the forwarding that replaces the register file round-trip."]],
      widths=[1.5,4.5]))
    A(fig("page054.jpg", w=12.5*gen.cm, cap="Tomasulo hardware: reservation stations, load/store buffers, and the Common Data Bus (source: lecture notes, p. 54)."))
    A(p("<b>Reading the figure.</b> The Tomasulo hardware. Reservation stations hold instructions waiting for operands, the register-result table names the producer of each register, and the Common Data Bus (CDB) broadcasts results to everyone waiting."))
    A(h3("8.3 How an instruction flows through Tomasulo"))
    A(fig("page043.jpg", w=10.5*gen.cm, cap="Reservation-station fields: Op, Vj, Vk, Qj, Qk and the CDB (source: p. 43)."))
    A(p("<b>Reading the figure.</b> The fields of a reservation station: Op, Vj, Vk, Qj, Qk. This is the heart of the exam question — <b>V</b> is a ready operand value, <b>Q</b> names the station that will produce it."))
    A(bullets([
      "<b>Issue</b> — take the next instruction from the queue. If a free reservation station exists for its "
      "unit, issue it. If the operands are ready, place them in Vj/Vk; otherwise put the producing station's "
      "name in Qj/Qk. This renames the destination register (the register-result table now points to this "
      "station).",
      "<b>Execute</b> — when both Qj and Qk are empty (operands ready) and the unit is free, start "
      "execution. Loads/stores compute addresses first, then access memory.",
      "<b>Write result</b> — when done, broadcast the value on the CDB. Stations with Qj/Qk equal to this "
      "station read it; the register-result table is updated if this station is the pending producer.",
    ]))
    A(h3("8.4 The data structures you must draw in the exam"))
    A(fig("page057.jpg", w=10.5*gen.cm, cap="Tomasulo instruction-status and reservation-station tables (source: p. 57)."))
    A(p("<b>Reading the figure.</b> The instruction-status table and reservation-station tables you must fill in cycle by cycle for a Tomasulo question. Track Issue, Execute and Write-result for every instruction."))
    A(table(["Structure","Columns","Meaning"],
      [["Instruction status","Instruction | Issue | Execute-complete | Write-result","Which stage each instruction is in"],
       ["Reservation stations","Name | Busy | Op | Vj | Vk | Qj | Qk (and A for addresses)","State of each buffer entry"],
       ["Register result status","Register | producer station","Which station will write each register"]],
      widths=[1.5,2.3,2.2]))
    A(callout("<b>How to attack a Tomasulo question:</b> (1) draw the three tables empty; (2) issue one "
              "instruction per cycle while a free station exists; (3) fill V if ready, else Q; (4) start "
              "execution when both Q's are clear and the unit is free; (5) on completion, broadcast on the "
              "CDB and clear every matching Q; (6) record the write-result cycle. Keep a cycle-by-cycle log.", 'tip'))

    A(h3("8.5 Scoreboard vs Tomasulo — the exam comparison"))
    A(fig("page056.jpg", w=10.5*gen.cm, cap="Tomasulo instruction-status table with Issue/Execute/Write-result (source: p. 56)."))
    A(p("<b>Reading the figure.</b> The Tomasulo tables with the Issue / Execute / Write-result columns, showing how a CDB broadcast clears the Q fields of waiting instructions."))
    A(table(["Feature","Scoreboard","Tomasulo"],
      [["Issue order","In order","In order"],
       ["Execution","Out of order","Out of order"],
       ["Write-back","In order","Out of order (via CDB)"],
       ["Register renaming","No","Yes (Qj/Qk)"],
       ["Forwarding","No (register file)","Yes (Common Data Bus)"],
       ["Handles WAR/WAW","Stalls","Renames them away"],
       ["Control speculation","No","Not in the original; added later with a ROB"]],
      widths=[1.6,2.0,2.4]))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Tomasulo & dynamic scheduling"))
    A(Paragraph("Q (ca12 · Q4). Execute the code below using Tomasulo's algorithm; compute the values during "
                "clock cycle 6. Use the given tables.", ST['q']))
    A(formula("LD   F6, 34(R2)\nLD   F2, 45(R3)\nMULF F0, F2, F4\nSUBF F8, F6, F2\nDIVF F10, F0, F6"))
    A(Paragraph("<b>Solution.</b> Issue LD F6 (cycle 1) and LD F2 (cycle 2) into Load1/Load2; MULF issues to "
                "Mult1 with Qj = Load2 (F2 pending); SUBF issues to Add1 with Qj = Load1 (F6); DIVF issues "
                "with Qj = Mult1 and Qk = Load1. As the loads complete they broadcast on the CDB and clear "
                "the matching Q's, letting MUL and SUB begin. By cycle 6 the two loads have completed, MUL "
                "and SUB are executing, and DIV is still waiting on Mult1. The instruction-status and "
                "reservation-station tables are filled in exactly this way (Issue / Execute-complete / "
                "Write-result columns, plus Busy, Op, Vj, Vk, Qj, Qk per station).", ST['ans']))
    A(table(["Instruction","Issue","Exec-complete","Write-result"],
      [["LD F6,34(R2)","1","2","3"],
       ["LD F2,45(R3)","2","3","4"],
       ["MULF F0,F2,F4","3","— (starts at 5)","—"],
       ["SUBF F8,F6,F2","4","— (starts at 5)","—"],
       ["DIVF F10,F0,F6","5","— (waits on Mult1)","—"]],
      widths=[1.6,0.8,1.4,1.2]))
    A(table(["Station","Busy","Op","Vj","Vk","Qj","Qk"],
      [["Load1","No","—","—","—","—","—"],
       ["Load2","No","—","—","—","—","—"],
       ["Add1","Yes","SUB","34(R2) value","F2 value","—","—"],
       ["Mult1","Yes","MUL","F2 value","F4 value","—","—"],
       ["Mult2","No","—","—","—","—","—"]],
      widths=[0.9,0.6,0.7,1.2,1.0,0.7,0.7]))
    A(p("<b>Register-result status at cycle 6:</b> F0 → Mult1, F8 → Add1, F10 → Mult2; F2 and F6 already "
        "written (from the loads). This is the snapshot the question asks for."))

    A(Paragraph("Q (ca18 · Q3). Implement the loop below using Tomasulo's algorithm. Multiply takes 4 clocks; "
                "loads may miss in the cache. Use the given tables.", ST['q']))
    A(formula("LD   F0, 0(R1)\nMULT F4, F0, F2\nSD   F4, 0(R1)\nSUBI R1, R1, #8\nBNEZ R1, Loop"))
    A(Paragraph("<b>Solution.</b> Each iteration: LD F0 issues to a Load buffer (F0 renamed to Load1); MULT "
                "F4 issues to Mult1 with Qj = Load1 (waiting for F0) — this is the renaming that lets the "
                "next iteration's LD F0 use a <i>different</i> load station, so the WAW on F0 disappears. "
                "SD issues to Store1, waiting on Mult1 for F4. SUBI (integer) and BNEZ (branch) issue to "
                "their own units. Because MULT takes 4 clocks and loads may miss, the second iteration's LD "
                "can issue into Load2 while the first MULT is still executing — this is exactly the "
                "out-of-order overlap Tomasulo enables. Fill the instruction-status table cycle by cycle and "
                "the reservation-station table with Qj/Qk pointing at the pending producers.", ST['ans']))
    A(table(["Iteration","Instruction","Issues to","Waits on (Q)"],
      [["1","LD F0,0(R1)","Load1","— (address ready)"],
       ["1","MULT F4,F0,F2","Mult1","Qj = Load1"],
       ["1","SD F4,0(R1)","Store1","Qk = Mult1"],
       ["1","SUBI R1,R1,#8","Int unit","—"],
       ["1","BNEZ R1,Loop","Branch unit","—"],
       ["2","LD F0,0(R1)","Load2","— (different station: F0 renamed)"]],
      widths=[0.9,1.6,1.2,2.3]))

    A(Paragraph("Q (ca34 · Q2b). The instruction sequence below executes on a system that issues in order "
                "but executes out of order, with 3 load units, 3 adders and 2 multipliers. FP add = 2, FP "
                "multiply = 10, divide = 40 cycles. Using Tomasulo with dynamic branch prediction, at what "
                "cycle is the final value of F10 available, and what is the state of the functional units "
                "when DIVD is executing? Picture the reservation stations.", ST['q']))
    A(formula("LD   F6, 34(R2)\nLD   F2, 45(R3)\nMULTD F0, F2, F4\nSUBD F8, F6, F2\nDIVD F10, F0, F6\nADDD F6, F8, F2"))
    A(Paragraph("<b>Solution.</b> Trace the CDB broadcasts:", ST['ans']))
    A(bullets([
      "LD F6 completes and broadcasts; SUBD can start (needs F6, F2).",
      "LD F2 completes and broadcasts; MULTD and SUBD both have their operands.",
      "MULTD takes 10 cycles; when it finishes it broadcasts F0, which is what DIVD is waiting for.",
      "DIVD then takes 40 cycles. The final value of F10 = (cycle MULTD finishes) + 40.",
      "While DIVD executes, the 3 adders and 2 multipliers are otherwise idle (SUBD has finished), and the "
      "load units are free; the reservation stations show Div busy with its Vj/Vk filled and the ADDD "
      "either done or waiting on F8.",
    ]))
    A(formula("Cycle(F10) = Cycle(LD F2 done) + 10 (MULT) + 40 (DIV)\n"
              "         = 3 + 10 + 40 = 53 cycles (illustrative, per the given issue order)"))
    A(p("The point being tested is that the divide cannot start until the multiply completes (RAW on F0), and "
        "the multiply cannot start until the load completes — so the latencies chain up. Tomasulo lets the "
        "independent ADDD and SUBD proceed in parallel meanwhile."))

    # ============ 9. SPECULATION ============
    A(PageBreak())
    A(h1(9,"Hardware Speculation & the Reorder Buffer","Committing safely when you guess"))
    A(p("Tomasulo lets us execute out of order, but it cannot execute <i>past a branch</i> safely: if we "
        "guessed the branch wrong, we must be able to undo. <b>Speculation</b> solves this by keeping "
        "speculative results out of the architectural state until the instruction is certain to be executed. "
        "The hardware device that does this is the <b>Reorder Buffer (ROB)</b>."))

    A(h3("9.1 What speculation adds to Tomasulo"))
    A(fig("page066.jpg", w=10.5*gen.cm, cap="Pipeline timing table with speculation and the commit stage (source: p. 66)."))
    A(p("<b>Reading the figure.</b> Pipeline timing with speculation. Instructions issue and execute out of order, but <i>commit</i> (update the architectural state) only in program order — that is what makes precise exceptions possible."))
    A(table(["Addition","Purpose"],
      [["Reorder Buffer (ROB)","Holds results of instructions from issue to commit, in program order. Acts as a "
        "renaming table and provides operands (so no separate register file write is needed until commit)."],
       ["Speculative execution past branches","Instructions on the predicted path execute and write to the ROB, "
        "not to the architectural registers."],
       ["Commit (retire) stage","An instruction's result is written to the register file / memory only when it "
        "reaches the head of the ROB <i>and</i> is no longer speculative. Commits happen in program order."],
       ["Branch misprediction","If a branch is wrong, its ROB entries (and those of all later instructions) are "
        "flushed; the correct path restarts. Speculative state is discarded."],
       ["Exceptions","Because commits are in order, an exception can be taken precisely — no earlier "
        "speculative instruction has altered state."]],
      widths=[1.6,4.4]))
    A(fig("page055.jpg", w=9.5*gen.cm, cap="Commit / write-result stage added by speculation (source: lecture notes, p. 55)."))
    A(p("<b>Reading the figure.</b> The three phases of dynamic scheduling — issue, execute, write result — with the reorder buffer enforcing program-order commitment."))

    A(h3("9.2 The four steps of a speculation pipeline"))
    A(fig("page065.jpg", w=10.5*gen.cm, cap="Pipeline timing with speculation: issue, execute, read, write, commit (source: p. 65)."))
    A(p("<b>Reading the figure.</b> The speculative pipeline laid out cycle by cycle: issue, execute, read, write and commit. Notice that the commit stage is strictly in order even though the others are not."))
    A(bullets([
      "<b>Issue</b> — get an instruction from the queue into a reservation station and a ROB entry (in order).",
      "<b>Execute</b> — when operands are ready; may go out of order; results go to the ROB.",
      "<b>Write result</b> — broadcast on the CDB; the ROB and waiting stations capture the value.",
      "<b>Commit</b> — when the instruction reaches the head of the ROB and is non-speculative, write the "
      "register file / memory and free the ROB entry. This is the only step that changes architectural state.",
    ]))
    A(callout("<b>Why commit matters:</b> it is the single point where the out-of-order, speculative "
              "execution becomes permanent and visible. Everything before commit is undoable; everything "
              "after is architectural truth. This is what makes precise exceptions and correct branch "
              "recovery possible.", 'tip'))

    A(h3("9.3 Exam-relevant insights"))
    A(bullets([
      "Renaming (Tomasulo) removes WAR/WAW; a ROB additionally gives <i>precise</i> state at commit.",
      "ROB entries are allocated in program order and freed in program order — a circular queue.",
      "A mispredicted branch flushes the ROB entries after the branch.",
      "Speculation can also prefetch/execute past <i>exceptions</i>, but the exception is only raised at commit.",
      "Draw the ROB as a table: Entry | Instruction | Destination | Value | Ready | Speculative.",
    ]))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Speculation & ROB"))
    A(Paragraph("Q (ca25 · Q2). For the loop below, what are the contents of the ROB when we have issued all "
                "instructions in the loop twice, assuming the L.D and S.D of the first iteration have "
                "committed and all other instructions have completed execution?", ST['q']))
    A(formula("Loop: L.D    F0, 0(R1)   ; F0 = array element\n"
              "      ADD.D  F4, F0, F2   ; add scalar in F2\n"
              "      S.D    F4, 0(R1)    ; store result\n"
              "      DADDUI R1, R1, #-8  ; decrement pointer\n"
              "      BNE    R1, R2, Loop ; branch"))
    A(Paragraph("<b>Solution.</b> Issuing the loop twice gives 10 instructions. The first iteration's L.D and "
                "S.D have <i>committed</i> (left the ROB); every other instruction has <i>completed execution</i> "
                "but is still waiting to commit (or, for the branch, has resolved). So the ROB holds the "
                "completed-but-uncommitted entries in program order: ADD.D(F4), DADDUI(R1), BNE, then the "
                "second iteration's L.D(F0), ADD.D(F4), S.D(F4), DADDUI(R1), BNE — each with its computed "
                "value, marked ready, and flagged speculative where it lies past a branch that has not "
                "committed.", ST['ans']))
    A(table(["ROB entry (in program order)","Instruction","Value ready?","Committed?"],
      [["1 (L.D F0,0(R1))","iter 1","Yes","Committed → left the ROB"],
       ["2 ADD.D F4,F0,F2","iter 1","Yes","Waiting to commit"],
       ["3 (S.D F4,0(R1))","iter 1","Yes","Committed → left the ROB"],
       ["4 DADDUI R1,R1,#-8","iter 1","Yes","Waiting"],
       ["5 BNE R1,R2,Loop","iter 1","Yes","Waiting (resolved)"],
       ["6 L.D F0,0(R1)","iter 2","Yes","Waiting"],
       ["7 ADD.D F4,F0,F2","iter 2","Yes","Waiting"],
       ["8 S.D F4,0(R1)","iter 2","Yes","Waiting"],
       ["9 DADDUI R1,R1,#-8","iter 2","Yes","Waiting"],
       ["10 BNE R1,R2,Loop","iter 2","Yes","Waiting"]],
      widths=[2.0,0.8,1.0,2.2]))
    A(p("This shows the essence of speculation: even though execution has run far ahead, the architectural "
        "state only advances when entries commit in order — so the first iteration's memory writes are "
        "already permanent while later ones wait."))

    A(Paragraph("Q (ca28 · Q4c). How is Tomasulo's algorithm modified to include speculation? What additional "
                "hardware is required?", ST['q']))
    A(Paragraph("<b>Solution.</b> Add a <b>Reorder Buffer</b> and a <b>commit</b> stage. Instructions allocate "
                "ROB entries in order at issue; results are written to the ROB and broadcast on the CDB; the "
                "ROB supplies operands to waiting instructions and the register file is only updated at "
                "commit, in program order. Branch prediction directs which path is fetched; on a "
                "misprediction the ROB is flushed past the branch. Additional hardware: the ROB itself (with "
                "valid/ready/speculative bits), logic to handle ROB head commit, branch-prediction hardware, "
                "and flush/recovery logic. This yields precise exceptions and correct recovery from "
                "mispredicted branches.", ST['ans']))

    A(Paragraph("Q (ca40 · Q3d). Discuss the role of Tomasulo's algorithm in out-of-order execution, with an "
                "example, and explain the necessity of the commit stage and the role of the reorder buffer in "
                "hardware-based speculation.", ST['q']))
    A(Paragraph("<b>Solution (pointwise).</b>", ST['ans']))
    A(bullets([
      "<b>Role:</b> Tomasulo lets the hardware issue instructions in order but execute them out of order, "
      "using reservation stations to hold pending operands and the CDB to forward results — so a stalled "
      "instruction (e.g. a cache-missing load) does not block independent work behind it.",
      "<b>Example:</b> <font face='Mono'>MUL F0,F2,F4 ; ADD F6,F0,F8 ; SUB F10,F12,F14</font>. The SUB is "
      "independent, so it executes while the MUL (10 cycles) runs; the ADD waits on F0 via Qj = Mult1.",
      "<b>Necessity of commit:</b> out-of-order execution and speculation create results that may be wrong "
      "(mispredicted branch) or incomplete. The commit stage is the barrier that makes results permanent only "
      "when they are certain, giving precise state and precise exceptions.",
      "<b>ROB role:</b> it buffers speculative results in program order, supplies operands, tracks readiness, "
      "and is the structure that is flushed on a misprediction — the hardware bookkeeping that makes "
      "speculation safe.",
    ]))


    A(Paragraph("Q (ca32 · Q1). What are the four different types of predictors? Elaborate on their "
      "performance in terms of average misprediction rate.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(table(["Predictor","Rule","Typical misprediction rate"],
      [["Always taken","Predict taken for every branch.","~30-40%"],
       ["Always not taken","Predict not taken for every branch.","~30-40%"],
       ["BTFNT (backward taken, forward not taken)","Loops (backward) taken; if-statements (forward) not taken.","~20-25%"],
       ["2-bit saturating counter","Per-branch counter needs two wrong outcomes to flip.","~10-15%"]],
      widths=[1.8,2.8,1.4]))
    A(p("(Correlating and tournament predictors go further, reaching ~5% and ~3% respectively.) The numbers "
      "show why simple static rules are rarely used in real processors."))

    A(Paragraph("Q (ca39 · Q3b). A compiler/hardware keeps multiple loop iterations in flight by renaming "
      "registers using a pool of 64 temporary registers T0-T63, indexed by the source register and holding the "
      "last destination that targeted it. Maintain true dependences and construct the renamed code.", ST['q']))
    A(formula("Loop:  L.D   F4, 0(Rx)\n       MULTD F2, F0, F2\n       DIVD  F8, F4, F2\n"
              "       L.D   F4, 0(Ry)\n       ADDD  F6, F0, F4\n       SUBD  F8, F8, F6\n       S.D   F8, 0(Ry)"))
    A(Paragraph("<b>Solution.</b> Each iteration re-uses F4, F2, F8. Rename the destinations of the "
      "second-iteration instructions to fresh T registers so the two iterations do not collide, keeping the "
      "RAW chain intact:", ST['ans']))
    A(formula("iter1: L.D  F4,0(Rx)   → dest F4  (→T1)\n"
              "       MULTD F2,F0,F2  → dest F2  (→T2)\n"
              "       DIVD  F8,F4,F2  → dest F8  (→T3)\n"
              "iter2: L.D  T4,0(Ry)   ; renamed (was F4)\n"
              "       ADDD T5,F0,T4   ; renamed (was F6)\n"
              "       SUBD T6,T3,T5   ; renamed, still uses iter1's F8 (T3)\n"
              "       S.D  T6,0(Ry)"))
    A(p("Renaming removes WAR/WAW (name) dependences so the iterations can overlap; true (RAW) dependences "
      "such as DIVD's use of F4/F2 and SUBD's use of F8 are preserved by pointing the renamed register at the "
      "correct producer."))

    A(Paragraph("Q (ca39 · Q3c). If the pipeline detected data dependences and stalled only on those, how many "
      "cycles would the loop body require? Show the code with &lt;stall&gt; inserted where needed (latency "
      "1+N means N stall cycles).", ST['q']))
    A(Paragraph("<b>Solution.</b> Walk through the loop body and, for each consumer, insert <i>N</i> stall "
      "cycles where <i>N</i> is the producer's extra latency beyond 1. Independent instruction pairs get no "
      "stalls. For the sequence above with FP latencies (multiply ~4-5, add ~2-3), the MULTD→DIVD and "
      "ADDD→SUBD pairs need stalls, while the independent L.D of the second iteration can fill them.", ST['ans']))
    A(formula("L.D   F4,0(Rx)\nMULTD F2,F0,F2\nDIVD  F8,F4,F2\n<stall> ×(mult-latency−1)\n"
              "L.D   F4,0(Ry)   ; independent — fills a slot\nADDD  F6,F0,F4\n<stall> ×(add-latency−1)\n"
              "SUBD  F8,F8,F6\nS.D   F8,0(Ry)"))
    A(p("<b>Method:</b> latency 1+0 → no stall; 1+1 → one stall; 1+N → N stalls. Insert stalls only on "
      "producer→consumer pairs."))

    A(Paragraph("Q (ca28 · Q4a,b). (a) Distinguish between static and dynamic scheduling. (b) Name three major "
      "techniques that reduce control-hazard stalls and explain them.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "<b>(a)</b> Static scheduling decides the instruction order at compile time (no run-time information); "
      "dynamic scheduling reorders instructions in hardware at run time using reservation stations and can "
      "react to cache misses and variable latencies.",
      "<b>(b)</b> (1) <b>Branch prediction</b> — guess the direction and fetch down that path, flushing only "
      "on a misprediction. (2) <b>Delayed branch</b> — the compiler places a useful instruction in the branch "
      "delay slot so it always executes. (3) <b>Branch Target Buffer</b> — cache the branch's target and "
      "direction so fetching continues with no penalty on a hit. (Speculation with a reorder buffer is a "
      "fourth.)",
    ]))

    A(Paragraph("Q (ca34 · Q1a). State the advantages of out-of-order pipelines over in-order pipelines.", ST['q']))
    A(Paragraph("<b>Solution.</b> An out-of-order (OOO) pipeline can execute independent instructions while "
      "a slow instruction (e.g. a cache-missing load or a long FP divide) waits, so it keeps functional units "
      "busy and achieves a lower effective CPI. In-order pipelines must stall the whole pipe behind the slow "
      "instruction. OOO also adapts to run-time events (misses, variable latencies) that a static schedule "
      "cannot see. The cost is extra hardware: reservation stations, a reorder buffer, and complex issue "
      "logic.", ST['ans']))

    return F
