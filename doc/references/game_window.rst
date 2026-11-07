.. _reference_game_window:

Reference: Game window variables
================================

:ref:`Deep dive on game window variables <deep_dive_game_window>`

The following are all global variables that correspond to the settings of the
game window PGTurbo creates. They are available even if not set by the
developer and then contain their defaults:

.. attribute:: WIDTH

    The width of the game window in pixels. Use integer values.

    When the game window size changes, ``WIDTH`` is automatically updated.

    Default is ``800``.

.. attribute:: HEIGHT

    The height of the game window in pixels. Use integer values.

    When the game window size changes, ``HEIGHT`` is automatically updated.

    Default is ``600``.

.. attribute:: TITLE

    The text the game window displays as its name. Use string values.

    Default is ``"Pygame Turbo Game"``.

.. attribute:: ICON

    The image to use as a small icon for the game window. Use a string value
    for the image name as you would when creating an actor (just the name of
    the file without the file extension text).

    The image file needs to be in the ``images`` directory of your game.

    Default is a special indicator value for PGTurbo to use the default icon
    instead of an image name. This is the one variable not useful in its
    default state to check by the developer.

.. attribute:: FULLSCREEN

    Whether the game window should be in fullscreen mode or not. Use ``True``
    or ``False``.

    When the game is in fullscreen mode, ``WIDTH`` and ``HEIGHT`` stay roughly
    the same and all the visuals of your game are scaled up to display at
    fullscreen resolution. This means you can keep your code the same without
    worrying about how fullscreen mode changes the literal pixel resolution of
    the game window.

    The game window can't always stay at the exact same resolution as it was
    when windowed, since displays have a fixed aspect ratio, but Pygame will
    pick a resolution as close to the same as possible.

    Default is ``False``.

.. attribute:: RESIZABLE

    Whether the game window can be resized by dragging its edges with the
    mouse. Use ``True`` or ``False``. If the game window is in fullscreen mode,
    ``RESIZABLE`` is ignored, meaning only windows not in fullscreen mode can
    be resizable.

    Default is ``False``.


.. _reference_game_window_changelog:

Changelog
---------

* **1.15:** Made all game window variables always present in global scope with
  their default values if the user didn't set them. Prevents crashes when
  reading without having set.
* **1.13:** Added ``FULLSCREEN`` and ``RESIZABLE`` game window variables.
* **1.4:** First release of PGTurbo after fork from PGZero.
