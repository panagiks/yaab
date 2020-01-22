========================
Yet Another Adapter Base
========================


.. image:: https://img.shields.io/pypi/v/yaab.svg
        :target: https://pypi.python.org/pypi/yaab

.. image:: https://img.shields.io/travis/panagiks/yaab.svg
        :target: https://travis-ci.org/panagiks/yaab

.. image:: https://readthedocs.org/projects/yaab/badge/?version=latest
        :target: https://yaab.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




YAAB aims to provide a flexible base for Adapter Design Pattern implementations based on dataclasses.


* Free software: MIT license
* Documentation: https://yaab.readthedocs.io.


Example Usage
-------------

Let's assume that you are interfacing an API that returns a `JSON` object with the following structure:

.. code-block:: json

    {
        "weird_name": "My name",
        "oid": "3"
    }

And you would like to transform it into a schema that fits the rest of your API, let's assume:

.. code-block:: json

    {
        "name": "My name",
        "id": 3
    }

Then you would define and use your model in the following way:

::

    >>> from dataclasses import asdict, dataclass, field
    >>>
    >>> from yaab.adapter import BaseAdapter
    >>>
    >>> @dataclass
    ... class MyModel(BaseAdapter):
    ...     id: int = field(metadata={"transformations": ("oid", int)})
    ...     name: str = field(metadata={"transformations": ("weird_name", )})
    ...
    >>> m = MyModel.from_dict({"weird_name": "My name", "oid": "3"})
    >>> print(m)
    MyModel(id=3, name='My name')
    >>> asdict(m)
    {'id': 3, 'name': 'My name'}


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
