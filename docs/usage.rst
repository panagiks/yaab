=====
Usage
=====

To use Yet Another Adapter Base in a project, the base requirement is to create a dataclass that inherits from `BaseAdapter`. In order for
`yaab` to know how to obtain the data for each of the dataclass' fields you need to provide a chain of `transformations`. `transformations`
are by default provided in `field`'s `metadata` kwarg as a `tuple` under the key `transformations`.

If a `transformation` is another `dataclass` then its `from_any` classmethod is invoked with the element as it has been transformed up to
now as its starting element. This allows for nesting but most importantly allows the innermost class to be agnostic as to how the
encapsulating class will use it::

    from dataclasses import asdict, dataclass, field

    from yaab.adapter import BaseAdapter


    @dataclass
    class DbModel(BaseAdapter):
        host: str = field(metadata={"transformations": ("db_host", )})
        port: int = field(metadata={"transformations": ("db_port", int)})

    @dataclass
    class ConfigModel(BaseAdapter):
        name: str = field(metadata={"transformations": ("app_name", )})
        db: DbModel = field(metadata={"transformations": ("db_conf", DbModel)})

    conf = ConfigModel.from_dict({"app_name": "My App", "db_conf": {"db_host": "my.db", "db_port": 123}})
    print(conf)
    print(asdict(conf))

The above will print::

    ConfigModel(name='My App', db=DbModel(host='my.db', port=123))
    {'name': 'My App', 'db': {'host': 'my.db', 'port': 123}}
