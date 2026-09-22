from opltools import Implementation, Generator, Reference, Library, Variable, Constraint
from pydantic_yaml import to_yaml_str

things = {}

things["cobi_impl"] = Implementation(
    name="COBI Implementation",
    description="Python library for COBI (COnstrained BI-objective optimization) problem generator",
    language="python",
    links=[
        {
            "type": "repository",
            "url": "https://github.com/numbbo/cobi-problem-generator/",
        },
        {
            "type": "v0.5.0",
            "url": "https://github.com/numbbo/cobi-problem-generator/releases/tag/v0.5.0",
        },
    ],
    requirements="https://github.com/numbbo/cobi-problem-generator/blob/main/requirements.txt",
)

things["cobi_problem"] = Generator(
    name="COBI Problem",
    description="Generator of COnstrained BI-objective optimization problems",
    tags={
        "constrained",
        "bi-objective",
        "continuous",
        "black-box",
        "location",
        "multi-peak",
        "convex-quadratic",
    },
    references=[
        Reference(
            title="Pareto Set Characterization in Constrained Multiobjective Optimization and the COBI Problem Generator",
            authors=["Anne Auger", "Dimo Brockhoff", "Luka Opravš", "Tea Tušar"],
            link={"type": "arxiv", "url": "https://arxiv.org/abs/2604.09131"},
            type="definition"
        )
    ],
    objectives={2},
    variables=[Variable(type="continuous", dim={"min": 1})],
    implementations={"cobi_impl"},
    can_evaluate_objectives_independently="no",
    constraints=[
        Constraint(type="box", hard="yes", number={"min": 0}),
        Constraint(type="linear", hard="yes", number={"min": 0}),
        Constraint(type="function", hard="yes", number={"min": 0}),
    ],
    noise_type={"none"},
    dynamic_type=None,
    allows_partial_evaluation="no",
    modality={"multi-modal per objective"},
    fidelity_levels={1},
    source={"artificial"},
    code_examples={"./code_153.py"},
)
library = Library(things)

print(to_yaml_str(library))
