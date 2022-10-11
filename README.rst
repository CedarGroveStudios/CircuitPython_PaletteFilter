Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/CircuitPython_PaletteFilter/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/CircuitPython_PaletteFilter/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

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
`cedargrove_palettefilter.compare_colors()` helper function.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install cedargrove_palettefilter

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: py

    import displayio
    from cedargrove_palettefilter import PaletteFilter

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
    filter = PaletteFilter(SOURCE_PALETTE, TARGET_COLOR, FILL_COLOR, TOLERANCE)
    print(f"target_color: {hex(filter.target_color)}")

    print("------")
    print("source palette:")
    print("index, color, transparency")
    for index, color in enumerate(SOURCE_PALETTE):
        print(index, hex(color), SOURCE_PALETTE.is_transparent(index))

    print("------")
    print("new palette:")
    print("index, color, transparency")
    for index, color in enumerate(filter.palette):
        print(index, hex(color), filter.palette.is_transparent(index))

    while True:
        pass


Documentation
=============
API documentation for this library can be found in `PaletteFilter_API <https://github.com/CedarGroveStudios/CircuitPython_PaletteFilter/blob/main/media/pseudo_readthedocs_palettefilter.pdf>`_.

.. image:: https://github.com/CedarGroveStudios/CircuitPython_PaletteFilter/blob/main/media/flying_lars_test.png

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_PaletteFilter/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
