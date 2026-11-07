.. _deep_dive_player_input:

Deep dive: player input
=======================

This deep dive covers all relevant methods for getting player input and
reacting to it. Since these intersect with the topics of other deep dives
however (event hooks for example), they will not always be exhaustively covered
here.

Two methods for input handling
------------------------------

There are generally two distinct methods for a PGTurbo game to react to player
input.

#. Checking the current state of input devices and acting based on their
   returned values.

    Example::

        def update():
            if keyboard.space:
                player.y = player.y - 10

#. Writing functions for event hooks that involve player input and writing code
   to handle the input in those functions.

    Example::

        def on_key_down(key):
            if key == keys.SPACE:
                player.y = player.y - 100

While you can code a game using only of these options exclusively, it is
usually recommended to mix their use, since they fit different scenarios best.

Checking the state of input buttons and axes is most useful for inputs that are
expected to be held down by the player for a length of time. The most basic
example is moving an actor around. The user expects that the player character
will keep moving as long as they hold a movement button on the keyboard.

Defining event hook functions for input events is best done to check for inputs
that are meant to be singular, as in pressing the spacebar to make a character
jump for example. Most games don't allow the character to simply keep floating
up in the air, but instead expect that the player must release the spacebar
first, before another action of the same type can be made.


.. _deep_dive_player_input_properties:

Checking input properties
-------------------------

For each type of input device supported by PGTurbo, there are builtin objects
that are always accessible for you to check the state of the represented
device: ``keyboard``, ``mouse`` and ``joy``.

Each builtin has properties whose values you can only get, not set yourself.
PGTurbo automatically updates all of these properties to always reflect the
state of the represented input device.

As an example, if no keys on the keyboard are pressed, every single property of
``keyboard`` will return ``False``. If the player then presses down on the
space key of the keyboard, ``keyboard.space`` will return ``True`` as long as
the button is held down. Once let go, ``keyboard.space`` will return ``False``
again.

This way, inputs that are meant to be held down are easy to implement::

    def update():
        if mouse.pressed_left:
            player.pos = mouse.pos

        if keyboard.space:
            player.scale_x = player.scale_x * 1.05
            player.scale_y = player.scale_y * 1.05
        if keyboard.lshift:
            player.scale_x = player.scale_x * 0.95
            player.scale_y = player.scale_y * 0.95

In the example above, the player characters follows the mouse around, as long
as the left mouse button is held down. If the space or left shift key on the
keyboard are held down, the player character also grows or shrinks continually.


.. _deep_dive_keyboard:

The keyboard builtin
""""""""""""""""""""

:ref:`Reference page on the keyboard builtin <reference_keyboard>`

The ``keyboard`` builtin is the simplest of the three builtins meant to be used
to check the state of input devices. It has no properties that can be set by
you to influence its behavior and simply returns ``True`` or ``False`` for any
key you wish to check.

A full list of all keys can be found on the reference page linked above, but
generally there are four groups of keys named as follows:

* Simple letters use their letter as the name: ``keyboard.a``, ``keyboard.u``,
  etc. ...
* Special symbols use their general name: ``keyboard.enter``, ``keyboard.down``
  (arrow key pointing down), ``keyboard.colon``, etc. ...
* The number keys above the letter keys use ``k_number``: ``keyboard.k_1``,
  ``keyboard.k_7``, etc. ...
* The keys on the numpad some keyboards have use ``kp`` as a prefix:
  ``keyboard.kp4`` (the number four on the numpad), ``keyboard.kp_minus`` (the
  minus key on the numpad), etc. ...


.. _deep_dive_mouse:

