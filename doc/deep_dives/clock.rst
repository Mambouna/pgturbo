.. _deep_dive_clock:

Deep dive: clock
================

:ref:`Reference page on the clock builtin <reference_clock>`

Games often require a number of different functionalities that have to do with
time and time running down or being counted up. For all these purposes, the
``clock`` builtin exists.


.. _deep_dive_clock_scheduling:

Scheduling
----------

The single most powerful ability that ``clock`` has is allowing you to set
function to be called in the future. Let's say you want a new enemy to appear
every five seconds. To do this, you simply write a single function that creates
a new enemy and then ask ``clock`` to call this function every five seconds
for you::

    def new_enemy():
        e = Actor("enemy")
        e.x = random.randint(100, WIDTH - 100)
        e.y = random.randint(100, HEIGHT - 100)
        enemy_list.append(e)

    clock.schedule_interval(new_enemy, 5.0)

You can ignore the specific code in ``new_enemy()`` for now. Relevant is only
how we use ``clock`` to call it on a repeating timer of five seconds.

To schedule a function to be called, use ``clock.schedule()``, 
``clock.schedule_interval()`` or ``clock.schedule_unique()``. Each of these
take the same kinds of arguments:

#. The name of a function that should be called after the scheduled timer. It
   is important to write the name WITHOUT () parentheses, since that would
   immediately call it. Instead, write the function name without ().
