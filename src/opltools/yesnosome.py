from enum import Enum


class YesNoSome(Enum):
    yes = "yes"
    no = "no"
    some = "some"
    unknown = "unknown"


def union(
    a: YesNoSome | set[YesNoSome], b: YesNoSome | set[YesNoSome]
) -> YesNoSome | set[YesNoSome]:
    result = set()
    if isinstance(a, YesNoSome):
        result.add(a)
    else:
        result.update(a)

    if isinstance(b, YesNoSome):
        result.add(b)
    else:
        result.update(b)

    if len(result) == 1:
        return result.pop()
    else:
        return result
