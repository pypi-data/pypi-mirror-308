# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/components/tensor_dimension_selection.fbs".

# You can extend this class by creating a "TensorDimensionIndexSelectionExt" class in "tensor_dimension_index_selection_ext.py".

from __future__ import annotations

from .. import datatypes
from .._baseclasses import (
    ComponentBatchMixin,
    ComponentMixin,
)

__all__ = ["TensorDimensionIndexSelection", "TensorDimensionIndexSelectionBatch", "TensorDimensionIndexSelectionType"]


class TensorDimensionIndexSelection(datatypes.TensorDimensionIndexSelection, ComponentMixin):
    """**Component**: Specifies a concrete index on a tensor dimension."""

    _BATCH_TYPE = None
    # You can define your own __init__ function as a member of TensorDimensionIndexSelectionExt in tensor_dimension_index_selection_ext.py

    # Note: there are no fields here because TensorDimensionIndexSelection delegates to datatypes.TensorDimensionIndexSelection
    pass


class TensorDimensionIndexSelectionType(datatypes.TensorDimensionIndexSelectionType):
    _TYPE_NAME: str = "rerun.components.TensorDimensionIndexSelection"


class TensorDimensionIndexSelectionBatch(datatypes.TensorDimensionIndexSelectionBatch, ComponentBatchMixin):
    _ARROW_TYPE = TensorDimensionIndexSelectionType()


# This is patched in late to avoid circular dependencies.
TensorDimensionIndexSelection._BATCH_TYPE = TensorDimensionIndexSelectionBatch  # type: ignore[assignment]
