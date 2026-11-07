.. _tutorial_from_scratch:

Tutorial: Migrating from Scratch
================================

This tutorial will compare an implementation of Flappybird written in Scratch
with one written in Pygame Turbo. The Scratch and Pygame Turbo programs are
similar to a remarkable extent.

You can download a ``.zip`` file with the game project
:download:`here </_downloads/flappybird.zip>`. It contained folder holds both
the Python file for the PGTurbo version and its assets as well as Scratch 1.4
and Scratch 3 versions of the game.

The Pygame Turbo version includes scoring logic, which is omitted in the code
examples on this page to make it a closer comparison.

The Python code shown below is re-arranged for clarity within the examples.


The stage
---------

Here's how the stage is laid out in our Scratch program:

.. image:: /_static/scratch/flappybird_stage.png

There are just three objects, aside from the background: the bird, and the top
and bottom pipes.

This corresponds to the Pygame Turbo code setting these objects up as
``Actors``::

    bird = Actor('bird', (75, 200))
    pipe_top = Actor('top', anchor=('left', 'bottom'))
    pipe_bottom = Actor('bottom', anchor=('left', 'top'))

In Pygame Turbo we also have to ensure we draw these objects. In principle this
gives a little more flexibility about how to draw the scene::

    def draw():
        screen.blit('background', (0, 0))

        pipe_top.draw()
        pipe_bottom.draw()
        bird.draw()


Pipe movement
-------------

The pipes move at a constant rate irrespective of the bird. When they move off
the left-hand side of the screen, they loop around to the right, and their
vertical position moves at random.

In Scratch this can be achieved by creating two different scripts for the top
and bottom pipe.

.. image:: /_static/scratch/flappybird_top_start.png
    :width: 55%

.. image:: /_static/scratch/flappybird_bottom_start.png
    :width: 44%

To summarise what's happening here:

* The condition ``x position < -240`` is true when a pipe is off the left-hand
  side of the screen, and this is the trigger to reset the pipes.
* The ``pipe_height`` variable is used to coordinate the two pipes. Because the
  gap between them should remain the same, we can't pick *both* heights
  randomly. Therefore one of the scripts has this logic and the other doesn't.
* The ``set y position to pipe height +/- 230`` sets one pipe to be above
  ``pipe_height`` and the other pipe below ``pipe_height``.

This code becomes much simpler in Pygame Turbo. We could write a single function
that updates both pipes. In fact we split it a different way to make it clear
that the reset actions go together::

    import random

    WIDTH = 400
    HEIGHT = 708
    GAP = 130
    SPEED = 3

    def reset_pipes():
        pipe_gap_y = random.randint(200, HEIGHT - 200)
        pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
        pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)

    def update_pipes():
        pipe_top.left -= SPEED
        pipe_bottom.left -= SPEED
        if pipe_top.right < 0:
            reset_pipes()

A small difference here is that we can extract values that we want to re-use as
"constants", spelled in UPPERCASE. This lets us change them in one place when
we want to tune the game. For example, in the code above, we could widen or
narrow the gap between the two pipes simply by changing ``GAP``.

The biggest thing that differs is that there is no ``forever`` loop in Python
code.  This is the big difference between Scratch and most text-based
programming languages: you must update the game by one animation step and then
return.  Returning gives Pygame Turbo a chance to do things like processing
input or redrawing the screen. Loop forever and the game would just sit there,
so any loops need to finish quickly.

Pygame Turbo calls an ``update()`` function when it wants you to update the
animation by one step, so we just need to add a call to ``update_pipes()``::

    def update():
        update_pipes()


The Bird
--------

The patterns described above for how Scratch logic translates to Python code
also apply for the bird logic. Let's look at the Python code first this time.

The code to update the bird is organised into a function called
``update_bird()``. The first thing this function contains is some code to move
the bird according to gravity::

    GRAVITY = 0.3

    # Bird starts alive
    bird.data["dead"] = False

    def update_bird():
        bird.vy += GRAVITY
        bird.move_by_vel()

``bird.data["dead"]`` gives the ``bird`` actor a value with the name ``"dead"``
to track. We could store many more other values in ``bird.data``, but for this
game, we only need to know if the bird is still alive.

Below that, in ``update_bird()``, we use a simple gravity formula:

* Gravity means constant **acceleration downwards**.
* Acceleration is change in **velocity**.
* Velocity is change in **position**.

Actors in PGTurbo (which the bird is) have the ``.vx`` and ``.vy`` properties
that represent their linear velocity in either axis. So by adding ``GRAVITY``
to it each frame, we make it so moving with its velocity will move the bird
further than last frame. Essentially, we've made the bird accelerate.
``bird.move_by_vel()`` simply changes the position of the bird by its velocity.

* Gravity means constant acceleration downwards: ``GRAVITY`` is greater than 0.
* Acceleration is change in velocity: ``GRAVITY`` gets added to ``bird.vy``
* Velocity is change in position: ``bird.move_by_vel()`` changes the position
  of the actor by its velocity.

Note that the bird does not move horizontally! We created the actor at X = 75,
so as long as ``bird.vx`` is zero and we don't change its ``.x`` property
otherwise, it will always stay on the left side of the game window.

We simulate the forward movement by moving the pipes towards the bird. This
looks as though it's a moving camera following the bird. This trick is used a
lot in games. Instead of moving the player character and a camera around the
world, just make the world move around the main character. It ends up looking
the same to the player and is much easier to do.

