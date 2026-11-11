"""Page-by-page annotations for handwritten pages 53-70."""

PAGES = {}

PAGES[53] = dict(
 title="Precise exceptions and speculation (exceptions in flight)",
 transcript="""Precise exceptions:  when an exception occurs, the state must be exactly as if
  instructions before it completed and none after it started.

  Handling imprecise exceptions: exceptions must not corrupt the state.
  In-order commit.

  Speculation:  allow instructions to execute before it is known whether they
  should execute.

  Example (MUL → previous instructions):
    Issue MUL, execute, write back; if an earlier instruction takes an
    exception, the MUL must be discarded (squashed).

  Two kinds of pairs: {taken, not-taken} — branch outcomes.""",
 explain=r'''
    A(p("<b>What the page says.</b> <b>Precise exceptions</b> require that when an instruction faults, "
        "the machine state is exactly as if all earlier instructions finished and no later one began. "
        "<b>Speculation</b> lets the processor run ahead (e.g. past a branch) but then forces "
        "<i>in-order commit</i> so that a wrong guess can be discarded cleanly."))
    A(bullets([
        "<b>Precise exception</b> — the register and memory state is consistent with the program order at "
        "the point of the faulting instruction.",
        "<b>Speculation</b> — execute instructions that might not belong to the final path (past a "
        "predicted branch), keeping their results in a buffer.",
        "<b>Squash / flush</b> — if the guess was wrong (or an earlier instruction faults), throw away "
        "the speculative results and restart from the correct point.",
        "<b>In-order commit</b> — results become visible (written to the architectural state) strictly in "
        "program order, which is what makes exceptions precise.",
    ]))
    A(formula("MUL F0, F2, F4    ; execute speculatively\n"
              "… if an earlier instruction raises an exception, the MUL’s result\n"
              "  must NOT be committed — it is squashed and the register file is\n"
              "  restored to the state before the faulting instruction."))
''',
 pyqs=[])

PAGES[54] = dict(
 title="Tomasulo hardware — the full datapath with a reorder buffer and CDB",
 transcript="""Tomasulo’s Algorithm (hardware block diagram):

  From instruction unit → Instruction queue
  Load/store operations → Load buffers / Store address & data
  FP registers
  Operand buses
  Address unit
  FP adders, FP multipliers
  Reservation stations
  Common Data Bus (CDB)
  Reorder buffer
  Load data

  (Busy / Address / Op / Vj / Vk / Qj / Qk fields shown in the stations.)""",
 explain=r'''
    A(p("<b>What the page says.</b> The complete Tomasulo datapath. This is the diagram to reproduce in "
        "the exam."))
    A(bullets([
        "<b>Instruction queue</b> — holds decoded instructions waiting to issue.",
        "<b>Reservation stations</b> — one group per functional unit (add, multiply, load, store); each "
        "holds an instruction’s op and operands, with Qj/Qk tags for missing values.",
        "<b>Functional units</b> — the FP adders and multipliers that execute; they put their results on "
        "the CDB.",
        "<b>Load/store buffers</b> — hold the address and data for memory operations.",
        "<b>Common Data Bus (CDB)</b> — broadcasts (tag, value) from a finishing unit to every station and "
        "to the register file.",
        "<b>Register file / result status</b> — for each register, which station will produce it.",
        "<b>Reorder buffer</b> — added for speculation; holds results until commit, in program order.",
    ]))
    A(formula("Data flow:  queue → reservation station → (operands ready?) →\n"
              "functional unit → CDB broadcast → waiting stations grab the value →\n"
              "ROB holds the result until in-order commit → register file."))
    A(p("<b>How to draw it.</b> Left to right: instruction queue, then the reservation-station groups, "
        "then the functional units; a single horizontal <b>CDB</b> line runs across, tapped by every "
        "station and by the register file. The ROB sits between the units and the register file."))
''',
 pyqs=[])

