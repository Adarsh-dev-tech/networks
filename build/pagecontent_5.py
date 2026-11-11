"""Page-by-page annotations for handwritten pages 71-87."""

PAGES = {}

PAGES[71] = dict(
 title="Set-associative cache — organisation and address bits",
 transcript="""Set-Associative Cache:

  Each set holds n ways (n = associativity).

  A block maps to a SET:  set = (block number) mod (number of sets),
  and within the set it can go in ANY of the n ways.

  Address:  | Tag | Set index | Offset |

  Example: 2-way set associative, 16 sets:
     block → set (mod 16), then any of the 2 ways.

  Replaces fully-associative (all lines) with set-associative (a set of lines).""",
 explain=r'''
    A(p("<b>What the page says.</b> The middle ground between direct-mapped and fully-associative: a "
        "block maps to one <b>set</b>, but within that set it can occupy any of <b>n</b> ways."))
    A(formula("set = (block number) mod (number of sets)\n"
              "  n-way set associative: n lines per set\n"
              "  direct mapped  = 1-way set associative\n"
              "  fully associative = 1 set with all the lines\n\n"
              "Address = [ Tag | Set index | Offset ]\n"
              "  set-index bits = log₂(number of sets)"))
    A(bullets([
        "Fewer conflict misses than direct-mapped (a block has n homes, not one).",
        "Cheaper and faster than fully-associative (only n tags are compared, not all lines).",
        "Requires a <b>replacement policy</b> to choose which way to evict when the set is full.",
    ]))
    A(p("<b>Reconstructed diagram.</b> Draw a table with <i>sets</i> as rows and <i>ways</i> as columns; "
        "each cell is a line holding a tag, valid bit and data. The set index selects the row; the tag "
        "is compared against all cells in that row."))
''',
 pyqs=[])

PAGES[72] = dict(
 title="Set-associative cache — worked address example",
 transcript="""Set-Associative worked example:

  Cache with several sets and ways.
  Block size, number of sets, associativity given.

  Address split:  Tag | Set | Offset

  (Worked example computing the number of bits in each field and which set a
  given address maps to.)

  Advantages:
   - Reduces conflict misses (a block has several possible homes),
   - Replacement policy can choose.
  Disadvantage:
   - More hardware (n tags compared) and a replacement decision.""",
 explain=r'''
    A(p("<b>What the page says.</b> A worked example that splits a physical address into tag, set and "
        "offset fields for a set-associative cache."))
    A(formula("Example: 32-bit address, 64 KB cache, 64-byte blocks, 4-way set associative.\n"
              "  offset = log₂64 = 6 bits\n"
              "  lines  = 64 KB / 64 B = 1024 lines\n"
              "  sets   = 1024 / 4 (ways) = 256 sets  →  set index = log₂256 = 8 bits\n"
              "  tag    = 32 − 8 − 6 = 18 bits\n"
              "  Address = [ 18-bit tag | 8-bit set | 6-bit offset ]"))
    A(callout("<b>Order of computation.</b> Always work out offset first (from block size), then the "
        "number of sets (from cache size, block size and associativity), then the tag (whatever is "
        "left).", 'tip'))
''',
 pyqs=[])

PAGES[73] = dict(
 title="Replacement policies — FIFO, LRU, optimal, random",
 transcript="""Replacement policies (when a set is full, which line to evict?):

  * Random      — pick any line at random.
  * FIFO        — first in, first out (evict the oldest).
  * LRU         — least recently used (evict the one not touched for longest).
  * Optimal     — evict the line that will be used farthest in the future
                  (theoretical best; needs future knowledge).

  Which is best?  Optimal (cannot be implemented); LRU is a good practical
  approximation; FIFO and Random are cheaper but worse.""",
 explain=r'''
    A(p("<b>What the page says.</b> The four classic replacement policies, with a note that the optimal "
        "one is a theoretical benchmark."))
    A(table(["Policy","Rule","Comment"],
      [["Random","Evict a random line","Cheap; can evict a useful line"],
       ["FIFO","Evict the oldest line","Cheap; ignores recent use"],
       ["LRU","Evict the least recently used line","Good approximation to optimal; needs counters"],
       ["Optimal","Evict the line used farthest in the future","Best possible; cannot be implemented (needs the future)"]],
      widths=[1.0,2.7,2.8]))
    A(formula("LRU bookkeeping: a “time-stamp” or age bits per line;\n"
              "on every access update the used line; on a miss evict the oldest.\n"
              "Optimal is used only as a benchmark to judge other policies."))
    A(callout("<b>Which to use?</b> LRU (or an approximation such as pseudo-LRU) is the usual practical "
        "choice, because locality means the recently used lines are likely to be used again. Optimal "
        "exists only to measure how much better a policy could possibly be.", 'tip'))
''',
 pyqs=[])

