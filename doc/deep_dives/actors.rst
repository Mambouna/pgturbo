.. _deep_dive_actors:

Deep dive: actors
=================

:ref:`Reference page on actors <reference_actor>`

Actors are the fundamental game objects in PGTurbo. Each actors has an
image it displays and a variety of useful properties and methods to use on
them. You create an actor by supplying an image name for it to use::

    alien = Actor("alien")

The image name must match a filename (without the file extension) in the
*images* :ref:`resource folder <deep_dive_resources_and_storage>`.

After creation, you can change the actor's properties to move it around the
game world, change its size and many other things::

    def update():
        if keyboard.left and alien.x > 0:
            alien.x = alien.x - 10
        elif keyboard.right and alien.x < WIDTH:
            alien.x = alien.x + 10

The code above moves the alien left and right only up to the edges of the game
window based on pressed arrow keys on the keyboard. The ``.x`` and ``.y``
properties are the X and Y position of the actor's anchor point in the game
world. Anchor points are discussed in more detail below.

Checking the properties allows you to react to where in the game world an
actor is and changing them moves the actor around.

If you copy the code into your own script, you won't see any of that however.
That is because to be able to see actors, we must draw them in the ``draw()``
function::

    def draw():
        screen.clear()
        alien.draw()


These basics should get an actor on your screen and moving around. The
following sections each go into more detail on single topics.


.. _deep_dive_actors_creating_actors:

Creating actors
---------------

To create an actor, you instance an object of the ``Actor`` class. If that
sounds confusing, don't worry. This is a fundamental concept of object-oriented
programming, but for PGTurbo, you won't need to know all of the details.

The broad strokes are this:

#. The ``Actor`` class is provided by PGTurbo and basically defines what an
   actor is and what it can do.
#. To actually use actors, you create a specific object from the class (the
   blueprint so to speak) and save that to a variable (or in a list or
   similar).
#. Once that's done, you can manipulate the game object by writing the variable
   name followed by a period (``.``) and then either a property name or a
   function call.

Here's a short example to show all of that in action::

    ninja = Actor("ninja")
    ninja.x = 300
    ninja.y = 150
    
    def update():
        if keyboard.space:
            ninja.move_towards_point(mouse.pos, 10)

The first line in the example above is where a new actor game object is
created. To do so, we call a class name (notice it starts with a capital
letter) like a function. PGTurbo provides the ``Actor`` class to use for us.

In the parentheses, we can put values that will be used to create the game
object. In this case, it's the name of the image the actor should use. This
name will be used by PGTurbo to load an image from the *images*
:ref:`resource directory <deep_dive_resources_and_storage>`. The short version
is that you'd need a file named *ninja.png* in a folder names *images* next to
your game's ``.py`` file for PGTurbo to load it. Other formats are possible but
PNGs usually work best because of their transparent backgrounds.

The following two lines access properties of the actor and set them to a value.
This works just like setting a variable to a certain value, but an object is
a collection of many variables all belonging to a single thing. In this case,
that thing is a game object, so it has many properties around its position,
rotation, scale and others. The ``.x`` and ``.y`` properties are the position
of the actor on the X and Y axes respectively.

In the ``update()`` function, if the space key is pressed, we make the game
object move towards the mouse pointer. This is done by calling a function on
an object, also called a method. Just like properties, game objects have many
different functions that can all be used like ``actor.function()``. Functions
called like this always act on the object they are called from.

If you call ``actor_a.move_towards_point()``, only the actor saved in that
variable will move in the game. If there is also an actor B on screen, that one
will stay still unless you call ``actor_b.move_towards_point()``.


.. _deep_dive_actors_creating_actors_arguments:

Creating actors with more arguments
"""""""""""""""""""""""""""""""""""

As we saw before, we put information that should be used in the creation of an
actor in the parentheses after ``Actor``. The minimum for this for normal
actor creation is an image name like ``"ninja"``. We can however provide more
to set up the new actor position and anchor in a single line::

    ninja = Actor("ninja", (300, 150), anchor=("center", "bottom"))

The code above is equivalent to this::

    ninja = Actor("ninja")
    ninja.pos = (300, 150)
    ninja.anchor = ("center", "bottom")

When creating an actor, the first argument in the parentheses must be the image
name to use. A second optional argument can be the position the actor should
start at as a position tuple like ``(x, y)``.

After that, you can set up the `anchor` property as well with a keyword
argument. Anchors are explained in a dedicated section below.

If you don't give a position tuple, you can instead set the initial position
with one of the symbolic position properties as a keyword argument::

    ninja = Actor("ninja", bottomright=(300, 150), anchor=("center", "bottom"))

How those symbolic position properties are different will be explained in the
section on positioning actors below. The available ones for setting during
actor creation are ``topleft``, ``midtop``, ``topright``, ``midleft``,
``center``, ``midright``, ``bottomleft``, ``midbottom``, ``bottomright``.

*Note:* Giving both an unnamed position tuple as well as a symbolic position
argument or multiple different symbolic position arguments will error and cause
a crash.


.. _deep_dive_actors_creating_actors_simple_shapes:

Actors from simple shapes
"""""""""""""""""""""""""

If you don't have images to use for your game yet, don't worry. You can start
by creating actors from simple colored shapes like rectangles or circles.

To do so, call ``Actor.Shape()`` with a specific shape name instead of just
``Actor()``.

The following shapes are possible::

    actor_recard = Actor.Rectangle(100, 100, "red")
    actor_elli = Actor.Ellipse(60, 20, "blue")
    actor_tristan = Actor.Triangle(50, 15, "green")

As you can see, the arguments put into the parentheses are different from when
we create an actor with an image. All simple shape constructors for actors need
the following three arguments in order: ``width``, ``height``, ``color``.

These three basically replace the single ``image_name`` argument normal actors
get. After those three, you can put other arguments like before: the position
as a position tuple and anything else as a keyword argument like
``property=value``.

Actors with simple shapes are handy because they are very easy to replace later
when you have images to use. Just make sure the simple shape actors have
roughly the right width and height you are planning for. Then replacing them
later is done in a single line::

    actor_recard = Actor("character_recard")

Because simple shape actors work exactly the same as normal actors, once you've
replaced the line you created the actor on, the rest of your game will work
exactly as before without any adjustment.

The only exception to this would be if the image you chose has a very different
size from the simple shape actor you used before, since then the base size of
the actor will be different.


.. _deep_dive_actors_draw:

Drawing actors on screen
""""""""""""""""""""""""

Once an actor is created, you might expect that you can run your game and see
that they are there, but that is not the case. Remember that with the game loop
update/draw cycle, we have to write the code that displays the game ourselves.

For actors, this is very easy: ``Actor.draw()``. The ``.draw()`` will take care
of everything for you, displaying the actor image at the correct position,
scale, rotation, tint and opacity.

To get all of your game's actors on screen then, you simply need to call
``.draw()`` on each of them in the ``draw()`` function::

    import random    

    ninja = Actor("ninja")
    dots = []
    for i in range(10):
        dot = Actor.Ellipse(20, 20, "blue")
        dot.x = random.randint(10, WIDTH - 10)
        dot.y = random.randint(10, HEIGHT - 10)
        dots.append(dot)

    def draw():
        screen.clear()
        ninja.draw()
        for dot in dots:
            dot.draw()

In the example above, we create one normal actor with an image and then ten
small simple shape actors looking like circles with a loop stored in a list.
In the ``draw()`` function, we first draw the ninja actor and then go through
the same list calling the same method on each of the small circle actors.


.. _deep_dive_actors_draw_image:

Changing actor image
--------------------

If you want to change the image an actor display, for example to change a fresh
apple to an eaten one after the player touched it, you just set the ``.image``
property of the actor::

    def update():
        if player.colliderect(apple):
            apple.image = "apple_bite"

The same rules apply as when creating an actor. The image name must be a
filename from the *images*
:ref:`resource directory <deep_dive_resources_and_storage>` without the file
extension.

You can also check what the current image is and will get the name back::

    def on_key_down():
        if coin.image == "heads":
            coin.image = "tails"
        else:
            coin.image = "heads"


.. _deep_dive_actors_positioning_and_anchor_points:

Positioning and anchors points
------------------------------


.. _deep_dive_actors_anchor_points:

Anchor points
"""""""""""""

One of the most important things your actors can do in a game is move. Because
it's so important, there are a lot of ways to move them around, but to
understand how actors move, we first have to understand their anchor points.

The anchor point of an actor is the specific spot on its image that the actor's
position refers to. Here's a quick example: If we have a ninja actor with an
image that is 48 by 64 pixels in size, where should the single position tuple
that represents an actor's position point to? The top left corner of the image?
The center bottom spot? The middle of the entire image?

There is no single right answer for all cases. For a spaceship maybe the
position should refer to the center of the image. For a character in a
platformer, maybe it would be better if the position is the center bottom point
to make it easier to check whether the actor is "standing" on the ground.

To allow any of these possibilitier, actors have an ``anchor``. This is where
in the actor image the position property of the actor actually points to. By
default the anchor has a value of ``("center", "center")``. This means the
anchor point is in the middle of the actor image in both axes.

The first value in the tuple is where the anchor should be horizontally on the
actor. Possible values are ``"left"``, ``"center"`` and ``"right"``. The second
value is where the anchor should be vertically, allowing ``"top"``,
``"center"`` and ``"bottom"``. The possible combinations from these values
should be enough for most usecases.

.. image:: /_static/actor/anchor_points.png

Alternatively, you can set the anchor with pixel values relative to the top
left corner of the actor image. So doing ``ninja.anchor = (10, 20)`` would put
the anchor point ten pixels to the right of the image's left edge and twenty
pixels from the top edge of the image.


.. _deep_dive_actors_positioning_properties:

Positioning with properties
"""""""""""""""""""""""""""

