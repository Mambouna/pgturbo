.. _example_snake:

Example game: Snake
===================

:ref:`Back to the overview <examples_overview_snake>`

.. image:: /_static/examples/snake.png
   :alt: Snake
   :height: 500
   :align: center

:download:`Download the project archive here </_downloads/snake.zip>`

This explainer will go into detail on how the code of the *snake* example game
works.

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

In the *snake* project, the section defining game window globals is placed
under the one defining game mechanic constants. This is because the width and
height of the game window are determined by the values of some constants.
Because of this, the constants have to be defined before the game window
variables::

    TILE_PX_SIZE = 24
    HORIZONTAL_TILES = 20
    VERTICAL_TILES = 15

    # ... More constants here ...

    WIDTH = TILE_PX_SIZE * HORIZONTAL_TILES
    HEIGHT = TILE_PX_SIZE * VERTICAL_TILES


Game window global variables
----------------------------

.. code::

    TITLE = "Snake"
    ICON = "snake_head"
    WIDTH = TILE_PX_SIZE * HORIZONTAL_TILES
    HEIGHT = TILE_PX_SIZE * VERTICAL_TILES

As shown above, the ``WIDTH`` and ``HEIGHT`` are set from a few constants. This
is because those constants basically define a grid on which the game takes
place. Each grid cell has a certain size and the width and height of the game
window are then that size multiplied by however many cells there should be in
an axis.


Game mechanics constants
------------------------

.. code::

    TILE_PX_SIZE = 24
    HORIZONTAL_TILES = 20
    VERTICAL_TILES = 15

    INITIAL_UPDATE_INTERVAL = 0.4
    UPDATE_INTERVAL_DIVISOR = 80

``TILE_PX_SIZE`` determines how large in pixels each grid cell should be as a
rectangle, so with the value above each grid cell is 24x24 pixels.
``HORIZONTAL_TILES`` and ``VERTICAL_TILES`` then set how large the playing
field is by giving the number of cells in the grid in each direction.

Thus, the grid will be twenty cells wide and fifteen cells tall with each cell
being 24x24 pixels in size.

The two other constants are for controlling game feel and difficulty. *Snake*
takes place in discreet steps or turns. The snake head doesn't move smoothly
forward but always moves in discreet jumps across the grid. To do this, we
basically make the game a turn-based game where each turn takes a set amount
of time.

``INITIAL_UPDATE_INTERVAL`` controls how long each turn takes at the start of
the game, starting with ``0.4`` seconds for example.
``UPDATE_INTERVAL_DIVISOR`` then controls how much faster the turns get each
time the snake eats an apple. Larger values mean the game gets faster less
drastically. Smaller values will make the diffculty escalate quicker.


Utility grid functions
----------------------

grid_from_pos()
"""""""""""""""

.. code::

    def grid_from_pos(position):
        return (position[0] // TILE_PX_SIZE, position[1] // TILE_PX_SIZE)

Since the game takes place on a grid, we have two small functions that make
working with the grid easier. The first, ``grid_from_pos()`` calculates the
grid cell from a position in the game window.

It does so by dividing the position value with how big each cell is
specifically as an integer division (``//`` operator). Why does this work?
Imagine we are given the X value of 55 and need
to figure out which grid cell this is. The first grid cell spans from X = 0 to
X = 23, the second from X = 24 to X = 47, the third from X = 48 to X = 71.

So it's the third grid cell. How can we get there generally with maths?
If we divide the X value by how large each cell is, we get 2.2916... for X = 55
and 24 as the size. If we treat grid cell indices like list indices, then 2 is
already the correct answer, since those start from 0. However we don't need the
0.2916... part of the number.

Using the integer division operator ``//`` in python means that any fraction
after the point in a non-round number is discarded. So 2.2916... simply becomes
2, the correct index for the third grid cell.

The same thing works for the Y coordinate of the grid cell too.


pos_from_grid()
"""""""""""""""

.. code::

    def pos_from_grid(grid_coords):
        return ((grid_coords[0]) * TILE_PX_SIZE + TILE_PX_SIZE / 2,
                (grid_coords[1]) * TILE_PX_SIZE + TILE_PX_SIZE / 2)

The second function does the opposite. It gives us a position in the game
window that matches the center of any grid coordinate pair we give it.

