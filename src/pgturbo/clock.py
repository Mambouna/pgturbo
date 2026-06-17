"""Clock/event scheduler.

This is a Pygame implementation of a scheduler inspired by the clock
classes in Pyglet.

"""
import heapq
from weakref import ref
from functools import total_ordering
from inspect import signature
from types import MethodType

__all__ = [
    'Clock', 'schedule', 'schedule_interval', 'unschedule'
]

# This type can't be weakreffed in Python 3.4
builtin_function_or_method = type(open)


def weak_method(method):
    """Quick weak method ref in case users aren't using Python 3.4"""
    selfref = ref(method.__self__)
    funcref = ref(method.__func__)

    def weakref():
        self = selfref()
        func = funcref()
        if self is None or func is None:
            return None
        return func.__get__(self)
    return weakref


def mkref(o):
    if isinstance(o, MethodType):
        return weak_method(o)
    else:
        try:
            return ref(o)
        except TypeError:
            if isinstance(o, builtin_function_or_method):
                return lambda: o
            raise


class ReadyTimer:
    """Very small helper class for timer objects."""

    def __init__(self, name, timeout):
        self.name = name
        self.timeout = timeout
        self.ready = True


@total_ordering
class Event:
    """An event scheduled for a future time.

    Events are ordered by their scheduled execution time.

    """

    def __init__(self, time, cb, repeat=None, *args, **kwargs):
        self.time = time
        self.repeat = repeat
        self.cb = mkref(cb)
        # This function signature allows us to ensure invalid arguments
        # are immediately detected and rejected before the function is called.
        self.cb_signature = signature(cb)
        self.bound = self.cb_signature.bind(*args, **kwargs)
        self.bound.apply_defaults()
        self.name = str(cb)
        self.repeat = repeat

    def __lt__(self, ano):
        return self.time < ano.time

    def __eq__(self, ano):
        return self.time == ano.time

    @property
    def callback(self):
        return self.cb()


