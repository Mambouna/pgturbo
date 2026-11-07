.. _example_pong:

Example game: Pong
==================

:ref:`Back to the overview <examples_overview>`

.. image:: /_static/examples/pong.png
   :alt: Pong
   :height: 500
   :align: center

:download:`Download the project archive here </_downloads/pong.zip>`

This explainer will go into detail on how the code of the *pong* example game
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


Game window global variables
----------------------------

.. code::

    TITLE = "Pong"
    WIDTH = 800
    HEIGHT = 600

There is nothing special here, we set the game window dimensions to something
a bit wider than tall to give a good looking play space.


Game mechanics constants
------------------------

.. code::

    MAIN_COLOR = "yellow"
    WIN_POINTS = 11

    PADDLE_WIDTH = 15
    PADDLE_HEIGHT = 100
    BALL_DIAMETER = 20

    PLAYER_SPEED = 5
    COMPUTER_SPEED = 4
    BALL_SPEED = 8

Next, we define the different constants we will use throughout the game. This
is also similar to the other example projects. To make it quick, we define
variables (making their names UPPERCASE to show they are meant to be constants)
with set values that affect all the different gameplay aspects of the game
project.

If we later want to tweak how the game plays, we can do so simply by changing
the values at the top of the game file. This way, we have don't have to go
through the code and change all individual occurrences of different values.

For this game, we set the main color to use for the game elements and how many
points are necessary to win the match for the general constants.

For the two paddles, we set their width and height and the diameter for the
ball.

Most important for tweaking difficulty later, we create constants for how
fast the player paddle, computer opponent paddle and the ball will move.


Computer paddle setup
---------------------

The next section creates the actor for the computer opponent paddle and the
necessary functions to have it act by itself.

Actor for the computer paddle
"""""""""""""""""""""""""""""

.. code::

    computer = Actor.Rectangle(PADDLE_WIDTH, PADDLE_HEIGHT, MAIN_COLOR)
    computer.pos = (30, HEIGHT / 2)
    computer.y_limits = (20, HEIGHT - 20)
    computer.data["score"] = 0
    computer.data["bounced"] = False

The actor is a simple shape actor from a rectangle and takes all its properties
from the constants we defined above.

It's then placed on the left side of the game window and centered vertically.
``y_limits`` define that the actor can move below the Y axis value ``20`` and
above ``HEIGHT - 20``. This means it can't simply move off-screen trying to
followe where the ball goes.

Afterwards, we just create two values to track in its ``.data`` dictionary:
``"score"`` tracks how many points the computer has and ``"bounced"`` is used
to ensure that the ball cannot bounce "inside" the computer paddle multiple
times. More on that later.


computer_reset_start_params()
"""""""""""""""""""""""""""""

.. code::

    def computer_reset_start_params():
        computer.data["start_direction"] = random.choice((-1, 1))
        computer.data["start_duration"] = random.randint(5, 20) / 10

    computer_reset_start_params()

This function sets two more values on the ``.data`` dictionary of the computer.

Both of these are randomized and used to control how the computer moves and
for how long before shooting the ball at the start of the match or after it
scored a point.

The function is called right under the definition to give the computer an
initial value for both variables. This is because the computer is first to
start the match with the ball.