PAGES[74] = dict(
 title="Direct-mapped cache worked example — address field split",
 transcript="""Worked example — direct-mapped cache:

  Q: A direct-mapped cache of 3 KB? / given size and block size.
     Address width = 32 bits.
     Find the number of bits for tag, index and offset.

  Offset bits = log₂(block size)
  Index bits  = log₂(number of lines)
  Tag bits    = 32 − index − offset

  (Detailed arithmetic:  block size, number of lines, etc.)""",
 explain=r'''
    A(p("<b>What the page says.</b> A direct-mapped cache address-split question, worked in full."))
    A(formula("Given: 32-bit address, cache = 4 KB, block size = 32 bytes, direct mapped.\n"
              "  offset = log₂32 = 5 bits\n"
              "  lines  = 4 KB / 32 B = 128 lines  →  index = log₂128 = 7 bits\n"
              "  tag    = 32 − 7 − 5 = 20 bits\n"
              "  Address = [ 20-bit tag | 7-bit index | 5-bit offset ]"))
    A(bullets([
        "Two blocks that share the same index (i.e. differ only in the tag) map to the <b>same line</b> "
        "and will evict each other — a conflict miss.",
        "The line number is <i>block number mod number of lines</i>; the index bits are exactly the "
        "low-order bits of the block number.",
    ]))
''',
 pyqs=[38])

PAGES[75] = dict(
 title="Cache address split — worked example (tag/index/offset)",
 transcript="""Worked example:

  Cache size = 256 KB, block size = 1 KB? / 512 B?
  Number of sets, associativity given.

  Physical address → split into Tag | Set | Offset.

  (Compute offset, then index/set, then tag; show the bit fields.)

  Replace/decide which lines are used.""",
 explain=r'''
    A(p("<b>What the page says.</b> Another worked address-split example, this time for a larger "
        "cache."))
    A(formula("Given: 256 KB cache, 512-byte blocks, direct mapped, 32-bit address.\n"
              "  offset = log₂512 = 9 bits\n"
              "  lines  = 256 KB / 512 B = 512 lines  →  index = log₂512 = 9 bits\n"
              "  tag    = 32 − 9 − 9 = 14 bits\n"
              "  Address = [ 14-bit tag | 9-bit index | 9-bit offset ]\n\n"
              "If instead it is 4-way set associative:\n"
              "  sets = 512 / 4 = 128  →  index = log₂128 = 7 bits ;  tag = 32 − 7 − 9 = 16 bits"))
    A(callout("<b>Check your answer.</b> tag + index + offset must equal the address width. Compute "
        "offset and index first, then subtract.", 'tip'))
''',
 pyqs=[37])

