"""Page-by-page annotations for handwritten pages 34-52."""

PAGES = {}

PAGES[34] = dict(
 title="The five pipeline stages in detail; instruction fetch and PC update",
 transcript="""Instruction fetch and PC update:
  IF: read the instruction at the address in PC from memory;
      PC ← PC + 4 (the next instruction).

Uniform code completion (when all stages are of equal length):
  Stage lengths must be balanced so the clock is not limited by one slow stage.

Pipeline hazards:
  Structural (resource) hazard — a hardware resource is used by two instructions at once.
  Data hazard — an instruction needs data not yet produced.
  Control hazard — a branch changes which instruction is fetched next.

Register file: ALU output → write to register file
  (data forwarding / bypass)""",
 explain=r'''
    A(p("<b>What the page says.</b> The five stages are explained one by one, with the fetch/PC update "
        "spelled out, and the three hazard classes are named."))
    A(table(["Stage","Name","What happens"],
      [["1","IF — Instruction Fetch","Read instruction at PC; PC ← PC + 4"],
       ["2","ID — Instruction Decode","Decode opcode; read the register file"],
       ["3","EX — Execute","ALU operation or address calculation"],
       ["4","MEM — Memory access","Load from or store to data memory"],
       ["5","WB — Write Back","Write the result into the register file"]],
      widths=[0.7,1.7,4.0]))
    A(formula("PC update:  PC ← PC + 4     (4 bytes = 32-bit instruction)\n"
              "Each stage is separated by a pipeline register that latches the\n"
              "intermediate result at the end of the cycle."))
    A(h3("Why the stages must be balanced"))
    A(p("The clock period equals the longest stage plus the register overhead. If one stage is much "
        "slower than the others, all the other stages idle while waiting for it, so the design should "
        "split any slow stage (this is why a slow memory stage might itself be pipelined)."))
    A(h3("The three hazard classes (named here, developed next)"))
    A(bullets([
        "<b>Structural (resource) hazard</b> — two instructions want the same hardware at the same time "
        "(e.g. one memory for both instruction fetch and data access).",
        "<b>Data hazard</b> — an instruction needs a value that a previous instruction has not produced yet.",
        "<b>Control hazard</b> — a branch decides the next PC, but the decision is not ready when the "
        "next fetch must happen.",
    ]))
''',
 pyqs=[20])

PAGES[35] = dict(
 title="Pipeline timing with real instruction latencies; the load-use stall",
 transcript="""Pipeline timing:
  IF | ID | EX | MEM | WB

For a load:
  IF | ID | EX | MEM | WB  — data available after MEM

Load-use: the value is read in MEM, so an instruction that uses it must wait
  → one stall cycle (with forwarding) or more (without).

Branch: takes 2 clock cycles (may be more than other instructions).

Timing table example:
  cycles:  1  2  3  4  5  6
  load:    IF ID EX MEM WB
  use:        IF ID  *  EX MEM WB   (* = stall)""",
 explain=r'''
    A(p("<b>What the page says.</b> A load does not produce its result until the MEM stage, so an "
        "instruction that immediately uses the loaded value must wait — the <b>load-use stall</b>. The "
        "page draws the timing table and marks the stall."))
    A(formula("Load:      IF  ID  EX  MEM  WB      ← result ready after MEM\n"
              "Use:           IF  ID  *   EX   MEM  WB   (* = one stall cycle)\n\n"
              "With forwarding, the value can be sent from MEM/WB straight to the\n"
              "use instruction’s EX stage, so only ONE bubble is needed.\n"
              "Without forwarding, the use must wait until the load writes back → 2–3 bubbles."))
    A(bullets([
        "A <b>stall (bubble)</b> is an empty slot inserted into the pipeline; it wastes a cycle but keeps "
        "the timing correct.",
        "<b>Forwarding (bypassing)</b> sends the result from an internal pipeline register straight to "
        "the waiting ALU, avoiding the wait in most cases.",
        "The <b>load-use</b> case cannot be fully fixed by forwarding because the data is not ready until "
        "after MEM, so one stall remains.",
        "A <b>branch</b> may take two cycles in the ID stage, adding a control-hazard penalty.",
    ]))
''',
 pyqs=[9, 10, 13, 16, 21, 31])

