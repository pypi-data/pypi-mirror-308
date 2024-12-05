# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/archetypes/line_strips2d.fbs".

# You can extend this class by creating a "LineStrips2DExt" class in "line_strips2d_ext.py".

from __future__ import annotations

from typing import Any

from attrs import define, field

from .. import components, datatypes
from .._baseclasses import (
    Archetype,
)
from ..error_utils import catch_and_log_exceptions

__all__ = ["LineStrips2D"]


@define(str=False, repr=False, init=False)
class LineStrips2D(Archetype):
    """
    **Archetype**: 2D line strips with positions and optional colors, radii, labels, etc.

    Examples
    --------
    ### `line_strip2d_batch`:
    ```python
    import rerun as rr
    import rerun.blueprint as rrb

    rr.init("rerun_example_line_strip2d_batch", spawn=True)

    rr.log(
        "strips",
        rr.LineStrips2D(
            [
                [[0, 0], [2, 1], [4, -1], [6, 0]],
                [[0, 3], [1, 4], [2, 2], [3, 4], [4, 2], [5, 4], [6, 3]],
            ],
            colors=[[255, 0, 0], [0, 255, 0]],
            radii=[0.025, 0.005],
            labels=["one strip here", "and one strip there"],
        ),
    )

    # Set view bounds:
    rr.send_blueprint(rrb.Spatial2DView(visual_bounds=rrb.VisualBounds2D(x_range=[-1, 7], y_range=[-3, 6])))
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/line_strip2d_batch/c6f4062bcf510462d298a5dfe9fdbe87c754acee/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/line_strip2d_batch/c6f4062bcf510462d298a5dfe9fdbe87c754acee/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/line_strip2d_batch/c6f4062bcf510462d298a5dfe9fdbe87c754acee/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/line_strip2d_batch/c6f4062bcf510462d298a5dfe9fdbe87c754acee/1200w.png">
      <img src="https://static.rerun.io/line_strip2d_batch/c6f4062bcf510462d298a5dfe9fdbe87c754acee/full.png" width="640">
    </picture>
    </center>

    ### Lines with scene & UI radius each:
    ```python
    import rerun as rr

    rr.init("rerun_example_line_strip3d_ui_radius", spawn=True)

    # A blue line with a scene unit radii of 0.01.
    points = [[0, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 1]]
    rr.log(
        "scene_unit_line",
        rr.LineStrips3D(
            [points],
            # By default, radii are interpreted as world-space units.
            radii=0.01,
            colors=[0, 0, 255],
        ),
    )

    # A red line with a ui point radii of 5.
    # UI points are independent of zooming in Views, but are sensitive to the application UI scaling.
    # For 100% ui scaling, UI points are equal to pixels.
    points = [[3, 0, 0], [3, 0, 1], [4, 0, 0], [4, 0, 1]]
    rr.log(
        "ui_points_line",
        rr.LineStrips3D(
            [points],
            # rr.Radius.ui_points produces radii that the viewer interprets as given in ui points.
            radii=rr.Radius.ui_points(5.0),
            colors=[255, 0, 0],
        ),
    )
    ```

    """

    def __init__(
        self: Any,
        strips: components.LineStrip2DArrayLike,
        *,
        radii: datatypes.Float32ArrayLike | None = None,
        colors: datatypes.Rgba32ArrayLike | None = None,
        labels: datatypes.Utf8ArrayLike | None = None,
        show_labels: datatypes.BoolLike | None = None,
        draw_order: datatypes.Float32Like | None = None,
        class_ids: datatypes.ClassIdArrayLike | None = None,
    ):
        """
        Create a new instance of the LineStrips2D archetype.

        Parameters
        ----------
        strips:
            All the actual 2D line strips that make up the batch.
        radii:
            Optional radii for the line strips.
        colors:
            Optional colors for the line strips.
        labels:
            Optional text labels for the line strips.

            If there's a single label present, it will be placed at the center of the entity.
            Otherwise, each instance will have its own label.
        show_labels:
            Optional choice of whether the text labels should be shown by default.
        draw_order:
            An optional floating point value that specifies the 2D drawing order of each line strip.

            Objects with higher values are drawn on top of those with lower values.
        class_ids:
            Optional [`components.ClassId`][rerun.components.ClassId]s for the lines.

            The [`components.ClassId`][rerun.components.ClassId] provides colors and labels if not specified explicitly.

        """

        # You can define your own __init__ function as a member of LineStrips2DExt in line_strips2d_ext.py
        with catch_and_log_exceptions(context=self.__class__.__name__):
            self.__attrs_init__(
                strips=strips,
                radii=radii,
                colors=colors,
                labels=labels,
                show_labels=show_labels,
                draw_order=draw_order,
                class_ids=class_ids,
            )
            return
        self.__attrs_clear__()

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            strips=None,  # type: ignore[arg-type]
            radii=None,  # type: ignore[arg-type]
            colors=None,  # type: ignore[arg-type]
            labels=None,  # type: ignore[arg-type]
            show_labels=None,  # type: ignore[arg-type]
            draw_order=None,  # type: ignore[arg-type]
            class_ids=None,  # type: ignore[arg-type]
        )

    @classmethod
    def _clear(cls) -> LineStrips2D:
        """Produce an empty LineStrips2D, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    strips: components.LineStrip2DBatch = field(
        metadata={"component": "required"},
        converter=components.LineStrip2DBatch._required,  # type: ignore[misc]
    )
    # All the actual 2D line strips that make up the batch.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    radii: components.RadiusBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.RadiusBatch._optional,  # type: ignore[misc]
    )
    # Optional radii for the line strips.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    colors: components.ColorBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ColorBatch._optional,  # type: ignore[misc]
    )
    # Optional colors for the line strips.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    labels: components.TextBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.TextBatch._optional,  # type: ignore[misc]
    )
    # Optional text labels for the line strips.
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

    draw_order: components.DrawOrderBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.DrawOrderBatch._optional,  # type: ignore[misc]
    )
    # An optional floating point value that specifies the 2D drawing order of each line strip.
    #
    # Objects with higher values are drawn on top of those with lower values.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    class_ids: components.ClassIdBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ClassIdBatch._optional,  # type: ignore[misc]
    )
    # Optional [`components.ClassId`][rerun.components.ClassId]s for the lines.
    #
    # The [`components.ClassId`][rerun.components.ClassId] provides colors and labels if not specified explicitly.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