It does so by simply multiplying the grid coordinate with the size of each
cell and then adding half that size again. Adding half means we end up in the
middle of whatever cell we are looking at, since the topleft of the game window
is also the topleft corner of the first grid cell.

Multiplying the grid cell number with the size of each cell shifts the starting
point over to where we need it. It also comes in handy here that we count grid
cells from 0 like list indices. For the first grid cell, multiplying the size
by 0 means we stay at the topleft corner of the game window and then just shift
over by half the size, landing us directly in the middle of the first cell.

As a convenient bonus, we can align any position in the game window with the
center of the grid cell it is in just by calling both the utility functions
after each other: ``pos_from_grid(grid_from_pos(position))``.

This is because the call to ``grid_from_pos()`` gives the grid coordinate the
original position is in and ``pos_from_grid()`` then returns the position in
the game window at the center of that grid cell.


Snake setup
-----------

Next is setting up the player character: the snake. First, the actor itself
is created and its necessary data initialized. Then, functions relating to the
snake are defined.


Actor setup
"""""""""""

.. code::

    snake = Actor("snake_head")
    snake.pos = pos_from_grid(grid_from_pos((WIDTH / 2, HEIGHT / 2)))
    snake.angle = 90
    snake.data["alive"] = True
    snake.data["next_move"] = "straight"
    snake.data["spawn_segment"] = False
    snake.data["turns"] = []
    snake.data["score"] = 0

The snake actor uses the image of the snake head. It's tail is made up of many
individual actors covered later. It begins in the middle of the playing field
and here is where the trick that was just mentioned is used. With both utility
functions used together we make sure the snake head is placed in the middle of
the grid cell closest to the center of the game window.

Afterwards, the angle is set to ``90`` so the snake begins by facing up in the
game window.

Then the data necessary for the game is initialized in its ``.data``
dictionary. ``"alive"`` tracks if the game is over, ``"next_move"`` saves if
the snake should go straight or turn left or right on the next turn update.
``"spawn_segment"`` tracks if a new segment should be added to the tail next
turn, ``"turns"`` in this case refers to bends in the tail not game turns and
tracks where in the tail there should be a bend and in which direction.
Lastly, ``"score"`` keeps track of how many apples the snake has eaten.


update_snake()
""""""""""""""

.. code::

    def update_snake():
        if snake.data["next_move"] == "turn_left":
            snake.angle += 90
            snake.data["turns"].insert(0, ("left", 0))
        elif snake.data["next_move"] == "turn_right":
            snake.angle -= 90
            snake.data["turns"].insert(0, ("right", 0))
        snake.data["next_move"] = "straight"

        snake.move_forward(TILE_PX_SIZE)

        if not snake.is_onscreen(-1):
            snake.data["alive"] = False

        if snake.distance_to(apple) < TILE_PX_SIZE / 2:
            snake.data["score"] += 1
            apple.pos = pos_from_grid((random.randint(0, HORIZONTAL_TILES - 1),
                                       random.randint(0, VERTICAL_TILES - 1)))
            snake.data["spawn_segment"] = True

This function is called by the general updating function every turn of the
game. It moves the snake, checks if the game is over because of leaving the
game window and eats an apple if it is collided with.


Turning and moving
''''''''''''''''''

First, if a turn to the left or right was called for by user input, the angle
property of the snake is adjusted. Since angles in PGTurbo count
counterclockwise, adding ``90`` to an angle means a quarter circle turn to the
left from the perspective of the previous heading. Reducing the angle by ``90``
instead is the same kind of turn to the right.

In both cases, since a turn was made, a record is inserted at the start of the
``.data["turns"]`` list the snake keeps. This list has an entry for each turn
in the current display of the snake, recording where in the snake the turn
should currently be shown and which direction the turn was made in.

The first value in the tuple is the direction, the second the index of which
segment the turn should currently be displayed at.

After managing turning, the snake is moved forward by one grid cell size. Since
it starts in the center of one grid cell, this means it will move to the center
of the next grid cell in whatever direction it is currently facing.


Check on screen
'''''''''''''''

Next, ``is_onscreen()`` is used to check if the snake head has left the game
window. A margin of ``-1`` means that even if one pixel of the snake image is
still in the game window, it still counts as being outside it.

If the snake has left, the game is over and ``.data["alive"]`` is updated to
reflect this.


Collision with the apple
''''''''''''''''''''''''

Last, a simple distance based collision check is made with the apple. The
``.distance_to()`` method returns how far the ``.pos`` property of one actor
is from the same property of another actor. For this game, that means it tells
us how far the center of the snake head is from the center of the apple.

Since we know that both actors sit in grid cells, their distance when sitting
in adjacent grid cells should be basically the size of the grid cells. As such,
if they are in the same grid cell that distance should be considerably less.

Because of this, we can say that we are sure that a collision happened if their
distance is less than half a grid cell size. This is good enough because the
game happens on a grid and both actors are roughly shaped like a uniform blob
instead of some weird shape.


Eating the apple
''''''''''''''''

If the snake has collided with the apple, it "eats" it. To do that, we add
one to the ``data["score"]`` of the snake and make it reappear somewhere else.

For that, we simply get a random grid cell with two random numbers and then
get the game window position from that grid coordinate. We set the ``.pos`` of
the apple to this so it gets teleported to its new position.

Last, we set ``snake.data["spawn_segment"]`` to ``True`` so that a new segment
will be added to the tail in a turn.


increment_turns()
"""""""""""""""""

