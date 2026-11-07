.. _reference_fonts:

Reference: fonts
================

:ref:`Deep dive on text display <deep_dive_screen_draw_text>`

Font resources are exclusively accessed via the `fontname` keyword argument
of the methods ``screen.draw.text()`` and ``screen.draw.textbox()``.

Example: ``screen.draw.text("Hello", (50, 50), fontname="viga")``

In the above example, the font resource loader will fetch the font file
*viga.ttf* in the background. In contrast to some of the other resource
loaders, there is no reason to access font resources directly.


.. _reference_fonts_location_filenames_and_formats:

Location, filenames and formats
--------------------------------

Fonts must be placed in a directory called *fonts*, placed next to your game's
main python file.

Filenames can consist of lowercase letters, numbers and underscores and must
start with a letter.

For example, these filenames are valid::

    viga.ttf
    viga_italic.ttf
    viga_bold_2.ttf

These filenames are not valid::

    3.ttf
    2viga.ttf
    viga-italic.ttf
    viga italic.ttf

Fonts are only supported in the TTF file format: ``.ttf``.
