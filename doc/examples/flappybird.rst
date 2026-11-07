.. _example_flappybird:

Example game: Flappybird
========================

:ref:`Back to the overview <examples_overview_flappybird>`

.. image:: /_static/examples/flappybird.png
   :alt: Flappybird
   :height: 500
   :align: center

:download:`Download the project archive here </_downloads/flappybird.zip>`

This explainer will go into detail on how the code of the *flappybird* example
game works.

*If you want to learn from it, it's recommended you first have a look through
the source code yourself. Try to understand the overall structuring of the
project and then see if you can understand what the different parts of the code
do. You can also make changes and run the project a couple of times to see how
they affect the game.*

Once you've done so, feel free to read through this explainer to clear up any
confusion or misunderstandings.


Structure
---------

This general structuring is shared by all the example projects:

#. Imports (usually for PGTurbo and getting random values)
#. Definitions of game window global variables and game mechanics constants
#. Different sections setting up all the actors and their functions for the
   project
#. Event hook function definitions
#. Game loop function definitions (for update and drawing)

In *Flappybird*, we track the highscore from previous times playing the game,
which is why there is one section for persistent data saving setup together
with other actor setup stuff.


Game window global variables
----------------------------

.. code::

    TITLE = 'Flappy Bird'
    WIDTH = 400
    HEIGHT = 708

For this game, the game window globals are simple. We set the window title to
the name of the game and set ``width`` and ``height`` so we get a narrow and
tall window just like smartphone screens are usually shaped.


Game mechanics constants
------------------------

.. code::

    GAP = 130
    GRAVITY = 0.3
    FLAP_STRENGTH = 6.5
    SPEED = 3

The ``GAP`` global controls how far apart the pipes are that the bird has to
fly through. A lower value will make the game harder and at some point even
impossible.

The ``GRAVITY`` constant sets up how quickly the bird falls down by itself if
the player doesn't flap its wings. Finding good values for things like gravity
is often a process of trial an error. Write some game code, set a first value
just to see what happens and play. Then adjust the constant value while trying
the game for yourself over and over again until you find something that feels
right.

It's similar for ``FLAP_STRENGTH`` and ``SPEED``. The first controls how far
a flap pushes the bird upward and how quickly it starts to fall again while
the second is how quickly the pipes move towards the bird. Both of these were
also found just by trying them out.


Persistent data setup
---------------------

.. code::

    storage.autosave = True
    storage.load()
    storage.setdefault('highscore', 0)

For our version of *Flappybird*, we want to track what the reached highscore
was not just for a single game session but also if the game gets closed and
opened again later.

That means we need to store *persistent data*, meaning data that will stay on
the computer somewhere in a file and can be used to check what the previously
set highscore was when the game is opened again later.

In PGTurbo, we can store such data with the ``storage`` builtin. It works
like a dictionary, meaning every data entry has a name (key) and a value.
Different from a normal dictionary is that you can ``.save()`` and ``.load()``
its contents and that's exactly how data can stay present between game
sessions.

For our game, we want the highscore to be saved to the filesystem whenever it
is changed and for that, ``storage`` has a handy ``.autosave`` property. If
this is ``True``, then whenever a value is set in ``storage``, the whole
dictionary is immediately saved.

After enabling this setting, we ``storage.load()`` to make sure we have the
previous highscore loaded if it exists. But what if this is the first time
running the game? Usually, if you try to read a dictionary value by its name
when that name doesn't exist yet, an error would happen and the same is true
for ``storage``.

To help with this, the ``.setdefault()`` method takes a name and a value and
inserts it into ``storage`` only if that name doesn't exist yet. This means if
it's the first time running the game, highscore tracking will start at 0. If
there is already a value for the name ``"highscore"`` however, it won't be
changed.

This pattern is very common and useful. Make the necessary settings, load data
and then ensure every name you will use has a default value as a fallback with
``.setdefault()``.


Bird setup
----------


Actor setup
"""""""""""

.. code::

    bird = Actor('bird', (75, 200))
    bird.top_limit = 0
    bird.data["dead"] = False
    bird.data["score"] = 0

The bird actor is created from the appropriate image and positioned to the
left of the game window and in the upper half.

The ``.top_limit`` is set to prevent the bird from flying up outside the game
window. With a value of ``0``, whenever the top edge of the bird would go under
this value, it will instead be positioned so it matches the limit.

Other than that, we just need the bird to track two values for its game
mechanics, which we can do with the ``.data`` dictionary all actors have.

``data["dead"]`` tracks whether the game has to be reset because the bird hit
a pipe or full out of the bottom of the game window. ``data["score"]`` tracks
how many pipes the bird has passed.

These are values that should reset with each game session and even whenever the
game is reset inside a single game session. Because of this, they are not
suitable to save with ``storage`` as that would always preserve their values
for other game sessions as well.


flap_bird()
"""""""""""

