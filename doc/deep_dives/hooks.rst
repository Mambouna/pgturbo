.. _deep_dive_hooks:

Deep dive: event hooks
======================

:ref:`Reference page on event hooks <reference_hooks>`

An event hook generally is a function with a specific name that PGTurbo looks
out for when running your game. If you define a function with a predetermined
name that PGTurbo knows, it can then call that function whenever it is
appropriate. As such, PGTurbo "hooks" into functions you write when certain
"events" happen, thus: event hooks.

As event hooks often interact with other systems, they aren't all covered in
detail here. Instead, this deep dive tells you how they work generally and
covers event hooks that are not deeply tied into other systems.

``update()`` and ``draw()`` are covered in the
:ref:`deep dive on the game loop <deep_dive_update_draw_cycle>`, while the
:ref:`deep dive on player input <deep_dive_player_input_hooks>` covers most
others in detail.


.. _deep_dive_hooks_general_function:

General function
----------------

The two most fundamental event hook functions should be familiar from the game
loop itself: ``update()`` and ``draw()``. As mentioned before, PGTurbo will
check if your python file contains functions with these names and if yes, call
them when needed.

For the game loop, each function will be called once a frame, so the event that
the hooks are there to respond to is simply a new frame being processed. Other
functions are only called under certain circumstances however. Most other event
hooks are those called when the player makes some input. For them, the player
making some change in the input devices is the circumstance that triggers their
event hook functions being called.

``on_mouse_down()`` for example is always called when a mouse button is pressed
down. Each other input event hook similarly has a certain change in input that
will trigger it being called on. A mouse movement, a keystroke or pressing a
button on a controller.

When this happens, PGTurbo first processes these inputs internally and then
checks if you defined hook functions for the appropriate input type. If yes,
the function is called and PGTurbo will give it all appropriate arguments you
prepared it for.

This is why ``on_mouse_down()``, ``on_mouse_down(pos)`` and
``on_mouse_down(pos, button)`` definitions all work. Before actually calling
the functions, PGTurbo will check whether you want them to receive arguments.
Depending on your function definition, it will call the function with the
number of arguments you prepared for.

The limitation of this approach is that you cannot switch the order of those
arguments around. If you want to know which mouse button was pressed, you have
to define the function with two arguments and the button pressed will be the
second one.

All other hook functions work the same way. There are internal PGTurbo
processes that will call on them when appropriate and depending on how you
write the function definition, they will be called with the arguments you want.

To know what arguments you can receive in event hook functions, check the
:ref:`reference page on event hooks <reference_hooks>`. It lists all possible
event hook functions you can define and what arguments they can take.


.. _deep_dive_hooks_self_calling:

Don't call event hooks yourself
-------------------------------

If your code does something you usually want to happen when a certain key is
pressed and you've already written that functionality in the ``on_key_down()``
event hook, you might be tempted to call the function yourself. This is almost
never a good idea.

PGTurbo manages a lot of internal systems and game hook functions are your way
to connect to those systems and react to what is happening in them. If you
start calling those functions yourself, it can easily get confusing, where a
certain call came from.

For example, if you just got an automatic call of ``on_key_down()`` by PGTurbo,
you can be sure there is a key recorded as depressed in the ``keyboard``
builtin. But if you yourself start calling the function, that is no longer
true.

If you want to have certain things happen based not only on event hooks but
also when you want them to happen, it's usually best to write them in separate
functions and simply call those from an event hook::

    def jump():
        player.y = player.y - 50

    def on_key_down(key):
        if key == keys.SPACE:
            jump()

    def update():
        if timer_ran_out:
            jump()

While maybe a bit unusual to have the player jump without pressing a key, this
would be how you can safely have functionality that happens both on user input
and based on other factors, without mixing up event hook calls with your own
calls.


.. _deep_dive_hooks_general_hooks:

Hooks beside game loop and player input
---------------------------------------

The remaining event hooks beside ``update()``, ``draw()`` and the many hooks
for input events will be covered here.

One is triggered when a music track finishes playing: ``on_music_end()``. It
does not take any arguments and is only triggered when music stops either with
``music.stop()`` or a piece of music played with ``.play_once()`` finishes.

Another can be used to react to the size of the game window changing (for
example because it is set to allow resizing): ``on_window_resized()``.
This can take two arguments, ``width`` and ``height`` which will be filled with
the new dimensions of the window after the resize if used.

Note that this also triggers when the window is resized due to fullscreen mode
being activated or deactivated.

The last event hook allows you to run code before the game exits (for example
to save progress or similar): ``on_exit()``. It doesn't take any arguments and
cannot be used to prevent the exit since it will happen independently from how
this event hook is used or not.
