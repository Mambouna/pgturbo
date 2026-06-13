import unittest
from unittest.mock import Mock

import pygame

from pgturbo.actor import Actor
from pgturbo.loaders import set_root
from pgturbo.clock import clock


TEST_MODULE = "pgturbo.actor_animation"
TEST_DISP_W, TEST_DISP_H = (200, 100)


# Helper function since we have to call clock.tick() many times to advance
# frames in this test file.
def multitick(dt, num):
    for _ in range(num):
        clock.tick(dt)


class ActorAnimationTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))
        set_root(__file__)

    @classmethod
    def tearDownClass(self):
        # Make sure we don't leave the clock with events left in the queue.
        clock.clear()
        pygame.display.quit()

    def test_missing_animation_errors(self):
        a = Actor("ninja")
        with self.assertRaises(KeyError):
            a.anim.add("nonsense")

    def test_add_animation_from_folder_with_defaults(self):
        """We can add animations from folders and defaults are correclty
        applied."""
        a = Actor("ninja")
        a.anim.add("walk_down")

        self.assertEqual(a.anim.animation_pool, ("walk_down",))

        added_anim = a.anim._animation_pool["walk_down"]
        self.assertEqual(len(added_anim.frames), 4)
        self.assertEqual(len(added_anim.durations), 4)
        self.assertTrue(all(dur == 0.25 for dur in added_anim.durations))
        self.assertEqual(len(added_anim.offsets), 4)
        self.assertTrue(all(off == (0, 0) for off in added_anim.offsets))
        self.assertIsNone(added_anim.callback)

    def test_add_animation_from_spritesheet_horizontal(self):
        """We can add animations from horizontally arranged spritesheets."""
        a = Actor("ninja")
        a.anim.add_spritesheet("walk_down", 64, 64)

        self.assertEqual(a.anim.animation_pool, ("walk_down",))
        added_anim = a.anim._animation_pool["walk_down"]
        self.assertEqual(len(added_anim.frames), 4)
        # The rest of the defaults are gotten the same so don't have to be
        # rechecked here.

    def test_add_animation_from_spritesheet_vertical(self):
        """We can also get vertically arranged spritesheets."""
        a = Actor("ninja")
        a.anim.add_spritesheet("walk_down_ver", 64, 64, vertical=True)

        self.assertEqual(a.anim.animation_pool, ("walk_down_ver",))
        added_anim = a.anim._animation_pool["walk_down_ver"]
        self.assertEqual(len(added_anim.frames), 4)

    def test_add_animation_custom_total_duration(self):
        """We can add animations with a custom total duration."""
        a = Actor("ninja")
        a.anim.add("walk_down", 2.0)
        durations = a.anim._animation_pool["walk_down"].durations
        self.assertTrue(all(dur == 0.5 for dur in durations))

    def test_add_animation_custom_different_durations(self):
        """We can add animations with per frame durations."""
        a = Actor("ninja")
        a.anim.add("walk_down", (0.5, 0.25, 0.25, 0.5))
        durations = a.anim._animation_pool["walk_down"].durations
        self.assertEqual(durations[0], 0.5)
        self.assertEqual(durations[1], 0.25)
        self.assertEqual(durations[2], 0.25)
        self.assertEqual(durations[3], 0.5)

    def test_adding_animation_with_wrong_duration_num_errors(self):
        """Trying to add an animation with a number of durations different
        from the number of frames errors."""
        a = Actor("ninja")
        with self.assertRaises(ValueError):
            a.anim.add("walk_down", (0.5, 0.25, 0.25))

    def test_add_animation_custom_general_offset(self):
        """We can add animations with a custom general offset."""
        a = Actor("ninja")
        a.anim.add("walk_down", offsets=(0, -16))
        offsets = a.anim._animation_pool["walk_down"].offsets
        self.assertTrue(all(off == (0, -16) for off in offsets))

    def test_add_animation_custom_different_offsets(self):
        """We can add animations with per frame offsets."""
        a = Actor("ninja")
        a.anim.add("walk_down", offsets=((0, 0), (0, -32), (16, 8), (32, 0)))
        offsets = a.anim._animation_pool["walk_down"].offsets
        self.assertEqual(offsets[0], (0, 0))
        self.assertEqual(offsets[1], (0, -32))
        self.assertEqual(offsets[2], (16, 8))
        self.assertEqual(offsets[3], (32, 0))

    def test_adding_animation_with_wrong_offset_num_errors(self):
        """Trying to add an animation with a number of offsets different
        from the number of frames errors."""
        a = Actor("ninja")
        with self.assertRaises(ValueError):
            a.anim.add("walk_down", offsets=((0, 0), (0, -32), (16, 8)))

    def test_add_animation_with_custom_callback(self):
        """A supplied callback function is called after the animation
        finishes running."""
        test_func_mock = Mock()
        a = Actor("ninja")
        a.anim.add("walk_down", offsets=(0, -16), callback=test_func_mock)
        a.anim.play("walk_down")
        # We use clock.tick() to step through each animation frame here since
        # currently, animations can only advance at most one frame per tick.
        clock.tick(0.1)
        multitick(0.25, 4)
        test_func_mock.assert_called_once()

    def test_play_animation(self):
        """We can play animations which switches actor images out correctly.
        Calling the function mid animation again does not restart playing."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.play("walk_down")
        # These are the frames we expect to be playing through.
        frames = a.anim._animation_pool["walk_down"].frames
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_down"])
        clock.tick(0.1)
        # We can use this to change the actors _a_image without actually
        # drawing the actor.
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[0])
        clock.tick(0.25)
        # Calling this again while the animation is running should not
        # restart it.
        a.anim.play("walk_down")
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[1])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[2])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[3])
        # After the last step, the actor should return to its static image.
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_start_animation(self):
        """We can start playing animations just like before but calling the
        function again will restart playing."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.start("walk_down")
        frames = a.anim._animation_pool["walk_down"].frames
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[0])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[1])
        # This restarts the animation.
        a.anim.start("walk_down")
        clock.tick(0.1)
        a._manage_frame_advancement()
        # Here we expect the first frame again since start() reset the
        # animation progress.
        self.assertEqual(a._a_image, frames[0])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[1])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[2])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[3])
        # After the last step, the actor should return to its static image.
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_base_animation_playing(self):
        """We can set a base animation that always plays when no other
        animation is playing."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        # This animation should automatically play once the first is done.
        a.anim.add("walk_up")
        self.assertIsNone(a.anim._base_animation)
        a.anim.set_base("walk_up")
        self.assertEqual(a.anim._base_animation,
                         a.anim._animation_pool["walk_up"])
        frames = a.anim._animation_pool["walk_up"].frames
        # We play the first animation.
        a.anim.play("walk_down")
        # We advance the clock manually multiple times since currently
        # animations can only move at most one frame per tick.
        clock.tick(0.1)
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[0])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[1])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[2])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frames[3])
        clock.tick(0.25)
        a._manage_frame_advancement()
        # Since it was set as a base animation, it should immediately play
        # again.
        self.assertEqual(a._a_image, frames[0])

    def test_base_animation_changing(self):
        """We can change the base animation while it is playing and it will
        immediately switch to the new animation."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        self.assertIsNone(a.anim._base_animation)
        a.anim.set_base("walk_up")
        self.assertEqual(a.anim._base_animation,
                         a.anim._animation_pool["walk_up"])
        frame = a.anim._animation_pool["walk_up"].frames[0]
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)
        clock.tick(0.25)
        # Changing the set base animation should start the new one.
        a.anim.set_base("walk_down")
        frame = a.anim._animation_pool["walk_down"].frames[0]
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)

    def test_base_animation_remove(self):
        """We can remove the base animation and if it is playing, it will be
        stopped."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.set_base("walk_down")
        frame = a.anim._animation_pool["walk_down"].frames[0]
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)
        a.anim.remove_base()
        self.assertIsNone(a.anim._base_animation)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_add_animation_queue(self):
        """We can add a sequence of animations as a queue with a name."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        self.assertEqual(a.anim.queue_pool, ("walking_queue",))
        self.assertEqual(a.anim._queue_pool["walking_queue"]._animations,
                         ("walk_down", "walk_up"))
        self.assertIsNone(a.anim._queue_pool["walking_queue"]._callback)
        self.assertIsNone(a.anim._queue_pool["walking_queue"]._new_base)

    def test_add_animation_queue_with_callback(self):
        """We can also add a queue with a callback."""
        test_func_mock = Mock()
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"),
                         callback=test_func_mock)
        a.anim.play_queue("walking_queue")
        # We let both animations play out.
        clock.tick(0.1)
        multitick(0.25, 8)
        test_func_mock.assert_called_once()

    def test_add_animation_queue_with_new_base(self):
        """We can also add a queue that change the base animation once
        finished."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.set_base("walk_down")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"),
                         new_base="walk_up")
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.base, "walk_down")
        # We let both animations play out.
        clock.tick(0.1)
        multitick(0.25, 8)
        self.assertEqual(a.anim.base, "walk_up")

    def test_play_animation_queue(self):
        """We can play animation queues and calling it again does not restart
        the queue."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        a.anim.play_queue("walking_queue")
        # These are the animation names we expect to be playing through.
        anim_names = a.anim._queue_pool["walking_queue"]._animations
        # These are the frames of the first animation in the queue.
        first_frame = a.anim._animation_pool[anim_names[0]].frames[0]
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        multitick(0.25, 4)
        # We should now be in the second animation
        # Calling this again while the queue is running should not restart it.
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        first_frame = a.anim._animation_pool[anim_names[1]].frames[0]
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        multitick(0.25, 4)
        # The second animation should now have finished, also finishing the
        # queue.
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_start_animation_queue(self):
        """We can play animation queues and calling it again will restart the
        queue."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        a.anim.start_queue("walking_queue")
        # First we check the same way we did for play_queue().
        anim_names = a.anim._queue_pool["walking_queue"]._animations
        first_frame = a.anim._animation_pool[anim_names[0]].frames[0]
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        multitick(0.25, 2)
        # Now we restart the queue in the middle of the first animation.
        a.anim.start_queue("walking_queue")
        # We check everything again, this time staying just like the test for
        # play_queue().
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        first_frame = a.anim._animation_pool[anim_names[1]].frames[0]
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_pause(self):
        """We can pause animation playback."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.play("walk_down")
        frame = a.anim._animation_pool["walk_down"].frames[1]
        clock.tick(0.1)
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've started playing the animation.
        self.assertEqual(a._a_image, frame)
        # Now we pause, it, a._a_image should not advance.
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, frame)

    def test_pause_then_play(self):
        """We can play animations normally after having paused before."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.play("walk_down")
        frame = a.anim._animation_pool["walk_down"].frames[1]
        clock.tick(0.1)
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, frame)
        # We can start playing again however we want with no interference.
        a.anim.play("walk_down")
        frame = a.anim._animation_pool["walk_down"].frames[0]
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)

    def test_unpause(self):
        """We can resume playback from a paused state with unpause."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.play("walk_down")
        frame = a.anim._animation_pool["walk_down"].frames[1]
        clock.tick(0.1)
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)
        # We can resume the previous playback with animation progress retained.
        a.anim.unpause()
        frame = a.anim._animation_pool["walk_down"].frames[2]
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, frame)

    def test_pause_queue(self):
        """We can also pause queues with no problem."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        a.anim.play_queue("walking_queue")
        # These are the animation names we expect to be playing through.
        anim_names = a.anim._queue_pool["walking_queue"]._animations
        # This is the first frame of the first animation in the queue.
        first_frame = a.anim._animation_pool[anim_names[0]].frames[0]
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        # Now the frame should not advance further.
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, first_frame)
        # The whole queue should also not advance its animation once the
        # current one would have been done.
        multitick(0.25, 4)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, first_frame)

    def test_pause_queue_then_play(self):
        """We can also play a queue after a pause."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        a.anim.play_queue("walking_queue")
        anim_names = a.anim._queue_pool["walking_queue"]._animations
        first_frame = a.anim._animation_pool[anim_names[0]].frames[0]
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        # We add a new queue so the expected image does not match the one
        # we were holding on at during the pause.
        a.anim.add_queue("walking_reversed", ("walk_up", "walk_down"))
        a.anim.play_queue("walking_reversed")
        # This is the first frame of "walking_up" this time.
        first_frame = a.anim._animation_pool[anim_names[1]].frames[0]
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_reversed"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        # We've correctly changed the animation image.
        self.assertEqual(a._a_image, first_frame)

    def test_unpause_queue(self):
        """We can also unpause queues and retain their previous state."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        a.anim.play_queue("walking_queue")
        anim_names = a.anim._queue_pool["walking_queue"]._animations
        first_frame = a.anim._animation_pool[anim_names[0]].frames[0]
        self.assertEqual(a.anim.current, a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim.current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, first_frame)
        # Now we should resume playback normally.
        a.anim.unpause()
        second_frame = a.anim._animation_pool[anim_names[0]].frames[1]
        clock.tick(0.25)
        a._manage_frame_advancement()
        # Here should be the second frame of the first animation.
        self.assertEqual(a._a_image, second_frame)
        multitick(0.25, 3)
        a._manage_frame_advancement()
        # And now we should be in the first frame of the second animation.
        first_frame = a.anim._animation_pool[anim_names[1]].frames[0]
        second_frame = a.anim._animation_pool[anim_names[1]].frames[1]
        self.assertEqual(a._a_image, first_frame)
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, second_frame)

    def test_check_animation_type(self):
        """We can get the type of currently playing animation as a string."""
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        self.assertIsNone(a.anim.current_type)
        a.anim.set_base("walk_up")
        a.anim.play("walk_down")
        self.assertEqual(a.anim.current_type, "single")
        clock.tick(0.1)
        multitick(0.25, 4)
        self.assertEqual(a.anim.current_type, "base")
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.current_type, "queue")

    def test_actors_get_individual_animation_systems(self):
        """All actors get their own animation system and are unaffected by
        operations done to others'."""
        a = Actor("ninja")
        b = Actor("ninja")
        a.anim.add("walk_down")
        self.assertEqual(len(a.anim.animation_pool), 1)
        self.assertEqual(len(b.anim.animation_pool), 0)
