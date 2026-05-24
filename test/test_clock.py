import unittest

import pgturbo.clock as clock


class ClockTest(unittest.TestCase):
    def setUp(self):
        clock.clock.t = 5900.20
        clock.mark_time("test_mark")

    def tearDown(self):
        clock.clock._marks = {}

    def test_time(self):
        self.assertEqual(clock.time(), 5900.20)

    def test_mark_time(self):
        clock.clock.t = 22100.75
        clock.mark_time("other_test_mark")
        self.assertEqual(len(clock.clock._marks), 2)
        self.assertIn("test_mark", clock.clock._marks)
        self.assertIn("other_test_mark", clock.clock._marks)
        self.assertEqual(clock.clock._marks["other_test_mark"], 22100.75)

    def test_get_mark_time(self):
        self.assertEqual(clock.get_mark_time("test_mark"), 5900.20)

    def test_time_since_mark(self):
        clock.clock.t = 22100.75
        self.assertEqual(clock.time_since_mark("test_mark"), 16200.55)
