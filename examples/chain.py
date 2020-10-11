import json

from dataclasses import dataclass, field, asdict
from yaab.adapter import BaseAdapter



@dataclass
class DatabaseConfig(BaseAdapter):
    host: str = field(metadata={"transformations": ("db_host", )})
    port: int = field(metadata={"transformations": ("db_port", int)})


@dataclass
class AppConfig(BaseAdapter):
    name: str = field(metadata={"transformations": ("app_name", )})
    db: DatabaseConfig = field(metadata={"transformations": ("db_conf", DatabaseConfig)})


def get_config() -> AppConfig:
    input_dict = {"app_name": "My App", "db_conf": {"db_host": "my.db", "db_port": 123}}
    return AppConfig.from_dict(input_dict)


def main():
    config = get_config()
    print("Loaded dataclass: ", config)
    output_dict = asdict(config)
    print("Output dictionary: ", output_dict)


if __name__ == "__main__":
    main()