PAGES[76] = dict(
 title="Write-through policy; the local miss-rate / average-access-time formula",
 transcript="""Write policy 1: Write-through.

  Every write updates BOTH the cache and the main memory.

  Consequence: main memory is always up to date; but write traffic to memory
  is high (slow).

  Average access time:
    AMAT = Hit time + Miss rate × Miss penalty
    T_avg = (1 − H) · t_miss + H · t_hit

  where H = hit rate.

  Different organisation → different write policies:
   1) write-through,
   2) write-back,
   3) write-allocate / no-write-allocate.""",
 explain=r'''
    A(p("<b>What the page says.</b> The write-through policy and the average-memory-access-time "
        "formula."))
    A(h3("Write-through"))
    A(bullets([
        "Every store writes the cache <i>and</i> the next level of memory.",
        "<b>Advantage:</b> main memory is always consistent with the cache, so coherence and recovery "
        "are simpler.",
        "<b>Disadvantage:</b> every write causes memory traffic, which is slow; a <b>write buffer</b> is "
        "used to hide the latency.",
    ]))
    A(h3("Average memory access time"))
    A(formula("AMAT = Hit time + Miss rate × Miss penalty\n"
              "or, in hit-rate form:  T_avg = H · t_hit + (1 − H) · t_miss\n"
              "  H = hit rate,  t_hit = hit time,  t_miss = miss penalty.\n"
              "Multi-level:  AMAT = t_L1 + m_L1 · (t_L2 + m_L2 · t_mem)"))
    A(p("<b>Reading the formula.</b> The miss rate is multiplied by the miss penalty because only the "
        "misses pay that penalty. Reducing the miss rate and reducing the miss penalty are two separate "
        "optimisation targets (developed on pages 79–80)."))
''',
 pyqs=[27])

PAGES[77] = dict(
 title="Write-back and write-allocate policies",
 transcript="""Write policy 2: Write-back.

  On a write, update only the cache and mark the line “dirty”.
  The line is written to memory only when it is EVICTED.

  → Less memory traffic than write-through (good), but memory can be stale
    and coherence is harder.

Write policy 3: Write-allocate.

  On a write miss, first fetch the block into the cache, then write it.

  (No-write-allocate: on a write miss, write straight to memory.)

  Write-back + write-allocate is the common combination.""",
 explain=r'''
    A(p("<b>What the page says.</b> The write-back and write-allocate policies and how they combine."))
    A(table(["Policy","On a write hit","On a write miss"],
      [["Write-through","Write cache and memory","Usually no-write-allocate (write to memory)"],
       ["Write-back","Write cache only; mark dirty","Depends on allocate policy"],
       ["Write-allocate","—","Fetch the block into the cache, then write"],
       ["No-write-allocate","—","Write straight to memory, do not allocate"]],
      widths=[1.3,2.4,2.6]))
    A(formula("Write-back traffic: a dirty line is written to memory ONCE, on eviction.\n"
              "  → fewer memory writes than write-through when a line is written many times.\n\n"
              "Write-through traffic: every store goes to memory immediately.\n"
              "  → simpler coherence, more bandwidth used."))
    A(callout("<b>Common combination.</b> Write-back + write-allocate is standard in real caches: it "
        "keeps repeated writes on-chip and only pays the memory cost once, on eviction.", 'tip'))
''',
 pyqs=[])

PAGES[78] = dict(
 title="Write-allocate / write-back combinations (summary)",
 transcript="""Combinations:

  Write-through + no-write-allocate  (write straight through, no fetch)
  Write-through + write-allocate
  Write-back   + write-allocate      (the usual choice)
  Write-back   + no-write-allocate

  Diagram: on each write, decide (a) update cache? (b) fetch block?
  “Write-through → memory always updated.”
  “Write-back → memory updated on eviction (dirty line).”""",
 explain=r'''
    A(p("<b>What the page says.</b> The four possible combinations of the write-hit policy and the "
        "write-miss (allocate) policy, with a decision diagram."))
    A(table(["Write-hit policy","Write-miss policy","When memory is updated","Typical use"],
      [["Write-through","No-write-allocate","On every write","Simple systems"],
       ["Write-through","Write-allocate","On every write; block fetched on miss","Rare"],
       ["Write-back","Write-allocate","On eviction of a dirty line","Most caches"],
       ["Write-back","No-write-allocate","On eviction of a dirty line","Rare"]],
      widths=[1.4,1.5,2.3,1.3]))
    A(formula("Decision diagram:\n"
              "  Write hit?  yes → update cache (write-through also updates memory)\n"
              "  Write miss? → write-allocate: fetch block, then update cache\n"
              "                no-write-allocate: write straight to memory"))
    A(p("<b>Why write-back + write-allocate dominates.</b> Repeated writes to the same block stay in the "
        "cache and are written to memory only once; the fetch on a write miss means the whole block is "
        "available for subsequent writes."))
''',
 pyqs=[])

