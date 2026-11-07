.. _deep_dive_property_animation:

Deep dive: property animation
=============================

:ref:`Reference page on the animate function <reference_animate>`

It is easy to make changes to the game state gradually or in a single moment::

    def on_key_down(key):
        if key == keys.SPACE:
            player.pos = (150, 100)

    def update():
        if keyboard.up:
            player.y = player.y - 5

The event hook immediately teleports the player actor, while the code in
``update()`` makes small incremental changes instead.

But what if instead of a change starting out at state A and ending directly at
state B, it should have more flair? What if a thrown object should speed up
during its movement? What if a growing character should slightly overshoot its
target size before settling back down?

These kinds of small stylish variations to movements or state changes can make
games feel a lot more exciting to play, but they can be tricky to implement in
code. To help with this, PGTurbo provides the ``animate()`` function.


.. _deep_dive_property_animation_animate:

Animate function
----------------

The ``animate(object)`` function takes as its first argument an object (usually
an actor) and any number of properties to change for that object over time.
Here's a simple example::

    player.pos = (150, 100)
    animate(player, pos=(500, 150))

Thi will move the player actor smoothly from its position when the
``animate()`` function was called to the position given as a keyword argument
in the function call. The movement will happen over the course of one second,
since that is the default.

Any property of the object can be transitioned by using the property name as
the keyword argument name and giving the value that should be transitioned to
as the value for the keyword argument.

A few more examples::

    player.scale = 1.0
    animate(player, scale=0.1)

    player.angle = 0
    animate(player, angle=-120)

    player.opacity = 0.0
    animate(player, opacity=1.0)

So far, not very exciting. The true strength of ``animate()`` comes in tweening
the change from state A to state B. This slight change to the first example
makes the movement look very different::

    animate(player, tween="bounce_end", duration=1.5, pos=(500, 150))

For one thing, it takes slightly longer, since we set `duration` to one and a
half seconds this time. More noticeable is that the player actor will now
bounce at the target point before settling down.

``animate()`` allows you to easily give your actors more flair in their
movements and other state changes. However, it is only suitable when you know
an actor is going to move from state A to state B in exactly the time
`duration`.


.. _deep_dive_property_animation_tweening:

Tweening options
----------------

``animate()`` has a number of different tweening styles that change how the
transition is livened. The table below gives the string name you need to set
`tween` to to get a certain style, a short description and a visual
representation of the change:

+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'linear'           | Animate at a constant speed from start to finish     | .. image:: /_static/animate_plots/linear.png           |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'accelerate'       | Start slower and accelerate to finish                | .. image:: /_static/animate_plots/accelerate.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'decelerate'       | Start fast and decelerate to finish                  | .. image:: /_static/animate_plots/decelerate.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'accel_decel'      | Accelerate to mid point and decelerate to finish     | .. image:: /_static/animate_plots/accel_decel.png      |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'in_elastic'       | Give a little wobble at the start                    | .. image:: /_static/animate_plots/in_elastic.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'out_elastic'      | Give a little wobble at the end                      | .. image:: /_static/animate_plots/out_elastic.png      |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'in_out_elastic'   | Give a wobble at both ends                           | .. image:: /_static/animate_plots/in_out_elastic.png   |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'bounce_end'       | Accelerate to the finish and bounce there            | .. image:: /_static/animate_plots/bounce_end.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'bounce_start'     | Bounce at the start                                  | .. image:: /_static/animate_plots/bounce_start.png     |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'bounce_start_end' | Bounce at both ends                                  | .. image:: /_static/animate_plots/bounce_start_end.png |
+--------------------+------------------------------------------------------+--------------------------------------------------------+

If many of these still seem abstract, just copy the following PGTurbo code and
change the `tween` argument for ``animate()`` between running it to see the
differences::

    import pgtrun

    WIDTH = 600
    HEIGHT = 400
    player = Actor.Rectangle(60, 80, "red", (60, HEIGHT / 2))

    def on_key_down(key):
        player.pos = (60, HEIGHT / 2)
        animate(player, tween="linear", duration=2.0,
                pos=(WIDTH - 60, HEIGHT / 2))

    def draw():
        screen.clear()
        player.draw()

    pgtrun.go()


.. _deep_dive_property_animation_multiple_properties:

Multiple properties
-------------------

You can transition any number of properties with ``animate()`` at once. Simply
give each property name and the target value as their own keyword arguments and
all of them will be changed the same relative amount based on the chosen
tweening over the same time period::

    player.pos = (150, 100)
    player.scale = 0.1
    animate(player, tween="accelerate", duration=1.5, pos=(500, 150),
            scale=2.0)

This does not allow different properties to be animated at different speeds or
with different tweening however. If that is desired, use two separate calls
of ``animate()`` instead::

    player.pos = (150, 100)
    player.scale = 0.1
    animate(player, tween="accelerate", duration=1.5, pos=(500, 150))
    animate(player, tween="decelerate", duration=2.0, scale=2.0)


.. _deep_dive_property_animation_callback:

On finished callback
--------------------

You can specify a callback with the `on_finished` keyword argument. This
function will be called when the transition between states is completed.

If we want a sound to play once the player has arrived at their new position
for example, we could do so like this::

    def fanfare():
        sounds.trumpets.play()

    player.pos = (150, 100)
    animate(player, tween="bounce_end", duration=1.5, pos=(500, 150),
            on_finished=fanfare)

As with scheduling functions with ``clock``, it's important that you don't
give the callback with () here. If you did, the function is called and its
return value is set as the callback, which won't work. Instead, only give the
name of the function without the parentheses.

In contrast to ``clock``, you cannot set a callback function that requires
arguments to call with ``animate()``. Only functions that don't take any
arguments are useable here.


.. _deep_dive_property_animation_absolute:

Timescale or not
----------------

By default, property animations using ``animate()`` respect the value of
``clock.timescale``. That means, if you set the game time speed to half,
all property animations will also happen half as fast. The opposite is true as
well, if ``clock.timescale`` is ``3.0``, everything will happen much quicker.

If you want to have some animations running at the same speed regardless of
``clock.timescale``, you can call ``animate()`` with the keyword argument
``absolute=True``. This will makes it so that specific property animation
runs at normal real time speed no matter what value ``clock.timescale`` has.


.. _deep_dive_property_animation_object:

Animation objects
-----------------

When calling ``animate()``, the function actually returns an object of the
class ``Animation``. You can keep a reference to this object to interrupt an
ongoing property animation or check if it is still running::

    player.pos = (150, 100)
    move_animation_obj = animate(player, tween="bounce_end", duration=5.0,
                                 pos=(500, 150))

    def on_key_down():
        move_animation_obj.stop()

In the above example, if any key is pressed during the property animation, it
is interrupted and stops. The actor simply remains where it was when the key
was pressed.

Alternatively, if you call ``Animation.stop(True)`` (optional boolean
parameter), the animation is interrupted but the actor is teleported to its
destination instead. Calling with ``True`` will set the property that was
animated to the target value immediately instead of just interrupting and
leaving it where ever it was.

Checking ``Animation.running`` will return whether a property animation is
finished or not.

Checking or setting ``Animation.on_finished`` also allows you to switch what
or if a function should be called when the animation is done while it is still
ongoing.
