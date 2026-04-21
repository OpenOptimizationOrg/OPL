from enum import Enum
from typing_extensions import Self
from pydantic import BaseModel, RootModel, ConfigDict, model_validator

from .utils import ValueRange, union_range


class OPLType(Enum):
    problem = "problem"
    suite = "suite"
    generator = "generator"
    implementation = 'implementation'


class YesNoSome(Enum):
    yes = "yes"
    no = "no"
    some = "some"
    unknown = "?"


class Link(BaseModel):
    type: str | None = None
    url: str


class Thing(BaseModel):
    type: OPLType
    model_config = ConfigDict(extra='allow')


class Objectives(RootModel):
    root: int | set[int] | ValueRange = 0

    def union(self, other: Self) -> Self:
        self.root = union_range(self.root, other.root)
        return self


class Variables(BaseModel):
    continuous: int | set[int] | ValueRange = 0
    integer: int | set[int] | ValueRange = 0
    binary: int | set[int] | ValueRange = 0
    categorical: int | set[int] | ValueRange = 0

    def union(self, other: Self) -> Self:
        self.continuous = union_range(self.continuous, other.continuous)
        self.integer = union_range(self.integer, other.integer)
        self.binary = union_range(self.integer, other.binary)
        self.categorical = union_range(self.integer, other.categorical)
        return self


class Constraints(BaseModel):
    box: int | set[int] | ValueRange = 0
    linear: int | set[int] | ValueRange = 0
    function: int | set[int] | ValueRange = 0

    def union(self, other: Variables) -> Self:
        self.box = union_range(self.box, other.box)
        self.linear = union_range(self.linear, other.linear)
        self.function = union_range(self.function, other.function)
        return self


class Reference(BaseModel):
    title: str
    authors: list[str]
    link: Link | None = None


class Usage(BaseModel):
    language: str
    code: str


class Implementation(Thing):
    type: OPLType= OPLType.implementation
    name: str
    description: str
    links: list[Link] | None = None
    language: str | None = None
    evaluation_time: str | None = None
    requirements: str | list[str] | None = None


class ProblemLike(Thing):
    name: str
    long_name: str | None = None
    description: str | None = None
    tags: set[str] | None = None
    references: set[Reference] | None = None
    implementations: set[str] | None = None
    objectives: set[int] | None = None
    variables: Variables | None = None
    constraints: Constraints | None = None
    soft_constraints: Constraints | None = None
    dynamic_type: set[str] | None = None
    noise_type: set[str] | None = None
    allows_partial_evaluation: YesNoSome | None = None
    can_evaluate_objectives_independently: YesNoSome | None = None
    modality: set[str] | None = None
    fidelity_levels: set[int] | None = None
    code_examples: set[str] | None = None
    source: set[str] | None = None


class Problem(ProblemLike):
    type:OPLType = OPLType.problem
    instances: ValueRange | list[str] | None = None


class Suite(ProblemLike):
    type:OPLType = OPLType.suite
    problems: set[str] | None = None


class Generator(ProblemLike):
    type:OPLType = OPLType.generator


class Library(RootModel):
    root: dict[str, Problem | Generator | Suite | Implementation] | None

    def _check_id_references(self, ids, type:OPLType) -> None:
        if not self.root: return
        for id in ids:
            if id in self.root:
                if self.root[id].type != type:
                    raise ValueError(f"ID {id} is a {self.root[id].name}, expected a {type.name}")
            else:
                raise ValueError(f"Missing {type.name} with id '{id}'")

    def _fixup_fidelity(self, suite: Suite) -> Suite:
        return suite

    @model_validator(mode="after")
    def validate(self) -> Self:
        if not self.root: return self

        # Make sure all problems referenced in suites exists
        for id, thing in self.root.items():
            if isinstance(thing, Suite) and thing.problems:
                for problem_id in thing.problems:
                    if problem_id not in self.root:
                        raise ValueError(f"Suite {id} references problem with undefined id '{problem_id}'.")
                    if self.root[problem_id].type != OPLType.problem:
                        raise ValueError(f"Suite {id} references problem with id '{problem_id}' but id is a {self.root[problem_id].type.name}.")
        return self

__all__ = [
    "Problem",
    "Suite",
    "Generator",
    "Implementation",
    "Library",
    "YesNoSome",
    "Link",
    "Reference"
]
