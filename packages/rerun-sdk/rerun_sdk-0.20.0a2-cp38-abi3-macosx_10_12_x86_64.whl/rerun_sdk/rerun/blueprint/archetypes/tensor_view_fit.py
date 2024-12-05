# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/archetypes/tensor_view_fit.fbs".

# You can extend this class by creating a "TensorViewFitExt" class in "tensor_view_fit_ext.py".

from __future__ import annotations

from attrs import define, field

from ..._baseclasses import (
    Archetype,
)
from ...blueprint import components as blueprint_components
from .tensor_view_fit_ext import TensorViewFitExt

__all__ = ["TensorViewFit"]


@define(str=False, repr=False, init=False)
class TensorViewFit(TensorViewFitExt, Archetype):
    """**Archetype**: Configures how a selected tensor slice is shown on screen."""

    # __init__ can be found in tensor_view_fit_ext.py

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            scaling=None,  # type: ignore[arg-type]
        )

    @classmethod
    def _clear(cls) -> TensorViewFit:
        """Produce an empty TensorViewFit, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    scaling: blueprint_components.ViewFitBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=blueprint_components.ViewFitBatch._optional,  # type: ignore[misc]
    )
    # How the image is scaled to fit the view.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