The mouse builtin
"""""""""""""""""

:ref:`Reference page on the mouse builtin <reference_mouse>`

The ``mouse`` builtin is more complex than ``keyboard``. It also has properties
that return ``True`` or ``False`` based on whether mouse buttons are held down,
but it also has many properties that return more complex values like the
current position of the mouse cursor in the game window or what kind of visual
cursor is displayed.

The following properties return whether a single button is pressed or not:
``mouse.pressed_left``, ``mouse.pressed_middle``, ``mouse.pressed_right``. You
can also get the state of all three mouse buttons in a tuple like
``(True, False, False)`` with ``mouse.pressed``.


Position and movement properties
''''''''''''''''''''''''''''''''

There are a number of properties around the position of the mouse cursor:

* ``mouse.pos`` simply returns the current position as a tuple like ``(x, y)``.
* ``mouse.last_called_pos`` returns the position the mouse cursor had the last
  time this property was accessed. This might be a bit convoluted, but an
  example might illustrate it well.

    Let's say you want the player to be able to build a road in your game and
    for this the player first clicks on one point in the game window and then a
    second to set where the road starts and ends. If you read both
    ``mouse.pos`` and ``mouse.last_called_pos`` on each click, then on the
    second click, you will get the mouse position at the first point from
    ``mouse.last_called_pos`` as that property was last accessed there and the
    second point just from ``mouse.pos``.

    If this is still confusing, you don't need to make use of this property as
    you could just save the points where the mouse was clicked manually in a
    list or in many other ways.
* ``mouse.recent_pos`` returns a tuple of the last 60 mouse positions
  from the previous frames. This could be used to draw a tail along where the
  mouse was dragged for example::

    def draw():
        for position in mouse.recent_pos:
            screen.draw.filled_circle(position, 10, "blue")

For each property that reports positions of the mouse, there are also
properties that report relative movement of the mouse. These also return tuples
like ``(x, y)``, but in this case they don't report a point in the game window
but a movement in it. ``(-14, 28)`` for example means that the mouse position
moved left by 14 pixels and down by 28 pixels.

* ``mouse.rel`` returns the most recent mouse movement.
* ``mouse.last_called_rel`` returns the cumulative movement of the mouse since
  the last time the property was accessed. This is the same as the difference
  in position between the current mouse position and the mouse position when
  ``last_called_rel`` was last called.
* ``mouse.recent_rel`` returns a tuple of the 60 last recorded mouse movements,
  just like ``recent_pos`` does for actual mouse positions.


Visibility and game window focus
''''''''''''''''''''''''''''''''

Since many games hide the mouse cursor (for example if they are only controlled
by the keyboard or controllers), you can check and control cursor visibility
with ``mouse.visible``. By setting ``mouse.visible = False``, the mouse cursor
will be hidden in the game window.

Beside your game, there might also be other programs open on the PC of the
player and most operating systems allow only one program to retain focus at a
time. If you want to pause your game in case it looses focus for example, you
can check whether the game window is currently focused with ``mouse.focused``.
This property cannot be set to force the game window to get focus back, it can
only check the current status.


.. _deep_dive_mouse_cursor:

Mouse cursors
'''''''''''''

Many games change how the mouse cursor looks. PGTurbo lets you control
this by setting the ``mouse.cursor`` attribute. There are two options
here: system cursors or custom cursors.

Windows, MacOS and Linux systems all come with a variety of pre-made cursor
shapes ready to use. To change to any of them, simply use
``mouse.cursor = "ARROW"`` where *"ARROW"* is usually the default cursor on
your system. The other available strings to set system cursors to use are
*"ARROW", "IBEAM", "WAIT", "CROSSHAIR", "HAND"*.

If you want to use a custom cursor from an image you have in the *images*
:ref:`resource folder <reference_images>`, just call
``mouse.cursor = "image_name"`` and the cursor will automatically be loaded.

When using a custom cursor, you might also want to tell PGTurbo where
in the image the spot is, where an actual mouse click should occur.
By default, clicks happen at the top left corner of the cursor image, but if
you want to define a hotspot, you can give the cursor image and a position
tuple for the hotspot together when setting the cursor:
``mouse.cursor = ("image_name", (20, 20))``.

If the cursor is an image with dimensions of 40x40 pixels for example, this
would make it so mouse clicks occur at the center of the cursor image. The
hotspot position tuple is always in relation to the top left corner of the
cursor image.

System cursors define their own hotspot, so you don't have to worry about
them. This also means you can't manually check the hotspot of system
cursors with ``mouse.cursor_hotspot`` however. This will return ``None``
when a system cursor is in use.

If a custom cursor is used, you can get the image name with
``mouse.cursor_name`` and the hotspot position tuple currently active with
``mouse.cursor_hotspot``.


.. _deep_dive_joy:

The joy builtin
"""""""""""""""

:ref:`Reference page on joystick support <reference_joysticks>`

In PGTurbo, any input devices beside a keyboard and mouse are handled as
joysticks. These conform to the typical layout of a twin-stick handheld
controller, like an Xbox or Playstation controller.

Since more than one controller can be connected to a PC at a time, there is
functionality to manage them, but this is explained in more detail
:ref:`below <deep_dive_player_input_joystick_management>`.