PAGES[36] = dict(
 title="Forwarding, load vs store handling, and the compiler’s role in scheduling",
 transcript="""Compute-time optimisation:
  Reorder the code to fill the load delay slot.

LOOP:
  load → use  (dependency)

The pipeline register is too wide — try to avoid the load-delay slot.
  (Hardware forwarding helps; the compiler can also schedule.)

LOAD vs STORE:
  A load must complete before its value is used.
  A store can proceed without waiting (it does not produce a register value).

Instruction scheduling:
  The compiler reorders instructions to fill delay slots with useful work.""",
 explain=r'''
    A(p("<b>What the page says.</b> Two ways to hide the load delay: hardware forwarding and software "
        "scheduling by the compiler. It also distinguishes loads from stores."))
    A(bullets([
        "<b>Hardware forwarding</b> removes most stalls by routing a result as soon as it exists, but "
        "the load-use case still needs one stall because the data arrives late.",
        "<b>Compiler scheduling</b> reorders independent instructions so that useful work fills the "
        "delay slot — the “load delay slot” is occupied by an instruction that does not depend on the "
        "load.",
        "<b>Load vs store.</b> A load produces a register value, so a following use must wait for it. A "
        "store writes memory and produces no register value, so following instructions generally do not "
        "wait for it (it can be buffered).",
    ]))
    A(formula("Load-delay slot example:\n"
              "  lw   $t0, 0($s0)      ; t0 available after MEM\n"
              "  add  $t1, $t2, $t3    ; independent — fill the slot\n"
              "  add  $t4, $t0, $t5    ; now uses t0 with no stall"))
    A(callout("<b>Who fixes what.</b> Hardware forwarding is free but incomplete (load-use remains). "
        "Compiler scheduling is flexible but limited by the available independent instructions. The two "
        "are complementary.", 'tip'))
''',
 pyqs=[])

PAGES[37] = dict(
 title="Branch prediction — the one-bit predictor",
 transcript="""1) One-Bit Predictor

  State machine:  (Taken) ←→ (Not Taken)
      predict T        predict N

  “T”/“NT” stored per branch.

  Misclassification: a branch that changes direction costs a mispredict.

  Accuracy: mispredicts on every change of direction (e.g. a loop exit).

  Mixed class → easier branch behaviour.""",
 explain=r'''
    A(p("<b>What the page says.</b> The simplest dynamic branch predictor: one bit per branch that "
        "records the direction taken last time."))
    A(h3("How it works"))
    A(bullets([
        "Keep one bit per branch (in a small table indexed by the branch address).",
        "After the branch executes, set the bit to Taken (T) or Not-Taken (NT) according to what actually "
        "happened.",
        "Next time, predict whatever the bit says.",
    ]))
    A(formula("One-bit predictor state machine (two states):\n"
              "   predict T        actual T\n"
              "  [Not Taken] ──────────────→ [Taken]\n"
              "       ↑                          │\n"
              "       └──── actual NT ───────────┘\n"
              "   prediction = the state; mispredict whenever the direction changes."))
    A(p("<b>Weakness.</b> A loop that runs 100 times taken and once not-taken will mispredict <i>twice</i> "
        "per execution: once when it exits (predict T, actual NT) and once when it is entered again "
        "(predict NT, actual T). A 2-bit predictor fixes this."))
    A(formula("Misprediction examples:\n"
              "  Loop taken 100×, then not taken:\n"
              "    one-bit predictor → 2 mispredicts per loop execution.\n"
              "  Accuracy = correct / total."))
''',
 pyqs=[17, 32])