update_computer()
"""""""""""""""""

.. code::

    def update_computer():
        if state["phase"] == "start" and state["start_paddle"] == computer:
            computer.y += COMPUTER_SPEED * computer.data["start_direction"]
            if computer.top <= 20 or computer.bottom >= HEIGHT - 20:
                computer.data["start_direction"] *= -1
        elif state["phase"] == "game":
            if (ball.angle + 90) % 360 <= 180:
                computer.move_towards_point((computer.x, HEIGHT / 2),
                                            COMPUTER_SPEED)
            else:
                computer.move_towards_point((computer.x, ball.y), COMPUTER_SPEED)

This function is called by the game loop ``update()`` function and takes care
of the behavior of the computer paddle.

It has two different parts, one for how the computer acts when it is its turn
to start a rally and one for when the ball is in play.

In the first case, the computer simply moves in its previously randomly chosen
direction at its speed and turns around whenever it hits the edge of the play
field.

In the second, it's behavior is depended on how the ball is moving.

If the ball is moving away from the computer paddle, it simply moves to the
center of its side of the field. The condition for this is worth exploring more
than the movement code itself::

    if (ball.angle + 90) % 360 <= 180:

First, what is the goal? The goal is that the condition will be ``True`` if the
ball is moving towards the right at any angle and ``False`` if not.

To make this happen, we can start by thinking about what angle values apply to
this. Moving to the right is covered by an arc of 180 degrees spanning the
right side of the angle circle. Thinking simply, it means any angle from -90
to +90 fits. That is difficult to express as a condition however, since the
angle -90 is actually 270. So 270 to 359 and then 0 to 90 is a bit clunky as
a condition.

Instead, we can "rotate" all of the angles involved. By adding 90 to the actual
angle, now a previous angle of 90 will be 180 and a previous angle of 270 will
be 360. Anything larger than 270 as an initial angle will go above 360 however,
so to not have values overshoot, we modulo with 360. 

With this, we've effectively rotated the values of angles one quarter around
the angle circle counterclockwise. And that means, the valid values to move
towards the right are not just 0 to 180.

If the ball is moving towards the computer paddle instead, the it simply tries
to match the balls vertical position at any time.


Player paddle setup
-------------------

Actor creation
""""""""""""""

.. code::

    player = Actor.Rectangle(PADDLE_WIDTH, PADDLE_HEIGHT, MAIN_COLOR)
    player.pos = (WIDTH - 30, HEIGHT / 2)
    player.y_limits = (20, HEIGHT - 20)
    player.data["score"] = 0
    player.data["bounced"] = False

The player actor is basically the same as the computer one, just that it gets
placed on the right side of the screen.


update_player()
"""""""""""""""

.. code::

    def update_player():
        if state["phase"] != "end":
            if keyboard.up:
                player.y -= PLAYER_SPEED
            if keyboard.down:
                player.y += PLAYER_SPEED

The code for continous inputs for the player is also easy. As long as the
game hasn't ended, we move the paddle up or down if the keyboard arrows are
pressed for those directions.

We don't have to worry about moving off the game window because the paddle will
stop moving by its movement limits without us having to manually stop it.

That's already it. There's a bit more later in the event hook for keyboard
input but that's just to shoot the ball if the player is the one to start a
rally.


Ball setup
----------

.. code::

    ball = Actor.Ellipse(BALL_DIAMETER, BALL_DIAMETER, MAIN_COLOR)
    ball.pos = (computer.right + BALL_DIAMETER / 2, computer.y)

The ball is the most complex part of the whole project. It's actors is very
simple however: a simple shape actor of a circle, initially placed on the right
side of the computer paddle and vertically centered with it.


ball_scored()
"""""""""""""

.. code::

    def ball_scored(paddle):
        paddle.data["score"] += 1
        if ball.x > WIDTH:
            state["start_paddle"] = computer
            ball.x = computer.right + BALL_DIAMETER / 2
            computer_reset_start_params()
            clock.schedule(shoot_ball, computer.data["start_duration"])
        else:
            state["start_paddle"] = player
            ball.x = player.left - BALL_DIAMETER / 2
        ball.y = state["start_paddle"].y

        if paddle.data["score"] < WIN_POINTS:
            state["phase"] = "start"
        else:
            state["phase"] = "end"
            clock.unschedule_all(shoot_ball)

This function gets called when the ball leaves the game window and gets the
paddle that scored a point as an argument. First, the score of that paddle
is incremented. Then, based on whether the ball exited the screen left or right
the correct next paddle is made to be the next one to start a rally and the
ball set to its position on the paddle.

If that is the computer, ``computer_reset_start_params()`` is called to give
it a random direction to start moving in as well as a random time to wait
before shooting.

Then shooting the ball is scheduled for that time via ``clock.schedule()``.

Lastly, we check if the game should actually end. If the scoring paddle doesn't
have enough points to win yet, the ``state["phase"]`` is set to ``"start"``
again, otherwise to ``"end"``. In that case, ``shoot_ball`` is also unscheduled
so the ball doesn't suddenly start flying even though the game is over.


shoot_ball()
""""""""""""

.. code::

    def shoot_ball():
        if state["start_paddle"] == computer:
            if computer.data["start_direction"] == -1:
                angle = 70 - random.randint(1, 25)
            else:
                angle = -70 + random.randint(1, 25)
        else:
            if keyboard.up:
                angle = 180 - 70 + random.randint(1, 25)
            elif keyboard.down:
                angle = 180 + 70 - random.randint(1, 25)
            else:
                angle = 180 - 50 + random.randint(1, 100)
        ball.angle = angle
        state["phase"] = "game"
        computer.data["bounced"] = False
        player.data["bounced"] = False

    clock.schedule(shoot_ball, computer.data["start_duration"])

