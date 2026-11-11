"""Part V — Memory hierarchy, cache, virtual memory, cache coherence."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

def build():
    F=[]
    def A(x): F.extend(x if isinstance(x,list) else [x])

    # ============ 10. MEMORY HIERARCHY & CACHE ============
    A(PageBreak())
    A(h1(10,"The Memory Hierarchy & Cache Memory","Making memory look fast and cheap at the same time"))
    A(p("A perfect memory would be as fast as registers and as cheap and large as disk. No single technology "
        "does both, so we build a <b>hierarchy</b>: small, fast, expensive memories near the CPU and large, "
        "slow, cheap memories farther away. The trick that makes the hierarchy <i>work</i> is "
        "<b>locality of reference</b>."))

    A(h3("10.1 Locality — the reason caches work"))
    A(table(["Type","Meaning","Example"],
      [["Temporal locality","A location used once is likely to be used again soon.","A loop variable; a repeatedly-called function"],
       ["Spatial locality","Locations near a used one are likely to be used soon.","Array elements; consecutive instructions"]],
      widths=[1.4,2.6,2.0]))
    A(fig("page068.jpg", w=11.5*gen.cm, cap="Memory hierarchy: registers, cache levels, main memory and secondary storage (source: lecture notes, p. 68)."))
    A(p("<b>Reading the figure.</b> The memory-hierarchy pyramid: registers, L1/L2/L3 caches, main memory and disk. Each level down is bigger, slower and cheaper, and holds the level above it."))
    A(table(["Level","Typical size","Access time","Managed by"],
      [["Registers","< 1 KB","< 1 ns","Compiler"],
       ["L1 cache","32-64 KB","1-2 ns","Hardware"],
       ["L2 cache","256 KB - 1 MB","~10 ns","Hardware"],
       ["L3 cache","4-32 MB","~30 ns","Hardware"],
       ["Main memory (DRAM)","GB","~60-100 ns","OS + hardware"],
       ["Secondary (SSD/HDD)","TB","µs - ms","OS"]],
      widths=[1.4,1.2,1.2,1.4]))

    A(h3("10.2 Cache basics and the three organizations"))
    A(fig("page069.jpg", w=10.5*gen.cm, cap="Cache organisation: hit/miss and block placement (source: p. 69)."))
    A(p("<b>Reading the figure.</b> How a cache serves a hit and a miss. On a hit the data comes straight back; on a miss the whole block is fetched from the next level and placed according to the cache mapping."))
    A(p("A <b>cache</b> is a small fast memory that holds recently-used blocks (lines) of main memory. When "
        "the CPU asks for a word, the cache checks whether the containing block is present. If yes: a "
        "<b>hit</b>; if no: a <b>miss</b>, and the block is fetched from the next level. Where a block can be "
        "placed gives the three organizations:"))
    A(h4("Cache terminology you must be able to define"))
    A(table(["Term","Meaning"],
      [["Block (line)","The unit of transfer between cache and memory (e.g. 64 bytes)."],
       ["Hit / Miss","The requested block is / is not present in the cache."],
       ["Hit time","Time to access the cache (and confirm a hit)."],
       ["Miss rate","Fraction of accesses that miss = 1 − hit rate."],
       ["Miss penalty","Extra time to fetch the block from the next level."],
       ["Valid bit","One bit per line; 0 means the line holds no useful data (e.g. after power-up)."],
       ["Dirty bit","Set when a line is written in a write-back cache; the line must be written back on eviction."],
       ["Tag","The high-order address bits stored with a line so the cache can tell whether the block matches."]],
      widths=[1.3,4.7]))

    A(table(["Organization","Block placement","Search cost","Conflict misses","Hardware"],
      [["Direct mapped","Block i → line (i mod #lines). Exactly one place.","One comparison","High (many blocks map to one line)","Cheapest, fastest"],
       ["Fully associative","Block may go in any line.","Compare against all lines","None","Most expensive, slowest search"],
       ["Set associative (n-way)","Block goes in set (i mod #sets); within the set, any of n ways.","Compare n ways","Low (between the two)","Middle — the usual choice"]],
      widths=[1.4,2.2,1.2,1.3,1.2]))
    A(fig("page070.jpg", w=11.5*gen.cm, cap="Direct-mapped, set-associative and fully-associative cache organizations (source: lecture notes, p. 70)."))
    A(p("<b>Reading the figure.</b> The three cache organizations. Direct-mapped puts a block in exactly one place; set-associative allows n places within a set; fully associative allows any place."))
    A(h4("Address breakdown"))
    A(p("A physical address is split into three fields. For a cache of block size B bytes and S sets:"))
    A(formula("Offset bits = log₂(B)         (selects the byte within the block)\n"
              "Index bits  = log₂(S)         (selects the set/line)\n"
              "Tag bits    = Address bits − Index bits − Offset bits\n"
              "S = (cache size) / (associativity × block size)"))
    A(p("<b>Worked example (PYQ ca25 · Q4).</b> 8-way set-associative, 32 KB capacity, block = 8 words, word "
        "= 32 bits = 4 bytes, physical address space = 8 GB (33 bits)."))
    A(formula("Block size = 8 words × 4 B = 32 B → offset = log₂32 = 5 bits\n"
              "#sets = 32 KB / (8 ways × 32 B) = 32768 / 256 = 128 → index = log₂128 = 7 bits\n"
              "Address bits = log₂(8 GB) = log₂(2³³) = 33 bits\n"
              "Tag = 33 − 7 − 5 = 21 bits"))
    A(callout("<b>Answer: 21 tag bits.</b> Always compute offset first, then index, then tag = total − index − offset.", 'tip'))

    A(h3("10.3 Average Memory Access Time (AMAT)"))
    A(fig("page072.jpg", w=10.5*gen.cm, cap="Address decomposition: tag, set index and block offset (source: p. 72)."))
    A(p("<b>Reading the figure.</b> The address split. The offset selects the byte inside the block, the index selects the set, and the tag is compared to confirm the hit — this is the diagram behind every tag/index/offset question."))
    A(formula("AMAT = Hit time + Miss rate × Miss penalty\n"
              "For two levels: AMAT = HitTime_L1 + MissRate_L1 × ( HitTime_L2 + MissRate_L2 × MissPenalty )\n"
              "For multi-level: AMAT = HitTime_L1 + MR_L1 × ( HitTime_L2 + MR_L2 × ( HitTime_L3 + … ))"))
    A(p("<b>Why it matters:</b> AMAT tells you the average cost of one memory access. Reducing either the "
        "miss rate or the miss penalty improves it — the whole point of multi-level caches."))

    A(h3("10.4 The three C's of cache misses"))
    A(fig("page071.jpg", w=10.5*gen.cm, cap="Set-associative cache: ways, sets and address fields (source: p. 71)."))
    A(p("<b>Reading the figure.</b> A set-associative cache drawn as ways × sets, showing where the tag, index and offset bits point."))
    A(table(["Miss type","Cause","Fix"],
      [["Compulsory (cold)","First access to a block.","Prefetching; bigger blocks (fewer, larger cold misses)"],
       ["Capacity","Cache too small to hold the working set.","Bigger cache"],
       ["Conflict (collision)","Too many blocks map to the same set (direct-mapped or low associativity).","Higher associativity; victim cache"]],
      widths=[1.3,2.6,2.1]))

    A(h3("10.5 Cache optimization — the exam checklist"))
    A(fig("page075.jpg", w=10.5*gen.cm, cap="Worked address-decomposition example for a set-associative cache (source: p. 75)."))
    A(p("<b>Reading the figure.</b> A fully worked address-decomposition example: block size gives the offset bits, number of sets gives the index bits, and the remainder is the tag."))
    A(p("There are four families of optimization: reduce <i>miss rate</i>, reduce <i>miss penalty</i>, reduce "
        "<i>hit time</i>, and reduce <i>power</i>. The most examined are the miss-rate techniques."))
    A(h4("Reduce the miss rate"))
    A(bullets([
      "<b>Larger block size</b> — exploits spatial locality, but too large a block raises conflict misses and "
      "the miss penalty (more bytes to fetch).",
      "<b>Higher associativity</b> — reduces conflict misses (2:1 rule of thumb: going from direct-mapped to "
      "2-way roughly halves conflict misses; returns diminish beyond 8-way).",
      "<b>Larger cache</b> — reduces capacity misses (costly in area and access time).",
      "<b>Prefetching</b> — hardware or compiler fetches blocks before they are needed.",
      "<b>Compiler optimizations</b> — loop interchange, blocking (tiling), merging arrays to improve locality.",
      "<b>Victim cache</b> — a small fully-associative buffer holding recently-evicted blocks, to recover "
      "conflict misses.",
    ]))
    A(h4("Reduce the miss penalty"))
    A(bullets([
      "<b>Multi-level caches</b> — L2/L3 catch L1 misses; L2 can be big and slower.",
      "<b>Critical-word-first</b> — return the requested word first, then the rest of the block.",
      "<b>Early restart</b> — resume the processor as soon as the requested word arrives.",
      "<b>Merging write buffer</b> — combine writes to the same block before sending to memory.",
      "<b>Non-blocking (lockup-free) caches</b> — continue serving other accesses during a miss.",
    ]))
    A(h4("Reduce the hit time"))
    A(bullets([
      "Smaller, simpler (direct-mapped) caches access faster.",
      "<b>Way prediction</b> — predict which way will hit so only one way is read.",
      "<b>Pipelined cache access</b> — split cache access across cycles to raise clock frequency.",
      "Avoid address translation in the critical path (use virtual-indexed caches or a TLB).",
    ]))

    A(h3("10.6 Write policies"))
    A(fig("page077.jpg", w=10.5*gen.cm, cap="Write-through vs write-back and write-allocate policies (source: p. 77)."))
    A(p("<b>Reading the figure.</b> Write-through vs write-back, and write-allocate vs no-write-allocate. Compare the traffic each policy generates — write-back only writes a line when it is evicted."))
    A(table(["Policy","On a write hit","On a write miss","Trade-off"],
      [["Write-through","Write both cache and memory.","Usually write-allocate (fetch then write) or no-allocate.","Simple; memory always current; high memory traffic."],
       ["Write-back","Write only the cache; mark the line dirty.","Write-allocate.","Less memory traffic; needs a dirty bit; memory can be stale."],
       ["Write-allocate","—","Fetch the block into cache, then write.","Good locality; costs a fetch."],
       ["No-write-allocate","—","Write directly to memory.","Avoids fetching a block that may not be reused."]],
      widths=[1.2,1.8,1.8,1.6]))
    A(callout("<b>Write-back vs write-through efficiency (PYQ ca27):</b> a write-back cache writes a dirty "
              "line once when evicted; a write-through cache writes every store to memory. So write-back wins "
              "when a line is written many times before eviction — the “break-even” number of writes is the "
              "key number to compute.", 'tip'))

    A(h3("10.7 Replacement policies and multi-level caches"))
    A(table(["Policy","Rule","Notes"],
      [["LRU (least recently used)","Evict the line not used for the longest time.","Best hit rate, but expensive to track exactly; approximated (pseudo-LRU)."],
       ["FIFO","Evict the line brought in earliest.","Simple; can evict a heavily-used line (no recency)."],
       ["Random","Evict a line at random.","Cheapest; surprisingly close to LRU for high associativity."],
       ["Optimal (Belady)","Evict the line used furthest in the future.","Gives the best possible hit rate; not implementable (needs the future) — used as a benchmark."]],
      widths=[1.4,2.2,2.4]))
    A(p("In a <b>multi-level</b> cache there are two miss rates. The <b>local miss rate</b> is the misses of a "
        "level divided by the accesses to that level; the <b>global miss rate</b> is its misses divided by all "
        "CPU accesses. L2 usually has a <i>high</i> local miss rate but a <i>low</i> global miss rate."))
    A(formula("Local miss rate (L2)  = L2 misses / L2 accesses" + chr(10) +
              "Global miss rate (L2) = L2 misses / total CPU accesses = MR_L1 × MR_L2(local)"))
    A(callout("<b>The memory wall.</b> CPU speed has grown far faster than DRAM latency, so the gap (the "
              "“memory wall”) keeps widening. This is why caches, prefetching and memory-level parallelism "
              "matter so much: most of the time a modern CPU is waiting on memory, not computing.", 'tip'))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Cache memory"))
    A(Paragraph("Q (ca15 · Q1a / ca26 · Q3a). A microprocessor with one level of cache has an AMAT of 2.4 "
                "clock cycles; a hit takes 1 cycle; a miss costs 80 cycles from off-chip memory. Designers "
                "add an on-chip L2 that can be accessed in 6 cycles (L1 behaviour unchanged; off-chip "
                "accesses still 80 extra cycles). They want a 65% improvement in AMAT. How often must data be "
                "found in the L2?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Old AMAT = HitTime + MR×MissPenalty →  2.4 = 1 + MR×80  →  MR_L1 = 1.4/80 = 0.0175 (1.75%)\n"
              "Target AMAT (65% improvement) = 2.4 × (1 − 0.65) = 2.4 × 0.35 = 0.84 cycles"))
    A(p("With the L2, a miss in L1 goes to L2. If the L2 hit rate is h₂, an L1 miss costs "
        "6 + (1 − h₂)×80 (the 80 is the extra off-chip time, since the L2 access of 6 is already spent):"))
    A(formula("AMAT = 1 + MR_L1 × [ 6 + (1 − h₂)×80 ] = 0.84\n"
              "0.84 − 1 = 0.0175 × [ 6 + (1 − h₂)×80 ]\n"
              "−0.16 / 0.0175 = 6 + (1 − h₂)×80   →   −9.14 = 6 + 80(1 − h₂)\n"
              "(1 − h₂) = (−15.14)/80  →  negative → the target cannot be met by adding L2 alone"))
    A(callout("<b>Reading the numbers carefully:</b> a target AMAT of 0.84 cycles is <i>less than the 1-cycle "
              "L1 hit time</i>, which is impossible if every access pays the L1 hit time. In the actual paper "
              "the “improvement” is measured against the miss <i>portion</i>, and the required L2 hit rate "
              "comes out very high. The exam point is the method: write AMAT = HitTime + MR×MissPenalty, set "
              "the new AMAT, and solve for the L2 hit rate. State your interpretation of “65% improvement” "
              "explicitly.", 'warn'))

    A(Paragraph("Q (ca15 · Q1b). Single core: base CPI = 1 (excluding cache misses); 308,752 L1 misses per "
                "10,000,000 accesses; a hit is 1 cycle with no stall; a miss costs 10 cycles. Now a multicore "
                "chip with snooping + MSI coherence: 452,977 misses per 10,000,000 accesses, a hit is still 1 "
                "cycle, a miss now costs 14 cycles. What must the CPI of the multicore system be for it to be "
                "worthwhile to abandon the single core?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Single core:\n"
              "  miss rate = 308752 / 10000000 = 0.0308752\n"
              "  CPI_single = 1 + miss_rate × miss_penalty = 1 + 0.0308752×10 = 1.30875\n\n"
              "Multicore (if it must beat the single core):\n"
              "  miss rate = 452977 / 10000000 = 0.0452977\n"
              "  CPI_multi = 1 + 0.0452977 × 14 = 1 + 0.634 = 1.634  (this is what the multicore actually gives)\n"
              "For the multicore to be worthwhile it must have CPI_multi < CPI_single = 1.30875"))
    A(p("<b>Answer:</b> the multicore must achieve <b>CPI &lt; 1.309</b> (the single-core CPI) to be worth it. "
        "As computed, the observed multicore CPI is ≈ 1.634 — worse — so unless other factors (parallelism) "
        "compensate, abandoning the single core is not worthwhile. This is the classic “coherence has a cost” "
        "question."))

    A(Paragraph("Q (ca25 · Q3 / ca35 · Q1). Critical-word-first and early restart on L2 misses. A 1 MB L2 with "
                "64-byte blocks and a 16-byte-wide refill path. The L2 can be written with 16 bytes every 4 "
                "processor cycles; the first 16-byte block from the memory controller arrives in 120 cycles; "
                "each additional 16-byte block takes 16 cycles; data is bypassed directly to the L2 read port. "
                "How many cycles to service an L2 miss with and without critical-word-first and early restart?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Block = 64 B, path = 16 B wide → 4 chunks of 16 B.\n"
              "Without CWF: wait for the FIRST chunk (120) then the rest (3×16=48) = 168 cycles before the "
              "processor can use data (and the full fill takes 120+48 = 168).\n"
              "With CWF + early restart: the requested word's chunk arrives first at 120 cycles and is "
              "bypassed immediately; the remaining 3 chunks continue to stream in.\n"
              "  Time to first useful data = 120 cycles (vs 168 without CWF).\n"
              "  Full fill = 120 + 48 = 168 cycles either way."))
    A(p("<b>Answer:</b> without CWF the miss stalls ~168 cycles; with CWF the processor restarts at ~120 "
        "cycles, saving ~48 cycles per miss. The total fill is the same; CWF only shortens the time to the "
        "<i>critical</i> word. CWF/early-restart matter more for <b>L1</b> misses in latency terms (L1 is on "
        "the critical path), but are easier to apply at L2 because the L2 is off the immediate critical path."))

    A(Paragraph("Q (ca35 · Q4). Designing a write buffer between a write-through L1 and a write-back L2. The "
                "L2 write bus is 16 B wide and can write to an independent address every 4 processor cycles. "
                "(a) What should the size of each write-buffer entry be? (b) What speed-up from a merging "
                "write buffer when zeroing memory with 64-bit stores?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("(a) Entry size = one bus write = 16 bytes (so a full entry can be drained in one bus cycle).\n"
              "(b) Zeroing with 64-bit (=8 B) stores: two 8-B stores fill one 16-B entry. A non-merging buffer "
              "writes each 8 B separately → 2 bus writes; a merging buffer combines them → 1 bus write.\n"
              "  Speed-up ≈ 2× (up to the bus-width/entry-width ratio = 16/8 = 2)."))
    A(p("<b>Answer:</b> entry = 16 B; merging gives up to <b>2×</b> speed-up here (the ratio of bus width to "
        "store width)."))

    A(Paragraph("Q (ca37 · Q2a). Micro-benchmarking a cache hierarchy: two-level cache, L1 is a 4 KB "
                "set-associative cache; the latency chart for the first 64 reads with stride 1 is given. What "
                "are the L1 and L2 block sizes? Explain.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "The chart shows latency spikes (misses) at regular intervals. With stride = 1, consecutive accesses "
      "touch consecutive words, so a miss every <i>k</i> words means the block holds <i>k</i> words.",
      "The first spike is the compulsory miss; the gap to the next spike = number of elements per block.",
      "Read the chart: if misses occur at iterations 0, 16, 32, … then the L1 block is 16 words = 64 bytes "
      "(with 4-byte words). A second, larger period in the spikes reveals the L2 block size similarly.",
      "Explain: a miss loads the whole block, so the following (blocksize−1) accesses are hits at the short "
      "latency; the next miss happens when the block boundary is crossed.",
    ]))
    A(p("<b>Method to state:</b> block size (in elements) = distance between consecutive miss spikes; "
        "convert to bytes by multiplying by the word size."))

    A(Paragraph("Q (ca37 · Q2b / ca38). A 16 KB direct-mapped 256 B block unified cache attached to a 16 MB "
                "main memory; word/instruction length 16 bits. Routine M (12 instruction words from 0x4230FA) "
                "calls subroutine S (4 instruction words from 0x70F168); two data words at 0x748074 and "
                "0x846064; the last 5 instructions of M form a loop iterated 10 times; the 2nd instruction in "
                "the loop calls S. Cache initially empty. Find (i) the address components, (ii) the number of "
                "misses, (iii) the number of block evictions, (iv) the non-empty block numbers after execution.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("(i) Address components:\n"
              "   Block size 256 B → offset = log₂256 = 8 bits\n"
              "   Cache 16 KB, direct-mapped → #lines = 16384/256 = 64 → index = log₂64 = 6 bits\n"
              "   Main memory 16 MB = 2²⁴ → address = 24 bits → tag = 24 − 6 − 8 = 10 bits\n"
              "   [tag:10 | index:6 | offset:8]"))
    A(bullets([
      "<b>(ii) Misses:</b> the first execution of M's 12 words misses the block(s) they occupy; S's 4 words "
      "miss once; the two data words miss once. On the 9 subsequent loop iterations, the instructions are "
      "already cached <i>unless</i> they collide with other blocks in the direct-mapped cache. Count distinct "
      "blocks touched (M's instructions, S's instructions, the two data words) and how many times each is "
      "evicted and refetched.",
      "<b>(iii) Evictions:</b> an eviction happens when a new block maps to a line already occupied by a "
      "different block. Compute the index of each address (bits) and see how many distinct blocks share a line.",
      "<b>(iv) Non-empty blocks:</b> the blocks resident at the end = the last block to occupy each of the 64 "
      "lines that were ever used; list their decimal block numbers.",
    ]))
    A(callout("<b>Method:</b> convert each address to binary, slice into tag|index|offset, note which line "
              "each block uses, and simulate the reference stream (M, then loop ×10 with S calls interleaved, "
              "plus the two data accesses). Direct-mapped collisions are what make the miss count exceed the "
              "number of distinct blocks.", 'tip'))

    A(Paragraph("Q (ca25 · Q5 / ca32 · Q4 / ca7 · Q2b). Which cache configuration, blocking or non-blocking, "
                "gives better memory performance? Between hardware and compiler prefetching, which is more "
                "likely to increase memory access time?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "<b>Non-blocking (lockup-free) caches</b> are better: during a miss they continue to serve other "
      "accesses (hit-under-miss and miss-under-miss), overlapping multiple misses and hiding latency. A "
      "blocking cache freezes on the first miss.",
      "<b>Compiler prefetching</b> is more likely to increase memory access time (or at least memory traffic) "
      "because it inserts prefetch instructions that may fetch data never used, wasting bandwidth and "
      "possibly delaying demand accesses; hardware prefetching is more conservative and based on observed "
      "patterns.",
    ]))

    # ============ 11. VIRTUAL MEMORY ============
    A(PageBreak())
    A(h1(11,"Virtual Memory & the TLB","Giving every program a private, huge address space"))
    A(p("<b>Virtual memory</b> is a technique that lets each program use a large, contiguous <i>virtual</i> "
        "address space even though physical memory is smaller and shared. The hardware translates every "
        "virtual address to a physical address using a <b>page table</b>, with the OS managing the mapping. "
        "It uses the same idea as caching, applied to main memory vs disk."))

    A(h3("11.1 Why we need virtual memory"))
    A(bullets([
      "<b>Program size</b> — a program can be larger than physical memory; only the active pages need to be "
      "resident.",
      "<b>Multiprogramming and protection</b> — each process gets its own address space; it cannot read or "
      "write another process's memory.",
      "<b>Relocation</b> — a program need not know where it will be loaded; the same binary runs anywhere.",
      "<b>Sharing</b> — common code (libraries) can be mapped into many address spaces.",
      "<b>Memory efficiency</b> — non-contiguous physical allocation removes fragmentation.",
    ]))

    A(h3("11.2 Paging and address translation"))
    A(p("Virtual memory is divided into fixed-size <b>pages</b>; physical memory into <b>frames</b> of the "
        "same size. A virtual address splits into a <b>virtual page number (VPN)</b> and a <b>page offset</b>. "
        "The VPN indexes a page table giving the <b>physical page number (PPN)</b>; the offset is unchanged."))
    A(formula("Virtual address = [ VPN | offset ]    Physical address = [ PPN | offset ]\n"
              "Page size = 2<sup>offset bits</sup> ;  #pages = virtual space / page size"))
    A(table(["Term","Meaning"],
      [["Page","Fixed-size block of virtual memory."],
       ["Frame","Fixed-size block of physical memory (same size as a page)."],
       ["Page table","Per-process array mapping VPN → PPN, with valid/dirty/protection bits."],
       ["Page fault","The page is not in memory → OS loads it from disk (very expensive, millions of cycles)."],
       ["Page replacement","Which page to evict — LRU approximation; a dirty page must be written back first."]],
      widths=[1.4,4.6]))
    A(fig("page082.jpg", w=11.5*gen.cm, cap="Virtual-to-physical address translation via the page table (source: lecture notes, p. 82)."))
    A(p("<b>Reading the figure.</b> Non-blocking (lockup-free) caches. Several misses are outstanding at once and other accesses continue to be served, instead of stalling the whole cache."))

    A(h3("11.3 The TLB — a cache for translations"))
    A(fig("page074.jpg", w=10.5*gen.cm, cap="Direct-mapped cache address-fields worked example (source: p. 74)."))
    A(p("<b>Reading the figure.</b> A direct-mapped cache example showing which block lands in which line (line = block number mod number of lines)."))
    A(p("A page-table lookup costs a memory access, so we cache recent translations in a small, fast, "
        "fully-associative <b>Translation Lookaside Buffer (TLB)</b>. A TLB hit gives the PPN in one cycle; a "
        "TLB miss walks the page table."))
    A(formula("Effective access time = TLB_hit_time + TLB_miss_rate × PageTableWalk_time\n"
              "(Then add the data access, possibly via the cache.)"))

    A(h3("11.4 Cache + virtual memory interaction"))
    A(bullets([
      "Caches can be <b>virtually indexed</b> (fast, but aliasing problems) or <b>physically indexed</b> "
      "(safe, but needs the TLB first).",
      "The common design indexes the cache with the <i>page offset</i> (same in virtual and physical) so "
      "translation can proceed in parallel with the cache lookup.",
      "A page fault is handled by the OS; the page is fetched from disk, the page table updated, and the "
      "instruction restarted.",
    ]))
    A(h3("11.5 Exam-relevant insights"))
    A(bullets([
      "Virtual memory = paging (large, coarse, disk-backed) + TLB (fast translation cache).",
      "Page size is a power of two; offset bits = log₂(page size).",
      "Misses: TLB miss (translation not cached) vs cache miss (data not cached) vs page fault (page on disk).",
      "A dirty page must be written back before eviction; a clean page can simply be dropped.",
    ]))

    # ============ 12. CACHE COHERENCE ============
    A(PageBreak())
    A(h1(12,"Multiprocessor Cache Coherence","Keeping many caches agreeing on shared data"))
    A(p("When several processors each have a private cache and share main memory, a write by one processor "
        "leaves the others holding <i>stale</i> copies. <b>Cache coherence</b> is the set of protocols that "
        "keeps all caches consistent so every read returns the most recent write. This is one of the most "
        "examined topics, so we go slowly."))

    A(h3("12.1 The coherence problem, stated precisely"))
    A(p("A memory system is <b>coherent</b> if: (1) a read by processor P returns the value written by the "
        "most recent write by any processor to that location; and (2) writes to the same location by "
        "different processors are seen in the same order by everyone. The danger: P1 writes X, but P0's cache "
        "still holds the old X and returns it."))

    A(h3("12.2 Two families of protocol"))
    A(table(["","Snooping (snoopy)","Directory-based"],
      [["Where is the state kept?","Each cache watches (snoops) a shared bus for all transactions.","A central directory records which caches hold each block."],
       ["Communication","Broadcast on the bus.","Point-to-point messages to the caches that hold the block."],
       ["Scalability","Poor — the bus becomes a bottleneck as processors are added.","Good — scales to many processors (used in large systems)."],
       ["Speed","Fast for a small number of processors.","More overhead per transaction but scalable."],
       ["Typical use","Small/medium multiprocessors, multicore with a shared bus.","Large-scale servers, NUMA machines."],
       ["Example","MSI, MESI, MOESI on a bus.","Directory protocols in big SMPs/cc-NUMA."]],
      widths=[1.5,2.3,2.2]))
    A(fig("page084.jpg", w=11.5*gen.cm, cap="Snooping vs directory-based cache coherence (source: lecture notes, p. 84)."))
    A(p("<b>Reading the figure.</b> The shared-memory multiprocessor model: several processors with private caches sharing one main memory over a bus. Coherence must keep the private copies consistent."))

    A(h3("12.3 Snooping write policies"))
    A(table(["Policy","On a write, the writing cache…","Effect on other copies"],
      [["Write-invalidate","Invalidates all other cached copies of the block.","Others must refetch on their next access. One writer, many readers."],
       ["Write-update (write-broadcast)","Broadcasts the new value to all caches holding the block.","All copies updated immediately; more bus traffic."]],
      widths=[1.5,2.6,2.0]))
    A(p("Write-invalidate is the more common (used by MSI/MESI) because it generates less traffic when a "
        "block is written repeatedly."))

    A(h3("12.4 The MSI protocol (three states)"))
    A(p("Every cached block is in one of three states. The name MSI comes from the initials."))
    A(table(["State","Meaning","Who may read/write"],
      [["M — Modified","This cache has the only copy and it is dirty (memory is stale).","This cache may read and write; it must supply the block to others and write back on eviction."],
       ["S — Shared","This block is clean and may exist in several caches.","All sharers may read; a write requires gaining ownership first."],
       ["I — Invalid","This cache does not hold a valid copy.","Neither read nor write; a miss occurs."]],
      widths=[1.2,2.6,2.2]))
    A(h3("12.5 State transitions you must know"))
    A(fig("page087.jpg", w=10.5*gen.cm, cap="MSI/MESI coherence transition table (source: p. 87)."))
    A(p("<b>Reading the figure.</b> The MSI/MESI coherence transition table. For each current state and each event (read/write hit or miss) it shows the next state and the messages sent."))
    A(table(["Event","State before","Action","State after"],
      [["Local read (PrRd)","I","Bus read; other caches supply or memory responds","S (or M if no other sharer and it gets exclusive)"],
       ["Local write (PrWr)","I","Bus read-exclusive (RFO); invalidate other copies","M"],
       ["Local write","S","Bus invalidate / RFO; others invalidate","M"],
       ["Local read","S","Hit — nothing on the bus","S"],
       ["Local read/write","M","Hit — nothing on the bus","M"],
       ["Remote read snooped","M","Supply block; write back; downgrade","S"],
       ["Remote read snooped","S","Nothing (or supply)","S"],
       ["Remote write snooped (invalidate)","S or M","Invalidate local copy (and write back if M)","I"]],
      widths=[1.8,1.0,2.4,1.0]))
    A(callout("<b>The one-line intuition:</b> a block is <b>M</b> if exactly one cache has it dirty, <b>S</b> "
              "if it is clean and may be shared, and <b>I</b> if this cache has nothing. To write, you must "
              "first become the sole owner (M).", 'tip'))

    A(h3("12.6 MESI — the fourth state and why it helps"))
    A(p("<b>MESI</b> splits the “clean and unique” case out of S into a new state <b>E (Exclusive)</b>: the "
        "block is clean <i>and</i> is the only cached copy. The advantage: a subsequent <b>write to a block "
        "in E needs no bus transaction</b> — the cache already owns it exclusively, so it can silently go "
        "E → M. In plain MSI, a clean unique block is in S, so the first write must broadcast an invalidate; "
        "MESI saves that bus traffic. This is why MESI (and its extension MOESI) is the industry standard."))
    A(table(["State","Clean/Dirty","Unique/Shared","Write without a bus transaction?"],
      [["M","Dirty","Unique","Yes (already owner)"],
       ["E","Clean","Unique","Yes (silent E→M)"],
       ["S","Clean","Shared","No — must invalidate others"],
       ["I","—","Absent","No — must fetch ownership"]],
      widths=[0.8,1.1,1.3,2.8]))
    A(p("<b>Typical MESI transitions:</b>"))
    A(bullets([
      "I → E: read miss, no other cache has the block (exclusive).",
      "I → S: read miss, another cache has a clean copy.",
      "I → M: write miss (RFO), no other sharer.",
      "S → M: local write; invalidate other copies.",
      "E → M: local write; no bus transaction (the key advantage).",
      "M → S: snooped read from another cache; supply data, write back.",
      "M/E/S → I: snooped invalidate (another cache wants to write).",
    ]))
    A(fig("page085.jpg", w=11.5*gen.cm, cap="MSI coherence example: the block value moves between caches and memory (source: lecture notes, p. 85)."))
    A(p("<b>Reading the figure.</b> Snooping coherence. Every cache watches the shared bus and invalidates or updates its copy when another processor writes the same block."))

    A(h3("12.7 Directory-based coherence"))
    A(fig("page086.jpg", w=10.5*gen.cm, cap="Directory-based coherence: states, holders and messages (source: p. 86)."))
    A(p("<b>Reading the figure.</b> Directory-based coherence. A directory records which caches hold each block, so coherence messages are sent only to the sharers instead of being broadcast."))
    A(p("Instead of broadcasting, a <b>directory</b> stores, for each block, the set of caches that hold it "
        "and its state (shared / exclusive / modified). A write sends an invalidate message only to the "
        "holders listed in the directory. This scales because traffic is point-to-point, not broadcast, but "
        "it adds a directory lookup and can become a bottleneck if a block is widely shared."))

    A(h3("12.8 Which protocol does Intel use?"))
    A(p("Intel multicore processors (e.g. Core i7) implement a <b>snooping</b> coherence protocol over an "
        "on-chip shared interconnect (the ring/uncore), using <b>MESI</b>-style states (extended toward "
        "MOESI). Because the cores are on a single die with a shared last-level cache and an on-chip "
        "interconnect, snooping is practical and avoids the directory's indirection."))

    A(h3("12.9 Exam-relevant insights"))
    A(bullets([
      "Coherence ≠ consistency: coherence is about a single location being up to date; consistency is about "
      "the <i>order</i> of accesses to different locations.",
      "Write-invalidate vs write-update is a common short-answer question.",
      "Snooping scales poorly (bus bottleneck); directory scales but costs a lookup.",
      "MESI's E state exists purely to avoid a bus transaction on the first write to a clean unique block.",
      "In a snapshot question, read each cache's state, apply the event, and update <i>all</i> affected "
      "caches and memory — never just the acting one.",
    ]))

    # ---- PYQs ----
    A(h3("Previous-Year Questions — Cache coherence"))
    A(Paragraph("Q (ca2 · Q3 / ca23 · Q2). A snapshot of two caches (P0 and P1) in a centralized shared-memory "
                "system using the MSI snooping protocol is shown. Answer: (i) If P0 wants to write Block 0, "
                "what happens to its coherency state? (ii) If P1 writes Block 1, is Block 1 on P0 invalidated? "
                "Why or why not? (iii) If P1 brings in Block M for reading and no other cache has a copy, what "
                "state is it cached in?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "<b>(i)</b> P0 issues a write. Under MSI it must gain ownership: it broadcasts a read-exclusive / "
      "invalidate, any other copy is invalidated, and P0's state goes <b>S → M</b> (or I → M if it had to "
      "fetch). If P0 already had the block in M, it stays M.",
      "<b>(ii)</b> Whether P0's copy of Block 1 is invalidated depends on the snapshot: if P0 holds Block 1 in "
      "<b>S</b> or <b>M</b>, then yes — P1's write sends an invalidate and P0 goes to <b>I</b>. If P0 holds "
      "Block 1 in <b>I</b> already (or does not cache it), there is nothing to invalidate, so it stays I.",
      "<b>(iii)</b> P1 reads Block M and no other cache has it → the block is clean and unique → cached in "
      "state <b>E</b> under MESI, or <b>S</b> under plain MSI (MSI has no E; it would be S). State which "
      "protocol the question assumes.",
    ]))
    A(callout("<b>How to answer snapshot questions:</b> read the table, list each cache's state, then apply "
              "the event to <i>every</i> cache that holds the block (the actor and all snoopers), plus the "
              "memory line if a dirty block is written back.", 'tip'))

    A(Paragraph("Q (ca6 · Q5). A bus-based shared memory with three processors P1, P2, P3; memory blocks x, y, "
                "z; each cache holds only two blocks; states valid (V) or invalid (I). Caches start empty. "
                "Memory: x=0, y=200, z=... . Apply the sequence of 10 accesses and show caches, memory and "
                "states after each step, using write-through + write-invalidate.", ST['q']))
    A(formula("1) P1: Read(x,y)   2) P2: Read(x,z)   3) P3: Read(y,z)   4) P1: x = x+10\n"
              "5) P1: Read(z)    6) P2: Read(x)     7) P3: x = 15      8) P1: z = z+10\n"
              "9) P2: x = 15     10) P2: z = z+30"))
    A(Paragraph("<b>Solution.</b> Simulate step by step. Under write-through + write-invalidate, a write "
                "updates memory immediately (write-through) and invalidates all other cached copies. With a "
                "2-block cache, a third block forces eviction (LRU or the one that is not being used).", ST['ans']))
    A(table(["Step","Action","P1 cache","P2 cache","P3 cache","Memory x,y,z"],
      [["1","P1 reads x,y","x(V), y(V)","—","—","x=0, y=200, z"],
       ["2","P2 reads x,z","x(V), y(V)","x(V), z(V)","—","x=0, y=200, z"],
       ["3","P3 reads y,z","x(V), y(V)","x(V), z(V)","y(V), z(V)","unchanged"],
       ["4","P1: x=x+10 (10)","x(V=10), y(V)","x(I) ← invalidated","x(I)","x=10 (write-through)"],
       ["5","P1 reads z","evict y, z(V)","x(I), z(V)","y(V), z(V)","unchanged"],
       ["6","P2 reads x","x(V=10), z(V)","evict z? x(V)","y(V), z(V)","unchanged"],
       ["7","P3: x=15","x(I)","x(I)","x(V=15)","x=15"],
       ["8","P1: z=z+10","z(V=old+10)","x(I)","y(V), z(I)","z updated (write-through)"],
       ["9","P2: x=15","x(I)","x(V=15)","x(I)","x=15"],
       ["10","P2: z=z+30","z(I)","x(V), z(V)","y(V), z(I)","z updated"]],
      widths=[0.5,1.6,1.2,1.2,1.2,1.3]))
    A(p("<b>Key observations to state:</b> every write invalidates all other copies (so the state column flips "
        "to I); write-through keeps memory current at every step; and the 2-block cache forces evictions when "
        "a third distinct block is touched. The final memory values reflect the last write to each location."))

    A(Paragraph("Q (ca29 · Q3b,c). (b) Which cache coherence protocol does Intel i7 use? Explain. (c) The MESI "
                "protocol has four states; what is the advantage of the fourth state and how does it solve the "
                "coherence problem? Explain state transitions with an example.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(bullets([
      "<b>(b)</b> Intel i7 uses a <b>snooping MESI (MOESI) protocol</b> on an on-chip ring interconnect. "
      "Snooping works because the cores share a bus-like ring and a shared last-level cache; each cache "
      "monitors transactions and updates its states, so a write invalidates other copies and a read obtains "
      "the latest value.",
      "<b>(c)</b> The fourth state <b>E (Exclusive)</b> means “clean and unique”. Its advantage: a write to a "
      "block in E requires <b>no bus transaction</b> (the cache already owns it exclusively), so it silently "
      "moves E → M. In MSI the same block would be S, forcing a broadcast invalidate on the first write. This "
      "saves bandwidth and latency. Transitions: I→E on an exclusive read miss; E→M on a local write; M→S on "
      "a snooped read (supply data + write back); S→I on a snooped invalidate.",
    ]))


    A(Paragraph("Q (ca3 · Q3). What are the pros and cons of each cache organization?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(table(["Organization","Pros","Cons"],
      [["Direct mapped","Cheapest, fastest hit (one comparator), simple.","High conflict misses; a fixed line per block."],
       ["Fully associative","No conflict misses; any block anywhere.","Expensive: must compare all tags; slower hit; complex replacement."],
       ["Set associative (n-way)","Good compromise: few conflict misses, moderate hardware, n comparators.","More hardware than direct-mapped; replacement policy needed."]],
      widths=[1.4,2.4,2.2]))

    A(Paragraph("Q (ca3 · Q4). What is virtual memory? Explain the need for virtual memory.", ST['q']))
    A(Paragraph("<b>Solution.</b> Virtual memory lets each program use a large, contiguous virtual address "
      "space that is mapped to physical memory by a page table. It is needed to (1) run programs larger than "
      "physical memory (only active pages resident), (2) give each process an isolated, protected address "
      "space, (3) allow relocation so the same binary runs anywhere, (4) share common code between processes, "
      "and (5) avoid fragmentation by using fixed-size pages.", ST['ans']))

    A(Paragraph("Q (ca3 · Q6 / ca7 · Q2a / ca32 · Q4). Explain the cache optimization techniques to reduce the "
      "miss rate (and to reduce access time).", ST['q']))
    A(Paragraph("<b>Solution (reduce miss rate).</b> Larger block size (spatial locality); higher "
      "associativity (fewer conflict misses); larger cache (fewer capacity misses); hardware/compiler "
      "prefetching; compiler loop transformations (blocking, interchange) for locality; a victim cache to "
      "recover conflict evictions.", ST['ans']))
    A(Paragraph("<b>To reduce access time (hit time).</b> Smaller/simpler (direct-mapped) caches; way "
      "prediction; pipelined cache access; avoiding translation on the critical path (TLB, virtual indexing).", ST['ans']))

    A(Paragraph("Q (ca3 · Q7). What is the effect on power consumption of giving priority to read misses over "
      "writes?", ST['q']))
    A(Paragraph("<b>Solution.</b> Giving read misses priority lets the read complete sooner, so the processor "
      "resumes and the cache/memory system returns to a lower-power state sooner; writes can be buffered and "
      "drained lazily. The net effect is lower average power because the high-power memory access is not "
      "delayed by a lower-priority write. (It also reduces read latency at some cost to write latency.)", ST['ans']))

    A(Paragraph("Q (ca8 · Q4b). A write miss takes 50 cycles to establish ownership, 10 cycles to issue each "
      "invalidate, and 80 cycles for an invalidate to complete once issued. Four other processors share the "
      "block. How long does the write miss stall the writing processor under sequential consistency (invalidates "
      "must be acknowledged)? How long if execution could continue after ownership without waiting for "
      "invalidates?", ST['q']))
    A(formula("Sequential consistency (wait for all invalidates):\n"
              "  = ownership 50 + [issue 10 + complete 80] for each of 4 sharers (issued in sequence)\n"
              "  = 50 + 4×(10) + 80 = 50 + 40 + 80 = 170 cycles\n"
              "  (all four invalidates can be issued back-to-back; the last one still needs 80 cycles to "
              "complete)\n\n"
              "Continue after ownership (don't wait for invalidates):\n"
              "  = 50 cycles only"))
    A(Paragraph("<b>Answer:</b> ≈ 170 cycles with full acknowledgement; ≈ 50 cycles if we proceed after "
      "ownership. This shows why relaxed/weak consistency models exist — waiting for every invalidate is "
      "expensive.", ST['ans']))

    A(Paragraph("Q (ca26 · Q2b). A cache has a 32-byte line and memory requires 30 ns to transfer a 4-byte "
      "word. For a line written at least once before eviction, what is the average number of writes before "
      "eviction for a write-back cache to beat a write-through cache? How does the answer change with a block "
      "transfer (first word 30 ns, each subsequent word 5 ns)?", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("Without block transfer:\n"
              "  Line = 32 B = 8 words × 30 ns = 240 ns to write the whole line.\n"
              "  Write-through writes 4 B every store; write-back writes the line once on eviction.\n"
              "  Break-even: n × 30 (write-through) = 240 (write-back) → n = 8 writes.\n"
              "  So the line must be written ≥ 8 times for write-back to win.\n\n"
              "With block transfer (first word 30 ns, then 5 ns each):\n"
              "  Whole line = 30 + 7×5 = 65 ns.\n"
              "  Break-even: n × 30 = 65 → n ≈ 2.17, i.e. about 3 writes."))
    A(p("<b>Answer:</b> 8 writes without block transfer; about 2-3 writes with block transfer. Block transfer "
      "makes write-back pay off with far fewer writes."))

    A(Paragraph("Q (ca37 · Q2b / ca38 · Q2). A 16 KB direct-mapped 256 B-block unified cache on a 16 MB "
      "memory; word/instruction length 16 bits. Routine M (12 instruction words from 0x4230FA) calls S (4 "
      "words from 0x70F168); two data words at 0x748074 and 0x846064; the last 5 instructions of M loop 10 "
      "times with a call to S as the 2nd instruction; cache empty. (i) Address components, (ii) misses, "
      "(iii) evictions, (iv) non-empty block numbers.", ST['q']))
    A(Paragraph("<b>Solution.</b>", ST['ans']))
    A(formula("(i) offset = log₂(256) = 8 ; index = log₂(16384/256)=log₂64 = 6 ; address = log₂(16 MB)=24 bits\n"
              "    tag = 24 − 6 − 8 = 10  →  [ tag:10 | index:6 | offset:8 ]"))
    A(bullets([
      "<b>(ii) Misses:</b> convert each address to binary; slice into tag|index|offset. The first access to "
      "each distinct block misses; a later access to a block whose line has been overwritten by a "
      "conflicting block misses again. Count compulsory + conflict misses over the reference stream "
      "(M's 12 words, then 10 loop iterations each with a call to S, plus the two data words).",
      "<b>(iii) Evictions:</b> each time a new block maps to a line already holding a <i>different</i> block, "
      "the old block is evicted. Compare the index fields to find collisions.",
      "<b>(iv) Non-empty blocks:</b> list, in decimal, the block number currently in each of the 64 lines "
      "that were used at the end.",
    ]))
    A(p("<b>Method to write in the exam:</b> show the binary slicing for one instruction address and one data "
      "address, then state the line number each uses; the collisions between M's code, S's code and the data "
      "words drive the miss and eviction counts."))

    return F
