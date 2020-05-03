#!/usr/bin/env python

"""Tests for `yaab.mixin` module."""

import pytest
import warnings

from dataclasses import dataclass, field

from yaab.mixin import DictMixin, FieldMetaConverterMixin, FieldTypeConverterMixin


def test_dict_mixin():
    @dataclass
    class FakeDataclass(DictMixin):
        foo: str

    f = FakeDataclass(foo="bar")
    assert f["foo"] == "bar"
    f["foo"] = ""
    assert f["foo"] == ""
    with pytest.raises(KeyError):
        f["bar"]
    assert list(f.keys()) == ["foo"]
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        del f["foo"]
        assert len(w) == 1
        assert issubclass(w[-1].category, SyntaxWarning)
        with pytest.raises(KeyError):
            del f["bar"]


def test_field_meta_converter_mixin():
    @dataclass
    class FakeDataclass(FieldMetaConverterMixin):
        foo: str = field(metadata={"converter": str})
        bar: int

    f = FakeDataclass(2, 3)
    assert f.foo == "2"
    assert f.bar == 3


def test_field_type_converter_mixin():
    @dataclass
    class FakeDataclass(FieldTypeConverterMixin):
        foo: bool = field(metadata={"convert": True})
        bar: int = field(metadata={"convert": True})
        far: int = field(metadata={"convert": True})
        jar: str

    f = FakeDataclass("false", "2", 3, "jar")
    assert f.foo == False
    assert f.bar == 2
    assert f.far == 3
    assert f.jar == "jar"
