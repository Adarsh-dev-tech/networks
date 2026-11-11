"""Page-by-page annotations for handwritten pages 17-33."""

PAGES = {}

PAGES[17] = dict(
 title="Systolic arrays in detail; interconnection cost; thermal design and multicore",
 transcript="""Systolic array:
  (a grid of PEs; data flows in, results flow out)
  Development of the systolic array idea.

  Note:
   1) No. of pins is small — data exchange is 16 to 32 bits per line.
   2) Instruction set — each PE has a small, independent instruction set.
   3) No. of transistors is small.
   → Advantages: small pins, high throughput.

Communication network → Thermal management:
   1) Multicore ⇒ one big die with many cores + shared L2.
   2) Larger die ⇒ more heat.
   (Heat dissipation is the limit.)""",
 explain=r'''
    A(p("<b>What the page says.</b> The systolic array is analysed (why it is cheap in pins and "
        "transistors but fast), and the page closes with the thermal argument for multicore."))
    A(h3("Why systolic arrays are efficient"))
    A(bullets([
        "<b>Few pins.</b> Data moves between neighbouring PEs, so only short local wires (16–32 bits) are "
        "needed — no long, wide global buses.",
        "<b>Simple PEs.</b> Each element runs a tiny, independent instruction (usually multiply-accumulate), "
        "so the control logic is minimal and the design is regular and easy to replicate.",
        "<b>Few transistors</b> per element ⇒ high density and low power per operation.",
        "<b>High throughput.</b> After the pipeline fills, a new result appears every clock.",
    ]))
    A(formula("Systolic matrix multiply (n×n):\n"
              "  Each PE does one multiply-accumulate per beat.\n"
              "  Array fills in O(n) beats, then produces a result every beat → throughput ≈ 1 MAC/PE/cycle."))
    A(h3("The communication-network → thermal argument"))
    A(bullets([
        "A <b>multicore</b> chip is one large die carrying many cores and a shared L2 cache.",
        "A larger die means <b>more transistors</b> switching, hence <b>more heat</b> generated per chip.",
        "Heat must be removed; beyond a limit it cannot be, which is the <b>thermal/power wall</b>.",
    ]))
    A(callout("<b>Chain of reasoning to remember.</b> Higher clock ⇒ more power ⇒ more heat ⇒ cannot "
        "cool ⇒ stop raising the clock ⇒ add more cores instead. Every later topic (cache coherence, "
        "multiprocessors) exists because of this chain.", 'tip'))
''',
 pyqs=[])

PAGES[18] = dict(
 title="The ISA — the contract between software and hardware; ARM and the RISC architecture",
 transcript="""ISA (Instruction Set Architecture):
  “The interface between hardware and software.”

  [ Software ]  ⇄  [ ISA ]  ⇄  [ Hardware ]

ARM (example):
  a RISC architecture.

RISC Architecture:
  To increase ILP (instruction-level parallelism)
  T₁ = ?  (number of instructions)
  T₂ = ?  (cycles per instruction)""",
 explain=r'''
    A(p("<b>What the page says.</b> The <b>ISA</b> is the boundary across which software and hardware "
        "talk. The lecturer uses ARM (a RISC architecture) as the running example and starts to write the "
        "performance quantities."))
    A(h3("What the ISA fixes"))
    A(bullets([
        "The <b>instruction set</b>: which operations exist (add, load, branch, …).",
        "The <b>data types</b> and their sizes (byte, halfword, word, float).",
        "The <b>addressing modes</b>: how operands are located.",
        "The <b>registers</b> the programmer can see.",
        "The <b>instruction encoding</b> (fixed length for RISC, variable for CISC).",
    ]))
    A(p("<b>ARM</b> is a well-known <b>RISC</b> ISA: fixed 32-bit (or 16-bit Thumb) instructions, a "
        "load/store model, and 16 general-purpose registers. The goal of a RISC ISA is to make "
        "<b>instruction-level parallelism (ILP)</b> easy to exploit — uniform instructions pipeline "
        "cleanly."))
    A(formula("The two quantities the lecturer starts to write:\n"
              "  T₁ = number of instructions executed\n"
              "  T₂ = average cycles per instruction (CPI)\n"
              "  Total cycles = T₁ × T₂ ;  time = T₁ × T₂ × clock cycle time"))
    A(p("This leads directly into the performance equations on the following pages: the whole subject is "
        "built on the product of instruction count, CPI and clock period."))
''',
 pyqs=[])

