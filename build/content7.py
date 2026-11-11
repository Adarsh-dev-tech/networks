"""Part VII — Previous-year-question index / checklist."""
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST

# Map every PNG to (topic, what it asks)
INDEX = [
 ("ca1",  "1, 2, 3, 5", "Performance (MIPS, CPU time); pipelining speed-up vs multi-cycle; loop dependences & renaming", "§3, §2"),
 ("ca2",  "3, 12",      "Loop dependences (S1/S2) and parallelisation; MSI cache-coherence snapshot (2 caches)", "§2, §14"),
 ("ca3",  "1, 2, 3, 11","Arch vs organization; derive Amdahl; cache organizations pros/cons; virtual memory; FPSQR design comparison; cache optimization; power & read misses", "§1, §3, §12, §13"),
 ("ca4",  "2",          "Amdahl (fraction enhanced); quad-core Amdahl; benchmark CPI enhancements", "§3"),
 ("ca5",  "2",          "CPU time from instruction mix (ALU/branch/sw/lw) at 500 MHz", "§3"),
 ("ca6",  "12",         "3-processor bus shared memory, write-through + write-invalidate, full event trace", "§14"),
 ("ca7",  "2, 10, 12",  "Amdahl with communication overhead; cache optimization + ISA question; CPU time; snoopy vs directory coherence", "§3, §12, §14"),
 ("ca8",  "7, 12",      "Branch-target buffer penalty; write-miss stall time with ownership + invalidates", "§8, §14"),
 ("ca9",  "5, 7",       "5-stage pipeline flow; branch in pipeline; hazards, dependences & nops; branch-hazard schemes", "§6, §8"),
 ("ca10", "3, 5",       "Data dependences (RAW/WAW); optimal pipeline schedule with forwarding + CPI; C→MIPS hazards & reorder", "§2, §6"),
 ("ca11", "6",          "DAXPY loop unrolled 3×, fresh registers, redundant computation removed", "§7"),
 ("ca12", "8, 14",      "Tomasulo tables at cycle 6; vector vs SIMD vs GPU", "§9, §15"),
 ("ca13", "3, 5",       "Four RISC fragments: dependences & forwarding/stalls; 5-stage latencies → cycle time, latency, throughput; MIPS deps & schedule", "§2, §6"),
 ("ca14", "5, 9",       "Reorder instructions to remove stalls; count RAW hazards and register-rename", "§6, §10"),
 ("ca15", "10, 12",     "AMAT with an added L2 (required L2 hit rate); multicore CPI needed to beat single core", "§12, §14"),
 ("ca16", "5",          "For each sequence: must stall / forwarding / no stall", "§6"),
 ("ca17", "5, 7",       "Pipeline instruction mix: branch-adder use %, data-memory use %, pipelining speed-up", "§6, §8"),
 ("ca18", "8",          "Tomasulo on a loop with multiply latency and possible cache misses", "§9"),
 ("ca19", "2, 5",       "Performance (MIPS, CPU time) + pipelining speed-up (repeat of ca1 Q1)", "§3, §6"),
 ("ca20", "5",          "Resource/control hazards on a MIPS fragment with two memories", "§6"),
 ("ca21", "5, 7, 8",    "Single-memory structural hazard; pipeline mix; Tomasulo for hazards", "§6, §8, §9"),
 ("ca22", "3",          "Loop dependences (true/output/anti) and renaming (repeat of ca1 Q2a)", "§2"),
 ("ca23", "14, 12",     "Basic structure of a vector architecture; MSI coherence snapshot", "§15, §14"),
 ("ca24", "6",          "DAXPY unroll-until-no-stalls, schedule and time per element", "§7"),
 ("ca25", "9, 10",      "ROB contents after 2 loop iterations; critical-word-first; cache tag bits; blocking vs non-blocking + prefetch", "§10, §12"),
 ("ca26", "2, 10, 14",  "Amdahl (scalar + matrix); energy saved by V/f scaling; AMAT with L2", "§3, §12, §15"),
 ("ca27", "3, 5, 10",   "Write-back vs write-through break-even; RAW/WAR/WAW; pipeline phases and branch overhead", "§2, §6, §12"),
 ("ca28", "6, 7, 9",    "Static vs dynamic scheduling; three control-hazard techniques; Tomasulo + speculation hardware", "§7, §8, §10"),
 ("ca29", "12, 14",     "GPU peak throughput & memory bound; Intel i7 coherence; MESI fourth state", "§14, §15"),
 ("ca30", "4, 2, 5",    "Server-farm MTTF; 22-core Amdahl; pipeline throughput after splitting a stage", "§4, §3, §6"),
 ("ca31", "5",          "Types of hazards and impact; 5-stage (IF/ID/OF/EX/WO) cycle count with forwarding", "§6"),
 ("ca32", "5, 7, 9, 10","Four branch predictors & misprediction; clock cycle time (5 vs 10 stage); hardware speculation; cache optimization for access time; pipeline phases & branch overhead", "§6, §8, §10, §12"),
 ("ca33", "2, 4, 14",   "Three modification versions (component speedups) ranking; Amdahl matrix; energy; execution time", "§3, §4, §15"),
 ("ca34", "5, 8, 7",    "OOO advantages; pipeline phases with static predictor; discuss Tomasulo + cycle for F10", "§6, §8, §9"),
 ("ca35", "10",         "Critical-word-first & early restart cycles; merging write-buffer size and speed-up", "§12"),
 ("ca36", "2",          "Amdahl with a slowdown (FP unit speeds up but cache slows); vectorisation percentage to match a 2× vector speed-up", "§3"),
 ("ca37", "10",         "Micro-benchmark cache block sizes from a latency chart; direct-mapped cache address components", "§12"),
 ("ca38", "10, 7",      "Direct-mapped cache: misses, evictions, non-empty blocks; branch-target-buffer penalty", "§12, §8"),
 ("ca39", "6, 9",       "Register renaming with T-registers; count stalls with dependence-aware pipeline; Tomasulo & ROB", "§7, §10"),
 ("ca40", "9, 14",      "Tomasulo + ROB/commit discussion; vector vs hybrid (GPU) execution time", "§10, §15"),
 ("ca41", "14",         "Vector/array processor features used in GPUs", "§15"),
]

