from enum import Enum
from typing_extensions import Self
from pydantic import BaseModel, RootModel, ConfigDict, model_validator

from .yesnosome import YesNoSome
from .utils import ValueRange, union_range


class OPLType(Enum):
    problem = "problem"
    suite = "suite"
    generator = "generator"
    implementation = "implementation"


class Link(BaseModel):
    type: str | None = None
    url: str

    def __hash__(self):
        return hash(self.type) + hash(self.url)


class Thing(BaseModel):
    type: OPLType
    model_config = ConfigDict(extra="allow")


class Objectives(RootModel):
    root: int | set[int] | ValueRange = 0

    def union(self, other: Self) -> Self:
        self.root = union_range(self.root, other.root)
        return self


class VariableType(Enum):
    continuous = "continuous"
    integer = "integer"
    binary = "binary"
    categorical = "categorical"
    unknown = "unknown"


class Variable(BaseModel):
    type: VariableType = VariableType.unknown
    dim: int | set[int] | ValueRange | None = 0

    def __hash__(self):
        if isinstance(self.dim, set):
            dim_hash = hash(frozenset(self.dim))
        else:
            dim_hash = hash(self.dim)
        return hash(self.type) + dim_hash


class ConstraintType(Enum):
    box = "box"
    linear = "linear"
    function = "function"
    unknown = "unknown"


class Constraint(BaseModel):
    type: ConstraintType = ConstraintType.unknown
    hard: YesNoSome | None = None
    equality: YesNoSome | None = None
    number: int | set[int] | ValueRange | None = None

    def __hash__(self):
        number = frozenset(self.number) if isinstance(self.number, set) else self.number
        return hash((self.type, self.hard, self.equality, number))


class Reference(BaseModel):
    title: str | None = None
    authors: list[str] | None = None
    link: Link | None = None

    @model_validator(mode="after")
    def _validate(self) -> Self:
        if self.title is None and self.link is None:
            raise ValueError("References must have either a title or a link.")
        return self

    def __hash__(self):
        return hash(self.title) + hash(self.link)


class Usage(BaseModel):
    language: str
    code: str


class Implementation(Thing):
    type: OPLType = OPLType.implementation
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
    variables: set[Variable] | None = None
    constraints: set[Constraint] | None = None
    dynamic_type: set[str] | None = None
    noise_type: set[str] | None = None
    allows_partial_evaluation: YesNoSome | None = None
    can_evaluate_objectives_independently: YesNoSome | None = None
    modality: set[str] | None = None
    fidelity_levels: set[int] | None = None
    code_examples: set[str] | None = None
    source: set[str] | None = None

    def __hash__(self):
        return hash((self.type, self.name))


class Problem(ProblemLike):
    type: OPLType = OPLType.problem
    instances: ValueRange | list[str] | None = None


class Suite(ProblemLike):
    type: OPLType = OPLType.suite
    problems: set[str] | None = None


class Generator(ProblemLike):
    type: OPLType = OPLType.generator


class Library(RootModel):
    root: dict[str, Problem | Generator | Suite | Implementation] = {}

    def _check_id_references(self, ids, type: OPLType) -> None:
        for id in ids:
            if id in self.root:
                if self.root[id].type != type:
                    raise ValueError(
                        f"ID {id} is a {self.root[id].name}, expected a {type.name}"
                    )
            else:
                raise ValueError(f"Missing {type.name} with id '{id}'")

    # For a given suite, make sure the fidelty_levels property contains
    # the fidelity_levels of all problems in the suite.
    def _fixup_suite_fidelity(self, suite: Suite):
        if suite.problems:
            if not suite.fidelity_levels:
                suite.fidelity_levels = set()
            for pid in suite.problems:
                problem = self.root[pid]
                assert isinstance(problem, Problem)
                if problem.fidelity_levels:
                    suite.fidelity_levels.update(problem.fidelity_levels)

        return suite

    def _fixup_suite_variables(self, suite: Suite):
        if not suite.problems:
            return

        if suite.variables is None:
            suite.variables = set()
        for pid in suite.problems:
            problem = self.root[pid]
            assert isinstance(problem, Problem)
            if problem.variables is not None:
                suite.variables.update(problem.variables)

    @model_validator(mode="after")
    def _validate(self) -> Self:
        # Make sure all problems referenced in suites exists
        for id, thing in self.root.items():
            if isinstance(thing, Suite) and thing.problems:
                for problem_id in thing.problems:
                    if problem_id not in self.root:
                        raise ValueError(
                            f"Suite {id} references problem with undefined id '{problem_id}'."
                        )
                    if self.root[problem_id].type != OPLType.problem:
                        raise ValueError(
                            f"Suite {id} references problem with id '{problem_id}' but id is a {self.root[problem_id].type.name}."
                        )
                self._fixup_suite_fidelity(thing)
        return self


__all__ = [
    "Constraint",
    "Generator",
    "Implementation",
    "Library",
    "Link",
    "Problem",
    "Reference",
    "Suite",
    "Variable",
    "YesNoSome",
]