.. code::

    def increment_turns():
        k = 0
        while k < len(snake.data["turns"]):
            current_turn = snake.data["turns"][k]
            snake.data["turns"][k] = (current_turn[0], current_turn[1] + 1)

            k = k + 1

        if snake.data["turns"] and snake.data["turns"][-1][1] > len(segments):
            snake.data["turns"].pop(-1)

This function takes care of moving the bends in the snake backwards through the
tail segments until the whole snake has moved through them.

For this, we have to iterate through all the turns the snake shape currently
has. Since we need to change their data in the list however, we use a ``while``
loop, not a ``for`` loop.

For each turn, its index gets increased by one. This is because each turn the
snake moves by exactly one grid cell, no matter in which direction, so each
turn the segments also move through one grid cell the snake head previously
was. For the bends to stay in the same grid cell, they need to be displayed at
one segment further back in the tail each turn, until each segment has gone
through that bend.

This is why if there are bends and the last bend in the list has an index
higher than the number of segments, we know we can remove it from the list.


Tail setup
----------

Now we come to the most complicated part of the project code, the tail of the
snake. We need to solve one basic problem: The tail segments should move
through each grid cell that the snake head previously occupied and they should
do so one after the other so that it appears that the snake is smoothly sliding
along.

First, each segment of the snake tail will be one actor sitting in one grid
cell. Depending on whether the segment is currently in a bend or not we will
switch out the images they use on the fly.


Actor setup
"""""""""""

.. code::

    segments = []
    for i in range(3):
        segment = Actor("snake_straight")
        segment.x = snake.x
        segment.y = snake.y + TILE_PX_SIZE * (i + 1)
        segment.angle = 90
        segments.append(segment)

    segments[-1].image = "snake_tail"

To start out, we make a list to keep all the snake segments in: ``segments``.

Then we create three new segments and put them in the list. Each actor first
gets the image of the straight snake tail and is then put in the same X
position as the snake head (since it moves up at the start of the game).

For the Y position, they get the Y position of the snake head plus one grid
cell size down for which segment they are. The first segment is shifted down
one grid cell, the second two, the second three.

All segments are set so they are facing up, just like the snake head.

After creating all the actors, the last one gets its image set to be the image
of the tip of the tail.


spawn_segment()
"""""""""""""""

.. code::

    def spawn_segment():
        new_segment = Actor("snake_straight")
        if segments[-1].image == "snake_straight":
            new_segment.angle = segments[-1].angle
        elif segments[-1].image == "snake_turn_left":
            new_segment.angle = segments[-1].angle - 90
        else:
            new_segment.angle = segments[-1].angle + 90
        new_segment.pos = segments[-1].pos
        new_segment.move_backward(TILE_PX_SIZE)
        segments.append(new_segment)
        snake.data["spawn_segment"] = False

This function is responsible for adding a new segment to the tail and is called
whenever the snake eats an apple.