PAGES[55] = dict(
 title="Speculation — issue, execute, read, write and commit",
 transcript="""Speculation:  out-of-order execution with completion.

  Can do a load early:
   1) Fetch
   2) Issue / execute (out of order)
   3) Write result (but not to architectural state yet)
   4) Commit (in order) — only then is the state updated

  Cannot commit out of order:
   1) Fetch,
   2) Execute,
   3) Commit — when all prior instructions have committed,
   4) The result is written to the register file / memory.

  Commit stage = in-order update of the architectural state.""",
 explain=r'''
    A(p("<b>What the page says.</b> The five stages of a speculative pipeline. The first four may run "
        "out of order; the last one (commit) is strictly in program order."))
    A(table(["Stage","In order?","What happens"],
      [["1 Issue","yes","Get the instruction into the machine"],
       ["2 Execute","no","Run when the operands are ready"],
       ["3 Read","no","Read operands from the CDB / register file"],
       ["4 Write","no","Write the result into the ROB (speculative)"],
       ["5 Commit","yes","Copy the ROB value into the architectural state"]],
      widths=[1.0,0.9,4.6]))
    A(formula("Issue  → Execute → Read → Write (ROB) → Commit (in order)\n"
              "Only Commit changes the visible state; a mispredicted branch\n"
              "squashes the speculative entries before they commit."))
    A(callout("<b>Why this ordering gives precise exceptions.</b> Because commit is in order, a faulting "
        "instruction can be handled exactly at its point in the program: everything before it has "
        "committed, everything after it is still speculative and can be discarded.", 'tip'))
''',
 pyqs=[25, 40])

PAGES[56] = dict(
 title="Tomasulo instruction-status table (worked)",
 transcript="""Instruction status:

  Instruction   j    k    Issue   Execute   Write Result
  --------------------------------------------------------
  L.D  F6, 34(R2)      ...
  L.D  F2, 45(R3)      ...
  MUL.D F0, F2, F4     ...
  SUB.D F8, F6, F2     ...
  DIV.D F10, F0, F6    ...
  ADD.D F6, F8, F2     ...

  (Issue / Execute / Write-result cycles filled in.)

  Read (operand) values:
    Qj = station producing Vj ;  Qk = station producing Vk
    Values read from the register file when Q = 0.""",
 explain=r'''
    A(p("<b>What the page says.</b> The instruction-status table for the canonical Tomasulo example, "
        "with the Issue, Execute and Write-result cycles recorded."))
    A(formula("Canonical code and the table to fill:\n"
              "  L.D   F6, 34(R2)\n"
              "  L.D   F2, 45(R3)\n"
              "  MUL.D F0, F2, F4     ; depends on L.D F2\n"
              "  SUB.D F8, F6, F2     ; depends on both loads\n"
              "  DIV.D F10, F0, F6    ; depends on MUL and L.D F6\n"
              "  ADD.D F6, F8, F2     ; depends on SUB and L.D F2"))
    A(p("<b>How to fill it.</b> At each cycle, for each instruction record when it <i>issues</i> (a "
        "station is free), when it <i>starts executing</i> (both operands ready and the unit is free) and "
        "when it <i>writes its result</i> (the unit finishes and broadcasts on the CDB)."))
''',
 pyqs=[])

PAGES[57] = dict(
 title="Tomasulo — instruction-status and reservation-station tables (worked, cycles 1–10)",
 transcript="""Worked Tomasulo example:

  Clock:  1 2 3 4 5 6 7 8 9 10

  L.D   F6, 34(R2)     ; Load1
  L.D   F2, 45(R3)     ; Load2
  MUL.D F0, F2, F4     ; Mult1
  SUB.D F8, F6, F2     ; Add1
  DIV.D F10, F0, F6    ; Mult2
  ADD.D F6, F8, F2     ; Add2

  Reservation stations:
   Name  Busy  Op   Vj   Vk   Qj   Qk   A
   Load1  Yes  Load  -    -    -    -   34+R2
   Load2  Yes  Load  -    -    -    -   45+R3
   Add1   Yes  SUB  Mem  -    Load1 Load2 -
   Mult1  Yes  MUL  -    -    Load2  -   -
   ...""",
 explain=r'''
    A(p("<b>What the page says.</b> The complete worked Tomasulo example with both tables filled in "
        "cycle by cycle. This is exactly what an exam question asks you to produce."))
    A(formula("Reservation-station fields at issue time (example):\n"
              "  Add1 (SUB): Op=SUB, Qj=Load1 (needs F6), Qk=Load2 (needs F2)\n"
              "  Mult1 (MUL): Op=MUL, Qj=Load2 (needs F2), Vk=F4 (ready)\n"
              "  Mult2 (DIV): Op=DIV, Qj=Mult1 (needs F0), Qk=Load1 (needs F6)\n"
              "  Add2 (ADD): Op=ADD, Qj=Add1 (needs F8), Qk=Load2 (needs F2)"))
    A(bullets([
        "The loads issue first; when Load1 finishes it broadcasts its value on the CDB, so Add1 and Mult2 "
        "clear their Qj/Qk fields.",
        "MUL can start as soon as F2 arrives; DIV waits for both F0 (from MUL) and F6.",
        "Each broadcast frees every waiting station at once — this is the parallelism Tomasulo exploits.",
    ]))
    A(p("The full transcription of the printed question and the complete cycle-by-cycle solution are "
        "given in the past-paper solutions (ca12)."))
''',
 pyqs=[])

