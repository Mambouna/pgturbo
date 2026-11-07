.. _reference_images:

Reference: images
==================

:ref:`Deep dive on resources <deep_dive_resources>`

Image files are usually accessed via ``images.filename``, where filename is a
file in the *images* resource directory of the game without the file
extension.

An exception is the creation of an actor, where the filename is given as a
string argument and then automatically loaded from the images resource loader.


.. _reference_images_location_filenames_and_formats:

Location, filenames and formats
--------------------------------

The ``images`` builtin can access all valid image files in a directory called
*images*, placed next to your game's main python file.

Filenames can consist of lowercase letters, numbers and underscores and must
start with a letter.

For example, these filenames are valid::

    alien.png
    alien_hurt.png
    alien_run_7.png

These filenames are not valid::

    Alien.png
    ALIEN.png
    3.png
    3degrees.png
    my-cat.png
    sam's dog.png

The following file formats can be used for ``images``: ``.png``, ``.gif``,
``.jpg``, ``.jpeg``, ``.bmp``, ``.webp``.


.. _reference_images_methods_on_image_files:

Methods on image files
-----------------------

.. method:: get_width()

    Returns the width of the image in pixels.

.. method:: get_height()

    Returns the height of the image in pixels.

.. method:: get_size()

    Returns a tuple (width, height) indicating the size in pixels of the
    surface.

.. method:: get_rect()

    Get a ``Rect`` that is pre-populated with the bounds of the image
    if the image was located at the origin.

    Effectively this is equivalent to ``Rect((0, 0), image.get_size())``.


.. _reference_images_methods_on_images_builtin:

Methods on images builtin
--------------------------

There are two relevant methods that can be called on the ``images`` builtin
itself:

.. method:: unload(filename)

    Removes the image file called `filename` from the ``images`` builtin cache.

    You should not usually need this unless your game is very large and starts
    consuming a lot of memory from all the cached resource files.

.. method:: unload_all()

    Completely empties the ``images`` builtin cache.

    You should not usually need this unless your game is very large and starts
    consuming a lot of memory from all the cached resource files.


.. _reference_images_changelog:

Changelog
---------

* **1.4:** First release of PGTurbo after fork from PGZero.
