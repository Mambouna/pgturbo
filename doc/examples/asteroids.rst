.. _example_asteroids:

Example game: Asteroids
=======================

:ref:`Back to the overview <examples_overview_asteroids>`

.. image:: /_static/examples/asteroids.png
   :alt: Asteroids
   :height: 500
   :align: center

:download:`Download the project archive here </_downloads/asteroids.zip>`

This explainer will go into detail on how the code of the *asteroids* example
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


Game window global variables
----------------------------

.. code::

    TITLE = "ASTEROIDS"
    ICON = "player"
    WIDTH = 800
    HEIGHT = 600

The game window constants for this game are quite simple, normal setup of
window icon and title.

The dimensions of the game window are made to be a bit wider that they are
tall.


Game mechanics constants
------------------------

This is likely the most complex example game and as such there are quite a few
constants. Because of this, they are covered in different subsections depending
on what game systems they touch.


General constants
"""""""""""""""""

.. code::

    INITIAL_BLOCK_INPUT_DURATION = 1.0
    END_BLOCK_INPUT_DURATION = 2.0
    SOUND_VOLUME = 0.4
    STARS_POSITION = (random.randint(-1 * WIDTH // 2, 0),
                      random.randint(-1 * HEIGHT // 2, 0))

First are constants that affect the game as a whole. The first is how long
player inputs should not be processed after starting the game to avoid
accidentally making an input that was unwanted. The same goes for the second
one, just for the end of the game.

``SOUND_VOLUME`` will be applied to all the used sound effects and can be used
to tune how loud the game should be.

``STARS_POSITION`` is a constant that gets randomized every game session. There
is one large image file for the background star scape for the game. This image
is bigger than the game window so shifting around where it is drawn makes the
game feel as if there were many more star constellations than there actually
are.

So for each run of the game, we randomize a position tuple that sets how the
star scape image is placed. ``(0, 0)`` would mean the topleft corner of the
image is placed at the topleft corner of the game window. That is one possible
extreme of the placement.

The other extreme is half the game window size shifted over on both axes. This
value was chosen because the image in question is bigger than the game window
by half.


Player constants
""""""""""""""""

.. code::

    START_LIVES = 3
    INVULNERABLE_DURATION = 4.0
    BLINK_INTERVAL = 0.4
    THRUST = 0.2
    BRAKE = 0.01
    TURN_SPEED = 4

These constants all affect the player ship in the game. The first is how many
lives the ship starts each game level with. The second is how long the ship is
made invulnerable after being hit by an asteroid. The third is how fast the
ship blinks when it is invulnerable between visible and invisible.

The last three constants control the movement fell of the ship. ``THRUST`` is
how quickly the ship accelerates when the user holds the up arrow key.
``BRAKE`` controls how fast the ship sheds its speed when no acceleration is
made. The ``TURN_SPEED`` sets how quickly the ship turns around when the left
or right arrows are held.


Bullet constants
""""""""""""""""

.. code::

    BULLET_SIZE = 4
    BULLET_SPEED = 10
    BULLET_STAY_DURATION = 1.5

These affect the bullets shot by the player ship. The first is how wide the
bullet circle actors are on screen, the second how fast bullets fly.

The third is after how much time the bullets disappear from the game. As with
everything in the game, bullets wrap around on the game window edges, so
shooting one to the right can cause it fly in from the left again.

If that happened with no limit, there could be thousands of bullets at once
after some time. To prevent this, bullets just disappear after a set amount of
time in the game.


Asteroid constants
""""""""""""""""""

.. code::

    ASTEROID_IMAGES = ("asteroid_1", "asteroid_2", "asteroid_3")
    SPLIT_SIZE_REDUCTION = 0.4
    BIG_SPEED = 1
    MEDIUM_SPEED = 2
    SMALL_SPEED = 3
    BIG_SCORE = 120
    MEDIUM_SCORE = 60
    SMALL_SCORE = 30

These constants manage the asteroids in the game, the obstacles the player ship
has to avoid touching. ``ASTEROID_IMAGES`` is a tuple of which images can be
randomly selected for any new asteroid actor.

``SPLIT_SIZE_REDUCTION`` is how much smaller asteroids when split up by being
hit by a bullet. This value has to stay small enough that reducing the size
of a asteroid at ``scale`` of ``1.0`` won't put them in the negative since that
would cause a crash.

The three following constants are how fast the different sizes of asteroids
move around and the three after that are how much each is worth in points when
shot by a bullet.

The scores here are the baseline and are affected by how much time has passed
before actually being awarded to the player. That will be covered later in more
detail.


General setup
-------------

Sound setup
"""""""""""