This function will trigger the ball to be shot. It's either called via clock
scheduling if the computer paddle should start the next really or when it's the
player who starts, then on a press of the space key.

First, the angle that the ball should travel at is calculated. If the computer
starts the rally, then then the angle will be anywhere from +45 to +71 if it
is travelling upwards at the time of shooting or the same just negative if it
is going downwards.

For the player, it is similar. If the player is going up or down, the angles
are the same, flipped horizontally. If the player is standing still when the
ball gets shot, then the angle is anywhere from -50 to +50 flipped
horizontally.

After the angle has been calculated, it is applied to the ``ball`` actor.

After that, the ``state["phase"]`` is set to ``"game"`` and both paddles get
their ``"bounced"`` value reset. This is done so they will correctly handle a
collision with the ball.

Directly after the function definition, a function call is scheduled since
the computer begins the first rally after opening the game.


update_ball()
"""""""""""""

.. code::

    def update_ball():
        if state["phase"] == "start":
            ball.y = state["start_paddle"].y
        elif state["phase"] == "game":
            if ball.y <= 40 or ball.y >= HEIGHT - 40:
                ball.angle = -1 * ball.angle

            ball.move_forward(BALL_SPEED)

            if ball.collidemask(computer) and not computer.data["bounced"]:
                if computer.left <= ball.x <= computer.right:
                    ball.angle = -1 * ball.angle
                else:
                    ball.angle = 180 - ball.angle
                ball.angle += random.randint(-10, 10)
                computer.data["bounced"] = True
                player.data["bounced"] = False
            elif ball.collidemask(player) and not player.data["bounced"]:
                if player.left <= ball.x <= player.right:
                    ball.angle = -1 * ball.angle
                else:
                    ball.angle = 180 - ball.angle
                if keyboard.up:
                    ball.angle -= random.randint(5, 10)
                elif keyboard.down:
                    ball.angle += random.randint(5, 10)
                else:
                    ball.angle += random.randint(-10, 10)
                player.data["bounced"] = True
                computer.data["bounced"] = False

            if ball.right < 0:
                ball_scored(player)
            elif ball.left > WIDTH:
                ball_scored(computer)

This is the most complicated function in the project. Let's break it down
part by part.


First if conditional
''''''''''''''''''''

First is a simple part. If the game is in the ``"start"`` phase, the ball's
Y position is simply always set to match that of the paddle starting the next
rally.

The rest only happens if a rally is ongoing, so the phase is ``"game"``.


Vertical bouncing
'''''''''''''''''

First of all, bouncing of the top or bottom of the play field is handled.
Angles can be inverted vertically simply by multiplying them with ``-1``.
This is because an angle of zero points straight right, meaning ``90`` points
straight up and ``-90`` points straight down.

Then, the ball is moved with ``move_forward()``. Since the angle of the ball
actor decides where it is pointing, we can use this single function call to
move it whereever it is heading.


Collisions with paddles
'''''''''''''''''''''''

Now comes the more complex part. If the ball hits a paddle, we need it to
bounce off the paddle realistically. At the same time, we want there to be a
small amount of variation in the bounce angle to avoid stalemates where an
angle the ball is flying at is so easy that both computer and player can keep
the rally going forever.

First, we check if the ball collides with one of the paddles, but we also check
if that same paddle has ``"bounced"`` yet. What's this value for? Collisions in
games can be very complicated and a common problem is how to deal with repeated
collisions when only one should occur.

If we needed very realistic collisions, this would be a very nuanced problem,
but we can help ourselves with a trick. Playing the ball back and forth means
that after the ball bounced on the computer paddle, the next bounce MUST happen
on the player paddle and the opposite is also true. Because of this, we can
just see if a collision already happened once since the last time the other
paddle got hit. That's what the ``"bounced"`` value is for.

Once a paddle is collided with, it will set that paddle's ``"bounced"`` to
``True`` to prevent repeat collisions and set the other paddle's value to
``False``, making it ready for the now incoming ball.