PAGES[79] = dict(
 title="Write-policy summary; AMAT; cache-optimisation checklist",
 transcript="""Write policies summary:
  - Write-through : memory updated on every write.
  - Write-back    : memory updated on eviction (dirty).
  - Write-allocate / no-write-allocate : whether a write miss fetches the block.

Cache optimisation:
  AMAT = Hit time + Miss rate × Miss penalty

  To improve performance, reduce ONE of the three terms:
   1) Reduce the hit time (smaller/faster cache, simpler addressing),
   2) Reduce the miss rate (bigger cache, higher associativity, better
      replacement, blocking),
   3) Reduce the miss penalty (multilevel caches, critical-word-first,
      non-blocking caches, prefetching).""",
 explain=r'''
    A(p("<b>What the page says.</b> The summary of write policies and the master cache-optimisation "
        "equation with its three levers."))
    A(formula("AMAT = Hit time + Miss rate × Miss penalty\n"
              "   → three independent ways to reduce AMAT:\n"
              "     1) reduce hit time        2) reduce miss rate        3) reduce miss penalty"))
    A(h3("The three levers"))
    A(bullets([
        "<b>Reduce hit time</b> — use a smaller/faster cache, a simpler (direct-mapped) organisation, "
        "and avoid adding address-translation delay to the critical path.",
        "<b>Reduce miss rate</b> — use a bigger cache, higher associativity, better replacement "
        "(LRU), and reduce the three C’s (compulsory, capacity, conflict).",
        "<b>Reduce miss penalty</b> — use multilevel caches, <b>critical-word-first</b> (return the "
        "needed word first), <b>non-blocking</b> caches (several misses in flight), and prefetching.",
    ]))
    A(callout("<b>Key point.</b> These three goals often conflict — a bigger cache lowers the miss rate "
        "but raises the hit time. Cache design is the art of balancing the three terms of AMAT.", 'tip'))
''',
 pyqs=[35])

PAGES[80] = dict(
 title="Multilevel caches; inclusive/exclusive; local vs global miss rate",
 transcript="""Multilevel caches:

  L1 (small, fast, private) → L2 (bigger) → L3 → main memory.

  Inclusive: a block in L1 is also in L2 (L2 ⊇ L1).
  Exclusive: a block is in only one level (L1 ∩ L2 = ∅).

  Local miss rate  = misses in THIS cache / accesses to THIS cache.
  Global miss rate = misses in THIS cache / total accesses to the CPU.

  Multilevel caches reduce the miss penalty (the L2 serves the L1’s misses).""",
 explain=r'''
    A(p("<b>What the page says.</b> How several cache levels cooperate, the inclusive/exclusive "
        "distinction, and the two ways of measuring a miss rate."))
    A(bullets([
        "<b>Multilevel caches</b> — a small fast L1 backed by a larger slower L2, then L3, then memory. "
        "The L2 serves the L1’s misses, so the effective miss penalty seen by the CPU is much smaller.",
        "<b>Inclusive</b> — every block in L1 is also in L2 (L2 ⊇ L1). This makes coherence and "
        "invalidation simpler (checking L2 tells you about L1).",
        "<b>Exclusive</b> — a block lives in only one level at a time (L1 ∩ L2 = ∅), which uses the total "
        "capacity better.",
    ]))
    A(formula("Local miss rate  = misses in this cache / accesses to this cache\n"
              "Global miss rate = misses in this cache / total accesses to the CPU\n\n"
              "AMAT (two levels) = t_L1 + m_L1 · ( t_L2 + m_L2 · t_mem )\n"
              "  m_L1 = L1 miss rate, m_L2 = L2 LOCAL miss rate."))
    A(callout("<b>Which miss rate to use?</b> When combining levels, use the <i>local</i> miss rate of "
        "the second level inside the formula above. The <i>global</i> miss rate of L2 is m_L1 × m_L2 — "
        "the fraction of all CPU accesses that miss in both.", 'tip'))
''',
 pyqs=[15])

