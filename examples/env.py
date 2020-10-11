import os

from dataclasses import asdict, dataclass, field

from yaab.adapter import BaseAdapter


@dataclass
class SchemaAdapter(BaseAdapter):
    id: int = field(metadata={"transformations": ("oid", int)})
    name: str = field(metadata={"transformations": ("weird_name", )})


def main():
    os.environ['weird_name'] = "My name"
    os.environ['oid'] = "3"
    m = SchemaAdapter.from_env()
    print("Loaded dataclass: ", m)
    output_dict = asdict(m)
    print("Output dictionary: ", output_dict)


if __name__ == "__main__":
    main()
