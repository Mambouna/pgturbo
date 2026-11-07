.. _reference_joysticks:

Reference: joysticks / controllers
==================================

:ref:`Deep dive on joystick support <deep_dive_joy>`

Both the ``joy`` builtin virtual joystick as well as individual connected
devices accessed via ``joysticks[instance_id]`` are ``Joystick`` objects and
have the same properties.


.. _reference_joysticks_joystick_properties:

Joystick Properties
-------------------

.. attribute:: face_up

    Returns ``True`` if the upper face button is currently held down.
    ``face_down``, ``face_left`` and ``face_right`` are also
    available.

.. attribute:: dpad_up

    Returns ``True`` if the DPAD is held up. ``dpad_down``,
    ``dpad_left`` and ``dpad_right`` are also available.

.. attribute:: shoulder_left

    Returns ``True`` if the left shoulder button is pressed down.
    ``shoulder_right`` is also available.

.. attribute:: push_left

    Returns ``True`` if the left thumbstick is pressed in.
    ``push_right`` is also available.

.. attribute:: center_left

    Returns ``True`` if the left most button on the controller front is
    pressed. ``center_middle`` and ``center_right`` are also
    available.

    *Note:* Left, middle and right buttons usually correspond to the
    physical locations on the controller, but there may be some devices
    where this is not true.

.. attribute:: left_x

    Returns the value of the X axis of the left thumbstick (horizontal
    movement). Values range from ``-1`` to ``1`` with ``-1`` being fully
    pressed left, ``0`` being centered and ``1`` being fully pressed right.
    ``right_x`` is also available.

.. attribute:: left_y

    Returns the value of the Y axis of the left thumbstick (vertical
    movement). Values range from ``-1`` to ``1`` with ``-1`` being fully
    pressed up, ``0`` being centered and ``1`` being fully pressed down.
    ``right_x`` is also available.

.. attribute:: left_stick

    Returns the values of both axes of the left thumbstick as a tuple of
    two floats between ``-1`` and ``1``. ``right_stick`` ist also available.

.. attribute:: left_angle

    Returns the angle to which the left thumbstick is currently held with
    ``0`` degrees indicating straight right (see
    :ref:`rotation <deep_dive_actors_angle>` of Actors). ``right_angle`` is
    also available.

    If the stick is centered, ``None`` is returned.

.. attribute:: left_trigger

    Returns the value of the left trigger axis as a float between ``0`` and
    ``1`` with ``0`` being unpressed and ``1`` being fully pressed in.
    ``right_trigger`` is also available.

.. attribute:: name

    Returns the human readable name of the controller as a string.

    *Note:* Since the ``joy`` builtin is a virtual controller affected by all
    connected devices, it has a placeholder ``name``.

.. attribute:: guid

    Returns the unique hardware identifier of the controller as a string.

    *Note:* Since the ``joy`` builtin is a virtual controller affected by all
    connected devices, it has a placeholder ``guid``.

.. attribute:: instance_id

    Returns the integer index by which the controller is identified in
    PGTurbo. This is used to get access to a specific controller (see
    :ref:`joystick management <deep_dive_player_input_joystick_management>`) or
    to determine which controller triggered an event.

    *Note:* Since the ``joy`` builtin is a virtual controller affected by all
    connected devices, it has a placeholder ``instance id``.


.. _reference_joysticks_joystick_manager:

Joystick manager
----------------

The ``joysticks`` builtin is an automatically managed dictionary that can be
used to access individual connected joystick devices. As such, writing to it
manually or trying to call normal dict functions that modify the contents
cause an error.

To get the ids of all connected devices, you can use ``joysticks.ids``. To
access an individual device, then use ``joysticks[id]``.

The following properties are available:

.. attribute:: num

    Returns the number of connected devices.

    This is identical to ``len(joysticks)``.

.. attribute:: ids

    Returns a tuple of all connected device ids.

.. attribute:: last_used

    Returns the ``Joystick`` object that last had an input event.

The usual dictionary methods that don't alter the contents are also there:

.. method:: keys()

    Returns the ids of all connected devices in an iterable.

.. method:: values()

    Returns all connected ``Joystick`` objects in an iterable.

.. method:: items()

    Returns tuple pairs of instance id and ``Joystick`` object of all connected
    devices in an iterable.


.. _reference_joystick_constants:

Constants for event hooks
-------------------------

When using hooks like ``on_joy_down(joybtn)`` or ``on_joy_move(axis)`` to react
to joystick events, use the ``joybutton`` and ``joyaxis`` enum constants to
check which button was pressed or axis was moved. ``joy`` can't be used, since
its properties just return booleans of whether something is pressed.

Example: ``if axis == joyaxis.LEFT_X:``

.. class:: joyaxis

    .. attribute:: LEFT_X
    .. attribute:: LEFT_Y
    .. attribute:: LEFT_TRIGGER
    .. attribute:: RIGHT_X
    .. attribute:: RIGHT_Y
    .. attribute:: RIGHT_TRIGGER
    .. attribute:: UNKNOWN

Whenever an axis is used that is not recognized for the standard layout
PGTurbo supports, the ``UNKNOWN`` axis is reported used.

Example: ``if joybtn == joybutton.FACE_DOWN:``

.. class:: joybutton

    .. attribute:: FACE_UP
    .. attribute:: FACE_DOWN
    .. attribute:: FACE_LEFT
    .. attribute:: FACE_RIGHT
    .. attribute:: DPAD_UP
    .. attribute:: DPAD_DOWN
    .. attribute:: DPAD_LEFT
    .. attribute:: DPAD_RIGHT
    .. attribute:: SHOULDER_LEFT
    .. attribute:: SHOULDER_RIGHT
    .. attribute:: PUSH_LEFT
    .. attribute:: PUSH_RIGHT
    .. attribute:: CENTER_LEFT
    .. attribute:: CENTER_MIDDLE
    .. attribute:: CENTER_RIGHT
    .. attribute:: UNKNOWN

Whenever a button is used that is not recognized for the standard layout
PGTurbo supports, the ``UNKNOWN`` button is reported used.


.. _reference_joystick_changelog:

Changelog
---------

* **1.4:** First release of PGTurbo after fork from PGZero. Added the full
  joystick support of PGTurbo.
