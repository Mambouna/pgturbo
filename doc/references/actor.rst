.. _reference_actor:

Reference: Actor
=================

:ref:`Deep dive on actors <deep_dive_actors>`


.. _reference_actor_attributes:

Attributes
----------

.. attribute:: pos

    The X and Y position of the actor's anchor point as a tuple of two numbers.
    Can be set to move the actor.

    Example value: ``(10, -15)``

.. attribute:: x

    Only the X position of the actor's anchor point as a number. Can be set to
    move the actor.

    Example value: ``10``

.. attribute:: y

    Only the Y position of the actor's anchor point as a number. Can be set to
    move the actor.

    Note that in video games, Y axis values grow towards the bottom. So the top
    of the window is Y = 0 and the value grows as an actor moves down. This is
    different from the orientation of the Y axis in maths.

    Example value: ``-15``

.. attribute:: left

    Only the X position of the left side of the actor's rectangle. Can be set
    to move the actor.

    Example value: ``25``

.. attribute:: right

    Only the X position of the right side of the actor's rectangle. Can be
    set to move the actor.

    Example value: ``50``

.. attribute:: top

    Only the Y position of the top edge of the actor's rectangle. Can be
    set to move the actor.

    Example value: ``30``

.. attribute:: bottom

    Only the Y position of the bottom edge of the actor's rectangle. Can be
    set to move the actor.

    Example value: ``55``

.. attribute:: topleft

    The X and Y position of the top left corner of the actor's rectangle.
    Can be set to move the actor.

    *Note:* This always reports the position of the bounding box of the actor,
    not its image. For an illustration of the possible difference whith rotated
    actors, check the image below the property list.

    The following properties work the same way for the other corners and
    sides of the actor: ``bottomleft``, ``topright``, ``bottomright``,
    ``midtop``, ``midleft``, ``midright``, ``center``.

    Example value: ``(25, 30)``

    Default value: ``(0, 0)``. If an actor is created without specifying
    a position, its top left corner will be placed at ``(0, 0)``.


.. attribute:: image

    The string name of the image the actor shows on the screen. Can be set
    to change the appearance of the actor. This will look for an image file
    in the *images* :ref:`resource folder <reference_images>` with the given name to
    load for the actor to use.

    Example value: ``"rabbit"``

.. attribute:: anim

    This attribute functions as the manager of all things related to actor
    sprite animation. There should never be a reason for you to just get the
    component itself without accessing some attribute or method on it.

    The attributes and methods of the ``anim`` component are detailed
    in a separate section below this one.

.. attribute:: anchor

    Returns the position of the anchor point of the actor in relation to its
    image. Can be returned in one of two ways:

    #. If the anchor is set to a symbolic position, for example the default
       of ``("center", "center")``, it will be reported as a tuple of strings.
    #. If the anchor is set to a pixel position in relation to the topleft
       corner of its image, a tuple of integers will be returned. A position
       in the middle and bottom of an actor with an image size of 16x32 pixels
       for example could be ``(8, 32)``.

    Can be set to change the anchor position, which does not immediately move
    the actor image. Symbolic anchor positions are given as a tuple with the
    following options:

    ``"left"``, ``"center"``, ``"middle"`` or ``"right"`` for the horizontal
    anchor position. ``"top"``, ``"center"``, ``"middle"`` or ``"bottom"`` for
    the vertical anchor position.

    To set a pixel position for the anchor, simply use a tuple of two integers
    or floats.


.. attribute:: angle

    The rotation value the actor is currently at as a number. Can be set to
    rotate the actor.

    In Pygame Turbo, an angle of ``0`` means the actor is "looking" towards
    the right edge of the game window, with values growing counter
    clockwise. So ``90`` will have the actor "looking" up, ``180`` left
    and ``270`` down.

    Default value: ``0``