.. code::

    sounds.asteroid_explosion.set_volume(SOUND_VOLUME - 0.1)
    sounds.player_explosion.set_volume(SOUND_VOLUME)
    sounds.fire.set_volume(SOUND_VOLUME)

Here, we simply set the volumes of the three sound effects used in the game.
The first is set a bit lower than the constant meant for this because its quite
a bit louder than the other two in the file itself. The adjustment tries to
balance it a bit.


Persistent data setup
"""""""""""""""""""""

.. code::

    storage.load()
    storage.setdefault("highscore", 0)

The game stores the highscore as persistent data. That means it's not data that
will disappear as soon as the game window is closed. To do this, it must be
stored on the file system of the computer.

PGTurbo has the ``storage`` builtin to help you with that. It basically works
like a normal dictionary but it has ``.load()`` and ``.save()`` methods that
read or write it to disk.

So first, we use ``storage.load()``. However, what happens if this is the first
time running the game? If a value is read from a dictionary that doesn't exist,
an error will happen.

For this, ``storage`` has the useful method ``.setdefault()``. It takes a name
(key) for the dictionary and a value. If that name already exists in storage,
nothing is done. If however it isn't there yet, then the name and value will
be inserted.

This way, you can ensure that there is always a safe default value in the
``storage`` dictionary.


Game state setup
""""""""""""""""

.. code::

    state = {"phase": "start", "level": 1, "input_blocked": True,
             "got_highscore": False}

This dictionary is used to track the global state of the game. It has the
following entries:

* ``"phase"`` stores if a level is running, hasn't started yet or is over.
* ``"level"`` tracks which level the player is on, starting at ``1``.
* ``"input_blocked"`` is a boolean that tells the game whether player inputs
  like keyboard keys should be ignored or not. The reason it starts with
  ``True`` is that there is a short window of blocked input at game startup.
* ``"got_highscore"`` is a boolean flag value that tells the level over screen
  if it should display a congratulation about the new highscore.


unblock_input()
"""""""""""""""

.. code::

    def unblock_input():
        state["input_blocked"] = False

    clock.schedule(unblock_input, INITIAL_BLOCK_INPUT_DURATION)

This function simply sets the game state ``"input_blocked"`` to ``False``. The
reason we need a function for this is that ``clock.schedule()`` always needs a
function name to call later.

Scheduling this immediately after defining it means that when the game starts,
used input is briefly blocked to allow the player to orient themselves before
beginning and scheduling the function call will enable user input after the
given delay.


edge_swap_actor()
"""""""""""""""""

.. code::

    def edge_swap_actor(actor):
        if actor.right < 0:
            actor.left = WIDTH
        elif actor.left > WIDTH:
            actor.right = 0

        if actor.bottom < 0:
            actor.top = HEIGHT
        elif actor.top > HEIGHT:
            actor.bottom = 0

This function is used on all actors in the game and simply checks whether they
have left the game window in any direction. If yes, they are teleported to the
other side of the game window so they immediately enter it in the same
direction again.


start_game()
""""""""""""

.. code::

    def start_game(restart):
        player.pos = (WIDTH / 2, HEIGHT / 2)
        player.angle = 90
        player.vel = (0, 0)
        player.data["lives"] = START_LIVES
        make_invulnerable()

        if restart:
            state["level"] = 1
            player.data["score"] = 0

        bullets.clear()

        asteroids.clear()
        spawn_asteroids(state["level"])

        state["phase"] = "game"
        state["got_highscore"] = False
        clock.mark_time("level_start")

This function resets all necessary values to start a new round of the game at
a certain level. The ``restart`` parameter being either ``True`` or ``False``
indicates whether the game should be reset to level 1 and score 0 after the
ship was destroyed or if it should begin the next level with the existing score
if the ship destroyed all the asteroids of the previous level.