Actors have a large number of properties that report something about their
position in the game and can be set to move them around. Internally, all of
these return information from the same source, so using one over the other is
usually just a question of convenience.

The three most fundamental position properties are ``.pos``, ``.x`` and ``.y``.

* ``.pos`` returns a position tuple like ``(x, y)`` with the position of the
  anchor point of the actor in the game world in pixels.
* ``.x`` returns only the X axis position of the anchor point in the game
  world in pixels.
* ``.y`` does the same only for the Y axis.

Here's an example of the three properties in use::

    ninja = Actor("ninja")
    ninja.pos = (WIDTH / 2, HEIGHT / 2)

    def update():
        if keyboard.left:
            ninja.x = ninja.x - 10
        if keyboard.right:
            ninja.x = ninja.x + 10
        if keyboard.up:
            ninja.y = ninja.y - 10
        if keyboard.down:
            ninja.y = ninja.y + 10

If you want to set the exact position of an actor, using ``.pos`` is a good way
to do so. Here we put the actor in the middle of the game screen. If you handle
player input, it's usually handy to treat both axes of a position separately to
handle movement.

For convenience, there's a number of other position properties you can check
and set:

* ``.topleft``, ``.midtop``, ``.topright``, ``.midleft``, ``.center``,
  ``.midright``, ``.bottomleft``, ``.midbottom``, ``.bottomright`` all return
  position tuples like ``.pos`` does. You can set them to position a certain
  spot on an actor's image exactly where you want to.
* ``.left``, ``.right``, ``.top`` and ``.bottom`` all return single values like
  ``.x`` or ``.y``.

All of these properties can also be set by you and can be easier to use than
calculating where exactly a certain spot on an actor image is yourself::

    blob = Actor.Rectangle(50, 50, "red")
    blob.pos = (WIDTH / 2, HEIGHT / 2)

    def update():
        blob.x = blob.x + 10
        if blob.left > WIDTH:
            blob.right = 0

By checking if the left edge of the actor is larger than ``WIDTH``, we can
easily tell if an actor is completely off the game screen on the right side.
By then setting the ``.right`` property we can position it so it will move onto
the game screen from the left exactly in the next frame.


.. _deep_dive_actors_positioning_methods:

Positioning with methods
""""""""""""""""""""""""


.. _deep_dive_actors_positioning_methods_angle:

Moving actors by their facing
'''''''''''''''''''''''''''''

Instead of changing the value of properties, actors can also be moved by
different methods on them. For most of these, the ``.angle`` property of actors
is relevant. It will be covered in more detail below. For now, it's only
important to know that the angle of an actor basically determines what
direction the actor is "looking in".

The following methods all move an actor based on the direction it is facing
(its ``.angle`` property): ``move_forward(distance)``,
``move_backward(distance)``, ``move_left(distance)`` and
``move_right(distance)``. These directions are in respect to the facing of the
actor, which you can see below for an angle of zero (looking to the right):

.. image:: /_static/actor/move_directions.svg

If an actor is "looking down" instead, then moving forward will move it down,
backward will move it up, left will move it right and right will move it left.
This is because the directions are always treated as if the direction the actor
is facing is the front, so left is left as seen from that perspective and right
works the same way.

The *distance* argument for these four methods is how far the actor should
move in the given direction in pixels. Here's a quick example of how these
methods can be used::

    ship = Actor("spaceship", (WIDTH / 2, HEIGHT / 2))

    def update():
        if keyboard.w:
            ship.move_forward(10)
        if keyboard.s:
            ship.move_backward(10)
        if keyboard.a:
            ship.angle = ship.angle + 5
        if keyboard.d:
            ship.angle = ship.angle - 5
        if keyboard.q:
            ship.move_left(5)
        if keyboard.e:
            ship.move_right(5)

    def draw():
        screen.clear()
        ship.draw()

With this code, we can turn the ship with the *A* and *D* keys left and right
and move it along its facing with *W* forward or backward with *S*. Pressing
*Q* or *E* will instead shift the ship sideways in respect to its facing
slowly.


.. _deep_dive_actors_positioning_methods_target:

Moving towards a set target
'''''''''''''''''''''''''''

The previously explained methods all move actors with their own ``.angle`` in
mind. There are two methods you can use to move them towards some set target as
well: ``move_towards_angle(angle, distance)`` and
``move_towards_point(target, distance)``.

``move_towards_angle(angle, distance)`` will simply move the actor in the
supplied direction no matter where it is facing. ``0`` will move it right,
``45`` diagonally up and right, ``180`` left and so on just like the directions
work for the ``.angle`` property of actors.

This is one way to get smooth diagonal movement for actors that is not further
than movement in one axis. Here's the basic problem: If your actor should move
10 pixels every frame a movement key is held, what happens if a horizontal and
vertical movement key are held at the same time? The actor moves ten pixels
horizontally and 10 pixels vertically. In total, the diagonal movement the
actor made will be more than just 10 pixels. This is a classic problem for
diagonal movement in games.

You can solve this problem by checking whether a diagonal input is held and
then using the ``move_towards_angle()`` method to move the actor exactly ten
pixels in that direction.

``move_towards_point(target, distance)`` instead takes a target point which can
either be a position tuple like ``(x, y)`` or another actor, and move the actor
you called the method on towards that target by the given distance in pixels.