Here's a simple example::

    def update():
        if joy.face_down:
            move_speed = 15
        else:
            move_speed = 10

        player.x = player.x + joy.left_x * move_speed
        player.y = player.y + joy.left_y * move_speed

Supporting a single controller in PGTurbo is very easy with the ``joy``
builtin. This is a builtin representing a single controller. Any input from
connected controller devices will be reflected in the state of the ``joy``
builtin.

This way, you don't have to worry about figuring out which controller
is actively being used or how to access it correctly. You also don't have to
check if any controller is connected at all. If nothing is connected, ``joy``
will simply report all buttons unpressed, both thumbsticks centered and neither
shoulder trigger pressed in at all.

Joystick objects behave a bit like ``keyboard`` and a bit like ``mouse``. They
only have properties that return the current state of the device like
``keyboard``, but some of their properties return values other than ``True``
and ``False`` like ``mouse``.

The following properties just return ``True`` or ``False`` for whether
different buttons on the controller are pressed:

* ``face_up``, ``face_down``, ``face_left``, ``face_right`` are the A, B, X and
  Y buttons on an Xbox or similar controller or the geometric shape buttons on
  a Playstation controller. Since we need consistent names, they are called by
  their position relative to each other.
* ``dpad_up``, ``dpad_down``, ``dpad_left``, ``dpad_right`` are the different
  directions of the DPAD most controllers have. To check for diagonal
  directions with the DPAD, use ``if joy.dpad_up and joy.dpad_left`` for
  example.
* ``shoulder_left`` and ``shoulder_right`` are the two pressable should buttons
  that don't track how far they are pushed in, simply whether they are pressed.
* ``push_left`` and ``push_right`` return whether the left or right thumbsticks
  are pressed in.
* ``center_left``, ``center_middle`` and ``center_right`` return whether the
  central menu buttons are pressed. Since their position differs from
  controller to controller, it can't be guaranteed that they are actually left,
  right and center, but in most cases the names should fit the locations.

Then there are a number of properties that report the state of the axis
controls of the joystick like the thumbsticks and the shoulder triggers. These
all return values between ``-1.0`` and ``1.0`` (thumbsticks) or ``0.0`` and
``1.0`` (triggers) to show how far they are deflected.

For thumbsticks, ``0.0`` means the stick is centered while for a trigger
``0.0`` means the trigger is not pressed in at all. ``-1.0`` and ``1.0`` mean a
thumbstick is pushed as far to the side as is possible and for triggers ``1.0``
means the trigger is pushed in all the way.

These are the relevant properties:

* ``left_x``, ``left_y``, ``right_x`` and ``right_y`` return how far a
  thumbstick is deflected for a single axis. For the X axis, ``-1.0`` means the
  stick is pushed all the way to the left. For the Y axis, ``-1.0`` means the
  stick is pushed all the way up.

    This is why in the example code above we use ``joy.left_x * move_speed``.
    If we just used the value of ``left_x``, the actor would move at most one
    pixel per frame.

    Instead, when working with axis inputs from controllers, you should always
    have a number for the maximum change allowed. In this case, ``move_speed``
    contains the maximum speed the actors should be able to move in a frame.
    Multiplying this with ``left_x`` means pushing the stick only halfway will
    move the actor at half of the maximum allowed speed.

* ``left_stick`` and ``right_stick`` return a tuple of the X and Y deflection
  of the thumbstick together.
* ``left_trigger`` and ``right_trigger`` return how far either trigger is
  pushed in.

Apart from these simple properties, ``left_angle`` and ``right_angle`` return
the angle that a thumbstick is currently held at. If the stick is centered,
they will return ``None`` instead. If a stick is held away from the center,
the returned angle follows the same rules as the ``.angle`` property of actors:
``0`` means straight to the right, ``90`` means straight up, ``180`` means
straight left and ``270`` means straight down.

This way, it's easy to make an actor look the same direction as a thumbstick is
held::

    def update():
        if joy.right_angle:
            player.angle = joy.right_angle

Since ``joy.right_angle`` could return ``None``, we first check whether there
is an angle to get and only then make the player character look in the same
direction.

Lastly, joystick objects can report their ``name``, ``guid`` and
``instance_id``, but these are more relevant if you want to support multiple
controllers at once in your game. For ``joy``, all of these return placeholder
values instead, since any connected controller affects the ``joy`` builtin.


.. _deep_dive_player_input_hooks:

Defining event hook functions
-----------------------------