First, the player ship is reset. It's teleported to the center of the game
window and oriented upwards. Its velocity is reset to zero so it stays still
and the lives are set to constant value assigned above. The ship is also made
invulnerable at the start of each round so the player has time to get out of
the way of asteroids that spawned on top of them.

If the game should restart from scratch, the level and score are reset.

Afterwards, the ``bullets`` list is emptied. The ``.clear()`` method erases all
values in a list without reassigning an empty list. Since we are dealing with
global variables, using ``.clear()`` avoids potential trouble with either
having forgotten to declare ``global bullets`` above and accidentally creating
a local variable and possible confusion.

Just like the bullet list, ``asteroids.clear()`` also empties that list, after
which new asteroids for the level are created with ``spawn_asteroids()``.

Last, the game state phase is set to ``"game"`` to allow all actors to move and
fulfill their normal functions, the flag tracking if a new highscore was
achieved is reset and a time mark made for when the round was started.

If time marks are unfamiliar, you can store timestamps with
``clock.mark_time("name")`` and then later check how much time has passed since
then with ``clock.time_since_mark("name")``. In this case, we use how much time
has passed in a round to slowly decrease how much score each shot asteroid
gives.

The reason for this is to make scores more interesting. Level 1 always starts
with three big asteroids, so clearing the level would always leave players with
the exact same score if nothing else affected them. Slowly decreasing gained
score with the time in a level means that beside clearing the level, doing so
fastest will give the best score.


end_game()
""""""""""

.. code::

    def end_game(result):
        state["phase"] = result
        if result == "win":
            state["level"] += 1
        state["input_blocked"] = True
        clock.schedule(unblock_input, END_BLOCK_INPUT_DURATION)

        if player.data["score"] > storage["highscore"]:
            state["got_highscore"] = True
            storage["highscore"] = player.data["score"]
            storage.save()

The opposite of ``start_game()``, this function takes care of setting necessary
data when a level ended either from the player dying or succeeding in shooting
all asteroids.

The ``result`` argument contains either ``"win"`` or ``"dead"``. If the player
shot all the asteroids, we increase the current level by one so when the user
continues more asteroids will spawn.

In both cases, we block user input to prevent accidentally directly starting a
new or next round and then schedule unblocking the input with the constant set
delay.

The last thing we need to do is check whether the player achieved a new
highscore. If yes, we note that in ``state["got_highscore"]`` so it can be
displayed on the end screen and update the highscore saved in ``storage`` and
save it to the file system.


get_time_adjusted_score()
"""""""""""""""""""""""""

.. code::

    def get_time_adjusted_score(base_add):
        seconds = clock.time_since_mark("level_start")
        return round(base_add / (1 + seconds / 100))

This function is what allows us to give players different scores based on how
quickly they shot asteroids. It gets the base score a shot asteroid gives as an
argument and then computes a lower actual score to give the player.

It does this by checking how much time has passed in seconds since the current
level was started with ``clock.time_since_mark("level_start")``.

The base score from the asteroid is then divided by one plus the elapsed
seconds divided by 100. The reason for why we do it like this is a few
different goals we want:

* At time zero the full score should be given.
* No matter how long it takes, the player should always get at least a few
  points (so the result shouldn't become zero).
* No matter what the received score should never become negative (actually
  reducing the player score).

For cases where we want something to slowly become less, fractions can be very
useful. For this, we basically always just divide a starting value by one
plus the elapsed time divided by a control value. In this case, the base score
is the starting value, the elapsed time are the seconds and the control value
is ``100``.

Let's plug in a few numbers to see what happens. All of the following examples
assume a large asteroid that gives ``120`` base score was shot.

* After 10 seconds, the player would get ``109`` score
  (``120 / (1 + 10 / 100)``).
* After a minute, the player would get ``75`` socre
  (``120 / (1 + 60 / 100)``).
* After 100 seconds, the player would get ``60`` score
  (``120 / (1 + 100 / 100)``).

Specifically for this kind of formula, the control value is how long you want
it to take before the base value is cut in half. So a control value of ``100``
means that after 100 seconds, each asteroid shot will only be worth half as
many points.

Looking at it now, this might have been another good value to make into a game
mechanic constant to allow easier tweaking of how the scoring works.

The result of the calculation is rounded with the ``round()`` function on
return to always keep scores at full numbers.


Player setup
------------

With general utility done, next we create the player ship.


Actor setup
"""""""""""

