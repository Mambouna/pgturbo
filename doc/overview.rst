.. _overview:

Overview
========

This is an overview of most of the important builtin objects and functions of
PGTurbo. If you don't know where to look for in the documentation, look over
the summaries here and then go to the linked deep dives or references.


.. _overview_installation_and_running_a_game:

Installation and running a game
-------------------------------

To install PGTurbo, execute the command ``python -m pip install pgturbo``.

To run a PGTurbo game, there's two options:

#. Use the ``pgtrun game.py`` command, substituting the name of your script.
#. Put ``import pgtrun`` at the very top of your script, ``pgtrun.go()`` at the
   very bottom of it and run the script through python: ``python game.py``.

Even a completely empty file is a valid PGTurbo game, so try it out and check
that an empty game window opens.

You can close the window via the X button of the game window or with the key
combination ``Ctrl+Q``.

To learn more, check out the
:ref:`deep dive on installation and running game files
<deep_dive_installation_and_running>`.


.. _overview_update_draw:

The update/draw cycle
---------------------

Game development with PGTurbo uses the update/draw cycle. This means we
separate game logic from displaying the game on screen.

In the update step, we run any logic that changes the game state, like
characters moving or player input. In the draw step, the state of the game is
displayed, for example all characters drawn or text rendered. Then a cycle is
done and we repeat:

.. image:: _static/update_draw_diagram.png

To follow this design principle, we just write a function for each step:
``update()`` and ``draw()``. With both defined, PGTurbo runs each once a frame,
taking care of the game loop for us::

    # Code to setup the the initial game state here.

    def update():
        # Code to change the state of the game here.

    def draw():
        # Code to display the game here.

For a more detailed explanation, check the
:ref:`deep dive on the update/draw cycle <deep_dive_update_draw_cycle>`.


.. _overview_actors:

Actors - game objects
---------------------

Actors are the fundamental game objects of PGTurbo, each having an image and
a variety of different properties and methods handy for games.

Here's a quick example of an actor in action::

    player = Actor("alien")
    player.pos = (50, 50)

    def update():
        if keyboard.left:
            player.x = player.x - 10
        if keyboard.right:
            player.x = player.x + 10

    def draw():
        screen.clear()
        player.draw()

The string in ``Actor()`` tells PGTurbo which image to load for the new actor.
You give the image name without its file extension and it has to be placed in
a folder named *images*, which is next to your game file.

Actors are manipulated by changing their various properties in the ``update()``
function and finally drawn to the game window with their own ``draw()`` method
in the global ``draw()`` function.

The following are some of the important properties and methods of actors:

* ``Actor.pos`` is the current position as a tuple. ``.x`` and ``.y`` are only
  the X or Y position each. Set them to move the actor around the game world.
* ``Actor.angle`` is the rotation of the actor, ``0`` meaning the actor "looks"
  straight to the right. The possible values range from ``0`` to ``359``.
* ``Actor.scale`` is how enlarged or shrunk the actor is, ``1.0`` being normal
  size. ``0.5`` then is half size and ``2.0`` doubled size.
* ``Actor.draw()`` is the most important method for any actor. It's used in
  the ``draw()`` function to display the actor on the screen.
* ``Actor.distance_to(target)`` and ``Actor.angle_to(target)`` are useful to
  figure out where things are in relation to an actor.
* ``Actor.colliderect(target)`` checks whether two actors are colliding with
  each other.

There's far more to learn, so read the
:ref:`deep dive on actors <deep_dive_actors>` to get all the details.


.. _overview_screen:

Screen - displaying anything
----------------------------

In the ``draw()`` function, you write all code that displays the game state.
This should usually always start with either ``screen.clear()`` or
``screen.fill(color)``, to overwrite the visuals left from the previous frame.

``screen.clear()`` wipes the game window to black, while ``.fill(color)``
paints everything in the given color. Colors in PGTurbo can always be either a
string like ``"red"`` or an RGB tuple like ``(128, 0, 96)``.

After having a solid background color, you draw everything in the frame on top.
This will be actors that you call ``Actor.draw()`` on, but maybe also general
shapes or text. For this, there's the ``screen.draw`` module:

* ``screen.draw.line(startpos, endpos, color)``
* ``screen.draw.circle(position, radius, color)``
* ``screen.draw.rect(rect, color)``
* ``filled_circle()`` and ``filled_rect()`` are also available.
* ``screen.draw.text(text, **options)``

There's many more possibilities and deep customization explained in the
:ref:`deep dive on the screen builtin <deep_dive_screen>`.


.. _overview_game_window:

Setting up the game window
--------------------------

The game is displayed in a window on your computer. To change the properties
of the game window, you set certain predetermined global variables. The
simplest of these control the size of your game window::

    WIDTH = 600
    HEIGHT = 400

Typically, you put the settings for the game window at the top of the program
where you set up the rest of the game's starting state. You can also change
them later though, for example to allow the user to set whether the game should
be in fullscreen mode or not. Any change to the variables immediately updates
the game window.

To learn about all the available variables, check the
:ref:`deep dive on the game window <deep_dive_game_window>`.


.. _overview_player_input:

Player input - keyboard and mouse
---------------------------------

All games need player input. It's easy to check whether a keyboard button is
pressed or where the mouse currently is::

    if keyboard.space:
        move_speed = 10
    else:
        move_speed = 5

    if mouse.pressed_left:
        alien.move_towards_point(mouse.pos, move_speed)

