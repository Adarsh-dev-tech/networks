"""Part I — Foundations, ISA and Performance."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

def build():
    F=[]
    def A(x):
        F.extend(x if isinstance(x,list) else [x])

    # ================= 1. INTRODUCTION =================
    A(h1(1,"Introduction to Computer Architecture","What the subject is about; architecture vs organization"))
    A(p("<b>Computer Architecture</b> is the study of how a computer is designed and built, at the level "
        "where a programmer can still see the machine. The subject sits on the boundary between hardware "
        "and software: it decides what the hardware exposes to the compiler, and how the hardware is "
        "organised internally to make that exposed interface fast and cheap."))
    A(p("Every computer, from a watch to a supercomputer, is a <b>stored-program machine</b> (von Neumann "
        "model): a processor reads instructions from memory, executes them one after another, and writes "
        "results back. The instructions and the data live in the same memory, which is why the model is "
        "called <i>stored-program</i>."))

    A(h3("Architecture vs Organization"))
    A(p("These two terms are used constantly in the exam, and they are <i>not</i> the same. A useful way "
        "to remember the difference: <b>architecture</b> answers “<i>what</i> does the machine do?”, "
        "while <b>organization</b> answers “<i>how</i> is it built?”."))
    A(table(["Attribute","Computer Architecture (what)","Computer Organization (how)"],
      [["Level","High-level / logical view","Low-level / physical view"],
       ["Decides","Instruction set, data types, addressing modes, registers visible to the programmer",
        "Data paths, control signals, memory technology, clock, buses, cache hardware"],
       ["Sees","Only the ISA (instruction set architecture)","The whole hardware implementation"],
       ["Example","Does the ISA have a floating-point multiply instruction?",
        "Is the FP multiplier built from one unit or pipelined across several stages?"],
       ["Impact","A program written for the architecture runs on all machines with that architecture",
        "Different organizations of the same architecture can have very different speeds and costs"],
       ["Same for all?","Yes — architecture is fixed for a family (e.g. x86, MIPS, RISC-V)",
        "No — organization changes every generation"]],
      widths=[1.1,2.6,2.6]))
    A(callout("<b>Exam line to remember:</b> Architecture is <i>programmer-visible</i> and changes slowly; "
              "organization is <i>transparent to the programmer</i> and changes with technology.", 'tip'))

    A(h3("The stored-program computer: the classic block diagram"))
    A(p("The von Neumann machine has five classic units: the <b>control unit</b> (decides what to do), the "
        "<b>arithmetic-logic unit / ALU</b> (does the arithmetic), the <b>memory</b> (stores programs and data), "
        "and <b>input/output</b> devices. Registers (PC, IR, MAR, MDR, general-purpose registers) sit inside "
        "the CPU. The CPU repeatedly performs the <b>fetch-decode-execute</b> cycle."))
    A(fig("page002.jpg", w=11.5*gen.cm, cap="Von Neumann (stored-program) organisation and the fetch–decode–execute cycle (source: lecture notes, p. 2)."))
    A(p("<b>Reading the figure.</b> Read this diagram as the whole subject in miniature: the CPU fetches an instruction from the shared memory, decodes it, executes it in the ALU and writes the result back — the stored-program cycle. Notice that code and data share one memory and one bus, which is why it is called <i>stored-program</i> and why the single bus is a bottleneck."))
    A(table(["Unit","Role"],
      [["Control Unit (CU)","Fetches the instruction, decodes it and generates control signals so every other unit acts in the right order."],
       ["ALU","Performs arithmetic (add, multiply) and logic (AND, OR, compare) operations."],
       ["Registers","Very fast on-chip storage. PC = program counter, IR = instruction register, MAR/MDR = memory address/data registers."],
       ["Memory","Holds both the program and its data; addressed by location."],
       ["I/O","Moves data in and out (keyboard, disk, network)."]],
      widths=[1.3,4.7]))

    A(h3("Von Neumann vs Harvard — one memory or two?"))
    A(p("The classic von Neumann machine keeps instructions and data in the <b>same</b> memory and reaches "
        "them through a <b>single</b> bus. The <b>Harvard</b> architecture instead has <b>two separate "
        "memories</b> (and two buses) — one for instructions, one for data — so a fetch and a data access "
        "can happen in the same cycle."))
    A(table(["Aspect","Von Neumann (Princeton)","Harvard"],
      [["Memory","One shared memory for code and data","Two separate memories (instruction + data)"],
       ["Buses","One shared bus","Separate instruction and data buses"],
       ["Bottleneck","The single bus is the “von Neumann bottleneck”","No instruction/data conflict"],
       ["Advantage","Simple, flexible; code and data can share space","Faster (parallel fetch and data access)"],
       ["Used in","General-purpose CPUs (program stored in RAM)","Most embedded/DSP chips; modern CPUs use a split L1 (Harvard-style I-cache + D-cache)"]],
      widths=[1.0,2.6,2.6]))
    A(callout("<b>Exam link:</b> a split Level-1 cache (separate instruction and data caches) is the Harvard "
              "idea applied inside a von Neumann CPU; it removes the structural hazard of a single memory "
              "port and is why L1 hit time can be one cycle."))

    A(h3("Flynn's taxonomy — how machines handle instruction/data streams"))
    A(fig("page006.jpg", w=10.5*gen.cm, cap="Flynn's taxonomy: SISD, SIMD, MISD, MIMD (source: p. 6)."))
    A(p("<b>Reading the figure.</b> Notice the four quadrants. SISD (one instruction, one datum) is the scalar CPU; SIMD (one instruction, many data) is the vector/GPU idea; MIMD (many instructions, many data) is the multicore idea; MISD (many instructions, one datum) is only theoretical."))
    A(p("A computer processes two streams: an <b>instruction stream</b> and a <b>data stream</b>. Depending "
        "on whether each stream is single or multiple, Michael Flynn classified all computers into four "
        "types. This classification appears in almost every exam."))
    A(table(["Class","Full name","Meaning","Examples"],
      [["SISD","Single Instruction, Single Data","One instruction works on one piece of data at a time — the classic scalar uniprocessor.","Old PCs, classic CPU"],
       ["SIMD","Single Instruction, Multiple Data","One instruction is applied to many data elements in parallel. Vector/array processors and GPU threads.","Vector processors, GPUs, SSE/AVX"],
       ["MISD","Multiple Instruction, Single Data","Several instructions act on the same data (rare; mostly theoretical).","Fault-tolerant arrays (rare)"],
       ["MIMD","Multiple Instruction, Multiple Data","Independent processors run independent instruction and data streams.","Multicore CPUs, clusters"]],
      widths=[0.7,1.7,2.6,1.4]))
    A(callout("<b>Why it matters:</b> SIMD is the basis of vector processors and GPUs (Topic 19). "
              "MIMD is the basis of multicore and shared-memory multiprocessors (Topics 16–18)."))
    A(h3("Multithreading — many threads on one core"))
    A(p("A single core often stalls (waiting for memory or a cache miss). <b>Multithreading</b> lets one "
        "core hold several threads at once and switch to another when one stalls, so the functional units "
        "stay busy. There are three classic flavours."))
    A(table(["Type","How it switches","Key idea"],
      [["Fine-grained (interleaved)","Every clock cycle, round-robin between threads","Hides short stalls; needs many threads; each thread runs slowly"],
       ["Coarse-grained","Switch only on a long stall (e.g. a cache miss)","Cheap to add; the new thread needs time to refill its pipeline"],
       ["Simultaneous multithreading (SMT)","Issue instructions from several threads in the <i>same</i> cycle","Best use of a superscalar core's issue slots; appears as “hyper-threading”"]],
      widths=[1.5,2.2,2.3]))
    A(callout("<b>Distinguish carefully:</b> <i>multithreading</i> = several threads on one core (SMT); "
              "<i>multicore/CMP</i> = several cores on one chip; <i>multiprocessor</i> = several chips in one "
              "system. SMT exploits thread-level parallelism (TLP) inside a core to hide latency.", 'tip'))


    A(h3("Program execution at the instruction level"))
    A(p("A program is a sequence of instructions. Each instruction passes through a series of steps. In the "
        "simplest single-cycle machine every step happens in one clock period. In practice we break the work "
        "into <b>stages</b> so several instructions can overlap — this is pipelining (Topic 5)."))
    A(bullets([
      "<b>Fetch</b> — read the instruction at address PC from memory; increment PC.",
      "<b>Decode</b> — work out what the instruction means and which registers it needs.",
      "<b>Execute</b> — perform the operation in the ALU.",
      "<b>Memory</b> — access data memory (only for load/store).",
      "<b>Write-back</b> — store the result in a register.",
    ]))
    A(callout("<b>Key idea of the whole subject:</b> almost every technique in this guide — pipelining, "
              "caches, branch prediction, out-of-order execution — exists to keep the processor busy and to "
              "hide the fact that memory and operations take many cycles.", 'tip'))

    # ================= 2. PERFORMANCE & AMDAHL =================
    A(PageBreak())
    A(h1(2,"Measuring Performance: CPU Time, CPI, MIPS & Amdahl's Law","The single most examined numerical topic"))
    A(p("Performance is about <i>time</i>. The only true measure of a computer's speed is how long a real "
        "program takes to run. But to reason about <i>why</i> one machine is faster, we break that time into "
        "parts we can measure and change. This section builds the performance equation from scratch, because "
        "almost every numerical question in the papers uses it."))

    A(h3("2.1 Response time vs throughput"))
    A(table(["Concept","Definition","How you improve it"],
      [["Response (execution) time","Time between the start and the completion of one task.","Faster clock, lower CPI, fewer instructions."],
       ["Throughput","Total work done per unit time (e.g. tasks per second).","More cores / more parallelism, better overlap (pipelining)."]],
      widths=[1.3,3.2,2.0]))
    A(callout("<b>Classic distinction:</b> adding processors usually improves throughput but not the response "
              "time of a single task. Pipelining improves throughput without shortening the latency of one task."))

    A(h3("2.2 The performance equation (the master formula)"))
    A(p("A program's execution time depends on three things, and they multiply:"))
    A(formula("CPU Time = Instruction Count (IC) × CPI × Clock Cycle Time\n"
              "CPU Time = (IC × CPI) / Clock Frequency"))
    A(table(["Term","Meaning","Units"],
      [["IC (Instruction Count)","Number of instructions the program executes.","instructions"],
       ["CPI","Average <b>Cycles Per Instruction</b> = total cycles / IC.","cycles per instruction"],
       ["Clock Cycle Time (CCT)","Duration of one clock period, CCT = 1 / f.","seconds (or ns)"],
       ["Clock Frequency (f)","Number of cycles per second.","Hz (GHz = 10<sup>9</sup> Hz)"]],
      widths=[1.7,3.5,1.3]))
    A(p("Because different instruction types cost different numbers of cycles, the <b>average CPI</b> is a "
        "weighted average of the CPI of each class:"))
    A(formula("CPI = Σ (CPIᵢ × Fᵢ) ,   where Fᵢ = fraction (or share) of instructions of class i,  Σ Fᵢ = 1\n"
              "Equivalently  CPI = (Σ CPIᵢ × countᵢ) / IC"))

    A(h3("2.3 Deriving the equation (why it is a product)"))
    A(fig("page028.jpg", w=10.5*gen.cm, cap="CPU-time and CPI worked examples from the lecture notes (source: p. 28)."))
    A(p("<b>Reading the figure.</b> These are the worked CPU-time examples from the notes. Follow how IC, CPI and clock period multiply to give total time, and how the instruction mix turns into an average CPI — this is exactly the calculation the paper asks for."))
    A(p("Suppose a program has <i>IC</i> instructions. On average each instruction takes <i>CPI</i> clock "
        "cycles. So the total number of clock cycles is <i>IC × CPI</i>. Each cycle lasts <i>CCT</i> seconds. "
        "Multiplying gives the total time. This is why the three factors are independent levers: you can "
        "reduce any one of them to speed up the program."))
    A(callout("<b>Trap:</b> reducing instruction count may raise CPI (e.g. CISC), and raising clock speed may "
              "raise CPI (deeper pipeline). The three factors are <i>not</i> independent in real designs.", 'warn'))

    A(h3("2.4 MIPS — million instructions per second"))
    A(formula("MIPS = IC / (Execution Time × 10⁶) = f / (CPI × 10⁶)"))
    A(p("<b>MIPS</b> measures how many millions of instructions are executed each second. It is easy to quote "
        "but dangerous to trust, because:"))
    A(bullets([
      "It does not account for what an instruction does — a machine with tiny instructions looks fast.",
      "It varies between programs on the same machine (different instruction mixes).",
      "It ignores I/O and memory behaviour.",
      "It can be used only to compare machines with the <i>same</i> ISA.",
    ]))
    A(callout("<b>Memory hook:</b> MIPS is <i>meaningless</i> across different ISAs. Use CPU time for fair "
              "comparisons. (This is exactly the point of PYQ ca1/ca19.)", 'warn'))

    A(h3("2.5 Speed-up and Amdahl's Law"))
    A(fig("page019.jpg", w=10.0*gen.cm, cap="Deriving Amdahl's law and the effect of the serial part (source: p. 19)."))
    A(p("<b>Reading the figure.</b> The derivation of Amdahl's law. The time is split into the enhanced fraction <i>f</i> and the unenhanced fraction (1−f). As the enhancement factor <i>k</i> grows, the speed-up saturates at 1/(1−f) — the serial part sets the ceiling."))
    A(p("Amdahl's Law answers: <i>“If I speed up part of the machine, how much faster does the whole program "
        "get?”</i> The answer is limited by the part you did <b>not</b> speed up."))
    A(formula("Speed-up S = Old execution time / New execution time = T<sub>old</sub> / T<sub>new</sub>\n"
              "Amdahl:  S = 1 / [ (1 − f) + f / k ]\n"
              "   f = fraction of the original time that is enhanced (0 ≤ f ≤ 1)\n"
              "   k = speed-up of the enhanced portion (k &gt; 1)"))
    A(p("<b>Derivation.</b> Let the original time be 1 unit. The enhanced fraction <i>f</i> is sped up by a "
        "factor <i>k</i>, so it now takes <i>f/k</i>. The unenhanced fraction (1 − f) is unchanged. The new "
        "total time is (1 − f) + f/k. The speed-up is the ratio of old to new: 1 / [(1 − f) + f/k]."))
    A(h3("2.6 The ceiling: the serial fraction limits everything"))
    A(p("As k → ∞ (the enhanced part becomes infinitely fast), the speed-up tends to a hard ceiling:"))
    A(formula("Maximum speed-up = 1 / (1 − f)   as k → ∞\n"
              "If 10% of the code cannot be parallelised (1 − f = 0.1), the maximum speed-up is 1/0.1 = 10× — "
              "no matter how many processors you add."))
    A(callout("<b>Interpreting f:</b> in parallel-speedup problems, f is the <i>parallelisable fraction</i> and "
              "k is the <i>number of processors</i> P. Then S = 1 / [(1 − f) + f/P].", 'tip'))

    A(h3("2.7 Amdahl with a slowdown elsewhere (trade-off version)"))
    A(fig("page020.jpg", w=10.5*gen.cm, cap="Deriving the performance/Amdahl relationships from first principles (source: p. 20)."))
    A(p("<b>Reading the figure.</b> The same algebra written out for the general case, showing why a fixed serial fraction caps the achievable speed-up no matter how much you improve the parallel part."))
    A(p("Real design changes can slow down <i>other</i> parts. If enhancing one part speeds it by k₁ but "
        "slows another fraction by k₂ (k₂ &lt; 1 means slower), extend the law to add the slowed fraction:"))
    A(formula("T<sub>new</sub> = (1 − f₁ − f₂) + f₁/k₁ + f₂/k₂ ,   S = 1 / T<sub>new</sub>\n"
              "f₁ = fraction enhanced, k₁ = its speed-up;  f₂ = fraction slowed, k₂ = its speed factor"))
    A(p("After the change, the <b>new share</b> of a component is its new time divided by the new total time. "
        "The relative importance of components shifts, which is why a second enhancement may be less "
        "valuable than it first appears (PYQ ca36)."))

    A(h3("2.8 Mean performance and benchmarks"))
    A(table(["Mean","Formula","When to use"],
      [["Arithmetic mean","(1/n) Σ Tᵢ","When timing equal work (total time matters)."],
       ["Harmonic mean","n / Σ (1/Rᵢ)","For rates such as MIPS or FPS — the correct average of rates."],
       ["Geometric mean","(Π Rᵢ)<sup>1/n</sup>","For normalised ratios (SPEC) — the only mean that gives the same result when you change the reference machine."]],
      widths=[1.2,2.1,3.2]))
    A(callout("<b>Exam rule:</b> average <i>times</i> with the arithmetic mean, average <i>rates</i> with the "
              "harmonic mean, and average <i>normalised ratios</i> with the geometric mean.", 'tip'))

    A(h3("2.9 Quantitative principles of design"))
    A(p("A handful of principles explain almost every design decision in the subject. Examiners like to ask "
        "for these by name."))
    A(table(["Principle","Meaning","Where you see it"],
      [["Make the common case fast","Optimise what happens most often.","Small instructions, fast ALU path, cache for the common access"],
       ["Amdahl's law","Speed-up is limited by the unenhanced part.","Deciding which component to improve"],
       ["Locality","Programs reuse data and instructions that are near each other.","Caches, TLBs, prefetching"],
       ["Parallelism","Do independent work at the same time.","Pipelining, superscalar, multicore, vector/SIMD"]],
      widths=[1.4,2.6,2.0]))
    A(h3("2.10 Design constraints: power, thermal and the multicore shift"))
    A(p("For decades, transistor size shrank (Moore's law) and Dennard scaling kept power density constant, so "
        "clock speeds rose every generation. Dennard scaling ended around 2005: power density started rising "
        "with each shrink, so clock frequency could no longer increase freely. Designers turned to "
        "<b>multicore</b> (more cores at moderate frequency) and to power-aware techniques instead."))
    A(table(["Constraint","Effect on design"],
      [["Power (dynamic)","P ∝ C·V²·f — reducing voltage is the biggest lever."],
       ["Power (static/leakage)","Rises as transistors shrink; limits how low voltage can go."],
       ["Thermal","Heat must be removed; limits sustained frequency (and motivates throttling)."],
       ["Energy","Battery life and cost; motivates DVFS (dynamic voltage/frequency scaling)."],
       ["Multicore shift","Instead of a faster single core, put more cores on the chip."]],
      widths=[1.6,4.4]))
    A(h3("2.9 Exam-relevant insights"))
    A(bullets([
      "<b>Never</b> compare MIPS across ISAs; compare CPU time.",
      "CPI is an <i>average</i> — always weight by the fraction of each instruction class.",
      "Amdahl's Law always has the form 1 / (unimproved + improved). Identify f first, then plug in.",
      "Speed-up = old/new; “X% faster” means new = old/(1+X/100).",
      "Watch units: GHz = 10⁹ Hz; convert cycles to time with CCT = 1/f.",
      "A “65% improvement” in AMAT means the new AMAT is 35% of the old (see PYQ ca15/ca26).",
    ]))
    A(callout("<b>Common mistake:</b> in Amdahl problems, students speed up the wrong fraction. Read the "
              "question twice and write down f and k explicitly before computing.", 'warn'))


    A(h3("Previous-Year Questions — Performance & Amdahl"))
    A(Paragraph("Q (ca3 · Q2). Derive and explain Amdahl's law.", ST['q']))
    A(Paragraph("<b>Solution.</b> Let a program take time T. A fraction f of that time can be enhanced; "
      "the enhancement makes that fraction k times faster. The unenhanced part (1−f)T is unchanged. New time "
      "= (1−f)T + (fT)/k. Speed-up S = T / new time = 1/[(1−f) + f/k]. As k→∞, S→1/(1−f): the serial part "
      "sets the ceiling.", ST['ans']))
    A(formula("T_new = (1−f)T + (fT)/k ;   S = 1 / [(1−f) + f/k] ;   S_max = 1/(1−f)"))

    A(Paragraph("Q (ca4 · Q1). A program has a portion enhanced to run 4× faster, giving a system speed-up "
      "of 3.3×. What is the fraction enhanced?", ST['q']))
    A(formula("3.3 = 1/[(1−f) + f/4]  →  0.3030 = (1−f) + 0.25f = 1 − 0.75f\n"
              "0.75f = 0.6970  →  f = 0.929  = 92.9%"))
    A(Paragraph("<b>Answer: f ≈ 92.9%</b> of the original time must be in the enhanced portion.", ST['ans']))

    A(Paragraph("Q (ca4 · Q2). A quad-core could speed up a computer by 4×, but rarely does. Use Amdahl to "
      "find the percentage of execution that must be parallelised for overall speed-ups of 3, 2, 1.5, 1.25.", ST['q']))
    A(formula("S = 1/[(1−f) + f/4].  Solve for f:  f = 4(S−1) / (3S).\n"
              "S=3   → f = 4(2)/(9)   = 0.889  = 88.9%\n"
              "S=2   → f = 4(1)/(6)   = 0.667  = 66.7%\n"
              "S=1.5 → f = 4(0.5)/4.5 = 0.444  = 44.4%\n"
              "S=1.25→ f = 4(0.25)/3.75= 0.267  = 26.7%"))
    A(Paragraph("<b>Answer:</b> to gain 3× you must parallelise ~88.9%; for 2× ~66.7%; for 1.5× ~44.4%; for "
      "1.25× ~26.7%. Notice how quickly the required parallel fraction grows.", ST['ans']))

    A(Paragraph("Q (ca4 · Q3). A benchmark: 39% loads, 12% stores, 28% ALU, 6% multiplies, 2% divides, 10% "
      "conditional branches, 3% unconditional branches. CPIs: loads/stores 5, ALU 3, multiply 6, divide 15, "
      "branch 4. Which single ALU enhancement is best?", ST['q']))
    A(formula("CPI_base = 0.39(5)+0.12(5)+0.28(3)+0.06(6)+0.02(15)+0.13(4)\n"
              "         = 1.95 + 0.60 + 0.84 + 0.36 + 0.30 + 0.52 = 4.57\n"
              "(a) cond-branch CPI→2 : ΔCPI = 0.10×(4−2) = 0.20 → new 4.37\n"
              "(b) multiply CPI→3   : ΔCPI = 0.06×(6−3) = 0.18 → new 4.39\n"
              "(c) divide CPI→7     : ΔCPI = 0.02×(15−7)= 0.16 → new 4.41\n"
              "(d) ALU CPI→2        : ΔCPI = 0.28×(3−2) = 0.28 → new 4.29"))
    A(Paragraph("<b>Answer: (d)</b> — improving the ALU (non-multiply/divide) gives the largest CPI "
      "reduction (0.28), because ALU operations are the most frequent.", ST['ans']))

    A(Paragraph("Q (ca5 · Q4 / ca19 · Q1). MIPS ISA at 500 MHz: ALU 3 cycles, branch/jump 2, sw 4, lw 5. A "
      "program executes 200M ALU, 55M branch/jump, 25M sw and 20M lw. Find the CPU time.", ST['q']))
    A(formula("IC = 200M + 55M + 25M + 20M = 300M instructions\n"
              "Total cycles = 200M×3 + 55M×2 + 25M×4 + 20M×5\n"
              "             = 600M + 110M + 100M + 100M = 910M cycles\n"
              "T_clock = 1/500 MHz = 2 ns\n"
              "CPU time = 910M × 2 ns = 1820 ms = 1.82 s"))
    A(Paragraph("<b>Answer: CPU time = 1.82 s</b> (CPI = 910M/300M ≈ 3.03).", ST['ans']))

    A(Paragraph("Q (ca7 · Q1a). Amdahl with communication overhead. (a) Speed-up with 8 processors if, for "
      "every processor added, communication overhead is 0.5% of the original execution time. (b) Speed-up "
      "with N processors if, each time the number of processors doubles, the overhead increases by 0.5%.", ST['q']))
    A(formula("(a) With P processors, serial part s, parallel part (1−s), plus overhead 0.5%×(P−1):\n"
              "    T_new = s + (1−s)/P + 0.005(P−1)   (times the original time)\n"
              "    For P=8: S = 1 / [ s + (1−s)/8 + 0.005×7 ] = 1/[ s + (1−s)/8 + 0.035 ]\n"
              "    (substitute the given serial fraction s).\n"
              "(b) With N processors, overhead = 0.005×log₂N:\n"
              "    S(N) = 1 / [ s + (1−s)/N + 0.005·log₂N ]"))
    A(Paragraph("<b>Idea being tested:</b> communication overhead grows with the number of processors, so "
      "speed-up saturates and can even fall — this is the practical limit Amdahl's plain form ignores.", ST['ans']))

    A(Paragraph("Q (ca33 · Q1). Three modification versions affect components X, Y, Z whose execution-time "
      "fractions are 30%, 45%, 25%. Given each version's speed factors, find the overall speed-up of each and "
      "rank them.", ST['q']))
    A(formula("S_version = 1 / [ 0.30/k_X + 0.45/k_Y + 0.25/k_Z ]\n"
              "(read k_X,k_Y,k_Z from the table for each version; k<1 means slower)"))
    A(Paragraph("<b>Method:</b> evaluate the weighted sum for each version, take the reciprocal, then rank "
      "from largest S. A component that is slowed (k<1) increases its term and can pull S below 1.", ST['ans']))

    A(Paragraph("Q (ca36 · Q1a). (i) A new FP unit speeds FP by 2×; FP is 20% of execution time — overall "
      "speed-up? (ii) The change also slows data-cache accesses by 1.5× (2/3 speed-up); data-cache accesses "
      "are 10% of time — overall speed-up now? (iii) What % of the new execution time is FP, and what % is "
      "data cache?", ST['q']))
    A(formula("(i) S = 1/[(1−0.20) + 0.20/2] = 1/[0.80 + 0.10] = 1/0.90 = 1.111  (≈11.1% faster)\n"
              "(ii) now also slow 10% by factor 2/3:\n"
              "     T_new = (1 − 0.20 − 0.10) + 0.20/2 + 0.10/(2/3)\n"
              "           = 0.70 + 0.10 + 0.15 = 0.95  →  S = 1/0.95 = 1.053\n"
              "(iii) new shares: FP = 0.10/0.95 = 10.5% ; data cache = 0.15/0.95 = 15.8%"))
    A(Paragraph("<b>Answer:</b> (i) 1.11×; (ii) 1.05× (the cache slowdown eats most of the gain); (iii) FP "
      "≈ 10.5%, data cache ≈ 15.8% of the new time.", ST['ans']))

    A(Paragraph("Q (ca36 · Q1b). Vector hardware makes a computation 10× faster; the measured vectorisation "
      "is 70%. What vectorisation would be needed to equal a further 2× speed-up of the vector unit (i.e. 20× "
      "total)?", ST['q']))
    A(formula("Current:  S = 1/[(1−0.7) + 0.7/10] = 1/[0.30 + 0.07] = 1/0.37 = 2.703\n"
              "Target  :  a 2× faster vector unit gives 20× on the vector part:\n"
              "           S' = 1/[(1−f) + f/20].  Set S' = 2.703\n"
              "           0.37 = (1−f) + f/20 = 1 − 0.95f  →  0.95f = 0.63  →  f = 0.663 = 66.3%"))
    A(Paragraph("<b>Answer:</b> the compiler team would need only ≈66.3% vectorisation (actually <i>less</i> "
      "than the current 70%) — meaning the current vectorisation already beats the proposed 2× hardware "
      "speed-up. State the comparison explicitly.", ST['ans']))

    return F