.. code::

    player = Actor("player_horizontal", (WIDTH / 2, HEIGHT / 2))
    player.angle = 90
    player.data["invulnerable"] = True
    player.data["lives"] = START_LIVES
    player.data["score"] = 0

The player actor is created with the player ship icon pointing to the right
to align the image with the ``angle`` of the actor. That property is then set
to ``90`` so the player starts the game facing up.

Then the relevant value for the player are set up in the ``.data`` dictionary.
``"invulnerable"`` determines whether the player can lose lives by being hit by
asteroids. ``"lives"`` is how many time the ship can get hit before a game over
and is controlled by a game mechanic constant. ``"score"`` is how many points
the player has gotten by shooting asteroids yet.


make_vulnerable()
"""""""""""""""""

.. code::

    def make_vulnerable():
        player.data["invulnerable"] = False
        player.opacity = 1.0
        clock.unschedule(blink_player)

When the player is hit by an asteroid, they are made invulnerable for some time
to give the player time to react. This function stops that invulnerable state.

It first sets the appropriate value in the ``actor.data`` dictionary. It also
sets ``player.opacity = 1.0`` to make sure the player is visible. During the
invincibility, the player blinks in and out of visibility so when it ends we
need to be sure the player ship can be seen.

Last we unschedule the blinking function since that is what keeps the player
changing visibility, so we don't want the player to be made invisible after
just setting it visible again.


make_invulnerable()
"""""""""""""""""""

.. code::

    def make_invulnerable():
        player.data["invulnerable"] = True
        clock.schedule(blink_player, BLINK_INTERVAL)
        clock.schedule(make_vulnerable, INVULNERABLE_DURATION)

This is the opposite of the previous function, starting the invulnerability of
the player ship.

It sets the same value on the player ship and then schedules both the blinking
function that always switches the player between visible and invisible and the
call to the ``make_vulnerable()`` function that will end the invincibility
again.


blink_player()
""""""""""""""

.. code::

    def blink_player():
        if player.opacity == 0.0:
            player.opacity = 1.0
        else:
            player.opacity = 0.0
        clock.schedule(blink_player, BLINK_INTERVAL)

This is the function that keeps the player blinking in and out of visibility.
If the ship is visible, make it invisible, otherwise the opposite, all via the
``.opacity`` property.

Each call then schedules the next call, meaning this would continue forever if
it was not interrupted by the ``clock.unschedule()`` call in the
``make_vulnerable()`` function.


lose_life()
"""""""""""

.. code::

    def lose_life():
        sounds.player_explosion.play()
        player.data["lives"] -= 1
        if player.data["lives"] == 0:
            end_game("dead")
        else:
            player.opacity = 0.0
            make_invulnerable()

This function is called whenever the player ship should lose a life point.
First it plays a sound effect (``sounds.player_explosion``) and also decreases
the ``"lives"`` value of the player.

If the lives have hit zero, the game is over and we call ``end_game()`` with
``"dead"`` as the argument to show a lose screen.

If not, the player is made invisible and ``make_invulnerable()`` is called to
prevent them losing multiple lives at once. Inside that function the
``blink_player()`` call will also be scheduled to flip the visibility of the
ship again.

The reason we make it invisible here is just to start the process with some
immediate visual feedback, not just from audio.


