.. _deep_dive_screen:

Deep dive: screen
=================

:ref:`Reference page on the screen builtin <reference_screen>`

The ``screen`` builtin is one of the two main ways to draw visuals to the
game window. As such, you will use it almost exclusively in the ``draw()``
function.

The other way to draw visuals to the screen is by calling ``Actor.draw()``.
You can read more about this in the :ref:`actor deep dive <deep_dive_actors>`.


.. _deep_dive_screen_wiping_the_last_frame:

Wiping the last frame
---------------------

Usually, you'll want to start the code in the ``draw()`` function with a call
of either ``screen.clear()`` or ``screen.fill(color)``.

These methods fill the entire game window with a solid color, erasing all the
visuals of the last frame. This is important because if you simply draw new
frames on top of old ones, you might end up with visuals from multiple past
frames smeared together across the game window.

``screen.clear()`` fills the game window with black. ``screen.fill(color)``
fills it with whatever color you specified as the argument.

In PGTurbo, colors can always we specified in one of two ways:

#. With a string of the color name, for example ``"lightblue"`` or ``"white"``.
   The possible options for these color strings can be found on the
   :ref:`colors reference page <reference_colors>`.

#. As an RGB tuple like ``(128, 0, 64)``. The first number specifies the red
   component of the color, the second green and the third blue. Each of the
   values in the tuple can have values from ``0`` to ``255``.

   ``(0, 0, 0)`` is fully black, ``(255, 255, 255)`` is fully white.

Optionally, a second color argument can be given to ``screen.fill()``. If
specified, the screen is filled with a gradient from the first argument color
at the top of the game window to the second argument color at the bottom of the
game window.


.. _deep_dive_screen_blit:

Blitting to the screen
----------------------

After the remnants of the last frame have been cleared, the visuals of this
frame can be drawn to the game window. The simplest thing to do is just display
a single image at a set position in the game window.

The ``screen.blit(image, position)`` method takes an `image` and draws it to
the game window such that its top left corner is at `position`. The image
argument can either be a string name of an image resource file in the
*images* resource folder or otherwise a Pygame Surface object.

You will most often use this with an image resource name. In short, image files
placed in a folder named *images* next to your game's ``.py`` file can be
automatically loaded by PGTurbo via their file name without the file extension.

``screen.blit("alien", (50, 70))`` would look for an image file named
*alien.png* or *alien.jpg* or similar in a folder named *images* next to your
game's Python file and then paste it to the game window. The image would end
up with its left upper corner at position 50 on the X axis and 70 on the Y
axis.

This is mostly useful for static images like backgrounds. If your images should
be moving around the game window, it's strongly recommended to use an 
:ref:`actor <deep_dive_actors>` instead of manually calling ``screen.blit()``
with ever changing `position` arguments.

For more details on images from string names, check the
:ref:`deep dive on resource folders <deep_dive_resources_and_storage>`.


.. _deep_dive_screen_draw:

Drawing with screen
-------------------

Beside working with existing images, ``screen`` has the ``screen.draw`` module,
which allows you to draw various shapes and text to the game window.

Its methods can broadly be split in two groups:
#. Methods to draw simple shapes like rectangles or circles.
#. Two powerful methods to draw text to the game window.


.. _deep_dive_screen_draw_simple_shapes:

Simple shapes
"""""""""""""

There's five methods that allow you to draw simple shapes to the game window.
As their use is self explanatory in many ways, they are simply listed below
and only points to clear up confusion are written about at length.

The first is that the basic drawing methods (``line()``, ``circle()`` and
``rect()``) all draw outlines, not filled shapes. As such, each of these takes
an optional `width` parameter, which specifies the line thickness used in
pixels. The default used if no `width` is given is ``1``.

As before, colors can always either be a color string name or an RGB tuple.

``rect()`` and ``filled_rect()`` have a slightly complex first argument in
`rect`. This is usually given as a tuple like
``((left, top), (width, height))``. For a rectangle with its topleft corner
at X = 50, Y = 100 and 200 pixels tall and wide, you'd do the following::

    screen.draw.rect(((50, 100), (200, 200)), "red", 2)