.. code::

    def flap_bird():
        if not bird.data["dead"]:
            bird.vy = -1 * FLAP_STRENGTH

A very short an simple function, this just checks if the bird is still alive
and if yes, changes its velocity to simulate a wing flap.

The reason just setting the velocity to something negative looks convincing is
because the bird is moved every frame according to its velocity and negative
Y values point up in PGTurbo. So with a ``FLAP_STRENGTH`` of for example 4,
when the bird flaps its wings its velocity will move it up the next frame.

Afterwards, the gravity mechanic will start drawing this upwards velocity down
again which makes the bird smoothly move up for a short time, then plateau
when the velocity is around zero before starting to fall again and falling
faster and faster with time.


update_bird()
"""""""""""""

.. code::

    def update_bird():
        bird.vy += GRAVITY
        bird.move_by_vel()

        if not bird.data["dead"]:
            if bird.vy < -3:
                bird.angle = 30
                bird.image = 'bird_up'
            else:
                bird.angle = 0
                bird.image = 'bird'

        if bird.collidemask(pipe_top) or bird.collidemask(pipe_bottom):
            bird.data["dead"] = True
            bird.image = 'bird_dead'

        if bird.top > HEIGHT:
            bird.y = 200
            bird.data["dead"] = False
            bird.data["score"] = 0
            bird.vy = 0
            reset_pipes()

This function is called every frame by the game loop ``update()`` and manages
the bird's ongoing state changes. First, its velocity is increased by the value
of the ``GRAVITY`` constant, meaning it "falls" toward the bottom of the screen
faster and faster with time if moved by its velocity. Doing just that is then
done with ``bird.move_by_vel()``.

After that, as long as the bird is alive, its look is changed depending on its
velocity. Why use the velocity? Because it's a single value that indicates
whether the bird is moving up or down right now.

If the velocity is under ``-3``, i.e. it is moving up with some speed, then
its ``angle`` is set to ``30`` to make it face upwards and the ``image`` is
changed to a version with the wing stubs flapped down.

Otherwise, the ``angle`` is made ``0`` and the standard ``image`` set.

It's a small thing, but this visual feedback of player action alone helps make
the game pop a bit more.

Next is checking whether the bird hit any pipes. For this, the bird simply
does a collision checks again both pipe actors and if one of them returns
``True``, ``bird.data["dead"]`` is made true and the image changed to show
the hit state. This also disables controlling the bird via wing flaps.

Last we need the game to reset whenever the bird "falls" out of the game window
at the bottom. For that, we just check if the top edge of the bird actor image
has left the screen vertically (``HEIGHT`` is the maximum Y value visible on
screen).

If yes, the bird's Y position is reset, its ``"dead"`` and ``"score"`` values
are set back to their defaults, its velocity to ``0`` and the pipes are put in
a new starting position with ``reset_pipes()``. That's all that's needed to
reset the game.


Pipes setup
-----------