update_player()
"""""""""""""""

.. code::

    def update_player():
        if keyboard.up:
            add_vel = player.velocity_towards_angle(player.angle, THRUST)
            player.vx += add_vel[0]
            player.vy += add_vel[1]
        else:
            player.vx *= 1.0 - BRAKE
            player.vy *= 1.0 - BRAKE

        if keyboard.left:
            player.angle += TURN_SPEED
        elif keyboard.right:
            player.angle -= TURN_SPEED

        player.move_by_vel()
        edge_swap_actor(player)

Last for the player is its update function.

First, if the up arrow key is held, we get a velocity in the current facing
direction and then add it to the current velocity. If up is not held, instead
we break the velocity of the player ship slightly. By breaking only by small
amounts but doing so each frame the player is not accelerating, we get the ship
to smoothly come to a relative stop when the player isn't pushing it forward.

After that we manage turning the player ship. Since it always moves according
to its ``angle`` property, we just need to increase or decrease that when the
left or right arrow keys are held. The specific values for all of these come
from game mechanic constants to make adjustments easier.

Last, we actually move the player ship actor according to the newly changed
velocity with ``.move_by_vel()`` and also call ``edge_swap_actor()`` so that if
the movement caused the player ship to leave the screen, it will then wrap
around to the other edge of the screen and come back in.


Bullet setup
------------

.. code::

    bullets = []

After the player, now we need to take care of the bullets the ship can shoot
to destroy asteroids. First is to have a list that can hold all the bullet
actors present in the game.


delete_bullet()
"""""""""""""""

.. code::

    def delete_bullet(bullet):
        bullets.remove(bullet)
        clock.unschedule(delete_bullet, bullet)

This function just removes a bullet actor from the ``bullets`` list and
unschedules the same call. The reason we need to use ``clock.unschedule()``
here is that there are two circumstances in which the function is called.

#. When a new bullet is created, a call to ``delete_bullet()`` is immediately
   scheduled since bullets disappear after a short time by themselves. When
   this call happens, there are no more calls to delete this bullet left in the
   clock scheduling queue.
#. If a bullet hits an asteroid, this function is also called however and if
   that happens, a call to the function is still in the clock scheduling queue.
   Since the function deletes the bullet though, trying to call the function
   again for the same bullet will result in an error from ``bullets.remove()``.

To make sure the possible error described in the second scenario doesn't
happen, we just always unschedule the ``delete_bullet()`` function call for the
deleted bullet just in case. Trying to unschedule something that wasn't
scheduled isn't any problem, so with this solution there is nothing to worry
about.


shoot_bullet()
""""""""""""""

.. code::

    def shoot_bullet():
        sounds.fire.play()
        bullet = Actor.Ellipse(BULLET_SIZE, BULLET_SIZE, "white", player.pos)
        bullet.vel = bullet.velocity_towards_angle(player.angle, BULLET_SPEED)
        bullets.append(bullet)
        clock.schedule(delete_bullet, BULLET_STAY_DURATION, bullet)

This function is what creates new bullet actors and fires them. First, it plays
the appropriate sound effect ``sounds.fire``.

Then, a new simple shape actor of a circle is created and placed on top of the
player ship. Since bullets don't hit the ship just asteroids we can just place
them together.

The bullet then gets its ``vel`` set to one matching the ``angle`` of the
player ship but with the speed for bullets from the matching constant.

The bullet is then added to the list of all ``bullets``.

Last, we schedule the deletion of the bullet actor after a short while. For
this we use the fact that function calls can be scheduled with arguments like
``clock.schedule(function_name, delay, arg1, arg2, arg3, ...)``. ``bullet`` at
the end of the argument list means this function call is scheduled specifically
with this bullet actor as its argument and will destroy only this specific one
when the call happens.



update_bullets()
""""""""""""""""

.. code::

    def update_bullets():
        for bullet in bullets:
            bullet.move_by_vel()
            edge_swap_actor(bullet)

This function updates all the bullets. It simply moves them all by the velocity
set up at their creation. Then it teleports the bullet across the game window
if it exited on one side to make if fly back in from the other side next frame.


Asteroid setup
--------------

.. code::

    asteroids = []

With player and bullets set up, now we need the obstacles of the game. Just
like with the bullets, we need a list to keep all asteroids in.


spawn_asteroids()
"""""""""""""""""

.. code::

    def spawn_asteroids(level):
        for i in range(2 + level):
            new_asteroid = Actor(random.choice(ASTEROID_IMAGES))
            new_asteroid.x = random.randint(100, WIDTH - 100)
            new_asteroid.y = random.randint(100, HEIGHT - 100)
            new_asteroid.angle = random.randint(0, 359)
            new_asteroid.data["speed"] = BIG_SPEED
            asteroids.append(new_asteroid)