.. attribute:: scale

    What size to scale the actor image to. Returns a tuple of two numbers
    for the scale in X and Y directions. Can be set to change the scale.

    *Note:* You can also set this with a single number which will then be
    applied to both axis scales: ``alien.scale = 2.0`` will result in a new
    value of ``(2.0, 2.0)``.

    Default value: ``(1.0, 1.0)``

.. attribute:: scale_x

    The scale of the actor image in the X direction. Returns a single
    number. Can be set to change the scaling.

    Default value: ``1.0``

.. attribute:: scale_y

    The scale of the actor image in the Y direction. Returns a single
    number. Can be set to change the scaling.

    Default value: ``1.0``

.. attribute:: flip_x

    Boolean value of whether the actor image should be flipped on its X
    axis. Can be set to flip the actor image.

    Default value: ``False``

.. attribute:: flip_y

    Boolean value of whether the actor image should be flipped on its Y
    axis. Can be set to flip the actor image.

    Default value: ``False``

.. attribute:: opacity

    Number value of how solid or transparent the actor image is drawn.
    ``1.0`` means the image is fully solid where ``0.0`` means its fully
    transparent and thus invisible. Can be set to change image opacity.

    Default value: ``1.0``

    The following image shows the progression from transparency to solid
    color based on the float value used:

    .. image:: /_static/actor/opacity.svg

.. attribute:: tint_color

    Color used to tint the actor image if ``tint_value`` is other than ``0.0``.

    Default value: ``"darkgray"``

    This allows both brightening and darkening of actors while leaving their
    color balance alone.

    Brighter colors are more suitable to brightening tints while darker colors
    are better at darkening tints.

.. attribute:: tint_value

    Value controlling if and how a tint is applied to the actor image.

    Default value: ``0.0``

    ``0.0`` means no tinting is applied. Values from ``0.0`` to ``1.0`` will
    apply a tint that brightens the image.

    Values from ``0.0`` to ``-1.0`` will apply a tint that darkens the image.

    The tint will use the ``tint_color`` color and relative the strength of
    the effect is also dependent on how bright or dark the color used for
    tinting is by itself.

.. attribute:: vel

    Tuple of two numbers representing the velocity of the actor. Each
    number represents how far the actor will move in the X and Y axis per
    call of ``move_by_vel()``. Allows easy management of actors that move
    in straight lines at constant speed. Can be set.

    Default value: ``(0, 0)``

.. attribute:: vx

    Number representing the velocity in the X axis of the actor. Can be
    set.

    Default value: ``0``

.. attribute:: vy

    Number representing the velocity in the Y axis of the actor. Can be
    set.

    Default value: ``0``


.. attribute:: x_limits

    Tuple of two numbers or ``None`` representing the minimum and maximum
    pixel values the actors' image bounds cannot cross in the X axis. Can
    be set to create or remove limits.

    ``None`` means the actor is free to move in that direction where a
    number means that if the actor is moved beyond this value in the axis,
    it will be set back automatically to stay at the limit instead.

    The first value represents the left limit, under which the left edge of
    the actor cannot cross. The second value is the right limit, over which
    the right edge of the actor cannot cross.

    Example value: ``(15, WIDTH - 15)``. This would limit the actor
    horizontally so it cannot move off the screen.

    Default value: ``(None, None)``

.. attribute:: y_limits

    Tuple of two numbers or ``None`` representing the minimum and maximum
    pixel values the actors' image bounds cannot cross in the Y axis. Can
    be set to create or remove limits.

    ``None`` means the actor is free to move in that direction where a
    number means that if the actor is moved beyond this value in the axis,
    it will be set back automatically to stay at the limit instead.

    The first value represents the top limit, under which the top edge of
    the actor cannot cross. The second value is the bottom limit, over
    which the bottom edge of the actor cannot cross.

    Example value: ``(15, HEIGHT - 15)``. This would limit the actor
    vertically so it cannot move off the screen.

    Default value: ``(None, None)``