PAGES[81] = dict(
 title="Prefetching — hardware and software",
 transcript="""Prefetching:

  1) Hardware prefetching: the cache hardware notices a pattern (e.g. sequential
     access) and fetches blocks ahead of time, into the cache.

  2) Software prefetching: the compiler inserts explicit prefetch instructions
     that bring data in before it is needed.

  3) Hybrid prefetching: a combination of the two.

  Prefetching reduces the effective miss penalty (and sometimes the miss rate)
  by hiding memory latency behind useful work.

  Cost: extra memory traffic; a wrong prefetch wastes bandwidth.""",
 explain=r'''
    A(p("<b>What the page says.</b> Prefetching hides memory latency by bringing data into the cache "
        "before it is asked for. The page lists the hardware, software and hybrid forms."))
    A(bullets([
        "<b>Hardware prefetching</b> — the cache observes a stream (e.g. sequential addresses) and "
        "fetches the next blocks automatically. No program changes needed.",
        "<b>Software prefetching</b> — the compiler inserts prefetch instructions early in the code so "
        "the data is in the cache by the time it is used.",
        "<b>Hybrid</b> — hardware and software prefetching together.",
    ]))
    A(formula("Benefit: the memory latency is overlapped with useful work,\n"
              "  so the effective miss penalty falls (the data is already in the cache).\n"
              "Cost:   extra memory bandwidth; a mis-predicted prefetch fetches data\n"
              "  that is never used (cache pollution)."))
    A(callout("<b>Prefetch vs critical-word-first.</b> Both attack the miss penalty. Prefetching brings "
        "data in <i>earlier</i>; critical-word-first returns the <i>needed word first</i> so the CPU can "
        "restart sooner. A good design uses both.", 'tip'))
''',
 pyqs=[])

PAGES[82] = dict(
 title="Virtual memory — address translation, the TLB and page faults",
 transcript="""Virtual Memory:

  Virtual address → (page table) → Physical address

  Address split:  [ Virtual page number | Page offset ]
                  [ Physical page number | Page offset ]

  All pages of a process map into one linear virtual address space.

  TLB (Translation Lookaside Buffer): a small cache of recent translations.

  Page fault: the page is not in memory → bring it in from disk.

  Critical-word-first; write-back caches (for the page table entries).""",
 explain=r'''
    A(p("<b>What the page says.</b> Virtual memory: every program uses virtual addresses that are "
        "translated to physical addresses through a page table, with a TLB to speed up the translation."))
    A(formula("Virtual address = [ Virtual Page Number (VPN) | Page Offset ]\n"
              "Physical address = [ Physical Page Number (PPN) | Page Offset ]\n"
              "  page offset bits = log₂(page size)   (e.g. 4 KB page → 12 bits)\n"
              "  PPN = page_table[VPN]"))
    A(bullets([
        "<b>Why virtual memory?</b> Each process gets its own address space; programs can be larger than "
        "physical memory; and memory is protected between processes.",
        "<b>Page table</b> — maps each virtual page to a physical page (or marks it “not present”).",
        "<b>TLB</b> — a small, fast cache of recent translations, so most accesses avoid the page-table "
        "walk.",
        "<b>Page fault</b> — the page is not in physical memory; the OS brings it in from disk and "
        "restarts the instruction.",
    ]))
    A(p("<b>Reconstructed diagram.</b> Draw the CPU issuing a virtual address; split it into VPN and "
        "offset; the VPN indexes the page table (or, on a hit, the TLB) to give the PPN; concatenate the "
        "PPN with the offset to form the physical address."))
''',
 pyqs=[])

