"""Conversion of problems.yaml into the opltools schema.

Every entry from the original YAML is preserved as a `#!` comment block
directly above the Python object(s) it was converted into.  Where the
original YAML carried information that does not fit into the new schema,
a `FIXME` comment is used to flag the loss.

IDs use the prefixes:
    fn_    - single Problem
    suite_ - Suite
    gen_   - Generator
    impl_  - Implementation
"""

from opltools import (
    Library,
    Problem,
    Suite,
    Generator,
    Implementation,
    Reference,
    Link,
    Variable,
    Constraint,
    ValueRange,
)
from pydantic_yaml import to_yaml_str

things = {}


# =====================================================================
# Shared implementations (reused by multiple YAML entries).
# =====================================================================

things["impl_coco"] = Implementation(
    name="COCO framework",
    description="Comparing Continuous Optimizers: black-box optimization benchmarking platform",
    language="C/Python",
    links=[Link(type="repository", url="https://github.com/numbbo/coco")],
)

things["impl_coco_legacy"] = Implementation(
    name="COCO legacy (bbob-noisy)",
    description="Archived COCO download page that hosted the bbob-noisy suite",
    language="C/Python",
    links=[
        Link(
            type="archive",
            url="https://web.archive.org/web/20210416065610/https://coco.gforge.inria.fr/doku.php?id=downloads",
        )
    ],
)

things["impl_iohexperimenter"] = Implementation(
    name="IOHexperimenter",
    description="IOHprofiler experimenter framework",
    language="C++/Python",
    links=[Link(type="repository", url="https://github.com/IOHprofiler/IOHexperimenter")],
)

things["impl_pymoo"] = Implementation(
    name="pymoo",
    description="Multi-objective optimization in Python",
    language="Python",
    links=[Link(type="repository", url="https://github.com/anyoptimization/pymoo")],
)

things["impl_mocobench"] = Implementation(
    name="mocobench",
    description="Multi-objective combinatorial optimization benchmark",
    language="C++",
    links=[Link(type="repository", url="https://gitlab.com/aliefooghe/mocobench/")],
)

things["impl_reproblems"] = Implementation(
    name="reproblems",
    description="Real-world inspired multi-objective optimization problem suite",
    language="Python",
    links=[Link(type="repository", url="https://github.com/ryojitanabe/reproblems")],
)


# =====================================================================
# Shared references (reused by multiple YAML entries).
# =====================================================================

things["ref_coco_a_platform_for"] = Reference(
    title="COCO: a platform for comparing continuous optimizers in a black-box setting",
    link=Link(url="https://doi.org/10.1080/10556788.2020.1808977"),
)
things["ref_bbob_bi_objective_test_suite"] = Reference(
    title="BBOB bi-objective test suite",
    link=Link(url="https://doi.org/10.48550/arXiv.1604.00359"),
)
things["ref_real_parameter_black_box"] = Reference(
    title="Real-parameter black-box optimization benchmarking: noisy functions definitions",
    link=Link(url="https://hal.inria.fr/inria-00369466"),
)
things["ref_bbob_large_scale_test_suite"] = Reference(
    title="BBOB large-scale test suite",
    link=Link(url="https://doi.org/10.48550/arXiv.1903.06396"),
)
things["ref_bbob_mixed_integer_test_suite"] = Reference(
    title="BBOB bi-objective mixed-integer test suite",
    link=Link(url="https://doi.org/10.1145/3321707.3321868"),
)
things["ref_bbob_constrained_documentation"] = Reference(
    title="bbob-constrained documentation",
    link=Link(url="http://numbbo.github.io/coco-doc/bbob-constrained/"),
)
things["ref_comparison_of_multiobjective_evolutionary"] = Reference(
    title="Comparison of multiobjective evolutionary algorithms: empirical results",
    authors=["Eckart Zitzler", "Kalyanmoy Deb", "Lothar Thiele"],
    link=Link(url="https://doi.org/10.1162/106365600568202"),
)
things["ref_scalable_multi_objective_optimization"] = Reference(
    title="Scalable multi-objective optimization test problems",
    authors=["Kalyanmoy Deb", "Lothar Thiele", "Marco Laumanns", "Eckart Zitzler"],
    link=Link(url="https://doi.org/10.1109/CEC.2002.1007032"),
)
things["ref_a_review_of_multiobjective"] = Reference(
    title="A review of multiobjective test problems and a scalable test problem toolkit",
    authors=["Simon Huband", "Philip Hingston", "Luigi Barone", "Lyndon While"],
    link=Link(url="https://doi.org/10.1109/TEVC.2005.861417"),
)
things["ref_cdmp_benchmark"] = Reference(
    title="CDMP benchmark",
    link=Link(url="https://doi.org/10.1145/3321707.3321878"),
)
things["ref_sdp_dynamic_multi_objective_benchmark"] = Reference(
    title="SDP dynamic multi-objective benchmark",
    link=Link(url="https://doi.org/10.1109/TCYB.2019.2896021"),
)
things["ref_maop_benchmark"] = Reference(
    title="MaOP benchmark",
    link=Link(url="https://doi.org/10.1016/j.swevo.2019.02.003"),
)
things["ref_bp_benchmark"] = Reference(
    title="BP benchmark",
    link=Link(url="https://doi.org/10.1109/CEC.2019.8790277"),
)
things["ref_gpd_generator"] = Reference(
    title="GPD generator",
    link=Link(url="https://doi.org/10.1016/j.asoc.2020.106139"),
)
things["ref_evolutionary_many_task_optimization"] = Reference(
    title="Evolutionary many-task optimization framework",
    link=Link(url="https://doi.org/10.48550/arXiv.2110.08033"),
)
things["ref_mmopp_technical_report"] = Reference(
    title="MMOPP technical report",
    link=Link(url="http://www5.zzu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1327567121&wbfileid=4764412"),
)
things["ref_cfd_test_problem_suite"] = Reference(
    title="CFD test problem suite",
    link=Link(url="https://doi.org/10.1007/978-3-319-99259-4_24"),
)
things["ref_game_benchmark_for_evolutionary"] = Reference(
    title="Game benchmark for evolutionary algorithms",
    link=Link(url="https://doi.org/10.1145/3321707.3321805"),
)
things["ref_car_structure_design_benchmark"] = Reference(
    title="Car structure design benchmark",
    link=Link(url="https://doi.org/10.1145/3205651.3205702"),
)
things["ref_bbcomp_emo_2017"] = Reference(
    title="BBComp EMO 2017",
    link=Link(url="https://www.ini.rub.de/PEOPLE/glasmtbl/projects/bbcomp/"),
)
things["ref_jpnsec_ec_symposium_2019_competition"] = Reference(
    title="JPNSEC EC-Symposium 2019 competition",
    link=Link(url="http://www.jpnsec.org/files/competition2019/EC-Symposium-2019-Competition-English.html"),
)
things["ref_easy_to_evaluate_real"] = Reference(
    title="Easy-to-evaluate real-world multi-objective optimization problems",
    authors=["Ryoji Tanabe", "Hisao Ishibuchi"],
    link=Link(url="https://doi.org/10.1016/j.asoc.2020.106078"),
)
things["ref_radar_waveform_design"] = Reference(
    title="Radar waveform design",
    link=Link(url="https://doi.org/10.1007/978-3-540-70928-2_53"),
)
things["ref_mf2_a_collection_of"] = Reference(
    title="mf2: a collection of multi-fidelity benchmark functions in Python",
    link=Link(url="https://doi.org/10.21105/joss.02049"),
)
things["ref_amvop"] = Reference(
    title="RWMVOP",
    link=Link(url="https://doi.org/10.1109/TEVC.2013.2281531"),
)
things["ref_sbox_cost"] = Reference(
    title="SBOX-COST",
    link=Link(url="https://doi.org/10.48550/arXiv.2305.12221"),
)
things["ref_on_the_design_of"] = Reference(
    title="On the design of multi-objective evolutionary algorithms based on NK-landscapes",
    link=Link(url="https://doi.org/10.1016/j.ejor.2012.12.019"),
)
things["ref_mubqp_benchmark"] = Reference(
    title="mUBQP benchmark",
    link=Link(url="https://doi.org/10.1016/j.asoc.2013.11.008"),
)
things["ref_on_the_impact_of"] = Reference(
    title="On the impact of multi-objective scalability for the ρmTSP",
    link=Link(url="https://doi.org/10.1007/978-3-319-45823-6_40"),
)
things["ref_benchmark_functions_for_cec"] = Reference(
    title="Benchmark Functions for CEC 2015 Special Session and Competition on Dynamic Multi-objective Optimization",
)
things["ref_ealain"] = Reference(
    title="Ealain",
    link=Link(url="https://doi.org/10.1145/3638530.3654299"),
)
things["ref_ma_bbob"] = Reference(
    title="MA-BBOB",
    link=Link(url="https://doi.org/10.1145/3673908"),
)
things["ref_mpm2_technical_report_tr15_01"] = Reference(
    title="MPM2 technical report TR15-01",
    link=Link(url="https://ls11-www.cs.tu-dortmund.de/_media/techreports/tr15-01.pdf"),
)
things["ref_convex_dtlz2"] = Reference(
    title="Convex DTLZ2",
    link=Link(url="https://doi.org/10.1109/TEVC.2013.2281535"),
)
things["ref_inverted_dtlz1"] = Reference(
    title="Inverted DTLZ1",
    link=Link(url="https://doi.org/10.1109/TEVC.2013.2281534"),
)
things["ref_minus_dtlz_minus_wfg"] = Reference(
    title="Minus DTLZ / Minus WFG",
    link=Link(url="https://doi.org/10.1109/TEVC.2016.2587749"),
)
things["ref_linkage_zdt_dtlz_variants"] = Reference(
    title="Linkage ZDT/DTLZ variants",
    link=Link(url="https://doi.org/10.1145/1143997.1144179"),
)
things["ref_cec2018_dmop_competition_tr"] = Reference(
    title="CEC2018 DMOP Competition TR",
    link=Link(url="https://www.academia.edu/download/94499025/TR-CEC2018-DMOP-Competition.pdf"),
)
things["ref_modact"] = Reference(
    title="MODAct",
    link=Link(url="https://doi.org/10.1109/TEVC.2020.3020046"),
)
things["ref_iohclustering"] = Reference(
    title="IOHClustering",
    link=Link(url="https://arxiv.org/pdf/2505.09233"),
)
things["ref_gnbg_ii"] = Reference(
    title="GNBG-II",
    link=Link(url="https://dl.acm.org/doi/pdf/10.1145/3712255.3734271"),
)
things["ref_gnbg"] = Reference(
    title="GNBG",
    link=Link(url="https://arxiv.org/abs/2312.07083"),
)
things["ref_dynamicbinval"] = Reference(
    title="DynamicBinVal",
    link=Link(url="https://arxiv.org/pdf/2404.15837"),
)
things["ref_pbo_benchmarks"] = Reference(
    title="PBO benchmarks",
    link=Link(url="https://dl.acm.org/doi/pdf/10.1145/3319619.3326810"),
)
things["ref_w_model"] = Reference(
    title="W-model",
    link=Link(url="https://dl.acm.org/doi/abs/10.1145/3205651.3208240"),
)
things["ref_submodular_optimization_benchmark"] = Reference(
    title="Submodular optimization benchmark",
    link=Link(url="https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10254181"),
)
things["ref_cec2013_definitions"] = Reference(
    title="CEC2013 definitions",
    link=Link(url="https://peerj.com/articles/cs-2671/CEC2013.pdf"),
)
things["ref_cec2022_tr"] = Reference(
    title="CEC2022 TR",
    link=Link(url="https://github.com/P-N-Suganthan/2022-SO-BO/blob/main/CEC2022%20TR.pdf"),
)
things["ref_onemax_sphere_zeromax_sphere"] = Reference(
    title="Mixed-variable multi-objective test problems",
    link=Link(url="https://doi.org/10.1145/3449726.3459521"),
)
things["ref_porkchop_plot_interplanetary_trajectory"] = Reference(
    title="Porkchop plot interplanetary trajectory benchmark",
    link=Link(url="https://doi.org/10.1109/CEC65147.2025.11042973"),
)
things["ref_kinematics_of_a_robot_arm"] = Reference(
    title="Kinematics of a robot arm",
    link=Link(url="https://doi.org/10.1023/A:1013258808932"),
)
things["ref_vehicledynamics_benchmark"] = Reference(
    title="VehicleDynamics benchmark",
    link=Link(url="https://www.scitepress.org/Papers/2023/121580/121580.pdf"),
)
things["ref_mechbench"] = Reference(
    title="MECHBench",
    link=Link(url="https://arxiv.org/abs/2511.10821"),
)
things["ref_expobench"] = Reference(
    title="EXPObench",
    link=Link(url="https://doi.org/10.1016/j.asoc.2023.110744"),
)
things["ref_gasoline_direct_injection_engine_design"] = Reference(
    title="Gasoline direct injection engine design",
    link=Link(url="https://doi.org/10.1016/j.ejor.2022.08.032"),
)
things["ref_beacon"] = Reference(
    title="BEACON",
    link=Link(url="https://dl.acm.org/doi/10.1145/3712255.3734303"),
)
things["ref_tulipaenergymodel_jl_scientific_references"] = Reference(
    title="TulipaEnergyModel.jl scientific references",
    link=Link(url="https://tulipaenergy.github.io/TulipaEnergyModel.jl/stable/40-scientific-foundation/45-scientific-references"),
)
things["ref_brachytherapy_treatment_planning"] = Reference(
    title="Brachytherapy treatment planning",
    link=Link(url="https://www.sciencedirect.com/science/article/pii/S1538472123016781"),
)
things["ref_fleetopt"] = Reference(
    title="FleetOpt",
    link=Link(url="https://dl.acm.org/doi/abs/10.1145/3638530.3664137"),
)
things["ref_building_spatial_design"] = Reference(
    title="Building spatial design",
    link=Link(url="https://hdl.handle.net/1887/81789"),
)
things["ref_a_multi_step_evaluation"] = Reference(
    title="A Multi-Step Evaluation Process in Electric Motor Design",
    authors=["Tea Tušar", "Peter Korošec", "Bogdan Filipič"],
    link=Link(url="https://dis.ijs.si/tea/Publications/Tusar23Multistep.pdf"),
)
things["ref_cuter"] = Reference(
    title="CUTEr",
    link=Link(url="https://dl.acm.org/doi/10.1145/962437.962439"),
)
things["ref_cutest"] = Reference(
    title="CUTEst",
    link=Link(url="https://link.springer.com/article/10.1007/s10589-014-9687-3"),
)
things["ref_puboi"] = Reference(
    title="PUBOi",
    link=Link(url="https://link.springer.com/chapter/10.1007/978-3-031-04148-8_12"),
)

