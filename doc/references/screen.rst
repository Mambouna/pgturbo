.. _reference_screen:

Reference: Screen
==================

:ref:`Deep dive on the screen builtin <deep_dive_screen>`

.. tip::

    Colors can always be specified either as a preset string color name or
    as an RGB tuple of ``(r, g, b)`` with each value being an integer between
    ``0`` and ``255``.

    You can find all available preset color names
    :ref:`here <reference_colors>`.


.. _reference_screen_attributes:

Attributes
----------

.. attribute:: surface

    The raw `Pygame surface`_ that represents the screen buffer. You can
    use this for advanced graphics operations.

    .. _`Pygame surface`: https://www.pygame.org/docs/ref/surface.html


.. _reference_screen_methods:

Methods
-------

.. method:: clear()

    Reset the screen to black.

.. method:: fill(color, [gcolor])

    Fill the screen with a solid `color`. 

    If `gcolor` is given then fill with a gradient, from `color` at
    the top of the screen to `gcolor` at the bottom.

    :param color: The color to fill the screen with. Either a preset string
                  name or an RGB tuple as specified above.
    :param gcolor: Optional second color to create a gradient from.

.. method:: blit(image, position)

    Draw the image to the screen at the given position.

    :param image: Either a Surface or an image string name found in the
                  :ref:`images resource folder <deep_dive_resources>`.
    :param position: A tuple of two pixel numbers for X and Y. The image will
                     be placed so its top left corner is at the specified
                     `position`.

.. method:: draw.line(start, end, color, [width])

    Draw a colored line from `start` to `end` to the game window.

    :param start: A position tuple for where the line should start.
    :param end: A position tuple for where the line should end.
    :param color: The color the line should have, either as a string or RGB
                  tuple.
    :param width: Optionally a thicker width in pixels for the line. Default is
                  ``1``.

.. method:: draw.circle(pos, radius, color, [width])

    Draw the outline of a circle to the game window.

    :param pos: Position tuple for the center of the drawn circle.
    :param radius: The radius in pixels the drawn circle should have.
    :param color: The color the circle outline should have.
    :param width: Optionally a thicker width in pixels for the outline. Default
                  is ``1``.

.. method:: draw.filled_circle(pos, radius, color)

    Draw a filled circle to the game window.

    :param pos: Position tuple for the center of the drawn circle.
    :param radius: The radius in pixels the drawn circle should have.
    :param color: The color the circle should have.

.. method:: draw.rect(rect, color, [width])

    Draw the outline of a rectangle to the game window.

    :param rect: The rectangle to draw. Must be a Pygame Rect object (create
                 with ``Rect((left, top), (width, height))``) or a tuple
                 exactly like ``((left, top), (width, height))``.
    :param color: What color the outline should have.
    :param width: Optionally a thicker line width in pixels for the outline.
                  Default is ``1``.

.. method:: draw.filled_rect(rect, color)

    Draw a filled rectangle to the game window.

    :param rect: The rectangle to draw. Must be a Pygame Rect object (create
                 with ``Rect((left, top), (width, height))``) or a tuple
                 exactly like ``((left, top), (width, height))``.
    :param color: What color the drawn rectangle should have.

.. method:: draw.text(text[, position, **kwargs])

    .. Comment to disable wrong syntax highlighting because of stars.**

    Draw text to the game window.

    There's an extremely rich API for positioning and formatting text. See
    :ref:`deep_dive_screen_draw_text` for full details or the list of
    :ref:`text keyword arguments <reference_screen_ptext_keywords>`
    below.

    :param text: The string that should be drawn to the game window.
    :param position: Optionally the position of the top left corner of the
                     text to be drawn. It's usually preferable to be explicit
                     about positioning by using keyword arguments instead of
                     this argument.
    :param kwargs: Any number of keyword arguments to position and style the
                   text to be drawn.

.. method:: draw.textbox(text, rect, **kwargs)

    .. Comment to disable wrong syntax highlighting because of stars.**

    Draw text, sized to fill the given rect.

    There's an extremely rich API for positioning and formatting text. See
    :ref:`deep_dive_screen_draw_text` for full details or the list of
    :ref:`text keyword arguments <reference_screen_ptext_keywords>`
    below.

    :param text: The string that should be drawn to the game window.
    :param rect: The rectangle in which the text should fit. Can be a
                 Rect object or otherwise a rectangle tuple in the form
                 of ``((pos_x, pos_y), (width, height))`` with each individual
                 value being an integer. The first tuple specifies the top left
                 corner position for the rectangle. The second one the
                 dimensions.
    :param kwargs: Any number of keyword arguments to style the text to be
                   drawn. Note that not all keyword arguments usable in
                   ``screen.draw.text()`` are available here, since positioning
                   and sizing are decided by `rect`.

.. method:: screenshot()

    Takes a screenshot of the entire game window and saves it to
    the ``pgturbo`` folder in your home ``Pictures`` directory.

    Returns the path of the file that was written, as a string.

    You can press F12 to take a screenshot at any time, without needing to
    call this function manually from your game code. This will print the
    picture save path to the console output.

.. method:: bounds()

    Return a ZRect representing the bounds of the screen.


.. _reference_screen_ptext_keywords:

Keyword arguments for text drawing
----------------------------------

- ``fontname``: Filename without file extension of the font to draw, gotten
  from the ``fonts`` resource folder. Must be a ``.ttf`` font file. Defaults to
  using the default system font instead.
