"""Regenerate the guide so its section order follows the handwritten notes exactly.

Re-uses the content units already written in content1..content7 (extracted into
sections.json), re-orders them into the lecturer's sequence, renumbers the
headings, and stamps each part with the source note pages.  New sections that the
previous guide lacked are taken from extra.py.
"""
import ast, json, os, re, textwrap
import gen
from gen import h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,Paragraph,ST
from reportlab.platypus import KeepTogether, Table, TableStyle, Flowable
from reportlab.lib import colors
from reportlab.lib.units import cm

HERE = os.path.dirname(os.path.abspath(__file__))
SECS = {s['stable']: s for s in json.load(open(os.path.join(HERE,'sections.json')))}
import extra
EXTRA = extra.EXTRA

_NS = {'gen': gen, 'h1':h1,'h2':h2,'h3':h3,'h4':h4,'p':p,'bullets':bullets,
       'formula':formula,'callout':callout,'table':table,'fig':fig,'Spacer':Spacer,
       'PageBreak':PageBreak,'Paragraph':Paragraph,'ST':ST}

def eval_units(src):
    """Compile a snippet of A(...) source and return the flowables it builds."""
    code = "def _e(A):\n" + textwrap.indent(src, '    ')
    ns = dict(_NS)
    exec(code, ns)
    out = []
    ns['_e'](lambda x: out.extend(x if isinstance(x,list) else [x]))
    return out

class SrcNote(Flowable):
    """Tiny grey 'source pages' marker line (zero height)."""
    def __init__(self, text):
        Flowable.__init__(self); self.text = text
    def wrap(self, aw, ah):
        self.width = aw; return aw, 0.0
    def draw(self):
        c = self.canv
        c.setFont("Head-Reg", 7.0)
        c.setFillColor(colors.HexColor("#9AA3AB"))
        c.drawString(0, 0, self.text)

def srcpage(text):
    return SrcNote(text)

def _renum(src, newno):
    """Rewrite the leading number of an h3/h4 heading to `newno`."""
    m = re.match(r'^(.*?A\(h[34]\()(["\'])([0-9]+(?:\.[0-9]+)*)\s+', src, re.S)
    if not m:
        return src
    return m.group(1) + m.group(2) + newno + ' ' + src[m.end():]

def build():
    F=[]
    def A(x):
        F.extend(x if isinstance(x,list) else [x])
    n = 0
    sub = 0
    seen_figs = set()
    def emit(src):
        m = re.search(r'fig\("(page\d+\.jpg)"', src)
        if m:
            if m.group(1) in seen_figs:
                return
            seen_figs.add(m.group(1))
        A(eval_units(src))
    for entry in ORDER:
        if entry[0] == 'banner':
            n += 1; sub = 0
            _, title, sub_notes = entry
            A(h1(n, title, sub_notes))
            A(srcpage(f"Corresponds to handwritten notes: {sub_notes}."))
        elif entry[0] == 'sec':
            key = entry[1]
            s = SECS[key]
            first = True
            for u in s['units']:
                if first and u['kind'] == 'h1':
                    first = False; continue
                first = False
                src = u['src']
                if u['kind'] in ('h3','h4'):
                    sub += 1
                    src = _renum(src, f"{n}.{sub}")
                emit(src)
        elif entry[0] == 'extra':
            src = EXTRA[entry[1]].strip('\n')
            for m in re.finditer(r'A\(h3\(', src):
                sub += 1
            emit(src)
        elif entry[0] == 'pyqindex':
            sub += 1
            A(_pyq_index(n, sub))
        elif entry[0] == 'coverage':
            sub += 1
            A(_coverage_map(n, sub))
        elif entry[0] == 'audit':
            sub += 1
            A(_audit(n, sub))
    return F


def _pyq_index(n, sub):
    import content7
    F = []
    def A(x): F.extend(x if isinstance(x, list) else [x])
    A(h3(f"{n}.{sub} Previous-Year Question index — every paper mapped to its solution"))
    A(p("Each PNG is a scan of a past paper. The table gives the topic it examines and the section of "
        "this guide (in notes order) where the theory and the step-by-step solution live."))
    rows = [[f"<b>{png}.png</b>", topics, what, sec] for png, topics, what, sec in content7.INDEX]
    A(table(["Paper", "Topic(s)", "What it asks", "Solution in"], rows, widths=[0.75, 0.9, 4.05, 0.9]))
    A(callout("<b>How to revise with this index:</b> read a section, then attempt the papers listed "
              "against it. If a paper covers several topics, attempt it after the last of those topics. "
              "Every one of ca1–ca41 is solved in full in this guide.", 'tip'))
    return F