For each keyboard button, ``keyboard.identifier`` will return ``True`` if
pressed and ``False`` if not. The same is true for ``mouse.pressed_left`` as
well as the middle and right button. Additionally, you can get the current
position of the mouse in the game window with ``mouse.pos``.

Read more about the different options in the deep dive on
:ref:`player input <deep_dive_player_input>`.


.. _overview_event_hooks:

Event hooks - reacting to events
--------------------------------

Checking what buttons are currently held is good for continuous inputs, like
for player movement. For singular input events, hooks are usually better::

    def on_key_down(key):
        if key == keys.SPACE:
            player_jump()

Event hooks are run once whenever certain things that are tracked by PGTurbo
happen. To use them, you define a function with a predetermined name and
PGTurbo automatically picks it up and runs it when appropriate.

The basic input event hooks are ``on_key_down()`` / ``_up()``,
``on_mouse_down()`` / ``_up()`` and ``on_mouse_move()``. Each hook has preset
argument names that you can include in your definition to check for example
which button was pressed down or where the mouse moved.

Beside input there's also general hooks: ``on_music_end()`` or ``on_exit()``.

All the available event hooks are explained in the
:ref:`deep dive on event hooks <deep_dive_hooks>`.


.. _overview_clock:

Clock - time management
-----------------------

Many games do things in certain time intervals or allow some actions only after
a set waiting period. For this, PGTurbo has the ``clock`` builtin. It's main
feature is being able to schedule a function to be called after a delay::

    def spawn_apple():
        # Code to spawn an apple here...

    clock.schedule_interval(spawn_apple, 5.0)

The code above calls the function ``spawn_apple()`` every five seconds. The
clock has ``schedule()`` to trigger a function once after the delay or
``schedule_interval()`` to call after every timer interval again.

*Note:* It's important to give the function name WITHOUT () parentheses here.

Besides scheduling, ``clock`` can also tell you how much time has elapsed since
program start or since a time mark you set previously or track ready timers
for you.

These options are explained in the :ref:`deep dive on clock <deep_dive_clock>`.


.. _overview_music_and_sounds:

Music and sounds
----------------

To play music and sounds, you need to put the audio files in *sounds* and
*music* directories next to your game's ``.py`` file, just like with
*images* for actors before.

Once done, you can play any sound with ``sounds.filename.play()`` and the same
is true for music files: ``music.filename.play()``.

The difference between the two is that ``music`` loads audio files in small
chunks at a time, so you should use ``music`` for longer files that play
continuously and ``sounds`` for short sound effects that play repeatedly but
aren't long individually.

As a last option, you can also let PGTurbo synthesize short sine wave tones for
you::

    tone.play("E4", 1.5)

The controls for all three are found in the
:ref:`deep dive on music and sounds <deep_dive_audio>`.


.. _overview_property_animation:

Property animation
------------------

While actors have a deep sprite animation system (see the
:ref:`actor deep dive <deep_dive_actors>`), you can also "animate" in the sense
of smoothly transitioning values between a starting and end point.

The ``animate()`` function allows you to automatically have a property, for
example the position of an actor, shift over time to a target value::

    animate(alien, pos=(120, 80))

This will smoothly change the ``.pos`` of the ``alien`` actor from it's current
value when called to the target value of ``(120, 80)`` in one second.

To control how the transition happens, you can set different tweening styles
and how long the change takes. To have the same happen over two seconds with
the transition starting slow and then speeding up, you can use the following::

    animate(alien, tween="accelerate", duration=2.0, pos=(120, 80))

All the tweening options are in the
:ref:`deep dive on the animate function <deep_dive_property_animation>`.

.. _overview_resources_and_save_data:

Resources and save data
-----------------------

As mentioned above multiple times, PGTurbo automatically looks for some folders
placed next to your game's ``.py`` file, like *images*, *music* and others.

PGTurbo caches all of these resources, so you don't have to worry about
"loading" the same image for twenty actors again and again. Internally it only
happens once so no memory or performance is wasted.

In a different topic, PGTurbo also allows you to store persistent data
like save data or configuration values betweens runs of the game with the
``storage`` builtin.

This acts like a normal dictionary that you can also call ``.save()`` and
``.load()`` on to write or read it from disk. There are some pitfalls to its
use though, so it is recommended to read the deep dive before utilizing it.

Details on ``storage`` as well as supported file formats and the necessary
naming scheme for resources are found in the
:ref:`deep dive on resources and storage <deep_dive_resources_and_storage>`.


.. _overview_joysticks_and_controllers:

Joysticks and controllers
-------------------------

PGTurbo has easy controller support for single player games built in::

    if joy.face_down:
        move_speed = 10
    else:
        move_speed = 5

    alien.x = alien.x + joy.left_x * move_speed
    alien.y = alien.y + joy.left_y * move_speed

``joy`` is an object that accepts inputs from any connected controller, so you
can always use it for joystick controls.

Checking button states is the same as for ``keyboard``, but joysticks also
have axes like ``joy.left_x``. Each axis can either have values ranging
from ``-1`` to ``1`` or ``0`` to ``1``, indicating how far they are
deflected.

You can find all the buttons, axes and how to support multiple controllers in
the
:ref:`deep dive on joystick / controller support <deep_dive_joy>`.
