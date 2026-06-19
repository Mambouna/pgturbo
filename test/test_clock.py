import unittest
from unittest.mock import patch, Mock

from pgturbo.clock import clock, ReadyTimerSystem


class ClockTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global test_func_mock
        clock.clear()
        # This creates a mock function signature where we can check later
        # if it was called.
        test_func_mock = Mock()

    def setUp(self):
        clock._t = 5900.20
        clock._absolute_t = 7900.20
        clock.mark_time("test_mark")
        clock._t = 22100.75
        clock._absolute_t = 24100.75
        clock.mark_time("other_test_mark")
        clock._timescale = 1.0

    def tearDown(self):
        clock._marks = {}
        clock.clear()
        test_func_mock.reset_mock()

    def test_time(self):
        self.assertEqual(clock.time, 22100.75)
        clock.tick(0.05)
        self.assertEqual(clock.time, 22100.80)

    def test_absolute_time(self):
        self.assertEqual(clock.absolute_time, 24100.75)
        clock.tick(0.05)
        self.assertEqual(clock.absolute_time, 24100.80)

    def test_timescale_get(self):
        self.assertEqual(clock.timescale, 1.0)
        clock.timescale = 0.5
        self.assertEqual(clock.timescale, 0.5)

    def test_timescale_down(self):
        clock.timescale = 0.5
        clock.tick(0.05)
        self.assertEqual(clock._timescale, 0.5)
        self.assertEqual(clock.time, 22100.775)

    def test_timescale_up(self):
        clock.timescale = 2.0
        clock.tick(0.05)
        self.assertEqual(clock._timescale, 2.0)
        self.assertEqual(clock.time, 22100.85)

    def test_timescale_pause(self):
        clock.timescale = 0.0
        clock.tick(0.05)
        self.assertEqual(clock._timescale, 0.0)
        self.assertEqual(clock.time, 22100.75)

    def test_timescale_negative_raises_error(self):
        with self.assertRaises(ValueError):
            clock.timescale = -1.0

    def test_absolute_time_unaffected_by_timescale(self):
        clock.timescale = 2.0
        clock.tick(0.05)
        self.assertEqual(clock._timescale, 2.0)
        self.assertEqual(clock.absolute_time, 24100.8)

    def test_mark_time(self):
        self.assertEqual(len(clock._marks), 2)
        clock._t = 500000
        clock._absolute_t = 80000
        clock.mark_time("last_test_mark")
        self.assertEqual(len(clock._marks), 3)
        self.assertEqual(clock._marks["last_test_mark"], (500000, 80000))

    def test_get_mark_time(self):
        self.assertEqual(clock.get_mark_time("test_mark"), 5900.20)
        self.assertEqual(clock.get_mark_time("other_test_mark"), 22100.75)
        self.assertIsNone(clock.get_mark_time("not_a_mark"))

    def test_get_mark_time_absolute(self):
        self.assertEqual(clock.get_mark_time("test_mark", True), 7900.20)
        self.assertEqual(clock.get_mark_time("other_test_mark", True),
                         24100.75)
        self.assertIsNone(clock.get_mark_time("not_a_mark", True))

    def test_time_since_mark(self):
        self.assertEqual(clock.time_since_mark("test_mark"), 16200.55)
        clock.mark_time("test_mark")
        self.assertEqual(clock.time_since_mark("test_mark"), 0)
        self.assertIsNone(clock.time_since_mark("not_a_mark"))

    def test_time_since_mark_absolute(self):
        clock.timescale = 0.1
        clock.tick(1)
        self.assertEqual(clock.time_since_mark("test_mark", True), 16201.55)
        clock.mark_time("test_mark")
        self.assertEqual(clock.time_since_mark("test_mark", True), 0)

    def test_get_all_marks(self):
        compare_dict = {"test_mark": 5900.20, "other_test_mark": 22100.75}
        returned_dict = clock.get_all_marks()
        self.assertEqual(returned_dict, compare_dict)
        # This checks that users can't edit the actual dict in clock but
        # only get a copy back from get_all_marks().
        returned_dict.pop("test_mark")
        self.assertEqual(clock.get_all_marks(), compare_dict)

    def test_get_all_marks_absolute(self):
        compare_dict = {"test_mark": 7900.20, "other_test_mark": 24100.75}
        returned_dict = clock.get_all_marks(True)
        self.assertEqual(returned_dict, compare_dict)
        # This checks that users can't edit the actual dict in clock but
        # only get a copy back from get_all_marks().
        returned_dict.pop("test_mark")
        self.assertEqual(clock.get_all_marks(True), compare_dict)

    @patch("pgturbo.clock.ReadyTimerSystem")
    def test_ready_timer_calls_passed_on(self, rts_mock):
        """Calls to the clocks methods around ready timers are simply passed
        on to its ready timer system."""
        clock._ready_timer_system = rts_mock
        clock.track_ready("jump", 2.0)
        rts_mock.track_ready.assert_called_with("jump", 2.0)
        clock.is_ready("jimp")
        rts_mock.is_ready.assert_called_with("jimp")
        clock.get_ready("jamp")
        rts_mock.is_ready.assert_called_with("jamp")
        clock.timeout_ready("jemp", 3, absolute=True)
        rts_mock.timeout_ready.assert_called_with("jemp", 3, True)
        clock.set_ready("jomp", False)
        rts_mock.set_ready.assert_called_with("jomp", False)
        clock.set_ready_timeout("jaemp", 3.5)
        rts_mock.set_ready_timeout.assert_called_with("jaemp", 3.5)
        clock.get_all_ready()
        rts_mock.get_all_ready.assert_called_once()

    def test_schedule_single_no_args(self):
        """Scheduled functions are called but only after the right amount of
        time."""
        # This creates a mock function signature where we can check later
        # if it was called.
        clock.schedule(test_func_mock, 1.0)
        # The call has been added to the clock events list.
        self.assertEqual(len(clock.events), 1)
        # Not enough time, call should not have been made.
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        # Now enough time has passed that it should have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 0)
        # It should also not have been called multiple times.
        test_func_mock.assert_called_once()

    def test_schedule_single_no_args_absolute(self):
        clock.schedule(test_func_mock, 1.0, absolute=True)
        # The call has been added to the clock events list.
        self.assertEqual(len(clock.events_absolute), 1)
        # Not enough time, call should not have been made.
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        # Now enough time has passed that it should have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 0)
        # It should also not have been called multiple times.
        test_func_mock.assert_called_once()

    def test_schedule_unique_no_args(self):
        """Uniquely scheduled functions delay previous scheduling correctly."""
        clock.schedule(test_func_mock, 1.0)
        self.assertEqual(len(clock.events), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        # Schedule unique should remove the old scheduling, leaving only the
        # new one.
        clock.schedule_unique(test_func_mock, 1.5)
        self.assertEqual(len(clock.events), 1)
        # Since the old event was removed, the function should still not
        # have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        # Only now should it have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 0)
        test_func_mock.assert_called_once()

    def test_schedule_unique_no_args_absolute(self):
        clock.schedule(test_func_mock, 1.0, absolute=True)
        self.assertEqual(len(clock.events_absolute), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        # Schedule unique should remove the old scheduling, leaving only the
        # new one.
        clock.schedule_unique(test_func_mock, 1.5, absolute=True)
        self.assertEqual(len(clock.events_absolute), 1)
        # Since the old event was removed, the function should still not
        # have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        # Only now should it have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 0)
        test_func_mock.assert_called_once()

    def test_schedule_interval_no_args(self):
        """Scheduling with an interval keeps the event in the queue and calls
        repeatedly."""
        clock.schedule_interval(test_func_mock, 1.0)
        self.assertEqual(len(clock.events), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        # Here we should have gotten the first call.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_called_once()
        # Another call.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        self.assertEqual(test_func_mock.call_count, 2)
        # Another call.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        self.assertEqual(test_func_mock.call_count, 3)

    def test_schedule_interval_no_args_absolute(self):
        clock.schedule_interval(test_func_mock, 1.0, absolute=True)
        self.assertEqual(len(clock.events_absolute), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        # Here we should have gotten the first call.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_called_once()
        # Another call.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        self.assertEqual(test_func_mock.call_count, 2)
        # Another call.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        self.assertEqual(test_func_mock.call_count, 3)

    def test_schedule_single_with_args(self):
        """Simple scheduling works with supplied arguments."""
        clock.schedule(test_func_mock, 1.0, 42, "test", kword="test")
        self.assertEqual(len(clock.events), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 0)
        test_func_mock.assert_called_once_with(42, "test", kword="test")

    def test_schedule_single_with_args_absolute(self):
        clock.schedule(test_func_mock, 1.0, 42, "test", kword="test",
                       absolute=True)
        self.assertEqual(len(clock.events_absolute), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 0)
        test_func_mock.assert_called_once_with(42, "test", kword="test")

    def test_schedule_unique_with_args(self):
        """Uniquely scheduled functions delay previous scheduling correctly
        and different arguments don't intersect when rescheduling."""
        clock.schedule(test_func_mock, 1.0, 42, "test", kword="test")
        self.assertEqual(len(clock.events), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        # This should not remove the old call because the supplied args differ.
        clock.schedule_unique(test_func_mock, 5.0)
        self.assertEqual(len(clock.events), 2)
        # This should reschedule however.
        clock.schedule_unique(test_func_mock, 1.5, 42, "test", kword="test")
        self.assertEqual(len(clock.events), 2)
        # Since the old event was removed, the function should still not
        # have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 2)
        test_func_mock.assert_not_called()
        # Only now should it have been called with the other call remaining.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_called_once_with(42, "test", kword="test")
        clock.tick(10.0)
        self.assertEqual(len(clock.events), 0)
        # The last call should have been without arguments.
        test_func_mock.assert_called_with()
        # In total two calls should have happened.
        self.assertEqual(test_func_mock.call_count, 2)

    def test_schedule_unique_with_args_absolute(self):
        clock.schedule(test_func_mock, 1.0, 42, "test", kword="test",
                       absolute=True)
        self.assertEqual(len(clock.events_absolute), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        # This should not remove the old call because the supplied args differ.
        clock.schedule_unique(test_func_mock, 5.0, absolute=True)
        self.assertEqual(len(clock.events_absolute), 2)
        # This should reschedule however.
        clock.schedule_unique(test_func_mock, 1.5, 42, "test", kword="test",
                              absolute=True)
        self.assertEqual(len(clock.events_absolute), 2)
        # Since the old event was removed, the function should still not
        # have been called.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 2)
        test_func_mock.assert_not_called()
        # Only now should it have been called with the other call remaining.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_called_once_with(42, "test", kword="test")
        clock.tick(10.0)
        self.assertEqual(len(clock.events_absolute), 0)
        # The last call should have been without arguments.
        test_func_mock.assert_called_with()
        # In total two calls should have happened.
        self.assertEqual(test_func_mock.call_count, 2)

    def test_schedule_interval_with_args(self):
        """Interval scheduling also works with arguments."""
        clock.schedule_interval(test_func_mock, 1.0, 42, "test", kword="test")
        self.assertEqual(len(clock.events), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_called_once_with(42, "test", kword="test")
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        self.assertEqual(test_func_mock.call_count, 2)
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        self.assertEqual(test_func_mock.call_count, 3)

    def test_schedule_interval_with_args_absolute(self):
        clock.schedule_interval(test_func_mock, 1.0, 42, "test", kword="test",
                                absolute=True)
        self.assertEqual(len(clock.events_absolute), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_called_once_with(42, "test", kword="test")
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        self.assertEqual(test_func_mock.call_count, 2)
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        self.assertEqual(test_func_mock.call_count, 3)

    def test_unschedule_no_args(self):
        """Scheduled events can be removed from the queue."""
        clock.schedule(test_func_mock, 1.0)
        self.assertEqual(len(clock.events), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_not_called()
        clock.unschedule(test_func_mock)
        # No calls should have been made since it was unscheduled.
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 0)
        test_func_mock.assert_not_called()

    def test_unschedule_no_args_absolute(self):
        clock.schedule(test_func_mock, 1.0, absolute=True)
        self.assertEqual(len(clock.events_absolute), 1)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_not_called()
        clock.unschedule(test_func_mock, absolute=True)
        # No calls should have been made since it was unscheduled.
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 0)
        test_func_mock.assert_not_called()

    def test_unschedule_with_args(self):
        """Scheduled events can be removed from the queue."""
        clock.schedule(test_func_mock, 1.0, 42, "test", kword="test")
        clock.schedule(test_func_mock, 2.0, 42, "test", kword="test")
        self.assertEqual(len(clock.events), 2)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 2)
        test_func_mock.assert_not_called()
        # This does not unschedule the calls because of the difference
        # in supplied arguments.
        clock.unschedule(test_func_mock)
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 1)
        test_func_mock.assert_called_once_with(42, "test", kword="test")
        # This unschedules the remaining call because the arguments match.
        clock.unschedule(test_func_mock, 42, "test", kword="test")
        clock.tick(1.0)
        self.assertEqual(len(clock.events), 0)
        self.assertEqual(test_func_mock.call_count, 1)

    def test_unschedule_with_args_absolute(self):
        clock.schedule(test_func_mock, 1.0, 42, "test", kword="test",
                       absolute=True)
        clock.schedule(test_func_mock, 2.0, 42, "test", kword="test",
                       absolute=True)
        self.assertEqual(len(clock.events_absolute), 2)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 2)
        test_func_mock.assert_not_called()
        # This does not unschedule the calls because of the difference
        # in supplied arguments.
        clock.unschedule(test_func_mock, absolute=True)
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 1)
        test_func_mock.assert_called_once_with(42, "test", kword="test")
        # This unschedules the remaining call because the arguments match.
        clock.unschedule(test_func_mock, 42, "test", kword="test",
                         absolute=True)
        clock.tick(1.0)
        self.assertEqual(len(clock.events_absolute), 0)
        self.assertEqual(test_func_mock.call_count, 1)

    def test_events_and_absolute_events_dont_conflict(self):
        """Scheduling events non-absolute and absolute does not conflict with
        each other."""
        test_func_mock_two = Mock()
        # We add one event each to the timescale affected queue and the
        # absolute one.
        clock.schedule(test_func_mock, 1.0)
        clock.schedule(test_func_mock_two, 1.0, absolute=True)
        self.assertEqual(len(clock.events), 1)
        self.assertEqual(len(clock.events_absolute), 1)
        # With half timespeed, only the absolute event should have been called
        # after one second of real time.
        clock.timescale = 0.5
        clock.tick(1.0)
        test_func_mock.assert_not_called()
        test_func_mock_two.assert_called_once()
        clock.tick(1.0)
        test_func_mock.assert_called_once()
        # We schedule the same events again to test unscheduling.
        clock.timescale = 1.0
        clock.schedule(test_func_mock, 1.0)
        clock.schedule(test_func_mock_two, 1.0, absolute=True)
        clock.tick(0.5)
        # This should leave the absolute scheduled event untouched.
        clock.unschedule(test_func_mock)
        clock.unschedule(test_func_mock_two)
        self.assertEqual(len(clock.events), 0)
        self.assertEqual(len(clock.events_absolute), 1)
        clock.clear()
        # Same check but the other way around.
        clock.schedule(test_func_mock, 1.0)
        clock.schedule(test_func_mock_two, 1.0, absolute=True)
        clock.unschedule(test_func_mock, absolute=True)
        clock.unschedule(test_func_mock_two, absolute=True)
        self.assertEqual(len(clock.events), 1)
        self.assertEqual(len(clock.events_absolute), 0)

    def test_unschedule_all(self):
        """Unschedule all removes callbacks regardless of their args."""
        clock.schedule(test_func_mock, 1.0)
        clock.schedule(test_func_mock, 2.0, 42, "test", kword="test")
        self.assertEqual(len(clock.events), 2)
        clock.tick(0.5)
        self.assertEqual(len(clock.events), 2)
        test_func_mock.assert_not_called()
        # This should remove both scheduled calls.
        clock.unschedule_all(test_func_mock)
        self.assertEqual(len(clock.events), 0)
        clock.tick(2.0)
        test_func_mock.assert_not_called()

    def test_unschedule_all_absolute(self):
        clock.schedule(test_func_mock, 1.0, absolute=True)
        clock.schedule(test_func_mock, 2.0, 42, "test", kword="test",
                       absolute=True)
        self.assertEqual(len(clock.events_absolute), 2)
        clock.tick(0.5)
        self.assertEqual(len(clock.events_absolute), 2)
        test_func_mock.assert_not_called()
        # This should remove both scheduled calls.
        clock.unschedule_all(test_func_mock, absolute=True)
        self.assertEqual(len(clock.events_absolute), 0)
        clock.tick(2.0)
        test_func_mock.assert_not_called()


class ReadyTimerSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global test_func_mock, rts
        clock.clear()
        # This creates a mock function signature where we can check later
        # if it was called.
        test_func_mock = Mock()
        rts = ReadyTimerSystem()

    def setUp(self):
        rts._clear()
        clock.clear()
        clock.timescale = 1.0
        test_func_mock.reset_mock()

    def test_track_ready_timer_single_two_values(self):
        """We can add timers to countdown later with two individual values."""
        rts.track_ready("jump", 2.0)
        self.assertEqual(len(rts._ready_timers), 1)

    def test_track_ready_timer_single_one_tuple(self):
        """We can add timers to countdown later with one tuple."""
        rts.track_ready(("jump", 2))
        self.assertEqual(len(rts._ready_timers), 1)

    def test_track_ready_timer_multiple(self):
        """We can add multiple timers at the same time to countdown later with
        tuples or lists."""
        rts.track_ready(("jump", 2.0), ["double_jump", 1])
        self.assertEqual(len(rts._ready_timers), 2)

    def test_track_ready_timer_errors_with_wrong_args(self):
        """Trying to add timers with other types or values errors."""
        with self.assertRaises(TypeError):
            rts.track_ready("jump")
        with self.assertRaises(TypeError):
            rts.track_ready("jump", 2, "double_jump", 1)
        with self.assertRaises(TypeError):
            rts.track_ready(("jump", 2), ("double_jump", 1, True))

    def test_track_ready_timer_same_name_errors(self):
        """Trying to add a new timer with an existing name errors."""
        rts.track_ready("jump", 2)
        with self.assertRaises(KeyError):
            rts.track_ready("jump", 2)

    def test_is_ready_timer_ready(self):
        """We can see if a timer is currently ready (not running down)."""
        rts.track_ready("jump", 2)
        self.assertTrue(rts.is_ready("jump"))

    def test_is_ready_timer_ready_alias(self):
        """We can also use get_ready for the same purpose."""
        rts.track_ready("jump", 2)
        self.assertTrue(rts.get_ready("jump"))

    def test_is_ready_timer_ready_errors_with_wrong_name(self):
        """If a name is checked that doesn't exist, an error is thrown."""
        rts.track_ready("jump", 2)
        with self.assertRaises(KeyError):
            rts.is_ready("double_jump")

    def test_timeout_ready_timer(self):
        """We can run the ready timer which first disables and then enables it
        again after the timeout period."""
        rts.track_ready("jump", 2.0)
        self.assertTrue(rts.is_ready("jump"))
        rts.timeout_ready("jump")
        clock.tick(1)
        self.assertFalse(rts.is_ready("jump"))
        clock.tick(1)
        self.assertTrue(rts.is_ready("jump"))

    def test_timeout_ready_timer_with_time_override(self):
        """We can override the normal timeout period when unreadying a
        timer."""
        rts.track_ready("jump", 2.0)
        self.assertTrue(rts.is_ready("jump"))
        rts.timeout_ready("jump", 3.0)
        clock.tick(2.5)
        self.assertFalse(rts.is_ready("jump"))
        clock.tick(1)
        self.assertTrue(rts.is_ready("jump"))

    def test_timeout_ready_timer_with_time_override_wrong_value_errors(self):
        """If a wrong kind of value is given for the time override, an error
        is thrown."""
        rts.track_ready("jump", 2.0)
        with self.assertRaises(TypeError):
            rts.timeout_ready("jump", "five seconds")

    def test_timeout_ready_timer_affected_by_timescale(self):
        """Running the timeout normally means its affected by timescale."""
        rts.track_ready("jump", 2.0)
        self.assertTrue(rts._ready_timers["jump"].ready)
        clock.timescale = 0.5
        rts.timeout_ready("jump")
        clock.tick(1)
        self.assertFalse(rts._ready_timers["jump"].ready)
        clock.tick(1)
        self.assertFalse(rts._ready_timers["jump"].ready)
        clock.tick(2)
        self.assertTrue(rts._ready_timers["jump"].ready)

    def test_timeout_ready_timer_absolute_unaffected_by_timescale(self):
        """If we run the timeout with absolute=True instead, timescale is
        ignored."""
        rts.track_ready("jump", 2.0)
        self.assertTrue(rts._ready_timers["jump"].ready)
        clock.timescale = 0.5
        rts.timeout_ready("jump", absolute=True)
        clock.tick(1)
        self.assertFalse(rts._ready_timers["jump"].ready)
        clock.tick(1)
        self.assertTrue(rts._ready_timers["jump"].ready)

    def test_set_ready_timer(self):
        """We can permanently set the ready value of a ready timer."""
        rts.track_ready("jump", 2.0)
        self.assertTrue(rts._ready_timers["jump"].ready)
        rts.set_ready("jump", False)
        self.assertFalse(rts._ready_timers["jump"].ready)

    def test_set_ready_timer_wrong_value_errors(self):
        """If a non-boolean is given, throw a descriptive error."""
        rts.track_ready("jump", 2.0)
        with self.assertRaises(TypeError):
            rts.set_ready("jump", "true")

    def test_set_ready_timer_timeout(self):
        """We can change the timeout value of a ready timer."""
        rts.track_ready("jump", 2.0)
        self.assertEqual(rts._ready_timers["jump"].timeout, 2.0)
        rts.set_ready_timeout("jump", 3.0)
        self.assertEqual(rts._ready_timers["jump"].timeout, 3.0)

    def test_set_ready_timer_timeout_wrong_value_errors(self):
        """If the wrong type of value is given, throw an error."""
        rts.track_ready("jump", 2.0)
        with self.assertRaises(TypeError):
            rts.set_ready_timeout("jump", True)

    def test_get_all_ready_timers(self):
        """We can get the ready state of all ready timers at once."""
        rts.track_ready("jump", 2.0)
        rts.track_ready("double_jump", 1.0)
        compare_dict = {"jump": False, "double_jump": True}
        rts.timeout_ready("jump")
        clock.tick(1)
        self.assertEqual(rts.get_all_ready(), compare_dict)
        clock.tick(1)
        compare_dict["jump"] = True
        self.assertEqual(rts.get_all_ready(), compare_dict)