PAGES[38] = dict(
 title="Tournament (hybrid) branch predictor",
 transcript="""Tournament Branch Predictor

  Uses two-level prediction — combining a local and a global predictor.

  Local predictor:  (history of THIS branch)
  Global predictor: (history of RECENT branches)

  A chooser (selector) picks whichever predictor has been more accurate.

  Diagram: two predictor tables (local, global) feed a multiplexer whose
  select line comes from a small “chooser” counter table.

  Global history register: a shift register of the last k branch outcomes.""",
 explain=r'''
    A(p("<b>What the page says.</b> A <b>tournament</b> (hybrid) predictor runs two predictors at once "
        "and uses a chooser to decide which to believe."))
    A(bullets([
        "<b>Local predictor</b> — remembers the history of <i>this particular</i> branch (useful for "
        "branches with their own repeating pattern).",
        "<b>Global predictor</b> — remembers the pattern of the <i>most recent branches</i> overall "
        "(useful when branches are correlated with each other).",
        "<b>Chooser</b> — a small table of 2-bit counters, one per branch, that records which of the two "
        "predictors has been right more often and selects it.",
    ]))
    A(formula("Global history register (GHR):  k bits, shifted after each branch\n"
              "  e.g. history T T N T  →  1101\n"
              "  This pattern indexes a table of counters (a two-level predictor).\n\n"
              "Prediction = chooser_counter ? global_pred : local_pred"))
    A(p("<b>Reconstructed diagram.</b> Draw two boxes side by side — “Local predictor” and “Global "
        "predictor” — whose outputs go into a 2:1 multiplexer. The multiplexer’s select comes from a "
        "third small table, the “chooser”, indexed by the branch address. The global predictor is fed by "
        "a shift register (the GHR)."))
    A(callout("<b>Why it wins.</b> Neither predictor alone is best for every branch; the chooser learns "
        "per branch which one to trust, so the combined accuracy is higher than either alone. Real CPUs "
        "(e.g. Intel, AMD) use tournament-style predictors.", 'tip'))
''',
 pyqs=[8])

PAGES[39] = dict(
 title="One-bit predictor state machine (worked table)",
 transcript="""One-bit predictor:

  current state   actual   next state   correct?
      T             T         T            yes
      T             N         N            no
      N             T         T            no
      N             N         N            yes

  Sequence of outcomes and the corresponding predictions/updates
  (a table of T/N and hit/miss).

  Prediction = previous outcome. Accuracy = fraction correct.""",
 explain=r'''
    A(p("<b>What the page says.</b> The one-bit predictor written as a truth table: the next state is "
        "simply the actual outcome, and the prediction is correct only when the outcome repeats."))
    A(table(["Current state","Actual","Next state","Correct?"],
      [["T (Taken)","T","T","✔ yes"],
       ["T (Taken)","N","N","✘ no"],
       ["N (Not taken)","T","T","✘ no"],
       ["N (Not taken)","N","N","✔ yes"]],
      widths=[1.5,1.1,1.4,1.4]))
    A(formula("State = last outcome.  Prediction = state.\n"
              "A mispredict happens exactly when the branch changes direction.\n"
              "For a loop taken m times then not taken:\n"
              "   mispredicts per pass = 2  (entry and exit)."))
    A(p("<b>Worked sequence.</b> Take the outcome string  N T T T T N T … The predictor starts in some "
        "state; after each branch it copies the outcome into the state, so it predicts the <i>previous</i> "
        "outcome. Every change from T to N or N to T costs one misprediction."))
''',
 pyqs=[])

PAGES[40] = dict(
 title="Two-bit saturating counter predictor (state machine)",
 transcript="""Two-bit saturating counter:

  States:  00 (strongly NT)  01 (weakly NT)
           10 (weakly T)      11 (strongly T)

  Transitions:
    actual T:  00→01, 01→10, 10→11, 11→11
    actual N:  11→10, 10→01, 01→00, 00→00

  Predict taken if the high bit is 1 (states 10, 11).

  A single change of direction does NOT flip the prediction
  (it must saturate first) → fewer mispredicts on loop exits.""",
 explain=r'''
    A(p("<b>What the page says.</b> The 2-bit saturating counter: a small state machine that needs "
        "<i>two</i> wrong guesses in a row before it changes its mind, which fixes the loop-exit problem "
        "of the one-bit predictor."))
    A(formula("2-bit saturating counter state machine:\n"
              "   00 (strong NT) --T--> 01 (weak NT) --T--> 10 (weak T) --T--> 11 (strong T)\n"
              "   11 (strong T)  --N--> 10 (weak T)  --N--> 01 (weak NT) --N--> 00 (strong NT)\n"
              "   Prediction: TAKEN if state ∈ {10, 11};  NOT TAKEN if state ∈ {00, 01}\n"
              "   The counter saturates at 00 and 11 (it cannot wrap around)."))
    A(table(["State","Meaning","Predicts"],
      [["00","strongly not taken","Not taken"],
       ["01","weakly not taken","Not taken"],
       ["10","weakly taken","Taken"],
       ["11","strongly taken","Taken"]],
      widths=[1.0,2.2,1.6]))
    A(p("<b>Why it is better.</b> A loop that runs 100 times taken then once not-taken: the counter sits "
        "in state 11; the exit takes it to 10, which still predicts Taken — but the next (first) iteration "
        "is taken, so it moves back to 11 and no mispredict occurs on re-entry. Only the exit and the "
        "re-entry are “weak”, so the 2-bit predictor mispredicts roughly once per loop execution instead "
        "of twice."))
    A(formula("One-bit: 2 mispredicts per loop pass.\n"
              "Two-bit: about 1 mispredict per loop pass (only the exit)."))
''',
 pyqs=[])