The second way to get user inputs is to define event hook functions to react
to PGTurbo input events. Event hooks in general are introduced in more detail
in the :ref:`deep dive on event hooks <deep_dive_hooks>`, so their general use
is only briefly covered here.

To react to events that PGTurbo supports, you define functions with
predetermined names, just like ``update()`` and ``draw()``::

    def on_key_down(key):
        if key == keys.SPACE:
            player.y = player.y - 50

The event hook function above is called by PGTurbo each time a keyboard key is
pressed down when it was not pressed before, so there are no no repeat events
for keys that are held down. This means that reacting to events is suitable for
inputs that should occur as single actions without being held down.

Event hook functions can be defined with different amounts of parameters. If
the example above didn't include the parameter ``key`` for ``on_key_down()``,
the function would still be called for each key being pressed down, but you
wouldn't be able to distinguish which key was being pressed.

For keyboard events, it usually doesn't matter that you can leave out
parameters, but for mouse events for example you can either receive them with
just the position the press occurred at at or also with the button that was
pressed.


Event hooks for keyboard inputs
"""""""""""""""""""""""""""""""

There are two event hooks defined for keyboard events: ``on_key_down()`` and
``on_key_up()``. These are always called when a keyboard key is either
initially pressed down or released.

The first optional parameter you can define the hooks with is ``key``. This
will be an identifier you can use to check which key was pressed down or let
go of. To do this, you compare ``key`` to a keyboard key constant like
``keys.ENTER`` or ``keys.A``. 

The keyboard key constants are written the same way as ``keyboard`` properties
for checking a button is held down, but they are written in UPPERCASE and
accessed on the ``keys`` builtin instead.

The reason you can't use ``keyboard.key`` for this is that the ``key`` argument
is filled with an internal integer number that represents a key, whereas
``keyboard.key`` always returns either ``True`` or ``False``.

The second optional parameter you can get is ``mod``. This is a single value
representing the modifier keys held while a key was pressed down or released.
You can use this to distinguish the A key being pressed normally or with the
Shift key also held for example.

The details of how bitmasks work are a bit much for this deep dive. For our
purposes, all that is relevant is that you can check the ``mod`` value against
constants just like you can do with ``key`` to figure out if and what modifiers
were held during the event.

You do this with the ``keymods`` constant values. Checking if a modifier was
held is done like this::

    def on_key_down(key, mod):
        if mod & keymods.SHIFT:
            sprinting = True
        else:
            sprinting = False

To see if no modifiers were held at all, you can use
``if mod == keymods.NONE:``. The ``.SHIFT`` modifier checked above will work
if either the left shift or right shift key or both were held down. For each
type of modifier where there are multiple physical keys, there are constants
for each physical key and a general one for the type of modifier.

A list of all ``keymods`` constants can be found in the
:ref:`reference page on the keyboard <reference_keyboard>`.

The third possible parameter is ``unicode``. If you define the hook with this
parameter, it will be filled with the printable unicode character resulting
from the made keystroke. For simple letter keys with no modifiers pressed,
this will just be that letter as a string, for example ``"a"`` or ``"5"``.

If modifiers are being held, then ``unicode`` contains the printable character
resulting from the combination of the hit key and all active modifiers, for
example ``"!"`` for the number key 1 with modifier shift held. If there is no
printable character from the keystroke, ``unicode`` will contain an empty
string: ``""``.

Note that ``unicode`` is only available for ``on_key_down()``, not
``on_key_up()`` since releasing a key cannot produce a printable character.
``key`` and ``mod`` are available and behave the same for ``on_key_up()`` as
for ``on_key_down()``.