# =====================================================================
# Entries
# =====================================================================

#! - name: BBOB
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1080/10556788.2020.1808977
#!   implementation: https://github.com/numbbo/coco
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_bbob"] = Suite(
    name="BBOB",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    modality={"multimodal"},
    references={"ref_coco_a_platform_for"},
    implementations={"impl_coco"},
)

#! - name: BBOB-biobj
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: 2-40
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.48550/arXiv.1604.00359
#!   implementation: https://github.com/numbbo/coco
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_bbob_biobj"] = Suite(
    name="BBOB-biobj",
    objectives={2},
    variables=[Variable(type="continuous", dim=ValueRange(min=2, max=40))],
    modality={"multimodal"},
    references={"ref_bbob_bi_objective_test_suite"},
    implementations={"impl_coco"},
)

#! - name: BBOB-noisy
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'yes'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://hal.inria.fr/inria-00369466
#!   implementation: https://web.archive.org/web/20210416065610/https://coco.gforge.inria.fr/doku.php?id=downloads
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_bbob_noisy"] = Suite(
    name="BBOB-noisy",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    modality={"multimodal"},
    noise_type={"noisy"},
    references={"ref_real_parameter_black_box"},
    implementations={"impl_coco_legacy"},
)

#! - name: BBOB-largescale
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: 20-640
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.48550/arXiv.1903.06396
#!   implementation: https://github.com/numbbo/coco
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_bbob_largescale"] = Suite(
    name="BBOB-largescale",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=20, max=640))],
    modality={"multimodal"},
    references={"ref_bbob_large_scale_test_suite"},
    implementations={"impl_coco"},
)

#! - name: BBOB-mixint
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: 5-160
#!   variable type: integer;continuous;mixed
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3321707.3321868
#!   implementation: https://github.com/numbbo/coco
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_bbob_mixint"] = Suite(
    name="BBOB-mixint",
    objectives={1},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=5, max=160)),
        Variable(type="integer", dim=ValueRange(min=5, max=160)),
    ],
    modality={"multimodal"},
    references={"ref_bbob_mixed_integer_test_suite"},
    implementations={"impl_coco"},
)

#! - name: BBOB-biobj-mixint
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: 5-160
#!   variable type: integer;continuous;mixed
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3321707.3321868
#!   implementation: https://github.com/numbbo/coco
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_bbob_biobj_mixint"] = Suite(
    name="BBOB-biobj-mixint",
    objectives={2},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=5, max=160)),
        Variable(type="integer", dim=ValueRange(min=5, max=160)),
    ],
    modality={"multimodal"},
    references={"ref_bbob_mixed_integer_test_suite"},
    implementations={"impl_coco"},
)

#! - name: BBOB-constrained
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: 2-40
#!   variable type: continuous
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: http://numbbo.github.io/coco-doc/bbob-constrained/
#!   implementation: https://github.com/numbbo/coco
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_bbob_constrained"] = Suite(
    name="BBOB-constrained",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=2, max=40))],
    constraints=[Constraint(hard="yes")],
    modality={"multimodal"},
    references={"ref_bbob_constrained_documentation"},
    implementations={"impl_coco"},
)

#! - name: MOrepo
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: '?'
#!   variable type: combinatorial
#!   constraints: '?'
#!   dynamic: '?'
#!   noise: '?'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: ''
#!   implementation: https://github.com/MCDMSociety/MOrepo
#!   source (real-world/artificial): ''
#!   textual description: ''
things["impl_morepo"] = Implementation(
    name="MOrepo",
    description="Multi-objective optimisation problem repository",
    links=[Link(type="repository", url="https://github.com/MCDMSociety/MOrepo")],
)
# FIXME: "combinatorial" has no direct VariableType; dimensionality "?" unknown.
things["suite_morepo"] = Suite(
    name="MOrepo",
    objectives={2},
    variables=[Variable(type="unknown")],
    constraints=[Constraint(hard="?")],
    dynamic_type={"unknown"},
    noise_type={"unknown"},
    implementations={"impl_morepo"},
)

#! - name: ZDT
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: scalable
#!   variable type: continuous;binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1162/106365600568202
#!   implementation: https://github.com/anyoptimization/pymoo
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_zdt"] = Suite(
    name="ZDT",
    objectives={2},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    references={"ref_comparison_of_multiobjective_evolutionary"},
    implementations={"impl_pymoo"},
)

#! - name: DTLZ
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/CEC.2002.1007032
#!   implementation: https://pymoo.org/problems/many/dtlz.html
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_dtlz"] = Suite(
    name="DTLZ",
    # FIXME: original "2+" - schema requires set[int]; truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_scalable_multi_objective_optimization"},
    implementations={"impl_pymoo"},
)

#! - name: WFG
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2005.861417
#!   implementation: https://pymoo.org/problems/many/wfg.html
#!   source (real-world/artificial): ''
#!   textual description: ''
things["suite_wfg"] = Suite(
    name="WFG",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_a_review_of_multiobjective"},
    implementations={"impl_pymoo"},
)

#! - name: CDMP
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'yes'
#!   dynamic: '?'
#!   noise: '?'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3321707.3321878
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: ''
# FIXME: implementation unknown.
things["suite_cdmp"] = Suite(
    name="CDMP",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    constraints=[Constraint(hard="yes")],
    dynamic_type={"unknown"},
    noise_type={"unknown"},
    references={"ref_cdmp_benchmark"},
)

#! - name: SDP
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'yes'
#!   noise: '?'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TCYB.2019.2896021
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: ''
# FIXME: implementation unknown.
things["suite_sdp"] = Suite(
    name="SDP",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    dynamic_type={"dynamic"},
    noise_type={"unknown"},
    references={"ref_sdp_dynamic_multi_objective_benchmark"},
)

#! - name: MaOP
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: '?'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1016/j.swevo.2019.02.003
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: ''
# FIXME: implementation unknown.
things["suite_maop"] = Suite(
    name="MaOP",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    noise_type={"unknown"},
    references={"ref_maop_benchmark"},
)

#! - name: BP
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: '?'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/CEC.2019.8790277
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: ''
# FIXME: implementation unknown.
things["suite_bp"] = Suite(
    name="BP",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    noise_type={"unknown"},
    references={"ref_bp_benchmark"},
)

#! - name: GPD
#!   suite/generator/single: generator
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: optional
#!   dynamic: 'no'
#!   noise: optional
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1016/j.asoc.2020.106139
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: ''
# FIXME: implementation unknown.
things["gen_gpd"] = Generator(
    name="GPD",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    constraints=[Constraint(hard="some")],
    noise_type={"optional"},
    references={"ref_gpd_generator"},
)

