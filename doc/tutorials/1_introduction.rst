.. _tutorial_introduction_to_pygame_turbo:

Tutorial: Introduction to Pygame Turbo
======================================

First, make sure you have Python installed. If you don't, head over to `their
website <https://www.python.org/>`__ and check under the Downloads section.

Second, install Pygame Turbo. Use the following command in a terminal (for
example PowerShell on Windows): ``python -m pip install pgturbo``

Now we're set to begin! Create a new python file and type out the following::

    import pgtrun

    WIDTH = 800
    HEIGHT = 600

    player = Actor.Ellipse(40, 60, "lightblue")
    player.pos = (WIDTH / 2, HEIGHT / 2)

    def draw():
        screen.fill("darkgreen")
        player.draw()

    pgtrun.go()

Run the python file. You'll see a window filled with green and a white oval
sitting in the middle. To stop the game running, simply click the X on the
window or press ``Ctrl+Q`` on the keyboard. This key combination will always
quit PGTurbo games.

Let's go through what the different parts of the code do:

#. ``import pgtrun`` and ``pgtrun.go()`` hook into Pygame Turbo to turn your
   user code into a working game. They always have to be the first and last
   lines of the program so PGTurbo can use everything you created.
#. ``WIDTH`` and ``HEIGHT`` are special variable names that PGTurbo will use to
   set the window size for your game in pixels. So our game has a window 800
   pixels wide and 600 pixels tall.
#. ``player = Actor ...`` creates a game object and saves it to a variable.
   If something in your game should move or react somehow to things happening,
   it should probably be an Actor. Here we make one from a basic shape, an
   ellipse. As arguments we give the width, height and color for the shape.
#. After creating the Actor, we set its position in the game window with
   ``player.pos = (WIDTH / 2, HEIGHT / 2)``. The ``.pos`` property of Actors
   is their current position in the game and we can set it with a tuple of two
   values: ``(x, y)``. In this case, the Actor should sit in the middle of the
   window, so half the width and height is perfect.

   *Note: In games, the X-axis goes from left to right and the Y-axis goes from
   top to bottom. So the top of the window is Y = 0 and the bottom is Y =
   HEIGHT.*
#. The ``draw()`` function is called by PGTurbo every frame to show the state
   of your game. First we fill the window with green to cover up how the game
   window looked last frame and then we draw the player (ellipse) on top of the
   background.

So far, the actor is just sitting around. Let's make it move! Add the following
code between us creating the player actor and ``def draw()``::

    # player.pos = ... is above here

    def update():
        if keyboard.left:
            player.x = player.x - 5
        if keyboard.right:
            player.x = player.x + 5
        if keyboard.up:
            player.y = player.y - 5
        if keyboard.down:
            player.y = player.y + 5

    # def draw(): is below here

Run the program again and you can move the ellipse around with the arrow keys.

#. The ``update()`` function is also called every frame by PGTurbo. In it, you
   should put code that changes the game state, such as moving actors around,
   checking conditions and updating values based on them or creating new actors
   that take part in the game.

   The starting state of the game can't be put in ``update()`` though because
   if you put it there, the game would be reset every frame to the starting
   state.
#. ``if keyboard.left:`` allows you to check if a keyboard key is currently
   pressed down. When there are controls for your game where buttons should be
   held down, such as moving a character around, this is usually the easiest
   way to check for the input.

   You can check any key on the keyboard with ``keyboard.KEYNAME``.
#. ``player.x = player.x + 5`` increases the X axis position of the actor by 5.
   The ellipse 'moves' a bit to the right. Smooth movement in games is achieved
   by changing a value only slightly but very quickly again and again. For
   every frame you hold down an arrow key on the keyboard, the player moves 5
   pixels.

**It's that easy to start developing a game with PGTurbo!**

While moving a blob around the screen is neat, proper games are usually more
complicated than that. To learn more about game dev with PGTurbo and improve
this project, check out the
:ref:`next tutorial on game mechanics <tutorial_game_mechanics>`.

If you'd prefer a more general overview of how PGTurbo works and what
functionality it offers you, skim the :ref:`PGTurbo Overview <overview>`.