PAGES[83] = dict(
 title="Summary of instruction-level optimisations (the compiler/hardware toolbox)",
 transcript="""Instruction-level optimisations (summary):

  * Compiler optimisations
  * Multicast (FP)
  * Speculative loading
  * Branch prediction
  * Loop unrolling
  * Scheduling
  * Tomasulo’s algorithm
  * Dynamic scheduling
  * Superscalar (VLIW)
  * Cache memory

  Hardware prefetching; deals with long-latency instructions — when an
  instruction loop executes, instructions are fetched from the stream of code.""",
 explain=r'''
    A(p("<b>What the page says.</b> A summary checklist of every technique the notes have covered for "
        "extracting instruction-level parallelism and hiding latency."))
    A(table(["Technique","What it does"],
      [["Compiler optimisation","Reorders/rewrites code to expose ILP"],
       ["Multicast (FP)","Broadcast one result to several consumers at once"],
       ["Speculative loading","Load early, before it is certain the load is needed"],
       ["Branch prediction","Guess the branch direction to avoid control stalls"],
       ["Loop unrolling","Repeat the body to amortise overhead and expose ILP"],
       ["Scheduling","Reorder instructions to fill delay slots"],
       ["Tomasulo’s algorithm","Dynamic scheduling with renaming and the CDB"],
       ["Dynamic scheduling","Hardware reorders at run time"],
       ["Superscalar / VLIW","Issue several instructions per cycle"],
       ["Cache memory","Keep data close to reduce memory latency"]],
      widths=[1.7,4.8]))
    A(callout("<b>Two families.</b> <i>Static</i> techniques (compiler: unrolling, scheduling, software "
        "prefetch) fix the schedule at build time. <i>Dynamic</i> techniques (branch prediction, "
        "Tomasulo, speculation, superscalar) adapt at run time. Real CPUs use both together.", 'tip'))
''',
 pyqs=[])

PAGES[84] = dict(
 title="Cache coherence — the problem, MSI/MESI and snooping vs directory",
 transcript="""Cache Coherence:

  Problem: several private caches may hold copies of one block; a write to one
  must not leave the others stale.

  Two families of protocol:
   1) Snooping (broadcast on a shared bus),
   2) Directory-based (a directory records who holds each block).

  States: MSI (Modified, Shared, Invalid) and MESI (+ Exclusive).

  Write policy: write-through or write-back.

  Example protocol diagram (shared bus, invalidate on write).""",
 explain=r'''
    A(p("<b>What the page says.</b> The cache-coherence problem and the two families of solution, with "
        "the MSI/MESI states."))
    A(h3("The coherence problem"))
    A(p("When several caches keep private copies of a block, a write by one core makes the others stale. "
        "A coherence protocol guarantees that every read returns the latest write."))
    A(table(["State","Meaning"],
      [["M — Modified","This cache has the only copy, and it is dirty (differs from memory)"],
       ["S — Shared","The block is clean and may be in several caches"],
       ["I — Invalid","This cache does not have a valid copy"],
       ["E — Exclusive (MESI)","Clean, held by this cache only (a silent upgrade to M is possible)"]],
      widths=[1.4,5.1]))
    A(h3("Two families of protocol"))
    A(bullets([
        "<b>Snooping</b> — every cache watches (snoops) the shared bus; a write is broadcast and the "
        "other caches invalidate or update their copies. Simple; needs a bus (does not scale).",
        "<b>Directory-based</b> — a directory records which caches hold each block, so coherence "
        "messages go only to the sharers. Scales to many nodes.",
    ]))
    A(formula("MSI transitions (example):\n"
              "  read miss (no sharer)   : I → S\n"
              "  write miss              : I → M  (and invalidate other copies)\n"
              "  write hit in S          : S → M  (invalidate others)\n"
              "  snoop read while M      : M → S  (write back / supply data)\n"
              "  snoop write while S/M   : S/M → I"))
''',
 pyqs=[2, 23, 29])