By default, this will stop at the target, so if the target point is 20 pixels
away but you called ``move_towards_point(target, 50)``, the actor won't
overshoot the target. This is done because otherwise using this method in
``update()`` can make actors flicker back and forth over a target point very
quickly.

If you want the actor to possibly go past the target, always just moving the
exact specified distance, you can call the method with an optional keyword
argument: ``move_towards_point(target, distance, overshoot=True)``.

Here's a short example where an actor follows the mouse cursor around if the
left mouse button is held::

    dog = Actor("dog")

    def update():
        if mouse.pressed_left:
            dog.move_towards_point(mouse.pos, 10)

    def draw():
        screen.clear()
        dog.draw()


.. _deep_dive_actors_positioning_methods_velocity:

Moving with velocity
''''''''''''''''''''

A last way you can move actors via methods is the ``move_by_vel()`` method.
What's *vel*? ``.vel`` is a property of actors that can represent their
constant velocity. ``.vel``, ``.vx`` and ``.vy`` work very similarly to
``.pos``, ``.x`` and ``.y``.

``.vel`` is the velocity of the actor in both axes as a tuple like ``(x, y)``.
Here the tuple is not a position but rather how far the actor should move in
each axis every time ``move_by_vel()`` is called. ``.vx`` and ``.vy`` are
single values representing the velocity for each axis separately.

By default, ``.vel`` is ``(0, 0)``, so calling ``move_by_vel()`` does nothing.
If set to some velocity however, calling ``move_by_vel()`` once will move the
actor by their velocity once. This can be useful if you have many similar
actors moving in different directions::

    import random

    robots = []
    for i in range(50):
        robot = Actor.Rectangle(15, 15, "blue", (WIDTH / 2, HEIGHT / 2))
        robot.vx = random.randint(-5, 5)
        robot.vy = random.randint(-5, 5)
        robots.append(robot):

    def update():
        for robot in robots:
            robot.move_by_vel()

    def draw():
        screen.clear()
        for robot in robots:
            robot.draw()

The example above spawns a bunch of rectangles and has all of them move from
the center of the screen outwards in different directions with different
speeds, all just by setting their velocities differently.

You can also call ``move_by_vel(scale=value)`` to multiply the moved distance.
Let's say your game enters slow motion, then everything should move slower. In
this case you could call ``enemy.move_by_vel(scale=0.5)`` to have all the
enemies in the game move half as fast, or similarly
``player.move_by_vel(scale=2.0)`` to move the player much quicker.

It's easy to set velocity when actors should move straight up, down, left or
right. But if they should move at other angles, the problem of diagonal
movement being less than obvious to give uniform speed rears its head again.

To help with this, you can give actors a velocity of a set magnite (i.e. speed)
towards a certain given angle or point in the game world:
``velocity_towards_angle(angle, magnitude)`` and
``velocity_towards_point(target, magnitude)``.

These work similarly to ``move_towards_angle()`` and ``move_towards_point()``,
but instead of directly changing the position of the actor, the methods just
return a tuple suitable for ``.vel``. The velocity will be calculated so that
if it is used for ``.vel``, the actor will move *magnitude* amount of pixels
each time ``move_by_vel()`` is called::

    def on_mouse_down(pos):
        ball = Actor.Ellipse(20, 20, "white")
        ball.pos = player.pos
        ball.vel = ball.velocity_towards_point(pos, 10)

Here we set ``ball.vel`` to the velocity calculated to move it towards the
position of the mouse click with ten pixels of speed per call of
``move_by_vel()``.


.. _deep_dive_actors_positioning_methods_velocity_intercept:

Intercept velocity
''''''''''''''''''

This section discusses a very specific but useful method actors have. Let's
say you want a game object in your game to go from one point to another actor
but that other actor is moving. How do you know how to move the actor so it
will reach it's target?

The maths involved in something like that are quite complex so PGTurbo can do
it for you. This however only works if the actor that you want to find out how
to get to for has a ``.vel`` set and is using ``move_by_vel()`` each frame.

Basically, for this to work the target actor has to move along a straight line
at a constant speed. That is usually easiest to achieve with velocity, so
that's why those conditions are there.

Once this is done, you can call ``intercept_velocity(target, speed)`` to
calculate a velocity with which the actor you used the method on could reach
the target actor.

The first argument *target* is the other actor that this one should move to
with the calculated velocity. It needs to have a ``.vel`` set and use it each
frame with ``move_by_vel()``.

The second argument *speed* is the distance in pixels the actor you are using
the method on should move each frame with the calculated velocity.

Using the method will return a tuple suitable for ``.vel`` if there is a
possible interception or ``None`` if not. The reason there might not be a
solution is simple. Imagine actor A is moving straight away from actor B and
actor B uses ``intercept_velocity()``, but with a lower *speed* given than
actor A has. No matter how actor B tries to move, it will never catch up to
actor A.

Generally, the higher the speed of the intercepting actor (the *speed* value
given to ``.intercept_velocity()``) in comparison to the actor that should be
intercepted, the less likely it is that there will be no valid solution.

That was all quite theoretical, here's an example you can copy to a file and
try out yourself::

    WIDTH = 400
    HEIGHT = 400

    thrower = Actor.Rectangle(40, 40, "blue", (WIDTH / 2, HEIGHT / 2))
    catcher = Actor.Rectangle(40, 40, "red", (40, 40))
    ball = Actor.Ellipse(20, 20, "white", (WIDTH / 2, HEIGHT / 2))

    def on_mouse_down(pos):
        ball.pos = thrower.pos
        ball.vel = ball.velocity_towards_point(pos, 5)
        catcher.pos = (40, 40)
        possible_vel = catcher.intercept_velocity(ball, 10)
        if possible_vel:
            catcher.vel = possible_vel
        else:
            catcher.vel = (0, 0)

    def update():
        catcher.move_by_vel()
        ball.move_by_vel()

        if catcher.colliderect(ball):
            ball.vel = (0, 0)
            catcher.vel = (0, 0)

    def draw():
        screen.fill("darkgreen")
        thrower.draw()
        catcher.draw()
        ball.draw()

What happens here?

#. We have three actors: ``thrower`` sitting in the middle, ``catcher`` always
   starting in the top left corner and ``ball`` getting thrown.
#. When a mouse button is clicked, we teleport the ball back to the center and
   set its velocity to move towards the point that was clicked.
#. After this, we let ``catcher`` calculate an intercept velocity to towards
   the ``ball``. We don't directly set ``.vel`` to this, because it's usually
   possible for there to be no possible solution. So before setting ``.vel`` we
   check that we actually got a valid velocity before setting it for
   ``catcher``. If there was no solution, we zero the velocity of ``catcher``.

   (With the speeds we picked for ball and catcher, there should always be a
   solution for this code, but it's good to always follow safe coding
   practises anyways.)
#. The rest is simpler, we always move ``catcher`` and ``ball`` by their
   velocity, stop them if the ball is caught up with and draw everything to the
   screen.


.. _deep_dive_actors_positioning_limits:

Movement limits
"""""""""""""""

While everything so far has been about making actors move, this section is
about stopping them from moving. For example, you might want to restrict the
player character in your game to the game window, so it can't go outside of the
visible area.

To do so, you can set movement limits on actors. Whenever an actor would exceed
those limits by moving, it instead stops at the set limit. The following
properties can be used to set and check limits: ``.x_limits``, ``.y_limits``,
``.left_limit``, ``.right_limit``, ``.top_limit`` and ``.bottom_limit``.

``.x_limits`` and ``.y_limits`` set left and right or top and bottom limits
respectively via a tuple, for example ``ninja.x_limits = (15, WIDTH - 15)``.
This would prevent the ``ninja`` actor from moving its left edge under the X
position of ``15`` and its right edge over the X position 15 pixels from the
right game window edge. ``.y_limits`` can be set the same way.

Where the former two properties set two limits at the same time, they can also
be set individually: ``jumper.bottom_limit = HEIGHT - 20``. In this case, the
``jumper`` actor could go as high as it wants to, but its bottom edge can never
go under 20 pixels from the bottom game window edge.

To remove limits, simply set them to ``None``. To free the ninja to move even
off-screen, we could do it like so::

    ninja.x_limits = (None, None)
    ninja.y_limits = (None, None)


.. _deep_dive_actors_angle_scale_flip_opacity:

Angle, scale, flip, opacity and tint
------------------------------------


.. _deep_dive_actors_angle:

Angle / Rotation
""""""""""""""""

As mentioned before in the section on moving actors with methods, actors have
a ``.angle`` property which determines where the actor is facing / "looking
at". Phrased a different way, the angle is the rotation of the actor image.

``.angle`` is counted in degrees, counterclockwise, starting from ``0`` when
looking straight right. If that was a confusing sentence, the image below
should illustrate it.

.. image:: /_static/actor/rotation.svg

Because ``0`` rotation is looking to the right, you should set up your game's
images so that the facing of any sprites where rotation is relevant should also
be to the right.

The center of rotation is the anchor point of an actor. In the image above, the
anchor point is centered, but if it was at one end of the ship, the image would
have been turned around that point instead.

Since it is a normal property, you can rotate an actor by setting its
``.angle`` just like you can move actors by setting those properties too::

    asteroid = Actor.Ellipse(50, 50, "brown", (300, 300))

    def update():
        asteroid.angle = asteroid.angle + 3

    def draw():
        screen.fill("white")
        asteroid.draw()

As mentioned before, rotation works counterclockwise, so *increasing* the value
of ``.angle`` will make an actor turn around its left side (when seeing the
current angle as the front). Decreasing the value will turn around its right
side instead::

    asteroid.angle = asteroid.angle - 3

The value of ``.angle`` is always kept between ``0`` and ``359`` degrees
automatically. This means if you start at an angle of ``0`` and then do
``asteroid.angle = asteroid.angle - 90``, the value will end up not at ``-90``
but at ``270`` instead. This is done so that any heading always has an exact
``.angle`` value to match it and you don't have to worry about where values
could grow or shrink to if you keep turning an actor in the same direction.

If you want to make your actors "look at" something, then you can set their
``.angle`` to the angle to that thing from the actor::

    ship = Actor("spaceship")

    def on_mouse_move(pos):
        ship.angle = ship.angle_to(pos)

The method ``Actor.angle_to(target)`` will return the angle from the actor to
the target, which can either be a position tuple or another actor. In the
example above, the ship will always turn to face the position of the mouse.


.. _deep_dive_actors_bounding_width_and_height:

Bounding width and height
'''''''''''''''''''''''''

When an image is rotated, its dimensions have to change internally, because
images are always rectangles. But if you rotate a rectangle, it will suddenly
peek out over the edges of its former borders. To account for this, games often
contain rotated images in larger rectangles to represent them. The image below
illustrates this:

.. image:: /_static/actor/dimensions_vs_bounding_dimensions.png

When you change the ``.angle`` of an actor, there are then two possible widths
or heights that could be meant when you ask "How wide is the image?". The
``.width`` and ``.height`` stay the same and represent the base image size of
the actor itself. ``.bounding_width`` and ``.bounding_height`` track how large
a rectangle containing all of an actor with its rotation is.


.. _deep_dive_actors_scale:

Scale
"""""

By default, actors will appear in your game world at the size of their image
file. If an actor image is 66x92 pixels, then the actor in the game window will
span 66 and 92 pixels in each axis respectively. You might want actors to
appear at different sizes however, which is why you can *scale* them.

Actors have a number of properties that control their scaling. Easiest is to
give them a single scale factor to resize them::

    ninja = Actor("ninja", (100, 80))
    big_ninja = Actor("ninja", (160, 80))
    big_ninja.scale = 2.0

Even though both actors were created from the same image, setting
``.scale = 2.0`` will make the second one look twice as large as the first.
Scaling always happens around the anchor point of an actor, so in this case
the ``big_ninja`` image grew around its center (because that is the default
anchor point).

Setting ``.scale`` to a single value like ``2.0`` or ``0.1`` will change the
size of both dimensions, but you can also scale the X and Y dimensions of an
actor individually::

    ninja = Actor("ninja", (WIDTH / 2, HEIGHT / 2))

    def update():
        if keyboard.up:
            ninja.scale_y = ninja.scale_y + 0.1
        if keyboard.down and ninja.scale_y > 0.1:
            ninja.scale_y = ninja.scale_y - 0.1
        if keyboard.right:
            ninja.scale_x = ninja.scale_x + 0.1
        if keyboard.left and ninja.scale_x > 0.1:
            ninja.scale_x = ninja.scale_x - 0.1

With this code, you can freely stretch an actor in both directions. Note that
we put a second condition on *reducing* the scale. This is because an actor
cannot have a negative scale, so we need to prevent trying to set any of the
relevant properties to a value under ``0.0``.

If you want to use a certain proportion, you can also set both scaling
dimensions like this: ``.scale = (2.0, 0.75)``. The first value in the tuple is
the scaling factor for the X axis and the second the factor for the Y axis.

When you check the value of ``.scale``, you always get a tuple like this back
since it's not possible to represent all scaling options with a single number.
If you are sure you always scale actors uniformly in your game, you can get the
scaling factor safely either just from one dimension like ``.scale_x`` or with
``.scale[0]`` to get one of the values in the tuple returned by ``.scale``.


.. _deep_dive_actors_width_and_height:

Width and height
''''''''''''''''

As mentioned before, actors have different dimensions when rotated. You can
check how large the bounding box of an actor is, but you can do more than just
get the value of the image width and height.

You can directly set ``.width`` and / or ``.height`` to pixel values to change
the dimensions of actors to match those. We can rewrite the example above like
this::

    ninja = Actor("ninja", (WIDTH / 2, HEIGHT / 2))

    def update():
        if keyboard.up:
            ninja.height = ninja.height + 4
        if keyboard.down and ninja.height > 4:
            ninja.height = ninja.height - 4
        if keyboard.right:
            ninja.width = ninja.width + 4
        if keyboard.left and ninja.width > 4:
            ninja.width = ninja.width - 4

Just like before, neither ``.width`` nor ``.height`` can be negative, so we
have to check for that to avoid crashing the game when we try to set them to
invalid values.

Relative scale via ``.scale``, ``.scale_x`` and ``.scale_y`` as well as
absolute size via ``.width`` and ``.height`` always keep each other
synchronized. Changing ``.scale`` will change ``.width`` in the background and
the other way around to keep everything up to date.

``.bounding_width`` and ``.bounding_height`` cannot be set by you since they
are just a reflection of what rectangle size would be necessary to contain a
rotated actor.


.. _deep_dive_actors_flipping:

Flipping
""""""""

In some game frameworks, you can flip the image of something by setting its
scale to the negative value of the same magnitude. We just covered that that's
not possible in PGTurbo, so how do you flip actor images?

It's simple, there are ``.flip_x`` and ``.flip_y`` properties which take
boolean values (``True`` or ``False``). To flip an actor horizontally, just do
``actor.flip_x = True``. If you want to change the value to its opposite, no
matter what it is right now, you can use ``actor.flip_x = not actor.flip_x``.
(The ``not`` keyword inverts a boolean truth value.)

Flipping the actor image like this does not move an actor image however. No
matter where the anchor point is, flipping with ``.flip_x`` and ``.flip_y``
will only ever change how the image looks, not where it is drawn.

Sometimes we might want the image to move however. Imagine a platforming game
where the anchor point of the player character is ``("center", "bottom")`` and
now we would like to make it so the character can "hang" from the ceiling.
Ideally, we want to flip the actor image vertically and we also want the anchor
point to move so that it will be where the feet of the character are in the
image again.

To make this possible, actors have two methods: ``Actor.flip_x_over_anchor()``
and ``Actor.flip_y_over_anchor()``. Calling these methods will change the flip
property to whatever value it is currently not and also adjust the anchor point
to shift where it was previously in relation to the image.

The image below illustrates the difference:

.. image:: /_static/actor/flip_vs_flip_over_anchor.png


.. _deep_dive_actors_opacity:

Opacity / Transparency
""""""""""""""""""""""