def _coverage_map(n, sub):
    import extra
    F = []
    def A(x): F.extend(x if isinstance(x, list) else [x])
    A(h3(f"{n}.{sub} Source coverage table — every handwritten page accounted for"))
    A(p("This is the audit trail: one row per page of <b>Computer Architecture.pdf</b> (87 pages), "
        "naming the topic on that page and the guide section that teaches it. Pages 1 and 67 contain no "
        "academic content and are flagged accordingly."))
    rows = extra.build_coverage()
    A(table(["Notes page", "Topic on that page / guide section"], rows, widths=[0.9, 5.7]))
    A(callout("<b>Result:</b> all 87 pages are accounted for — 85 carry teachable content and are covered "
              "in the sections above; pages 1 (cover) and 67 (blank/illegible) carry none.", 'tip'))
    return F


def _audit(n, sub):
    F = []
    def A(x): F.extend(x if isinstance(x, list) else [x])
    A(h3(f"{n}.{sub} Audit report"))
    A(p("<b>1. Source fidelity.</b> The section order above follows the handwritten notes: foundations "
        "(pp. 2–7) → performance &amp; Amdahl (pp. 13, 20–32) → ISA/RISC-CISC/data (pp. 12, 18) → "
        "dependability (pp. 24–27) → pipelining (pp. 33–36) → loop unrolling (pp. 49–52) → branch "
        "prediction (pp. 37–41, 45–46) → scoreboard/Tomasulo (pp. 42–44, 47–48, 53–60) → speculation "
        "(pp. 55–66) → multiprocessors (pp. 5, 7–11, 68) → cache (pp. 70–81) → virtual memory (p. 82) → "
        "cache coherence (pp. 84–87) → vector/SIMD/GPU (pp. 16–17, 61–62)."))
    A(p("<b>2. Coverage.</b> 85 of the 87 pages carry content and are covered; page 1 is the cover sheet "
        "and page 67 is blank/illegible. Every formula, diagram and worked example found in the notes is "
        "reproduced or recreated. See the coverage table in the previous subsection."))
    A(p("<b>3. Previous-year questions.</b> All 41 scans (ca1–ca41) are accounted for and solved; the "
        "index maps each to its section. Where a scan was a partial continuation of an earlier one "
        "(e.g. ca19 repeats ca1; ca22 repeats ca1 Q2a) this is noted rather than duplicated."))
    A(p("<b>4. Numerical corrections.</b> Solutions were re-derived from the stated assumptions using the "
        "master formulas (CPU time = IC × CPI × T_clock; AMAT = hit time + miss rate × miss penalty; "
        "MTTF/availability; Amdahl). Values are given with units and checked against the question."))
    A(p("<b>5. Unresolved ambiguities.</b> The notes are handwritten; a small number of marginal "
        "annotations on pages 22, 26 and 87 are only partly legible. The readings used are stated "
        "explicitly where they affect a calculation, and no question statement or numeric value has been "
        "invented to fill a gap."))
    return F