Event hooks for mouse inputs
""""""""""""""""""""""""""""

As with keyboard events, there are two event hook functions for mouse button
events: ``on_mouse_down()`` and ``on_mouse_up()``. Their possible parameters
are different from the keyboard events, however. Both mouse button hooks can
take the same parameter.

The first paramater is ``pos``, which contains a position tuple like ``(x, y)``
indicating where in the game window the mouse press occurred. The second is
``button``, which contains a mouse button constant that identifies the mouse
button that was pressed down or released.

As with ``key`` and ``keys``, you cannot compare ``button`` to mouse properties
like ``mouse.pressed_left``. For the mouse however, the constants are stored
in the same builtin: ``mouse``. Here's an example::

    def on_mouse_down(pos, button):
        if button == mouse.LEFT:
            player.pos = pos

The available constants for mouse buttons are ``mouse.LEFT``, ``mouse.MIDDLE``
and ``mouse.RIGHT``.

In addition to the button events, there is also an event hook for mouse
movement: ``on_mouse_move()``. This is called each time an individual mouse
movement is recorded by the operating system and could thus happen multiple
times for a single frame.

As with the button events, the first parameter for ``on_mouse_move()`` is
``pos``, which works the same way as above. The second is ``rel``, which is
given a tuple similar to a position tuple but which indicates how far the mouse
was moved in either axis. An example would be ``(12, -8)``, indicating the
mouse was moved right by 12 pixels and up by 8 pixels in the movement.

The third possible parameter for ``on_mouse_move()`` is ``buttons``, which is
a set containing all the mouse buttons that were depressed during the move. To
check if a button was held during a mouse move, you can do the following::

    def on_mouse_move(pos, rel, buttons):
        if mouse.RIGHT in buttons:
            player.x = player.x + rel[0]
            player.y = player.y + rel[1]

The code above would drag the player actor along the same movements as the
mouse if the right mouse button is held down.


Event hooks for joysticks
"""""""""""""""""""""""""

Three event hook functions for joysticks mirror those for the mouse:
``on_joy_down()``, ``on_joy_up()`` and ``on_joy_move()``. Their possible
parameters are different again though.

The first is ``joybtn`` for ``on_joy_down()`` and ``on_joy_up()`` with the same
functionality as ``key`` for keyboard events. Compare the value of ``joybtn``
to a ``joybutton`` constant like ``joybutton.FACE_DOWN`` to identify which
button was pressed::

    def on_joy_down(joybtn):
        if joybtn == joybutton.FACE_DOWN:
            player.y = player.y - 50

The button constants match the properties on ``joy``, just like keyboard
constants match the ``keyboard`` builtin properties: ``joybutton.FACE_UP``,
``.FACE_DOWN``, ``.FACE_LEFT``, ``.FACE_RIGHT``, ``.DPAD_UP``, ``.DPAD_DOWN``,
``.DPAD_LEFT``, ``.DPAD_RIGHT``, ``.SHOULDER_LEFT``, ``.SHOULDER_RIGHT``,
``.PUSH_LEFT``, ``.PUSH_RIGHT``, ``.CENTER_LEFT``, ``.CENTER_MIDDLE`` and
``.CENTER_RIGHT``.

There are no modifier key masks or unicode symbols for ``on_joy_down()`` and
``on_joy_up()``.

``on_joy_move()`` has ``axis`` as its first parameter, which you can compare to
a ``joyaxis`` constant to figure out which axis recorded a movement. Typical
axes for a dualshock style controller are an X and Y axis for each thumbstick
as well as two axes for the shoulder triggers.

As above, the constants follow the ``joy`` properties: ``joyaxis.LEFT_X``,
``.LEFT_Y``, ``.RIGHT_X``, ``.RIGHT_Y``, ``.LEFT_TRIGGER`` and
``.RIGHT_TRIGGER``.

The second parameter for axis movement hooks is ``value``, which contains a
float number in the range of ``-1.0`` to ``1.0`` for thumbstick axes or ``0.0``
to ``1.0`` for shoulder triggers.

For thumbsticks, ``-1.0`` indicates the stick is held fully left or fully up
depending on the axis and ``1.0`` indicates fully right or fully down. ``0.0``
means the stick is centered. For shoulder triggers, ``0.0`` means the trigger
is not pressed in at all and ``1.0`` means it is fully pressed in.

Since controllers might be disconnected and reconnected while a game is
running, there are two more event hooks for joysticks: ``on_joy_added()`` and
``on_joy_removed()``. These only have a single possible parameter, which they
share with all other joystick events: ``instance_id``. With these events, you
could assign new controllers if a previously used one was disconnected.

``instance_id`` is the identifier with which you can tell which specific
joystick device connected to the computer was the one that had a button pressed
or an axis moved. More details on this are found below in the section on
:ref:`joystick management <deep_dive_player_input_joystick_management>`.

.. tip::

   The ``instance_id`` parameter for event hook functions and the ``joysticks``
   management builtin discussed below are only relevant if you want to support
   multiple controllers being used at the same time in your game. If you just
   need controller support for single player gaming, stick to using the ``joy``
   builtin and ignore ``instance_id`` as a parameter and you will be just fine.


.. _deep_dive_player_input_joystick_management:

Joystick management
-------------------

If you want two players to be able to play your game with two controllers at
the same time, you cannot use ``joy`` for controller inputs anymore. Both
players making inputs on their individual controllers will constantly change
the state of ``joy``, since it follows ALL connected joystick devices.

Instead, you have to assign the different controllers to the players directly
and then only react to the inputs of the respective device for each player.
To do this, we have to talk about the ``joysticks`` builtin. This is a manager
object through which you can access all the connected joystick devices::

    if joysticks.num >= 2:
        con_ids = joysticks.ids
        player_1_con = joysticks[con_ids[0]]
        player_2_con = joysticks[con_ids[1]]

What happened up there? First, ``joysticks.num`` returns the total number of
connected joystick devices. So in the code above, we assign multiplayer
controls only if there are two or more controllers connected.

Second, we get a tuple of all the IDs that identify the different controllers
with ``joysticks.ids``. Each connected joystick device gets assigned an
*instance ID*, and you can get the actual joystick object from ``joysticks``
with ``joysticks[id]``.

This is what is done in the last two lines. We get the joystick devices with
the first two instance IDs and assign them to variables so we can easily access
them later. ``joysticks`` acts like a dictionary that you can only read from,
not write to. It holds all the connected joystick objects.

Once you have access to a joystick objects, it acts exactly the same way
``joy`` did before, just that only inputs from that specific controller will
change the state of the joystick object. Additionally, the ``name``, ``guid``
and ``instace_id`` properties will report their actual values for individual
joysticks.

Here's an example of how two different actors could be moved with two different
connected controllers::

    def update():
        if player_1_con:
            p1_actor.x = p1_actor.x + player_1_con.left_x * move_speed
            p1_actor.y = p1_actor.y + player_1_con.left_y * move_speed

        if player_2_con:
            p2_actor.x = p2_actor.x + player_2_con.left_x * move_speed
            p2_actor.y = p2_actor.y + player_2_con.left_y * move_speed

Since we aren't working with ``joy`` anymore but with specific devices,
we always have to make sure to account for the possibility of them being
disconnected.

If that happens, whatever access method we used before (directly via
``joysticks`` or with a variable) will return ``None`` instead. This way,
simply checking ``if con_object:`` let's us only run code if a valid device can
be reached.

.. warning::

    Since ``joysticks`` automatically updates the connected controllers, we
    can't change the contents of the "dictionary" it represents. Trying to do
    something like ``joysticks[5] = ...`` will result in an error.


Last used device
""""""""""""""""