In some cases it is useful to make an Actor object partially transparent. This
can be used to fade it in or out, or to indicate that it is disabled /
deactivated.

The ``.opacity`` attribute of an Actor controls how transparent or opaque it
is.

* When an actor is not at all transparent, we say it is "opaque" and it has
  ``.opacity`` of ``1.0``, and you can't see through it at all.
* When an actor is completely transparent, it has an ``.opacity`` of ``0.0``.
  This will make it completely invisible.

To make an actor that is half-transparent (like a ghost), you could write
this::

    ghost = Actor('ghost')
    ghost.opacity = 0.5

The following diagram shows how a solid red actor might look at different
levels of ``.opacity`` from ``0.0`` to ``1.0``. The checkerboard pattern behind
the color strip is there to make it easier to tell how much red color is there.
In an actual PGTurbo game, transparency is truly transparent.

.. image:: /_static/actor/opacity.svg

One thing to note is that the order of drawing semi-transparent actors matters
for how they look. A ghost seen through a window looks slightly different from
a window seen through a ghost.


.. _deep_dive_actors_tint:

Tint
""""

Many games feature effects that change the color and brightness of game
objects. Think of a red flash when the player is getting hit or interactable
game objects being highlighted when you hover over them with the mouse.

Such simple color and highlight effects can be achieved with the
``.tint_color`` and ``.tint_value`` properties of actors. ``.tint_color`` is a
solid color used for the tinting of the actor image. ``.tint_value`` is whether
tinting should make the image brighter or darker and how strong the effect
should be.

``.tint_color`` can be any valid color either as a string name or color tuple
and defaults to ``"darkgray"``. This is because a medium gray allows both
brightening and darkening of the actor image just with ``.tint_value``.

``.tint_value`` is a number between ``-1.0`` and ``1.0`` and defaults to
``0.0``. Zero means there is no tinting, no visual effect. Positive numbers
will increasingly tint the actor image while making it brighter. Negative
values will tint the image more and more while making it darker.

Here's how that looks at different points for ``.tint_value`` at the default
color:

.. image:: /_static/actor/tint_darkgray.png

With a gray between black or white, the color balance of the actor image stays
the same and it just gets brighter or darker. Now let's look at the same
examples with a ``.tint_color`` of ``"blue"``:

.. image:: /_static/actor/tint_blue.png

As you can see, now everything is made bluish, but the overall look is also
darker. That is because blue as a solid color of only one channel is not very
bright to begin with. The brighter the ``.tint_color``, the brighter results
will be and the same is true for the opposite as well.

Here we can see an extreme example when using fully saturated ``"yellow"`` as
the ``.tint_color``:

.. image:: /_static/actor/tint_yellow.png

Because the color is already very bright, the brightening effect is strong
while trying to darken the actor with such a bright color barely works. And
here is the same again when using a darker yellow (half the values of the last
one): ``(128, 128, 0)``.

.. image:: /_static/actor/tint_yellow_dark.png

Because the base color is darker, now we can also achieve far more darkening
through negative values for ``.tint_value``.

As as example for how these might be used in a game, let's circle back to the
example from before and the player being hit::

    player = Actor("ninja")
    # ... More setup here ...

    def untint_player():
        player.tint_value = 0.0

    def player_hit():
        # ... Reduce health etc. ...
        player.tint_color = "red"
        player.tint_value = -0.5
        clock.schedule(untint_player, 0.15)

In the code above, when the ``player_hit()`` function is called (maybe when an
enemy collides with the player), its tint color will be made red and the value
set to ``-0.5`` meaning it will be a darker red look. The ``clock`` is then
used to schedule when the effect should end with the ``untint_player()``
function.

The result will be that whenever the player is hit, its actor image will be
reddened for around a sixth of a second before returning to normal.


.. _deep_dive_actors_handy_methods:

Handy methods on actors
-----------------------

Beside the other methods actors have that usually have a very specific purpose
like moving them around or calculating velocities, there are three generally
useful methods all actors have: ``Actor.distance_to(target)``,
``Actor.angle_to(target)`` and ``Actor.is_onscreen()``.

* ``Actor.distance_to(target)`` returns the distance in pixels from the actor
  you call this method on to the target. The target can be either a position
  tuple like ``(x, y)`` or another actor.
* ``Actor.angle_to(target)`` returns the angle from the actor you call this
  method on to the target. Here as well, a position tuple or an actor is
  possible.

  As always, an angle of ``0`` is straight right, ``90`` is up, ``180`` is left
  and ``270`` is down.

  (We've already seen this method in action before to make an actor track its
  facing to the mouse position.)
* ``Actor.is_onscreen()`` returns ``True`` if any part of the actor's image is
  within the visible game window. If not a single pixel of the actor is inside
  the screen bounds, it returns ``False`` instead.

  You can call ``.is_onscreen(20)`` to let any actor that is within twenty
  pixels of the screen bounds still count as onscreen. This is useful if you
  create actors just outside the visible area but they shouldn't count as
  having left the play area yet.

  It's also possible to give different margins for the horizontal and vertical
  bounds of the game window like ``.is_onscreen(20, 10)``. This would leave a
  twenty pixel horizontal margin and a ten pixel vertical margin.

``Actor.is_onscreen()`` is very useful to clean up actors that have left the
playing area. Imagine a game where the player character has to dodge cars while
crossing a road. If you always create new car actors to make drive across the
screen, at some point there will be dozens or hundreds of actors that aren't
visible anymore still doing calculations and checking for collisions driving
off into infinity.

By making them check ``car.is_onscreen()`` you can clean them up when they
left the visible area of play. Since saving a bunch of similar actors in a
list is usually a good idea, removing them from the game can be as easy as
removing them from that list.

:download:`This example script </_downloads/cars_is_onscreen.py>` shows how you
can continuously create actors and discard them after they have left the
screen.


.. _deep_dive_actors_collision_checks:

Collision checks
----------------

Checking whether game objects run into each other is a fundamental requirement
of most games. Is the player character getting hit? Is it hitting something
else that should react? Did you move it to the target zone to get to the next
level? All of these have to do with collision checks.

Since actors are game objects in PGTurbo, they have three methods for collision
checking: ``Actor.colliderect(target)``, ``Actor.collidepoint(target)`` and
``Actor.collidemask(target)``.

``Actor.colliderect()`` takes another actor or a ``Rect`` object as an argument
and returns whether the actor's rectangle bounds overlap those of the target.
The rectangle of an actor is NOT the exact pixels of its image. Below is an
illustration of the different results when using it:

.. image:: /_static/actor/colliderect.png

``Actor.collidepoint()`` takes a position tuple like ``(120, 80)`` as an
argument and checks whether the rectangle bounds of the actor cover that point.
Here as well there is an illustration below:

.. image:: /_static/actor/collidepoint.png

``Actor.collidemask()`` takes either another actor OR a position tuple as an
argument and returns results like the other two methods. Either whether the
actor images overlap or if the actor image covers the point in the game world.
The difference is that ``.collidemask()`` does a pixel perfect check, meaning
it is far more precise than the other methods. Below are same same types of
examples as before, but this time with pixel precision:

.. image:: /_static/actor/collidemask_rect.png

.. image:: /_static/actor/collidemask_point.png

The downside to this perfect precision is that the performance hit of mask
based collision detection is far higher than that of the other two methods.

If coarse collision detection is good enough, ALWAYS use ``.colliderect()`` or
``.collidepoint()``. Only if you need very precise checks should you use
``.collidemask()`` and then only as little as you need to.

In your code, you'll usually use these methods in ``if`` conditionals, since
they return truth values. In the example below, items disappear once the
player character touches them::

    player = Actor.Triangle(80, 40, "yellow", (WIDTH / 2, HEIGHT / 2))
    player.angle = 90

    orbs = []
    for i in range(8):    
        orb = Actor.Ellipse(30, 30, "blue", (100 + 40 * i, 100))
        orbs.append(orb)

    def update():
        if mouse.pressed_left:
            player.move_towards_point(mouse.pos, 8)

        i = 0
        while i < len(orbs):
            orb = orbs[i]
            if orb.colliderect(player):
                orbs.pop(i)
            else:
                i = i + 1

    def draw():
        screen.clear()
        player.draw()
        for orb in orbs:
            orb.draw()

You can download the code above by clicking
:download:`here </_downloads/orb_collisions.py>`.

If you run this code, note how the blue orbs disappear before actually touching
the visual yellow triangle. This is because a rough collision check is used.
Try switching ``.colliderect()`` for ``.collidemask()`` and see the difference.


.. _deep_dive_actors_data:

Tracking custom values with .data
---------------------------------

Actors have many properties useful for manipulating where they are or how they
look, but how can you track your own game's special values for game mechanics?

In a platformer, maybe your player character is collecting coins. In an
adventure game, maybe enemies need to track their health points. To allow you
to save, check and manipulate anything like this on actors, they have the
``.data`` property.

``.data`` is a dictionary you can fill with whatever you want. For the
platformer example above, maybe you use it like this::

    player = Actor("ben")
    player.data["coins"] = 0

    def update():
        # ... Player movement here ...
        for coin in coins:
            if coin.colliderect(player):
                # ... Removing the coin here ...
                player.data["coins"] = player.data["coins"] + 1

For the adventure game, something like this::

    def update():
        # ... Game mechanics here ...
        for mushroom in mushrooms:
            if mushroom.colliderect(player_sword):
                mushroom.data["health"] = mushroom.data["health"] - 5

                if mushroom.data["health"] <= 0:
                    # ... Remove the mushroom here ...

Since it's a dictionary, you can store as much as you want in ``.data``, all
with their own name and value. The only thing you have to look out for is that
if you have actors of different types, they might not all have the same values
in their ``.data`` property.

In the platformer, only the player character has ``.data["coins"]``, so if you
try to check ``Actor.data["coins"]`` on any other actor, it will crash the game
because there is no such value in their data dictionaries.

If you aren't sure what actor might end up with what values in the dictionary,
you can check if they have a certain one before trying to manipulate it like
this::

    if "coins" in actor.data:
        # ... Do something with coins here ...

Checking ``in`` for any string and the ``.data`` property of an actor will
return ``True`` only if the dictionary holds a value for that name. Otherwise,
it will return ``False``, allowing you to avoid errors.

If you want to reset an actor's data dictionary to be completely empty again,
you can do so with ``actor.data.clear()``. Note this doesn't reset values to
their original value but completely empties the dictionary so there will be no
values tracked with it anymore.


.. _deep_dive_actors_ready_timers:

Actor ready timers
------------------

If you don't know what ready timers are, read
:ref:`this section of the clock deep dive <deep_dive_clock_ready_timers>` to
get all the details. In broad, the ready timer system allows you to track
cooldowns for different things happening in your game. There is a global one
in the ``clock`` builtin, but each actor also has their own individual ready
timer system.

This allows you to track the same kind of ready timer many times without having
to call each something different. Image there are many monkeys in your game and
they can all jump with a cooldown managed by a ready timer. You could track all
of those with ``clock`` but then each would need its own name and checking them
all would require manually writing each check or somehow constructing the name
of each correct ready timer from the monkey actor.

Neither sounds ideal. It's much simpler to just give each monkey its own
``"jump"`` ready timer::

    for monkey in monkeys:
        monkey.track_ready("jump", 2.0)

Now they can jump at different times and all individually track when the next
jump is ready.

Actors all have exactly the same methods for ready timers that ``clock`` also
has, requiring all the same arguments and having all the same conditions.


.. _deep_dive_actors_animation:

Actor animation
---------------

Most games don't use static images for characters but rather have lots of
animations that play whenever characters walk around, jump or just stand
around. Just like a video is a series of still images being played quickly,
animations are made by just quickly cycling the display image of an actor
through many frames in an animation. Actors in PGTurbo have a robust sprite
animation system that is easy to start using put powerful if you dive into it.

Everything to do with animations for actors is accessed via their ``.anim``
property. So calling animation related methods works like ``Actor.anim.add()``
instead of calling a method directly on the actor itself.

Before an actor can be animated, the animations they are supposed to use have
to be loaded, much like their image has to be set to create them.


.. _deep_dive_actors_animation_loading:

Loading animations
""""""""""""""""""

There are two different ways to load an animation. For both of these, the
relevant files must be placed in the *animations*
:ref:`resource directory <deep_dive_resources_and_storage>`.


.. _deep_dive_actors_animation_loading_folders:

Loading animations from folders
'''''''''''''''''''''''''''''''

The first way to organize your animations for a game is in separate folders
inside the *animations* resource folder.

Each animation is a single folder inside the *animations* folder. The
name of that folder will be the name under which PGTurbo finds the animation.
The individual frames of an animation are placed inside that folder as separate
images.

The alphabetical filename order will determine the order of animation frames
when loading it. This means it's easiest to organize if all the frames are
called the same except for a number running up indicating each frame either at
the start or end of the filenames. Here's an example:

.. code-block:: none

    .
    ├── animations/
    │   ├── walk_down/
    │   │   ├── walk_down_1.png
    │   │   ├── walk_down_2.png
    │   │   ├── walk_down_3.png
    │   │   └── walk_down_4.png
    │   └── idle/
    │       ├── idle_1.png
    │       └── idle_2.png
    └── main.py

With this structure, PGTurbo will be able to find and load two animations:
``walk_down`` and ``idle``. To do so, simply create an actor and load the
animations into its ``anim`` component::

    ninja = Actor("ninja", (150, 200), anchor=("center", "bottom"))
    ninja.anim.add("walk_down", 1.5)
    ninja.anim.add("idle", 1.0)

``Actor.anim.add()`` loads an animation to use with the actor. The string is
the name of the animation to load from the *animations* resource folder while
the number is over how many seconds the animation should play. In the example
above, playing the ``"walk_down"`` animation once will take 1.5 seconds where
``"idle"`` will play out in one second.

*Note:* Any non-image or non-supported image files as well as other directories
inside an animation folder are ignored by PGTurbo.


.. _deep_dive_actors_animation_loading_spritesheet:

Loading from a spritesheet
''''''''''''''''''''''''''

Instead of placing individual frames in a folder with that folder representing
one full animation, you can also load an entire animation from a spritesheet.

A spritesheet is a single image file that holds all the frame images for an
entire animation. In general, a spritesheet can even hold frames of many
different animations, but PGTurbo only supports spritesheets with a single
animation on them. Here's an example of how such a spritesheet file can look
like with the individual frames highlighted:

.. image:: /_static/actor/walk_down_frames.png

In a spritesheet, the image file is cut up into multiple chunks of the same
size and each of these chunks is one animation frame. In the example above, the
walking animation has four frames.

Spritesheet image files are directly placed in the *animations* resource folder
and their filename is their animation name, just like a filename is the image
name for files in the *images* folder.

If you were to put the same animations as before in spritesheets instead of
folders, the file structure in *animations* could look like this:

.. code-block:: none

    .
    ├── animations/
    │   ├── walk_down.png
    │   └── idle.png
    └── main.py

Loading an animation from a spritesheet is just a little more complicated than
loading it from a folder. When we do so, we have to tell PGTurbo what size to
make the chunks that will become individual animation frames::

    ninja = Actor("alien", (150, 200), anchor=("center", "bottom"))
    ninja.anim.add_spritesheet("walk_down", 64, 64, 1.5)

As you can see, this time we use ``.add_spritesheet()`` instead of ``.add()``
and there is not just the animation name ``"walk_down"`` that has to be
provided, but two more numbers before the seconds argument which is still
``1.5``. These two numbers are how wide and how tall each animation frame is in
the spritesheet file.

To load a spritesheet and have the animation look correct afterwards, it's very
important that you know how large each individual animation frame is in the
spritesheet image.

PGTurbo can load spritesheets either with their frames arranged horizontally
from left to right or vertically from top to bottom. If a spritesheet contains
its frames vertically, you need to pass the ``vertical=True`` keyword argument
when using ``Actor.anim.add_spritesheet()``::

    ninja = Actor("alien", (150, 200), anchor=("center", "bottom"))
    ninja.anim.add_spritesheet("walk_down", 64, 64, 1.5, vertical=True)


.. _deep_dive_actors_animation_loading_options:

Setting options when loading
''''''''''''''''''''''''''''

When you load an animation, you can set many different options for how it
should behave when you use it. Except for the animation name (when using
``.add()``) and cell width and height (when using ``.add_spritesheet()``), all
of them are optional and have sensible defaults.

To set them, either provide them all in the order listed below or otherwise
set them as keyword arguments like ``.add("name", offsets=..., callback=...)``.

**durations**

This option controls how long the animation runs for and how long each
individual frame of the animation is shown. If given a single value like
``1.5``, then animation will play out over that time and each frame will be
shown equally.

As an example, the ``"walk_down"`` animation from above with ``1.5`` as the
duration would show each of its four individual frames for 0.375 seconds.

Instead of giving a single value, `durations` can also be given a tuple with
one value per frame of the animation to set each frame to show for an exact
amount of time.

With the same example, giving ``(0.25, 0.5, 0.5, 0.25)`` would result in the
second and third frame of that animation being shown for half a second each
where the first and fourth would appear only for a quarter second.

If no duration is specified, a duration of ``1.0`` is used and distributed
equally among the frames.


**offsets**

When loading from folders, animation frames can have different sizes from each
other. If using a spritesheet, some animations might still have frames that are
a different size to the size of the base image of the actor. To make sure that
the images are still properly aligned when playing back, offsets can be
specified.

Each offset defines how the animation frame image should be moved in relation
to the actor base image top left corner to align it properly. Let's say frog
jumping animation has frames that are all 32 pixels taller than its base image.
In this case, we might have to shift them up by that amount in relation to
the base image top left corner to align them properly.

To do so, we can give an offset of ``(0, -32)``. A single offset is always a
tuple of two numbers, one for how the frame should be moved in the X axis and
one for how it should move in the Y axis. To shift a frame 32 pixels up,
``-32`` in the Y axis is needed.

If only one offset value is given, that offset is applied to all frames of the
animation. To set individual offsets for frames, a uple of offsets can be
supplied just like for `durations` a tuple of numbers could be given. In this
case, each animation frame gets the offset from the tuple at its position in
the order.

By default, no offsets are used.


**sound**

This is simpler option. If a ``sounds`` sound object is provided, that sound
will be played when the animation starts running. It's important that this is
an actual sound object, not the name of the sound.

Correct: ``actor.anim.add("jump", 1.0, sound=sounds.poof)``

Wrong: ``actor.anim.add("jump", 1.0, sound="poof")``

By default, no sound is set to play.


**callback**

If a function name is provided, that function will be called once the animation
has finished playing. The function must not take any arguments, otherwise the
game will crash when trying to call it. It's important that this is the name
of a function without the parentheses, not a call of that same function.

Correct: ``actor.anim.add("jump", 1.0, callback=create_splash)``

Wrong: ``actor.anim.add("jump", 1.0, callback=create_splash())``

By default, no function call is made.


**new_base**

The string name of a loaded animation to make the new base animation once
this animation has finished playing. A value of ``None`` will remove the base
animation once this one has finished playing. Base animations are covered in
more detail below.

By default, the base animation won't be changed.


.. _deep_dive_actors_animation_play:

Playing animations
""""""""""""""""""

Once your animations are loaded in, it's simple to play them::

    def update():
        if keyboard.down:
            ninja.y = ninja.y + 8
            ninja.anim.play("walk_down")
        else:
            ninja.anim.play("idle")

That's it! The ``actor.anim.play(name)`` function will start to play the
animation you tell it to with the given animation name. If that animation is
already running, it won't do anything. This is perfect for animations that
should run and repeat while the player is holding down a button for example.

``actor.anim.start(name)`` works a bit differently. This method will always
start playing the given animation from the beginning, even if it was already
running.

In general, ``anim.play()`` is probably the right choice if it's an animation
that should repeat as long as some input is held or some condition is met.
``anim.start()`` is better when a single input or action should trigger an
animation to run from start, no matter what happened before.


Option overrides
''''''''''''''''

When you play an animation either with ``anim.play()`` or ``anim.start()``,
the first argument must be the name of the animation to run. Optionally, you
can also give up to three further arguments to override the usual options
set for the animation: ``sound``, ``callback`` and ``new_base``.

If an animation has anything set for these options, the appropriate actions
are triggered either when the animation starts or finishes. But if you call
``anim.play()`` or ``anim.start()`` with any of these options set as keyword
arguments, their value will override the standard one::

    ninja.anim.add("jump", sound=sounds.poof)

    def on_key_down(key):
        if key == keys.SPACE:
            ninja.anim.start("jump", sound=sounds.wind)

In the example above, even though the ``"jump"`` animation should normally
play the ``sounds.poof`` sound when it starts, by overriding the option in
``anim.start()``, it will instead play ``sounds.wind`` just for this once.

If we call ``ninja.anim.start("jump")`` later again, it will play with
``sounds.poof``, because that is the normal option and wasn't overriden with
the call.

The other two options work the same and can also be combined::

    ninja.anim.add("jump", sound=sounds.poof, callback=create_splash)

    def update():
        ninja.anim.play("jump", callback=create_boom, new_base="idle")

Here, we override two options at once, one of which supercedes a set option
(``callback``) and the other which is used where normally no option is set
for ``new_base``. Since there was no override for the ``sound`` option,
``sounds.poof`` was played as normal.


Pausing / Stopping animations
"""""""""""""""""""""""""""""