Actor setup
"""""""""""

.. code::

    pipe_top = Actor('top', anchor=('left', 'bottom'))
    pipe_bottom = Actor('bottom', anchor=('left', 'top'))

There are two pipes and so we use two actors for them. The reason we change
their anchors is to make positioning them easier. Their anchors now sit so that
the edge of their pipe lines up with their Y position and their X position
being left means placing them just outside the game window to the right is also
simple.


reset_pipes()
"""""""""""""

.. code::

    def reset_pipes():
        pipe_gap_y = random.randint(200, HEIGHT - 200)
        pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
        pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)

    reset_pipes()  # Set initial pipe positions.

This function places the pipes just off the screen to the right and randomizes
their vertical placement. For that, first a random Y position is gotten. The
reason it can't be across the entire Y axis is that if the center of the gap
was too close to the top or bottom edge of the screen, then maybe the bird
couldn't fit through it at all.

``pipe_gap_y`` then is the center of the gap. The pipes are placed half the
height of the gap apart, one below and one above the randomized center. The
reason the ``GAP`` constant is halved here is so the total gap (above and below
the center) equates to the full gap constant value. This way, adjusting the gap
size is more intuitive while figuring out the right values for the game
mechanics.

The X position for both pipes being ``WIDTH`` just means they are placed just
outside the game window, since their anchors are on their left side on the X
axis.

The function is immediately called after being defined to setup the pipes for
the first time when the game is opened.


update_pipes()
""""""""""""""

.. code::

    def update_pipes():
        pipe_top.left -= SPEED
        pipe_bottom.left -= SPEED
        if pipe_top.right < 0:
            reset_pipes()
            if not bird.data["dead"]:
                bird.data["score"] += 1
                if bird.data["score"] > storage['highscore']:
                    storage['highscore'] = bird.data["score"]

This function takes care of everything the pipes need to do every frame and is
called by the game loop ``update()`` function.

First, both pipes are moved to the left by whatever ``SPEED`` is set to. As
such, that constant is an important control for how difficult the game is as
higher speed leaves less time for the bird to find the gap in between the
pipes.

Then there's a simple check. If the pipes have left the screen to the left,
then the bird either successfully passed a gap or it died hitting the pipes.

In both cases, the pipes can be reset to create a new gap position and put them
to the right side again.

To separate a successful gap clear from hitting the pipes, we then check if the
bird is not ``"dead"``. If it is not, it gets its score increased.

Also, if the gotten score is now higher than the previous highscore, we set
``storage["highscore"]`` to the new value.

Remember that we set ``storage.autosave = True`` before? That means setting the
value automatically also saves it to the file system to be preserved for future
game sessions.


Event hooks
-----------

.. code::

    def on_key_down():
        flap_bird()

Very simply, whenever a keyboard key is pressed in this game, the bird flaps
its wings to gain some altitude. We do this by calling the function covered
above: ``flap_bird()``.


Game loop
---------


update()
""""""""

.. code::

    def update():
        update_pipes()
        update_bird()

The ``update()`` function in this game is very simple, because we separated
the code managing the bird and the pipes into their own functions. As such, all
that happens here is to call each of those functions.

You might ask why we don't just write everything in this function. In a simple
game like this that might work without too many problems, but it can still be
good practise to structure your code so it's easy to find everything.

One simple way to do such structuring is to just put every bit of code for a
certain game system together. So in this case everything that the bird is and
does is put in one place, first the code creating it, then any functions
manipulating it.

The same is true for the pipes as well and if the game was larger, we could do
it this way for any other actors and systems too. That way, if we want to
change something about the bird but we aren't sure where in the code that
should go, we still have just one place to look instead of possibly going back
and forth between places.


draw()
""""""

.. code::

    def draw():
        screen.blit('background', (0, 0))

        pipe_top.draw()
        pipe_bottom.draw()
        bird.draw()

        screen.draw.text(
            str(bird.data["score"]),
            color='white',
            midtop=(WIDTH // 2, 10),
            fontsize=70,
            shadow=(1, 1)
        )

        screen.draw.text(
            "Best: {}".format(storage['highscore']),
            color=(200, 170, 0),
            midbottom=(WIDTH // 2, HEIGHT - 10),
            fontsize=30,
            shadow=(1, 1)
        )

Since we have a background image for the game, we blit it every frame to the
topleft. If you haven't seen the ``screen.blit()`` function before, it takes an
image name and a position tuple as its arguments and draws the image onto the
screen so the topleft corner of the image is at the given position.

For games with a static background, this means you can create a background
image the size of the game window and simply blit it every frame to the top
left corner to show the background.

Because this overwrites anything from the last frame as well, we don't need
another ``screen.clear()`` or ``screen.fill()`` as we usually would to make
sure nothing from the last frame shows up in this one.

After showing the background, we just draw the three actors in the game, the
pipes and the bird.

Last, we want to show the current score and the highscore previously achieved.
For this we draw text twice. For the first one we just convert the score number
into a string since ``screen.draw.text()`` needs a string as the first
argument. For the second, we have a text that we insert the score number into
at the right position with ``.format()``.

The ``.format()`` function can be called on strings and replaces any ``{}`` in
the text with the values in the function parentheses in order. In this case it
means the ``{}`` in ``Best: {}`` is replaced by the highscore number.

Other than this, one option argument for the text drawing calls might be
unfamiliar. ``shadow`` draw the text with a text shadow underneath. The tuple
value contains two numbers that set the placement of the text shadow in the
X and Y axis. These numbers are relative and set up so that ``1.0`` should
usually be a good starting point.

:ref:`Back to the overview <examples_overview_flappybird>`