#! - name: ETMOF
#!   suite/generator/single: suite
#!   objectives: 2-50
#!   dimensionality: 25-10000
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'yes'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.48550/arXiv.2110.08033
#!   implementation: https://github.com/songbai-liu/etmo
#!   source (real-world/artificial): ''
#!   textual description: ''
things["impl_etmof"] = Implementation(
    name="ETMOF",
    description="Evolutionary many-task optimization framework",
    links=[Link(type="repository", url="https://github.com/songbai-liu/etmo")],
)
things["suite_etmof"] = Suite(
    name="ETMOF",
    objectives=set(range(2, 51)),
    variables=[Variable(type="continuous", dim=ValueRange(min=25, max=10000))],
    dynamic_type={"dynamic"},
    references={"ref_evolutionary_many_task_optimization"},
    implementations={"impl_etmof"},
)

#! - name: MMOPP
#!   suite/generator/single: suite
#!   objectives: 2-7
#!   dimensionality: '?'
#!   variable type: '?'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: http://www5.zzu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1327567121&wbfileid=4764412
#!   implementation: http://www5.zzu.edu.cn/ecilab/info/1036/1251.htm
#!   source (real-world/artificial): ''
#!   textual description: ''
things["impl_mmopp"] = Implementation(
    name="MMOPP",
    description="ECI lab distribution page for MMOPP",
    links=[Link(type="website", url="http://www5.zzu.edu.cn/ecilab/info/1036/1251.htm")],
)
# FIXME: variable type and dimensionality unknown ("?").
things["suite_mmopp"] = Suite(
    name="MMOPP",
    objectives=set(range(2, 8)),
    variables=[Variable(type="unknown")],
    constraints=[Constraint(hard="yes")],
    modality={"multimodal"},
    references={"ref_mmopp_technical_report"},
    implementations={"impl_mmopp"},
)

#! - name: CFD
#!   suite/generator/single: suite
#!   objectives: 1-2
#!   dimensionality: scalable
#!   variable type: '?'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1007/978-3-319-99259-4_24
#!   implementation: https://bitbucket.org/arahat/cfd-test-problem-suite
#!   source (real-world/artificial): real world
#!   textual description: expensive evaluations 30s-15m
things["impl_cfd"] = Implementation(
    name="CFD test problem suite",
    description="Expensive real-world CFD-based test problems",
    evaluation_time=["30s", "15m"],
    links=[Link(type="repository", url="https://bitbucket.org/arahat/cfd-test-problem-suite")],
)
# FIXME: variable type unknown.
things["suite_cfd"] = Suite(
    name="CFD",
    description="expensive evaluations 30s-15m",
    objectives={1, 2},
    variables=[Variable(type="unknown", dim=ValueRange(min=1))],
    constraints=[Constraint(hard="yes")],
    source={"real-world"},
    references={"ref_cfd_test_problem_suite"},
    implementations={"impl_cfd"},
)

#! - name: GBEA
#!   suite/generator/single: suite
#!   objectives: 1-2
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'yes'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3321707.3321805
#!   implementation: 'https://github.com/ttusar/coco-gbea'
#!   source (real-world/artificial): real world
#!   textual description: 'expensive evaluations 5s-35s, RW-GAN-Mario and TopTrumps are part of GBEA'
things["impl_gbea"] = Implementation(
    name="coco-gbea",
    description="Game-Benchmark for Evolutionary Algorithms (COCO fork)",
    evaluation_time=["5 seconds", "34 seconds"],
    links=[Link(type="repository", url="https://github.com/ttusar/coco-gbea")],
)
things["suite_gbea"] = Suite(
    name="GBEA",
    description="expensive evaluations 5s-35s, RW-GAN-Mario and TopTrumps are part of GBEA",
    objectives={1, 2},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    noise_type={"noisy"},
    modality={"multimodal"},
    source={"real-world"},
    references={"ref_game_benchmark_for_evolutionary"},
    implementations={"impl_gbea"},
)

#! - name: Car structure
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: 144-222
#!   variable type: discrete
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3205651.3205702
#!   implementation: http://ladse.eng.isas.jaxa.jp/benchmark/
#!   source (real-world/artificial): real world
#!   textual description: 54 constraints
things["impl_car_structure"] = Implementation(
    name="Car-structure benchmark",
    description="JAXA LADSE benchmark problems",
    links=[Link(type="website", url="http://ladse.eng.isas.jaxa.jp/benchmark/")],
)
# FIXME: "discrete" has no direct VariableType - using integer.
things["suite_car_structure"] = Suite(
    name="Car structure",
    description="54 constraints",
    objectives={2},
    variables=[Variable(type="integer", dim=ValueRange(min=144, max=222))],
    constraints=[Constraint(hard="yes", number=54)],
    source={"real-world"},
    references={"ref_car_structure_design_benchmark"},
    implementations={"impl_car_structure"},
)

#! - name: EMO2017
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: 4-24
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://www.ini.rub.de/PEOPLE/glasmtbl/projects/bbcomp/
#!   implementation: https://www.ini.rub.de/PEOPLE/glasmtbl/projects/bbcomp/downloads/realworld-problems-bbcomp-EMO-2017.zip
#!   source (real-world/artificial): real world
#!   textual description: ''
things["impl_emo2017"] = Implementation(
    name="EMO 2017 real-world problems",
    description="BBComp EMO-2017 real-world problem archive",
    links=[
        Link(
            type="download",
            url="https://www.ini.rub.de/PEOPLE/glasmtbl/projects/bbcomp/downloads/realworld-problems-bbcomp-EMO-2017.zip",
        )
    ],
)
things["suite_emo2017"] = Suite(
    name="EMO2017",
    objectives={2},
    variables=[Variable(type="continuous", dim=ValueRange(min=4, max=24))],
    source={"real-world"},
    references={"ref_bbcomp_emo_2017"},
    implementations={"impl_emo2017"},
)

#! - name: JSEC2019
#!   suite/generator/single: single
#!   objectives: 1-5
#!   dimensionality: '32'
#!   variable type: continuous
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: http://www.jpnsec.org/files/competition2019/EC-Symposium-2019-Competition-English.html
#!   implementation: http://www.jpnsec.org/files/competition2019/EC-Symposium-2019-Competition-English.html
#!   source (real-world/artificial): real world
#!   textual description: expensive evaluations 3s; 22 constraints
things["impl_jsec2019"] = Implementation(
    name="JSEC 2019 competition",
    description="JPNSEC EC-Symposium 2019 competition problem",
    evaluation_time=["3s"],
    links=[
        Link(
            type="website",
            url="http://www.jpnsec.org/files/competition2019/EC-Symposium-2019-Competition-English.html",
        )
    ],
)
things["fn_jsec2019"] = Problem(
    name="JSEC2019",
    description="expensive evaluations 3s; 22 constraints",
    objectives={1, 2, 3, 4, 5},
    variables=[Variable(type="continuous", dim=32)],
    constraints=[Constraint(hard="yes", number=22)],
    source={"real-world"},
    references={"ref_jpnsec_ec_symposium_2019_competition"},
    implementations={"impl_jsec2019"},
)

#! - name: RE
#!   suite/generator/single: suite
#!   objectives: 2-9
#!   dimensionality: 2-7
#!   variable type: continuous;integer;mixed
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1016/j.asoc.2020.106078
#!   implementation: https://github.com/ryojitanabe/reproblems
#!   source (real-world/artificial): real world like
#!   textual description: ''
things["suite_re"] = Suite(
    name="RE",
    objectives=set(range(2, 10)),
    variables=[
        Variable(type="continuous", dim=ValueRange(min=2, max=7)),
        Variable(type="integer", dim=ValueRange(min=2, max=7)),
    ],
    source={"real-world-like"},
    references={"ref_easy_to_evaluate_real"},
    implementations={"impl_reproblems"},
)

#! - name: CRE
#!   suite/generator/single: suite
#!   objectives: 2-5
#!   dimensionality: 3-7
#!   variable type: continuous;integer;mixed
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1016/j.asoc.2020.106078
#!   implementation: https://github.com/ryojitanabe/reproblems
#!   source (real-world/artificial): real world like
#!   textual description: ''
things["suite_cre"] = Suite(
    name="CRE",
    objectives={2, 3, 4, 5},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=3, max=7)),
        Variable(type="integer", dim=ValueRange(min=3, max=7)),
    ],
    constraints=[Constraint(hard="yes")],
    source={"real-world-like"},
    references={"ref_easy_to_evaluate_real"},
    implementations={"impl_reproblems"},
)

#! - name: Radar waveform
#!   suite/generator/single: single
#!   objectives: '9'
#!   dimensionality: 4-12
#!   variable type: integer
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1007/978-3-540-70928-2_53
#!   implementation: http://code.evanhughes.org/
#!   source (real-world/artificial): real world
#!   textual description: ''
things["impl_radar_waveform"] = Implementation(
    name="Evan Hughes radar waveform code",
    description="Radar waveform design reference implementation",
    links=[Link(type="website", url="http://code.evanhughes.org/")],
)
things["fn_radar_waveform"] = Problem(
    name="Radar waveform",
    objectives={9},
    variables=[Variable(type="integer", dim=ValueRange(min=4, max=12))],
    constraints=[Constraint(hard="yes")],
    source={"real-world"},
    references={"ref_radar_waveform_design"},
    implementations={"impl_radar_waveform"},
)

#! - name: MF2
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: 1-n
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'yes'
#!   reference: https://doi.org/10.21105/joss.02049
#!   implementation: https://github.com/sjvrijn/mf2
#!   source (real-world/artificial): ''
#!   textual description: ''
things["impl_mf2"] = Implementation(
    name="mf2",
    description="Multi-fidelity test function collection",
    language="Python",
    links=[Link(type="repository", url="https://github.com/sjvrijn/mf2")],
)
things["suite_mf2"] = Suite(
    name="MF2",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    fidelity_levels={1, 2},
    references={"ref_mf2_a_collection_of"},
    implementations={"impl_mf2"},
)

#! - name: AMVOP
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: mixed continuous+ordinal+categorical+both
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2013.2281531
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: ''
# FIXME: implementation unknown. "ordinal" not representable, using integer+categorical+continuous.
things["suite_amvop"] = Suite(
    name="AMVOP",
    objectives={1},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="integer", dim=ValueRange(min=1)),
        Variable(type="categorical", dim=ValueRange(min=1)),
    ],
    modality={"multimodal"},
    references={"ref_amvop"},
)

