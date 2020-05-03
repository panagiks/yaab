import warnings

from contextlib import suppress
from dataclasses import fields
from distutils.util import strtobool
from typing import Any, Callable, ClassVar, Dict, Optional, Tuple


class DictMixin:
    """
    A Mixin that provides dict-like behavior for Dataclasses.
    """

    __slots__ = tuple()

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key) from None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        warnings.warn(
            "Deleting a Dataclass' field! This can cause unexpected behavior "
            "when invoking the Dataclass' representation, comparisson or other "
            "function which may 'automatically' utilize this field!",
            SyntaxWarning,
        )
        try:
            delattr(self, key)
        except AttributeError:
            raise KeyError(key) from None

    def keys(self):
        return (obj_field.name for obj_field in fields(self))


class FieldMetaConverterMixin:
    """
    A Mixin that provides field conversions based on the provided field metadata.
    """

    __slots__ = tuple()
    _meta_cnv: ClassVar[str] = "converter"

    def __post_init__(self):
        for obj_field in fields(self):
            field_name = obj_field.name
            with suppress(KeyError):
                converter = obj_field.metadata[self._meta_cnv]
                setattr(self, field_name, converter(getattr(self, field_name)))


class FieldTypeConverterMixin:
    """
    A Mixin that provides field conversions based on the field type.
    """

    __slots__ = tuple()
    _extra_cnv: ClassVar[Dict[Tuple[Any, Any], Callable[[Any], Any]]] = {
        (str, bool): lambda x: bool(strtobool(x)),
    }

    def __post_init__(self):
        for obj_field in fields(self):
            if not obj_field.metadata.get("convert"):
                continue
            field_name = obj_field.name
            field_type = obj_field.type
            value = getattr(self, field_name)
            if isinstance(value, field_type):
                continue
            true_type = type(value)
            converter = self._extra_cnv.get((true_type, field_type))
            if converter is not None:
                value = converter(value)
            else:
                value = field_type(value)
            setattr(self, field_name, value)
