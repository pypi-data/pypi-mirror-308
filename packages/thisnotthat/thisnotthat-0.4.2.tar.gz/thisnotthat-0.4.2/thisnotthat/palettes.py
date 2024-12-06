from matplotlib.colors import rgb2hex
import matplotlib
import matplotlib.cm
import colorcet
import glasbey
import cmocean

try:
    import seaborn

    _HAVE_SEABORN = True
except ImportError:
    _HAVE_SEABORN = False

import bokeh.palettes

from typing import *

from numpy import linspace
from string import capwords
from .utils import _palette_index

_ALT_NAMES = {}
for full_name in colorcet.aliases:
    for alias in colorcet.aliases[full_name]:
        _ALT_NAMES[alias] = full_name

# different versions of matplotlib handle things differently
if hasattr(matplotlib.cm, "_cmap_registry"):
    _mpl_colormaps = matplotlib.cm._cmap_registry
else:
    _mpl_colormaps = matplotlib.colormaps
    _mpl_color_sequences = matplotlib.color_sequences

all_palettes = set(
    colorcet.all_original_names()
    + list(_mpl_colormaps.keys())
    + list(bokeh.palettes.all_palettes.keys())
)

suggested_categorical_palettes = (
    "glasbey_category10",
    "tab10",
    "Set1",
    "glasbey",
)

suggested_continuous_palettes = (
    "viridis",
    "magma",
    "gouldian",
    "fire",
    "mako",
    "rocket",
    "haline",
    "spectral",
)

def get_palette(name: str, length: Optional[int] = None, extend: bool = True, scrambled: bool = False):

    if name in _ALT_NAMES:
        name = _ALT_NAMES[name]

    if name in colorcet.all_original_names():
        if length is None:
            palette = [rgb2hex(c) for c in getattr(colorcet, name)]
        elif "glasbey" in name:
            palette = [rgb2hex(c) for c in getattr(colorcet, name)[:length]]
        else:
            palette = getattr(colorcet, name)
            palette = [rgb2hex(palette[int(x)]) for x in linspace(0, 255, length)]

    elif (
        name in _mpl_colormaps
        or f"cmo.{name}" in _mpl_colormaps
        or capwords(name) in _mpl_colormaps
    ):  # Matplotlib cmap

        if f"cmo.{name}" in _mpl_colormaps:
            name = f"cmo.{name}"

        if capwords(name) in _mpl_colormaps:
            name = capwords(name)

        if length is None:
            mpl_palette = _mpl_colormaps[name]
        elif len(getattr(_mpl_colormaps[name], "colors", [0] * 256)) < length:
            mpl_palette = _mpl_colormaps[name]
        else:
            mpl_palette = matplotlib.cm._cmap_registry[name]._resample(length)

        if hasattr(mpl_palette, "colors"):
            palette = [rgb2hex(c) for c in mpl_palette.colors]
        elif hasattr(mpl_palette, "_lut"):
            palette = [rgb2hex(c) for c in mpl_palette._lut[:-3]]
        else:
            palette = [
                rgb2hex(c)
                for c in mpl_palette(
                    linspace(0, 1, length if length is not None else 256)
                )
            ]

        if len(palette) < length and extend:
            palette = glasbey.extend_palette(palette, palette_size=length, as_hex=True)

    elif (
        name in bokeh.palettes.all_palettes
        or capwords(name) in bokeh.palettes.all_palettes
    ):  # Bokeh palette

        if capwords(name) in bokeh.palettes.all_palettes:
            name = capwords(name)

        bokeh_palette_options = bokeh.palettes.all_palettes[name]
        if length in bokeh_palette_options:
            palette = bokeh_palette_options[length]
        elif length < min(bokeh_palette_options):
            palette = bokeh_palette_options[min(bokeh_palette_options)][:length]
        elif length < max(bokeh_palette_options):
            full_bokeh_palette = bokeh_palette_options[max(bokeh_palette_options)]
            palette = [
                full_bokeh_palette[int(round(x))]
                for x in linspace(0, len(full_bokeh_palette), length)
            ]
        elif extend:
            full_bokeh_palette = bokeh_palette_options[max(bokeh_palette_options)]
            palette = glasbey.extend_palette(full_bokeh_palette, palette_size=length)
        else:  # Try to match matplotlib resampling
            full_bokeh_palette = bokeh_palette_options[max(bokeh_palette_options)]
            palette = [
                full_bokeh_palette[int(round(x))]
                for x in linspace(0, len(full_bokeh_palette), length)
            ]
    else:
        raise ValueError("Unrecognized palette {name}. Try a name from {all_palettes}")

    if scrambled:
        palette = [palette[x] for x in _palette_index(len(palette))]

    return palette
