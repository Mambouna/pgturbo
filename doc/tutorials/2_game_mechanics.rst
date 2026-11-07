.. _tutorial_game_mechanics:

Tutorial: Game mechanics
========================

Our script is fun, but proper games need goals to fulfill, scores to track or
challenges to overcome. Let's add some proper game mechanics to our script to
make it more interesting.

How about the player has to go to different food items and eat them to get
points? It would be easy to add some at certain spots in the game world, but
many games make use of a lot of random elements to keep play interesting. 

The following is a rather chunky block of code to add, so make sure you check
where each piece of code is supposed to go (the comments indicate what's before
and after each)::

    # import pgtrun is above here

    import random

    # WIDTH = 800 is below here

    # player.pos = ... is above here

    food_items = []

    def new_food():
        if len(food_items) < 5:
            fresh_food = Actor.Triangle(30, 30, "orange")
            fresh_food.x = random.randint(20, WIDTH - 20)
            fresh_food.y = random.randint(20, HEIGHT - 20)
            fresh_food.angle = random.randint(0, 359)
            food_items.append(fresh_food)

    clock.schedule_interval(new_food, 2.0)

    # def update(): is below here

    # player.draw() is above here

        for food in food_items:
            food.draw()

    # pgtrun.go() is below here

Suddenly there's triangles popping up all over the place!

#. With ``import random``, we bring in functions that we can use to get random
   numbers or choices. These are important since most games use random events
   heavily.
#. ``food_items = []`` creates a list in which we'll hold all the new game
   objects we'll make. In games, there's often many game objects of the same
   type, so saving them together in a list so we can always apply the same
   behavior to them makes a lot of sense.
#. ``new_food()`` is a function that creates a new Actor game object
   (``fresh_food = Actor.Triangle(...)``), puts it in a random position in the
   game window (``fresh_food.x = random.randint()``) and rotates it around
   randomly as well (``fresh_food.angle = random.randint()``). ``angle`` is the
   property of an actor controlling its rotation.

   Last in the function, we add the new food to the list of all food items
   (``food_items.append(fresh_food)``).
#. With ``clock.schedule()``, we can tell the game to call a function after a
   certain period of time. Using ``schedule_interval()``, that function is
   called again and again after the same amount of time. In this case, we want
   our function to be called every two seconds, so the arguments are
   ``new_food`` and ``2.0``.

   Note that we don't put ``new_food()`` as the argument, since that would
   immediately call the function. We use the name of the function without (),
   so that clock will call it for us later.

   The ``clock`` builtin is one of the key tools in PGTurbo that allows you to
   make complex game mechanics, because it means you can have things happen
   on timers, which is a constant necessity in much of game development.
#. In the ``draw()`` function, we go through all foods in the list and draw
   each of them on the game window.

Now we should make it so our player can eat the food::

    # if keyboard.down: player.y = ... is above here

        i = 0
        while i < len(food_items):
            food = food_items[i]
            if food.collidemask(player):
                food_items.pop(i)
            else:
                i = i + 1

    # def draw(): is below here

That's it.

#. In the ``update()`` function, we go through each food item with a ``while``
   loop. We don't use a ``for`` loop because we might remove objects from the
   list we are iterating through, which skips other items in the list in a
   ``for`` loop.
#. We repeat until we are at the end of the list of food items, using a
   variable to track which index we are currently on: ``i``.
#. We assign each food item to a variable name and then check whether it is
   currently touching the player with ``if food.collidemask(player):``. In
   that case, we simply remove the item from the list of all foods.

   Since we use the list to draw all foods, its as if the food item
   disappeared.
#. Only if there is no collision we advance our list index counter. We do this
   so that if we removed an element, the next loop will get the element that
   moved up in the list without skipping it.

Seeing the ellipse swallow triangles can be fun, but most games let you track
your progress or points somehow so we should add a score::

    # player.pos = ... is above here

    player.data["score"] = 0

    # food_items = [] is below here

    # food_items.pop(i) is above here

                player.data["score"] = player.data["score"] + 1

    # else: i = i + 1 is below here

    # food.draw() is above here

        screen.draw.text("Score: " + str(player.data["score"]), fontsize=36,
                         center=(WIDTH / 2, HEIGHT - 40))

    # pgtrun.go() is below here

With a few quick changes, the game shows us how much we've eaten.

#. First we give the player actor a new value to track with
   ``player.data["score"] = 0``. ``Actor.data`` is a dictionary you can use to
   manage any game mechanics related values that an actor should have like a
   score, health points, movement speeds or anything else.

   Putting values in uses ``Actor.data["name"] = value`` and getting a current
   value is ``Actor.data["name"]``.
#. Then we just add one to the score whenever a food item is eaten (= removed
   when touching the player).
#. Last is to display the score for the user to see. PGTurbo has a powerful
   builtin way to draw and style text on the screen. You just give it a string
   to display and set the styling as you want.

   In this case, increasing the fontsize a bit helps and we place the center
   of the text display in the middle and towards the bottom of the game window.

**That was a whirlwind of changes, but now it's starting to feel like a proper
game, right?**

We have a player character to move, goals to complete that keep coming and a
point system to track our progress.

Now that the game mechanics are taken care of, we should make the game look and
sound nicer. If that interests you, keep following along in the
:ref:`next tutorial on images, sounds and music <tutorial_images_sounds_and_music>`.

Otherwise, the :ref:`PGTurbo overview <overview>` is still a great place to
start looking for any details that interest you.