We know how to run animations now, but what if they should stop? The animation
system has four methods allowing you to control whether it is running or not:
``anim.pause()``, ``anim.unpause()``, ``anim.stop()`` and ``anim.stop_all()``.

``anim.pause()`` interrupts the currently running animation and freezes the
display image of the actor at the last gotten animation frame. This is a
temporary state and all of the current options and overrides associated with
the previous animation are preserved. If the animation system is already
paused, this does nothing further.

``anim.unpause()`` returns the animation system from a paused state to resume
running what was interrupted, including all option overrides and settings. If
the animation system was already running, this does nothing further.

Starting any animation while the animation system is paused also unpauses it
but discards the previous state and simply runs whatever was called.

``anim.stop()`` interrupts the current animation but does not pause all
animation and doesn't record a paused state. Instead, the previous animation is
just reset and the animation system returns to playing the base animation if
one is present. If not, the actor returns to its base image display.

``anim.stop_all()`` also interrupts the current animation and resets it without
a pause state, but it also sets the base animation to ``None`` so even if one
was set, the actor returns to its base image display.


The base animation
""""""""""""""""""

The base animation was already mentioned multiple times, but what is it? By
calling ``anim.set_base(name)``, you can specify a loaded animation that should
always run whenever no other animations are playing.

If your game is animated, usually even if an actor is standing still, there
should be some movement visible since few things except for background images
are ever truly static.

