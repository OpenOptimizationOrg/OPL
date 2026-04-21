from opltools import Suite, Problem, Library, Link, Variables, ValueRange
from pydantic_yaml import to_yaml_str
from opltools.schema import Implementation, YesNoSome, Constraints, Generator, Reference
import numpy as np

things = {}

things["cobi_impl"] = Implementation(
    name="COBI Implementation",
    description="Python library for COBI (COnstrained BI-objective optimization) problem generator",
    language="python",
    links=[
        Link(
            type="repository", url="https://github.com/numbbo/cobi-problem-generator/"
        ),
        Link(
            type="v0.5.0",
            url="https://github.com/numbbo/cobi-problem-generator/releases/tag/v0.5.0",
        ),
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
    references={
        Reference(
            title="Pareto Set Characterization in Constrained Multiobjective Optimization and the COBI Problem Generator",
            authors=["Anne Auger", "Dimo Brockhoff", "Luka Opravˇs", "Tea Tuˇsar"],
            link=Link(type="arxiv", url="https://arxiv.org/abs/2604.09131"),
        )
    },
    objectives={2},
    variables=Variables(continuous=ValueRange(min=1, max=np.inf)),  # inf?
    implementations=["cobi_impl"],
    can_evaluate_objectives_independently=YesNoSome.no,
    constraints=Constraints(
        box=1, linear=np.inf, function=np.inf
    ),  # convex-quadratic or multipeak, one box per variable?
    noise_type={"none"},
    soft_constraints=None,
    dynamic_type=None,
    allows_partial_evaluation=YesNoSome.no,
    modality={"multi-modal per objective"},
    fidelity_levels={1},
    source={"artificial"},
    code_examples={"./code_153.py"},
)
library = Library(things)

print(to_yaml_str(library))
