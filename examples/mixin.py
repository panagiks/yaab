from dataclasses import asdict, dataclass, field

from yaab.adapter import BaseAdapter
from yaab.mixin import DictMixin


@dataclass
class SchemaAdapter(BaseAdapter, DictMixin):
    id: int = field(metadata={"transformations": ("oid", int)})
    name: str = field(metadata={"transformations": ("weird_name", )})


def main():
    input_dict = {"weird_name": "My name", "oid": "3"}
    m = SchemaAdapter.from_dict(input_dict)
    print("Loaded dataclass: ", m)
    print("Accessing adapter as dict: ", m['id'])
    output_dict = asdict(m)
    print("Output dictionary: ", output_dict)


if __name__ == "__main__":
    main()