This function creates the right amount of asteroids for a certain level. Each
level creates one more asteroid than the last, starting with three asteroids at
level one. As such, we just use a simple ``for`` loop to make as many
repititions as we need.

Each asteroid is an actor with a random image chosen from the available ones.
The position and ``angle`` are then also randomized to make each asteroid move
in a different way.

Since these asteroids are created at the start of the game, they are all the
large and unbroken kind of asteroid that moves very slowly. Because different
sizes move at different speeds, we let each asteroid track its own speed in
``.data["speed"]``.

Last, we also add each new asteroid to the big list.


destroy_asteroid()
"""""""""""""""""""

.. code::

    def destroy_asteroid(asteroid):
        sounds.asteroid_explosion.play()
        asteroids.remove(asteroid)

        if asteroid.data["speed"] != SMALL_SPEED:
            for i in range(3):
                new_asteroid = Actor(random.choice(ASTEROID_IMAGES), asteroid.pos)
                new_asteroid.angle = random.randint(0, 359)
                new_asteroid.scale = asteroid.scale_x - SPLIT_SIZE_REDUCTION
                if asteroid.data["speed"] == BIG_SPEED:
                    new_asteroid.data["speed"] = MEDIUM_SPEED
                else:
                    new_asteroid.data["speed"] = SMALL_SPEED
                asteroids.append(new_asteroid)

        if asteroid.data["speed"] == BIG_SPEED:
            player.data["score"] += get_time_adjusted_score(BIG_SCORE)
        elif asteroid.data["speed"] == MEDIUM_SPEED:
            player.data["score"] += get_time_adjusted_score(MEDIUM_SCORE)
        else:
            player.data["score"] += get_time_adjusted_score(SMALL_SCORE)

        if len(asteroids) == 0:
            end_game("win")

This function is a bit more complex so let's take it one step at a time. It's
called when a bullet hits an asteroid and so that asteroid has to be split up
or just disappear if it is small enough.

First, we play a sound effect and remove the current asteroid from the list.

Then, if the ``data["speed"]`` of the destroyed asteroid was not that of a
small asteroid, we split it up intro three smaller chunks. This works since
the different asteroid sizes all have different speeds, so we can use the speed
to identify if an asteroid is big, medium or small sized.

That means that if a small asteroid is hit, it just disappears and is not split
again.

If the asteroid should be split however, the following happens three times
since each split creates three new asteroids. A new actor is created, again
from a random image chosen but not the position matches the one of the hit
bigger asteroid. The ``angle`` is randomized again however so all three new
smaller asteroid don't move the same way.

The scale is then reduced to make the asteroid smaller, like a chunk flying
off from the big destroyed one. Then the same kind of check as above is made
again. If the previous speed was ``BIG_SPEED``, we know we now have new medium
sized asteroids so we assign their ``data["speed"]`` accordingly. Otherwise
they have to be small asteroids, so they get that speed.

Then each new chunk is added to the list.

After managing the splitting up of asteroids, we need to give the player
points. This is also dependent on the size of asteroids and can thus again be
checked via their ``data["speed"]``. For each case, we call
``get_time_adjusted_score()`` with the appropriate base score for each size
of asteroid and add that to the ``player.data["score"]``.

Lastly, if there are no more asteroids left (i.e. the list of all of them is
empty), then the player ship has successfully cleared the current level and
we call ``end_game()`` with the argument ``"win"``.



update_asteroids()
""""""""""""""""""

.. code::

    def update_asteroids():
        i = 0
        while i < len(asteroids):
            asteroid = asteroids[i]
            asteroid.move_forward(asteroid.data["speed"])
            edge_swap_actor(asteroid)

            if not player.data["invulnerable"] and asteroid.colliderect(player):
                lose_life()

            hit = False
            k = 0
            while k < len(bullets):
                bullet = bullets[k]
                if asteroid.colliderect(bullet):
                    destroy_asteroid(asteroid)
                    delete_bullet(bullet)
                    hit = True
                    break
                else:
                    k = k + 1

            if not hit:
                i = i + 1

In this function, we move asteroids and check if they hit the player or are hit
in turn by bullets. To do this, we iterate through all the asteroids in the
``asteroids`` list.


