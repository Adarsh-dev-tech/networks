"""Part II — Instruction Set Architecture, ILP and Pipelining Fundamentals."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

def build():
    F=[]
    def A(x): F.extend(x if isinstance(x,list) else [x])

    # ============ 3. ISA ============
    A(PageBreak())
    A(h1(3,"Instruction Set Architecture: RISC vs CISC","The hardware/software contract"))
    A(p("The <b>Instruction Set Architecture (ISA)</b> is the complete set of instructions, registers, "
        "addressing modes and data types that a processor understands. It is the <i>interface</i> between "
        "hardware and software: the compiler targets the ISA, and the hardware implements it. Two programs "
        "written for the same ISA run on every processor of that family, no matter how differently the "
        "hardware is built."))
    A(h4("What the ISA fixes"))
    A(bullets([
      "<b>Instruction set</b> — which operations exist (add, load, branch …).",
      "<b>Data types</b> and their widths (integer 8/16/32/64-bit, IEEE floating point).",
      "<b>Registers</b> visible to the programmer and their count.",
      "<b>Addressing modes</b> — how an operand's address is computed (immediate, register, displacement …).",
      "<b>Encoding</b> — how instructions are laid out as bits (fixed vs variable length).",
    ]))

    A(h3("RISC vs CISC — the great divide"))
    A(p("In the 1970s-80s, instruction sets grew complex to make compilers easy and to close the "
        "“semantic gap” with high-level languages. These are <b>CISC</b> (Complex Instruction Set Computer) "
        "machines. Studies showed compilers rarely used most complex instructions, and complex instructions "
        "are hard to pipeline. The <b>RISC</b> (Reduced Instruction Set Computer) movement kept the "
        "instruction set small and regular so that each instruction executes in one cycle and the pipeline "
        "runs fast."))
    A(table(["Aspect","CISC","RISC"],
      [["Instruction count","Many; variable-length, complex","Few; fixed-length, simple"],
       ["Instructions per operation","One complex instruction does a lot","Several simple instructions"],
       ["CPI","High (many cycles per instruction)","Low — close to 1"],
       ["Clock rate","Lower","Higher (simple stages)"],
       ["Pipelining","Hard (variable work per instruction)","Easy (uniform work per stage)"],
       ["Registers","Few","Many (register–register model)"],
       ["Memory access","Many instructions may access memory","Only load/store access memory"],
       ["Control unit","Micro-programmed","Hard-wired"],
       ["Decoding","Complex","Simple and fast"],
       ["Compiler role","Hardware does much work","Compiler does much work (optimisation)"],
       ["Examples","x86, VAX","MIPS, ARM, RISC-V, SPARC"]],
      widths=[1.4,2.3,2.3]))
    A(callout("<b>Why RISC won the performance race:</b> a simple, regular instruction set lets you build a "
              "deep pipeline with a fast clock. <i>Loss of power in the instruction set is repaid in speed of "
              "the pipeline.</i> Modern x86 chips are CISC <i>outside</i> but decode into RISC-like "
              "micro-operations <i>inside</i> — the best of both.", 'tip'))

    A(h3("Addressing modes"))
    A(fig("page012.jpg", w=10.5*gen.cm, cap="RISC vs CISC characteristics compared (source: p. 12)."))
    A(p("<b>Reading the figure.</b> The RISC vs CISC comparison. RISC uses simple, fixed-length instructions and many registers with a load/store model; CISC uses complex, variable-length instructions often implemented with microcode. Count the differences — this table is a frequent short-answer question."))
    A(table(["Mode","Operand is…","Example (MIPS-style)"],
      [["Immediate","A constant inside the instruction","<font face='Mono'>addi r1,r2,4</font>"],
       ["Register","A register's contents","<font face='Mono'>add r1,r2,r3</font>"],
       ["Base + displacement","memory[base + const]","<font face='Mono'>lw r1,20(r2)</font>"],
       ["Register indirect","memory[register]","<font face='Mono'>lw r1,0(r2)</font>"],
       ["Indexed","memory[base + index]","<font face='Mono'>lw r1,(r2+r3)</font>"],
       ["PC-relative","memory[PC + const] — used for branches","<font face='Mono'>beq r1,r2,L</font>"]],
      widths=[1.5,2.6,1.9]))

    A(h3("Data representation: integers and IEEE 754 floating point"))
    A(p("The ISA also fixes how numbers are encoded, and the exam often asks about floating point. Know the "
        "three integer schemes and the IEEE 754 layout."))
    A(table(["Scheme","How a negative number is stored","Range (n bits)","Notes"],
      [["Sign-magnitude","Top bit is the sign; rest is magnitude.","−(2ⁿ⁻¹−1) … +(2ⁿ⁻¹−1)","Two zeros (+0, −0); awkward arithmetic."],
       ["One's complement","Flip every bit.","−(2ⁿ⁻¹−1) … +(2ⁿ⁻¹−1)","Still two zeros; end-around carry."],
       ["Two's complement","Flip every bit, then add 1.","−2ⁿ⁻¹ … +(2ⁿ⁻¹−1)","One zero; subtraction = addition; used everywhere."]],
      widths=[1.1,2.0,1.5,1.4]))
    A(p("<b>IEEE 754 single precision (32 bits)</b> stores a number as sign × 1.fraction × 2<sup>(exponent−bias)</sup>:"))
    A(formula("IEEE 754 single:  [ sign : 1 | exponent : 8 | fraction : 23 ]\n"
              "  Value = (−1)^sign × 1.fraction × 2^(exponent − 127)\n"
              "  Exponent bias = 127 ;  exponent 0 and 255 are reserved\n"
              "IEEE 754 double:  [ sign : 1 | exponent : 11 | fraction : 52 ], bias = 1023"))
    A(table(["Special case","Exponent","Fraction","Meaning"],
      [["Zero","all 0","all 0","±0"],
       ["Denormalised","all 0","non-zero","tiny numbers, no implicit leading 1"],
       ["Infinity","all 1","all 0","±∞ (e.g. divide by zero)"],
       ["NaN","all 1","non-zero","Not a Number (e.g. 0/0)"]],
      widths=[1.2,1.0,1.0,2.8]))
    A(p("<b>Example (also seen in the notes, p. 15):</b> represent 0.4 as a single-precision float."))
    A(formula("0.4 × 2 = 0.8 → 0 ; 0.8×2 = 1.6 → 1 ; 0.6×2 = 1.2 → 1 ; 0.2×2 = 0.4 → 0 ; 0.4×2 = 0.8 → 0 …\n"
              "0.4 = 0.011001100110011…₂ = 1.1001100110011…₂ × 2⁻²\n"
              "exponent = −2 + 127 = 125 = 01111101₂ ; fraction = 1001100110011… (23 bits)\n"
              "0.4 = 0 01111101 10011001100110011001100"))
    A(h3("Instruction-level parallelism (ILP) — the goal"))
    A(p("<b>ILP</b> is the number of independent operations the hardware can overlap in a pipeline. If "
        "instructions are independent, they can execute simultaneously. If they depend on one another, they "
        "must wait. Almost all of the rest of this guide is about <i>finding and exploiting ILP</i>."))
    A(table(["Technique","Static or dynamic","Idea"],
      [["Pipelining","Hardware (dynamic)","Overlap stages of consecutive instructions"],
       ["Superscalar","Dynamic","Issue &gt;1 instruction per cycle"],
       ["VLIW","Static (compiler)","Compiler packs independent ops into one long instruction"],
       ["Loop unrolling","Static (compiler)","Replicate the body to expose more independent work"],
       ["Scoreboarding / Tomasulo","Dynamic (hardware)","Issue out of order, resolve hazards in hardware"],
       ["Speculation (ROB)","Dynamic","Execute past branches / predicted paths safely"]],
      widths=[1.5,1.4,3.1]))

    A(h3("Dependences vs hazards — the key distinction"))
    A(p("A <b>dependence</b> is a property of the <i>program</i> (its meaning). A <b>hazard</b> is a "
        "property of the <i>pipeline</i> — a situation where overlapping would give the wrong answer. "
        "Dependences are fixed; hazards depend on the implementation and can sometimes be engineered away."))
    A(table(["Type","Symbol","Meaning","Can we remove it?"],
      [["True (data) dependence","RAW — Read After Write","Instruction j needs a value that instruction i "
        "produces. This is a <b>real</b> dependence.","<b>No</b> — must preserve the order (but can forward the value)."],
       ["Antidependence","WAR — Write After Read","j writes a location that i reads. j must not overwrite "
        "before i reads.","<b>Yes</b> — by register renaming."],
       ["Output dependence","WAW — Write After Write","i and j write the same location; the final value must "
        "come from the later one.","<b>Yes</b> — by register renaming."],
       ["Control dependence","branch","An instruction is executed only if a branch goes a certain way.","Reduce "
        "with prediction / speculation."]],
      widths=[1.5,1.3,2.7,1.5]))
    A(callout("<b>Memory hook:</b> <b>RAW is real</b> (True); WAR and WAW are <i>name</i> dependences — they "
              "exist only because two instructions happen to use the same register name, so renaming kills "
              "them. This is the single most examined distinction in the subject.", 'tip'))
    A(p("A worked example (used in PYQ ca1/ca22). Consider the loop:"))
    A(formula("A[i] = A[i] * B[i];   /* S1 */\n"
              "B[i] = A[i] + c;       /* S2 */\n"
              "A[i] = C[i] * c;       /* S3 */\n"
              "C[i] = D[i] * A[i];    /* S4 */"))
    A(table(["Dependence","Between","Type","Reason"],
      [["S1 → S2","S1 produces A[i], S2 reads A[i]","RAW (true)","Real data flow"],
       ["S1 → S3","S1 writes A[i], S3 writes A[i]","WAW (output)","Both write A[i]"],
       ["S3 → S4","S3 writes A[i], S4 reads A[i]","RAW (true)","Real data flow"],
       ["S2 → S3","S2 reads A[i], S3 writes A[i]","WAR (anti)","Name reuse"]],
      widths=[0.9,2.2,1.1,2.0]))
    A(p("<b>Renaming</b> removes the name dependences (WAW S1→S3 and WAR S2→S3) by giving S3 a fresh "
        "register, e.g. <font face='Mono'>A2[i] = C[i]*c</font>. The true dependences (S1→S2, S3→S4) stay."))

    # ---- PYQ ----
    A(h3("Previous-Year Questions — ISA, dependences & renaming"))
    A(Paragraph("Q (ca1 · Q2a / ca22 · Q2). Find all true, output and antidependences in the loop below and "
                "eliminate output dependences and antidependences by renaming.", ST['q']))
    A(formula("for (i = 0; i < 100; i++) {\n"
              "   A[i] = A[i] * B[i];   /* S1 */\n"
              "   B[i] = A[i] + c;      /* S2 */\n"
              "   A[i] = C[i] * c;      /* S3 */\n"
              "   C[i] = D[i] * A[i];   /* S4 */\n}"))
    A(Paragraph("<b>Solution.</b> Work through every pair of statements, asking “do they touch the same "
                "location, and in what order?”", ST['ans']))
    A(bullets([
      "<b>RAW (true) dependences</b> — a later statement <i>reads</i> what an earlier one <i>writes</i>:",
      "~S1 → S2: S1 writes A[i]; S2 reads A[i]. RAW on A[i].",
      "~S3 → S4: S3 writes A[i]; S4 reads A[i]. RAW on A[i].",
      "<b>WAW (output) dependence</b> — two statements write the same location:",
      "~S1 → S3: both write A[i]. The final value of A[i] must be S3's, so order matters.",
      "<b>WAR (antidependence)</b> — a later statement writes what an earlier one reads:",
      "~S2 → S3: S2 reads A[i]; S3 writes A[i]. S3 must not overwrite before S2 reads.",
    ]))
    A(p("<b>Renaming.</b> Give the “second writer” of A[i] a new name so no two live values share a "
        "register. S1 writes A[i] and S3 overwrites A[i] — rename S3's target to A2:"))
    A(formula("A[i]  = A[i] * B[i];   /* S1 : writes A[i]  */\n"
              "B[i]  = A[i] + c;      /* S2 : reads  A[i]  */\n"
              "A2[i] = C[i] * c;      /* S3 : writes A2[i] (renamed) */\n"
              "C[i]  = D[i] * A2[i];  /* S4 : reads  A2[i]  */"))
    A(p("After renaming, the WAW (S1→S3) and the WAR (S2→S3) disappear. The true dependences S1→S2 and "
        "S3→S4 remain because they carry real data. Renaming therefore removes <i>false</i> dependences "
        "only — it never removes a true dependence."))
    A(callout("<b>Exam tip:</b> list the statements, then for each later statement check every earlier one. "
              "You will always find the RAW pairs by following the data flow, and the WAW/WAR pairs by "
              "looking for repeated register names.", 'tip'))

    A(Paragraph("Q (ca2 · Qb). Consider the loop below. Are there dependences between S1 and S2? Is the loop "
                "parallel? If not, show how to make it parallel.", ST['q']))
    A(formula("for (i = 0; i < 100; i++) {\n"
              "   A[i] = A[i] + B[i];   /* S1 */\n"
              "   B[i+1] = C[i] + y[i]; /* S2 */\n}"))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "Look at the <i>subscripts</i>, not just the array names. S1 writes <font face='Mono'>A[i]</font> and "
      "reads <font face='Mono'>A[i], B[i]</font>. S2 writes <font face='Mono'>B[i+1]</font> and reads "
      "<font face='Mono'>C[i], y[i]</font>.",
      "S1 writes <b>B[i]</b>; S2 writes <b>B[i+1]</b>. For the same <i>i</i> these are different elements, so "
      "there is <b>no</b> dependence between S1 and S2 in the same iteration.",
      "But across iterations: S1 in iteration i writes B[i], and S2 in iteration i−1 writes B[i]. Both write "
      "B[i] (different iterations) — a <b>WAW loop-carried output dependence</b> on B[i]. There is no RAW "
      "involving B because S1 never <i>reads</i> B[i+1] and S2 never reads B[i].",
      "So the only cross-iteration dependence is the output dependence on B between S1 of iteration i and S2 "
      "of iteration i−1.",
    ]))
    A(p("<b>Is it parallel?</b> The loop is <b>not</b> fully parallel as written, because the two statements "
        "write overlapping B elements across iterations. <b>Fix:</b> rename the B array written by S2 into a "
        "separate array B2, so the two writers no longer collide:"))
    A(formula("for (i = 0; i < 100; i++) {\n"
              "   A[i]    = A[i] + B[i];   /* S1 */\n"
              "   B2[i+1] = C[i] + y[i];   /* S2 : renamed output */\n}"))
    A(p("Now S1 writes A/B and S2 writes B2 — no overlap — so every iteration is independent and the loop "
        "can be executed in parallel."))

    # ============ 4. DEPENDABILITY ============
    A(PageBreak())
    A(h1(4,"Dependability & Reliability","MTTF, MTTR, availability and how to keep a farm alive"))
    A(p("A system is <b>dependable</b> if it keeps delivering correct service. Dependability has two big "
        "ingredients: <b>reliability</b> (how long until something fails) and <b>availability</b> (what "
        "fraction of time the service is up). These are measured with a small set of times that appear in "
        "the exam."))
    A(table(["Term","Symbol","Meaning"],
      [["Mean Time To Failure","MTTF","Average time from the start (or a repair) until the next failure. Measures <i>reliability</i>."],
       ["Mean Time To Repair","MTTR","Average time to fix a failure and restore service."],
       ["Mean Time Between Failures","MTBF","MTBF = MTTF + MTTR — average time between two consecutive failures."],
       ["Availability","A","Fraction of time the system is usable."],
       ["Failure Rate","λ","Failures per unit time; λ = 1 / MTTF."]],
      widths=[1.7,0.8,3.5]))
    A(formula("Availability A = MTTF / (MTTF + MTTR) = MTTF / MTBF\n"
              "Failure rate  λ = 1 / MTTF"))
    A(p("<b>Derivation of availability.</b> In one failure–repair cycle the system is up for MTTF and down "
        "for MTTR, so the fraction of time it is up is MTTF / (MTTF + MTTR). A system with MTTF = 1,000,000 h "
        "and MTTR = 1 h has A = 10⁶/(10⁶+1) ≈ 0.999999 — “six nines”."))
    A(h3("Reliability of a whole system"))
    A(p("If a system is made of many components, its failure rate is the <i>sum</i> of the component failure "
        "rates (for independent components that each must work):"))
    A(formula("1 / MTTF<sub>system</sub> = Σ (1 / MTTF<sub>i</sub>)\n"
              "So MTTF<sub>system</sub> = 1 / (1/MTTF₁ + 1/MTTF₂ + …)"))
    A(callout("<b>Why server farms still work:</b> 10,000 computers each with MTTF = 35 days fail often as a "
              "whole, but if the service tolerates losing a third of them, the <i>service</i> MTTF is far "
              "longer than any one machine. Adding components lowers whole-system MTTF but can raise "
              "availability if failures are masked by redundancy. (See PYQ ca30.)", 'tip'))
    A(h3("4.1 Exam-relevant insights"))
    A(bullets([
      "A is a fraction; multiply by 100 for a percentage, or count “nines” for SLA language.",
      "λ = 1/MTTF, so halving MTTF doubles the failure rate.",
      "For <i>series</i> reliability (all must work) add failure rates.",
      "For <i>parallel</i> redundancy (only one must work) availability rises.",
    ]))


    A(h3("4.2 Worked reliability examples (notes pp. 24-27)"))
    A(p("<b>Q1 (p. 25).</b> MTTF = 100 hours, MTTR = 36 hours. Find MTBF and the availability."))
    A(formula("MTBF = MTTF + MTTR = 100 + 36 = 136 h" + chr(10) +
              "A = MTTF / MTBF = 100 / 136 = 0.735 = 73.5%"))
    A(p("<b>Q2 (p. 25).</b> A hard drive fails after 5000 hours of use on average. Over two years "
        "(≈ 2 × 8760 = 17520 h) with replacement, how many failures are expected, and what is the failure rate?"))
    A(formula("Failures = 17520 / 5000 ≈ 3.5 failures in two years" + chr(10) +
              "Failure rate λ = 1 / MTTF = 1 / 5000 h = 2 × 10⁻⁴ per hour"))
    A(p("<b>Q3 (p. 26).</b> A web service runs on two identical servers in parallel (redundant). Each has "
        "MTTF = 2 months. What is the MTTF of the pair, and does redundancy raise or lower it?"))
    A(formula("For n components that must ALL work (series):" + chr(10) +
              "  1/MTTF_sys = Σ 1/MTTF_i  →  MTTF_sys = MTTF/n = 2/2 = 1 month (LOWER)" + chr(10) +
              "For redundancy where only ONE must work (parallel): the pair fails only if BOTH fail," + chr(10) +
              "  so availability RISES: A_sys = 1 − (1 − A)²"))
    A(callout("<b>Read the question carefully.</b> “MTTF of the system” (all must work) gets <i>worse</i> as "
              "you add components — failure rates add. But “availability / service uptime” (redundancy) gets "
              "<i>better</i>, because one failure is masked. The notes stress this distinction (pp. 24-26).", 'tip'))
    A(p("<b>Q4 (p. 27).</b> MTTF = 936 hours and availability A = 0.99. Find the unavailability and MTTR."))
    A(formula("Unavailability = 1 − A = 1 − 0.99 = 0.01" + chr(10) +
              "A = MTTF/(MTTF+MTTR)  →  MTTR = MTTF × (1−A)/A = 936 × 0.01/0.99 ≈ 9.45 h"))

    A(h3("Previous-Year Questions — Dependability"))
    A(Paragraph("Q (ca10 · Q2). Convert the C code below to MIPS, find the hazards, and reorder to avoid "
      "stalls.", ST['q']))
    A(formula("A = B + E;\nC = B + F;"))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("lw  $t0, B        # $t0 = B\nlw  $t1, E        # $t1 = E\nadd $t2, $t0, $t1  # A = B + E\n"
              "sw  $t2, A\nlw  $t3, F        # $t3 = F\nadd $t4, $t0, $t3  # C = B + F\nsw  $t4, C"))
    A(bullets([
      "<b>Hazards:</b> the <font face='Mono'>add $t2,$t0,$t1</font> depends on the two loads (RAW, load-use); "
      "the second add reuses $t0 (B) which is already loaded (no new hazard).",
      "<b>Reorder:</b> hoist the independent <font face='Mono'>lw $t3,F</font> above the first add so the "
      "load-use slot is filled:",
    ]))
    A(formula("lw  $t0, B\nlw  $t1, E\nlw  $t3, F        ; independent load fills the slot\n"
              "add $t2, $t0, $t1\nsw  $t2, A\nadd $t4, $t0, $t3\nsw  $t4, C"))

    return F