With the caveats out of the way, here are the method descriptions:

* ``screen.draw.line(start, end, color, [width])`` will draw a line from the
  `start` position tuple to the `end` position tuple with the given `color`.
  The default `width` is ``1`` pixel but can be set by providing a fourth
  argument.
* ``screen.draw.circle(pos, radius, color, [width])`` will draw a circle with
  the given `radius` around the position tuple `pos` with `color`. Again,
  `width` is ``1`` or specified.

  * ``screen.draw.filled_circle(pos, radius, color)`` simply draws the same
    kind of circle but with the solid given `color`.

* ``screen.draw.rect(rect, color, [width])`` draws a rectangle with the
  properies of a `rect` as explained above with `color`. Width works the same.

  Valid rectangles are tuples like ``((left, top), (width, height))`` or
  Pygame ``Rect`` objects.

  * ``screen.draw.filled_rect(rect, color)`` draws the same kind of rectangle
    but with the solid `color` given.

As an aside, it's also possible to directly create Pygame ``Rect`` objects, no
extra import needed: ``Rect((left, top), (width, height))``. These can also be
given as `rect` arguments for the two relevant functions. If you don't know
about them though, you can just use tuples as explained above.


.. _deep_dive_screen_draw_text:

Drawing text
""""""""""""

The draw methods for text are extremely versatile, since they hook into the
`pygame text package <https://github.com/cosmologicon/pygame-text>`.

The first method to draw text to the game window with is
``screen.draw.text(text)``. The first argument is the `text` as a
string that should be drawn. Optionally, a second argument can be given, which
is a position tuple like ``(x, y)``. This positions the top left corner of the
drawn text at the given `position`.

All other settings are optional are set via keyword arguments. They are covered
below in a few categories, each with examples and explanations.


Settings
""""""""

Positioning
'''''''''''

::

    screen.draw.text("Hello World!", centerx=120, top=80)
    screen.draw.text("Hello World!", midtop=(120, 80))

Keyword arguments: *see below*

This is enough to render simple text, however the ``draw.text()`` method allows
for a great level of customization by allowing a large number of keyword
arguments to be used for styling or positioning.

In fact, it is recommended not to use the optional second parameter for
positioning without naming it but instead use one of the following keyword
parameters to place the text instead::

    top left bottom right centerx centery

    topleft bottomleft topright bottomright
    midtop midleft midbottom midright center

The first row are keyword arguments that set either the X or Y position of the
drawn text, allowing precise placement by using two of them::

    screen.draw.text("Hello World!", centerx=120, top=80)

This will position the text so its top edge is at pixel 80 on the Y axis and
its horizontal center is at pixel 120 on the X axis.

The second and third row of keywords allow positioning via a single position
tuple by fixing one point of the rendered text, for example the middle of the
top edge::

    screen.draw.text("Hello World!", midtop=(120, 80))

By using the positioning keyword arguments, it is far easier to precisely place
the text, which is why their use is recommended over simply specifying a second
unnamed argument with a position tuple.

If there are conflicting arguments given via keywords (for example specifying
both ``left`` and ``right`` values), then only one fix for each axis is used.
This behavior is not consistent however, so you should always make sure that
you are properly setting positioning.

If you want to draw text in a specific area, there is the
``screen.draw.textbox()`` method to use instead, which is meant specifically
for this purpose. It is explained
:ref:`here below <deep_dive_screen_draw_textbox>`.


Font and sizing
'''''''''''''''

::

    screen.draw.text("Hello World!", topright=(100, 100), fontname="viga",
                     fontsize=32, antialias=False)

Keyword arguments: ``fontname``, ``fontsize``, ``antialias``

``fontname`` controls which font to draw with. Font names are strings and the
available fonts are the ``.ttf`` files located in the *fonts* resource folder.

As with other resources, file names must follow certain naming rules and are
given without the file extension. More details can be found in the
:ref:`reference page on the fonts resource folder <reference_fonts>`.

