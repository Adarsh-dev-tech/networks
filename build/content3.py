"""Part III — Pipelining, Hazards and Branch Prediction."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

def build():
    F=[]
    def A(x): F.extend(x if isinstance(x,list) else [x])

    # ============ 5. PIPELINING ============
    A(PageBreak())
    A(h1(5,"Pipelining: The Assembly Line of the CPU","Speed-up, hazards and the MIPS 5-stage pipeline"))
    A(p("A single-cycle processor does fetch, decode, execute, memory and write-back one after another in "
        "one long clock period — wasteful, because at any instant most hardware sits idle. A "
        "<b>pipelined</b> processor overlaps these steps: while instruction 1 executes, instruction 2 is "
        "decoded and instruction 3 is fetched. Exactly like a car assembly line, throughput rises sharply "
        "even though the time for <i>one</i> instruction (its latency) does not fall."))

    A(h3("5.1 The classic MIPS 5-stage pipeline"))
    A(fig("page014.jpg", w=10.5*gen.cm, cap="Instruction execution and the five pipeline stages (source: p. 14)."))
    A(p("<b>Reading the figure.</b> The five pipeline stages (IF, ID, EX, MEM, WB) and how successive instructions overlap. The first instruction takes all five cycles; after that the pipeline is full and one instruction finishes per cycle."))
    A(table(["Stage","Name","What happens"],
      [["1","IF — Instruction Fetch","Read the instruction at PC from memory; PC ← PC + 4."],
       ["2","ID — Instruction Decode","Decode the opcode, read the register file, compute branch targets."],
       ["3","EX — Execute","ALU does the arithmetic or address calculation; branch decision made."],
       ["4","MEM — Memory","Load or store data (only for load/store instructions)."],
       ["5","WB — Write-Back","Write the ALU or loaded value back into the register file."]],
      widths=[0.6,1.7,3.7]))
    A(fig("page033.jpg", w=12.5*gen.cm, cap="Classic 5-stage pipeline: the instruction stream advances one stage per cycle (source: lecture notes, p. 33)."))
    A(p("<b>Reading the figure.</b> The pipeline timing (space–time) chart. Each instruction occupies a diagonal band across the stages, and in steady state the throughput is one instruction per cycle — the ideal CPI of 1."))
    A(p("An instruction moves one stage to the right every cycle. The <b>pipeline registers</b> between "
        "stages hold the intermediate results so that each stage works on a different instruction in the "
        "same cycle."))
    A(h3("5.2 Pipeline timing diagram (space-time chart)"))
    A(fig("page034.jpg", w=10.5*gen.cm, cap="Instruction types and their pipeline stage usage (source: p. 34)."))
    A(p("<b>Reading the figure.</b> Different instruction types occupy different numbers of cycles (loads/stores and branches take longer than ALU ops). This is why the real CPI is above 1 even with an ideal pipeline."))
    A(p("The standard way to show a pipeline is a table where rows are instructions and columns are clock "
        "cycles. Below, four instructions I1–I4 flow through the five stages:"))
    A(table(["Instruction","C1","C2","C3","C4","C5","C6","C7","C8"],
      [["I1","IF","ID","EX","MEM","WB","","",""],
       ["I2","","IF","ID","EX","MEM","WB","",""],
       ["I3","","","IF","ID","EX","MEM","WB",""],
       ["I4","","","","IF","ID","EX","MEM","WB"]],
      widths=[1.3,0.62,0.62,0.62,0.62,0.62,0.62,0.62,0.62]))
    A(p("The first instruction finishes at cycle 5; every cycle after that one instruction completes. "
        "The pipeline is <b>full</b> from cycle 5 onward."))

    A(h3("5.3 Speed-up, throughput and the ideal CPI"))
    A(p("With <i>k</i> stages and <i>N</i> instructions, ignoring stalls:"))
    A(formula("Non-pipelined time  = N × k × t      (t = delay of one stage)\n"
              "Pipelined time      = (k + N − 1) × t\n"
              "Speed-up S = N·k / (k + N − 1)  →  k   as N → ∞\n"
              "Ideal CPI = 1 instruction per cycle (throughput = f)"))
    A(p("<b>Derivation.</b> The first instruction needs all k stages (k cycles). Each of the remaining "
        "N − 1 instructions adds exactly one more cycle, because they overlap. Total cycles = k + (N − 1). "
        "Dividing the un-pipelined time N·k by the pipelined time gives the speed-up."))
    A(callout("<b>Three key facts.</b> (1) Pipelining improves <i>throughput</i>, not the latency of a "
              "single instruction. (2) The ideal speed-up is the number of stages. (3) The clock period is "
              "set by the <i>slowest</i> stage (plus register delay).", 'tip'))

    A(h3("5.4 Clock period, latency, throughput and the effect of register overhead"))
    A(p("The pipeline can run no faster than its slowest stage. If stage <i>i</i> takes delay <i>tᵢ</i> and "
        "each pipeline register adds delay <i>d</i>, then:"))
    A(formula("Cycle time T = max(t₁, t₂, …, t_k) + d\n"
              "Latency of one instruction = k × T\n"
              "Throughput = 1 / T  (instructions per second, ideal)"))
    A(p("Splitting a stage into two halves lets you use a shorter cycle time — but the extra pipeline "
        "register also adds delay <i>d</i>, and deeper pipelines mean more hazards and more penalty when a "
        "branch mispredicts. This trade-off is examined (PYQ ca30/ca32)."))

    A(h3("5.5 Pipeline hazards — the three enemies"))
    A(fig("page035.jpg", w=10.5*gen.cm, cap="Five-stage pipeline with per-instruction stage counts (source: p. 35)."))
    A(p("<b>Reading the figure.</b> The stage-by-stage view used to count stalls for a given instruction sequence. Each row is an instruction, each column a cycle; the gaps are the stall cycles."))
    A(p("A <b>hazard</b> is any situation that prevents the next instruction from executing in the next "
        "cycle. There are exactly three kinds, and you must be able to name and fix each."))
    A(table(["Hazard","Cause","Example","Fixes"],
      [["Structural","Two instructions need the same hardware resource in the same cycle",
        "IF and MEM both need memory; one ALU for two EX stages",
        "Duplicate hardware (split I/D caches), stall, or schedule differently"],
       ["Data (RAW/WAR/WAW)","An instruction needs an operand that an earlier instruction has not yet produced",
        "<font face='Mono'>add r1,r2,r3 ; sub r4,r1,r5</font>","Forwarding (bypassing), stalling, scheduling, renaming"],
       ["Control","The next PC depends on a branch that has not resolved yet",
        "<font face='Mono'>beq … ; next instruction unknown</font>","Stall, predict (static/dynamic), delayed branch, speculation"]],
      widths=[0.95,1.9,1.9,1.7]))

    A(h3("5.6 Data hazards in detail"))
    A(table(["Type","Full name","Meaning"],
      [["RAW","Read After Write","j reads a register that i writes → j must wait for i's value (true dependence)."],
       ["WAR","Write After Read","j writes a register that i reads → j must not write before i reads (name dependence)."],
       ["WAW","Write After Write","j writes a register that i also writes → final order must be preserved (name dependence)."]],
      widths=[0.7,1.5,4.0]))
    A(p("<b>Forwarding (bypassing)</b> fixes most RAW hazards: instead of waiting for the value to be "
        "written back, the ALU output is sent straight to the next instruction's EX stage. The hardware "
        "adds a path from the EX/MEM and MEM/WB pipeline registers back to the ALU inputs. With forwarding, "
        "a RAW that needs an ALU result costs <b>no</b> stall; a RAW after a load needs <b>one</b> stall "
        "(the load-use hazard) because the data only arrives after MEM."))
    A(callout("<b>Load-use hazard:</b> a load followed immediately by an instruction that uses the loaded "
              "register must stall one cycle even with forwarding — the value simply does not exist yet at "
              "the start of EX. This is the most common stall in MIPS pipelines.", 'warn'))

    A(h3("5.7 Control hazards and their cost"))
    A(fig("page046.jpg", w=10.5*gen.cm, cap="Control and data hazards with example instruction sequences (source: p. 46)."))
    A(p("<b>Reading the figure.</b> A control/data hazard example. The branch must wait for the comparison result, and a load followed immediately by a use of the loaded value needs a stall even with forwarding."))
    A(p("A branch is decided in the EX stage in the classic pipeline, but the next instruction is fetched in "
        "ID — before we know which way the branch goes. If we simply stall until the branch resolves, we "
        "lose cycles on every branch. The number of lost cycles is the <b>branch penalty</b>."))
    A(formula("Stalls per branch = (number of stages between IF and the stage that resolves the branch)\n"
              "Branch penalty (CPI added) = branch frequency × misprediction rate × penalty cycles\n"
              "Effective CPI = ideal CPI + stall cycles per instruction"))
    A(table(["Technique","How it reduces the penalty"],
      [["Stall until resolved","Simple; penalty = pipeline depth to resolution (e.g. 2-3 cycles)."],
       ["Predict (static)","Guess a direction (always-not-taken / always-taken / BTFNT); flush only on a wrong guess."],
       ["Delayed branch","The compiler puts a useful instruction in the branch delay slot — executed regardless."],
       ["Branch target buffer","Cache the branch's previous target and outcome, so fetch continues without waiting."],
       ["Speculation","Execute down the predicted path and keep the results safe until the branch is confirmed."]],
      widths=[1.3,4.7]))
    A(p("We develop branch prediction fully in Topic 7; here it is enough to know that it converts a "
        "<i>certain</i> penalty into a <i>probabilistic</i> one: you only pay when you guess wrong."))

    A(h3("5.8 Superscalar and deeper pipelines"))
    A(p("A <b>superscalar</b> processor issues more than one instruction per cycle (e.g. 2- or 4-wide). It "
        "needs several functional units and extra logic to detect dependences among the parallel-issued "
        "instructions. A <b>VLIW</b> machine instead has the compiler pack independent operations into one "
        "very long instruction word, moving the scheduling burden to software."))
    A(table(["Design","Who finds ILP?","Issue width","Hardware cost"],
      [["Scalar pipeline","Hardware (pipeline)","1","Low"],
       ["Superscalar","Hardware (dynamic)","&gt;1","High"],
       ["VLIW / EPIC","Compiler (static)","&gt;1 (in one word)","Lower hardware, smarter compiler"]],
      widths=[1.3,2.1,1.3,1.3]))

    A(h3("5.9 Exam-relevant insights"))
    A(bullets([
      "Speed-up ≤ number of stages; achieved only with a long instruction stream and no stalls.",
      "Cycle time = slowest stage + register delay. Adding stages can shorten the cycle but adds register overhead.",
      "Always draw the timing table; count stalls per instruction; add them to the ideal CPI.",
      "Forwarding removes ALU-result stalls but not load-use stalls.",
      "A control hazard resolved in EX costs 2 wasted fetch cycles in the classic pipeline.",
      "When a branch is <b>taken</b> and predicted not-taken, you must flush the wrongly-fetched instructions.",
    ]))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Pipelining & hazards"))
    A(Paragraph("Q (ca9 · Q1). Consider the following instructions executed in a five-stage pipeline. "
                "Explain the flow of execution using two simple diagrams.", ST['q']))
    A(formula("lw  R1, 0(R2)\nadd R3, R4, R5\nsub R6, R1, R3"))
    A(Paragraph("<b>Solution.</b> Use the IF–ID–EX–MEM–WB stages.", ST['ans']))
    A(bullets([
      "Draw the space-time diagram with the three instructions as rows and cycles as columns.",
      "<b>lw</b> uses all five stages: IF, ID, EX, MEM, WB.",
      "<b>add</b> uses IF, ID, EX, (no MEM), WB — a blank in MEM.",
      "<b>sub</b> reads R1 (written by lw) and R3 (written by add) — two RAW dependences.",
    ]))
    A(table(["Instr","C1","C2","C3","C4","C5","C6","C7","C8"],
      [["lw  R1,0(R2)","IF","ID","EX","MEM","WB","","",""],
       ["add R3,R4,R5","","IF","ID","EX","—","WB","",""],
       ["sub R6,R1,R3","","","IF","ID","stall","EX","MEM","WB"]],
      widths=[1.5,0.6,0.6,0.6,0.6,0.6,0.65,0.6,0.6]))
    A(p("The <b>sub</b> must wait one cycle because R1 is produced by the load (load-use hazard). "
        "With forwarding from MEM to EX, the load's result reaches sub's EX stage just in time; the diagram "
        "above shows one stall inserted if forwarding is not available at that point. Two simple diagrams = "
        "(1) the stage-by-stage block flow, and (2) this space-time chart."))

    A(Paragraph("Q (ca9 · Q2a / ca20). Show how the instructions below proceed through the pipeline. Assume "
                "(i) the branch is not taken, and (ii) when it is executed R1 = R2. On which results does the "
                "last <i>add</i> depend? Indicate the hazards and data dependences.", ST['q']))
    A(formula("lw   R3, 0(R5)\nsub  R6, R3, R3\nbeq  R1, R2, Label\nadd  R4, R1, R2"))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "<b>lw → sub</b>: RAW on R3 (load-use). Needs 1 stall even with forwarding.",
      "<b>sub → beq</b>: the branch compares R1,R2, not R6, so no dependence on sub.",
      "<b>beq → add</b>: control dependence — whether <i>add</i> executes depends on the branch. If R1 = R2 "
      "the branch is taken, so <i>add</i> is skipped (or fetched then flushed).",
      "The last <b>add R4,R1,R2</b> depends on <b>R1 and R2</b> — and if the branch is taken it does not "
      "execute at all. Its true dependences are on whichever earlier instructions last wrote R1 and R2 "
      "(here, none in the fragment — they come from before).",
    ]))
    A(table(["Instr","C1","C2","C3","C4","C5","C6","C7","C8","C9"],
      [["lw  R3,0(R5)","IF","ID","EX","MEM","WB","","","",""],
       ["sub R6,R3,R3","","IF","ID","stall","EX","MEM","WB","",""],
       ["beq R1,R2,L","","","IF","ID","stall","EX","","",""],
       ["add R4,R1,R2","","","","IF","ID","stall","IF*","…",""]],
      widths=[1.4,0.56,0.56,0.56,0.56,0.56,0.56,0.6,0.56,0.56]))
    A(p("Hazards present: a <b>data (RAW) hazard</b> lw→sub; a <b>control hazard</b> at the branch (the "
        "fetch after beq is uncertain until EX). With R1 = R2 the branch is taken, so the add fetched after "
        "beq must be flushed and the pipeline redirected to <i>Label</i>."))

    A(Paragraph("Q (ca16 · Q2). For each code sequence state whether it must stall, can avoid stalls using "
                "only forwarding, or can execute without stalling or forwarding.", ST['q']))
    A(formula("(i)  lw $t0,0($t0)\n     add $t1,$t0,$t0\n     addi $t3,$t0,2\n\n"
              "(ii) add $t1,$t0,$t0\n     addi $t2,$t0,5\n     addi $t4,$t1,5\n\n"
              "(iii)addi $t1,$t0,1\n     addi $t2,$t0,2\n     addi $t3,$t0,4\n     addi $t5,$t0,5"))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(table(["Sequence","Dependence","Verdict"],
      [["(i) lw→add","RAW on $t0; the value comes from MEM, not yet available in EX","<b>Must stall 1 cycle</b> (load-use), even with forwarding"],
       ["(i) add→addi","RAW on $t0? No — addi reads $t0 (not $t1), and $t0 was not written by add","No dependence"],
       ["(ii) add→addi→addi","add writes $t1; the third instruction reads $t1","Can avoid stalls with forwarding (ALU result)"],
       ["(iii) four addi","All read $t0; none writes $t0 → completely independent","No stall, no forwarding needed"]],
      widths=[1.3,2.7,2.0]))

    A(Paragraph("Q (ca13 · Q1a). For each RISC fragment, identify the dependences and whether forwarding "
                "suffices or stall cycles are needed.", ST['q']))
    A(formula("(i)  addi r1,#4 ;  load r2,7(r1)\n(ii) add r3,r1,12 ;  store r2,7(r1)\n"
              "(iii)breq r1,place ; store r1,7(r1)\n(iv) store r3,17(r10) ; load r2,12(r8)"))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(table(["Fragment","Dependence","Forwarding enough?","Stalls"],
      [["(i) addi→load","RAW on r1 (address used by load)","Yes — r1 forwarded from EX/MEM","0"],
       ["(ii) add→store","RAW on r1 (store address); store data r2 is not produced here","Yes","0"],
       ["(iii) breq→store","Control dependence (store runs only if branch not taken); store reads r1 also compared by breq","Yes for data; control handled by prediction","0 data; branch penalty on mispredict"],
       ["(iv) store→load","No dependence — store writes memory[r10+17], load reads memory[r8+12]; different addresses","Not needed","0"]],
      widths=[1.2,2.6,1.6,1.1]))

    A(Paragraph("Q (ca27 · Q3b / ca32 · Q5 / ca34 · Q1b). Five-stage pipeline (fetch, decode, execute, memory, "
                "write-back). All ops are 1 cycle except LW and SW (1+2 cycles) and branches (1+1 cycles). "
                "No forwarding. Show the phases per clock for one loop iteration and state the cycles lost to "
                "branch overhead.", ST['q']))
    A(formula("Loop:  LW  R3, 0(R0)\n       LW  R1, 0(R3)\n       ADDI R1, R1, #1\n"
              "       SUB R4, R3, R2\n       SW  R1, 0(R3)\n       BNZ R4, Loop"))
    A(Paragraph("<b>Solution.</b> Loads/stores occupy EX for 2 extra cycles; the branch occupies 1 extra "
                "cycle. Because there is no forwarding, each RAW needs stalls until the value is written "
                "back. The ADDI must wait for the second LW (RAW on R1), and the SW must wait for ADDI.", ST['ans']))
    A(table(["Instr","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"],
      [["LW R3,0(R0)","F","D","E","E","M","W","","","","","","","","","",""],
       ["LW R1,0(R3)","","F","D","st","st","E","E","M","W","","","","","","",""],
       ["ADDI R1,R1,#1","","","","","F","D","st","st","st","E","M","W","","","",""],
       ["SUB R4,R3,R2","","","","","","F","D","","","st","E","M","W","","",""],
       ["SW R1,0(R3)","","","","","","","F","D","","","st","E","E","M","W",""],
       ["BNZ R4,Loop","","","","","","","","F","D","","","st","E","E","M","W"]],
      widths=[1.35,0.35,0.35,0.35,0.35,0.35,0.35,0.38,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]))
    A(p("(F=fetch, D=decode, E=execute, M=memory, W=write-back, st=stall.) The branch occupies its extra "
        "cycle (1+1) and, having no prediction, costs the fetches of the instructions behind it. Counting "
        "the branch's two-stage execution plus the redirect, the <b>branch overhead is 2 cycles per loop "
        "iteration</b> in this no-forwarding, no-prediction model — the two cycles of the BNZ itself beyond "
        "decode that cannot be overlapped with useful work."))
    A(callout("<b>How to attack these questions:</b> (1) write the stage sequence for each instruction; "
              "(2) for each RAW, insert stalls until the producer's W cycle; (3) count the branch's extra "
              "cycles and any flushed fetches. Consistency beats speed.", 'tip'))

    A(Paragraph("Q (ca30 · Q3). The stage delays in a 4-stage pipeline are 800, 500, 400 and 300 ps. The "
                "first stage is replaced by two stages of 600 and 350 ps. What is the throughput increase?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Before: cycle = max(800,500,400,300) = 800 ps  →  throughput = 1/800 ps\n"
              "After : stages = 600,350,500,400,300 → cycle = max = 600 ps → throughput = 1/600 ps\n"
              "Increase = (1/600 − 1/800)/(1/800) × 100% = (800/600 − 1)×100% = 33.33%"))
    A(p("<b>Answer: ≈ 33.3% increase in throughput.</b> The bottleneck moved from 800 ps to 600 ps; the "
        "throughput ratio is 800/600 = 1.333."))

    A(Paragraph("Q (ca32 · Q2). In a 5-stage pipeline the longest stage requires 0.8 ns and the pipeline "
                "register delay is 0.1 ns. What is the clock cycle time? If a 10-stage pipeline splits all "
                "stages in half, what is the cycle time?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("5-stage : cycle = max stage + register delay = 0.8 + 0.1 = 0.9 ns\n"
              "10-stage: each stage halves to 0.4 ns; cycle = 0.4 + 0.1 = 0.5 ns"))
    A(p("<b>Answers: 0.9 ns (5-stage) and 0.5 ns (10-stage).</b> Notice the register delay does not halve, "
        "so doubling the depth does not double the speed (0.9/0.5 = 1.8×, not 2×) — the classic diminishing "
        "return of deep pipelining."))


    A(Paragraph("Q (ca10 · Q1 / ca13 · Q2). The following MIPS program runs on an IF-ID-EX-MEM-WB pipeline. "
      "Identify all data dependences in the form &lt;type&gt; on &lt;register&gt; from L_a to L_b, then work out "
      "the optimal pipeline schedule with forwarding from EX or MEM to any stage and compute the CPI.", ST['q']))
    A(formula("L1  lw  $t2, 60($t1)\nL2  lw  $t1, 40($t2)\nL3  slt $t1, $t1, $t2\nL4  sw  $t1, 20($t2)"))
    A(Paragraph("<b>Solution — dependences.</b>", ST['ans']))
    A(table(["Type","Register","From → To","Reason"],
      [["RAW","$t2","L1 → L2","L2 uses $t2 as a base address; L1 loads $t2"],
       ["RAW","$t2","L1 → L3","L3 reads $t2"],
       ["RAW","$t2","L1 → L4","L4 uses $t2 as a base address"],
       ["RAW","$t1","L2 → L3","L3 reads $t1 (loaded by L2)"],
       ["WAW","$t1","L2 → L3","L2 writes $t1 and L3 writes $t1"],
       ["RAW","$t1","L2 → L4","L4 stores $t1 (value from L2, but note L3 also writes $t1)"]],
      widths=[0.7,0.9,1.0,3.4]))
    A(p("There is also a WAR on $t1 (L3 writes what L2/L4 read). The key hazards are the two load-use RAW "
      "dependences on $t2 (L1→L2 and L1→L3) and the $t1 chain."))
    A(table(["Instr","1","2","3","4","5","6","7","8","9","10"],
      [["L1 lw $t2,60($t1)","IF","ID","EX","MEM","WB","","","",""],
       ["L2 lw $t1,40($t2)","","IF","ID","st","EX","MEM","WB","",""],
       ["L3 slt $t1,$t1,$t2","","","IF","ID","st","st","EX","MEM","WB"],
       ["L4 sw $t1,20($t2)","","","","IF","ID","st","st","EX","MEM","WB"]],
      widths=[1.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]))
    A(p("With forwarding, the load-use dependences still need one stall each (the loaded value only appears "
      "after MEM). <b>Total cycles = 10; CPI = 10/4 = 2.5.</b>"))

    A(Paragraph("Q (ca14 · Q1). Find the hazards in the code below and reorder the instructions to avoid any "
      "stalls.", ST['q']))
    A(formula("lw  $t1, 0($t0)\nlw  $t2, 4($t0)\nadd $t3, $t1, $t2\nsw  $t3, 12($t0)\nlw  $t4, 8($t0)\n"
              "add $t5, $t1, $t4\nsw  $t5, 16($t0)"))
    A(Paragraph("<b>Solution.</b> Hazards: <font face='Mono'>lw $t1</font> → <font face='Mono'>add $t3</font> "
      "(RAW on $t1, load-use); <font face='Mono'>lw $t2</font> → <font face='Mono'>add $t3</font> (RAW on $t2); "
      "<font face='Mono'>add $t3</font> → <font face='Mono'>sw $t3</font> (RAW). Reorder to fill the load-use "
      "slots with independent instructions (the other loads/stores):", ST['ans']))
    A(formula("lw  $t1, 0($t0)\nlw  $t2, 4($t0)\nlw  $t4, 8($t0)      ; independent load fills the slot\n"
              "add $t3, $t1, $t2\nadd $t5, $t1, $t4\nsw  $t3, 12($t0)\nsw  $t5, 16($t0)"))
    A(p("<b>Key:</b> scheduling works only because the loads and stores are independent of the ALU ops. "
      "Reorder to move independent instructions between a producer and its consumer."))

    A(Paragraph("Q (ca20 · Q2). A pipeline has only one memory (for both instructions and data). Whenever an "
      "instruction fetches in the same cycle another accesses data, that structural hazard is resolved in "
      "favour of the data access. What is the total execution time of the sequence? Can adding nops remove "
      "this structural hazard?", ST['q']))
    A(formula("lw  $1, 40($6)\nbeq $2, $0, Label   ; assume $2 == $0\nsw  $6, 50($2)\n"
              "Label: add $2, $3, $4\nsw  $3, 50($4)\nlw  $5, -16($5)\nsw  $4, -16($4)\n"
              "lw  $3, -20($4)\nbeq $2, $0, Label   ; assume $2 != $0\nadd $5, $1, $4"))
    A(Paragraph("<b>Solution.</b> Because there is a single memory, the fetch stage must yield whenever a "
      "load/store is in its MEM stage — that costs one extra cycle per such collision (an instruction-fetch "
      "structural hazard). Add up the base pipeline cycles plus one stall for each cycle in which a MEM access "
      "coincides with a fetch. <b>Adding nops cannot fix a structural hazard</b>: nops consume fetch slots "
      "too, so they do not free the memory — you must duplicate the resource (separate I-cache and D-cache) "
      "or stall.", ST['ans']))

    A(Paragraph("Q (ca31 · Q5). A 5-stage processor (IF, ID, OF, EX, WO). EX takes 1 cycle for ADD/SUB, 3 for "
      "MUL, 6 for DIV. Operand forwarding is used. IF, ID, OF, WO take 1 cycle. How many clock cycles for the "
      "sequence below?", ST['q']))
    A(formula("I0: MUL R2, R0, R1\nI1: DIV R5, R3, R4\nI2: ADD R2, R5, R2\nI3: SUB R5, R2, R6"))
    A(Paragraph("<b>Solution.</b> I2 (ADD) depends on I1 (DIV, RAW on R5) and I0 (MUL, RAW on R2). I3 depends "
      "on I2 (RAW on R2). Because EX is multi-cycle, the pipeline stalls until each producer leaves EX.", ST['ans']))
    A(table(["Instr","1","2","3","4","5","6","7","8","9","10","11","12","13","14"],
      [["I0 MUL (EX=3)","IF","ID","OF","EX","EX","EX","WO","","","","","",""],
       ["I1 DIV (EX=6)","","IF","ID","OF","st","st","st","EX","EX","EX","EX","EX","EX"],
       ["I2 ADD (EX=1)","","","IF","ID","st","st","st","st","st","st","OF","EX","WO",""],
       ["I3 SUB (EX=1)","","","","IF","ID","st","st","st","st","st","st","OF","EX","WO"]],
      widths=[1.35,0.34,0.34,0.34,0.34,0.34,0.34,0.34,0.34,0.34,0.34,0.34,0.34,0.34,0.34]))
    A(p("<b>Answer: ≈ 14 cycles.</b> Count the stalls caused by the 3-cycle multiply and 6-cycle divide "
      "before the dependent ADD can enter OF/EX, then the SUB after the ADD. The method matters more than the "
      "exact number — draw the table and count."))

    A(Paragraph("Q (ca27 · Q3a). Identify the RAW, WAR and WAW dependences in the sequence below.", ST['q']))
    A(formula("I1: R1 = 100\nI2: R1 = R2 + R4\nI3: R2 = R1 - 25\nI4: R4 = R1 + R3\nI5: R1 = R1 + 30"))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(table(["Type","Between","Register"],
      [["WAW","I1 → I2 (both write R1); I2 → I5 (both write R1)","R1"],
       ["RAW","I2 → I3 (I3 reads R1); I2 → I4 (I4 reads R1); I2 → I5 (I5 reads R1)","R1"],
       ["WAR","I2 → I1? (I1 writes R1 read by I2) — I2 → I3 reads R1 then I5 writes it: I3 → I5 WAR","R1"]],
      widths=[0.9,3.4,0.7]))
    A(p("Follow the data flow for RAW (later reader of R1 depends on the earlier writer) and repeated writes "
      "for WAW/WAR. All the action here is on R1."))


    A(Paragraph("Q (ca34 · Q1b). A five-stage pipeline (fetch, decode, execute, memory, write-back). All ops "
      "are 1 cycle except LW and SW (1+2) and branches (1+1). No forwarding. (a) Show the phases per clock for "
      "one loop iteration and how many cycles are lost to branch overhead. (b) If a static predictor recognises "
      "a backward branch in the Decode stage, how many cycles are wasted? (c) With a dynamic predictor, how "
      "many cycles are lost on a correct prediction?", ST['q']))
    A(Paragraph("<b>Solution.</b> (a) Use the same method as the loop question above: LW/SW occupy EX for two "
      "extra cycles and the branch one extra; with no forwarding each RAW stalls until write-back. (b) "
      "Recognising a <i>backward</i> branch in Decode lets the pipeline predict “taken” one stage earlier, so "
      "the wasted cycles drop by one (the branch resolves a stage sooner) — roughly halving the branch overhead "
      "from 2 to 1 cycle per iteration. (c) With a dynamic predictor and a <b>correct</b> prediction, "
      "<b>zero</b> cycles are lost — the pipeline continues down the correct path and never flushes.", ST['ans']))
    A(formula("Branch overhead: no prediction = 2 cycles/iter; static backward-branch (Decode) = 1 cycle/iter;\n"
              "dynamic correct prediction = 0 cycles/iter."))

    return F
