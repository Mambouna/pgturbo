.. _reference_clock:

Reference: clock
=================

:ref:`Deep dive on the clock builtin <deep_dive_clock>`


.. _reference_clock_attributes:

Attributes
----------

.. attribute:: time

    Returns the elapsed time since program start in seconds while respecting
    timescale changes.

    Cannot be set by the user.

.. attribute:: absolute_time

    Returns the elapsed time since program start in seconds without respecting
    timescale changes.

    This always returns the actual second count since program start.

    Cannot be set by the user.

.. attribute:: timescale

    Controls the speed at which time is counted for the ``time`` property and
    all other ``clock`` functionality. Can be set to change how fast game time
    flows.

    ``1.0`` is normal game time, values above will increase the speed while
    values between 0 and 1 slow the timing down. ``0.0`` will pause the
    time counting. This can be used to pause the game when set up
    correctly.

    Note that you will have to make all game mechanics other that ``clock``
    functions respect changes in game time speed yourself manually.

    Default value: ``1.0``


.. _reference_clock_methods:

Methods
-------


.. _reference_clock_scheduling:

.. method:: schedule(callback, delay, *args, **kwargs)

    .. Comment to disable wrong syntax highlighting from the stars.**

    Schedule `callback` to be called after the given delay.

    Repeated calls will schedule the callback repeatedly.

    Calling with ``absolute=True`` will schedule the callback such that it
    will not be affected by timescale.

    Any other further arguments will be passed on to the called function. The
    following example calls a function on an actor after one second and passes
    on the value ``(40, 60)`` as a positional argument to ``alien.teleport()``.

    Example: ``clock.schedule(alien.teleport, 1.0, (40, 60))``

    :param callback: A callable (usually a function you wrote).
    :param delay: The delay, in seconds, before the function should be
                  called.
    :param args: Any further arguments will be given to callback as
                 positional arguments when called.
    :param kwargs: Any further named arguments will be given to callback
                   as keyword arguments when called.

                   Note that the keyword `absolute` is reserved and won't
                   be passed on.

.. method:: schedule_unique(callback, delay, *args, **kwargs)

    .. Comment to disable wrong syntax highlighting from the stars.**

    Schedule `callback` to be called once after the given delay.

    If `callback` was already scheduled, cancel and reschedule it. This
    applies also if it was scheduled multiple times: after calling
    ``schedule_unique``, it will be scheduled exactly once.

    Calling with ``absolute=True`` will schedule the callback such that it
    will not be affected by timescale.

    Just like ``schedule()``, any other arguments are passed on to `callable`.

    :param callback: A callable (usually a function you wrote).
    :param delay: The delay, in seconds, before the function should be
                  called.
    :param args: Any further arguments will be given to callback as
                 positional arguments when called.
    :param kwargs: Any further named arguments will be given to callback
                   as keyword arguments when called.

                   Note that the keyword `absolute` is reserved and won't
                   be passed on.

.. method:: schedule_interval(callback, interval, *args, **kwargs)

    .. Comment to disable wrong syntax highlighting from the stars.**

    Schedule `callback` to be called repeatedly with a set period of `interval`
    between the calls. To stop the repeating calls, use ``unschedule()``.

    Calling with ``absolute=True`` will schedule the callback such that it
    will not be affected by timescale.

    Just like ``schedule()``, any other arguments are passed on to `callable`.

    :param callback: A callable (usually a function you wrote).
    :param interval: The interval in seconds between calls to `callback`.
    :param args: Any further arguments will be given to callback as
                 positional arguments when called.
    :param kwargs: Any further named arguments will be given to callback
                   as keyword arguments when called.

                   Note that the keyword `absolute` is reserved and won't
                   be passed on.

