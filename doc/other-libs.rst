Other libraries like Pygame Turbo
=================================

Pygame Zero is the project that sparked many Python "zero" libraries. Since
Turbo is a fork from that project, some of the following examples work
seamlessly with it as well, although that cannot be guaranteed.

Network Zero
------------

`Network Zero`_ makes it simpler to have several machines or several processes
on one machine discovering each other and talking across a network.

.. caution::

    If you want to use Network Zero with Pygame Turbo, make sure you don't let
    it **block** (stop everything while waiting for messages). This will
    interrupt Pygame Turbo so that it stops animating the screen or even
    responding to input.  Always set the ``wait_for_s`` or ``wait_for_reply_s``
    options to ``0`` seconds.


.. _`Network Zero`: https://networkzero.readthedocs.io


GUI Zero
--------

`GUI Zero`_ is a library for creating Graphical User Interfaces (GUIs) with
windows, buttons, sliders, textboxes and so on.

Because GUI Zero and Pygame Turbo both provide different approaches for drawing
to the screen, they are not usable together.


.. _`GUI Zero`: https://lawsie.github.io/guizero/


GPIO Zero
---------

`GPIO Zero`_ is a library for controlling devices connected to the General
Purpose Input/Output (GPIO) pins on a `Raspberry Pi`_.

GPIO Zero generally runs in its own thread, meaning that it will usually work
very well with Pygame Turbo.

.. caution::

    When copying GPIO Zero examples, do not copy the ``time.sleep()`` function
    calls or ``while True:`` loops, as these will stop Pygame Turbo animating
    the screen or responding to input. Use :ref:`clock` functions instead to
    call functions periodically, or the :func:`update()` function to check a
    value every frame.

.. _`GPIO Zero`: https://gpiozero.readthedocs.io/
.. _`Raspberry Pi`: https://www.raspberrypi.org/


Adventurelib
------------

`Adventurelib`_ is a library for making text-based games easier to write (and
which doesn't do everything for you!).

Writing text-based games requires a very different set of skills to writing
graphical games. Adventurelib is pitched at a slightly more advanced level of
Python programmer than Pygame Turbo.

Adventurelib cannot currently be combined with Pygame Turbo.

.. _Adventurelib: https://adventurelib.readthedocs.io/


Blue Dot
--------

`Blue Dot`_ allows you to control your Raspberry Pi projects wirelessly using
an Android device as a Bluetooth remote.

Blue Dot generally runs in its own thread, meaning that it will usually work
very well with Pygame Turbo.

.. caution::

    Avoid ``time.sleep()`` function calls, ``while True:`` loops and Blue Dot's
    blocking ``wait_for_press`` and ``wait_for_release`` methods, as these will
    stop Pygame Turbo animating the screen or responding to input. Use
    :ref:`clock` functions instead to call functions periodically, or the
    :func:`update()` function to check a value every frame.

.. _`Blue Dot`: https://bluedot.readthedocs.io/


.. tip::

    Know of another library that belongs here?

    `Open an issue <https://github.com/Mambouna/pgturbo/issues/new>`_ on the
    issue tracker to let us know!