PAGES[19] = dict(
 title="Speed-up and Amdahl’s Law — the derivation",
 transcript="""Speed-up = T_old / T_new = (time before) / (time after)

Amdahl’s Law:
  T_new = T_old (1 − f) + T_old · f / k
        = T_old [ (1 − f) + f/k ]

  Speed-up S = T_old / T_new = 1 / [ (1 − f) + f/k ]

  where f = fraction of the work that can be enhanced,
        k = speed-up of the enhanced portion.

As k → ∞:   S_max = 1 / (1 − f)

Hawkiness: cannot be replaced — all instructions must be executed
in some sequence (they are dependent), while others can be done in parallel.""",
 explain=r'''
    A(p("<b>What the page says.</b> Amdahl’s Law is derived from scratch and the limit is stated. This is "
        "one of the most examined topics, so the derivation must be reproducible."))
    A(h3("Deriving Amdahl’s Law"))
    A(p("Split the program’s time into the part you can improve (fraction <b>f</b>) and the part you "
        "cannot (fraction <b>1 − f</b>). Improve the first part by a factor <b>k</b>. The new time is:"))
    A(formula("T_new = T_old (1 − f)  +  T_old · f / k\n"
              "      = T_old [ (1 − f) + f/k ]\n\n"
              "S = T_old / T_new = 1 / [ (1 − f) + f/k ]\n\n"
              "Limit as k → ∞ :   S_max = 1 / (1 − f)"))
    A(h3("Reading the formula"))
    A(bullets([
        "<b>f</b> = the fraction of the original time that the enhancement speeds up (0 ≤ f ≤ 1).",
        "<b>k</b> = how many times faster the enhanced part becomes (k ≥ 1).",
        "The term <b>(1 − f)</b> is the <i>irreducible serial part</i>. No matter how large k becomes, "
        "it is still there, so it caps the speed-up at 1/(1 − f).",
    ]))
    A(callout("<b>The lesson.</b> Speed-up is limited by the part you do <i>not</i> improve. If 20% of "
        "the time is unimproved, even an infinitely fast enhancement gives at most 1/(1−0.8) = 5×. The "
        "notes’ phrase “cannot be replaced” means the serial instructions must still run in sequence.", 'tip'))
    A(table(["f (enhanced)","k = 2","k = 10","k = ∞"],
      [["10%","1.05","1.10","1.11"],
       ["50%","1.33","1.82","2.00"],
       ["80%","1.67","3.57","5.00"],
       ["90%","1.82","5.26","10.0"]],
      widths=[1.4,1.2,1.2,1.2]))
''',
 pyqs=[1])

PAGES[20] = dict(
 title="Amdahl in practice; integer vs floating-point instruction mix",
 transcript="""Example (Amdahl):
  T_old = 100 s, a portion is enhanced.
  New time = ...

Integer instructions vs Floating-point instructions:
  An instruction is either:
     - an Integer instruction  (fixed-point)
     - a Floating-point instruction  (uses the FP unit)
  Which case (mix) is this, and why does it matter?

Amdahl’s Law:
  T_old / T_new = speed-up
  (response time = clock ticks per program × clock cycle)

Corollary of Amdahl’s Law.""",
 explain=r'''
    A(p("<b>What the page says.</b> The law is applied to numbers, and the lecturer distinguishes the two "
        "kinds of instruction that make up a program — integer (fixed-point) and floating-point — because "
        "the instruction mix drives the average CPI."))
    A(h3("Applying Amdahl to a number"))
    A(formula("If T_old = 100 s and 40% of it is enhanced by k = 4:\n"
              "  T_new = 100 × (1 − 0.4) + 100 × 0.4/4 = 60 + 10 = 70 s\n"
              "  S = 100 / 70 ≈ 1.43×\n"
              "Limit with infinite k:  S_max = 1/(1 − 0.4) = 1.67×"))
    A(h3("Integer vs floating-point instructions"))
    A(p("Every executed instruction is either an <b>integer (fixed-point)</b> instruction — handled by "
        "the integer ALU — or a <b>floating-point</b> instruction — handled by the FP unit. Their "
        "proportions form the <b>instruction mix</b>, and because the two units have different CPIs the "
        "mix determines the average CPI of the program:"))
    A(formula("CPI_avg = Σ (CPI_i × fraction_i)\n"
              "  = CPI_int · f_int + CPI_fp · f_fp + …\n"
              "This is why a program with a large FP fraction behaves very differently\n"
              "from an integer-only program — and why Amdahl’s Law applies separately\n"
              "to each enhanced unit."))
    A(callout("<b>Corollary.</b> Making one unit faster only helps in proportion to how much of the time "
        "that unit is used. Speeding up the FP unit does nothing for an integer-only program (f = 0 for "
        "that unit).", 'tip'))
''',
 pyqs=[4, 33])