#! - name: RWMVOP
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous;mixed continuous+ordinal+categorical+both
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2013.2281531
#!   implementation: '?'
#!   source (real-world/artificial): real world
#!   textual description: ''
# FIXME: implementation unknown.
things["suite_rwmvop"] = Suite(
    name="RWMVOP",
    objectives={1},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="integer", dim=ValueRange(min=1)),
        Variable(type="categorical", dim=ValueRange(min=1)),
    ],
    constraints=[Constraint(hard="yes")],
    source={"real-world"},
    references={"ref_amvop"},
)

#! - name: SBOX-COST
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.48550/arXiv.2305.12221
#!   implementation: https://github.com/IOHprofiler/IOHexperimenter/
#!   source (real-world/artificial): ''
#!   textual description: problems from BBOB but allows instances with the optimum close to the
#!     boundary
things["suite_sbox_cost"] = Suite(
    name="SBOX-COST",
    description="problems from BBOB but allows instances with the optimum close to the boundary",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    modality={"multimodal"},
    references={"ref_sbox_cost"},
    implementations={"impl_iohexperimenter"},
)

#! - name: "\u03C1MNK-Landscapes"
#!   suite/generator/single: generator
#!   objectives: scalable
#!   dimensionality: scalable
#!   variable type: binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1016/j.ejor.2012.12.019
#!   implementation: https://gitlab.com/aliefooghe/mocobench/
#!   source (real-world/artificial): ''
#!   textual description: tunable variable and objective dimensions; tunable multimodality and
#!     correlation between objectives
things["gen_rho_mnk_landscapes"] = Generator(
    name="ρMNK-Landscapes",
    description="tunable variable and objective dimensions; tunable multimodality and correlation between objectives",
    # FIXME: original "scalable" - truncated to 1..10.
    objectives=set(range(1, 11)),
    variables=[Variable(type="binary", dim=ValueRange(min=1))],
    modality={"multimodal"},
    references={"ref_on_the_design_of"},
    implementations={"impl_mocobench"},
)

#! - name: mUBQP
#!   suite/generator/single: generator
#!   objectives: scalable
#!   dimensionality: scalable
#!   variable type: binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: yes (quadratic)
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1016/j.asoc.2013.11.008
#!   implementation: https://gitlab.com/aliefooghe/mocobench/
#!   source (real-world/artificial): ''
#!   textual description: tunable variable and objective dimensions; tunable density and correlation
#!     between objectives
things["gen_mubqp"] = Generator(
    name="mUBQP",
    description="tunable variable and objective dimensions; tunable density and correlation between objectives",
    # FIXME: original "scalable" - truncated to 1..10.
    objectives=set(range(1, 11)),
    variables=[Variable(type="binary", dim=ValueRange(min=1))],
    modality={"multimodal", "quadratic"},
    references={"ref_mubqp_benchmark"},
    implementations={"impl_mocobench"},
)

#! - name: "\u03C1mTSP"
#!   suite/generator/single: generator
#!   objectives: scalable
#!   dimensionality: scalable
#!   variable type: permutations
#!   constraints: no (apart from being permutations)
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: yes (quadratic)
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1007/978-3-319-45823-6_40
#!   implementation: https://gitlab.com/aliefooghe/mocobench/
#!   source (real-world/artificial): ''
#!   textual description: tunable variable and objective dimensions; tunable instance type (euclidian/random);
#!     tunable correlation between objectives
# FIXME: "permutations" has no direct VariableType; constraints are implicit permutations.
things["gen_rho_mtsp"] = Generator(
    name="ρmTSP",
    description="tunable variable and objective dimensions; tunable instance type (euclidean/random); tunable correlation between objectives",
    # FIXME: original "scalable" - truncated to 1..10.
    objectives=set(range(1, 11)),
    variables=[Variable(type="unknown", dim=ValueRange(min=1))],
    modality={"multimodal", "quadratic"},
    references={"ref_on_the_impact_of"},
    implementations={"impl_mocobench"},
)

#! - name: CEC2015-DMOO
#!   suite/generator/single: suite
#!   objectives: 2-3
#!   dimensionality: '?'
#!   variable type: continuous
#!   constraints: '?'
#!   dynamic: 'yes'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: Benchmark Functions for CEC 2015 Special Session and Competition on Dynamic
#!     Multi-objective Optimization
#!   implementation: ''
#!   source (real-world/artificial): ''
#!   textual description: ''
# FIXME: reference is a title-only string; implementation unavailable; dimensionality unknown.
things["suite_cec2015_dmoo"] = Suite(
    name="CEC2015-DMOO",
    objectives={2, 3},
    variables=[Variable(type="continuous")],
    constraints=[Constraint(hard="?")],
    dynamic_type={"dynamic"},
    references={"ref_benchmark_functions_for_cec"},
)

#! - name: Ealain
#!   suite/generator/single: generator
#!   objectives: 1+
#!   dimensionality: scalable
#!   variable type: continuous,binary,integer
#!   constraints: optional
#!   dynamic: optional
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: optional
#!   reference: https://doi.org/10.1145/3638530.3654299
#!   implementation: https://github.com/qrenau/Ealain
#!   source (real-world/artificial): Real-world-like
#!   textual description: Real-world-like, easily extensible to increase complexity
things["impl_ealain"] = Implementation(
    name="Ealain",
    description="Real-world-like extensible benchmark problem generator",
    links=[Link(type="repository", url="https://github.com/qrenau/Ealain")],
)
things["gen_ealain"] = Generator(
    name="Ealain",
    description="Real-world-like, easily extensible to increase complexity",
    # FIXME: original "1+" - truncated to 1..10.
    objectives=set(range(1, 11)),
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
        Variable(type="integer", dim=ValueRange(min=1)),
    ],
    constraints=[Constraint(hard="some")],
    dynamic_type={"optional"},
    fidelity_levels={1, 2},
    source={"real-world-like"},
    references={"ref_ealain"},
    implementations={"impl_ealain"},
)

#! - name: MA-BBOB
#!   suite/generator/single: generator
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3673908
#!   implementation: https://github.com/IOHprofiler/IOHexperimenter/blob/master/example/Competitions/MA-BBOB/Example_MABBOB.ipynb
#!   source (real-world/artificial): artificial
#!   textual description: Generator that creates affine combinations of BBOB functions
things["impl_ma_bbob"] = Implementation(
    name="MA-BBOB (IOHexperimenter)",
    description="Example notebook for MA-BBOB in IOHexperimenter",
    links=[
        Link(
            type="example",
            url="https://github.com/IOHprofiler/IOHexperimenter/blob/master/example/Competitions/MA-BBOB/Example_MABBOB.ipynb",
        )
    ],
)
things["gen_ma_bbob"] = Generator(
    name="MA-BBOB",
    description="Generator that creates affine combinations of BBOB functions",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    modality={"multimodal"},
    source={"artificial"},
    references={"ref_ma_bbob"},
    implementations={"impl_ma_bbob", "impl_iohexperimenter"},
)

#! - name: MPM2
#!   suite/generator/single: generator
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://ls11-www.cs.tu-dortmund.de/_media/techreports/tr15-01.pdf
#!   implementation: https://github.com/jakobbossek/smoof/blob/master/inst/mpm2.py
#!   source (real-world/artificial): ''
#!   textual description: nonlinear nonseparable nonsymmetric; scalable in terms of time to evaluate
#!     the objective function
things["impl_mpm2"] = Implementation(
    name="MPM2 (smoof)",
    description="Python implementation of MPM2 distributed with smoof",
    language="Python",
    links=[
        Link(
            type="source",
            url="https://github.com/jakobbossek/smoof/blob/master/inst/mpm2.py",
        )
    ],
)
things["gen_mpm2"] = Generator(
    name="MPM2",
    description="nonlinear nonseparable nonsymmetric; scalable in terms of time to evaluate the objective function",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    modality={"multimodal"},
    references={"ref_mpm2_technical_report_tr15_01"},
    implementations={"impl_mpm2"},
)

#! - name: Convex DTLZ2
#!   suite/generator/single: single
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2013.2281535
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of DTLZ2 with a convex Pareto front (instead of concave)
# FIXME: implementation unknown.
things["fn_convex_dtlz2"] = Problem(
    name="Convex DTLZ2",
    description="Variant of DTLZ2 with a convex Pareto front (instead of concave)",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_convex_dtlz2"},
)

#! - name: Inverted DTLZ1
#!   suite/generator/single: single
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2013.2281534
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of DTLZ1 with an inverted Pareto front
# FIXME: implementation unknown.
things["fn_inverted_dtlz1"] = Problem(
    name="Inverted DTLZ1",
    description="Variant of DTLZ1 with an inverted Pareto front",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_inverted_dtlz1"},
)

#! - name: Minus DTLZ
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2016.2587749
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of DTLZ that minimises the inverse of the base DTLZ functions
# FIXME: implementation unknown.
things["suite_minus_dtlz"] = Suite(
    name="Minus DTLZ",
    description="Variant of DTLZ that minimises the inverse of the base DTLZ functions",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_minus_dtlz_minus_wfg"},
)

#! - name: Minus WFG
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2016.2587749
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of WFG that minimises the inverse of the base WFG functions
# FIXME: implementation unknown.
things["suite_minus_wfg"] = Suite(
    name="Minus WFG",
    description="Variant of WFG that minimises the inverse of the base WFG functions",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_minus_dtlz_minus_wfg"},
)

#! - name: L1-ZDT
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: scalable
#!   variable type: continuous;binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/1143997.1144179
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of ZDT with linkages between variables within one of two groups
#!     but not between variables in a different group; Linear recombination operators
#!     can potentially take advantage of the problem structure
# FIXME: implementation unknown.
things["suite_l1_zdt"] = Suite(
    name="L1-ZDT",
    description="Variant of ZDT with linkages between variables within groups",
    objectives={2},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    references={"ref_linkage_zdt_dtlz_variants"},
)

#! - name: L2-ZDT
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: scalable
#!   variable type: continuous;binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/1143997.1144179
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of ZDT with linkages between all variables; Linear recombination
#!     operators can potentially take advantage of the problem structure
# FIXME: implementation unknown.
things["suite_l2_zdt"] = Suite(
    name="L2-ZDT",
    description="Variant of ZDT with linkages between all variables",
    objectives={2},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    references={"ref_linkage_zdt_dtlz_variants"},
)

#! - name: L3-ZDT
#!   suite/generator/single: suite
#!   objectives: '2'
#!   dimensionality: scalable
#!   variable type: continuous;binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/1143997.1144179
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of L2-ZDT using a mapping to prevent linear recombination operators
#!     from potentially taking advantage of the problem structure
# FIXME: implementation unknown.
things["suite_l3_zdt"] = Suite(
    name="L3-ZDT",
    description="Variant of L2-ZDT with anti-linkage mapping",
    objectives={2},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    references={"ref_linkage_zdt_dtlz_variants"},
)