While loops
'''''''''''

We use a ``while`` loop for it because it allows us to control how we get to
the next element in a list. Usually using ``for`` loops is much handier to do
something with every element of a list, but there is a problem if we delete
items from the list during the loop in that elements are skipped.

We can prevent this by using a while loop of the following rough shape::

    i = 0
    while i < len(some_list):
        some_element = some_list[i]

        # ... Do whatever we want here ...

        if condition_to_remove_the_element:
            # ... Maybe do something else ...
            some_list.pop(i)
        else:
            i = i + 1

The general idea is that we go through each element and decide based on some
condition whether that element should be kept in the list or not. If yes, we
just increment the loop variable and move on, normal ``while`` style.

If however the element should be removed, we do so and DON'T increment the loop
variable. What happens then is that removing the element from the list makes
all elements behind is shift forward by one index. So if we are at ``i`` = 4
and remove the element at index 4, the next element in the list will have the
same index of 4 again in the next cycle. So not increasing ``i`` means we will
correctly handle the next element in the list too.

We use two of these kinds of ``while`` loops in the function. One to go through
all the asteroids and one to go through all the bullets for each asteroid.


Movement and player collisions
''''''''''''''''''''''''''''''

.. code::

    asteroid = asteroids[i]
    asteroid.move_forward(asteroid.data["speed"])
    edge_swap_actor(asteroid)

    if not player.data["invulnerable"] and asteroid.colliderect(player):
        lose_life()

First, for each asteroid we move it by its ``data["speed"]`` and then wrap it
around the game window if it left it with ``edge_swap_actor()``.

Second, we check if the player ship is vulnerable and if yes, if the asteroid
is touching it. In that case, the player ship looses a life point via
``lose_life()``.


Collisions with bullets
'''''''''''''''''''''''

.. code::

    hit = False
    k = 0
    while k < len(bullets):
        bullet = bullets[k]
        if asteroid.colliderect(bullet):
            destroy_asteroid(asteroid)
            delete_bullet(bullet)
            hit = True
            break
        else:
            k = k + 1

    if not hit:
        i = i + 1

Now comes the tricky part. We need to see if the asteroid should get destroyed
because it was hit by a bullet. Because we need a second ``while`` loop to
check each bullet, we can't use a single condition like in the idealized
example above. Instead, we use the variable ``hit`` to track if the asteroid
was struck or not, defaulting to ``False``.

Now we iterate through all bullets mostly the same way we do for the asteroids
themselves. It's important here not to use ``i`` as the loop variable again as
its already used for the outer loop managing the asteroids, so instead this
time we use ``k``.

For each bullet, we check if the current asteroid collides with the bullet. If
not, we increment the loop variable. If there is a hit, we do several things.

We remove the asteroid with ``destroy_asteroid()`` and remove the bullet with
``delete_bullet()``. We also set ``hit = True`` so the outer ``while`` loop
knows we removed an asteroid from the list and won't increment the outer loop
variable.

Last, we ``break`` from the inner ``while`` loop since checking the rest of the
bullets doesn't make sense. If the asteroid is already destroyed, we don't need
to check if other bullets would double destroy it.

Now outside of the inner ``while`` loop, the outer one going through all the
asteroids only increments ``i`` if the current asteroid was not ``hit``.


Event hooks
-----------

.. code::

    def on_key_down(key):
        if state["input_blocked"] or key != keys.SPACE:
            return

        if state["phase"] == "game":
            if not player.data["invulnerable"]:
                shoot_bullet()
        elif state["phase"] == "win":
            start_game(False)
        else:
            start_game(True)

We need the ``on_key_down()`` hook only for the space key and only if inputs
by the player are currently allowed. As such, if either input is blocked or
the input was not from the space key, the function returns and thus nothing
happens.

Otherwise what the space key does depends on the current game phase. If the
game is ongoing, then it shoots a bullet. If the game has been won, then
pressing space starts the next level and if not, this means the game is over
and the player ship was destroyed. In that case, a new round is started but it
resets the level to one and the score to zero.


Game loop
---------


update()
""""""""

.. code::

    def update():
        if state["phase"] == "game":
            update_player()
            update_bullets()
            update_asteroids()