PAGES[21] = dict(
 title="Amdahl worked past-paper question (enhanced fraction)",
 transcript="""Q: A program runs in 100 s. A part of the code that takes 40% of the time is
   enhanced to run 5× faster. What is the overall speed-up?

  S = 1 / [ (1 − f) + f/k ] = 1 / [ 0.6 + 0.4/5 ] = 1 / 0.68 ≈ 1.47

Q: What if the enhanced portion runs 10× faster?
  S = 1 / [ 0.6 + 0.04 ] = 1 / 0.64 ≈ 1.5625

(Values computed step by step: 0.4/5 = 0.08 ; 0.4/10 = 0.04)""",
 explain=r'''
    A(p("<b>What the page says.</b> A worked Amdahl question: a 40% portion is enhanced, first by 5×, "
        "then by 10×, and the overall speed-up is computed."))
    A(formula("f = 0.40,  k = 5:\n"
              "  S = 1 / [ (1 − 0.4) + 0.4/5 ] = 1 / (0.6 + 0.08) = 1/0.68 ≈ 1.47×\n\n"
              "f = 0.40,  k = 10:\n"
              "  S = 1 / [ 0.6 + 0.4/10 ] = 1 / (0.6 + 0.04) = 1/0.64 = 1.5625×\n\n"
              "Limit (k → ∞):  S_max = 1/0.6 ≈ 1.667×"))
    A(p("The detailed solution and the full transcription of the original question are given with the "
        "other past-paper solutions at the end of this section (see ca4, ca7, ca33, ca36)."))
''',
 pyqs=[])

PAGES[22] = dict(
 title="Amdahl worked past-paper question (continued)",
 transcript="""(Continuation of the Amdahl arithmetic.)
  Speed-up values tabulated:
    enhanced fraction   speed-up of part   overall S
       40%                  5×               1.47
       40%                 10×               1.56
       33%                   ?               1.33
       25%                   ?               ...
  Intermediate values: 0.4/5 = 0.08 ; 1/0.68 = 1.47 ; 1/0.64 = 1.5625""",
 explain=r'''
    A(p("<b>What the page says.</b> More Amdahl arithmetic — the same formula applied to several "
        "fractions, building a small table of overall speed-ups."))
    A(formula("General:  S = 1 / [ (1 − f) + f/k ]\n"
              "  f = 0.33, k = 3:  S = 1 / [ 0.67 + 0.11 ] = 1/0.78 ≈ 1.28×\n"
              "  f = 0.25, k = 5:  S = 1 / [ 0.75 + 0.05 ] = 1/0.80 = 1.25×"))
    A(table(["Enhanced fraction f","Enhancement k","Overall speed-up S","Limit 1/(1−f)"],
      [["0.40","5","1.47","1.67"],
       ["0.40","10","1.56","1.67"],
       ["0.33","3","1.28","1.49"],
       ["0.25","5","1.25","1.33"]],
      widths=[1.6,1.3,1.6,1.5]))
    A(callout("<b>Pattern to notice.</b> Doubling k from 5 to 10 barely changes S (1.47 → 1.56). The "
        "unimproved 60% dominates. This is the single most common exam insight about Amdahl’s Law.", 'tip'))
''',
 pyqs=[36])

