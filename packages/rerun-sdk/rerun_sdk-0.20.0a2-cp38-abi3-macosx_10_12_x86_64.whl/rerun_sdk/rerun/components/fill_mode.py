# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/components/fill_mode.fbs".

# You can extend this class by creating a "FillModeExt" class in "fill_mode_ext.py".

from __future__ import annotations

from typing import Literal, Sequence, Union

import pyarrow as pa

from .._baseclasses import (
    BaseBatch,
    BaseExtensionType,
    ComponentBatchMixin,
)

__all__ = ["FillMode", "FillModeArrayLike", "FillModeBatch", "FillModeLike", "FillModeType"]


from enum import Enum


class FillMode(Enum):
    """**Component**: How a geometric shape is drawn and colored."""

    MajorWireframe = 1
    """
    Lines are drawn around the parts of the shape which directly correspond to the logged data.

    Examples of what this means:

    * An [`archetypes.Ellipsoids3D`][rerun.archetypes.Ellipsoids3D] will draw three axis-aligned ellipses that are cross-sections
      of each ellipsoid, each of which displays two out of three of the sizes of the ellipsoid.
    * For [`archetypes.Boxes3D`][rerun.archetypes.Boxes3D], it is the edges of the box, identical to `DenseWireframe`.
    """

    DenseWireframe = 2
    """
    Many lines are drawn to represent the surface of the shape in a see-through fashion.

    Examples of what this means:

    * An [`archetypes.Ellipsoids3D`][rerun.archetypes.Ellipsoids3D] will draw a wireframe triangle mesh that approximates each
      ellipsoid.
    * For [`archetypes.Boxes3D`][rerun.archetypes.Boxes3D], it is the edges of the box, identical to `MajorWireframe`.
    """

    Solid = 3
    """The surface of the shape is filled in with a solid color. No lines are drawn."""

    @classmethod
    def auto(cls, val: str | int | FillMode) -> FillMode:
        """Best-effort converter, including a case-insensitive string matcher."""
        if isinstance(val, FillMode):
            return val
        if isinstance(val, int):
            return cls(val)
        try:
            return cls[val]
        except KeyError:
            val_lower = val.lower()
            for variant in cls:
                if variant.name.lower() == val_lower:
                    return variant
        raise ValueError(f"Cannot convert {val} to {cls.__name__}")

    def __str__(self) -> str:
        """Returns the variant name."""
        return self.name


FillModeLike = Union[
    FillMode, Literal["DenseWireframe", "MajorWireframe", "Solid", "densewireframe", "majorwireframe", "solid"], int
]
FillModeArrayLike = Union[FillModeLike, Sequence[FillModeLike]]


class FillModeType(BaseExtensionType):
    _TYPE_NAME: str = "rerun.components.FillMode"

    def __init__(self) -> None:
        pa.ExtensionType.__init__(self, pa.uint8(), self._TYPE_NAME)


class FillModeBatch(BaseBatch[FillModeArrayLike], ComponentBatchMixin):
    _ARROW_TYPE = FillModeType()

    @staticmethod
    def _native_to_pa_array(data: FillModeArrayLike, data_type: pa.DataType) -> pa.Array:
        if isinstance(data, (FillMode, int, str)):
            data = [data]

        pa_data = [FillMode.auto(v).value if v is not None else None for v in data]  # type: ignore[redundant-expr]

        return pa.array(pa_data, type=data_type)