PAGES[41] = dict(
 title="Two-bit / correlating predictor (worked table and scheduling note)",
 transcript="""Two-bit / correlating predictor:

  A table indexed by (branch history, branch address) holding 2-bit counters.

  Scheduling note: the predictor reduces the branch penalty so that
  scheduling (filling delay slots) becomes easier.

  Worked table of (history → prediction) and hit/miss counts.

  Accuracy improves because the prediction depends on the pattern of
  recent branches, not just this branch.""",
 explain=r'''
    A(p("<b>What the page says.</b> The correlating (two-level) predictor: instead of one counter per "
        "branch, index a table of counters with the <i>history</i> of recent branches, so the prediction "
        "captures patterns such as “if the last two branches were taken, this one usually is too”."))
    A(formula("Two-level (correlating) predictor:\n"
              "  index = (global history register, branch address)\n"
              "  table[index] = 2-bit counter (as on the previous page)\n"
              "  Example history pattern  T T N T  →  a 4-bit index.\n"
              "  This distinguishes branch patterns that a single counter cannot."))
    A(p("<b>Reconstructed diagram.</b> Draw a shift register (the global history register) at the top "
        "that stores the last k outcomes. Its bits, concatenated with the branch address, form the index "
        "into a table of 2-bit counters. The selected counter gives the prediction."))
    A(callout("<b>Link to scheduling.</b> A better predictor means fewer control-hazard stalls, which "
        "makes the compiler’s job of filling delay slots easier — the page notes this connection "
        "explicitly.", 'tip'))
''',
 pyqs=[])

PAGES[42] = dict(
 title="Register renaming with a reorder buffer (data dependence resolution)",
 transcript="""Handling register renaming depends on data:
  1) Allocate an architectural register?
  2) Rename: the architectural register → a physical register (Reorder Buffer entry).
  → In the ROB, the entry holds the value; the register map points to it.

  Register file: architectural register numbers → physical register numbers.
  → Instruction writes to the ROB; on commit, the value is copied to the
    architectural register file.

  Instruction issue → update RAT (register alias table)
  Instruction completion → write to ROB
  (Commit) → write to ARF (architectural register file)""",
 explain=r'''
    A(p("<b>What the page says.</b> <b>Register renaming</b> removes false (name) dependences by giving "
        "each new value its own physical register. A <b>reorder buffer (ROB)</b> holds the speculative "
        "values until the instruction is certain to execute."))
    A(bullets([
        "<b>Architectural registers</b> — the ones the programmer sees (e.g. $t0, F0). There are only a "
        "few of them, so different instructions reuse the same names.",
        "<b>Physical registers</b> — a much larger pool. Renaming maps each architectural register to a "
        "physical one, so two instructions that use the same name no longer conflict.",
        "<b>Reorder buffer (ROB)</b> — a circular queue holding instructions in program order; each entry "
        "stores the destination value until the instruction commits.",
        "<b>Register alias table (RAT)</b> — the map from architectural to physical register, updated as "
        "instructions issue.",
        "<b>Commit</b> — when an instruction is the oldest and has no exceptions, its value is copied "
        "from the ROB into the architectural register file.",
    ]))
    A(formula("Rename removes WAR and WAW (name) dependences;\n"
              "RAW (true) dependences remain — they carry real data.\n\n"
              "Flow:  Issue → update RAT ;  Execute → produce value ;\n"
              "       Write → store value in ROB ;  Commit → copy ROB value to ARF"))
    A(p("<b>Reconstructed diagram.</b> Draw the architectural register file (ARF) on the left, the "
        "physical registers / ROB on the right, and the RAT as a table in the middle mapping each "
        "architectural name to a physical name."))
''',
 pyqs=[34, 39])