def build():
    F=[]
    def A(x): F.extend(x if isinstance(x,list) else [x])
    A(PageBreak())
    A(h1(16,"Previous-Year Question Index & Revision Checklist","Every exam question mapped to its topic and solution"))
    A(p("This table is your map. Each PNG file (a scan of a past paper) is listed with the topics it covers "
        "and the section of this guide where the theory and the worked solution live. Use it to jump "
        "straight from a topic to the questions that examine it, and to make sure no question is left "
        "unrevised."))
    rows=[]
    for png, topics, what, sec in INDEX:
        rows.append([f"<b>{png}.png</b>", topics, what, sec])
    A(table(["Paper","Topic(s)","What it asks","Solution in"], rows, widths=[0.7,0.9,4.2,0.8]))
    A(callout("<b>How to revise with this index:</b> read a section, then immediately attempt the papers "
              "listed against it. If a paper covers several topics, attempt it after the last of those "
              "topics. The section numbers in the right column point to the theory and the step-by-step "
              "solution for each question.", 'tip'))

    A(h3("Topic-to-paper cross-reference (the reverse view)"))
    A(table(["Topic","Papers that examine it"],
      [["§1 Architecture vs organization","ca3"],
       ["§3 Performance & Amdahl","ca1, ca3, ca4, ca5, ca7, ca19, ca26, ca30, ca33, ca36"],
       ["§2 ISA, dependences, renaming","ca1, ca2, ca10, ca13, ca22, ca27"],
       ["§4 Dependability (MTTF)","ca30, ca33"],
       ["§6 Pipelining & hazards","ca1, ca9, ca10, ca13, ca14, ca16, ca17, ca19, ca20, ca21, ca27, ca30, ca31, ca32, ca34"],
       ["§7 ILP, unrolling, scheduling","ca11, ca24, ca28, ca39"],
       ["§8 Branch prediction","ca8, ca9, ca17, ca21, ca28, ca32, ca34, ca38"],
       ["§9 Dynamic scheduling / Tomasulo","ca12, ca18, ca21, ca34"],
       ["§10 Speculation & ROB","ca14, ca25, ca28, ca32, ca39, ca40"],
       ["§12 Cache memory","ca3, ca7, ca15, ca25, ca26, ca27, ca32, ca35, ca37, ca38"],
       ["§13 Virtual memory","ca3"],
       ["§14 Cache coherence","ca2, ca6, ca7, ca8, ca15, ca23, ca29"],
       ["§11 Multiprocessors","ca7, ca15"],
       ["§15 Vector / SIMD / GPU","ca12, ca23, ca26, ca29, ca33, ca40, ca41"]],
      widths=[2.2,3.8]))

    A(h3("Final revision checklist"))
    A(p("Tick each item once you can explain it and do the associated questions without notes."))
    A(table(["✔","Skill","Section","Papers"],
      [["☐","Explain architecture vs organization with an example","§1","ca3"],
       ["☐","Compute CPU time, CPI, MIPS from an instruction mix","§3","ca1, ca5, ca19, ca33"],
       ["☐","Apply Amdahl's law, including with a slowdown","§3","ca3, ca4, ca7, ca26, ca30, ca36"],
       ["☐","Find RAW/WAR/WAW dependences and rename them away","§2","ca1, ca2, ca22, ca27"],
       ["☐","Compute MTTF, MTTR, availability","§4","ca30"],
       ["☐","Draw a pipeline timing table and count stalls","§6","ca9, ca10, ca13, ca16, ca27, ca31, ca32, ca34"],
       ["☐","Compute cycle time, latency, throughput, pipelining speed-up","§6","ca13, ca30, ca32"],
       ["☐","Unroll a loop, schedule it, compute time per element","§7","ca11, ca24, ca39"],
       ["☐","Compute branch penalties (static, BTB, 2-bit)","§8","ca8, ca17, ca32, ca38"],
       ["☐","Fill Tomasulo tables cycle by cycle","§9","ca12, ca18, ca34"],
       ["☐","Explain speculation, ROB and the commit stage","§10","ca25, ca28, ca39, ca40"],
       ["☐","Split an address into tag/index/offset; compute AMAT","§12","ca15, ca25, ca26, ca35, ca37, ca38"],
       ["☐","Explain virtual memory, paging and the TLB","§13","ca3"],
       ["☐","Apply MSI/MESI state transitions in a snapshot","§14","ca2, ca6, ca23, ca29"],
       ["☐","Compare snooping vs directory coherence","§14","ca7, ca29"],
       ["☐","Compute GPU peak throughput and decide memory-bound","§15","ca29, ca40, ca41"]],
      widths=[0.4,3.0,0.7,1.9]))
    A(callout("<b>You are exam-ready when</b> you can, from memory: write the performance equation and "
              "Amdahl's law; name the three hazards and their fixes; draw the 5-stage timing table; list the "
              "three C's and the address split; and walk through an MSI/MESI transition. Everything else in "
              "this guide hangs off those five skeletons.", 'tip'))
    return F
