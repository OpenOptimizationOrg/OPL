from opltools import Library, Problem, Implementation
from pydantic_yaml import to_yaml_str

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
#!       problem
#!     scientific motivation: Challenging to find good solutions in a limited time
#!     limitations: 'Unavailability, even if available, it wouldn''t be helpful to use
#!       for benchmarking due taking a long time to evaluate a single solution '
#!     implementation languages: Python
#!     approximate evaluation time: 8 minutes
#!     general: This is not an available problem, but could be interesting to show to
#!       researchers which difficulties appear in real-world problems

library = Library({
    "impl_emdo":  Implementation(
        name="Electric Motor Design Optimization",
        description="Not publicly available",
        language="python",
        evaluation_time=["8 minutes"]
    ),
    "fn_emdo":  Problem(
        name="Electric Motor Design Optimization",
        description="""# Goal
Find a design of a synchronous electric motor for power steering systems that minimizes costs and satisfies all constraints.

# Motivation
Challenging to find good solutions in a limited time

# Key Challenges
* Time-consuming solution evaluation,
* highly-constrained problem
* Constraints are multimodal

This is not an available problem, but could be interesting to show to researchers which difficulties appear in real-world problems""",
        objectives=[1],
        variables=[
            {"type": "continuous", "dim": {"min": None, "max": 13}},
            {"type": "integer", "dim": {"min": None, "max": 13}},
        ],
        modality=["multimodal"],
        allows_partial_evaluation="no",
        constraints=[
            {"type": "box", "hard": "some", "number": 12}
        ],
        dynamic_type=["no"],
        noise_type=["yes"],
        fidelity_levels=[1],
        source=["real-world"],
        references=[
            {
                "title": "A Multi-Step Evaluation Process in Electric Motor Design",
                "lang": "sj",
                "authors": ["Tea Tušar", "Peter Korošec", "Bogdan Filipič"],
                "link": {"url": "https://dis.ijs.si/tea/Publications/Tusar23Multistep.pdf"}
            }
        ],
        implementations=["impl_emdo"]
    )
})

print(to_yaml_str(library))
