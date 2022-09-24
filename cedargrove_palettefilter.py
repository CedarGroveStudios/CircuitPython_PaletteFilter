# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_palettefilter`
================================================================================

PaletteFilter is a CircuitPython helper class for replacing color index values
in a `displayio.Palette` object. A target color along with a tolerance parameter
determine the range of color values to be replaced. The class creates a new
palette object with the changes. The replacement color value (or `None` for
transparency) is substituted for the original palette entry and placed into the
new palette object, `PaletteFilter.palette`.

The filter uses a linear Euclidean comparison incorporating vision perception
('redmean') approximation to test palette color values with the specified
target color. https://en.wikipedia.org/wiki/Color_difference

For comparing a single color value, use the
`cedargrove_palettefilter.compare_colors() helper` function.

cedargrove_palettefilter.py v1.0.0 2022-09-22

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  <https://circuitpython.org/downloads>

"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_PaletteFilter.git"


import math
import displayio


class PaletteFilter:
    """Creates a displayio palette object, PaletteFilter.palette, updated with
    new palette values based upon a target color and a specified comparison
    tolerance parameter."""

    # pylint: disable = (too-many-arguments)
    def __init__(
        self, source_palette, target_color, fill_color=None, tolerance=0, invert=False
    ):
        """Instantiate the PaletteFilter class.

        :param displayio.Palette source_palette: The displayio source palette
          object. No default.
        :param int target_color: The 24-bit RGB color value to be replaced.
          No default.
        :param union(int, None) fill_color: The 24-bit RGB replacement
          color value. Defaults to None for transparent.
        :param float tolerance: The difference value used to detect color
          similarity. Value range is 0 to 765; 0 detects a single color.
          Default is 0 (makes one color transparent across the palette).
        :param bool invert: Inverts the color comparison logic so that only
          colors outside of the target color range will be changed.
          Default is False."""

        self._src_palette = source_palette
        self._target_color = target_color
        self._fill_color = fill_color
        self._tolerance = tolerance
        self._invert = invert

        # Create the result palette
        self.filter_palette()

    @property
    def tolerance(self):
        """The color shade value difference tolerance."""
        return self._tolerance

    @tolerance.setter
    def tolerance(self, new_tolerance):
        if self._tolerance != new_tolerance:
            self._tolerance = new_tolerance
            self.filter_palette()

    @property
    def target_color(self):
        """The target color value to be replaced."""
        return self._target_color

    @target_color.setter
    def target_color(self, new_target_color):
        if self._target_color != new_target_color:
            self._target_color = new_target_color
            self.filter_palette()

    @property
    def fill_color(self):
        """The replacement color value or transparent (None)."""
        return self._fill_color

    @fill_color.setter
    def fill_color(self, new_fill_color):
        if self._fill_color != new_fill_color:
            self._fill_color = new_fill_color
            self.filter_palette()

    @property
    def invert(self):
        """The fill inversion state."""
        return self._invert

    @property
    def palette(self):
        """The resultant displayio palette."""
        return self._new_palette

    # pylint: disable = (no-self-use)
    def rgb_splitter(self, color):
        """Separates 24-bit RGB color into three 8-bit component values.

        :param int color: The 24-bit RGB color value input. No default."""

        return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

    # pylint: disable = (too-many-locals)
    def compare_colors(self, color_1, color_2, tolerance, invert):
        """Compares a two colors. If the color value difference is within the
        tolerance band of the reference, the method returns True.

        :param int color_1: The 24-bit RGB color value to be tested.
          No default.
        :param int color_2: The reference 24-bit RGB color value.
          No default.
        :param float tolerance: The difference value used to detect color
          similarity. Value range is 0 to 765. Default is 0 (detects a single
          color value).
        :param bool invert: Inverts the color comparison logic so that only
          colors outside of the target color range will be changed.
          Default is False."""

        r_1, g_1, b_1 = self.rgb_splitter(color_1)
        r_2, g_2, b_2 = self.rgb_splitter(color_2)

        delta_r_2 = (r_1 - r_2) ** 2
        delta_g_2 = (g_1 - g_2) ** 2
        delta_b_2 = (b_1 - b_2) ** 2
        avg_r = (1 / 2) * (r_1 + r_2)

        delta_color = math.sqrt(
            ((2 + (avg_r / 256)) * delta_r_2)
            + (4 * delta_g_2)
            + ((2 + ((255 - avg_r) / 256)) * delta_b_2)
        )

        return bool(delta_color <= tolerance) ^ invert

    def filter_palette(self):
        """The primary function of the PaletteFilter class. Uses the
        current tolerance parameter to examine the source palette to find
        color values within the tolerance parameter range. A new palette is
        created using the fill color value or transparent. Source palette
        is not modified. Source palette transparency values are not transferred
        to the resultant palette."""

        # Create a new palette
        self._new_palette = displayio.Palette(len(self._src_palette))

        # Build the new palette with source palette colors
        for index, color in enumerate(self._src_palette):
            self._new_palette[index] = color
            if self.compare_colors(
                self._new_palette[index],
                self._target_color,
                self._tolerance,
                self._invert,
            ):
                # Source palette color is within the tolerance range; replace it
                if self._fill_color is not None:
                    # Set current index with fill color
                    self._new_palette[index] = self._fill_color
                else:
                    # Fill color is None; set current index to be transparent
                    self._new_palette.make_transparent(index)