class Clock:
    """A clock used for event scheduling.

    When tick() is called, all events scheduled for before now will be called
    in order.

    tick() would typically be called from the game loop for the default clock.

    Additional clocks could be created - for example, a game clock that could
    be suspended in pause screens. Your code must take care of calling tick()
    or not. You could also run the clock at a different rate if desired, by
    scaling dt before passing it to tick().

    """

    def __init__(self):
        self._t = 0
        self._absolute_t = 0
        self.fired = False
        self.events = []
        self.events_absolute = []
        self._each_tick = []
        self._marks = {}
        self._ready_timers = {}
        self._timescale = 1.0

    @property
    def time(self):
        """Simple property to return the total elapsed time affected by
        pauses."""
        return self._t

    @property
    def absolute_time(self):
        """Returns the elapsed time without respecting timescale changes."""
        return self._absolute_t

    @property
    def timescale(self):
        return self._timescale

    @timescale.setter
    def timescale(self, value):
        """Property to control how fast the user facing clock is running."""
        if not isinstance(value, (int, float)):
            raise TypeError("Timescale must be of type int or float, not "
                            "{}.".format(type(value)))
        elif value < 0:
            raise ValueError("Timescale values must not be negative. You set "
                             "it to {}.".format(value))
        self._timescale = value

    def mark_time(self, name):
        """Save a timestamp with a name for later."""
        self._marks[name] = (self._t, self._absolute_t)

    def get_mark_time(self, name, absolute=False):
        """Get the time saved with a mark name or return None if it doesn't
        exist."""
        mark = self._marks.get(name)
        if mark:
            return mark[1] if absolute else mark[0]
        return None

    def time_since_mark(self, name, absolute=False):
        """Get the elapsed time since a mark was made or return None if it
        doesn't exist."""
        m = self._marks.get(name)
        if m:
            return self._absolute_t - m[1] if absolute else self._t - m[0]
        return None

    def get_all_marks(self, absolute=False):
        """Return a copy of the current state of the marks dictionary. A copy
        is made to make sure users don't accidentally change the contents of
        the actual marks dict."""
        i = 1 if absolute else 0
        return {k: v[i] for k, v in self._marks.items()}

    def _add_ready_timer_internal(self, name, timeout):
        """Helper function to add a ready timer or error if one with the name
        exists."""
        if name not in self._ready_timers:
            self._ready_timers[name] = ReadyTimer(name, timeout)
        else:
            raise KeyError("A timer with name {} already "
                           "exists.".format(name))

    def track_ready(self, *args):
        """Adds every argument as a tracked countdown. Each argument should be
        a tuple of a string and a number in seconds. If there are two args
        and the first is a string and the second is a number, that is used
        for one ready timer."""
        match args:
            # If we get two args exactly how we need them, add one timer.
            case (str(name), float(timeout) | int(timeout)):
                self._add_ready_timer_internal(name, timeout)
            # Otherwise we have to deal with the individual items.
            case _:
                for arg in args:
                    match arg:
                        # Same thing, if the format is right, add it.
                        case (str(name), float(timeout) | int(timeout)):
                            self._add_ready_timer_internal(name, timeout)
                        # Otherwise, error.
                        case _:
                            raise TypeError("Ready timers must be given as "
                                            "tuples of a string and a number. "
                                            "You gave: {}".format(arg))

    def _check_ready_timer_name(self, name):
        if name not in self._ready_timers:
            raise KeyError("No ready timer with the name {} exists. These are "
                           "the current ready timer names: {}"
                           .format(name, ", ".join(self._ready_timers.keys())))

    def is_ready(self, name):
        """Returns whether a ready timer is currently ready (is not currently
        running down)."""
        self._check_ready_timer_name(name)
        return self._ready_timers[name].ready

    get_ready = is_ready

    def _set_ready(self, name, value):
        """Internal function that actually sets the ready value of a timer."""
        # Since it's not userfacing, we don't check the name is valid.
        self._ready_timers[name].ready = value

    def timeout_ready(self, name, absolute=False):
        """Set the timer ready to False and only set it back after the
        timeout."""
        self._check_ready_timer_name(name)
        timer = self._ready_timers[name]
        timer.ready = False
        self.schedule_unique(self._set_ready, timer.timeout, name, True,
                             absolute=absolute)

    def set_ready(self, name, value):
        """Userfacing version of _set_ready(). The reason we have both is so
        that if the user unschedules their own set_ready calls it won't affect
        the internal ones."""
        self._check_ready_timer_name(name)
        self._ready_timers[name].ready = value

    def clear(self):
        """Remove all handlers from this clock and clears the marks."""
        self.events.clear()
        self.events_absolute.clear()
        self._marks = {}
        self._ready_timers = {}
        self._each_tick.clear()

    def schedule(self, callback, delay, *args, **kwargs):
        """Schedule callback to be called once, at `delay` seconds from now.

        :param callback: A parameterless callable to be called.
        :param delay: The delay before the call (in clock time / seconds).
        """
        absolute = kwargs.pop("absolute", False)
        if absolute:
            event_list = self.events_absolute
            timestamp = self._absolute_t
        else:
            event_list = self.events
            timestamp = self._t

        heapq.heappush(event_list, Event(timestamp + delay, callback, None,
                                         *args, **kwargs))

    def schedule_unique(self, callback, delay, *args, **kwargs):
        """Schedule callback to be called once, at `delay` seconds from now.

        If it was already scheduled, postpone its firing.

        :param callback: A parameterless callable to be called.
        :param delay: The delay before the call (in clock time / seconds).

        """
        self.unschedule(callback, *args, **kwargs)
        self.schedule(callback, delay, *args, **kwargs)

    def schedule_interval(self, callback, delay, *args, **kwargs):
        """Schedule callback to be called every `delay` seconds.

        The first occurrence will be after `delay` seconds.

        :param callback: A parameterless callable to be called.
        :param delay: The interval in seconds.

        """
        absolute = kwargs.pop("absolute", False)
        if absolute:
            event_list = self.events_absolute
            timestamp = self._absolute_t
        else:
            event_list = self.events
            timestamp = self._t

        heapq.heappush(event_list, Event(timestamp + delay, callback, delay,
                                         *args, **kwargs))

    def _internal_unschedule(self, callback, with_args, *args, **kwargs):
        """Unschedule callbacks either with specified arguments or all
        of the same callback regardsless of params.

        If scheduled multiple times all instances will be unscheduled.
        """
        absolute = kwargs.pop("absolute", False)

        # Reference the same object as whichever event queue we want to edit.
        event_list = self.events_absolute if absolute else self.events
        # By using event_list[:] = we update the existing list object instead
        # of creating a new one and assigning it. This ensures we modify
        # whatever self.events or self.events_absolute are pointing to.
        event_list[:] = [
            e for e in event_list
            if e.callback is not None
            if (with_args and not (e.callback == callback
                                   and e.bound.args == args
                                   and e.bound.kwargs == kwargs)
                ) or (not with_args and e.callback != callback)
        ]
        heapq.heapify(event_list)

        self._each_tick = [e for e in self._each_tick if e() != callback]

    def unschedule(self, callback, *args, **kwargs):
        """Unschedule a callback with specified arguments."""
        self._internal_unschedule(callback, True, *args, **kwargs)

    def unschedule_all(self, callback, absolute=False):
        """Unschedule all callbacks of the same function regardless of their
        specified arguments."""
        self._internal_unschedule(callback, False, absolute=absolute)

    def each_tick(self, callback):
        """Schedule a callback to be called every tick.

        Unlike the standard scheduler functions, the callable is passed the
        elapsed clock time since the last call (the same value passed to tick).

        """
        self._each_tick.append(mkref(callback))

    def _fire_each_tick(self, dt):
        dead = [None]
        for r in self._each_tick:
            cb = r()
            if cb is not None:
                self.fired = True
                try:
                    cb(dt)
                except Exception:
                    import traceback
                    traceback.print_exc()
                    dead.append(cb)
        self._each_tick = [e for e in self._each_tick if e() not in dead]

    def _work_through_events(self, event_list, absolute):
        """Helper function that iterates through and triggers any necessary
        events from one of the two queues."""
        t = self._absolute_t if absolute else self._t
        while event_list and event_list[0].time <= t:
            ev = heapq.heappop(event_list)
            cb = ev.callback
            if not cb:
                continue

            if ev.repeat is not None:
                self.schedule_interval(cb, ev.repeat, absolute=absolute)

            self.fired = True
            try:
                cb(*ev.bound.args, **ev.bound.kwargs)
            except Exception:
                import traceback
                traceback.print_exc()
                self.unschedule(cb, absolute=absolute)

    def tick(self, dt):
        """Update the clock time and fire all scheduled events.

        :param dt: The elapsed time in seconds.

        """
        self.fired = False
        self._t += float(dt) * self._timescale
        self._absolute_t += float(dt)
        self._fire_each_tick(dt)

        self._work_through_events(self.events, False)
        self._work_through_events(self.events_absolute, True)


# One instance of a clock is available by default, to simplify the API
clock = Clock()
tick = clock.tick
schedule = clock.schedule
schedule_interval = clock.schedule_interval
schedule_unique = clock.schedule_unique
unschedule = clock.unschedule
each_tick = clock.each_tick
