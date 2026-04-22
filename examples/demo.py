from opltools import Suite, Problem, Library, Link, Variable, ValueRange
from pydantic_yaml import to_yaml_str
from opltools.schema import Implementation

things = {}

things["impl_py_cocoex"] = Implementation(
    name="coco-experiment Python module",
    description="Python bindings for the experiment part of the COCO framework",
    language="python",
    links=[
        Link(type="repository", url="https://github.com/numbbo/coco-experiment"),
        Link(type="package", url="https://pypi.org/project/coco-experiment/"),
    ],
    evaluation_time="sub second",
)

for fnr in range(1, 25):
    id = f"fn_bbob_f{fnr}"
    things[f"fn_bbob_f{fnr}"] = Problem(
        name=f"BBOB F_{fnr}",
        objectives={1},
        variables={Variable(type="continuous", dim=ValueRange(min=1, max=80))},
        implementations=["impl_py_cocoex"],
    )

things["suite_bbob"] = Suite(
    name="BBOB",
    problems={f"fn_bbob_f{fnr}" for fnr in range(1, 25)},
    implementations=["impl_py_cocoex"],
)

library = Library(things)

print(to_yaml_str(library))
