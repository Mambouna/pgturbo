.. _deep_dive_update_draw_cycle:

Deep dive: the update/draw cycle
================================

Fundamentally, running a video game means executing certain code over and over
again and again: Code to draw graphics to a game window, code to check whether
the user has made inputs, code to update the position of game objects or other
values that should change over time.

How all of these repeating requirements are met can broadly be called a **game
loop**. A loop of steps or program code that is executed over and over again,
forming the logic and behavior of a video game.

There are different approaches for how all of those requirements are split up
and their execution organized. Pygame Turbo follows one common way to do so:
the **update/draw cycle**.


.. _deep_dive_update_draw_game_state:

The game state
--------------

To understand the update/draw cycle, we must first understand what the game
state is. In any video game, there are a number of variables that track the
current state of different concepts important to the game. The position of
game objects, a score that the player is trying to raise, how much time has
passed since a certain trigger was activated and many other things.

All of these variable values together are the game state. In the update/draw
cycle, each repetition of the game loop centers around the following concept:
first change the game state based on elapsed time and user input, second draw
the graphics to the game window that represent the updated game state.


.. _deep_dive_update:

The update step
---------------

The update step is the first step that was just mentioned. There is a certain
previous game state, but since it was determined (since the last time the code
for the update step was run) some time has passed and maybe the user started
pressing down on a keyboard key. So we must transition from the previous game
state to a new one by reacting to the changed circumstances.

When we define a function named ``update()`` in our game script, PGTurbo will
automatically find it and call it every single cycle of the game loop. Any code
we write in the ``update()`` function thus becomes the code for the update step
of the update/draw cycle.

Here's a simple practical example::

    WIDTH = 400
    HEIGHT = 100
    player = Actor.Ellipse(40, 40, "blue")

    def update():
        if player.x < WIDTH:
            player.x = player.x + 10
        else:
            player.x = 0

*Note: If you aren't familiar with actors yet, they are game objects in PGTurbo
and their X property is simply their position on the X axis.*

Above, there are four lines of code that will be run by PGTurbo automatically
every single frame. They check the current position of a game object and
according to the result update it either by changing it a bit or resetting it.

If you were to copy this code into a game script and execute it however, you
would not see anything happening. This is because we have so far only done the
first of the two steps in each repetition of the update/draw cycle.


.. _deep_dive_draw:

The draw step
-------------

After the game state has been changed in ``update()``, it must be displayed to
the user in the game window. That is the sole responsibility in the draw step.
As such, the code of the draw step should never change the game state.

Pygame Turbo also has a preset function name for the draw step that it will
automatically find and execute each frame: ``draw()``.

To actually see the circle from the last example move across the screen, the
following code would work::

    WIDTH = 400
    HEIGHT = 100
    player = Actor.Ellipse(40, 40, "blue")

    def update():
        if player.x < WIDTH:
            player.x = player.x + 10
        else:
            player.x = 0

    def draw():
        screen.clear()
        player.draw()

Both of the lines of code in ``draw()`` create graphics in the game window.
``screen.clear()`` fills everything with black while ``player.draw()`` displays
an actor game object. Note that neither of these change any of the values
representing the game state, only showing the game state in its current form
to the player.

In more complex games, the code in ``draw()`` will also require control logic
like conditionals or loops. While those are used in ``update()`` to control how
the game state is changed, they can also be necessary in ``draw()`` to
determine which graphics to draw or to go through a list of game objects and
draw all their graphics.

Any of the lines changing ``player.x`` however should never be put in
``draw()``, since they change the game state.


.. _deep_dive_startup_code:

Startup code
------------

Looking at the example code above again, it's obvious which code belongs to
the update step and which to the draw step of the cycle, since both are in
their respective functions. But why is there also code outside of both
functions?

When a game is first launched, there needs to be an initial game state before
the update/draw cycle can be started. This starting game state is established
by startup code.

In Pygame Turbo, any code placed in the global scope of the program itself
(outside of any function) is executed at the very start of the game and thus is
the startup code.

