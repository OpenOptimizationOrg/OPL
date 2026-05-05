from typing_extensions import Self
from pydantic import BaseModel, model_validator


class ValueRange(BaseModel):
    min: int | None
    max: int | None = None

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.min is None and self.max is None:
            raise ValueError("Variable range should have at least a min or max value.")
        return self

    def __hash__(self):
        return hash((self.min, self.max))


def _none_min(a, b):
    if a and b:
        return min(a, b)
    elif a:
        return a
    else:
        return b


def _none_max(a, b):
    if a and b:
        return max(a, b)
    elif a:
        return a
    else:
        return b


def union_range(
    a: int | set[int] | ValueRange, b: int | set[int] | ValueRange
) -> int | set[int] | ValueRange:
    if isinstance(a, int):
        a = {a}
    if isinstance(b, int):
        b = {b}

    if isinstance(a, set) and isinstance(b, set):
        res = a.union(b)
        return res.pop() if len(res) == 1 else res
    elif isinstance(a, ValueRange) and isinstance(b, ValueRange):
        return ValueRange(min=_none_min(a.min, b.min), max=_none_max(a.max, b.max))

    if isinstance(a, set):
        a, b = b, a
    if isinstance(a, ValueRange) and isinstance(b, set):
        res = ValueRange(min=a.min, max=a.max)
        if res.min:
            for v in b:
                res.min = min(v, res.min)
        if res.max:
            for v in b:
                res.max = max(v, res.max)  #
        return res

    raise Exception("BAM")