.. attribute:: left_limit

    Number or ``None`` which represents the left limit for actor movement.
    ``None`` means there is no limit. A number is the X position under
    which the left edge of the actor cannot cross. Can be set to create or
    remove a limit.

    Default value: ``None``

.. attribute:: right_limit

    Number or ``None`` which represents the right limit for actor movement.
    ``None`` means there is no limit. A number is the X position over
    which the right edge of the actor cannot cross. Can be set to create or
    remove a limit.

    Default value: ``None``

.. attribute:: top_limit

    Number or ``None`` which represents the top limit for actor movement.
    ``None`` means there is no limit. A number is the Y position under
    which the top edge of the actor cannot cross. Can be set to create or
    remove a limit.

    Default value: ``None``

.. attribute:: bottom_limit

    Number or ``None`` which represents the bottom limit for actor
    movement. ``None`` means there is no limit. A number is the Y position
    under which the bottom edge of the actor cannot cross. Can be set to
    create or remove a limit.

    Default value: ``None``


.. attribute:: width

    The pixel width of the current actor image with scaling applied as a
    number. Can be set to adjust the scaling of the actor to fit the new
    width.

    *Note:* This is not the width of the bounding box that contains the
    actor if it is rotated. See the image below for an example of the
    difference between width and bounding width.

    Example value: ``64``

.. attribute:: height

    The pixel height of the current actor image with scaling applied as a
    number. Can be set to adjust the scaling of the actor to fit the new
    width.

    *Note:* This is not the height of the bounding box that contains the
    actor if it is rotated. See the image below for an example of the
    difference between height and bounding height.

    Example value: ``64``

.. attribute:: bounding_width

    The pixel width of the bounding box containing the current actor image
    with scaling and rotation applied. This only differs from ``width`` if
    the actor angle is not ``0``. Cannot be set.

    Example value: ``82``

.. attribute:: bounding_height

    The pixel height of the bounding box containing the current actor image
    with scaling and rotation applied. This only differs from ``height`` if
    the actor angle is not ``0``. Cannot be set.

    Example value: ``82``

.. attribute:: data

    A dictionary that can be filled with custom values for the game, useful
    for anything to do with game mechanics that aren't so general to be covered
    by PGTurbo itself.

    Tracking the movement speed of an actor might look like this::

        runner.data["move_speed"] = 8

    Values tracked can then used as follows::

        runner.x = runner.x + runner.data["movement_speed"]

    To check wheter a certain actor has a value for some name, use
    ``if "name" in actor.data:``. Reset the data dictionary to be empty with
    ``Actor.data.clear()``.

.. _reference_actor_dimensions_vs_bounding_dimensions:

.. image:: /_static/actor/dimensions_vs_bounding_dimensions.png


.. _reference_actor_methods:

Methods
-------

.. method:: draw()
    :no-index:

    Draws the actor onto the game window.

.. method:: colliderect(other_actor)

    Returns a boolean of whether the bounding rectangle of this actor touches
    the one of the other actor. This is fast and useful for quick but imprecise
    collision detection.

    ``True`` means the actors collide, ``False`` means they do not.

    :param other_actor: The other actor object that should be checked for a
                        collision.

.. method:: collidemask(target)

    Does a pixel perfect collision check against the `target`. The target can
    either be another actor or a position tuple.

    If the target is an actor, returns ``True`` if their images overlap at all,
    otherwise ``False``.

    If the target is a position tuple, returns ``True`` if the position tuple
    lies on the image of the actor, otherwise ``False``.

    **Important:** Pixel perfect collision detection is far less performant
    than rough collision detection like ``Actor.colliderect()`` or
    ``Actor.collidepoint()``.

    Use this only when the number of collision checks to do is low as it will
    cause performance problems if used too much.

    :param target: The other actor object or position tuple that should be
                   checked for a collision.


.. method:: angle_to(target)

    Returns the angle from this actor to the target. As with the actor
    ``angle`` attribute, ``0`` means directly to the right, ``90`` means
    directly up and so on.

    :param target: Either another actor or a position tuple of two numbers.