PAGES[23] = dict(
 title="Power, voltage and frequency scaling (the power wall)",
 transcript="""Dynamic power = Capacitor load  (a)
   P_dyn ∝ C · V² · f
   Power ∝ voltage² × frequency

  Energy ∝ Power × time
  (t = time, E = energy)

Overclocking → more power → more heat → cooling cost.
Voltage/frequency scaling → lower power.

“Power ∝ C × V² × f”  and “Overclocking → higher power/heat”.""",
 explain=r'''
    A(p("<b>What the page says.</b> The physics that forces parallelism: power depends on voltage squared "
        "and on frequency, so raising the clock is expensive in both power and heat."))
    A(formula("Dynamic power:   P_dyn = C · V² · f\n"
              "   C = switched capacitance, V = supply voltage, f = clock frequency\n"
              "Total power:     P = P_dyn + P_static  (P_static ∝ V · I_leak)\n"
              "Energy:          E = P · t   (joules)"))
    A(bullets([
        "<b>Frequency scaling.</b> To run faster you must raise f; but raising f at a fixed voltage also "
        "requires raising V (the transistors must switch faster), and power grows with V² — so power "
        "explodes.",
        "<b>Overclocking</b> pushes V and f above the rated point; power and heat rise sharply and "
        "cooling becomes the limit.",
        "<b>Voltage/frequency scaling (DVFS)</b> lowers V and f together to save energy with only a "
        "modest performance loss.",
    ]))
    A(formula("Example: reduce V by 20% and f by 20%:\n"
              "  P_new / P_old = 0.8² × 0.8 = 0.512  →  about 49% less dynamic power\n"
              "  (performance falls only ~20%.)"))
    A(callout("<b>Consequence.</b> Clock frequency stopped scaling around 2004 (the “power wall”). The "
        "industry responded by adding cores instead of raising the clock — the multicore shift that "
        "pages 16–17 describe.", 'tip'))
''',
 pyqs=[26])

PAGES[24] = dict(
 title="Cost of an integrated circuit; MTTF, MTTR, MTBF and availability",
 transcript="""Cost of IC:
  Cost = (Cost of die + Cost of testing) / Yield
  Cost of die = Cost of wafer / (Dies per wafer × Yield)

  Dies per wafer = π (wafer diameter / 2)² / Die area  −  π (wafer diameter) / √(2 × Die area)

Basic components of reliability:
  * A failure occurs when the service deviates from the specification.
  * Reliability = probability of correct service for a given time.
  Mean Time To Failure (MTTF)
  Mean Time To Repair (MTTR)
  Mean Time Between Failures (MTBF) = MTTF + MTTR
  Module availability = MTTF / (MTTF + MTTR)""",
 explain=r'''
    A(p("<b>What the page says.</b> The economics of making chips (cost per die, yield) and the four "
        "dependability quantities that are examined: MTTF, MTTR, MTBF and availability."))
    A(h3("Cost of an integrated circuit"))
    A(formula("Dies per wafer = π (d/2)² / (die area)  −  π d / √(2 · die area)\n"
              "   d = wafer diameter (the second term corrects for dies lost at the edge)\n\n"
              "Cost of die = Cost of wafer / (Dies per wafer × Yield)\n"
              "Cost of IC  = (Cost of die + Cost of testing) / Yield"))
    A(p("<b>Yield</b> is the fraction of dies that work. Yield falls as the die gets bigger (more area ⇒ "
        "more chance of a defect) and as the process gets newer. Because the cost is divided by yield, "
        "improving yield directly lowers cost — often more effective than shrinking the die."))
    A(h3("Dependability quantities"))
    A(formula("MTTF — Mean Time To Failure      (average time a component works)\n"
              "MTTR — Mean Time To Repair       (average time to fix it)\n"
              "MTBF — Mean Time Between Failures = MTTF + MTTR\n"
              "Availability A = MTTF / (MTTF + MTTR) = MTTF / MTBF"))
    A(bullets([
        "A <b>failure</b> occurs when the delivered service deviates from the specification.",
        "<b>Reliability</b> is the probability of correct service over a given time.",
        "Availability is a <i>fraction</i> (e.g. 0.99 = 99% uptime); MTTF and MTTR are times.",
    ]))
    A(callout("<b>Memory hook.</b> Availability = uptime / (uptime + downtime) = MTTF/MTBF. A larger MTTF "
        "or a smaller MTTR both raise availability.", 'tip'))
''',
 pyqs=[30])