PAGES[85] = dict(
 title="MSI example — write-invalidate on a shared bus (snapshot)",
 transcript="""MSI example (write-invalidate protocol):

  Snapshot:  caches C1..C4 with tags and coherency states.

  Q: When P0 writes block x, what happens to its state and to the others?
     → the writer’s copy becomes M; all other copies become I.

  Q: When P1 reads x, what happens?
     → the copy becomes S (shared).

  (Table of tags/states before and after each event.)

  Directory-based protocol introduced: a home directory tracks sharers.""",
 explain=r'''
    A(p("<b>What the page says.</b> A worked MSI snapshot: given the states of several caches, apply a "
        "sequence of events and update the states using the write-invalidate protocol."))
    A(formula("Write-invalidate rules (MSI):\n"
              "  • P writes a block it does not have (I) → fetch it, state M, invalidate all others.\n"
              "  • P writes a block it has shared (S)  → state M, invalidate all others.\n"
              "  • P reads a block it does not have (I) → state S (or M if no sharers, in MESI).\n"
              "  • A cache snooping a write to its S/M copy → its state becomes I."))
    A(p("<b>How to answer.</b> Build a table with a column per cache (and memory). For each event, "
        "update the writer’s state and invalidate/update every other copy that held the block. Read the "
        "table row by row."))
    A(p("The full printed question and its complete trace are in the past-paper solutions (ca2, ca6, "
        "ca23, ca29)."))
''',
 pyqs=[6])

PAGES[86] = dict(
 title="MSI example (continued) and directory-based protocol",
 transcript="""(Continuation of the MSI trace.)

  Directory-based protocol:
    Each block has a home node with a directory entry listing which caches
    hold it (the sharer set) and whether it is modified.

  Messages:
    - Read miss  → request to home; home replies with data and sharer list.
    - Write miss → request to home; home invalidates all sharers, then grants.
    - “Acknowledge” / “Write-back” messages update the directory.

  (Table of events with the resulting states.)""",
 explain=r'''
    A(p("<b>What the page says.</b> The trace continues, and the page introduces the directory-based "
        "protocol with its messages."))
    A(formula("Directory entry per block:  { state, sharer set }\n"
              "  • Read miss  : home sends data to requester, adds it to the sharer set.\n"
              "  • Write miss : home sends invalidations to all sharers, then grants\n"
              "                 exclusive ownership to the writer.\n"
              "  • Write-back : when an M block is replaced, its data returns to home."))
    A(bullets([
        "<b>Advantage of directories</b> — coherence traffic goes only to the sharers, so the design "
        "scales to large machines with no broadcast medium.",
        "<b>Cost</b> — the directory must be stored and updated (memory overhead, extra messages).",
    ]))
''',
 pyqs=[7])

PAGES[87] = dict(
 title="MSI example (continued) — write policy for a shared block",
 transcript="""MSI example (continued):

  Event trace with tags and states (C1..C4).

  Q: P0 writes x (which is shared) — what is the write policy?
     → write-invalidate: the other copies become I, the writer’s copy becomes M.

  Q: P1 reads x again — the copy becomes S.

  Write-back: the M copy is written back to memory when evicted.

  (Final state table.)

  “Write-back ⇒ memory updated on eviction; write-through ⇒ updated
   immediately.”""",
 explain=r'''
    A(p("<b>What the page says.</b> The final part of the MSI trace, focusing on the write policy for a "
        "block that several caches share."))
    A(formula("Write-invalidate on a shared block:\n"
              "  before:  C1 = S(x), C2 = S(x), C3 = S(x), memory = x\n"
              "  P1 writes x:  C2 → M(x);  C1 → I(x);  C3 → I(x);  memory stale\n"
              "  on eviction of the M copy:  write back x to memory (write-back policy)\n\n"
              "Write-through alternative: every write also updates memory immediately\n"
              "  (simpler coherence, more traffic)."))
    A(callout("<b>Summary of the coherence block.</b> Problem → two families (snooping / directory) → "
        "states (MSI / MESI) → write policy (write-through / write-back) → worked traces. The exam "
        "question is almost always “apply the protocol to this snapshot”, so practise the table method.", 'tip'))
''',
 pyqs=[])