PAGES[43] = dict(
 title="Reservation-station fields and the common data bus (CDB)",
 transcript="""Source → register from which to read the operand value.

Reservation station fields:
   Op    — the operation to perform
   Qj, Qk — the reservation stations that will produce Vj, Vk
   Vj, Vk — the operand values (if already available)
   A      — the address / immediate (for loads/stores)
   Busy   — whether the station is occupied

CDB (Common Data Bus): broadcasts results to all waiting stations.
  If busy = 0, the station is free; else it is waiting.

Result tag → identifies which instruction produced a value on the CDB.""",
 explain=r'''
    A(p("<b>What the page says.</b> The <b>reservation station</b> is the heart of Tomasulo’s algorithm. "
        "This page lists its fields — a favourite exam question."))
    A(table(["Field","Meaning"],
      [["Op","Operation to perform (ADD, MUL, LOAD, …)"],
       ["Vj, Vk","Operand values, if already available"],
       ["Qj, Qk","Names (tags) of the stations that will produce Vj, Vk (blank if the value is ready)"],
       ["A","Address or immediate field (used by load/store)"],
       ["Busy","1 if the station is occupied, 0 if free"]],
      widths=[1.2,5.3]))
    A(formula("Rule:  if Qj = 0 then Vj holds the value;  if Qj ≠ 0 then wait for\n"
              "       the result broadcast with tag Qj.\n"
              "CDB: when a unit finishes, it broadcasts (tag, value) to ALL stations\n"
              "     and to the register file; any station with a matching Q grabs the value."))
    A(p("<b>Why it works.</b> A station never reads a value until it is actually produced. When the "
        "producing unit finishes it puts the result on the <b>common data bus</b> tagged with the "
        "producer’s name; every waiting station compares its Q fields with that tag and, if they match, "
        "stores the value and clears the Q field."))
''',
 pyqs=[])

PAGES[44] = dict(
 title="Tomasulo tables — instruction status and reservation stations",
 transcript="""Tomasulo tables:

  Instruction status:
    Instruction | j | k | Issue | Execute | Write result

  Reservation stations:
    Name | Busy | Op | Vj | Vk | Qj | Qk | A

  Register result status:
    F0 F1 F2 ... — which station will produce each register

  (Example:  MUL F0, F2, F4  ;  ADD F6, F2, F4 ;  SUB F8, F6, F2 ; ...)

  Numbers:  cycles 1,2,3 ;  latency 2 cycles etc.""",
 explain=r'''
    A(p("<b>What the page says.</b> The three tables you must fill in for any Tomasulo question, with a "
        "small worked example."))
    A(table(["Table","Columns"],
      [["Instruction status","Instruction, j, k, Issue, Execute, Write Result"],
       ["Reservation stations","Name, Busy, Op, Vj, Vk, Qj, Qk, A"],
       ["Register result status","for each register: which station will write it"]],
      widths=[1.7,4.8]))
    A(formula("Example code:\n"
              "  MUL F0, F2, F4     ; F0 = F2 × F4\n"
              "  ADD F6, F2, F4     ; F6 = F2 + F4\n"
              "  SUB F8, F6, F2     ; F8 = F6 − F2\n"
              "The MUL and ADD can start together (both read F2, F4);\n"
              "the SUB must wait for F6 (Qj = the ADD’s station)."))
    A(callout("<b>Exam method.</b> Go cycle by cycle: at each cycle (1) issue any instruction whose "
        "reservation station is free, filling Qj/Qk with the tags of the producers or Vj/Vk with ready "
        "values; (2) start execution when Qj = Qk = 0; (3) broadcast the result and clear matching Q "
        "fields. Record the cycle numbers in the instruction-status table.", 'tip'))
''',
 pyqs=[])

PAGES[45] = dict(
 title="Parallelisation, CPI and the basics of branches",
 transcript="""Parallelisation reduces CPI:
   CPI_ideal = 1 ;  CPI = CPI_ideal + stalls

Compiler/benchmark uses dependence information to schedule instructions.

Hardware branch handling: register renaming, reorder buffer (ROB).

Parallelism reduces CPI (pipeline):  T = IC × CPI / f

Basics of branches:
  * Free list of registers, used as renaming targets.
  * Branches occur more often than expected.
  * Q = branch ? taken : not-taken …""",
 explain=r'''
    A(p("<b>What the page says.</b> The bridge from pipelining to dynamic scheduling: parallelism and "
        "renaming reduce the effective CPI, and branches are the main obstacle because they are frequent."))
    A(formula("CPI = CPI_ideal + stall_cycles_per_instruction\n"
              "     = 1 + (branch_penalty + load_use_stalls + …)\n"
              "T = IC × CPI / f"))
    A(bullets([
        "Pipelining makes CPI_ideal = 1; every hazard adds stalls on top.",
        "The compiler uses dependence information to schedule instructions and reduce stalls.",
        "Branches are common (roughly one in five instructions), so their cost matters a great deal.",
        "Hardware techniques — register renaming and the reorder buffer — let the processor keep working "
        "past a branch and past a false dependence.",
    ]))
''',
 pyqs=[])