``fontsize`` is the size of the text characters. The value is the height in
pixels of each character and defaults to ``24``.

``antialias`` sets whether to render the text with antialiasing enabled or not.
This defaults to ``True`` and should likely stay that way in most usecases.
The example above disables it only to demonstrate the use of the keyword
argument.


Text and background color
'''''''''''''''''''''''''

::

    screen.draw.text("Hi World!", center=(128, 64), color="red",
                     background="lightblue")

Keyword arguments: ``color``, ``background``

``color`` can be used to set the color of the drawn text. It defaults to
``"white"``.

``background`` sets a solid background color for the rendered text with sharp
edges and corners. This display style can not be customized. If you need a more
customizable background for text, consider using an image.

As always, colors can be a color string name or an RGB tuple.


Word wrapping and text width
''''''''''''''''''''''''''''

::

    screen.draw.text("Splitting\nlines.", (100, 100))
    screen.draw.text("Splitting lines.", (100, 100), width=60)

Keyword arguments: ``width``, ``widthem``, ``lineheight``

By default, text will grow infinitely wide unless you manually break the line
with the ``\n`` character in the `text` string. To enable automatic line
splitting, use the ``width`` keyword argument, which sets the maximum width of
the drawn text in pixels.

When a ``width`` is given, the drawn text will automatically split an spaces in
`text` to try and keep lines shorter than the specified maximum. If a single
word with no spaces anywhere is by itself wider than ``width``, the text will
simply go over the limit.

If you want to write a space where lines should not be broken, use the special
character ``\u00A0`` in the `text` string.

Alternatively to ``width``, which sets the maximum in pixels, you can use
``widthem``, which sets it in font based *em* units.

To further customize how large a gap is left between drawn lines of text, you
can set the ``lineheight`` to be used. This defaults to ``1.0`` if not given
and is increased or decreased as a relative to the default, so ``1.5`` is an
extra half over the default.


Text alignment
''''''''''''''

::

    screen.draw.text("Hello\nWorld!", bottomright=(500, 400),
                     align="left")

Keyword argument: ``align``

The ``align`` keyword determines if text lines sit straight along their left
end, right end or are all centered on each others width. If not specified, a
normally sensible default is chosen based on the positioning keyword arguments
used. Because of this, it's usually recommended to stick to the default
behavior.

If something looks wrong, you can specify ``align`` with the values ``"left"``,
``"right"``, ``"center"`` or a value between ``0.0`` and ``1.0``. In this case,
``0.0`` is full left alignment and ``1.0`` is full right alignment.


Text outline
''''''''''''

::

    screen.draw.text("Hi World!", midtop=(300, 100), owidth=1.0,
                     ocolor="blue")

Keyword arguments: ``owidth``, ``ocolor``

If ``owidth`` is given, the text will be drawn with an outline around each
character. The values to use are relative, with ``1.0`` meant to be a good
value in many usecases. Start there and adjust slightly up or down to fit your
needs.

Outlines are drawn manually and don't scale well, so they will likely look
quite bad at very large font sizes.

``ocolor`` can be used to set the color of the drawn outline. It defaults to
``"black"`` since text color defaults to ``"white"``. As always, colors can be
a color string name or an RGB tuple.


Drop shadow
'''''''''''

::

    screen.draw.text("Hi World!", bottomright=(100, 100),
                     shadow=(1.0, 1.0), scolor="blue")

Keyword arguments: ``shadow``, ``scolor``

If ``shadow`` is given, a drop shadow will be drawn for each character in the
text. The value is a tuple of two relative numbers, with ``(1.0, 1.0)`` meant
to be a good value in most usecases. Start there and adjust each value slightly
to fit your needs.

``(0.0, 0.0)`` places the drop shadow in the exact same position as your main
text, while values over ``1.0`` place it further and further away.

Positive values values place the drop shadow to the right and lower than the
main text characters. Negative values in either position place it instead left
and or higher than the main text characters.