Collision with computer
'''''''''''''''''''''''

Let's assume there was a collision with the computer paddle. There is another
conditional that checks whether the position of the ball in the X axis overlaps
the X position of the hit paddle. If that was the case, we can assume that the
paddle was hit on its narrow side from the top or bottom. In that case, we
simply bounce it vertically again by inverting its angle.

If not, we subtracts in angle from ``180``. This is a horizontal bounce because
``180`` angle (straight left) is the exact opposite from ``0`` angle (straight
right). Let's say there is an angle of ``+45`` going into the collision. That
is to say 45 degrees counterclockwise from straight right. Now what we want as
a result is 45 degrees clockwise from straight left. Since positive values are
counterclockwise in PGTurbo and ``0`` is straight right, we can write the
same angle as ``0 + 45``. In the same way, ``180`` is straight left and
clockwise is negative values. Because of this, we can write the resulting angle
after the bounce as ``180 - 45``.

Generalizing this, we can get a horizontal bounce with ``180 - current_angle``.
This also works the other way around. Assuming the angle is ``135`` going into
the collision, then ``180 - 135`` gives a resulting angle of ``45``.

Then we add a small random variation to the collision angle with the computer
and set the ``"bounced"`` values accordingly.


Collision with the player
'''''''''''''''''''''''''

Now let's look at a collision with the player paddle. The first part looks the
same. If there ball is over or under the paddle, we do a vertical bounce,
otherwise a horizontal one.

For the player however, we want to give them some control over how the angle
of the ball changes randomly. If the player is moving the paddle up when the
collision occurs, then it is decreased slightly. If they were moving down,
increased slightly. If they were not moving at all, the same randomness happens
as with the computer paddle.

Then the ``"bounced"`` values are set again, just the opposite of the computer.


Scoring
'''''''

The last part of this function just checks whether the ball has left the screen
on either side and if yes call ``ball_scored()`` either for the player or the
computer depending on which side the ball left on.


Game state setup
----------------

.. code::

    state = {"phase": "start", "start_paddle": computer}

All of that was just setup for the ball, nothing's happened yet...

The last thing to prepare for the game is the ``state`` dictionary with stores
global game state values. For this game, this is just what phase the game is
currently in and which paddle is the one to start the next rally if necessary.


Event hook functions
--------------------

.. code::

    def on_key_down(key):
        if (key == keys.SPACE and state["phase"] == "start"
                and state["start_paddle"] == player):
            shoot_ball()

We only need a single event hook function for when the player presses a key to
start the next rally. As such, we check three conditions:

#. Was the *space* key pressed?
#. Is the current phase the correct one for starting a new rally?
#. Is the paddle to start the next rally the player one?

If all of those are met, ``shoot_ball()`` gets called.


Game loop functions
-------------------

Last are the function definitions for the update draw cycle in PGTurbo.

update()
""""""""

.. code::

    def update():
        update_computer()

        update_ball()

        update_player()

The ``update()`` function is very slim because we've properly split up and
prepared the code to handle the different parts of the game in different
functions.

We simply call the three functions to handle the computer paddle, the ball and
the player paddle. That's it.


draw()
""""""

.. code::

    def draw():
        screen.fill((64, 64, 64))

        computer.draw()
        player.draw()

        screen.draw.text("Computer: {}".format(computer.data["score"]),
                         center=(WIDTH / 4, 40), fontsize=48, color=MAIN_COLOR)
        screen.draw.text("Player: {}".format(player.data["score"]),
                         center=(WIDTH * 3/4, 40), fontsize=48, color=MAIN_COLOR)
        screen.draw.line((WIDTH / 2, 40), (WIDTH / 2, HEIGHT - 40), MAIN_COLOR)

        ball.draw()

        if state["phase"] == "end":
            if player.data["score"] >= WIN_POINTS:
                screen.draw.text("PLAYER WINS", center=(WIDTH / 2, HEIGHT / 2),
                                 fontsize=68, color=MAIN_COLOR)
            else:
                screen.draw.text("COMPUTER WINS", center=(WIDTH / 2, HEIGHT / 2),
                                 fontsize=68, color=MAIN_COLOR)

The draw function is a bit more involved. First, the screen is filled with a
dark gray and the computer paddle and the player are drawn.

The ball is drawn after some text so that it appears on top of them instead of
below. For this game that doesn't matter much since they all have the same
color anyways, but it's just good practise to do so anyways.

We draw the computer paddle and player paddle scores with
``screen.draw.text()``, using ``{}`` in the text to fill with values later with
the ``.format()`` method. This can be used to put dynamic values from variables
into strings, where each ``{}`` in the string is filled with one value in the
parentheses of ``.format()``.

Then, we draw a line vertically across the screen with ``screen.draw.line()``.
The arguments are the starting point and end point for the line, followed by
the color.

Then happens ``ball.draw()``.

Last, if the game has ended, we draw either ``PLAYER WINS`` or
``COMPUTER WINS`` text on screen in the middle with a big font size.

:ref:`Back to the overview <examples_overview>`