PAGES[25] = dict(
 title="MTTF and failure-rate worked examples",
 transcript="""Failure rate λ = 1 / MTTF

For n identical components that must ALL work (series):
   1/MTTF_sys = Σ 1/MTTF_i  →  MTTF_sys = MTTF / n

Q1: MTTF = 400 h, MTTR = 7 h. Find MTBF.
    MTBF = 400 + 7 = 407 h

Q2: A hard drive with MTTF = 5000 h. Over 2 years (~ 9500 h?),
    how many failures?

Intermediate: MTTF = 100 h (example), etc.""",
 explain=r'''
    A(p("<b>What the page says.</b> The reliability quantities are applied to numbers: the failure rate, "
        "the MTTF of several components in series, and two worked questions."))
    A(formula("Failure rate:      λ = 1 / MTTF\n"
              "Series (all must work):  1/MTTF_sys = Σ 1/MTTF_i  →  MTTF_sys = MTTF/n for n identical\n"
              "Parallel (only one must work):  the system fails only if ALL fail\n"
              "   →  availability rises:  A_sys = 1 − (1 − A)ⁿ"))
    A(h3("Worked answers"))
    A(formula("Q1:  MTTF = 400 h, MTTR = 7 h  →  MTBF = 400 + 7 = 407 h\n"
              "     Availability = 400/407 ≈ 0.983 = 98.3%\n\n"
              "Q2:  MTTF = 5000 h per drive; two years ≈ 2 × 8760 = 17520 h\n"
              "     Expected failures = 17520 / 5000 ≈ 3.5\n"
              "     Failure rate λ = 1/5000 = 2 × 10⁻⁴ per hour"))
    A(callout("<b>Series vs parallel.</b> Adding components <i>in series</i> (all must work) makes the "
        "system <b>less</b> reliable — MTTF falls to MTTF/n. Adding <i>redundant</i> components (only one "
        "must work) makes it <b>more</b> available. The exam usually wants you to say which case applies.", 'tip'))
''',
 pyqs=[])

PAGES[26] = dict(
 title="Reliability past-paper questions (server farm, disk failures, die yield)",
 transcript="""Q3: A web service runs on 2 identical servers in parallel; MTTF = 20 h,
    MTTR = ... per server. (Availability of the pair.)

Q4: Silicon wafer (cost = 1000 monetary units, density = ...):
    Calculate die yield. A wafer of diameter 30 cm?  die area 60 mm²?
    defects per cm² = 0.23.

    Yield = (1 + Defects × Die area / 2)^(−2)

    Compare: for a bigger die the yield falls and the cost per good die rises.""",
 explain=r'''
    A(p("<b>What the page says.</b> Past-paper reliability questions: a redundant two-server farm, and a "
        "wafer-yield calculation using the standard yield model."))
    A(h3("Worked answers"))
    A(formula("Q3 (redundant servers):  each server MTTF = 20 h (say), MTTR = 2 h\n"
              "  Availability of one server  A = MTTF/(MTTF+MTTR) = 20/22 ≈ 0.909\n"
              "  Availability of the pair (only one needed): A_sys = 1 − (1 − A)²\n"
              "     = 1 − (0.091)² ≈ 0.992  → redundancy raises availability.\n\n"
              "Q4 (wafer yield):  Yield = (1 + Defects_per_area × Die_area / 2)^(−2)\n"
              "  With defects = 0.23 /cm² and die area = 0.6 cm²:\n"
              "     Yield = (1 + 0.23 × 0.6 / 2)^(−2) = (1 + 0.069)^(−2) = 1.069^(−2) ≈ 0.875\n"
              "  A larger die (bigger area) ⇒ smaller yield ⇒ higher cost per good die."))
    A(callout("<b>Two formulas, one idea.</b> Reliability questions either use the availability formula "
        "(MTTF/MTBF, with redundancy) or the yield formula (cost questions). Identify which family the "
        "question belongs to before substituting.", 'tip'))
''',
 pyqs=[])