In the example above, the three lines setting ``WIDTH``, ``HEIGHT`` and
``player = Actor.Ellipse(40, 40, "blue")`` are the entire startup code of the
game. For a more complex game, many more variables would be created to track
all the different systems of the game and each of their initial values together
would make up the initial game state.

To keep the code of your game organized, it's recommended to follow the general
structure outlined below::

    # Code to setup the the initial game state here.

    def update():
        # Code to change the state of the game here.

    def draw():
        # Code to display the game state here.


.. _deep_dive_update_deltatime:

Framerates and delta time
-------------------------

The example code above is quite simple, so even PCs with weaker hardware are
able to execude all that code hundreds or thousands of times a second. So why
isn't the game object zipping across the game window at lightning speed?

Pygame Turbo automatically tries to keep the framerate of games at around 60
frames per second (FPS). This allows you to write your games without worrying
about framerates and delta time if you don't want to. In this case, you can
skip this section.

If you do want to take FPS into consideration or need to, because your game
project is so complicated that it's starting to run at different speeds on
different computers, then read on below.

The *framerate* of a game is how many times a second the code of the game loop
runs. If the code of the game does not take the framerate into account for how
far it moves game objects for example, then the same game will look like things
are moving around faster on stronger PC hardware and slower on weaker hardware.

This is because if a game object is moved ``10`` pixels every frame (cycle of
the game loop), then if there are more frames in a second, then the game object
will also be moved further in a second.

This is usually undesirable however. We want our game's mechanics to work at
the same speed no matter what kind of hardware the game is played on. As
mentioned before, PGTurbo helps with that by automatically limiting the game
to 60 FPS.

For complex projects however, that will not always be possible. So in those
cases, your game code needs to account for the frame rate and make sure
everything happens at the correct speeds anyway. That is where *delta time*
comes in.

Delta time is the time that has passed since the last cycle of the game loop.
By tying all the code of our game that moves things around or relies on timing
things to delta time, we can make it independent of framerate. If the game runs
faster, delta time will be smaller each frame and so movements and timing code
will take smaller steps. If the game runs slower, delta time will be larger and
so movements and value changes will be bigger each frame.

Most of the time, tying something to delta time simply means multiplying it by
delta time::

    WIDTH = 400
    HEIGHT = 100
    player = Actor.Ellipse(40, 40, "blue")

    def update(dt):
        if player.x < WIDTH:
            player.x = player.x + 10 * dt
        else:
            player.x = 0

    def draw():
        screen.clear()
        player.draw()

There are only two small changes to the way the code worked before:

#. The function signature of ``update()`` now has a parameter named ``dt``.
#. The distance the game object moves each frame is not just ``10`` anymore,
   but ``10 * dt``.

``dt`` is delta time here. If we write ``update()`` with one parameter instead
of none, then PGTurbo passes the elapsed time since the last frame in seconds
as an argument to each call of ``update()``.

As mentioned before then, to tie the movement of the circle in the game code
to delta time, we simply multiply the value by ``dt``. If you run the code
above however, you will notice that the circle moves far slower than before.

When you tie your game code to delta time, any values that you multiply by
``dt`` will be the value for a whole second (because delta time is the elapsed
time since the last frame in seconds). For the example above, after tying the
movement to ``dt``, the circle will then move only ``10`` pixels in a whole
second.

How fast was the circle moving before? As mentioned before, PGTurbo tries to
keep games running at 60 FPS. So if the circle moves ten pixels a frame and
the game should have 60 frames in a second, the circle would have moved around
600 pixels each second when not tied to ``dt``.

Because of this, the following rule of thumb applies: if you use ``update(dt)``
and multiply by delta time, any hardcoded values that affect things happening
over time will need to be much larger than if you just use ``update()`` to
achieve the same feel for the player.

To get a similar level of perceived speed by the player, then multiply any
values that did not take ``dt`` into account by 60 before tying them to ``dt``.