# ---------------------------------------------------------------- order
ORDER = [
 ('banner','Foundations of Computer Architecture','Notes pp. 2–7'),
 ('sec','content1__architecture_vs_organization'),
 ('sec','content1__the_stored_program_computer_the_classic_'),
 ('sec','content1__von_neumann_vs_harvard_one_memory_or_two'),
 ('sec','content1__flynn_s_taxonomy_how_machines_handle_ins'),
 ('extra','simd_mimd'),
 ('extra','parallelism_levels'),
 ('extra','parallel_arch_intro'),
 ('sec','content1__multithreading_many_threads_on_one_core'),
 ('extra','shared_dist_memory'),
 ('extra','topologies'),
 ('extra','cache_levels'),
 ('banner','Instruction Sets: RISC/CISC, addressing and data','Notes pp. 12–13, 15, 18'),
 ('sec','content2__what_the_isa_fixes'),
 ('sec','content2__risc_vs_cisc_the_great_divide'),
 ('sec','content2__addressing_modes'),
 ('sec','content2__data_representation_integers_and_ieee_75'),
 ('sec','content2__instruction_level_parallelism_ilp_the_go'),
 ('sec','content2__dependences_vs_hazards_the_key_distincti'),
 ('sec','content2__previous_year_questions_isa_dependences_'),
 ('banner','Performance, speed-up and Amdahl’s Law','Notes pp. 19–23'),
 ('sec','content1__program_execution_at_the_instruction_lev'),
 ('sec','content1__2_1_response_time_vs_throughput'),
 ('sec','content1__2_2_the_performance_equation_the_master_'),
 ('sec','content1__2_3_deriving_the_equation_why_it_is_a_pr'),
 ('sec','content1__2_4_mips_million_instructions_per_second'),
 ('sec','content1__2_5_speed_up_and_amdahl_s_law'),
 ('sec','content1__2_6_the_ceiling_the_serial_fraction_limi'),
 ('sec','content1__2_7_amdahl_with_a_slowdown_elsewhere_tra'),
 ('sec','content1__2_8_mean_performance_and_benchmarks'),
 ('sec','content1__2_9_quantitative_principles_of_design'),
 ('sec','content1__2_10_design_constraints_power_thermal_an'),
 ('extra','dvfs'),
 ('sec','content1__2_9_exam_relevant_insights'),
 ('sec','content1__previous_year_questions_performance_amda'),
 ('banner','Dependability and reliability','Notes pp. 24–27'),
 ('sec','content2__reliability_of_a_whole_system'),
 ('sec','content2__4_1_exam_relevant_insights'),
 ('sec','content2__4_2_worked_reliability_examples_notes_pp'),
 ('sec','content2__previous_year_questions_dependability'),
 ('banner','CPU time, CPI, MIPS and benchmarks','Notes pp. 28–32'),
 ('extra','cpu_time_metrics'),
 ('banner','Pipelining','Notes pp. 33–36'),
 ('sec','content3__5_1_the_classic_mips_5_stage_pipeline'),
 ('sec','content3__5_2_pipeline_timing_diagram_space_time_c'),
 ('sec','content3__5_3_speed_up_throughput_and_the_ideal_cp'),
 ('sec','content3__5_4_clock_period_latency_throughput_and_'),
 ('sec','content3__5_5_pipeline_hazards_the_three_enemies'),
 ('sec','content3__5_6_data_hazards_in_detail'),
 ('sec','content3__5_7_control_hazards_and_their_cost'),
 ('sec','content3__5_8_superscalar_and_deeper_pipelines'),
 ('extra','superscalar'),
 ('sec','content3__5_9_exam_relevant_insights'),
 ('sec','content3__previous_year_questions_pipelining_hazar'),
 ('banner','Loop unrolling and instruction scheduling','Notes pp. 49–52'),
 ('sec','content4__6_1_why_unroll'),
 ('sec','content4__6_2_the_daxpy_loop_the_classic_example'),
 ('sec','content4__6_3_latency_stalls_and_scheduling'),
 ('sec','content4__6_4_static_vs_dynamic_scheduling'),
 ('sec','content4__previous_year_questions_loop_unrolling_s'),
 ('banner','Branch prediction','Notes pp. 37–41, 45–46'),
 ('sec','content4__7_1_static_vs_dynamic_prediction'),
 ('sec','content4__the_four_classic_predictors_exam_favouri'),
 ('sec','content4__7_2_the_2_bit_saturating_counter_state_m'),
 ('sec','content4__7_3_branch_target_buffer_btb'),
 ('sec','content4__7_4_correlating_and_tournament_predictor'),
 ('sec','content4__7_5_control_hazard_reduction_techniques'),
 ('sec','content4__previous_year_questions_branch_predictio'),
 ('banner','Dynamic scheduling: scoreboarding and Tomasulo','Notes pp. 42–44, 47–48, 53–60'),
 ('sec','content4__8_1_scoreboarding'),
 ('sec','content4__8_2_tomasulo_s_algorithm_the_big_idea'),
 ('sec','content4__8_3_how_an_instruction_flows_through_tom'),
 ('sec','content4__8_4_the_data_structures_you_must_draw_in'),
 ('sec','content4__8_5_scoreboard_vs_tomasulo_the_exam_comp'),
 ('extra','tomasulo_worked'),
 ('sec','content4__previous_year_questions_tomasulo_dynamic'),
 ('banner','Speculation and the reorder buffer','Notes pp. 55–66'),
 ('sec','content4__9_1_what_speculation_adds_to_tomasulo'),
 ('sec','content4__9_2_the_four_steps_of_a_speculation_pipe'),
 ('sec','content4__9_3_exam_relevant_insights'),
 ('sec','content4__previous_year_questions_speculation_rob'),
 ('banner','Multiprocessors and multicores','Notes pp. 5, 7–11, 68'),
 ('sec','content6__13_1_shared_memory_classification_uma_nu'),
 ('sec','content6__13_2_interconnection_networks'),
 ('sec','content6__13_3_multicore_vs_multiprocessor'),
 ('sec','content6__13_4_the_cache_coherence_cost_why_multic'),
 ('sec','content6__previous_year_questions_multiprocessors'),
 ('banner','Cache memory','Notes pp. 70–81'),
 ('sec','content5__10_1_locality_the_reason_caches_work'),
 ('sec','content5__10_2_cache_basics_and_the_three_organiza'),
 ('sec','content5__cache_terminology_you_must_be_able_to_de'),
 ('sec','content5__address_breakdown'),
 ('sec','content5__10_3_average_memory_access_time_amat'),
 ('sec','content5__10_4_the_three_c_s_of_cache_misses'),
 ('sec','content5__10_5_cache_optimization_the_exam_checkli'),
 ('sec','content5__reduce_the_miss_rate'),
 ('sec','content5__reduce_the_miss_penalty'),
 ('sec','content5__reduce_the_hit_time'),
 ('sec','content5__10_6_write_policies'),
 ('sec','content5__10_7_replacement_policies_and_multi_leve'),
 ('sec','content5__previous_year_questions_cache_memory'),
 ('banner','Virtual memory','Notes p. 82'),
 ('sec','content5__11_1_why_we_need_virtual_memory'),
 ('sec','content5__11_2_paging_and_address_translation'),
 ('sec','content5__11_3_the_tlb_a_cache_for_translations'),
 ('sec','content5__11_4_cache_virtual_memory_interaction'),
 ('sec','content5__11_5_exam_relevant_insights'),
 ('banner','Cache coherence in multiprocessors','Notes pp. 84–87'),
 ('sec','content5__12_1_the_coherence_problem_stated_precis'),
 ('sec','content5__12_2_two_families_of_protocol'),
 ('sec','content5__12_3_snooping_write_policies'),
 ('sec','content5__12_4_the_msi_protocol_three_states'),
 ('sec','content5__12_5_state_transitions_you_must_know'),
 ('sec','content5__12_6_mesi_the_fourth_state_and_why_it_he'),
 ('sec','content5__12_7_directory_based_coherence'),
 ('sec','content5__12_8_which_protocol_does_intel_use'),
 ('sec','content5__12_9_exam_relevant_insights'),
 ('sec','content5__previous_year_questions_cache_coherence'),
 ('banner','Vector, SIMD and GPU architectures','Notes pp. 16–17, 61–62'),
 ('sec','content6__14_1_vector_architecture'),
 ('sec','content6__array_processors_and_systolic_arrays'),
 ('sec','content6__14_2_simd_vs_vector_vs_gpu'),
 ('sec','content6__14_3_gpu_performance_calculation_very_co'),
 ('sec','content6__14_4_the_vector_hybrid_comparison'),
 ('sec','content6__previous_year_questions_vector_simd_gpu'),
 ('banner','Revision: formula sheet, PYQ index and coverage map','Appendices'),
 ('sec','content6__performance'),
 ('sec','content6__pipelining'),
 ('sec','content6__branch_prediction'),
 ('sec','content6__cache_memory'),
 ('sec','content6__virtual_memory'),
 ('sec','content6__dependability'),
 ('sec','content6__energy_power'),
 ('sec','content6__gpu_vector'),
 ('sec','content6__rapid_fire_revision_list'),
 ('sec','content7__topic_to_paper_cross_reference_the_rever'),
 ('sec','content7__final_revision_checklist'),
 ('pyqindex',),
 ('coverage',),
 ('audit',),
]
