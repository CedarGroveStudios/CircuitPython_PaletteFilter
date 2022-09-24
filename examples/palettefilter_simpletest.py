# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`palettefilter_simpletest.py`
================================================================================

* Author(s): JG

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import displayio
from cedargrove_palettefilter import PaletteFilter

_version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_PaletteFilter.git"

# Define the transparent color and tolerance values
TARGET_COLOR = 0x080808
FILL_COLOR = None
TOLERANCE = 4

# Make a displayio palette and set value(s) to transparent
SOURCE_COLORS = [
    0x000000,
    0x010101,
    0x020202,
    0x030303,
    0x040404,
    0x050505,
    0x060606,
    0x070707,
    0x080808,
    0x090909,
]
SOURCE_PALETTE = displayio.Palette(len(SOURCE_COLORS))
for index, color in enumerate(SOURCE_COLORS):
    SOURCE_PALETTE[index] = SOURCE_COLORS[index]

# Set a source palette value to transparent
SOURCE_PALETTE.make_transparent(3)

# Instantiate paletteFilter
palette_filter = PaletteFilter(SOURCE_PALETTE, TARGET_COLOR, FILL_COLOR, TOLERANCE)
print(f"target_color: {hex(palette_filter.target_color)}")

print("------")
print("source palette:")
print("index, color, transparency")
for index, color in enumerate(SOURCE_PALETTE):
    print(index, hex(color), SOURCE_PALETTE.is_transparent(index))

print("------")
print("new palette:")
print("index, color, transparency")
for index, color in enumerate(palette_filter.palette):
    print(index, hex(color), palette_filter.palette.is_transparent(index))

while True:
    pass