PAGES[58] = dict(
 title="Tomasulo tables (continued — second worked set)",
 transcript="""Tomasulo — second worked set:

  L.D   F2, 45(R3)
  L.D   F6, 0(R2)
  MUL.D F0, F2, F4
  SUB.D F8, F6, F2
  DIV.D F10, F0, F6
  ADD.D F6, F8, F2

  Reservation stations (Load1, Load2, Add1, Add2, Mult1, Mult2)
  and register result status (which station writes each F register).""",
 explain=r'''
    A(p("<b>What the page says.</b> A second worked Tomasulo set with the same structure but different "
        "latencies, to practise filling the tables."))
    A(formula("Register result status at the start (example):\n"
              "  F0 → Mult1 (MUL.D)\n"
              "  F6 → Load2, then Add2\n"
              "  F8 → Add1 (SUB.D)\n"
              "  F10 → Mult2 (DIV.D)"))
    A(p("Work through it exactly as on page 57: issue, execute when operands are ready, write result on "
        "the CDB, and update the register-result-status table as each producer changes."))
''',
 pyqs=[])

PAGES[59] = dict(
 title="Tomasulo tables (continued — with cycle numbers)",
 transcript="""Tomasulo — cycles:

  L.D   F6, 34(R2)   ; cycle 1 issue
  L.D   F2, 45(R3)   ; cycle 2
  MUL.D F0, F2, F4   ; cycle 3
  SUB.D F8, F6, F2   ; cycle 4
  DIV.D F10, F0, F6  ; cycle 5
  ADD.D F6, F8, F2   ; cycle 6

  (Execute and write-result cycles computed from the latencies.)""",
 explain=r'''
    A(p("<b>What the page says.</b> The same example with explicit cycle numbers, showing how the issue "
        "order and the operand-ready times determine the schedule."))
    A(formula("Rule for the Execute column:\n"
              "  Execute_start = max(issue cycle + 1, cycle when last operand arrives,\n"
              "                      cycle when the functional unit becomes free)\n"
              "  Write_result  = Execute_start + latency"))
    A(p("This is the arithmetic that turns the tables into a schedule. Practise it with the printed "
        "question in the past-paper solutions (ca12)."))
''',
 pyqs=[])

PAGES[60] = dict(
 title="Tomasulo tables (continued — final set)",
 transcript="""Tomasulo — final worked set:

  ADD.D F2, F4, F6
  ...
  SUB.D F8, F2, F6
  MUL.D F10, F2, F6
  ...
  (register result status: F2 → Add1, F8 → Add2, F10 → Mult1 …)

  Two classes of stalls identified.""",
 explain=r'''
    A(p("<b>What the page says.</b> The last Tomasulo worked set, ending with a note that stalls fall "
        "into two classes."))
    A(formula("The two classes of stall:\n"
              "  1) RAW / data stall — waiting for a real operand (Qj or Qk non-zero).\n"
              "  2) Structural stall — the required functional unit or station is busy.\n"
              "Tomasulo removes the WAR/WAW stalls (via renaming) but keeps RAW and structural ones."))
    A(p("This completes the Tomasulo block of the notes. The ideas are consolidated in the past-paper "
        "solutions (ca12, ca18, ca34, ca39, ca40)."))
''',
 pyqs=[])