.. method:: distance_to(target)

    Returns the distance to the target in pixels.

    :param target: Either another actor or a position tuple of two numbers.

.. method:: is_onscreen([margin, margin_y])

    Returns a boolean of whether the actor is currently inside the game window.

    Returns ``False`` only if not a single part of the bounding box of the
    actor is in the game window and ``True`` otherwise.

    If margins are provided via arguments, the screen will be interpreted as
    that much larger on either side when checking if the actor is still
    onscreen. If only one argument is given, that value is the margin in both
    X and Y directions. If two arguments are given, the first is for the X
    axis and the second for the Y axis.

    :param margin: Optional integer or float argument. If there is only one
                   argument, this is the margin used for both X and Y.
                   Otherwise it is the margin for the X axis.
    :param margin_y: Optional integer or float argument. Must be used together
                     with the ``margin`` argument. This is the margin for the
                     Y axis.


.. method:: move_towards_angle(angle, distance)

    Moves the actor the given distance along the specified angle.

    The ``angle`` attribute of the actor will not be changed by this method,
    only its position.

    :param angle: The angle along which the actor should be move. ``0`` means
                  straight right.
    :param distance: How far to move the actor in pixels.

.. method:: move_towards_point(target, distance, [overshoot])

    Moves the actor the given distance towards the specified point. The target
    point is a position tuple of two numbers or an actor object. If it is an
    actor, the ``.pos`` attribute of that actor is used as the target point.

    By default, if the distance to the point is smaller than the given distance
    to be moved, the actor will only move up to the point but not overshoot it.
    If the optional parameter ``overshoot`` is given as ``True`` however, the
    actor will move past the target point if the given distance is far enough.

    :param target: A position tuple of two numbers the actor should move
                   towards or another actor object.
    :param distance: The number of pixels the actor should move by.
    :param overshoot: Boolean of whether the actor should stop at the target
                      point if the given distance is enough to reach it or move
                      past it. Default is ``False``.
    
.. method:: move_forward(distance)

    Moves the actor forward along its current ``angle`` by the given distance.

    :param distance: The number of pixels the actor should be moved by.

.. method:: move_backward(distance)

    Moves the actor backwards in the opposite direction of its current
    ``angle`` by the given distance.

    :param distance: The number of pixels the actor should be moved by.

.. method:: move_left(distance)

    Moves the actor sideways to the left when viewing its ``angle`` as "up".

    This does not mean the actor moves along the Y-axis, but instead that if
    the actor is pointing to the right, then right is forward to the actor and
    left from its perspective would be up in the game window.

    :param distance: The number of pixels the actor should be moved by.

.. method:: move_right(distance)

    Moves the actor sideways to the right when viewing its ``angle`` as "up".

    The same applies here. Right is always in relation to where the actor is
    pointing.

    :param distance: The number of pixels the actor should be moved by.

.. method:: move_by_vel(distance, [scale])

    Moves the actor position by its velocity once. Calling this every
    ``update()`` will smoothly move the actor along its velocity trajectory.

    :param distance: The number of pixels the actor should be moved by.
    :param scale: A multiplier for the distance moved by the actor. Default is
                  ``1.0`` meaning the specified distance is moved. ``2.0``
                  would move the actor twice as far, whereas ``0.1`` would move
                  at 10% of the speed.

.. method:: intercept_velocity(target, speed)

    Returns a velocity tuple that will move from the position of the actor
    to intercept the target actor with the given speed, as long as the
    target does not change its velocity at some point.

    The target actor must have its velocity set for this to work. If no
    valid interception is possible (because the speed is too low), ``None`` is
    returned.

    :param target: The actor for which an intercept velocity should be
                   calculated.
    :param speed: How far in pixels the actor should move each call of
                  ``move_by_vel()`` if an intercept can be found.


