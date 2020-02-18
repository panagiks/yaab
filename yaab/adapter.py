"""Main module."""
import os

from contextlib import suppress
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Callable, ClassVar, Dict, Optional


_TAccessor = Callable[[Any, Any], Any]


@dataclass
class BaseAdapter:
    """
    Base Class for Adapter pattern Models.
    """

    __slots__ = tuple()
    _accessor: ClassVar[_TAccessor] = lambda el, tr: el
    _meta_key: ClassVar[str] = "transformations"

    @classmethod
    def from_any(
        cls,
        element: Any,
        *,
        accessor: Optional[_TAccessor] = None,
        **kwargs: Dict[str, Any]
    ) -> "BaseAdapter":
        if accessor is None:
            accessor = cls._accessor
        for cls_field in fields(cls):
            if cls_field.name in kwargs:
                continue
            value = element
            with suppress(KeyError):
                transformations = cls_field.metadata[cls._meta_key]
                for transformation in transformations:
                    if is_dataclass(transformation):
                        value = transformation.from_any(value, accessor=accessor)
                    elif callable(transformation):
                        value = transformation(value)
                    else:
                        value = accessor(value, transformation)
                kwargs[cls_field.name] = value
        return cls(**kwargs)

    @classmethod
    def from_dict(cls, element: Dict, **kwargs: Dict[str, Any]) -> "BaseAdapter":
        return cls.from_any(element, accessor=lambda el, tr: el[tr], **kwargs)

    @classmethod
    def from_env(cls, **kwargs: Dict) -> "BaseAdapter":
        return cls.from_any(None, accessor=lambda el, tr: os.environ[tr], **kwargs)