``scolor`` can be used to set the color of the drop shadow. It defaults to
``"black"`` since text color defaults to ``"white"``. As always, colors can be
a color string name or an RGB tuple.


Gradient coloring
'''''''''''''''''

::

    screen.draw.text("Hello World!", midbottom=(100, 100),
                     color="black", gcolor="green")
    screen.draw.text("Hello World!", midbottom=(100, 100), shade=1.0)

Keyword argument: ``gcolor``, ``shade``

Specify ``gcolor`` to render the text with a vertical color gradient going from
the text ``color`` at the top of each character to ``gcolor`` at the bottom.

The exact parameters of the gradient cannot be changed, as they are hardcoded.

A simple styling alternative with a gradient is to specify ``shade``. Instead
of two given colors, using ``shade`` makes it so the text color is simply
made smoothly lighter and darker at the top or bottom of each character. In
this way, it makes it look like there is a light shining on the text either
from above or below.

Values for shade are relative, with ``1.0`` meant to be a good one for many
usecases, while ``3.0`` is a very strong effect. Positive values create an
illuminated look from above, negative ones from below.


Alpha transparency
''''''''''''''''''

::

    screen.draw.text("Hello World!", topright=(150, 50), alpha=0.5)

Keyword argument: ``alpha``

``alpha`` sets the opacity of the drawn text, where ``0.0`` is fully invisible
and ``1.0`` is completely opaque.

While there are infinite possible values between ``0.0`` and ``1.0``, in
reality values for ``alpha`` are rounded, although to a precise enough degree
that it should not matter in normal use.


Anchored positioning
''''''''''''''''''''

::

    screen.draw.text("Hello World!", (80, 40), anchor=(0.3, 0.7))

Keyword argument: ``anchor``

Using ``anchor`` is an alternative approach to positioning that can only be
used when no positioning keywords are used and instead the unnamed second
argument is given.

The value for ``anchor`` is a tuple of two relative values between ``0.0`` and
``1.0``. Each controls how far the positioning is shifted in the X or Y axis
along the length or height of the drawn text in relation to the topleft corner.

As such, ``anchor=(0.0, 0.0)`` leaves the positioning to fix the topleft corner
like normal, whereas ``anchor=(1.0, 1.0)`` makes it so the position argument
instead fixes the bottom right corner of the drawn text.


Rotation
''''''''

::

    screen.draw.text("Hello World!", midright=(800, 600), angle=45)

Keyword argument: ``angle``

When given an ``angle``, text is drawn rotated counterclockwise by the number
of specified degrees.

Positioning of rotated text can be quite tricky, since it rotates around the
anchoring point created by the used positioning keywords. Simplest is rotating
when done so around a set ``center``. If you use other positioning, it's
recommended to experiment to see the changes in action and finetune the
positioning after deciding on the rotation of the text.


.. _deep_dive_screen_draw_textbox:

Textbox
"""""""

The second method for drawing text is
``screen.draw.textbox(text, rect)``. This method takes text as a string
as normal and then a rect, which can either be a pygame Rect object or a tuple
representing a rect like so: ``((left, top), (width, height))``. The text will
then be drawn and positioned so that it is as large as possible while still
fitting in the provided rectangle boundaries.

As with ``screen.draw.text()``, the same optional settings can be made via the
keyword arguments listed above. Since positioning and sizing of the text are
already handled automatically however, the keywords affecting those settings
are ignored by ``screen.draw.textbox()``.


.. _deep_dive_screen_screenshots:

Screenshots
-----------

One of the few times you might use the ``screen`` builtin outside of the
``draw()`` function is to take screenshots.

There is a default hotkey to take a screenshot, which is the F12 key.

To make PGTurbo take a screenshot from your code, call ``screen.screenshot()``.

Screenshots are saved to a folder called "pgturbo" located in the user Pictures
directory of the PC the game is running on. Their filename is made up of the
script / project name of the game the screenshot is from with a timestamp
appended that ensures any number of screenshots can be taken.