As such, it's very widespread to have an ``"idle"`` animation that is just the
character making slight movements while standing around for example::

    ninja.anim.add("idle", 2.0)
    ninja.set_base("idle")

    def update():
        if keyboard.up:
            ninja.y = ninja.y - 8
            ninja.anim.play("walk_up")
        # ... Other movement directions here ...

In the example above, even if we never explicitely call
``ninja.anim.play("idle")``, whenever the ninja is not moving and the last
walking animation cycle has played out, the ninja will return to playing its
``"idle"`` animation.

Calling ``anim.set_base(None)`` will remove a previously set base animation.


Animation queues
""""""""""""""""

While playing single animations is very handy, larger games often require
playing animations back to back in set orders. For example, the ninja might
be able to jump and slash in one move or jump and kick in another.

One option would be to put each variation in its own animation and simply use
them all as single tracks. But what if you need to change the jump animation
slightly? Then you would have to go into each animation that uses the jump
frames as well and adjust everything.

Instead, it's far more common to be able to combine multiple animations to run
in sequence. In PGTurbo, this is made possible with animation queues. Queues
are made up of already loaded single animations put into a certain order::

    ninja.add_queue("tornado_kick", ("jump", "kick", "roll"),
                    callback=create_splash)

Queues can also take ``sound``, ``callback`` and ``new_base`` options like
single animations. In addition to those, they also have the ``suppress``
option however, which defaults to ``False``. If set as ``suppress=True``, then
none of the ``sound``, ``callback`` and ``new_base`` options of the individual
animations in the queue will trigger when the queue is played.

Normally, when an animation plays as part of a queue, it will play its own
sound, trigger a callback function being called and change the base animation
if set up to do so. But if the queue has ``suppress=True`` set, then none of
these will be done. Instead, only those options of the queue itself will be
triggered.

If ``suppress`` is ``False`` (the default), then both the options of individual
animations that are part of the queue and those of the queue itself will
trigger.

Once a queue has been added, basically the same methods as for single
animations are available to run them, just always with ``_queue`` at the end::

    ninja.play_queue("tornado_kick", sound=sounds.wind)
    ninja.start_queue("tornado_kick")

Override options also work the same, just for queues, the ``suppress`` option
can also be overridden for single runs of the queue. In addition to those
option overrides, queues can also be started from any of their animations::

    ninja.play_queue("tornado_kick", position=1)

This will play the queue not from the first animation of its order but the
second. Passing ``2`` will play from the third and so on. In general, the
``position=number`` override will start playing a queue from any position in
its order as provided, starting with ``0`` as the first position.


Editing animation and queue options
'''''''''''''''''''''''''''''''''''

Once created, you can also change options for single animations or queues with
``anim.edit(name, option=value, ...)`` and
``anim.edit_queue(name, option=value, ...)``. In both cases, the first argument
is the name of the animation or queue that should have an option changed,
followed by any of the option name and the new value as a keyword argument
pair. Multiple options can be changed with the same call if they are just given
as multiple keyword argument pairs.

The list of options that can be changed on the fly is this:

* For single animations: ``durations``, ``offsets``, ``sound``, ``callback``,
  ``new_base``.
* For animation queues: ``animation_names``, ``sound``, ``callback``,
  ``new_base``, ``suppress``.

    * ``animation_names`` in this case is the tuple of which loaded animation
      names the queue is made up of. Since it's a required argument on
      creation, no name needs to be given there, but if you want to change
      which animations make up a queue later, do so like this:
      ``anim.edit_queue("tornado_kick", animation_names=("jump", "kick", "glide"))``.


Removing animations or queues
"""""""""""""""""""""""""""""

