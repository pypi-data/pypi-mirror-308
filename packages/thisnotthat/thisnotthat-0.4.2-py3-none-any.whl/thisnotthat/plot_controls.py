import panel as pn
import param
import pandas as pd
import numpy as np
import numpy.typing as npt
import bokeh.palettes
import bisect

from typing import *


class PlotControlWidget(pn.reactive.Reactive):
    """A Pane that provides access to control various properties of a PlotPane, including the point colour mapping,
    the palette used for colour mapping, the marker size, and the hover text, all based on a dataframe of data 
    associated to points in the plot.
    
    This is particularly useful when data has a vector representation, which has been converted to map representation
    and plotted, but also has a potentially large amount of metadata associated to each sample. This metadata can be 
    formatted in a dataframe, and used to quickly recolour the plot, or resize markers, based on different features
    of the metadata to gain an understanding of how the different metadata features are reflected in the map.

    Parameters
    ----------
    raw_dataframe: DataFrame
        The dataframe of associated metadata. The dataframe should have one row for each point in the plot, in the
        same order as the points in the plot. The ``PlotControlWidget`` will use dtypes of columns and column names
        of this dataframe to populate a variety of selectors that can be linked to a plot.

    scale_type_selector: bool
        Whether to include the ability to select scale types (Linear, Log, or Sqrt) for the numeric
        color-by and marker-size scales.

    width: int or None (optional, default = None)
        The width of the pane. If ``None`` the pane will size itself based on its contents.

    height: int or None (optional, default = None)
        The height of the pane. If ``None`` the pane will size itself based on its contents.

    title: str (optional, default = "#### Plot Controls")
        A title (in markdown) to place at the top of the pane.

    name: str (optional, default = "Plot Controls")
        The panel name of the pane. See panel documentation for more details.
    """

    color_by_vector = param.Series(doc="Color by")
    color_by_palette = param.List([], item_type=str, doc="Color by palette")
    marker_size = param.List([], item_type=float, doc="Marker size")
    hover_text = param.List([], item_type=str, doc="Hover text")
    # color_by_scale = param.ObjectSelector(default="Linear", objects=["Linear", "Log", "Sqrt"], doc="Color-by scale type")
    # marker_size_scale = param.ObjectSelector(default="Linear", objects=["Linear", "Log", "Sqrt"], doc="Marker-size scale type")

    def __init__(
        self,
        raw_dataframe: pd.DataFrame,
        *,
        scale_type_selector: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        title: str = "#### Plot Controls",
        name: str = "Plot Controls",
    ):
        super().__init__(name=name)
        self.dataframe = raw_dataframe

        self.palette_selector = pn.widgets.Select(
            name="Color Palette",
            groups={
                "Default": ["Default palette"],
                "ColorBrewer palettes": list(bokeh.palettes.brewer.keys()),
                "D3 palettes": list(bokeh.palettes.d3.keys()),
                "Smooth palettes": [
                    "Viridis",
                    "Cividis",
                    "Greys",
                    "Inferno",
                    "Magma",
                    "Plasma",
                    "Turbo",
                ],
            },
        )
        self.palette_selector.param.watch(
            self._options_changed, "value", onlychanged=True
        )
        self.color_by_column = pn.widgets.Select(
            name="Color by column", options=["Default"] + list(self.dataframe.columns),
        )
        self.color_by_column.param.watch(
            self._options_changed, "value", onlychanged=True
        )
        self.color_by_scale_selector = pn.Row(
            pn.widgets.StaticText(value="Scale type", align=("end", "center"), margin=(5, 0, 5, 5)),
            pn.widgets.ToggleGroup(
                name="Color by scale", options=["Linear", "Log", "Sqrt"], behavior="radio", value="Linear"
            ),
            margin=(0, 10),
            visible=scale_type_selector
        )
        self.color_by_scale_selector[1].param.watch(self._options_changed, "value", onlychanged=True)
        self.hover_text_column = pn.widgets.Select(
            name="Hover text column",
            options=["Default"] + list(self.dataframe.columns),
        )
        self.hover_text_column.param.watch(
            self._options_changed, "value", onlychanged=True
        )
        self.marker_size_column = pn.widgets.Select(
            name="Marker size column",
            options=["Default"]
            + list(self.dataframe.select_dtypes(include="number").columns),
        )
        self.marker_size_column.param.watch(
            self._options_changed, "value", onlychanged=True
        )
        self.marker_size_scale_selector = pn.Row(
            pn.widgets.StaticText(value="Scale type", align=("end", "center"), margin=(5, 0, 5, 5)),
            pn.widgets.ToggleGroup(
                name="Marker size scale", options=["Linear", "Log", "Sqrt"], behavior="radio", value="Linear"
            ),
            margin=(0, 5,  0, 10),
            visible=scale_type_selector
        )
        self.marker_size_scale_selector[1].param.watch(self._options_changed, "value", onlychanged=True)
        self.apply_changes = pn.widgets.Button(
            name="Apply Changes", button_type="success", disabled=True,
        )
        self.apply_changes.on_click(self._reapply_changes)
        self.bad_scaling_alert = pn.pane.Alert(
            "### Bad scale\nColumn with Log or Sqrt scale contains negative values; Using a linear scale",
            alert_type="danger",
            visible=False,
        )
        self.pane = pn.WidgetBox(
            title,
            pn.layout.Divider(margin=(0, 10, 10, 10), height=5),
            self.palette_selector,
            self.color_by_column,
            self.color_by_scale_selector,
            pn.layout.Divider(margin=(0, 10, 10, 10), height=5),
            self.marker_size_column,
            self.marker_size_scale_selector,
            pn.layout.Divider(margin=(0, 10, 10, 10), height=5),
            self.hover_text_column,
            pn.layout.Divider(margin=(0, 10, 10, 10), height=5),
            self.apply_changes,
            self.bad_scaling_alert,
            width=width,
            height=height,
        )

    def _get_model(self, *args, **kwds):
        return self.pane._get_model(*args, **kwds)

    def _options_changed(self, event) -> None:
        self.apply_changes.disabled = False
        self.bad_scaling_alert.visible = False

    def _change_palette(self):
        if pd.api.types.is_numeric_dtype(self.color_by_vector):
            # Continuous scale required
            if (
                self.palette_selector.value
                in self.palette_selector.groups["Smooth palettes"]
            ):
                palette_name = self.palette_selector.value + "256"
                self.color_by_palette = list(getattr(bokeh.palettes, palette_name))
            elif (
                self.palette_selector.value
                in self.palette_selector.groups["ColorBrewer palettes"]
            ):
                palette_dict = bokeh.palettes.brewer[self.palette_selector.value]
                max_palette_size = max(palette_dict.keys())
                palette = palette_dict[max_palette_size]
                self.color_by_palette = list(palette)
            elif (
                self.palette_selector.value
                in self.palette_selector.groups["D3 palettes"]
            ):
                palette_dict = bokeh.palettes.d3[self.palette_selector.value]
                max_palette_size = max(palette_dict.keys())
                palette = palette_dict[max_palette_size]
                self.color_by_palette = list(palette)
            else:
                raise ValueError("Palette option not in a valid palette group")
        else:
            # Discrete scale required
            n_colors_required = self.dataframe[self.color_by_column.value].nunique()
            if n_colors_required > 256:
                n_colors_required = 256

            if (
                self.palette_selector.value
                in self.palette_selector.groups["Smooth palettes"]
            ):
                palette_name = self.palette_selector.value + "256"
                raw_palette = getattr(bokeh.palettes, palette_name)
                palette = bokeh.palettes.linear_palette(raw_palette, n_colors_required)
                self.color_by_palette = list(palette)
            elif (
                self.palette_selector.value
                in self.palette_selector.groups["ColorBrewer palettes"]
            ):
                palette_dict = bokeh.palettes.brewer[self.palette_selector.value]
                palette_sizes = sorted(list(palette_dict.keys()))

                if n_colors_required <= max(palette_sizes):
                    best_size_index = bisect.bisect_left(
                        palette_sizes, n_colors_required
                    )
                    palette = palette_dict[palette_sizes[best_size_index]]
                else:
                    max_size = max(palette_sizes)
                    n_copies = (n_colors_required // max_size) + 1
                    palette = palette_dict[max_size] * n_copies

                self.color_by_palette = list(palette)
            elif (
                self.palette_selector.value
                in self.palette_selector.groups["D3 palettes"]
            ):
                palette_dict = bokeh.palettes.d3[self.palette_selector.value]
                palette_sizes = sorted(list(palette_dict.keys()))

                if n_colors_required <= max(palette_sizes):
                    best_size_index = bisect.bisect_left(
                        palette_sizes, n_colors_required
                    )
                    palette = palette_dict[palette_sizes[best_size_index]]
                else:
                    max_size = max(palette_sizes)
                    n_copies = (n_colors_required // max_size) + 1
                    palette = palette_dict[max_size] * n_copies

                self.color_by_palette = list(palette)
            else:
                raise ValueError("Palette option not in a valid palette group")

    def _apply_changes(self, event) -> None:
        if self.color_by_column.value == "Default":
            self.color_by_vector = pd.Series([])
        else:
            values = self.dataframe[self.color_by_column.value]
            if pd.api.types.is_numeric_dtype(values):
                if self.color_by_scale_selector[1].value == "Log":
                    if np.any(values <= 0):
                        self.bad_scaling_alert.visible = True
                        self.color_by_vector = values
                    else:
                        self.color_by_vector = pd.Series(np.log(values))
                elif self.color_by_scale_selector[1].value == "Sqrt":
                    if np.any(values < 0):
                        self.bad_scaling_alert.visible = True
                        self.color_by_vector = values
                    else:
                        self.color_by_vector = pd.Series(np.sqrt(values))
                else:
                    self.color_by_vector = values
            else:
                self.color_by_vector = values

        if self.palette_selector.value == "Default palette":
            self.color_by_palette = []
        else:
            self._change_palette()

        if self.hover_text_column.value == "Default":
            self.hover_text = []
        else:
            self.hover_text = (
                self.dataframe[self.hover_text_column.value].map(str).to_list()
            )

        if self.marker_size_column.value == "Default":
            self.marker_size = []
        else:
            if self.marker_size_scale_selector[1].value == "Log":
                values = self.dataframe[self.marker_size_column.value]
                if np.any(values <= 0):
                    self.bad_scaling_alert.visible = True
                    self.marker_size = values.to_list()
                else:
                    self.marker_size = np.log(values).to_list()
            elif self.marker_size_scale_selector[1].value == "Sqrt":
                values = self.dataframe[self.marker_size_column.value]
                if np.any(values < 0):
                    self.bad_scaling_alert.visible = True
                    self.marker_size = values.to_list()
                else:
                    self.marker_size = np.sqrt(values).to_list()
            else: # Linear scale
                self.marker_size = self.dataframe[self.marker_size_column.value].to_list()

        self.apply_changes.disabled = True

    # I have no idea why, but this fixes issues with marker size changes in plots. Don't ask
    def _reapply_changes(self, event):
        self._apply_changes(None)
        self._apply_changes(None)

    def link_to_plot(self, plot):
        """Link this pane to a plot pane using a default set of params that can sensibly be linked.

        Parameters
        ----------
        plot: PlotPane
            The plot pane to link to.

        Returns
        -------
        link:
            The link object.
        """
        return self.link(
            plot,
            color_by_vector="color_by_vector",
            color_by_palette="color_by_palette",
            hover_text="hover_text",
            marker_size="marker_size",
            bidirectional=True,
        )
