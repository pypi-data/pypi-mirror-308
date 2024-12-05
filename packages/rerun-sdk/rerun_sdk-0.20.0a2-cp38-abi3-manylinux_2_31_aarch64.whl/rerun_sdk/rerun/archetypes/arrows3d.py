# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/archetypes/arrows3d.fbs".

# You can extend this class by creating a "Arrows3DExt" class in "arrows3d_ext.py".

from __future__ import annotations

from attrs import define, field

from .. import components
from .._baseclasses import (
    Archetype,
)
from .arrows3d_ext import Arrows3DExt

__all__ = ["Arrows3D"]


@define(str=False, repr=False, init=False)
class Arrows3D(Arrows3DExt, Archetype):
    """
    **Archetype**: 3D arrows with optional colors, radii, labels, etc.

    Example
    -------
    ### Simple batch of 3D arrows:
    ```python
    from math import tau

    import numpy as np
    import rerun as rr

    rr.init("rerun_example_arrow3d", spawn=True)

    lengths = np.log2(np.arange(0, 100) + 1)
    angles = np.arange(start=0, stop=tau, step=tau * 0.01)
    origins = np.zeros((100, 3))
    vectors = np.column_stack([np.sin(angles) * lengths, np.zeros(100), np.cos(angles) * lengths])
    colors = [[1.0 - c, c, 0.5, 0.5] for c in angles / tau]

    rr.log("arrows", rr.Arrows3D(origins=origins, vectors=vectors, colors=colors))
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/arrow3d_simple/55e2f794a520bbf7527d7b828b0264732146c5d0/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/arrow3d_simple/55e2f794a520bbf7527d7b828b0264732146c5d0/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/arrow3d_simple/55e2f794a520bbf7527d7b828b0264732146c5d0/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/arrow3d_simple/55e2f794a520bbf7527d7b828b0264732146c5d0/1200w.png">
      <img src="https://static.rerun.io/arrow3d_simple/55e2f794a520bbf7527d7b828b0264732146c5d0/full.png" width="640">
    </picture>
    </center>

    """

    # __init__ can be found in arrows3d_ext.py

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            vectors=None,  # type: ignore[arg-type]
            origins=None,  # type: ignore[arg-type]
            radii=None,  # type: ignore[arg-type]
            colors=None,  # type: ignore[arg-type]
            labels=None,  # type: ignore[arg-type]
            show_labels=None,  # type: ignore[arg-type]
            class_ids=None,  # type: ignore[arg-type]
        )

    @classmethod
    def _clear(cls) -> Arrows3D:
        """Produce an empty Arrows3D, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    vectors: components.Vector3DBatch = field(
        metadata={"component": "required"},
        converter=components.Vector3DBatch._required,  # type: ignore[misc]
    )
    # All the vectors for each arrow in the batch.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    origins: components.Position3DBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.Position3DBatch._optional,  # type: ignore[misc]
    )
    # All the origin (base) positions for each arrow in the batch.
    #
    # If no origins are set, (0, 0, 0) is used as the origin for each arrow.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    radii: components.RadiusBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.RadiusBatch._optional,  # type: ignore[misc]
    )
    # Optional radii for the arrows.
    #
    # The shaft is rendered as a line with `radius = 0.5 * radius`.
    # The tip is rendered with `height = 2.0 * radius` and `radius = 1.0 * radius`.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    colors: components.ColorBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ColorBatch._optional,  # type: ignore[misc]
    )
    # Optional colors for the points.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    labels: components.TextBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.TextBatch._optional,  # type: ignore[misc]
    )
    # Optional text labels for the arrows.
    #
    # If there's a single label present, it will be placed at the center of the entity.
    # Otherwise, each instance will have its own label.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    show_labels: components.ShowLabelsBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ShowLabelsBatch._optional,  # type: ignore[misc]
    )
    # Optional choice of whether the text labels should be shown by default.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    class_ids: components.ClassIdBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ClassIdBatch._optional,  # type: ignore[misc]
    )
    # Optional class Ids for the points.
    #
    # The [`components.ClassId`][rerun.components.ClassId] provides colors and labels if not specified explicitly.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