PAGES[61] = dict(
 title="Superscalar processors and vector operations",
 transcript="""Superscalar Processors:

  Issue multiple instructions per cycle.

  Needs:
   1) Multiple functional units,
   2) Wide instruction fetch (fetch several instructions at once),
   3) Dependence checking in hardware,
   4) Wide CDB / multiple buses,
   5) Register renaming.

  Vector operations:
   Operate on whole vectors (arrays) with one instruction.

  Loop operations:  the vector instruction replaces the whole loop.""",
 explain=r'''
    A(p("<b>What the page says.</b> What it takes to issue more than one instruction per cycle "
        "(superscalar), and how a vector instruction replaces a whole loop."))
    A(bullets([
        "<b>Multiple functional units</b> — several adders, multipliers, load/store units so more than "
        "one operation can run at once.",
        "<b>Wide instruction fetch</b> — the front end must deliver several instructions per cycle, which "
        "usually means a large instruction cache and alignment handling.",
        "<b>Dependence checking</b> — hardware must detect which of the fetched instructions can go "
        "together.",
        "<b>Wide CDB / multiple buses</b> — several results must be broadcast in the same cycle.",
        "<b>Register renaming</b> — to remove false dependences so the parallel issue slots can be filled.",
    ]))
    A(formula("Superscalar width m (ideal):  IPC ≤ m ,  CPI ≥ 1/m\n"
              "Real IPC < m because of dependences, hazards and fetch limits.\n\n"
              "Vector:  one instruction operates on VL elements:\n"
              "  e.g.  ADDV V1, V2, V3   →   V1[i] = V2[i] + V3[i]  for i = 0…VL−1"))
    A(callout("<b>Superscalar vs vector.</b> Superscalar exploits ILP (independent scalar instructions); "
        "vector exploits DLP (the same operation on many data). GPUs combine both.", 'tip'))
''',
 pyqs=[])

PAGES[62] = dict(
 title="Vector/loop example and loop scheduling with loads",
 transcript="""Vector / loop example:

  L.D   F0, 0(R1)
  Stall
  ADD.D F4, F0, F2
  Stall
  S.D   F4, 0(R1)
  DADDUI R1, R1, #-8
  BNE   R1, R2, Loop

  Loop scheduling:
   Several iterations interleaved so the loads of one fill the stalls of another.

  Vector version:
   L.D   F0, 0(R1)   →   load a whole vector
   ADDV  V1, V0, V2
   S.D   V1, 0(R1)

  (Load latency 6, FP latency 4 …)""",
 explain=r'''
    A(p("<b>What the page says.</b> The scalar loop with its stalls, and how scheduling (or a vector "
        "instruction) removes them."))
    A(formula("Scalar (with stalls):\n"
              "  L.D   F0, 0(R1)      ; load latency ≈ 6 cycles\n"
              "  ADD.D F4, F0, F2     ; must wait for F0 → stall\n"
              "  S.D   F4, 0(R1)\n"
              "  DADDUI R1, R1, #-8\n"
              "  BNE   R1, R2, Loop\n\n"
              "Scheduled (interleave iterations): the load of iteration i+1 fills the\n"
              "stall of iteration i, so the loop runs with no bubbles."))
    A(p("<b>Vector version.</b> Replace the loop with vector instructions: one load brings in a whole "
        "vector, one ADDV adds the vectors element-wise, one store writes them back. The loop control "
        "disappears and the hardware pipelines the vector lanes."))
''',
 pyqs=[])

PAGES[63] = dict(
 title="Loop scheduling with speculation",
 transcript="""Loop scheduling with speculation:

  LOOP:  L.D   F0, 0(R1)
         ADD.D F4, F0, F2
         S.D   F4, 0(R1)
         DADDUI R1, R1, #-8
         BNE   R1, R2, LOOP

  Speculative execution: run the next iteration before the branch is resolved.

  Two versions shown side by side:
   (a) scheduled without speculation,
   (b) scheduled with speculation (branch predicted).""",
 explain=r'''
    A(p("<b>What the page says.</b> Combining scheduling with speculation: start the next loop iteration "
        "before the branch that controls the loop has resolved, then commit only if the prediction was "
        "right."))
    A(formula("Without speculation: the loop body waits for the BNE to resolve,\n"
              "  so the pipeline drains at every iteration.\n\n"
              "With speculation: predict the branch taken, fetch and execute the\n"
              "  next iteration immediately; keep its results in the ROB and commit\n"
              "  them only if the branch really was taken."))
    A(callout("<b>Why speculation is powerful here.</b> A loop branch is almost always taken, so the "
        "predictor is right nearly every time and the pipeline never drains — the loop runs at full "
        "throughput.", 'tip'))
''',
 pyqs=[])

