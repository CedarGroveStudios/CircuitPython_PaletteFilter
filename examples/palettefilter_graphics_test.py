# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`palettefilter_graphics_test.py`
================================================================================

* Author(s): JG

Implementation Notes
--------------------

**Hardware:**
Adafruit PyPortal

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""
import terminalio
import board
import displayio
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from cedargrove_palettefilter import PaletteFilter

_version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_PaletteFilter.git"

# Define a couple of display parameter values
BRIGHTNESS = 0.5  # 0.01 for camera
ROTATION = 0
BACKGROUND_COLOR = None
DISPLAY_SCALE = 1

# Define the transparent color and tolerance values
IMAGE_FILE = "/flying_lars.bmp"
TARGET_COLOR = 0x00FF00
FILL_COLOR = None
TOLERANCE = 1
INVERT = False


# Instantiate the display
display = board.DISPLAY
display.brightness = BRIGHTNESS
display.rotation = ROTATION

primary_disp_layer = displayio.Group(scale=DISPLAY_SCALE)
display.show(primary_disp_layer)

bkg_block = Rect(x=200, y=80, width=80, height=60, fill=BACKGROUND_COLOR)
primary_disp_layer.append(bkg_block)

bitmap, SOURCE_PALETTE = adafruit_imageload.load(
    IMAGE_FILE, bitmap=displayio.Bitmap, palette=displayio.Palette
)

tile_grid = displayio.TileGrid(bitmap, pixel_shader=SOURCE_PALETTE)
primary_disp_layer.append(tile_grid)

target_label = Label(terminalio.FONT, text="TARGET", color=0xFFFFFF)
target_label.anchor_point = (1.0, 0.5)
target_label.anchored_position = (48, 225)
target_block = Rect(x=50, y=240 - 35, width=30, height=30, fill=TARGET_COLOR)
primary_disp_layer.append(target_block)
primary_disp_layer.append(target_label)

fill_label = Label(terminalio.FONT, text="FILL", color=0xFFFFFF)
fill_label.anchor_point = (1.0, 0.5)
fill_label.anchored_position = (118, 225)
if FILL_COLOR is None:
    fill_label.anchor_point = (0.25, 0.5)
    fill_label.text = "TRANSPARENT"
fill_block = Rect(x=120, y=240 - 35, width=30, height=30, fill=FILL_COLOR)
primary_disp_layer.append(fill_block)
primary_disp_layer.append(fill_label)

tolerance_label = Label(terminalio.FONT, text="TOLERANCE", color=0xFFFFFF)
tolerance_label.anchor_point = (1.0, 0.5)
tolerance_label.anchored_position = (250, 225)
tolerance_value = Label(terminalio.FONT, text="0.0", color=0xFFFFFF)
tolerance_value.anchor_point = (1.0, 0.5)
tolerance_value.anchored_position = (250, 215)
primary_disp_layer.append(tolerance_label)
primary_disp_layer.append(tolerance_value)

invert_label = Label(terminalio.FONT, text="INVERT", color=0xFFFFFF)
invert_label.anchor_point = (1.0, 0.5)
invert_label.anchored_position = (315, 225)
invert_value = Label(terminalio.FONT, text="True", color=0xFFFFFF)
invert_value.anchor_point = (1.0, 0.5)
invert_value.anchored_position = (315, 215)
if not INVERT:
    invert_value.text = "False"
primary_disp_layer.append(invert_label)
primary_disp_layer.append(invert_value)


# Instantiate PaletteFilter
palette_filter = PaletteFilter(
    SOURCE_PALETTE, TARGET_COLOR, FILL_COLOR, TOLERANCE, INVERT
)


while True:
    for frame in range(0, 765, 2):
        tile_grid.pixel_shader = palette_filter.palette

        # palette_filter.tolerance = map_range(potentiometer.value, 300, 54000, 0, 765)
        palette_filter.tolerance = frame
        tolerance_value.text = str(f"{palette_filter.tolerance:6.1f}")