It's possible to remove animations from the animation pool of an actor, however
this is not usually advisable. If you try to play an animation that does not
exist anymore, the game will crash. While your projects are small, you usually
shouldn't have to worry about conserving resources, so it's fine to just leave
all animations in their system no matter what you do.

If you are working on a large project and are running into problems with
performance or memory usage, only then should you think about using these
methods: ``anim.remove(name)`` and ``anim.remove_queue(name)``. These will
delete a loaded animation or set queue from the animation system entirely.

Again, only use them if you need to and are careful about what you are doing
as otherwise crashes can happen quickly.


Animation system properties
"""""""""""""""""""""""""""

When you try to get the animation system to do something, it will always be
via methods. If you just want to know something about its current state
however, you can check the value of a few different properties ``anim`` has:

* ``anim.animation_pool`` will return a tuple of all the loaded animation
  names.
* ``anim.queue_pool`` will return a tuple of all the created animation queue
  names.
* ``anim.current`` will return the animation name that is currently running, if
  there is one. If not, it will return ``None``.
* ``anim.current_queue`` will return the name of the currently running queue,
  if there is one. If not, it will return ``None``.

    * *Note:* If a queue is running, then there will always be both a
      ``anim.current`` and a ``anim.current_queue``, since a queue is made up
      of single animations running one after the other.

* ``anim.current_queue_position`` will return the index of the currently
  running animation in the queue, ``0`` being the first, ``1`` the second and
  so on. If no queue is running, it will return ``None``.
* ``anim.base_animation`` is the name of the animation currently set to run
  whenever nothing else is running. Returns ``None`` if not set.
* ``anim.playing_base`` returns ``True`` if the base animation is currently
  playing, i.e. nothing else is in progress in the animation system right now.
  If not, returns ``False``.
* ``anim.paused`` returns ``True`` if the animation system is currently in a
  pause state or ``False`` if not.
* ``anim.current_type`` returns a string that specifies which type of playback
  the animation system is currently in: ``"base"`` means the base animation
  is playing, ``"queue"`` means a queue is playing and ``"single"`` means an
  animation which is not the base animation is playing not as part of a queue.
