.. _deep_dive_game_window:

Deep dive: the game window
==========================

:ref:`Reference page on game window variables <reference_game_window>`

Setting the properties of the game window Pygame Turbo runs in is not done by
manipulating an object representing it, but instead by setting predetermined
global variables::

    WIDTH = 600
    HEIGHT = 400
    TITLE = "My own game"
    ICON = "imagename"
    FULLSCREEN = False
    RESIZABLE = True

The above are all the provided options to customize the game window. It is
normal to set the basic options for your game at the start of your main file,
but changing these variables while the game is running will change the game
window in turn. This means you can for example change the fullscreen mode while
the game is running::

    def on_key_down(key):
        global FULLSCREEN
        if key == keys.SPACE:
            FULLSCREEN = not FULLSCREEN

*Note:* Because these variables are global, they have to be declared so when
trying to change them from within a function. Without the ``global FULLSCREEN``
at the start of the function, the above code would not work.

To check any of the current settings, simply get the variable value as you
would with any other::

    def update():
        if alien.x > WIDTH:
            alien.x = 0

Even if you didn't do ``WIDTH = 600`` or similar at the top of your game
yourself, the variables can still be read since PGTurbo filles them with their
defaults if you didn't specify them. The defaults for the different variables
are as follows:

* ``WIDTH`` is ``800``.
* ``HEIGHT`` is ``600``.
* ``TITLE`` is ``"Pygame Turbo Game"``.
* ``ICON`` is a special indicator value telling PGTurbo to use the default
  icon instead of an image name. This is the one default value you can't make
  much use of if you didn't set one yourself.
* ``FULLSCREEN`` is ``False``.
* ``RESIZABLE`` is ``False``.

Below is a more detailed explanation of each variable:

* ``WIDTH`` is the width of the game window created by PGTurbo in pixels.
* ``HEIGHT`` is the height of the game window.
* ``TITLE`` is the name the game window has in its title bar and also shown
  when hovering over the window in the taskbar.
* ``ICON`` is the image name used for the small icon in the game window top bar
  if present and also for the game window indicator in the taskbar.

  It must be a valid image name for the *images*
  :ref:`resource folder <reference_images>`.
* ``FULLSCREEN`` is a boolean value (``True`` or ``False``) for whether the
  game window should be displayed in fullscreen mode or not.

  Since the game window must conform to the resolution of the screen it is on
  when in fullscreen mode, Pygame will pick the best resolution to get as close
  as possible to the resolution set with ``WIDTH`` and ``HEIGHT`` if they
  cannot be the same.
* ``RESIZABLE`` is a boolean value for whether the game window should be able
  change its size, for example when dragged on its edges with the mouse.

  This setting is ignored if the game window is in fullscreen mode.

Regardless of how the game window changes size, be it through mouse dragging by
the user or by setting fullscreen mode, ``WIDTH`` and ``HEIGHT`` will always
be automatically updated to reflect the changes.