- ``sysfontname``: Name of the system font to use. Defaults to the default
  system font. If the specified font is not found, reverts to the default.
- ``fontsize``: Size of the font to use in pixels. Defaults to ``24``.
- ``antialias``: Whether to render with antialiasing. Defaults to ``True``.
- ``bold``: Whether to render the font bold or not. Defaults to ``None``
  which means no bolding.

  *Note:* It's highly recommended to just use the ``fontname`` that itself is
  bold instead. This argument will transform the text in a crude way,
  resulting in suboptimal looks.
- ``italic``: Whether to render the font italic or not. Defaults to ``None``
  which means no italics.

  *Note:* It's highly recommended to just use the ``fontname`` that itself is
  italic instead. This argument will transform the text in a crude way,
  resulting in suboptimal looks.
- ``underline``: Whether to apply underline font decoration. Defaults to
  ``None``, meaning no underline.
- ``color``: Foreground color to use for drawn text. Defaults to ``white``.
- ``background``: Background color to use. Defaults to ``None``.
- ``top``: Sets the position of the text by fixing where its upper edge is on
  the Y axis.
- ``left``: Sets the position of the text by fixing where its left edge is on
  the X axis.
- ``bottom``: Sets the position of the text by fixing where its lower edge is
  on the Y axis.
- ``right``: Sets the position of the text by fixing where it's right edge is
  on the X axis.
- ``topleft``: Sets the position of the text by fixing where its top and left
  corner is via a position tuple.
- ``bottomleft``: Sets the position of the text by fixing where its bottom and
  left corner is via a position tuple.
- ``topright``: Sets the position of the text by fixing where its top and right
  corner is via a position tuple.
- ``bottomright``: Sets the position of the text by fixing where its bottom and
  right corner is via a position tuple.
- ``midtop``: Sets the position of the text by fixing where the center of its
  top edge is via a position tuple.
- ``midleft``: Sets the position of the text by fixing where the center of its
  left edge is via a position tuple.
- ``midbottom``: Sets the position of the text by fixing where the center of its
  bottom edge is via a position tuple.
- ``midright``: Sets the position of the text by fixing where the center of its
  right edge is via a position tuple.
- ``center``: Sets the position of the text by fixing its center point in the
  X and Y axis via position tuple.
- ``centerx``: Sets the position of the text by fixing where the center of the
  text in the X axis is.
- ``centery``: Sets the position of the text by fixing where the center of the
  text in the Y axis is.
- ``width``: Maximum width of the text to draw in pixels. Defaults to ``None``.
- ``widthem``: Maximum width of the text to draw in font based *em* units.
  Defaults to ``None``.
- ``lineheight``: Vertical spacing between lines in units of the font's
  default line height. Defaults to ``1``.

  Only relevant if text is wrapped to multiple lines due to width or with
  ``\n`` characters.
- ``pspace``: Additional vertical spacing between paragraphs in units of the
  font's default line height. Defaults to ``0``.

  This is only applied when the text to draw contains ``\n`` characters, not
  from word wrapping.
- ``strip``: Whether to strip trailing whitespace at line breaks. Defaults to
  ``True``.
- ``align``: Horizontal positioning of lines relative to each other. Defaults
  to ``None``.
- ``owidth``: Thickness of an outline to draw around text characters. Defaults
  to ``None``, meaning no outline. Values are relative, so might require
  experimentation. Generally, a value of ``1.0`` is meant to give a reasonable
  outline thickness for many usecases.

  *Note:* Outlines are drawn manually and with a crude method. Large text will
  not look good with an outline of this kind.
- ``ocolor``: The color of a drawn outline. Defaults to ``"black"``.
- ``shadow``: (x, y) tuple for the offset of a drawn drop shadow. Defaults to
  ``None``, meaning no drop shadow. The tuple sets the positioning of the drop
  shadow in relative terms, with ``(1.0, 1.0)`` meant to give a good general
  position for many usecases.
- ``scolor``: The color of the drawn drop shadow. Defaults to ``"black"``.
- ``gcolor``: Sets a second color for the drawn text which results in a
  gradient from the ``color`` at the top of the text to the ``gcolor`` at the
  bottom of the text. Defaults to ``None``, meaning no gradient.
- ``shade``: Instead of a full gradient, simply lightens or darkens ``color``
  vertically. Positive values give a sense of text illuminated from the top,
  negative ones of text illuminated from the bottom. Defaults to ``0``. Values
  are relative with ``1`` meant to be a reasonable value for many usecases.
  ``3`` gives a very strong effect.
- ``alpha``: Alpha transparency to draw the text with. Defaults to ``1.0``,
  meaning full opacity. ``0.0`` is fully invisible.
- ``anchor``: Tuple of two float values that specify how to position the text
  in relation to its topleft corner. Defaults to ``(0.0, 0.0)``. ``1.0`` in
  either value will shift the text by its entire width or height along that
  axis, meaning using ``(1.0, 1.0)`` is equivalent to setting the rightbottom
  corner instead of the topleft one.

  Only applies if no positioning keyword arguments are used.
- ``angle``: Counterclockwise rotation to draw the text at. Defaults to ``0``.


.. _reference_screen_changelog:

Changelog
---------

* **1.8:** Added screenshot functionality.
* **1.4:** First release of PGTurbo after fork from PGZero.