The next section makes the bird flap its wings::

    if not bird.data["dead"]:
        if bird.vy < -3:
            bird.angle = 30
            bird.image = 'bird_up'
        else:
            bird.angle = 0
            bird.image = 'bird'

First, all of this only happens if the bird is still alive. For that, we check
the value we gave it to keep before.

Then we check if the bird is moving upwards or downwards. We show the
``'bird_up'`` image if it is moving upwards fast and the normal ``'bird'``
image otherwise. (``-3`` was picked by trial and error to make this look
convincing).

When moving up, we also angle the bird upwards slightly with the ``.angle``
property to make it look even better. Otherwise the bird just looks straight
ahead.

The next section checks if the bird has collided with a wall::

    if bird.collidemask(pipe_top) or bird.collidemask(pipe_bottom):
        bird.data["dead"] = True
        bird.image = 'bird_dead'

If so we set ``bird.data["dead"]`` to ``True``. This is a **boolean value**
meaning it is either ``True`` or ``False``. We can use this to easily check if
the bird is alive. If it isn't alive it won't respond to player input. We also
switch the player image again to show that the bird is dead.

And the final section checks if the bird has fallen off the bottom of the game
screen. If so it resets the bird::

    if bird.top > HEIGHT:
        bird.y = 200
        bird.data["dead"] = False
        bird.vy = 0
        reset_pipes()

What's ``reset_pipes()`` doing there? Because we organised the pipes code to
be a separate function, we can just call it whenever we want to reset the
walls. In this case it makes it a better game because it gives the player a
chance to react when the bird moves back to its start position.

Again, the code to manage the bird needs to be called every frame, so we add it
to ``update()``::

    def update():
        update_pipes()
        update_bird()

The final part of the bird logic is that it has to respond to player control.
When we press a key, the bird flaps upwards. Pygame Turbo will call an
``on_key_down()`` function - if you've defined one - whenever a key is
pressed::

    FLAP_STRENGTH = 6.5

    def flap_bird():
        if not bird.data["dead"]:
            bird.vy = -1 * FLAP_STRENGTH

    def on_key_down():
        flap_bird()

We wrote a very small ``flap_bird()`` function just to keep all the code for
the bird actor in one place. When a key is pressed, ``on_key_down()`` is called
automatically by Pygame Turbo. It then calls ``flap_bird()``. In that function,
if the bird is alive, we set its ``.vy`` to the negative ``FLAP_STRENGTH``.

In Pygame Turbo, the Y axis points down, not up. This means a negative vertical
velocity will move an actor upwards when ``.move_by_vel()`` is used.

You should be able to find a lot of parallels between the Python code and this
Scratch code:

.. image:: /_static/scratch/flappybird_bird_start.png
    :width: 60%

.. image:: /_static/scratch/flappybird_bird_space.png
    :width: 39%


The biggest differences between Scratch and Pygame Turbo are these:

* You cannot loop forever in Pygame Turbo - just update for one frame and then
  return.
* The coordinates are different. In Pygame Turbo, the top left of the screen is
  ``x = 0, y = 0``. The ``x`` direction goes from left to right as before, but
  ``y`` goes down the screen! This is why ``GRAVITY`` is a positive number and
  ``FLAP_VELOCITY`` is a negative number in Python.
* ``bird.data["dead"]`` is a bool, so we can write code like
  ``if not bird.data["dead"]:`` instead of ``dead = 0`` as in Scratch.


Summary
-------

Many of the concepts available in Scratch can be translated directly into
Pygame Turbo.

Here are some comparisons:

.. list-table::
    :header-rows: 1

    * - In Scratch
      - In Pygame Turbo
    * - .. image:: /_static/scratch/block_change_y.png
      - ``bird.y -= 1``
    * - .. image:: /_static/scratch/block_change_y_negative.png
      - ``bird.y += 1``
    * - .. image:: /_static/scratch/block_switch_costume.png
      - ``bird.image = "name"``
    * - .. image:: /_static/scratch/block_if_dead.png
      - ``if not bird.data["dead"]:``
    * - .. image:: /_static/scratch/block_set_dead.png
      - ``bird.data["dead"] = False``
    * - .. image:: /_static/scratch/block_if_touching_top.png
      - ``if bird.collidemask(pipe_top):``
    * - .. image:: /_static/scratch/block_when_flag_clicked.png
      - Put code into the ``update()`` function.
    * - .. image:: /_static/scratch/block_when_key_pressed.png
      - ``def on_key_down():``
    * - .. image:: /_static/scratch/block_pick_random.png
      - Put ``import random`` at the top of the file to load functions around randomness, then use ``random.randint(a, b)``.
    * - ``(0, 0)`` is the center of the stage.
      - ``(0, 0)`` is the top left corner of the game window.

In some cases, the code is simpler in Python because it can be
organised in a way that helps it make sense when you read it.

The power of Pygame Turbo's actors also makes the coordinate manipulation
easier. We used the ``.anchor`` property to position the pipes, and we were
able to see if a pipe was off-screen by checking ``pipe_top.right < 0``
rather than ``if x position < -240``.

You can find a more thorough comparison of Scratch blocks to Pygame Turbo
instructions in the
:ref:`Scratch / PGTurbo comparison reference page <reference_scratch_pgturbo_comparison>`.