PAGES[27] = dict(
 title="Availability from MTTF; the bridge to performance metrics (CPU time)",
 transcript="""Q1: MTTF = 936 h, A = 0.99 (or 0.951?)
   Un-availability = 1 − A = 0.01
   MTTR = MTTF × (1 − A)/A

Performance metrics:
  Response time, execution time, throughput.
  CPU time = Clock cycles × Clock cycle time
           = Clock cycles / Clock rate
  Clock cycles = Instructions per program × Cycles per instruction
  CPU time = IC × CPI × clock cycle time""",
 explain=r'''
    A(p("<b>What the page says.</b> A final availability calculation, then the pivot into performance "
        "metrics: CPU time is the product of instruction count, CPI and clock cycle time."))
    A(formula("Q1:  MTTF = 936 h, A = 0.99\n"
              "   Unavailability = 1 − A = 0.01\n"
              "   A = MTTF/(MTTF + MTTR)  →  MTTR = MTTF × (1 − A)/A = 936 × 0.01/0.99 ≈ 9.45 h"))
    A(h3("The performance equations"))
    A(formula("CPU time = Clock cycles × Clock cycle time\n"
              "         = Clock cycles / Clock rate\n"
              "Clock cycles = (Instructions / program) × (Cycles / instruction)\n"
              "CPU time = IC × CPI × T_clock = IC × CPI / f"))
    A(bullets([
        "<b>Response (execution) time</b> — how long one task takes; the metric a single program cares about.",
        "<b>Throughput</b> — how many tasks finish per unit time; the metric a server cares about.",
        "<b>IC</b> (instruction count) is fixed by the compiler and the ISA; <b>CPI</b> by the "
        "organization and the program; <b>T_clock</b> by the hardware technology.",
    ]))
    A(callout("<b>Everything follows from IC × CPI × T_clock.</b> Every “make it faster” question is one "
        "of: change IC (better compiler/ISA), change CPI (pipeline, caches, ILP), or change T_clock "
        "(technology, deeper pipeline).", 'tip'))
''',
 pyqs=[])

PAGES[28] = dict(
 title="CPU time worked example — instruction mix to average CPI",
 transcript="""CPU time = IC × CPI × Clock cycle time

Instruction mix (example):
   ALU      40%   CPI 1
   Load/Store 20%  CPI 2
   Control   30%   CPI 3
   Others    10%   CPI 4

CPI = 0.4×1 + 0.2×2 + 0.3×3 + 0.1×4
    = 0.4 + 0.4 + 0.9 + 0.4 = 2.1

Example: IC = 1×10⁶, f = ... → CPU time = IC × CPI / f

MIPS = (IC) / (execution time × 10⁶) = f / (CPI × 10⁶)""",
 explain=r'''
    A(p("<b>What the page says.</b> The classic instruction-mix calculation: convert the mix into an "
        "average CPI, then into CPU time and MIPS."))
    A(formula("CPI_avg = Σ (CPI_i × fraction_i)\n"
              "  = 0.4×1 + 0.2×2 + 0.3×3 + 0.1×4\n"
              "  = 0.4 + 0.4 + 0.9 + 0.4 = 2.1"))
    A(p("With the average CPI in hand, everything else is substitution:"))
    A(formula("CPU time = IC × CPI / f\n"
              "  e.g. IC = 10⁶ instructions, f = 2 GHz:  CPU time = 10⁶ × 2.1 / 2×10⁹ = 1.05 ms\n\n"
              "MIPS = f / (CPI × 10⁶) = 2×10⁹ / (2.1 × 10⁶) ≈ 952 MIPS"))
    A(callout("<b>Caution with MIPS.</b> MIPS = millions of instructions per second; it is only "
        "comparable between machines with the <i>same</i> ISA, because it ignores how much work each "
        "instruction does. For whole-program comparison use execution time.", 'tip'))
''',
 pyqs=[5])