#. A time in seconds after which the function should be called.
#. Any number of arguments that should be given to the function when it is
   being called. Note these values are set when scheduling and cannot be
   changed between scheduling and the function being called.

  Example: ``clock.schedule(spawn_gem, 3.0, "red", 200, 100)``

  This scheduling will mean the following call will be made after three seconds
  of time: ``spawn_gem("red, 200, 100)``.

The difference between the three given functions is as follows:

* ``clock.schedule()``: This schedules a single function call after the given
  time runs out. If the same function had already been scheduled before and is
  still waiting to be called, there will be two scheduled calls for that
  function afterwards.

  Let's say a reward is scheduled to appear after 10 seconds and four seconds
  later, another reward is scheduled to appear after 10 seconds. Using
  ``clock.schedule()`` will leave two calls of the same function scheduled, one
  in six seconds and one in ten seconds.
* ``clock.schedule_interval()``: This schedules a single function to be called
  after the given time runs out and then again and again after the same time
  span each time. If you want something to happen every X seconds, use
  ``clock.schedule_interval()``.
* ``clock.schedule_unique()``: This schedules a single function to be called
  after the given time runs out and unschedules any other calls for that same
  function with the same arguments that were previously scheduled and hadn't
  been called yet.

  Going back to the previous example of rewards being given, if
  ``clock.schedule_unique()`` was used after the first reward had been
  scheduled, that call would have been cancelled and afterwards there would
  only be one call to the function for after ten seconds.

In a real game, it is likely that many function calls will be scheduled all the
time with different delays and for different functions. What if you need to
stop an already scheduled call without creating a new one? For example, an
enemy might have been charging an attack but was then defeated.

Use ``clock.unschedule(function)`` to cancel a scheduled function call. When
doing so, you need to give the same arguments you used when scheduling the
function. Let's say the following was scheduled::

    clock.schedule(spawn_gem, 3.0, "blue", 200, 100)
    clock.schedule(spawn_gem, 4.0, "red", 400, 200)
    clock.schedule(spawn_gem, 5.0, "green", 600, 300)

Now to unschedule only the call to create a red gem, use the this::
    
    clock.unschedule(spawn_gem, "red", 400, 200)

If instead you need to unschedule all calls to a certain function regardless
of what arguments they were scheduled with, use
``clock.unschedule_all(function)``. To stop all the gems from above from
spawning, we'd to the following::

    clock.unschedule_all(spawn_gem)


Scheduling normally respects the ``timescale`` of the
``clock``. This will be discussed in more detail in the next section, but in
short, it allows you to slow down or speed up the timing functionality of your
game. If this changes, the scheduled calls will also happen earlier or later
depending on the timescale.

If you want a function call to be made after exactly the specified time,
regardless of any changes to ``timescale``, you can do so by giving the keyword
argument ``absolute=True`` to the scheduling::

    clock.schedule(close_menu, 2.0, absolute=True)

This also means you cannot use a keyword parameter named ``absolute`` for the
function to be called, as it is the single kind of argument past the first two
that will not be passed onto the called function.


.. _deep_dive_clock_timescale:

Timescale
---------

``clock`` allows you to control how fast its timekeeping functionality runs.
You can use this to effectively slow down or speed up time in your game, but it
requires some manual management by you.

Any functionality of clock itself will automatically be sped up or slowed down
to respect its ``timescale`` property. This property has the value ``1.0`` by
default, for which time runs at normal speed. A call scheduled for in two
seconds will happen after two seconds.

Decreasing ``timescale`` slows down timekeeping. Setting
``clock.timescale = 0.5`` before scheduling something for two seconds delay
will result in the call only being made four seconds later. This is because
time now "runs" half as fast.

Doing ``clock.timescale == 2.0`` on the other hand will make time "run" twice
as fast, resulting in the same scheduled call happening after only one second.

As mentioned before, anything managed by ``clock`` directly automatically
follows ``clock.timescale``, but nothing else does. What does this mean?

If you want to slow down your game's time, the characters should presumably
also move slower, but character movement isn't handled by ``clock``. This means
you have to adjust the movement speed of the characters yourself with
``timescale``. That could look something like this::

    def update():
        if keyboard.left:
            player.x = player.x - 10 * clock.timescale
        if keyboard.right:
            player.x = player.x + 10 * clock.timescale

This should look familiar. We multiply a base change to a value with a value
that changes it based on circumstances. You might have seen this before in the
:ref:`deep dive on the update/draw cycle <deep_dive_update_draw_cycle>` where
it was done with ``dt`` to make you game framerate independent.

Respecting the timescale of the game works the same way. If ``clock.timescale``
is ``1.0``, the player will move 10 pixels with each change. This is the
"normal" movement speed.

If timescale is ``2.0``, now each change will move the player by 20 pixels,
making it move faster across the screen. This make sense if your game is
supposed to look like time is running faster.

A timescale of ``0.5`` instead will make each change move the player by only
five pixels, making them move a lot slower, just like time was slowed down.

Whereever your game code changes values over time (usually in the ``update()``
function), you need to manually make the changes respect ``clock.timescale``,
if you want to create the effect of changing time speed. One exception to this
are actor sprite animations, since they internally use the clock builtin
themselves to change out their frames.

Another exception is the ``animate()`` builtin. Property animations by default
respect ``clock.timescale`` since they track their progress through the
``clock`` builtin. If you want an ``animate()`` change to happen without
following timescale, call it with the ``absolute=True`` keyword argument.

If you want your game to be framerate independent AND make use of
``clock.timescale``, you will usually have to make changes over time dependent
on both values::

    def update(dt):
        if keyboard.left:
            player.x = player.x - 10 * clock.timescale * dt
        if keyboard.right:
            player.x = player.x + 10 * clock.timescale * dt
        
``dt`` will make sure the game's framerate won't change how fast it runs and
``clock.timescale`` will then make the game mechanics run at the speed you set
for time.


.. _deep_dive_clock_elapsed_time_and_time_marks:

Elapsed time and time marks
'''''''''''''''''''''''''''

Another use of clock is to keep track of elapsed time in different ways. If you
just want to get the total time since the program started, ``clock.time``
will return how many seconds have passed, affected by ``clock.timescale`` (use
``clock.absolute_time`` to get the real elapsed seconds regardless of game time
speed).

Often though, we are more interested in how much time has gone by since a
certain starting moment, like the start of a round for example::

    def update():
        if keyboard.space and round_over:
            clock.mark_time("game_begin")
            # ...
        # ...
        if opponent.colliderect(player) and not round_over:
            time_played = clock.time_since_mark("game_begin")
            # ...

In the example, a round is started when the space key is pressed. Besides
everything else that needs to happen to start the game, we remember when the
game was started with ``clock.mark_time()``. We called the mark
``"game_begin"`` so that's what we need to use later again.

When the round ends (when the opponent touches the player) we can then get the
length of the round by calling ``clock.time_since_mark()`` with the name of the
mark we set up before.

Summing up, we can make a pin in a point in time with a given name by calling
``clock.mark_time("name")`` and later check how much time has passed since that
pin was placed with ``clock.time_since_mark("name")``.

If you ``mark_time()`` with the same name that a previous mark used, the
previous mark is replaced with the new one. In the example above, that is how
each round remembers the time for itself. Every new marking of *game_begin*
overwrites the previous one.

All marks allow you to check both the time since marking affected by
``clock.timescale`` and also how much real time has passed unaffected by game
time. To do the latter, use ``clock.time_since_mark("name", absolute=True)``.

To check what the time was when a mark was set, use
``clock.get_mark_time("name")``. To get a dictionary of all time marks with
their names as keys and when they were created as values, use
``clock.get_all_marks()``. For both of these methods, using the
``absolute=True`` keyword argument will return the mark timestamps as absolute
time instead of affected by ``clock.timescale``.


.. tip::

    Since times are returned in seconds, they are often long fractions of whole
    numbers. If you want to display time values in the game window, consider
    converting the timestamp to a whole number with ``int(timestamp)`` first.
    ``int()`` from a ``float`` will always round down, which is usually
    desirable for displaying elapsed seconds.


.. _deep_dive_clock_ready_timers:

Ready timers
''''''''''''

Often in games you'll want to only allow certain things to happen if they are
"ready". Say for example a character has a special ability to jump higher than
normal but they should only be able to do that again after five seconds have
passed. For any such scenario, you can use clock ready timers. To do so, first
you add something to track::

    clock.track_ready("superjump", 5.0)

Now you can check whether the tracked thing is ready like so::

    clock.is_ready("superjump")

This will return ``True`` if the ability can be used. If the ability is used,
you can then disable it for the timeout duration you added it with before as
follows::

    def update():
        if keyboard.space and clock.is_ready("superjump"):
            player.vy -= 25
            clock.timeout_ready("superjump")

When you call ``timeout_ready(name)`` the ready timer of the given name will be
set to ``False`` and only be set back to ``True`` once five seconds have passed
in this case.

If you want to add many different things to track, you can either call
``clock.track_ready()`` multiple times or add each ability as a tuple of a name
and the timeout period:
``clock.track_ready(("superjump", 5.0), ("slide", 2.5), ("jump", 0.75))``

Ready timers respect ``clock.timescale`` by default just like all other clock
functionality. To make a run of a ready timer use absolute time instead of
following the time scaling, use the ``absolute=True`` optional keyword
argument::

    if keyboard.space and clock.is_ready("time_magic"):
        do_time_magic()
        clock.timeout_ready("time_magic", absolute=True)

In the example above, maybe time magic changes ``clock.timescale`` but the
cooldown to use it again shouldn't be affected by that, so it is timed out as
``absolute=True`` instead.

After creation, you can check and change the timeout period set for ready
timers with ``clock.get_ready_timeout("name")`` and
``clock.set_ready_timeout("name", 2.0)``. When setting, the second argument is
the new timeout period the ready timer should use.

It's also possible to permanently set a ready timer's ready value, for example
if an ability should be deactivated permanently:
``clock.set_ready("superjump", False)``. At some later point, you either enable
an ability again and set it as ready with ``clock.set_ready("name", True)`` or
you can time it out with ``clock.timeout_ready("name")`` after which it will
be returned to ``True`` automatically.

To get a dictionary of all currently held ready timers with their names as
keys and their ready status as values, use ``clock.get_all_ready()``.