#! - name: L2-DTLZ
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/1143997.1144179
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of DTLZ2 and DTLZ3 with linkages between all variables; Linear
#!     recombination operators can potentially take advantage of the problem structure
# FIXME: implementation unknown.
things["suite_l2_dtlz"] = Suite(
    name="L2-DTLZ",
    description="Variant of DTLZ2/DTLZ3 with linkages between all variables",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_linkage_zdt_dtlz_variants"},
)

#! - name: L3-DTLZ
#!   suite/generator/single: suite
#!   objectives: 2+
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/1143997.1144179
#!   implementation: '?'
#!   source (real-world/artificial): ''
#!   textual description: Variant of L2-DTLZ using a mapping to prevent linear recombination operators
#!     from potentially taking advantage of the problem structure
# FIXME: implementation unknown.
things["suite_l3_dtlz"] = Suite(
    name="L3-DTLZ",
    description="Variant of L2-DTLZ with anti-linkage mapping",
    # FIXME: original "2+" - truncated to 2..10.
    objectives=set(range(2, 11)),
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    references={"ref_linkage_zdt_dtlz_variants"},
)

#! - name: CEC2018 DT - CEC2018 Competition on Dynamic Multiobjective Optimisation
#!   suite/generator/single: suite
#!   objectives: 2 or 3
#!   dimensionality: scalable?
#!   variable type: '?'
#!   constraints: 'no'
#!   dynamic: 'yes'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://www.academia.edu/download/94499025/TR-CEC2018-DMOP-Competition.pdf
#!   implementation: https://pymoo.org/problems/dynamic/df.html
#!   source (real-world/artificial): artificial
#!   textual description: '14 problems. Time-dependent: Pareto front/Pareto set geometry;
#!     irregular Pareto front shapes; variable-linkage; number of disconnected Pareto
#!     front segments; etc.'
# FIXME: variable type unknown.
things["suite_cec2018_dt"] = Suite(
    name="CEC2018 DT",
    long_name="CEC2018 Competition on Dynamic Multiobjective Optimisation",
    description="14 problems. Time-dependent: Pareto front/Pareto set geometry; irregular Pareto front shapes; variable-linkage; number of disconnected Pareto front segments; etc.",
    objectives={2, 3},
    variables=[Variable(type="unknown", dim=ValueRange(min=1))],
    dynamic_type={"dynamic"},
    source={"artificial"},
    references={"ref_cec2018_dmop_competition_tr"},
    implementations={"impl_pymoo"},
)

#! - name: MODAct - multiobjective design of actuators
#!   suite/generator/single: suite
#!   objectives: 2 3 4 or 5
#!   dimensionality: '20'
#!   variable type: mixed; integer and continuous
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/TEVC.2020.3020046
#!   implementation: https://pymoo.org/problems/constrained/modact.html
#!   source (real-world/artificial): real-world
#!   textual description: Realistic Constrained Multi-Objective Optimization Benchmark
#!     Problems from Design. Need the https://github.com/epfl-lamd/modact package installed; evaluation
#!     times around 20ms
things["impl_modact"] = Implementation(
    name="modact",
    description="EPFL-LAMD modact package",
    evaluation_time=["20ms"],
    links=[Link(type="repository", url="https://github.com/epfl-lamd/modact")],
)
things["suite_modact"] = Suite(
    name="MODAct",
    long_name="multiobjective design of actuators",
    description="Realistic Constrained Multi-Objective Optimization Benchmark Problems from Design.",
    objectives={2, 3, 4, 5},
    variables=[
        Variable(type="continuous", dim=20),
        Variable(type="integer", dim=20),
    ],
    constraints=[Constraint(hard="yes")],
    source={"real-world"},
    references={"ref_modact"},
    implementations={"impl_modact", "impl_pymoo"},
)

#! - name: IOHClustering
#!   suite/generator/single: suite; generator
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no '
#!   reference: https://arxiv.org/pdf/2505.09233
#!   implementation: https://github.com/IOHprofiler/IOHClustering
#!   source (real-world/artificial): artificial, but based on real data
#!   textual description: 'Set of benchmark problems from clustering: optimization task
#!     is selecting cluster centers for a given set of data, with the number of clusters
#!     defining problem dimensionality. Includes both a suite and a generator. Based on ML clustering datasets'
things["impl_iohclustering"] = Implementation(
    name="IOHClustering",
    description="Clustering-based optimization benchmark built on ML datasets",
    links=[Link(type="repository", url="https://github.com/IOHprofiler/IOHClustering")],
)
things["suite_iohclustering"] = Suite(
    name="IOHClustering",
    description="Set of benchmark problems from clustering: optimization task is selecting cluster centers for a given set of data.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    modality={"multimodal"},
    source={"artificial-from-real-data"},
    references={"ref_iohclustering"},
    implementations={"impl_iohclustering"},
)
things["gen_iohclustering"] = Generator(
    name="IOHClustering",
    description="Generator counterpart of the IOHClustering suite.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    modality={"multimodal"},
    source={"artificial-from-real-data"},
    references={"ref_iohclustering"},
    implementations={"impl_iohclustering"},
)

#! - name: GNBG-II
#!   suite/generator/single: suite; generator
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://dl.acm.org/doi/pdf/10.1145/3712255.3734271
#!   implementation: https://github.com/rohitsalgotra/GNBG-II
#!   source (real-world/artificial): artificial
#!   textual description: Generalized Numerical Benchmark Generator (version 2). Also in IOH https://github.com/IOHprofiler/IOHGNBG
things["impl_gnbg_ii"] = Implementation(
    name="GNBG-II",
    description="Generalized Numerical Benchmark Generator version 2",
    links=[Link(type="repository", url="https://github.com/rohitsalgotra/GNBG-II")],
)
things["impl_iohgnbg"] = Implementation(
    name="IOHGNBG",
    description="IOHprofiler version of GNBG",
    links=[Link(type="repository", url="https://github.com/IOHprofiler/IOHGNBG")],
)
things["suite_gnbg_ii"] = Suite(
    name="GNBG-II",
    description="Generalized Numerical Benchmark Generator (version 2). Also available in IOH.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_gnbg_ii"},
    implementations={"impl_gnbg_ii", "impl_iohgnbg"},
)
things["gen_gnbg_ii"] = Generator(
    name="GNBG-II",
    description="Generator counterpart of GNBG-II.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_gnbg_ii"},
    implementations={"impl_gnbg_ii", "impl_iohgnbg"},
)

#! - name: GNBG
#!   suite/generator/single: suite; generator
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://arxiv.org/abs/2312.07083
#!   implementation: https://github.com/Danial-Yazdani/GNBG-Generator
#!   source (real-world/artificial): artificial
#!   textual description: Generalized Numerical Benchmark Generator
things["impl_gnbg"] = Implementation(
    name="GNBG Generator",
    description="Generalized Numerical Benchmark Generator",
    links=[Link(type="repository", url="https://github.com/Danial-Yazdani/GNBG-Generator")],
)
things["suite_gnbg"] = Suite(
    name="GNBG",
    description="Generalized Numerical Benchmark Generator",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_gnbg"},
    implementations={"impl_gnbg"},
)
things["gen_gnbg"] = Generator(
    name="GNBG",
    description="Generator counterpart of GNBG.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_gnbg"},
    implementations={"impl_gnbg"},
)

#! - name: DynamicBinVal
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: binary
#!   constraints: 'no'
#!   dynamic: 'yes'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://arxiv.org/pdf/2404.15837
#!   implementation: https://github.com/IOHprofiler/IOHexperimenter
#!   source (real-world/artificial): artificial
#!   textual description: Four versions of the dynamic binary value problem
things["suite_dynamicbinval"] = Suite(
    name="DynamicBinVal",
    description="Four versions of the dynamic binary value problem",
    objectives={1},
    variables=[Variable(type="binary", dim=ValueRange(min=1))],
    dynamic_type={"dynamic"},
    source={"artificial"},
    references={"ref_dynamicbinval"},
    implementations={"impl_iohexperimenter"},
)