PAGES[46] = dict(
 title="Data dependences — RAW, WAR and WAW",
 transcript="""Dependences:
  True dependence (RAW): read-after-write — a later instruction reads a value an earlier one wrote.
  Anti-dependence (WAR): write-after-read — a later write would overwrite a value still needed.
  Output dependence (WAW): write-after-write — two writes to the same location.

  Register renaming removes WAR and WAW (name dependences);
  RAW (true) dependence remains.

  Example:  A = e + f ;  B = ... ; C = A + 1 …

  RAW (data dependence) — must be honoured.""",
 explain=r'''
    A(p("<b>What the page says.</b> The three kinds of register dependence, and the key fact that "
        "renaming removes two of them."))
    A(table(["Dependence","Also called","Meaning","Removed by renaming?"],
      [["RAW","True / flow","Later reads what earlier wrote","No — it is real data flow"],
       ["WAR","Anti","Later writes a value still being read","Yes (it is a name clash)"],
       ["WAW","Output","Two writes to the same register","Yes (it is a name clash)"]],
      widths=[0.9,1.0,2.6,2.0]))
    A(formula("Example:\n"
              "  I1:  F0 = F2 + F4\n"
              "  I2:  F6 = F0 − F8     ; RAW on F0 (must wait for I1)\n"
              "  I3:  F0 = F10 × F12   ; WAW on F0 with I1, WAR with I2 → renaming removes these\n"
              "After renaming, I3 writes a DIFFERENT physical register, so it can\n"
              "execute without waiting for I1 or I2."))
    A(callout("<b>The one-line summary.</b> RAW is a true dependence and cannot be removed — the data "
        "really must flow. WAR and WAW are only name clashes caused by reusing a small set of register "
        "names; give each new value a fresh name and they vanish.", 'tip'))
''',
 pyqs=[14, 22])

PAGES[47] = dict(
 title="Tomasulo worked example (loop) with reservation-station tables",
 transcript="""Tomasulo — loop example:

  Loop:  L.D  F0, 0(R1)
         MUL.D F4, F0, F2
         S.D  F4, 0(R1)
         ADD.D R1, R1, #-8     (or DADDIU R1, R1, -8)
         BNE  R1, R2, Loop

  Tables:
   Iteration 1: Load1, Mult1, Store1, Add1, ...
   Register result status per cycle.

  (Instruction status and reservation-station tables filled cycle by cycle.)""",
 explain=r'''
    A(p("<b>What the page says.</b> A full Tomasulo example on a loop — the classic exam question. The "
        "processor must keep several loop iterations in flight using the reservation stations."))
    A(formula("Loop body (the canonical example):\n"
              "  L.D    F0, 0(R1)      ; load A[i]\n"
              "  MUL.D  F4, F0, F2     ; multiply by scalar\n"
              "  S.D    F4, 0(R1)      ; store A[i]\n"
              "  DADDUI R1, R1, #-8    ; decrement pointer\n"
              "  BNE    R1, R2, Loop   ; branch back"))
    A(bullets([
        "The <b>Load</b> stations hold the address; the <b>Mult</b> stations hold the multiplier operands; "
        "the <b>Store</b> stations hold the store address and the value to store.",
        "Because the loop iterations are independent (different addresses), Tomasulo can overlap them: "
        "load i+1 can start while multiply i is still running.",
        "The register result status table shows, for each register, which station will write it — this is "
        "how the hardware tracks the RAW dependences without stalling everything.",
    ]))
    A(p("The full transcription of the printed question and the cycle-by-cycle solution are given in the "
        "past-paper solutions (ca12, ca18, ca34, ca39, ca40)."))
''',
 pyqs=[12, 18])