The game loop ``update()`` function mostly just calls the specific functions
taking care of the player ship, the bullets and the asteroids. They only do
so however if the game is ongoing, i.e. ``state["phase"] == "game"``.

This is a simple way to effectively freeze the game once it is won or lost.


draw()
""""""

.. code::

    def draw():
        screen.clear()
        screen.blit("stars", STARS_POSITION)

        for bullet in bullets:
            bullet.draw()

        for asteroid in asteroids:
            asteroid.draw()

        player.draw()

        if state["phase"] == "start":
            screen.draw.text("PRESS SPACE TO START",
                             center=(WIDTH / 2, HEIGHT / 2 - 80), fontsize=48)

        elif state["phase"] == "game":
            for i in range(player.data["lives"]):
                screen.blit("player", (5 + 30 * i, 5))

            screen.draw.text("Level: {}    Score: {}".format(state["level"],
                                                             player.data["score"]),
                             midtop=(WIDTH / 2, 10), fontsize=32)
            screen.draw.text("Highscore: {}".format(storage["highscore"]),
                             topright=(WIDTH - 5, 10), fontsize=32)

        else:
            if state["phase"] == "dead":
                main_text = "YOU DIED"
                start_text = "Press SPACE to restart"
            else:
                main_text = "YOU CLEARED LEVEL {}".format(state["level"] - 1)
                start_text = "Press SPACE to start the next level"

            screen.draw.text(main_text, center=(WIDTH / 2, HEIGHT / 2 - 40),
                             fontsize=48)
            screen.draw.text("Score: {}".format(player.data["score"]),
                             center=(WIDTH / 2, HEIGHT / 2 + 40), fontsize=36)

            if state["got_highscore"]:
                screen.draw.text("New Highscore!",
                                 center=(WIDTH / 2, HEIGHT / 2 + 80), fontsize=36)

            if not state["input_blocked"]:
                screen.draw.text(start_text, center=(WIDTH / 2, HEIGHT / 2 + 120),
                                 fontsize=36)

The final function of the game, ``draw()``. First, we clear the screen of
anything that was on it previously with black color with ``screen.clear()``.
Then we blit the star scape image onto the game window at the previously
randomized ``STARS_POSITION``.

We still need ``screen.clear()`` since the *stars* image has a transparent
background so only blitting it would not erase the previous frame.

Then we draw all the actors, first bullets then asteroids and last the player
ship. The ship is last because we want it to show up above asteroid images so
it needs to be drawn after them.

The whole rest of the function is drawing the necessary interface elements and
text for different game phases.

If the game hasn't started yet, we just draw a big text label telling the
player how to start the game.

If we are in a level, we draw some text to display the level, score and
highscore but more interesting is the display of life points.

Many games feature single symbols to represent one life point like a heart. In
this game, we use the ship image but upright as a life symbol. To draw the
amount of life points the player has then, we can just do a loop for however
many life points there are and ``screen.blit()`` the image once each time,
shifting the position of the blit over to the right with each cycle.

If a level has ended, we determine what text to show depending on if the player
won or lost the round and then show that together with their score.

Only if they got a new highscore, we congratulate the player with a text
message for that and only once the player is free to act again after the input
is unblocked we show them to restart or start the next level with the space
key.


Note on colliderect()
---------------------

All collision checks in this game are done with ``Actor.colliderect()`` instead
of the more precise ``Actor.collidemask()``. That is because ``.collidemask()``
is far more performance intensive and we need a lot of collision checks in the
game.

If the player fires bullets quickly, there could be around twenty of them in
the game at once while even at level one there could be as many as 27 small
asteroids at the same time.

If each of those asteroids has to check if it was hit by any bullet, that is
540 collision checks every single frame in the worst case scenario.

Using ``.collidemask()`` here could very well still work on your PC if it is
strong enough, but using ``.colliderect()`` is the safer choice since these
examples should also be playable on weaker hardware.

Other examples use ``.collidemask()`` often since they require far fewer
collision checks in total and thus it is safe to do so.

*For your own games, use ``.collidemask()`` only sparingly where you really
need a lot of precision and always use ``.colliderect()`` if possibly large
lists of actors have to check for collisions with other whole lists of actors.*

:ref:`Back to the overview <examples_overview_asteroids>`