.. method:: flip_x_over_anchor()

    Inverts the current ``flip_x`` attribute value while also flipping the
    entire actor image along the anchor axis. Does not only flip the image in
    place but rather moves it to appear flipped in space.

    This changes the anchor value. For example, a previous anchor of
    ``("center", "bottom")`` will be ``("center", "top")`` after the function
    call.

.. method:: flip_y_over_anchor()

    Inverts the current ``flip_y`` attribute value while also mirroring the
    anchor position along the same ayis. If the anchor is centered, this is
    equivalent to just using ``flip_y`` directly. If the anchor is not centered
    however, this will not only flip the actor image in place but rather flip
    the entire actor, moving the picture so that it ends up flipped along the
    anchor position in the axis.

.. method:: track_ready(*args)
    :no-index:
    
    .. Comment to disable wrong syntax highlighting from the star.*

    Adds one or multiple ready timers that the actor can report as ready and
    time out. If given one string and one number, a single ready timer is
    added for the actor. The string is the name for the ready timer and the
    number the timeout period in seconds.

    To add multiple timers with one call, give one tuple per timer as arguments
    where each tuple contains one string and one number.

    Example: ``alien.track_ready(("jump", 0.6), ("powerup", 2.5))``

    :param args: Argument sink to turn into one or more added ready timers.

.. method:: is_ready(name)
    :no-index:

    Returns ``True`` if the given timer is currently ready or ``False`` if
    not.

    :param name: Name of the ready timer to check.

.. method:: timeout_ready(name, [time, absolute])
    :no-index:

    Set a ready timer to ``False`` for the duration of its set timeout
    period, after which it will be returned to ``True`` again.

    :param name: The name of the ready timer to time out.
    :param time: Optional override for how long the timer should remain
                 ``False``. Give a number to use a timeout period other
                 than the default set for the ready timer.
    :param absolute: Optional boolean of whether the timeout period should be
                     tracked in absolute time or time affected by timescale.
                     Default is ``False``, meaning timescale affects the timer.

.. method:: set_ready(name, value)
    :no-index:

    Set the ready value of a ready timer manually and permanently. This
    could be used to disable an ability in general based on some state.
    Calling ``timeout_ready()`` will still set the timer back to ready
    after the timeout period.

    :param name: What timer to change the ready value on.
    :param value: Boolean of whether the ready timer should be permanently
                  ready (``True``) or not (``False``) until a timeout is
                  triggered.

.. method:: get_ready_timeout(name)
    :no-index:

    Returns the current timeout period set for a ready timer.

    :param name: String for which timer to get the timeout period of.

.. method:: set_ready_timeout(name, value)
    :no-index:

    Set the timeout period for the given ready timer. Doesn't affect a
    timeout that is already running.

    :param name: The timer for which to change the timeout period.
    :param value: Number value for the seconds the timeout period should
                  last.

.. method:: get_all_ready()
    :no-index:

    Returns a dictionary of all ready timers with their names as keys and
    their ready state as values.

    Changing the data in this dictionary does not change anything about the
    ready timers kept by the actor.


.. _reference_actor_anim:

Anim component
--------------

The following are the attributes and methods on the ``anim`` component all
actors have which is used for sprite animations. Each one is shown as
``anim.attribute`` or ``anim.method()`` for clarity.


.. _reference_actor_anim_attributes:

