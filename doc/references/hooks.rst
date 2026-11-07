.. _reference_hooks:

Reference: Event hooks
======================

:ref:`Deep dive on event hooks <deep_dive_hooks>`


.. _reference_hooks_game_loop:

Game loop hooks
---------------

.. function:: update() or update(dt)

    Called by Pygame Turbo to step your game logic. This will be called
    repeatedly, usually 60 times a second.

    There are two different approaches to writing an update function.

    In simple games you can assume a small time step (a fraction of a second)
    has elapsed between each call to ``update()``. Perhaps you don't even care
    how big that time step is: you can just move objects by a fixed number of
    pixels per frame (or accelerate them by a fixed constant, etc.)

    A more advanced approach is to base your movement and physics calculations
    on the actual amount of time that has elapsed between calls. This can give
    smoother animation, but the calculations involved can be harder and you
    must take more care to avoid unpredictable behaviour when the time steps
    grow larger.

    To use a time-based approach, you can change the update function to take a
    single parameter. If your update function takes an argument, Pygame Turbo
    will pass it the elapsed time in seconds. You can use this to scale your
    movement calculations.

.. function:: draw()

    Called by Pygame Turbo when it needs to redraw your game window.

    ``draw()`` must take no arguments.

    Pygame Turbo attempts to work out when the game screen needs to be redrawn
    to avoid redrawing if nothing has changed. On each step of the game loop
    it will draw the screen in the following situations:

    * If you have defined an ``update()`` function (see below).
    * If a clock event fires.
    * If an input event has been triggered.

    One way this can catch you out is if you attempt to modify or animate
    something within the draw function. For example, this code is wrong. The
    alien is not guaranteed to continue moving across the screen::

        def draw():
            alien.left += 1
            alien.draw()

    The correct code uses ``update()`` to modify or animate things and draw
    simply to paint the screen::

        def update():
            alien.left += 1

        def draw():
            alien.draw()


.. _reference_hooks_input:

Input hooks
-----------

.. function:: on_mouse_down([pos], [button])

    Called when a mouse button is pressed down.

    :param pos: A tuple (x, y) that gives the location of the mouse pointer
                when the button was pressed.
    :param button: A :ref:`mouse button constant <reference_mouse_constants>`
                   enum value indicating the button that was pressed. Compare
                   this value to a ``mouse`` constant to check if that mouse
                   button was pressed: ``if button = mouse.LEFT:``.

.. function:: on_mouse_up([pos], [button])

    Called when a mouse button is released.

    :param pos: A tuple (x, y) that gives the location of the mouse pointer
                when the button was released.
    :param button: A :ref:`mouse button constant <reference_mouse_constants>`
                   enum value indicating the button that was released. Compare
                   this value to a ``mouse`` constant to check if that mouse
                   button was let go of: ``if button = mouse.LEFT:``.

.. function:: on_mouse_move([pos], [rel], [buttons])

    Called when the mouse is moved.

    :param pos: A tuple (x, y) that gives the location that the mouse pointer
                moved to.
    :param rel: A tuple (delta_x, delta_y) that represent the change in the
                mouse pointer's position.
    :param buttons: A set of
                    :ref:`mouse button constant <reference_mouse_constants>`
                    enum values indicating the buttons that were depressed
                    during the move. Check if a mouse constant is part of the
                    set to see whether it was held during the move:
                    ``if mouse.LEFT in buttons:``.

.. function:: on_key_down([key], [mod], [unicode])

    Called when a key is depressed.

    :param key: A :ref:`key constant <reference_keyboard_constants>` enum value
                indicating the key that was pressed. Compare this value to
                a ``keys`` constant to check if that key was pressed down:
                ``if key == keys.SPACE:``.
    :param mod: A bitmask of modifier keys that were depressed. Use
                ``mod & keymods.SHIFT`` or other available constants to check
                for modifiers used with the keystroke.
    :param unicode: Where relevant, the character that was typed. Not all keys
                    will result in printable characters - many may be control
                    characters. In the event that a key doesn't correspond to
                    a Unicode character, this will be the empty string.

.. function:: on_key_up([key], [mod])

    Called when a key is released.

    :param key: A :ref:`key constant <reference_keyboard_constants>` enum value
                indicating the key that was released. Compare this value to
                a ``keys`` constant to check if that key was let go of:
                ``if key == keys.SPACE:``.
    :param mod: A bitmask of modifier keys that were depressed. Use
                ``mod & keymods.SHIFT`` or other available constants to check
                for modifiers used with the keystroke.

.. function:: on_joy_down([joybtn], [instance_id])

    Called when a controller button is depressed.

    :param joybtn: A :ref:`joystick button constant <reference_joystick_constants>`
                   enum value indicating the controller button that was
                   pressed. Compare this to a ``joybutton`` constant to check
                   if that button was pressed:
                   ``if joybtn == joybutton.FACE_DOWN:``.
    :param instance_id: An integer identifying the device on which the button
                        was pressed. This can be used to distinguish controls
                        for multiple controllers for example in co-op games.

.. function:: on_joy_up([joybtn], [instance_id])

    Called when a controller button is released.

    :param joybtn: A :ref:`joystick button constant <reference_joystick_constants>`
                   enum value indicating the controller button that was
                   released. Compare this to a ``joybutton`` constant to check
                   if that button was let go of:
                   ``if joybtn == joybutton.FACE_DOWN:``.
    :param instance_id: An integer identifying the device on which the button
                        was released.

.. function:: on_joy_move([axis], [value], [instance_id])

    Called when a controller axis is moved, for example the thumbsticks on a
    typical console controller.

    :param axis: A :ref:`joystick axis constant <reference_joystick_constants>`
                 enum value indicating the controller axis that was moved.
                 Compare this to an ``joyaxis`` constant to check if that
                 axis was moved: ``if axis == joyaxis.LEFT_X:``.
    :param value: The new value of the changed axis. Values for thumbsticks
                  range from -1 to 1 with 0 being centered while shoulder
                  triggers range from 0 to 1 with 1 being fully pressed in.
    :param instance_id: An integer identifying the device on which the axis
                        value was changed.

.. function:: on_joy_added([instance_id])

    Called when a new controller is connected.

    :param instance_id: An integer identifying the device that was just
                        connected.

.. function:: on_joy_removed([instance_id])

    Called when a known controller is disconnected.

    :param instance_id: An integer identifying the device that was just
                        disconnected.


.. _reference_hooks_general:

General event hooks
-------------------

.. function:: on_music_end()

    Called when a music track finishes playing.

    Note that this will not be called if the track is configured to loop.

.. function:: on_window_resized([width, height])

    Called when the game window has been resized (either by dragging its edges
    with the mouse or by setting ``WIDTH`` or ``HEIGHT`` from code).

    This function is also called when sizes change due to turning fullscreen
    mode on or off.

    :param width: The new width of the game window as an integer.
    :param height: The new height of the game window as an integer.

.. function:: on_exit()

    Called just before the game exits.

    At this stage, the exit cannot be prevented, so if you want to give the
    user the option to cancel closing the game or similar, you have to code
    the functionality yourself.


.. _reference_hooks_changelog:

Changelog
---------

* **1.13:** Added ``on_exit()`` and ``on_window_resized()`` hooks.
* **1.4:** First release of PGTurbo after fork from PGZero.
