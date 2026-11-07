.. _reference_mouse:

Reference: mouse
=================

:ref:`Deep dive on the mouse builtin <deep_dive_mouse>`


.. _reference_mouse_attributes:

Attributes
----------

.. attribute:: pressed

    Returns a tuple of three booleans for the left, middle and right
    mouse buttons in order. ``True`` means the button is currently pressed.

.. attribute:: pressed_left

    Returns ``True`` if the left mouse button is currently pressed, otherwise
    ``False``.

.. attribute:: pressed_middle

    Returns True if the middle mouse button is currently pressed, otherwise
    ``False``.

.. attribute:: pressed_right

    Returns True if the right mouse button is currently pressed, otherwise
    ``False``.

.. attribute:: pos
    :no-index:

    Returns the current position of the mouse in the game window as a tuple of
    two pixel numbers.

    Can be set to teleport the mouse to the given position inside the game
    window.

.. attribute:: last_called_pos

    Returns the position of the mouse at the time this value was last read.

.. attribute:: recent_pos

    Returns a tuple of the n last positions the mouse had moved to starting
    from the most recent. Default for n is 60 and can be changed via
    the ``recent_pos_max`` attribute.

.. attribute:: recent_pos_max

    Returns the total number of positions tracked via ``recent_pos``.

    Increasing this value simply extends the length of the queue of tracked
    positions. Decreasing it also cuts the queue to the new maximum number of
    elements.

    Default value: ``60``

.. attribute:: rel

    Returns the relative position change of the mouse over the last frame as a
    tuple of two pixel numbers.

.. attribute:: last_called_rel

    Returns the relative position change of the mouse since this value was last
    read.

.. attribute:: recent_rel

    Returns a tuple of the n last position changes the mouse had, starting from
    the most recent. Default for n is 60 and can be changed via
    ``recent_rel_max``.

.. attribute:: recent_rel_max

    Returns the total number of position changes tracked via ``recent_pos``.

    Increasing this value simply extends the length of the queue of tracked
    positions. Decreasing it also cuts the queue to the new maximum number of
    elements.

    Default value: ``60``

.. attribute:: visible

    Returns a boolean of whether the mouse cursor is currently visible.

    Setting this to either a boolean or 0 or 1 makes the mouse visible or
    invisible.

    Default value: ``True``

.. attribute:: focused

    Returns a boolean of whether the game window is currently focused.

.. attribute:: cursor

    Returns a tuple with two elements: the name string of the current cursor
    and the hotspot of the cursor if it is known or ``None`` otherwise. Setting
    this loads a new cursor and applies it to the mouse.

    To set a system cursor, set ``cursor`` to any of the following values:
    ``"ARROW"``, ``"IBEAM"``, ``"WAIT"``, ``"CROSSHAIR"`` or ``"HAND"``.

    To use an image in your
    :ref:`images resource folder <deep_dive_resources>`, set the cursor to the
    image string name. For example: ``mouse.cursor = "sword_cursor"``.

    To apply a custom hotspot to your image cursor, set ``cursor`` to a tuple
    of the image name and the hotspot as a position tuple:
    ``mouse.cursor = ("sword_cursor", (4, 2))``

    Default value: ``("ARROW", None)``

.. attribute:: cursor_name

    Returns the current name string of the mouse cursor.

    Default value: ``"ARROW"``

.. attribute:: cursor_hotspot

    Returns the hotspot tuple of the current cursor or ``None`` if the hotspot
    is unknown (because it is a system cursor).

    Default value: ``None``


.. _reference_mouse_constants:

Constants
---------

When using hooks like ``on_mouse_down(button)`` to react to mouse events, use
the following constants defined for mouse to check which button was pressed.

Example: ``if button == mouse.LEFT:``

- ``mouse.LEFT`` (value ``1``)
- ``mouse.MIDDLE`` (value ``2``)
- ``mouse.RIGHT`` (value ``3``)
- ``mouse.WHEEL_UP`` (value ``4``)
- ``mouse.WHEEL_DOWN`` (value ``5``)


.. _reference_mouse_changelog:

Changelog
---------

* **1.4:** First release of PGTurbo after fork from PGZero. Introduced the
  ``mouse`` builtin with all its properties.