Attributes
""""""""""

*Note:* None of the attributes on ``anim`` can be set. They are only used to
get information back. To act on ``anim``, you always use methods.

.. attribute:: anim.animation_pool

    A tuple of all currently valid animation names.

.. attribute:: anim.queue_pool

    A tuple of all currently valid queue names for the anim component.

.. attribute:: anim.current

    String name of the currently running animation or ``None`` if nothing
    is playing.

.. attribute:: anim.current_queue

    String name of the currently running queue or ``None`` if nothing is
    playing or a single animation is running not as part of a queue.

.. attribute:: anim.current_queue_position

    Integer index of which animation in the current queue is running. ``0`` is
    the first, ``1`` the second and so on to stay consistent with Python
    zero-indexing. Returns ``None`` if no queue is running.

.. attribute:: anim.base_animation

    String name of the currently set base animation or ``None`` if no base
    animation is set.

.. attribute:: anim.playing_base

    Boolean of whether the set base animation is currently running.

.. attribute:: anim.paused

    Boolean of whether animations are currently paused.

.. attribute:: anim.current_type

    String for which type of animation is currently playing or ``None`` if
    nothing is playing.

    ``"base"`` means the base animation is playing, ``"queue"`` means a
    queue is playing and ``"single"`` means any other animation which is
    not the base animation is playing and not as part of a queue.


.. _reference_actor_anim_methods:

Methods
"""""""

.. method:: anim.add(name, [durations, offsets, callback])

    Adds an animation from a folder with separate image files to the
    actor's animation pool.

    :param name: The name of the folder with the animation frames in it.
    :param durations: Over what time the animation should play out. Default
                      is one second. If given a single number, the
                      animation frames will be evenly distributed over that
                      time. If a list or tuple with a number of values
                      equal to the number of animation frames is given
                      instead, those specific values will be the duration
                      of the respectiv frames.
    :param offsets: How to move the animation frames in relation to the
                    actor's base image. This can be used to properly align
                    animation frames with sizes other than the base image
                    size. Offsets are given as tuples of X and Y changes in
                    relation to the base image topleft corner. For example,
                    if one animation frame is taller than the base image,
                    an offset of ``(0, -32)`` would shift it up by 32 pixels.

                    If a single tuple of two numbers is given, that offset
                    is applied to all animation frames. If a tuple or list
                    of multiple offsets is given, each will be applied to
                    only the respective animation frame.
    :param callback: A function name to call once the animation has
                     finished playing.

.. method:: anim.add_spritesheet(name, width, height, [durations, offsets, callback, vertical])

    Adds an animation from a spritesheet to the actor's animation pool.

    :param name: The filename of the spritesheet without a file extension.
    :param width: The width in pixels of an animation frame in the
                  spritesheet.
    :param height: The height in pixels of an animation frame in the sheet.
    :param durations: The duration over which the animation will play. Same
                      possible values and default as for ``anim.add()`` above.
    :param offsets: The offsets to be applied to the animation frame whe
                    drawing the actor. Same possible values and default as
                    for ``anim.add()`` above.
    :param callback: A function name to call once the animation has
                     finished playing.
    :param vertical: Boolean flag of whether the spritesheet is arranged
                     vertically or not. Default is ``False``, meaning that
                     spritesheets are normally read left to right. If set
                     to ``True``, the spritesheet will be read top to bottom
                     instead.

.. method:: anim.add_queue(name, animation_names, [callback, new_base])

    Adds a new animation queue made up of previously loaded animations.

    :param name: The name for the new animation queue.
    :param animation_names: A tuple or list of the animation names to be
                            included in the queue.
    :param callback: A function name to call once the animation queue has
                     finished playing.
    :param new_base: An animation name that should be set as the new base
                     animation once the queue has finished playing.

.. method:: anim.edit(name, **kwargs)
    
    .. Comment to disable wrong syntax highlighting from the double star.**

    Edits the settings of an existing animation. You can edit any of the
    optional parameters of an animation: durations, offsets, sound,
    callback and new_base.

    To change one, simply give that keyword with the new value as an
    argument to ``edit()``.

    Example: ``alien.anim.edit("walk_up", durations=2.0)``

    :param name: The name of the animation that should be edited.
    :param kwargs: Any number of keywords and values their options should
                   be set to.

.. method:: anim.edit_queue(name, **kwargs)
    
    .. Comment to disable wrong syntax highlighting from the double star.**

    Edits the settings of an existing queue. You can edit any of the
    optional parameters of a queue: sound, callback and new_base.
    Additionaly, you can also change what animations the queue plays by
    giving animation_names as a keyword parameter.

    Example:
    ``alien.anim.edit_queue("idle", animation_names=("stand", "sit"))``

    :param name: The name of the queue that should be edited.
    :param kwargs: Any number of keywords and values their options should
                   be set to.

.. method:: anim.set_base(name)

    Set the base animation to play when nothing else is running. If the
    former base animation was running, switch it to the new one.

    :param name: The name of the new base animation. Call with ``None`` to
                 remove the base animation.

.. method:: anim.remove(name)

    Removes a loaded animation from the animation pool. If the animation is
    currently playing as part of a queue, the queue will skip forward to
    the next animation in its sequence. If the animation is playing outside
    of a queue, it is stopped before removal. If the animation was on
    pause, the pause state is wiped, meaning unpausing will only play the
    base animation if there is one.

    :param name: The name of the animation to remove.

.. method:: anim.remove_queue(name)

    Removes a named queue from the queue pool. If the queue is currently
    playing, it will be stopped before removal. If the animation was on
    pause, the pause state is wiped, meaning unpausing will only play the
    base animation if there is one.

    :param name: The name of the queue to remove.

.. method:: anim.play(name)

    Play a loaded animation. If the same animation is already running,
    nothing is done. This means you can safely keep calling this without
    restarting the same animation over and over again.

    :param name: The string name of the animation to play.

.. method:: anim.play_queue(name, [position])

    Play a named animation queue. If it is already playing, it won't be
    restarted, just like with ``anim.play()``.

    :param name: The name of the queue to play.
    :param position: From what animation to start playing the queue.
                     Default is ``0``, which is the first animation. The
                     position numbers reflect zero-indexing.

.. method:: anim.start(name)

    Play a loaded animation. If it is already running, restart the
    animation. This is the important difference to ``anim.play()``. If you
    want to definitely start an animation from the beginning, even if it is
    already playing, use this function.

    :param name: The string name of the animation to start playing.

.. method:: anim.start_queue(name, [position])

    Play a named animation queue. If it is already playing, restart it just
    like ``anim.start()``.

    :param name: The name of the queue to start playing.
    :param position: From what animation to start playing the queue.
                     Default is ``0``, which is the first animation. The
                     position numbers reflect zero-indexing.

.. method:: anim.pause()

    Pause all animation playback, freezing the display image of the actor at
    the last animation frame image that was gotten.

.. method:: anim.unpause()

    Allow all animation playback and return to the state in animation
    before the pause. If something paused was removed, return to playing
    the base animation if there is one. If that was the case, a warning
    will be printed.

.. method:: anim.stop()

    Stop any currently running animation and return to the base animation
    if one is set.

.. method:: anim.stop_all()

    Stop any currently running animation as well as removing the base
    animation. This returns the display of the actor to the static image.


.. _reference_actor_changelog:

Changelog
---------

* **1.15:** Added ``velocity_towards_angle()`` and ``velocity_towards_point()``
  methods, added ``.data`` dictionary for all actors to store values for game
  mechanics, added ``.tint_color`` and ``.tint_value`` properties to shade and
  tint actor images, added ``suppress`` option for animation queue playing to
  control what individual animation option triggers are done, fixed a few bugs
  around the sprite animation system.
* **1.14:** Added point argument support for ``collidemask()``. Small
  documentation improvements.
* **1.13:** Added margin arguments for ``is_onscreen()``. Also improved a lot
  of documentation around ``move_towards_point()`` and ``anchor``. Minor
  bugfixes.
* **1.12.1:** Fixed some documentation problems around sprite animations and
  queues.
* **1.11:** Added movement limit support for actors.
* **1.10:** Added ready timer system for all actors.
* **1.9:** Added actor sprite animation system in ``anim``.
* **1.5:** Added scaling and flipping, allow ``width`` and ``height`` to be set
  to scale as well.
* **1.4.2:** Improved positional errors on actor creation.
* **1.4:** First release of PGTurbo after fork from PGZero.
