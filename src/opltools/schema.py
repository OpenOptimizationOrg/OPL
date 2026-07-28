import json
from enum import Enum
from typing import Any
from typing_extensions import Self
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    SerializerFunctionWrapHandler,
    model_serializer,
    model_validator,
)

from .yesnosome import YesNoSome
from .utils import ValueRange, union_range


def _sort_key(item: Any) -> Any:
    """Stable, total-order sort key for an already-serialized set member.

    Scalars (str, int, float, bool) sort by their natural ordering, so e.g.
    `{2, 10}` sorts numerically rather than as the strings "10" < "2". Dicts
    and lists (serialized nested models) have no natural ordering, so those
    fall back to a canonical JSON string.
    """
    if isinstance(item, (dict, list)):
        return json.dumps(item, sort_keys=True, default=str)
    return item


class _CanonicalMixin:
    """Serialize any `set`-valued field as a sorted list.

    `set` iteration order depends on Python's hash randomization, so two
    otherwise-identical models can serialize to different YAML on every run
    unless we impose a fixed order. Rather than hand-listing every `set`
    field on every model, this inspects each model's actual field values at
    serialization time and sorts whichever ones happen to be a `set` -
    including nested models' own sets (each canonicalizes itself the same
    way) and any `extra="allow"` fields.
    """

    @model_serializer(mode="wrap")
    def _canonicalize(self, handler: SerializerFunctionWrapHandler) -> Any:
        data = handler(self)
        values = dict(self.__dict__)
        extra = getattr(self, "__pydantic_extra__", None)
        if extra:
            values.update(extra)
        for name, value in values.items():
            if isinstance(value, set) and name in data:
                data[name] = sorted(data[name], key=_sort_key)
        return data


class CanonicalModel(_CanonicalMixin, BaseModel):
    pass


class CanonicalRootModel(_CanonicalMixin, RootModel):
    pass


class OPLType(Enum):
    problem = "problem"
    suite = "suite"
    generator = "generator"
    implementation = "implementation"


class Link(CanonicalModel):
    type: str | None = None
    url: str

    def __hash__(self):
        return hash(self.type) + hash(self.url)


class Thing(CanonicalModel):
    type: OPLType
    model_config = ConfigDict(extra="allow")


class Objectives(CanonicalRootModel):
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


class Variable(CanonicalModel):
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


class Constraint(CanonicalModel):
    type: ConstraintType = ConstraintType.unknown
    hard: YesNoSome | None = None
    equality: YesNoSome | None = None
    number: int | set[int] | ValueRange | None = None

    def __hash__(self):
        number = frozenset(self.number) if isinstance(self.number, set) else self.number
        return hash((self.type, self.hard, self.equality, number))


class Reference(CanonicalModel):
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


class Implementation(Thing):
    type: OPLType = OPLType.implementation
    name: str
    description: str
    links: list[Link] | None = None
    language: str | None = None
    evaluation_time: set[str] | None = None
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
    evaluation_time: set[str] | None = None
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


class Library(CanonicalRootModel):
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

    def _percolate_set(self, thing: Any, children: set | None, property: str):
        """Propagate some `property` from child objects to the parent by calculating the union of all the child property sets.

        This is useful to propagate properties like `variables`, `constraints`, etc. from problems up to the suite.
        """
        if children is None:
            return

        if getattr(thing, property, None) is None:
            setattr(thing, property, set())
        thing_set = getattr(thing, property)

        for child_id in children:
            child = self.root[child_id]
            child_set = getattr(child, property, None)
            if child_set is not None:
                thing_set.update(child_set)

    @model_validator(mode="after")
    def _validate(self) -> Self:
        # First check and fixup all problems
        for id, thing in self.root.items():
            if isinstance(thing, Problem) and thing.implementations:
                self._percolate_set(thing, thing.implementations, "evaluation_time")

        # Then check and fixup all suites because changes from the problems need to propagate to the suites
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

                self._percolate_set(thing, thing.problems, "fidelity_levels")
                self._percolate_set(thing, thing.problems, "variables")
                self._percolate_set(thing, thing.problems, "constraints")
                self._percolate_set(thing, thing.problems, "evaluation_time")

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