First, a new actor is created with the straight image. Then its angle has to be
set properly. If the last segment of the current snake tail is in a bend, then
the new segment also has to follow that bend as otherwise it will move randomly
across the screen.

So if the last snake segment was just moving straight, then the new segment can
just use the same angle as it. If it was in a left turn, then the new segment
should start where its bend came from instead of where it is right now
pointing.

That means it should be one quarter turn clockwise from the angle of the
previous segment, which is done with angle ``-90`` from the previous one. If
there was a right turn, then the new segment should should be where it came
from, meaning a quarter circle counterclockwise, so angle ``+90``.

To get the correct position of the new segment, we can just place it at the
position of the previous last one and then move it backwards by one grid cell,
since we just made sure its angle is correct.

After that, we just add it to the ``segments`` list and set the flag on
``snake.data`` back to ``False`` for the next game turn.


update_segment()
""""""""""""""""

.. code::

    def update_segments():
        turn_index = 0
        if len(snake.data["turns"]) > 0:
            next_turn = snake.data["turns"][turn_index]
        else:
            next_turn = ("nothing", -1)

        for i in range(len(segments)):
            segment = segments[i]
            segment.image = "snake_straight"
            segment.move_forward(TILE_PX_SIZE)

            if i == next_turn[1]:
                if next_turn[0] == "left":
                    segment.angle += 90
                    segment.image = "snake_turn_left"
                else:
                    segment.angle -= 90
                    segment.image = "snake_turn_right"
                
                turn_index += 1
                if turn_index < len(snake.data["turns"]):
                    next_turn = snake.data["turns"][turn_index]

            if segment.distance_to(snake) < TILE_PX_SIZE / 2:
                snake.data["alive"] = False

Now comes the function that properly moves all segments of the snake tail
along the previous path of the snake. How do we do that? One simple answer
would be just to have the snake store the N previous positions and angles it
was in as a list and then go through that list and the list of segments and
set them all individually.

In that case however, we would still need to store where the snake made a turn
somewhere to properly display them however. And if we store that information
anyways, then we can do something more clever to properly position all
segments.

Since each segment has the position from the previous game turn and its
previous heading, we just have to make them turn correctly and otherwise move
them forward once each game turn. How do we know when a segment should make a
turn? Well, from the same place we have to store where turns happened anyway
to correctly display them!


Image reset and movement
''''''''''''''''''''''''

So what happens here?

First, we get the first turn in the list of all made turns. This is the most
recently made turn. If there are no turns, we give the same variable a dummy
value that will never trigger the following code for turning in the segments,
so we won't have any problems.

Then we go through the indices of all segments with a ``for`` loop. We need the
index to check whether this segment should display a turn.

We get the current segment we are looking at and set its picture to straight.
This is done so segments showing a turn the previous game turn go back to
displaying straight. We then also move the actor forward one grid cell in its
facing direction. This is correct because the direction an actor looks at is
always the one it should move next turn, not the same one.


Managing turns
''''''''''''''

Only after moving, we set the direction to face for the next turn and also
whether the segment should display a turn. To do so, we check
``if i == next_turn[1]:``. The second value in the ``next_turn`` tuple is what
index of segment the turn should be displayed at.

If it's the current one, depending on the direction of the turn the angle of
the segment is updated and its image changed to fit the turn.

After that, we can go to the next turn in the snake since we know we properly
displayed the current one. To do so, we incremend ``turn_index`` and if there
is still another turn in the list, we set that as the next one to be processed.


Collisions with the snake head
''''''''''''''''''''''''''''''

Just like with the snake head and the apple, a very simple collision check is
enough to tell whether the snake head has hit the segment we are currently
looking at. It's the same kind of distance check to see if both actors are on
the same grid cell.

If so, ``snake.data["alive"] = False`` indicates to the rest of the game code
that the game is over.


Apple setup
-----------

.. code::

    apple = Actor("apple", (-100, -100))
    apple.pos = pos_from_grid((random.randint(0, HORIZONTAL_TILES - 1),
                               random.randint(0, VERTICAL_TILES - 1)))

The apple is a simple actor. We create it somewhere off screen and then
immediately put it in a random grid cell at the start of the game.

Eating the apple happens in ``update_snake()``, so the code to reposition it is
also there. The apple is entirely passive and just gets moved around whenever
necessary.


Event hooks
-----------

.. code::

    def on_key_down(key):
        if key == keys.LEFT:
            snake.data["next_move"] = "turn_left"
        elif key == keys.RIGHT:
            snake.data["next_move"] = "turn_right"

The only event hook necessary is for keyboard inputs. Whenever the left or
right arrow keys are pressed, we note that the snake should turn in that
direction on the next game turn. This means if the user presses different
directions inside a single game turn time, only the last one will actually be
followed.

Using those values happens in ``update_snake()`` as we saw before.


Custom update function
----------------------

.. code::

    def update_interval():
        if not snake.data["alive"]:
            return

        update_snake()

        update_segments()

        increment_turns()

        if snake.data["spawn_segment"]:
            spawn_segment()

        segments[-1].image = "snake_tail"

        new_interval = (INITIAL_UPDATE_INTERVAL
                        / (1 + snake.data["score"] / UPDATE_INTERVAL_DIVISOR))

        clock.schedule(update_interval, new_interval)
        
    # We have to start the custom update cycle manually here.
    clock.schedule(update_interval, INITIAL_UPDATE_INTERVAL)

This is the custom update function for the game, called not every frame
automatically by PGTurbo but instead by us in set intervals with
``clock.schedule()``.

If the game is over, nothing gets changed, effectively freezing the game state.

Otherwise, we update the different game objects in turn, first the snake head,
then its tail, then we update the turn counting mechanism for the whole snake
and if an apple was eaten (determined during ``update_snake()``), then we give
the snake tail a new segment.

Lastly for the snake, the last tail segment always gets its image set to the
snake tail. The reason this has to happen separately is because if we did it
earlier, then if a new segment was added, the last segment of the snake would
suddenly not look like the tip of the tail anymore.


Update intervals
""""""""""""""""