PAGES[48] = dict(
 title="Tomasulo example with a small FP unit and load/store buffers",
 transcript="""Tomasulo — small example:

  FP ALU operations  — 1 unit, latency 3
  FP load/store      — 1 unit, latency 2
  Load:   L.D  F0, 0(R1)
  ...
  ADD.D  F4, F0, F2
  ...
  S.D    F4, 0(R2)

  (Reservation-station table with Qj/Qk tags and Vj/Vk values.)""",
 explain=r'''
    A(p("<b>What the page says.</b> A compact Tomasulo example with stated unit latencies, so the "
        "cycle numbers can be computed exactly."))
    A(formula("Given:  FP add/mul latency = 3 cycles ;  load latency = 2 cycles\n"
              "Code:   L.D  F0, 0(R1)\n"
              "        ADD.D F4, F0, F2\n"
              "        S.D   F4, 0(R2)\n\n"
              "The ADD must wait for F0 (Qj = Load1); the store must wait for F4\n"
              "(Qk = Add1). Execution starts when both operands are ready and the\n"
              "functional unit is free."))
    A(p("Follow the three steps for every instruction — Issue, Execute, Write result — and record the "
        "cycle numbers. The reservation-station table shows the Q/V fields changing as results are "
        "broadcast on the CDB."))
''',
 pyqs=[])

PAGES[49] = dict(
 title="Loop unrolling — the DAXPY example",
 transcript="""Unrolling:

  L.D   F0, ...
  ADD.D F4, F0, F2
  S.D   F4, ...

  DAXPY:  Y[i] = a·X[i] + Y[i]

  Unroll the loop so that several iterations are done per pass,
  reducing loop overhead (the branch and pointer update).

  Loop unrolling: reduces the number of branches and exposes
  independent operations to schedule.""",
 explain=r'''
    A(p("<b>What the page says.</b> <b>Loop unrolling</b> repeats the loop body several times per "
        "iteration so that the loop-control instructions (branch, pointer update, counter) are amortised "
        "and more independent work is exposed to the scheduler."))
    A(formula("DAXPY:  for i = 0 … n−1:   Y[i] = a · X[i] + Y[i]\n"
              "  MIPS:  L.D   F0, 0(R1)      ; load X[i]\n"
              "         MUL.D F4, F0, F2      ; a · X[i]\n"
              "         L.D   F6, 0(R2)       ; load Y[i]\n"
              "         ADD.D F6, F4, F6      ; a·X[i] + Y[i]\n"
              "         S.D   F6, 0(R2)       ; store Y[i]\n"
              "         DADDUI R1, R1, #8 ; DADDUI R2, R2, #8 ; BNE …"))
    A(bullets([
        "<b>Why unroll?</b> Each pass still pays for the pointer updates and the branch, but does more "
        "useful work.",
        "<b>Effect on CPI:</b> fewer branches ⇒ fewer control hazards; more independent instructions ⇒ "
        "the scheduler can fill the delay slots.",
        "<b>Cost:</b> larger code (more instruction-cache pressure) and more registers needed to hold the "
        "independent values.",
    ]))
''',
 pyqs=[])

PAGES[50] = dict(
 title="Loop unrolling worked example (3× unrolled DAXPY)",
 transcript="""Unrolled DAXPY (3×):

  L.D   F0, 0(R1)
  L.D   F6, -8(R1)
  L.D   F10, -16(R1)
  L.D   F14, -24(R1)
  MUL.D F4, F0, F2
  MUL.D F8, F6, F2
  MUL.D F12, F10, F2
  MUL.D F16, F14, F2
  ADD.D F4, F4, F6
  ADD.D F8, F8, F10
  ADD.D F12, F12, F14
  S.D   F4, 0(R1)
  S.D   F8, -8(R1)
  S.D   F12, -16(R1)
  DADDUI R1, R1, #-32
  BNE   R1, R2, Loop

  (Reordering removes stalls; redundant computation removed.)""",
 explain=r'''
    A(p("<b>What the page says.</b> A 3× (really 4-element) unrolled DAXPY, showing the classic "
        "technique of loading several elements, multiplying them all, adding them all, and storing them "
        "all — so that long-latency operations overlap."))
    A(formula("Schedule idea:\n"
              "  • issue all the LOADS first (independent) — they overlap,\n"
              "  • then all the MULTIPLIES,\n"
              "  • then all the ADDs,\n"
              "  • then all the STOREs,\n"
              "  • one pointer update and one branch for the whole group."))
    A(bullets([
        "The compiler must give each unrolled iteration its <b>own registers</b> (F0, F6, F10, F14 …) so "
        "the operations are independent — otherwise a false (WAW/WAR) dependence would serialise them.",
        "It also <b>removes redundant computation</b> (e.g. re-loading the same scalar, or the "
        "loop-overhead work done once instead of per element).",
        "Unrolling exposes ILP; scheduling then fills the delay slots with useful work so the pipeline "
        "does not stall.",
    ]))
''',
 pyqs=[11])