It's common to assign controllers based on which one was last used. To
make this possible, ``joysticks.last_used`` returns the Joystick object
that last recorded an input.

If you want your players to be able to pick their controllers, simply tell them
to make any input and then assign them ``joysticks.last_used`` one after the
other.


Instance IDs and event hooks
""""""""""""""""""""""""""""

As mentioned above, the *instance ID* uniquely identifies each connected
controller. This is why ``instance_id`` is the last possible parameter for all
joystick event hooks. If you want to distinguish player controllers in event
hook functions, you must check them and apply the correct behavior based on
the result::

    def on_joy_down(joybtn, instance_id):
        if joybtn == joybutton.FACE_DOWN:
            if instance_id == player_1_con.instance_id:
                p1_actor.y = p1_actor.y - 50
            elif instance_id == player_2_con.instance_id:
                p2_actor.y = p2_actor.y - 50

In this case, we first check what button was pressed and then which player
character to apply the behavior to. For complex controls with many options
however, this can lead to a lot of repeated code. It can be more elegant to
check which actor to manipulate first and leave the rest of the code alone::

    def on_joy_down(joybtn, instance_id):
        if instance_id == player_1_con.instance_id:
            correct_actor = p1_actor
        elif instance_id == player_2_con.instance_id:
            correct_actor = p2_actor
        else:
            return

        if joybtn == joybutton.FACE_DOWN:
            correct_actor.y = correct_actor.y - 50

Above, we assign the player character of the controller whose button was
pressed to a local variable and then just act on this actor in the rest of the
logic. Since a button could have been pressed on a controller that is neither
assigned to player one or player two, we exit the function execution directly
if the instance ID of the action matches neither player.

While this looks like more effort for checking a single button, the more
different buttons you need to handle, the more this approach will be worth it.

.. tip::

    Controller management is a difficult problem to solve because there are so
    many edge cases to worry about. If you are just learning to develop games,
    it's fine to code controls for two controllers and not worry about every
    possibility. If the game works well under the conditions you accounted for,
    that's already a big success.
