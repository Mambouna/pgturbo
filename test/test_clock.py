import unittest

import pgturbo.clock as clock


class ClockTest(unittest.TestCase):
    def setUp(self):
        clock.clock.t = 5900.20
        clock.mark_time("test_mark")
        clock.clock.t = 22100.75
        clock.mark_time("other_test_mark")

    def tearDown(self):
        clock.clock._marks = {}

    def test_time(self):
        self.assertEqual(clock.time(), 22100.75)

    def test_mark_time(self):
        self.assertEqual(len(clock.clock._marks), 2)
        clock.clock.t = 500000
        clock.mark_time("last_test_mark")
        self.assertEqual(len(clock.clock._marks), 3)
        self.assertEqual(clock.clock._marks["last_test_mark"], 500000)

    def test_get_mark_time(self):
        self.assertEqual(clock.get_mark_time("test_mark"), 5900.20)
        self.assertEqual(clock.get_mark_time("other_test_mark"), 22100.75)

    def test_time_since_mark(self):
        self.assertEqual(clock.time_since_mark("test_mark"), 16200.55)

    def test_get_all_marks(self):
        compare_dict = {"test_mark": 5900.20, "other_test_mark": 22100.75}
        returned_dict = clock.get_all_marks()
        self.assertEqual(returned_dict, compare_dict)
        # This checks that users can't edit the actual dict in clock but
        # only get a copy back from get_all_marks().
        returned_dict.pop("test_mark")
        self.assertEqual(clock.get_all_marks(), compare_dict)