.. method:: unschedule(callback, *args, **kwargs)

    .. Comment to disable wrong syntax highlighting from the stars.**

    Unschedule only the callback with the given arguments if it has
    been previously scheduled (either because it had been scheduled with
    ``schedule()`` and has not yet been called, or because it had been
    scheduled to repeat with ``schedule_interval()``.

    This means that if you scheduled ``set_gem_color`` with ``"red"`` and
    ``"blue"`` for separate delays before and then call
    ``clock.unschedule(set_gem_color, "red")`` only the call with ``"red"``
    as an argument will be unscheduled.

    Calling with ``absolute=True`` will unschedule calls that were registered
    to follow the absolute time without respecting timescale.

    :param callback: A callable (usually a function you wrote).
    :param args: Any further arguments will be used to identify which
                 specific scheduled call to remove.
    :param kwargs: Any further named arguments will be used to identify
                   which specific scheduled call to remove.

                   Note that the keyword `absolute` is reserved and won't
                   be passed on.

.. method:: unschedule_all(callback, [absolute])

    Unschedule all calls of the given callback, ignoring any arguments
    supplied to them.

    This means that if you scheduled ``set_gem_color`` with ``"red"`` and
    ``"blue"`` for separate delays before, both will be unscheduled.

    Calling with ``absolute=True`` will unschedule calls that were registered
    to follow the absolute time without respecting timescale.

    :param callback: A callable (usually a function you wrote).
    :param absolute: Boolean of whether to unschedule the callbacks in the
                     absolute time event queue or the other one. Default is
                     ``False``.

*Note:* The Pygame Turbo clock only holds weak references to each callback
you give it. It will not fire scheduled events if the objects and methods are
not referenced elsewhere. This can help prevent the clock keeping objects
alive and continuing to fire unexpectedly after they are otherwise dead.

The downside to the weak references is that you won't be able to schedule
lambdas or any other object that has been created purely to be scheduled. You
will have to keep a reference to the object.


.. _reference_clock_time_marks:

.. method:: mark_time(name)

    Creates a record of the current elapsed time and saves it with the
    given `name`. Use this to save when something happened in the game.
    Calling the function again overwrites the previous timestamp with the
    new one.

    Both the absolute timestamp and the one affected by timescale are saved.

    :param name: A string name for the time mark.

.. method:: get_mark_time(name, [absolute])

    Returns the timestamp that was saved under `name`. If the mark does
    not exist (yet), returns ``None`` instead.

    :param name: A string name for the time mark.
    :param absolute: Optional boolean of whether to return the absolute
                     timestamp instead of the one affected by timescale.
                     Default is ``False``.

.. method:: time_since_mark(name, [absolute])

    Returns the time elapsed since the mark `name` was created. If the
    mark does not exist (yet), returns ``None`` instead.

    :param name: A string name for the time mark.
    :param absolute: Optional boolean of whether to return the absolute time
                     since the mark was created instead of the one affected by
                     timescale. Default is ``False``.

.. method:: get_all_marks([absolute])

    Returns a dictionary of all currently saved marks and their timestamps.
    Note that changing this dictionary does not affect the underlying data
    in clock.

    :param absolute: Boolean of whether to return all the absolute
                     timestamps instead of the ones affected by timescale.
                     Default is ``False``.


.. _reference_clock_ready_timers:

.. method:: track_ready(*args)

    .. Comment to disable wrong syntax highlighting from the star.*

    Adds one or multiple ready timers that the clock can report as ready and
    time out. If given one string and one number, a single ready timer is
    added. The string is the name for the ready timer and the number the
    timeout period in seconds.

    To add multiple timers with one call, give one tuple per timer as arguments
    where each tuple contains one string and one number.

    Example: ``clock.track_ready(("jump", 0.6), ("powerup", 2.5))``

    :param args: Argument sink to turn into one or more added ready timers.

.. method:: is_ready(name)

    Returns ``True`` if the given timer is currently ready or ``False`` if
    not.

    :param name: Name of the ready timer to check.

.. method:: timeout_ready(name, [time, absolute])

    Set a ready timer to ``False`` for the duration of its set timeout
    period, after which it will be returned to ``True`` again.

    :param name: The name of the ready timer to time out.
    :param time: An override for how long the timer should remain
                 ``False``. Give a number to use a timeout period other
                 than the default set for the ready timer.
    :param absolute: Optional boolean of whether the timeout period should be
                     tracked in absolute time or time affected by timescale.
                     Default is ``False``, meaning timescale affects the timer.

.. method:: set_ready(name, value)

    Set the ready value of a ready timer manually and permanently. This
    could be used to disable an ability in general based on some state.
    Calling ``timeout_ready()`` will still set the timer back to ready
    after the timeout period.

    :param name: What timer to change the ready value on.
    :param value: Boolean of whether the ready timer should be permanently
                  ready (``True``) or not (``False``) until a timeout is
                  triggered.

.. method:: get_ready_timeout(name)

    Returns the current timeout period set for a ready timer.

    :param name: String for which timer to get the timeout period of.

.. method:: set_ready_timeout(name, value)

    Set the timeout period for the given ready timer. Doesn't affect a
    timeout that is already running.

    :param name: The timer for which to change the timeout period.
    :param value: Number value for the seconds the timeout period should
                  last.

.. method:: get_all_ready()

    Returns a dictionary of all ready timers with their names as keys and
    their ready state as values.

    Changing the data in this dictionary does not change anything about the
    ready timers kept by ``clock``.


.. _reference_clock_changelog:

Changelog
---------

* **1.10** Added absolute timeframe options and ready timers.
* **1.7:** Allow scheduling functions with arguments.
* **1.6:** Added timescale property.
* **1.4:** First release of PGTurbo after fork from PGZero.