PAGES[64] = dict(
 title="Loop scheduling with speculation (continued)",
 transcript="""(Continuation.)
  LOOP:  L.D   F0, 0(R1)
         ADD.D F4, F0, F2
         S.D   F4, 0(R1)
         DADDUI R1, R1, #-8
         BNE   R1, R2, LOOP

  Scheduled speculatively: the loads/adds/stores of consecutive iterations
  are interleaved, with the branch predicted taken each time.""",
 explain=r'''
    A(p("<b>What the page says.</b> The speculative schedule laid out fully, showing the interleaving of "
        "successive iterations."))
    A(formula("Speculative schedule (sketch):\n"
              "  L.D(i)  L.D(i+1)  ADD(i)  L.D(i+2)  ADD(i+1)  S.D(i)  ADD(i+2) …\n"
              "Each load is followed, several instructions later, by its use — enough\n"
              "independent work in between to cover the load latency."))
    A(p("The two columns of the page are the same schedule with and without speculation; with "
        "speculation the branch no longer forces a drain, so the interleaving is tighter."))
''',
 pyqs=[])

PAGES[65] = dict(
 title="Speculation timing table (issue / execute / read / write / commit)",
 transcript="""With speculation — timing table:

  Iteration | Issue | Execute | Read | Write | Commit
  ----------+-------+---------+------+-------+-------
     1      |   1   |    2    |  4   |   5   |   7
     1      |   2   |    3    |  5   |   6   |   8
     ...
  (cycles across the top: 1 2 3 4 5 6 7 8 9 10 11 12 …)

  The commit column is strictly in order, later than the write column.""",
 explain=r'''
    A(p("<b>What the page says.</b> The timing table for the speculative pipeline, with a column for "
        "each of the five stages. Notice that the Commit column is monotonic (in order) even though the "
        "other columns may be out of order."))
    A(formula("Five columns:  Issue → Execute → Read → Write → Commit\n"
              "  • Issue and Execute can be out of order;\n"
              "  • Write places the result in the ROB;\n"
              "  • Commit is strictly increasing (program order)."))
    A(p("<b>How to read it.</b> Pick an instruction row and follow it across: it issues at some cycle, "
        "executes when its operands are ready, reads them, writes its result into the ROB, and finally "
        "commits. Because commit is in order, a later instruction may write before an earlier one but "
        "never commits before it."))
''',
 pyqs=[])

PAGES[66] = dict(
 title="Speculation timing table (continued)",
 transcript="""With speculation (continued):

  Time | Execute | Read | Write | CDB | Commit
  -----+---------+------+-------+-----+-------
   ... (the table continues, showing the CDB broadcast and the commit order)

  Commit is the final, in-order stage; the CDB carries the values between
  the functional units and the waiting reservation stations.""",
 explain=r'''
    A(p("<b>What the page says.</b> The continuation of the speculation timing table, adding the CDB "
        "broadcast column."))
    A(formula("Columns:  Time | Execute | Read | Write | CDB | Commit\n"
              "The CDB column marks the cycle in which the result is broadcast\n"
              "(and thus grabbed by every waiting station)."))
    A(p("This completes the speculation block of the notes. The full printed questions on speculation "
        "and the ROB are solved in the past-paper solutions (ca25, ca28, ca39, ca40)."))
''',
 pyqs=[])

PAGES[67] = dict(
 title="Blank / illegible page",
 transcript="""(No legible content. Only a stray word — “Defra…” — is visible;
the page is effectively blank.)""",
 explain=r'''
    A(p("This page carries no academic content — it is a blank page in the notes with only an "
        "illegible fragment. It is recorded here so that the page numbering stays aligned with the "
        "original; there is nothing to learn from it."))
''',
 pyqs=[])