#! - name: PBO
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://dl.acm.org/doi/pdf/10.1145/3319619.3326810
#!   implementation: https://github.com/IOHprofiler/IOHexperimenter
#!   source (real-world/artificial): artificial
#!   textual description: Suite of 25 binary optimization problems
things["suite_pbo"] = Suite(
    name="PBO",
    description="Suite of 25 binary optimization problems",
    objectives={1},
    variables=[Variable(type="binary", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_pbo_benchmarks"},
    implementations={"impl_iohexperimenter"},
)

#! - name: W-model
#!   suite/generator/single: generator
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://dl.acm.org/doi/abs/10.1145/3205651.3208240?casa_token=S4U_Pi9f6MwAAAAA:U9ztNTPwmupT8K3GamWZfBL7-8fqjxPtr_kprv51vdwA-REsp0EyOFGa99BtbANb0XbqyrVg795hIw
#!   implementation: https://github.com/thomasWeise/BBDOB_W_Model
#!   source (real-world/artificial): artificial
#!   textual description: Tunable generator for binary optimization based on several
#!     difficulty features
things["impl_wmodel"] = Implementation(
    name="BBDOB W-Model",
    description="Tunable generator for binary optimization",
    links=[Link(type="repository", url="https://github.com/thomasWeise/BBDOB_W_Model")],
)
things["gen_wmodel"] = Generator(
    name="W-model",
    description="Tunable generator for binary optimization based on several difficulty features",
    objectives={1},
    variables=[Variable(type="binary", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_w_model"},
    implementations={"impl_wmodel"},
)

#! - name: Submodular Optimitzation
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: binary
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10254181
#!   implementation: https://github.com/IOHprofiler/IOHexperimenter
#!   source (real-world/artificial): artificial
#!   textual description: set of graph-based submodular optimization problems from 4
#!     problem types
things["suite_submodular"] = Suite(
    name="Submodular Optimization",
    description="set of graph-based submodular optimization problems from 4 problem types",
    objectives={1},
    variables=[Variable(type="binary", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_submodular_optimization_benchmark"},
    implementations={"impl_iohexperimenter"},
)

#! - name: CEC2013
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://peerj.com/articles/cs-2671/CEC2013.pdf
#!   implementation: https://github.com/P-N-Suganthan/CEC2013
#!   source (real-world/artificial): artificial
#!   textual description: suite used for cec2013 competition. Also in IOH https://github.com/IOHprofiler/IOHexperimenter
things["impl_cec2013"] = Implementation(
    name="CEC2013 reference code",
    description="Suganthan's reference implementation",
    links=[Link(type="repository", url="https://github.com/P-N-Suganthan/CEC2013")],
)
things["suite_cec2013"] = Suite(
    name="CEC2013",
    description="suite used for cec2013 competition. Also in IOH.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_cec2013_definitions"},
    implementations={"impl_cec2013", "impl_iohexperimenter"},
)

#! - name: CEC2022
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: scalable
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: '?'
#!   multi-fidelity: 'no'
#!   reference: https://github.com/P-N-Suganthan/2022-SO-BO/blob/main/CEC2022%20TR.pdf
#!   implementation: https://github.com/P-N-Suganthan/2022-SO-BO
#!   source (real-world/artificial): artificial
#!   textual description: suite used for cec2022 competition. Also in IOH https://github.com/IOHprofiler/IOHexperimenter
things["impl_cec2022"] = Implementation(
    name="CEC2022 reference code",
    description="Suganthan's reference implementation",
    links=[Link(type="repository", url="https://github.com/P-N-Suganthan/2022-SO-BO")],
)
things["suite_cec2022"] = Suite(
    name="CEC2022",
    description="suite used for cec2022 competition. Also in IOH.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    source={"artificial"},
    references={"ref_cec2022_tr"},
    implementations={"impl_cec2022", "impl_iohexperimenter"},
)

#! - name: Onemax+Sphere / Zeromax+Sphere
#!   suite/generator/single: single
#!   objectives: '2'
#!   dimensionality: scalable
#!   variable type: binary and continuous;mixed;
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: ''
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3449726.3459521
#!   implementation:
#!   source (real-world/artificial): 'artificial'
#!   textual description: ''
# FIXME: no implementation provided.
things["fn_onemax_sphere_zeromax_sphere"] = Problem(
    name="Onemax+Sphere / Zeromax+Sphere",
    objectives={2},
    variables=[
        Variable(type="binary", dim=ValueRange(min=1)),
        Variable(type="continuous", dim=ValueRange(min=1)),
    ],
    source={"artificial"},
    references={"ref_onemax_sphere_zeromax_sphere"},
)

#! - name: Onemax+Sphere / DeceptiveTrap+RotatedEllipsoid
#!   suite/generator/single: single
#!   objectives: '2'
#!   dimensionality: scalable
#!   variable type: binary and continuous;mixed;
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: ''
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3449726.3459521
#!   implementation:
#!   source (real-world/artificial): 'artificial'
#!   textual description: ''
# FIXME: no implementation provided.
things["fn_onemax_sphere_deceptive_rotell"] = Problem(
    name="Onemax+Sphere / DeceptiveTrap+RotatedEllipsoid",
    objectives={2},
    variables=[
        Variable(type="binary", dim=ValueRange(min=1)),
        Variable(type="continuous", dim=ValueRange(min=1)),
    ],
    source={"artificial"},
    references={"ref_onemax_sphere_zeromax_sphere"},
)

#! - name: InverseDeceptiveTrap+RotatedEllipsoid / DeceptiveTrap+RotatedEllipsoid
#!   suite/generator/single: single
#!   objectives: '2'
#!   dimensionality: scalable
#!   variable type: binary and continuous;mixed;
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: ''
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1145/3449726.3459521
#!   implementation:
#!   source (real-world/artificial): 'artificial'
#!   textual description: ''
# FIXME: no implementation provided.
things["fn_invdeceptive_deceptive_rotell"] = Problem(
    name="InverseDeceptiveTrap+RotatedEllipsoid / DeceptiveTrap+RotatedEllipsoid",
    objectives={2},
    variables=[
        Variable(type="binary", dim=ValueRange(min=1)),
        Variable(type="continuous", dim=ValueRange(min=1)),
    ],
    source={"artificial"},
    references={"ref_onemax_sphere_zeromax_sphere"},
)

#! - name: PorkchopPlotInterplanetaryTrajectory
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: 2
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1109/CEC65147.2025.11042973
#!   implementation: https://github.com/ShuaiqunPan/Transfer_Random_forests_BBOB_Real_world
#!   source (real-world/artificial): 'real-world'
#!   textual description: ''
things["impl_transfer_rf_bbob_rw"] = Implementation(
    name="Transfer Random Forests BBOB Real-world",
    description="Real-world BBOB-like problem implementations (Porkchop, KinematicsRobotArm)",
    links=[
        Link(
            type="repository",
            url="https://github.com/ShuaiqunPan/Transfer_Random_forests_BBOB_Real_world",
        )
    ],
)
things["suite_porkchop"] = Suite(
    name="PorkchopPlotInterplanetaryTrajectory",
    objectives={1},
    variables=[Variable(type="continuous", dim=2)],
    modality={"multimodal"},
    source={"real-world"},
    references={"ref_porkchop_plot_interplanetary_trajectory"},
    implementations={"impl_transfer_rf_bbob_rw"},
)

#! - name: KinematicsRobotArm
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: 21
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'no'
#!   multi-fidelity: 'no'
#!   reference: https://doi.org/10.1023/A:1013258808932
#!   implementation: https://github.com/ShuaiqunPan/Transfer_Random_forests_BBOB_Real_world
#!   source (real-world/artificial): 'real-world'
#!   textual description: ''
things["suite_kinematics_robotarm"] = Suite(
    name="KinematicsRobotArm",
    objectives={1},
    variables=[Variable(type="continuous", dim=21)],
    modality={"unimodal"},
    source={"real-world"},
    references={"ref_kinematics_of_a_robot_arm"},
    implementations={"impl_transfer_rf_bbob_rw"},
)

#! - name:  VehicleDynamics
#!   suite/generator/single: suite
#!   objectives: '1'
#!   dimensionality: 2
#!   variable type: continuous
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   reference: https://www.scitepress.org/Papers/2023/121580/121580.pdf
#!   implementation: https://zenodo.org/records/8307853
#!   source (real-world/artificial): 'real-world'
#!   textual description: ''
things["impl_vehicle_dynamics"] = Implementation(
    name="VehicleDynamics (Zenodo)",
    description="Zenodo archive for the vehicle dynamics benchmark",
    links=[Link(type="archive", url="https://zenodo.org/records/8307853")],
)
things["suite_vehicle_dynamics"] = Suite(
    name="VehicleDynamics",
    objectives={1},
    variables=[Variable(type="continuous", dim=2)],
    modality={"multimodal"},
    source={"real-world"},
    references={"ref_vehicledynamics_benchmark"},
    implementations={"impl_vehicle_dynamics"},
)

#! - name: MECHBench
#!   suite/generator/single: Problem Suite
#!   variable type: Continuous
#!   dimensionality: scalable'
#!   objectives: '1'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Real-World Application
#!   implementation: https://github.com/BayesOptApp/MECHBench
#!   textual description: This is a set of problems with inspiration from Structural
#!     Mechanics Design Optimization. The suite comprises three physical models, from
#!     which the user may define different kind of problems which impact the final design
#!     output.
#!   reference: https://arxiv.org/abs/2511.10821
#!   other info:
#!     partial evaluations: 'no'
#!     full name: MECHBench
#!     constraint properties: Hard Constraints
#!     number of constraints: 1 or 2
#!     description of multimodality: Unstructured or non isotropic multimodality
#!     key challenges / characteristics: Embeds physical simulations and is flexible
#!       and modular
#!     scientific motivation: Bridge the black-box optimization techniques to a Mechanical
#!       Design Problem which require these kinds of algorithms
#!     limitations: The models do not include fracture or damage mechanics, just plasticity.
#!     implementation languages: Python
#!     approximate evaluation time: Times -> from 1 minute to 7 minutes
things["impl_mechbench"] = Implementation(
    name="MECHBench",
    description="Structural mechanics design optimization benchmark",
    language="Python",
    evaluation_time=["1 minute", "7 minutes"],
    links=[Link(type="repository", url="https://github.com/BayesOptApp/MECHBench")],
)
things["suite_mechbench"] = Suite(
    name="MECHBench",
    long_name="MECHBench",
    description="Set of problems inspired by Structural Mechanics Design Optimization. Embeds physical simulations (plasticity only, no fracture/damage). Unstructured/non-isotropic multimodality.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    constraints=[Constraint(hard="yes", number={1, 2})],
    modality={"multimodal"},
    allows_partial_evaluation="no",
    source={"real-world"},
    references={"ref_mechbench"},
    implementations={"impl_mechbench"},
)

#! - name: EXPObench
#!   suite/generator/single: Problem Suite
#!   variable type: Continuous, Integer, Categorical, Conditional
#!   dimensionality: 10 to 135
#!   objectives: '1'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'yes'
#!   multimodal: Unknown
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Real-World Application
#!   implementation: https://github.com/AlgTUDelft/ExpensiveOptimBenchmark
#!   textual description: Wind farm layout optimization, gas filter design, pipe shape
#!     optimization, hyperparameter tuning, and hospital simulation
#!   reference: https://doi.org/10.1016/j.asoc.2023.110744
#!   other info:
#!     partial evaluations: 'no'
#!     full name: EXPensive Optimization benchmark library
#!     constraint properties: Hard Constraints, Soft Constraints, Box Constraints, only
#!       box constraints implemented, others appear as penalty in objective
#!     number of constraints: 2 per variable (box), other constraints unknown (simulator
#!       fails)
#!     form of noise model: real-life (unknown)
#!     type of noise space: Observational
#!     key challenges / characteristics: Expensive objectives
#!     scientific motivation: Address the lack of real-life expensive benchmarks
#!     limitations: single-objective only, constraints are handled naively (penalty in
#!       objective), no parallelization
#!     implementation languages: Python
#!     approximate evaluation time: 2 to 80 seconds
# FIXME: "Conditional" variable type has no schema representation; box number expressed as 2 per variable cannot be encoded.
things["impl_expobench"] = Implementation(
    name="EXPObench",
    description="EXPensive Optimization benchmark library (wind farm layout, gas filter design, pipe shape, hyperparameter tuning, hospital simulation)",
    language="Python",
    evaluation_time=["2 seconds", "80 seconds"],
    links=[Link(type="repository", url="https://github.com/AlgTUDelft/ExpensiveOptimBenchmark")],
)
things["suite_expobench"] = Suite(
    name="EXPObench",
    long_name="EXPensive Optimization benchmark library",
    description="Wind farm layout optimization, gas filter design, pipe shape optimization, hyperparameter tuning, and hospital simulation",
    objectives={1},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=10, max=135)),
        Variable(type="integer", dim=ValueRange(min=10, max=135)),
        Variable(type="categorical", dim=ValueRange(min=10, max=135)),
    ],
    constraints=[
        Constraint(type="box", hard="yes"),
        Constraint(hard="some"),
    ],
    noise_type={"observational", "real-life"},
    allows_partial_evaluation="no",
    source={"real-world"},
    references={"ref_expobench"},
    implementations={"impl_expobench"},
)

#! - name: Gasoline direct injection engine design
#!   suite/generator/single: Single Problem
#!   variable type: Continuous, Ordinal
#!   dimensionality: '7'
#!   objectives: '2'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: Unknown
#!   multi-fidelity: 'yes'
#!   source (real-world/artificial): Real-World Application
#!   implementation: https://doi.org/10.1016/j.ejor.2022.08.032
#!   textual description: ...
#!   other info:
#!     partial evaluations: Unknown
#!     constraint properties: Hard Constraints, Soft Constraints
#!     number of constraints: '5'
#!     key challenges / characteristics: Expensive
#!     limitations: Proprietary
#!     implementation languages: Matlab Simulink and Wave RT co-simulation
# FIXME: "Ordinal" variable type not in schema; falling back to integer.
things["impl_gasoline"] = Implementation(
    name="Gasoline direct injection engine design",
    description="Proprietary Matlab Simulink + Wave RT co-simulation",
    language="Matlab Simulink / Wave RT",
    links=[Link(type="paper", url="https://doi.org/10.1016/j.ejor.2022.08.032")],
)
things["fn_gasoline"] = Problem(
    name="Gasoline direct injection engine design",
    description="Multi-objective optimization to minimize fuel consumption and NOx emissions over a two-minute dynamic duty cycle, subject to five constraints (turbine inlet temperature, knock occurrences, peak cylinder pressure, peak cylinder pressure rise, total work). Seven decision variables cover hardware choices and engine control parameters.",
    objectives={2},
    variables=[
        Variable(type="continuous", dim=7),
        Variable(type="integer", dim=7),
    ],
    constraints=[Constraint(hard="yes", number=5)],
    fidelity_levels={1, 2},
    source={"real-world"},
    references={"ref_gasoline_direct_injection_engine_design"},
    implementations={"impl_gasoline"},
)

#! - name: BEACON
#!   suite/generator/single: Generator
#!   variable type: Continuous
#!   dimensionality: scalable
#!   objectives: '2'
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Artificially Generated
#!   implementation: https://github.com/Stebbet/BEACON/
#!   textual description: Generator for bi-objective benchmark problems with explicitly
#!     controlled correlations in continuous spaces.
#!   reference: https://dl.acm.org/doi/10.1145/3712255.3734303
#!   other info:
#!     partial evaluations: 'no'
#!     full name: Continuous Bi-objective Benchmark problems with Explicit Adjustable
#!       COrrelatioN control
#!     constraint properties: Box Constraints
#!     number of constraints: '0'
#!     description of multimodality: Random
#!     key challenges / characteristics: Multimodal, different correlations among objectives
#!     scientific motivation: Controlled correlation among objectives
#!     limitations: No analytical Pareto front, only bi-objective
#!     implementation languages: Python
#!     approximate evaluation time: Negligible
things["impl_beacon"] = Implementation(
    name="BEACON",
    description="Continuous Bi-objective Benchmark with Explicit Adjustable COrrelatioN control",
    language="Python",
    evaluation_time=["negligible"],
    links=[Link(type="repository", url="https://github.com/Stebbet/BEACON/")],
)
things["gen_beacon"] = Generator(
    name="BEACON",
    long_name="Continuous Bi-objective Benchmark problems with Explicit Adjustable COrrelatioN control",
    description="Generator for bi-objective benchmark problems with explicitly controlled correlations in continuous spaces. Multimodal with random structure.",
    objectives={2},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    constraints=[Constraint(type="box", hard="yes", number=0)],
    modality={"multimodal"},
    allows_partial_evaluation="no",
    source={"artificial"},
    references={"ref_beacon"},
    implementations={"impl_beacon"},
)

#! - name: TulipaEnergy
#!   suite/generator/single: Problem Suite
#!   variable type: Continuous
#!   dimensionality: scalable
#!   objectives: '1'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'yes'
#!   multimodal: 'no'
#!   multi-fidelity: 'yes'
#!   source (real-world/artificial): Real-World Application
#!   implementation: https://tulipaenergy.github.io/TulipaEnergyModel.jl/stable/
#!   textual description: Determine the optimal investment and operation decisions  for
#!     different types of assets in the energy system ... minimizing loss of load.
#!   reference: See https://tulipaenergy.github.io/TulipaEnergyModel.jl/stable/40-scientific-foundation/45-scientific-references
#!   other info:
#!     partial evaluations: Unknown
#!     full name: TulipaEnergyModel.jl
#!     constraint properties: Hard Constraints, Soft Constraints
#!     number of constraints: millions
#!     type of dynamicism: none
#!     form of noise model: depends on input — still working on stochastic inputs
#!     type of noise space: Parameter
#!     key challenges / characteristics: modeled as a potentially very large linear program
#!     scientific motivation: new techniques for solving large whitebox linear optimization problems
#!     limitations: not yet stochastic
#!     implementation languages: Julia / JMP
#!     approximate evaluation time: from minutes to hours
#!     links to usage examples: https://github.com/TulipaEnergy/Tulipa-OBZ-CaseStudy
# FIXME: "number of constraints: millions" cannot be expressed precisely.
things["impl_tulipa"] = Implementation(
    name="TulipaEnergyModel.jl",
    description="Large linear program for optimal investment and operation of energy systems",
    language="Julia / JuMP",
    evaluation_time=["minutes", "hours"],
    links=[
        Link(type="website", url="https://tulipaenergy.github.io/TulipaEnergyModel.jl/stable/"),
        Link(type="example", url="https://github.com/TulipaEnergy/Tulipa-OBZ-CaseStudy"),
    ],
)
things["suite_tulipa_energy"] = Suite(
    name="TulipaEnergy",
    long_name="TulipaEnergyModel.jl",
    description="Determine the optimal investment and operation decisions for different assets in the energy system (production, consumption, conversion, storage, transport) while minimizing loss of load. Modelled as a potentially very large linear program with multiple fidelity levels.",
    objectives={1},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    constraints=[Constraint(hard="yes"), Constraint(hard="some")],
    noise_type={"parameter"},
    modality={"unimodal"},
    fidelity_levels={1, 2},
    source={"real-world"},
    references={"ref_tulipaenergymodel_jl_scientific_references"},
    implementations={"impl_tulipa"},
)

#! - name: ATO
#!   suite/generator/single: Single Problem
#!   variable type: Continuous
#!   dimensionality: '10'
#!   objectives: '2'
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'no'
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Real-World Application
#!   implementation: '-'
#!   textual description: Parameters of the Modules of the Automatic Train Operation
#!     should be optimized. The parameters are continuous with different ranges. There
#!     are two objectives (minimizing energy consumption, minimizing driving duration.
#!   other info:
#!     partial evaluations: 'no'
# FIXME: no implementation available.
things["fn_ato"] = Problem(
    name="ATO",
    description="Parameters of the Modules of the Automatic Train Operation are optimized; two objectives: minimizing energy consumption and minimizing driving duration.",
    objectives={2},
    variables=[Variable(type="continuous", dim=10)],
    modality={"unimodal"},
    allows_partial_evaluation="no",
    source={"real-world"},
)

#! - name: Brachytherapy treatment planning
#!   suite/generator/single: Problem Suite
#!   variable type: Continuous
#!   dimensionality: 100-500
#!   objectives: 2-3
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'yes'
#!   source (real-world/artificial): Real-World Application
#!   textual description: Treatment planning for internal radiation therapy
#!   reference: https://www.sciencedirect.com/science/article/pii/S1538472123016781
#!   other info:
#!     partial evaluations: 'yes'
#!     full name: Brachytherapy treatment planning
#!     constraint properties: Hard Constraints
#!     number of constraints: scalable
#!     key challenges / characteristics: Multi-objective; aggregated objectives
#!     limitations: No public source code
# FIXME: no public source code; no implementation URL.
things["suite_brachytherapy"] = Suite(
    name="Brachytherapy treatment planning",
    long_name="Brachytherapy treatment planning",
    description="Treatment planning for internal radiation therapy. Multi-objective with aggregated objectives; no public source code.",
    objectives={2, 3},
    variables=[Variable(type="continuous", dim=ValueRange(min=100, max=500))],
    constraints=[Constraint(hard="yes", number=ValueRange(min=1))],
    modality={"multimodal"},
    fidelity_levels={1, 2},
    allows_partial_evaluation="yes",
    source={"real-world"},
    references={"ref_brachytherapy_treatment_planning"},
)

#! - name: FleetOpt
#!   suite/generator/single: Single Problem
#!   variable type: Integer
#!   dimensionality: 'Upper level: 54; lower level: 13208'
#!   objectives: '1'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: Unknown
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Real-World Application
#!   implementation: 'Not public: was done for real client with their private data'
#!   textual description: Healthcare organisation in the UK ...
#!   reference: https://dl.acm.org/doi/abs/10.1145/3638530.3664137
#!   other info:
#!     partial evaluations: 'yes'
# FIXME: bilevel dimensionality (upper 54 / lower 13208) expressed as {54, 13208}; impl not public.
things["fn_fleetopt"] = Problem(
    name="FleetOpt",
    description="UK healthcare organisation fleet optimisation: reduce the fleet of non-emergency healthcare trip vehicles while still ensuring all trips can be covered. Bilevel: upper level 54 vars, lower level 13208 vars.",
    objectives={1},
    variables=[Variable(type="integer", dim={54, 13208})],
    constraints=[Constraint(hard="yes")],
    allows_partial_evaluation="yes",
    source={"real-world"},
    references={"ref_fleetopt"},
)

#! - name: Building spatial design
#!   suite/generator/single: Single Problem
#!   variable type: Continuous, Boolean
#!   dimensionality: scalable depending on problem size (e.g. 90 for)
#!   objectives: '2'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: Unknown
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Real-World Application
#!   implementation: https://github.com/TUe-excellent-buildings/BSO-toolbox
#!   textual description: 'Optimise the spatial layout of a building to: minimise energy
#!     consumption for climate control, and minimise the strain on the structure'
#!   reference: https://hdl.handle.net/1887/81789
#!   other info:
#!     partial evaluations: 'no'
#!     constraint properties: Hard Constraints, Box Constraints, Permutation Constraints
#!     number of constraints: 2065 (as example, depends on problem size)
#!     implementation languages: C++
#!     approximate evaluation time: Roughly 1 second per evaluation for the smallest
#!       considered design, and roughly 40 seconds for the larger designs we considered.
# FIXME: Permutation Constraints not representable in ConstraintType; using multiple Constraint objects.
things["impl_bso_toolbox"] = Implementation(
    name="BSO-toolbox",
    description="Building Spatial Design toolbox (TU/e)",
    language="C++",
    evaluation_time=["1 second", "40 seconds"],
    links=[Link(type="repository", url="https://github.com/TUe-excellent-buildings/BSO-toolbox")],
)
things["fn_building_spatial"] = Problem(
    name="Building spatial design",
    description="Optimise the spatial layout of a building to minimise energy consumption for climate control and minimise the strain on the structure. Many hard constraints; mixed-variable (continuous+binary); expensive evaluations.",
    objectives={2},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    constraints=[
        Constraint(hard="yes"),
        Constraint(type="box", hard="yes"),
    ],
    allows_partial_evaluation="no",
    source={"real-world"},
    references={"ref_building_spatial_design"},
    implementations={"impl_bso_toolbox"},
)

#! - name: Electric Motor Design Optimization
#!   suite/generator/single: Single Problem
#!   variable type: Continuous, Integer
#!   dimensionality: '13'
#!   objectives: '1'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'yes'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Real-World Application
#!   implementation: Implementation not freely available
#!   textual description: The goal is to find a design of a synchronous electric motor
#!     for power steering systems that minimizes costs and satisfies all constraints.
#!   reference: https://dis.ijs.si/tea/Publications/Tusar23Multistep.pdf (paper in Slovene)
#!   other info:
#!     partial evaluations: 'no'
#!     full name: Electric Motor Design Optimization
#!     constraint properties: Hard Constraints, Soft Constraints, Box Constraints
#!     number of constraints: '12'
#!     description of multimodality: Constraints are multimodal
#!     key challenges / characteristics: Time-consuming solution evaluation, highly-constrained
#!     scientific motivation: Challenging to find good solutions in a limited time
#!     limitations: 'Unavailability ...'
#!     implementation languages: Python
#!     approximate evaluation time: 8 minutes
#!     general: This is not an available problem, but could be interesting to show to
#!       researchers which difficulties appear in real-world problems
things["impl_emdo"] = Implementation(
    name="Electric Motor Design Optimization",
    description="Not publicly available",
    language="Python",
    evaluation_time=["8 minutes"],
)
things["fn_emdo"] = Problem(
    name="Electric Motor Design Optimization",
    long_name="Electric Motor Design Optimization",
    description="""# Goal
Find a design of a synchronous electric motor for power steering systems that minimizes costs and satisfies all constraints.

# Motivation
Challenging to find good solutions in a limited time.

# Key Challenges
* Time-consuming solution evaluation
* Highly-constrained problem
* Constraints are multimodal

This is not an available problem, but could be interesting to show to researchers which difficulties appear in real-world problems.""",
    objectives={1},
    variables=[
        Variable(type="continuous", dim=13),
        Variable(type="integer", dim=13),
    ],
    constraints=[
        Constraint(hard="yes", number=12),
        Constraint(hard="some"),
        Constraint(type="box", hard="yes"),
    ],
    noise_type={"noisy"},
    modality={"multimodal"},
    allows_partial_evaluation="no",
    source={"real-world"},
    references={"ref_a_multi_step_evaluation"},
    implementations={"impl_emdo"},
)

#! - name: BONO-Bench
#!   suite/generator/single: Generator
#!   variable type: Continuous
#!   dimensionality: scalable
#!   objectives: '2'
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Artificially Generated
#!   implementation: https://github.com/schaepermeier/bonobench
#!   textual description: Bi-objective problem generator and suite with scalable continuous
#!     decision space. Features complex problem properties (different types of multimodality
#!     and challenges in decision and objective space) as well as Pareto front approximations
#!     with error guarantees for the hypervolume and exact R2 indicators.
#!   other info:
#!     partial evaluations: 'no'
#!     full name: Bi-objective Numerical Optimization Benchmark (BONO-Bench)
#!     constraint properties: Box Constraints
#!     implementation languages: Python
things["impl_bonobench"] = Implementation(
    name="BONO-Bench",
    description="Bi-objective Numerical Optimization Benchmark (BONO-Bench)",
    language="Python",
    links=[Link(type="repository", url="https://github.com/schaepermeier/bonobench")],
)
things["gen_bono_bench"] = Generator(
    name="BONO-Bench",
    long_name="Bi-objective Numerical Optimization Benchmark",
    description="Bi-objective problem generator and suite with scalable continuous decision space. Features complex problem properties and Pareto front approximations with error guarantees for the hypervolume and exact R2 indicators.",
    objectives={2},
    variables=[Variable(type="continuous", dim=ValueRange(min=1))],
    constraints=[Constraint(type="box", hard="yes")],
    modality={"multimodal"},
    allows_partial_evaluation="no",
    source={"artificial"},
    implementations={"impl_bonobench"},
)

#! - name: RandOptGen
#!   suite/generator/single: Generator
#!   variable type: Continuous, Integer, Boolean
#!   dimensionality: scalable
#!   objectives: scalable
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Artificially Generated
#!   implementation: https://github.com/MALEO-research-group/RandOptGen
#!   textual description: 'RandOptGen: A Unified Random Problem Generator for Single-and
#!     Multi-Objective Optimization Problems with Mixed-Variable Input Spaces'
#!   other info:
#!     partial evaluations: 'no'
#!     full name: RandOptGen
#!     implementation languages: Python
#!     approximate evaluation time: milliseconds
#!     links to usage examples: https://doi.org/10.1145/3712256.3726478
things["impl_randoptgen"] = Implementation(
    name="RandOptGen",
    description="Unified Random Problem Generator for Single- and Multi-Objective Optimization with Mixed-Variable Input Spaces",
    language="Python",
    evaluation_time=["milliseconds"],
    links=[
        Link(type="repository", url="https://github.com/MALEO-research-group/RandOptGen"),
        Link(type="example", url="https://doi.org/10.1145/3712256.3726478"),
    ],
)
things["gen_randoptgen"] = Generator(
    name="RandOptGen",
    long_name="RandOptGen",
    description="A Unified Random Problem Generator for Single- and Multi-Objective Optimization Problems with Mixed-Variable Input Spaces.",
    # FIXME: original "scalable" - truncated to 1..10.
    objectives=set(range(1, 11)),
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="integer", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    modality={"multimodal"},
    allows_partial_evaluation="no",
    source={"artificial"},
    implementations={"impl_randoptgen"},
)

#! - name: CUTEr
#!   suite/generator/single: Problem Suite
#!   variable type: Continuous, Integer, Boolean
#!   dimensionality: scalable
#!   objectives: '1'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: Unknown
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Artificially Generated
#!   implementation: Not Found
#!   textual description: A constrained and unconstrained testing environment
#!   reference: https://dl.acm.org/doi/10.1145/962437.962439
#!   other info:
#!     partial evaluations: 'no'
# FIXME: implementation not found.
things["suite_cuter"] = Suite(
    name="CUTEr",
    description="A constrained and unconstrained testing environment.",
    objectives={1},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="integer", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    constraints=[Constraint(hard="yes")],
    allows_partial_evaluation="no",
    source={"artificial"},
    references={"ref_cuter"},
)

#! - name: CUTEst
#!   suite/generator/single: Problem Suite
#!   variable type: Continuous, Integer, Boolean
#!   dimensionality: scalable
#!   objectives: '1'
#!   constraints: 'yes'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: 'yes'
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Artificially Generated
#!   implementation: https://github.com/jfowkes/pycutest
#!   textual description: The Constrained and Unconstrained Testing Environment with
#!     safe threads (CUTEst) for optimization software
#!   reference: https://link.springer.com/article/10.1007/s10589-014-9687-3
#!   other info:
#!     partial evaluations: 'no'
#!     full name: 'Constrained and Unconstrained Testing Environment with safe threads '
#!     constraint properties: Soft Constraints, Box Constraints
#!     number of constraints: scalable
#!     implementation languages: Python, C++, Fortran
#!     general: 'Python implementation: https://github.com/jfowkes/pycutest'
things["impl_pycutest"] = Implementation(
    name="pycutest",
    description="Python interface to CUTEst",
    language="Python / C++ / Fortran",
    links=[Link(type="repository", url="https://github.com/jfowkes/pycutest")],
)
things["suite_cutest"] = Suite(
    name="CUTEst",
    long_name="Constrained and Unconstrained Testing Environment with safe threads",
    description="CUTEst for optimization software",
    objectives={1},
    variables=[
        Variable(type="continuous", dim=ValueRange(min=1)),
        Variable(type="integer", dim=ValueRange(min=1)),
        Variable(type="binary", dim=ValueRange(min=1)),
    ],
    constraints=[
        Constraint(hard="some", number=ValueRange(min=1)),
        Constraint(type="box", hard="yes"),
    ],
    modality={"multimodal"},
    allows_partial_evaluation="no",
    source={"artificial"},
    references={"ref_cutest"},
    implementations={"impl_pycutest"},
)

#! - name: PUBOi
#!   suite/generator/single: Generator
#!   variable type: Boolean
#!   dimensionality: scalable
#!   objectives: '1'
#!   constraints: 'no'
#!   dynamic: 'no'
#!   noise: 'no'
#!   multimodal: Unknown
#!   multi-fidelity: 'no'
#!   source (real-world/artificial): Artificially Generated
#!   implementation: https://gitlab.com/verel/pubo-importance-benchmark
#!   textual description: A benchmark in which variable importance is tunable, based
#!     on the Walsh function
#!   reference: https://link.springer.com/chapter/10.1007/978-3-031-04148-8_12
#!   other info:
#!     partial evaluations: 'no'
#!     full name: Polynomial Unconstrained Binary Optimization
#!     key challenges / characteristics: Tunable variable importance
#!     implementation languages: Python, C++
things["impl_puboi"] = Implementation(
    name="PUBO Importance Benchmark",
    description="A benchmark in which variable importance is tunable, based on the Walsh function",
    language="Python / C++",
    links=[Link(type="repository", url="https://gitlab.com/verel/pubo-importance-benchmark")],
)

things["gen_puboi"] = Generator(
    name="PUBOi",
    long_name="Polynomial Unconstrained Binary Optimization with tunable importance",
    description="A benchmark in which variable importance is tunable, based on the Walsh function.",
    objectives={1},
    variables=[Variable(type="binary", dim=ValueRange(min=1))],
    allows_partial_evaluation="no",
    source={"artificial"},
    references={"ref_puboi"},
    implementations={"impl_puboi"},
)


library = Library(things)

# Make sure model is really valid
Library.model_validate(library)

if __name__ == "__main__":
    with open("problems.yaml", "w") as fd:
        fd.write(to_yaml_str(library))