The interval of when to do the next game turn starts at
``INITIAL_UPDATE_INTERVAL`` but gradually gets shorter as the score of the
player increases.

We divide the initial interval by 1 plus some factor having to do with the
score. We want this factor to increase with a higher score so dividing the
initial value by 1 plus the factor will gradually decrease the resulting
update interval.

Just directly adding the score would be too extreme though. If we did that,
the game would suddenly run twice as fast as soon as the player ate a single
apple. Instead we just divide the score by a much larger number to make it so
any increase by another point in the score only shortens the update interval
by a little bit.

Finding a good value for this divisor can be done just by experimenting a few
times. To find the one in the example code, I just started at 100, thought it
was a bit too much and went down by 10 twice, arriving at 80 where it felt
right.

Finding good values for your game mechanics constants is often just playing the
game yourself to see what feels good.

Then the function schedules its next call with that calculated interval. To
actually start the cycle, we directly schedule it under the function definition
just with the initial update interval from the constant.


Game loop
---------

.. code::

    def draw():
        screen.clear()

        for segment in segments:
            segment.draw()

        apple.draw()

        snake.draw()

        score_text = "Score: {}".format(snake.data["score"])

        if snake.data["alive"]:
            screen.draw.text(score_text, topright=(WIDTH - 5, 5))

        else:
            screen.draw.text("YOU DIED", center=(WIDTH / 2, HEIGHT / 2),
                             fontsize=42)
            screen.draw.text(score_text, center=(WIDTH / 2, HEIGHT / 2 + 40))

Almost there, just the ``draw()`` function remains. By using ``screen.clear()``
we give the game a black background. Then we draw the segments in the tail,
then the apple and only then the snake head.

Why did we do it in this order? When drawing multiple things in the same spot,
anything drawn later is drawn "above" the previous elements. We want the snake
head to be drawn above the apple, so it has to be drawn second. We also want
the apple to display above the tail however, since it might appear on the tail
after being eaten and would otherwise be invisible until the whole tail moved
away. Because of this, we draw the whole tail at first.

Then we put together a string of what score the player has by using the
``.format()`` method. With this, any ``{}`` in a string is replaced by the
values in the parentheses of ``.format()`` in order.

If the game is still ongoing, we draw the score in the top right corner,
otherwise we do so centered under a big ``"YOU DIED"`` message.

:ref:`Back to the overview <examples_overview_snake>`