PAGES[68] = dict(
 title="UMA shared memory and multicore with private caches",
 transcript="""UMA (Uniform Memory Access):

  [Core]  [Core]  [Core]  [Core]
     \\      |       |      /
      \\     |       |     /
   ========== shared bus ==========
              |
        [Shared main memory]

  Multicore: several cores, each with a private cache, sharing main memory
  through a common interconnect.

  (Cache coherence is needed because the private caches may hold copies
  of the same block.)""",
 explain=r'''
    A(p("<b>What the page says.</b> The UMA multiprocessor picture: several cores, each with a private "
        "cache, all connected to one shared memory by a common interconnect."))
    A(bullets([
        "<b>UMA</b> — every core reaches the shared memory in the same time, hence “uniform”.",
        "<b>Private caches</b> are what make the machine fast (each core keeps its working set close), "
        "but they also mean the same memory block can live in several caches at once.",
        "That duplication is exactly the <b>cache-coherence problem</b>: if one core writes a block, the "
        "copies in the other caches become stale.",
    ]))
    A(formula("Shared bus bandwidth is divided among the cores:\n"
              "  per-core bandwidth ≈ BW_total / n   → falls as n grows\n"
              "  (this is why UMA/bus designs do not scale to many cores)"))
    A(p("<b>Reconstructed diagram.</b> Draw the cores in a row at the top, each with a small private "
        "cache box; a single horizontal bus below them; and the shared memory at the bottom. An arrow "
        "shows that all traffic must pass through the one bus."))
''',
 pyqs=[])

PAGES[69] = dict(
 title="Cache and coherence block diagram",
 transcript="""Cache coherence block diagram:

   [CPU] [CPU] [CPU] [CPU]
     |     |     |     |
   [C1]  [C2]  [C3]  [C4]     ← private caches
     \\     |     |     /
      ===== shared bus =====
              |
        [Shared memory]

  “(Miss clause)” — on a miss, the cache fetches the block and may need to
  invalidate or update other copies.""",
 explain=r'''
    A(p("<b>What the page says.</b> The coherence picture: several processors with private caches over a "
        "shared bus, and the note that a miss (or a write) forces the caches to coordinate."))
    A(formula("Coherence invariant (informal):\n"
              "  For every memory block, either it is present in no cache, or every\n"
              "  cached copy has the same value; a write must make all other copies\n"
              "  consistent (invalidated or updated)."))
    A(p("The next pages develop the protocol (write-through / write-back, write-invalidate) and the "
        "states (MSI / MESI). This page is the map of the system those protocols run on."))
''',
 pyqs=[])

PAGES[70] = dict(
 title="Cache basics — direct mapping (block number mod number of lines)",
 transcript="""Cache:

  Holds recently used blocks of memory close to the CPU.

  Direct Mapped:
    A block can go in exactly ONE line:  line = (block number) mod (number of lines)

    Address = | Tag | Index | Offset |
                ^      ^        ^
              identifies   selects   byte within
              the block    the line   the block

  Example:  memory block 12 → line 12 mod 4 = 0 (if there are 4 lines).

  The tag is stored with each line and compared on every access.""",
 explain=r'''
    A(p("<b>What the page says.</b> The simplest cache organisation: <b>direct mapping</b>, where each "
        "memory block has exactly one place it can live."))
    A(formula("line = (block number) mod (number of cache lines)\n"
              "  e.g. block 12, 4 lines:  12 mod 4 = 0  → line 0\n"
              "        block 13, 4 lines:  13 mod 4 = 1  → line 1"))
    A(h3("Address breakdown"))
    A(bullets([
        "<b>Offset</b> — the low bits; select the byte within the block.",
        "<b>Index</b> — the middle bits; select the cache line (set).",
        "<b>Tag</b> — the high bits; stored with the line and compared to confirm the hit.",
    ]))
    A(formula("Address (32 bits) = [ Tag | Index | Offset ]\n"
              "  offset bits = log₂(block size)\n"
              "  index  bits = log₂(number of lines)\n"
              "  tag    bits = 32 − index − offset"))
    A(callout("<b>Why direct mapping is simple but limited.</b> Each block has only one possible home, "
        "so the lookup is trivial (one tag comparison). But two blocks that map to the same line will "
        "keep evicting each other — this is called a <b>conflict miss</b>.", 'tip'))
''',
 pyqs=[])