PAGES[51] = dict(
 title="Unroll until no stalls — the scheduled loop",
 transcript="""Unroll until no stalls:

  L.D   F0, ...
  L.D   F6, ...
  L.D   F10, ...
  L.D   F14, ...
  (then the multiply / add / store schedule)
  ...
  S.D   F4, ...
  S.D   F8, ...
  S.D   F12, ...
  S.D   F16, ...
  DADDUI R1, R1, #-32
  BNE   R1, R2, Loop

  No stalls: every load-use gap is filled by an independent instruction.

  Disadvantages: loop overhead, larger code, more registers.

  Loop unrolling: reducing the overhead of branches.""",
 explain=r'''
    A(p("<b>What the page says.</b> The goal of unrolling is to reach a schedule in which <i>no</i> stall "
        "cycles are needed — every load-use delay is filled with an independent instruction."))
    A(formula("To remove every load-use stall, unroll enough times that the\n"
              "number of independent instructions ≥ the load latency.\n"
              "Example: load latency = 4 cycles ⇒ unroll ~4× and interleave."))
    A(bullets([
        "<b>Benefit:</b> the loop runs at (or near) one element per cycle with no pipeline bubbles.",
        "<b>Disadvantage 1 — loop overhead:</b> the counter, pointer updates and branch are still there, "
        "just amortised.",
        "<b>Disadvantage 2 — code size:</b> unrolled code is larger, so it may not fit in the instruction "
        "cache.",
        "<b>Disadvantage 3 — register pressure:</b> more live values need more registers.",
    ]))
    A(callout("<b>The trade-off.</b> Unroll too little and stalls remain; unroll too much and the code no "
        "longer fits in the I-cache or the registers spill. The sweet spot depends on the latencies and "
        "the cache size.", 'tip'))
''',
 pyqs=[24])

PAGES[52] = dict(
 title="Instruction scheduling rules (dynamic and static)",
 transcript="""Dynamic scheduling:
  Reorder the execution order of instructions.

  Advantages — doesn’t need the compiler; handles dependences at run time;
  can exploit ILP that the compiler cannot see.

  Compile-time (static) scheduling: the compiler reorders instructions.

  Instructions → fixed pipeline, so scheduling must avoid stalls.

  Rules for reordering instructions:
   1) One register per instruction (no false dependences),
   2) Allow for latency (respect the real delays),
   3) Do not move a load/store past a conflicting memory access,
   4) Do not move a branch (control) past a dependent instruction,
   5) Do not move a WAW/WAR pair unless renamed.

  Example:
    ADD F4, F0, F2
    MUL F4, ...   (WAR) → reorder or rename""",
 explain=r'''
    A(p("<b>What the page says.</b> The rules the scheduler (hardware or compiler) must obey when it "
        "reorders instructions to remove stalls."))
    A(bullets([
        "<b>1) Respect RAW.</b> Never move an instruction before the instruction that produces its input.",
        "<b>2) Respect latency.</b> Keep independent instructions between a producer and its consumer to "
        "cover the delay.",
        "<b>3) Respect memory dependences.</b> A load or store must not be moved past another memory "
        "access to the same address.",
        "<b>4) Respect control dependences.</b> Do not move an instruction past the branch it depends on "
        "(unless speculating).",
        "<b>5) Rename away WAW/WAR.</b> If two instructions clash on a name but not on real data, give "
        "them different registers so they can be reordered.",
    ]))
    A(formula("Example (WAR clash):\n"
              "  ADD  F4, F0, F2\n"
              "  MUL  F4, F6, F8     ; writes F4 again (WAW with the ADD)\n"
              "Fix by renaming the second destination:\n"
              "  ADD  F4, F0, F2\n"
              "  MUL  F10, F6, F8    ; now independent — can be reordered freely"))
    A(callout("<b>Static vs dynamic.</b> <i>Static</i> scheduling is done by the compiler at build time "
        "(fixed for the pipeline). <i>Dynamic</i> scheduling is done by the hardware at run time "
        "(scoreboard, Tomasulo) and can adapt to conditions the compiler cannot foresee — e.g. a cache "
        "miss.", 'tip'))
''',
 pyqs=[28])
