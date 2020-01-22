#!/usr/bin/env python

"""Tests for `yaab` package."""

import pytest
from dataclasses import dataclass, field

from yaab.adapter import BaseAdapter


TEST_ID = 1
TEST_NAME = "foo"


@dataclass
class FakeModel(BaseAdapter):
    id: int = field(metadata={"transformations": ("id",)})
    name: str = field(metadata={"transformations": ("name", str)})


def test_init():
    m = FakeModel(id=TEST_ID, name=TEST_NAME)
    assert m.id == TEST_ID
    assert m.name == TEST_NAME

def test_from_dict():
    m = FakeModel.from_dict({"id": TEST_ID, "name": TEST_NAME})
    assert m.id == TEST_ID
    assert m.name == TEST_NAME

def test_from_env():
    import os
    os.environ["APP_ID"] = str(TEST_ID)
    @dataclass
    class EnvFakeModel(BaseAdapter):
        id: int = field(metadata={"transformations": ("APP_ID", int)})
    m = EnvFakeModel.from_env()
    assert m.id == TEST_ID

def test_with_defaults():
    m = FakeModel.from_dict({"id": TEST_ID}, name=TEST_NAME)
    assert m.id == TEST_ID
    assert m.name == TEST_NAME

def test_accessor_none():
    class FakeModelExt(FakeModel):
        _accessor = lambda el, tr: el[tr]

    m = FakeModelExt.from_any({"id": TEST_ID, "name": TEST_NAME})
    assert m.id == TEST_ID
    assert m.name == TEST_NAME