PAGES[29] = dict(
 title="The components of CPU time; a worked “what is the clock rate?” question",
 transcript="""CPU time = IC × CPI × Clock Cycle Time
         = Instructions / program × Cycles / instruction × seconds / cycle

Components of CPU time:
  * Compiler          (determines IC)
  * ISA               (determines IC and CPI)
  * Organization      (determines CPI and T_clock)
  * Hardware / technology  (determines T_clock)

Q: A program runs in 35 s. The ISA/compiler part is 45%, and the improvement
   is 10%? How much improvement for the other processor?

(Worked arithmetic about which fraction to enhance to reach a target time.)""",
 explain=r'''
    A(p("<b>What the page says.</b> CPU time is decomposed into who controls each factor, and a worked "
        "question asks how much one component must improve to hit a target time."))
    A(table(["Factor","Who controls it","What it affects"],
      [["Instruction count (IC)","Compiler + ISA","How many instructions the program has"],
       ["CPI","Organization + program","How many cycles each instruction takes"],
       ["Clock cycle time","Organization + technology","How long a cycle lasts"]],
      widths=[1.5,2.0,2.0]))
    A(p("A question in this style gives the current time, states that one component occupies a fraction "
        "of the total, and asks what improvement in the <i>other</i> component is needed to reach a "
        "target. Solve it with Amdahl rearranged:"))
    A(formula("If a fraction f of the time is NOT changed, then\n"
              "  T_new = T_old [ (1 − f) + f/k ]  →  solve for the k (or f) that gives the target.\n"
              "Example: T_old = 35 s, the unchangeable part is 45% (0.45),\n"
              "  to reach T_new = 28 s:\n"
              "   28 = 35 [ 0.45 + 0.55/k ]  →  0.80 = 0.45 + 0.55/k\n"
              "   0.55/k = 0.35  →  k = 1.57  (the changeable part must speed up 1.57×)"))
    A(callout("<b>Reading the question.</b> “The other part is X%” tells you the unchangeable fraction "
        "(1 − f). Substitute, isolate k, done. Always check the answer is ≥ 1.", 'tip'))
''',
 pyqs=[])

PAGES[30] = dict(
 title="CPU-time / MIPS past-paper question (instruction classes)",
 transcript="""Instruction     Time    Frequency
  Load/Store     30%     5
  ALU            20%     4
  Others         20%     4
  ... (a mix)

Q1) Find the number of instructions if the clock = ... MHz?
Q2) CPU execution time?
Q3) If the compiler used fewer ... instructions, which is better?

(The lecturer works out CPI from the mix and then CPU time / MIPS.)""",
 explain=r'''
    A(p("<b>What the page says.</b> A past-paper performance question: given an instruction mix with "
        "cycle counts, find the average CPI, then the CPU time and MIPS."))
    A(formula("CPI_avg = Σ (fraction_i × CPI_i)\n"
              "  = 0.30×5 + 0.20×4 + 0.20×4 + (rest)…  →  substitute the actual figures\n"
              "CPU time = IC × CPI_avg / f\n"
              "MIPS = f / (CPI_avg × 10⁶)"))
    A(p("The full transcription of the original question, with the exact numbers as printed, and the "
        "complete step-by-step solution, are given with the other past-paper solutions at the end of this "
        "section (ca1 Q1, ca5 Q4, ca19 Q1)."))
    A(callout("<b>Method.</b> (1) Turn the mix into an average CPI. (2) Multiply by IC and divide by the "
        "clock rate for the time. (3) Invert to get MIPS. Always keep the units explicit.", 'tip'))
''',
 pyqs=[])

PAGES[31] = dict(
 title="CPU-time past-paper question (worked arithmetic)",
 transcript="""Working:
  CPU time = 3 s (example)
  Time components: 15, 20.5, 3 ...
  New CPU time = 9.5 s
  New CCT = 13 s

  CPI = 0.3×... + 0.4×0.5 + 3×0.2
      = 1.5 + 2 + 0.6 = ...

  MIPS = 200×10⁶ / (2×10⁶ ...) = 6×10⁷ ...
  Result ≈ 1.66×10⁸ Hz""",
 explain=r'''
    A(p("<b>What the page says.</b> Step-by-step arithmetic for a CPU-time question — computing an "
        "average CPI and then a clock rate or MIPS from the given numbers."))
    A(formula("CPI_avg = Σ fraction_i × CPI_i\n"
              "  = 0.3×? + 0.4×0.5 + 0.3×0.2  (substitute the printed values)\n\n"
              "Rearranged metrics:\n"
              "  f = IC × CPI / CPU time\n"
              "  MIPS = IC / (CPU time × 10⁶) = f / (CPI × 10⁶)"))
    A(p("The complete question text and every intermediate value are transcribed and solved in the "
        "past-paper solutions section. The key is to keep the three quantities — IC, CPI, clock — "
        "straight and solve for whichever one the question leaves unknown."))
''',
 pyqs=[])

PAGES[32] = dict(
 title="CPU-time past-paper question (continued)",
 transcript="""(Continued arithmetic.)
  0.35×1 + 0.5×... + 0.1×3 ...
  = 0.85 ... 
  ...
  0.25, 0.4, 0.1 ...
  → final clock rate ≈ ...

(Values carried through to a final answer.)""",
 explain=r'''
    A(p("<b>What the page says.</b> The completion of the CPU-time question: the average CPI and the "
        "resulting time or clock rate."))
    A(formula("CPI_avg = 0.35×1 + 0.50×? + 0.10×3 + …   (per the printed mix)\n"
              "CPU time = IC × CPI_avg / f ;   f = IC × CPI_avg / CPU time"))
    A(p("The exact figures and the final numeric answer are given, with the full reasoning, in the "
        "past-paper solutions at the end of this section. Read the printed question alongside this page."))
''',
 pyqs=[])

PAGES[33] = dict(
 title="Characteristics of pipelining; speed-up; the space–time (timing) diagram",
 transcript="""Characteristics of Pipeline:
  1) Performance of the pipeline depends on the slowest stage.
  2) Performance depends on the number of pipeline stages.

  Stages:  S1  S2  S3  S4  S5
           C1  C2  C3  C4  C5
           t1  t2  t3  t4  t5

  Time for 5 instructions, 5 stages = 9 cycles (fill + drain).

  Ideal speed-up = (n · k) / (n + k − 1)   →  ≈ k for large n
  Here k = 5, n = 5:  S = 25 / 9 ≈ 2.5

  Actual CPI ≈ 2.5? (example)
  Clock period = 1/5 of the ...""",
 explain=r'''
    A(p("<b>What the page says.</b> The two properties of a pipeline (its speed is set by the slowest "
        "stage, and by how many stages there are) and the timing diagram that gives the speed-up."))
    A(bullets([
        "<b>Property 1 — the slowest stage rules.</b> All stages advance together, so the clock period "
        "must be at least as long as the slowest stage. Making the other stages faster does not help "
        "unless you also speed up the slowest one (or split it).",
        "<b>Property 2 — the number of stages.</b> More stages can give a shorter clock, but the fill and "
        "drain overhead grows and each hazard costs more.",
    ]))
    A(formula("Non-pipelined time for n instructions, k stages:\n"
              "  T_serial = n · k · t      (each instruction occupies all k stages)\n"
              "Pipelined time:\n"
              "  T_pipe = (k + n − 1) · t  (k to fill, then one finishes per cycle)\n"
              "Speed-up:\n"
              "  S = T_serial / T_pipe = (n · k) / (n + k − 1)  →  k   as n → ∞\n"
              "Example: n = 5, k = 5:  S = 25/9 ≈ 2.78"))
    A(p("<b>The space–time diagram.</b> Draw a grid: instructions down the side, cycles across the top. "
        "Instruction i occupies stage j in cycle (i + j − 1), so the occupied cells form a diagonal "
        "band. In steady state every cycle has one instruction in every stage, and one instruction "
        "finishes per cycle."))
    A(callout("<b>Two numbers to keep apart.</b> <i>Latency</i> = k cycles (unchanged); <i>throughput</i> "
        "= 1 instruction/cycle in steady state. The speed-up is bounded by k, not equal to it, because "
        "of fill and drain.", 'tip'))
''',
 pyqs=[19])
