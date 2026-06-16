import unittest
from unittest.mock import patch, Mock
# Used to supress printed warnings in unittests.
from io import StringIO

import pygame

from pgturbo.actor import Actor
from pgturbo.loaders import set_root, sounds
from pgturbo.clock import clock


TEST_MODULE = "pgturbo.actor_animation"
TEST_DISP_W, TEST_DISP_H = (200, 100)


# Helper function since we have to call clock.tick() many times to advance
# frames in this test file.
def multitick(dt, num):
    for _ in range(num):
        clock.tick(dt)


# There's multiple test cases to allow testing adding animations and also
# using setUp() in the usage tests to not repeat a bunch of lines all the time.
class ActorAnimationAddingAnimsTest(unittest.TestCase):
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

    def setUp(self):
        global a
        a = Actor("ninja")

    def test_missing_animation_errors(self):
        with self.assertRaises(KeyError):
            a.anim.add("nonsense")

    def test_add_animation_from_folder_with_defaults(self):
        """We can add animations from folders and defaults are correclty
        applied."""
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
        a.anim.add_spritesheet("walk_down", 64, 64)

        self.assertEqual(a.anim.animation_pool, ("walk_down",))
        added_anim = a.anim._animation_pool["walk_down"]
        self.assertEqual(len(added_anim.frames), 4)
        # The rest of the defaults are gotten the same so don't have to be
        # rechecked here.

    def test_add_animation_from_spritesheet_vertical(self):
        """We can also get vertically arranged spritesheets."""
        a.anim.add_spritesheet("walk_down_ver", 64, 64, vertical=True)

        self.assertEqual(a.anim.animation_pool, ("walk_down_ver",))
        added_anim = a.anim._animation_pool["walk_down_ver"]
        self.assertEqual(len(added_anim.frames), 4)

    def test_add_animation_custom_total_duration(self):
        """We can add animations with a custom total duration."""
        a.anim.add("walk_down", 2.0)
        durations = a.anim._animation_pool["walk_down"].durations
        self.assertTrue(all(dur == 0.5 for dur in durations))

    def test_add_animation_custom_different_durations(self):
        """We can add animations with per frame durations."""
        a.anim.add("walk_down", (0.5, 0.25, 0.25, 0.5))
        durations = a.anim._animation_pool["walk_down"].durations
        self.assertEqual(durations[0], 0.5)
        self.assertEqual(durations[1], 0.25)
        self.assertEqual(durations[2], 0.25)
        self.assertEqual(durations[3], 0.5)

    def test_adding_animation_with_wrong_duration_num_errors(self):
        """Trying to add an animation with a number of durations different
        from the number of frames errors."""
        with self.assertRaises(ValueError):
            a.anim.add("walk_down", (0.5, 0.25, 0.25))

    def test_add_animation_custom_general_offset(self):
        """We can add animations with a custom general offset."""
        a.anim.add("walk_down", offsets=(0, -16))
        offsets = a.anim._animation_pool["walk_down"].offsets
        self.assertTrue(all(off == (0, -16) for off in offsets))

    def test_add_animation_custom_different_offsets(self):
        """We can add animations with per frame offsets."""
        a.anim.add("walk_down", offsets=((0, 0), (0, -32), (16, 8), (32, 0)))
        offsets = a.anim._animation_pool["walk_down"].offsets
        self.assertEqual(offsets[0], (0, 0))
        self.assertEqual(offsets[1], (0, -32))
        self.assertEqual(offsets[2], (16, 8))
        self.assertEqual(offsets[3], (32, 0))

    def test_adding_animation_with_wrong_offset_num_errors(self):
        """Trying to add an animation with a number of offsets different
        from the number of frames errors."""
        with self.assertRaises(ValueError):
            a.anim.add("walk_down", offsets=((0, 0), (0, -32), (16, 8)))

    def test_add_animation_with_custom_sound(self):
        """We can add an animation with a sound to play once it starts."""
        a.anim.add("walk_down", sound=sounds.powerup)
        self.assertIsNotNone(a.anim._animation_pool["walk_down"]._sound)
        self.assertIsInstance(a.anim._animation_pool["walk_down"]._sound,
                              pygame.mixer.Sound)

    def test_add_animation_with_custom_callback(self):
        """A supplied callback function is called after the animation
        finishes running."""
        test_func_mock = Mock()
        a.anim.add("walk_down", offsets=(0, -16), callback=test_func_mock)
        a.anim.play("walk_down")
        # We use clock.tick() to step through each animation frame here since
        # currently, animations can only advance at most one frame per tick.
        clock.tick(0.1)
        multitick(0.25, 4)
        test_func_mock.assert_called_once()

    def test_add_animation_with_new_base(self):
        """We can add an animation with a new base animation it should set once
        it finished playing."""
        a.anim.add("walk_up")
        a.anim.add("walk_down", new_base="walk_up")
        self.assertEqual(a.anim._animation_pool["walk_down"]._new_base,
                         "walk_up")

    def test_adding_same_animation_again_errors(self):
        """When the user tries to add the same animation twice for a single
        actor, an error is thrown."""
        a.anim.add("walk_down")
        with self.assertRaises(ValueError):
            a.anim.add("walk_down")

    def test_edit_added_animation(self):
        """We can edit the settings of animations after they have been
        loaded."""
        a.anim.add("walk_up")
        a.anim.add("walk_down", sound=sounds.powerup, callback=multitick)
        anim = a.anim._animation_pool["walk_down"]
        # Hooks so far are correct after adding the animation.
        self.assertIsNotNone(anim._sound)
        self.assertIsNotNone(anim._callback)
        self.assertIsNone(anim._new_base)
        # We can remove a former hook and others remain unchanged.
        a.anim.edit("walk_down", sound=None)
        self.assertIsNone(anim._sound)
        self.assertIsNotNone(anim._callback)
        # We can add a new hook and others remain unchanged.
        a.anim.edit("walk_down", new_base="walk_up")
        self.assertIsNotNone(anim._callback)
        self.assertIsNotNone(anim._new_base)
        # We can also edit fields that require preprocessing for the Anim.
        a.anim.edit("walk_down", durations=2.0)
        self.assertEqual(anim._durations, (0.5, 0.5, 0.5, 0.5))
        a.anim.edit("walk_down", offsets=((4, 6), (8, 10), (12, 14), (16, 18)))
        self.assertEqual(anim._offsets, ((4, 6), (8, 10), (12, 14), (16, 18)))
        # Correct errors are also raised when giving invalid values.
        with self.assertRaises(ValueError):
            a.anim.edit("walk_down", new_base="nonsense")
        with self.assertRaises(ValueError):
            a.anim.edit("walk_down", offsets=((4, 6), (8, 10)))
        # Trying to edit a queue while it is running errors.
        a.anim.play("walk_down")
        with self.assertRaises(RuntimeError):
            a.anim.edit("walk_down", new_base=None)
        # We reset the state here to clean up any mess we left in clock events.
        a.anim._reset()


class ActorAnimationAddingQueuesTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))
        set_root(__file__)

    @classmethod
    def tearDownClass(self):
        clock.clear()
        pygame.display.quit()

    def setUp(self):
        global a
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")

    def test_add_animation_queue(self):
        """We can add a sequence of animations as a queue with a name."""
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        self.assertEqual(a.anim.queue_pool, ("walking_queue",))
        self.assertEqual(a.anim._queue_pool["walking_queue"]._animations,
                         ("walk_down", "walk_up"))
        self.assertIsNone(a.anim._queue_pool["walking_queue"]._callback)
        self.assertIsNone(a.anim._queue_pool["walking_queue"]._new_base)

    def test_add_animation_queue_with_callback(self):
        """We can also add a queue with a callback."""
        test_func_mock = Mock()
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
        a.anim.set_base("walk_down")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"),
                         new_base="walk_up")
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.base, "walk_down")
        # We let both animations play out.
        clock.tick(0.1)
        multitick(0.25, 8)
        self.assertEqual(a.anim.base, "walk_up")

    def test_adding_same_queue_again_errors(self):
        """When the user tries to add two queues with the same name, an error
        is thrown."""
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        with self.assertRaises(ValueError):
            a.anim.add_queue("walking_queue", ("walk_up", "walk_down"))

    def test_edit_added_queues(self):
        """We can edit the settings of queues after they have been added."""
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"),
                         sound=sounds.powerup, callback=multitick)
        queue = a.anim._queue_pool["walking_queue"]
        # Hooks so far are correct after adding the queue.
        self.assertIsNotNone(queue._sound)
        self.assertIsNotNone(queue._callback)
        self.assertIsNone(queue._new_base)
        # We can remove a former hook and others remain unchanged.
        a.anim.edit_queue("walking_queue", sound=None)
        self.assertIsNone(queue._sound)
        self.assertIsNotNone(queue._callback)
        # We can add a new hook and others remain unchanged.
        a.anim.edit_queue("walking_queue", new_base="walk_up")
        self.assertIsNotNone(queue._callback)
        self.assertIsNotNone(queue._new_base)
        # We can also change the animations in a queue.
        a.anim.edit_queue("walking_queue",
                          animation_names=("walk_up", "walk_down"))
        self.assertEqual(queue._animations, ("walk_up", "walk_down"))
        # Correct errors are also raised when giving invalid values.
        with self.assertRaises(ValueError):
            a.anim.edit_queue("walking_queue", new_base="nonsense")
        with self.assertRaises(ValueError):
            a.anim.edit_queue("walking_queue", animation_names=("nonsense"))
        # Trying to edit a queue while it is running errors.
        a.anim.play_queue("walking_queue")
        with self.assertRaises(RuntimeError):
            a.anim.edit_queue("walking_queue", new_base=None)
        # We reset the state here to clean up any mess we left in clock events.
        a.anim._reset()


class ActorAnimationUsingTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global sounds_powerup_play, sounds_powerdown_play
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))
        set_root(__file__)
        # We first need to mock the sound object and then also the play
        # function on it to separately give the object to the animation and
        # then check whether play() was called on it later.
        sounds.powerup = Mock()
        sounds_powerup_play = Mock()
        sounds.powerup.attach_mock(sounds_powerup_play, "play")
        sounds.powerdown = Mock()
        sounds_powerdown_play = Mock()
        sounds.powerdown.attach_mock(sounds_powerdown_play, "play")

    @classmethod
    def tearDownClass(self):
        # Make sure we don't leave the clock with events left in the queue.
        clock.clear()
        pygame.display.quit()

    def setUp(self):
        global a, walk_down_frames, walk_up_frames
        a = Actor("ninja")
        a.anim.add("walk_down")
        a.anim.add("walk_up")
        a.anim.add_queue("walking_queue", ("walk_down", "walk_up"))
        a.anim.add_queue("walking_reversed", ("walk_up", "walk_down"))
        walk_down_frames = a.anim._animation_pool["walk_down"].frames
        walk_up_frames = a.anim._animation_pool["walk_up"].frames
        # Make sure no events are hanging around from other tests that weren't
        # cleaned up.
        clock.clear()
        sounds.powerup.reset_mock()
        sounds_powerup_play.reset_mock()
        sounds.powerdown.reset_mock()
        sounds_powerdown_play.reset_mock()

    def test_play_animation(self):
        """We can play animations which switches actor images out correctly.
        Calling the function mid animation again does not restart playing."""
        a.anim.play("walk_down")
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_down"])
        clock.tick(0.1)
        # We can use this to change the actors _a_image without actually
        # drawing the actor.
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        clock.tick(0.25)
        # Calling this again while the animation is running should not
        # restart it.
        a.anim.play("walk_down")
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[1])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[2])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[3])
        # After the last step, the actor should return to its static image.
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_play_animation_with_sound(self):
        """If an animation has an associated sound, it will play when run."""
        a.anim.edit("walk_down", sound=sounds.powerup)
        a.anim.play("walk_down")
        sounds_powerup_play.assert_called_once()
        # Since both play() and start() call _run() internally and the sound
        # is played there, we don't need to test separately for start().

    def test_play_animation_with_callback(self):
        """If an animation has an associated callback, it will be called after
        the animation has played out."""
        test_func_mock = Mock()
        a.anim.edit("walk_down", callback=test_func_mock)
        a.anim.play("walk_down")
        multitick(0.25, 4)
        test_func_mock.assert_called_once()

    def test_play_animation_with_new_base(self):
        """If an animation should set a new base animation after playing, it
        does so."""
        self.assertIsNone(a.anim.base_animation)
        a.anim.edit("walk_down", new_base="walk_up")
        a.anim.play("walk_down")
        multitick(0.25, 4)
        self.assertEqual(a.anim.base_animation, "walk_up")

    def test_play_animation_with_override_sound(self):
        """If an animation playback is done with overriden sound, the sound
        plays correctly."""
        a.anim.play("walk_down", sound=sounds.powerup)
        sounds_powerup_play.assert_called_once()

    def test_play_animation_with_override_callback(self):
        """If an animation is called with an override callback, it is called
        after the animation has run."""
        test_func_mock = Mock()
        a.anim.play("walk_down", callback=test_func_mock)
        multitick(0.25, 4)
        test_func_mock.assert_called_once()

    def test_play_animation_with_override_new_base(self):
        """If an animation is played with overriden new_base set, it's set
        after playing out."""
        self.assertIsNone(a.anim.base_animation)
        a.anim.play("walk_down", new_base="walk_up")
        multitick(0.25, 4)
        self.assertEqual(a.anim.base_animation, "walk_up")

    def test_play_animation_with_override_sound_no_base_sound(self):
        """If an animation playback is done with overriden sound, the sound
        plays correctly and any original set sound for the animation does
        not."""
        # powerup is the normally set sound for the animation, should not play
        a.anim.edit("walk_down", sound=sounds.powerup)
        # powerdown is the override which should play
        a.anim.play("walk_down", sound=sounds.powerdown)
        sounds_powerdown_play.assert_called_once()
        sounds_powerup_play.assert_not_called()

    def test_play_animation_with_override_callback_no_base_callback(self):
        """If an animation is called with an override callback, it is called
        after the animation has run and any originally set callback is not
        called."""
        test_func_mock_no_call = Mock()
        test_func_mock_should_call = Mock()
        # no_call is the mock original callback supplied to the animation
        a.anim.edit("walk_down", callback=test_func_mock_no_call)
        # play() overrides the callback with should_call
        a.anim.play("walk_down", callback=test_func_mock_should_call)
        multitick(0.25, 4)
        test_func_mock_should_call.assert_called_once()
        test_func_mock_no_call.assert_not_called()

    def test_play_animation_with_override_new_base_no_base_new_base(self):
        """If an animation is played with overriden new_base set, it's set
        after playing out and any original new_base setting is not applied."""
        self.assertIsNone(a.anim.base_animation)
        # walk_up is the normal setting for the new base after playing
        a.anim.edit("walk_down", new_base="walk_up")
        # play() overrides it to be walk_down instead
        a.anim.play("walk_down", new_base="walk_down")
        multitick(0.25, 4)
        self.assertEqual(a.anim.base_animation, "walk_down")

    def test_start_animation(self):
        """We can start playing animations just like before but calling the
        function again will restart playing."""
        a.anim.start("walk_down")
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[1])
        # This restarts the animation.
        a.anim.start("walk_down")
        clock.tick(0.1)
        a._manage_frame_advancement()
        # Here we expect the first frame again since start() reset the
        # animation progress.
        self.assertEqual(a._a_image, walk_down_frames[0])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[1])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[2])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[3])
        # After the last step, the actor should return to its static image.
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_base_animation_playing(self):
        """We can set a base animation that always plays when no other
        animation is playing."""
        self.assertIsNone(a.anim._base_animation)
        a.anim.set_base("walk_up")
        self.assertEqual(a.anim._base_animation,
                         a.anim._animation_pool["walk_up"])
        # We play the first animation.
        a.anim.play("walk_down")
        # We advance the clock manually multiple times since currently
        # animations can only move at most one frame per tick.
        clock.tick(0.1)
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[1])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[2])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[3])
        clock.tick(0.25)
        a._manage_frame_advancement()
        # Since it was set as a base animation, it should immediately play
        # again.
        self.assertEqual(a._a_image, walk_up_frames[0])

    def test_base_animation_changing(self):
        """We can change the base animation while it is playing and it will
        immediately switch to the new animation."""
        a.anim.set_base("walk_up")
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        clock.tick(0.25)
        # Changing the set base animation should start the new one.
        a.anim.set_base("walk_down")
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])

    def test_base_animation_remove(self):
        """We can remove the base animation and if it is playing, it will be
        stopped."""
        a.anim.set_base("walk_down")
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        a.anim.set_base(None)
        self.assertIsNone(a.anim._base_animation)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_play_animation_queue(self):
        """We can play animation queues and calling it again does not restart
        the queue."""
        a.anim.play_queue("walking_queue")
        # These are the frames of the first animation in the queue.
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        multitick(0.25, 4)
        # We should now be in the second animation
        # Calling this again while the queue is running should not restart it.
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        multitick(0.25, 4)
        # The second animation should now have finished, also finishing the
        # queue.
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_play_animation_queue_with_starting_position(self):
        """We can play animation queues from an animation not starting at the
        beginning of the queue."""
        # We start playing the queue from the second animation (index 1).
        a.anim.play_queue("walking_queue", 1)
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        multitick(0.25, 2)
        # We are in the middle of the animation, calling play_queue() again
        # does not restart.
        a.anim.play_queue("walking_queue", 0)
        multitick(0.25, 2)
        # The animation has now finished meaning the queue is done.
        self.assertIsNone(a.anim._current_animation)
        self.assertIsNone(a.anim._current_queue)

    def test_play_queue_with_negative_index(self):
        """When playing queues not from the start, negative indices also
        work."""
        a.anim.play_queue("walking_queue", -1)
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        multitick(0.25, 2)
        a.anim.play_queue("walking_queue", 0)
        multitick(0.25, 2)
        self.assertIsNone(a.anim._current_animation)
        self.assertIsNone(a.anim._current_queue)

    def test_play_queue_with_sound(self):
        """If an animation has an associated sound, it will play when run."""
        a.anim.edit_queue("walking_queue", sound=sounds.powerup)
        a.anim.play_queue("walking_queue")
        sounds_powerup_play.assert_called_once()
        # Since both play() and start() call _run() internally and the sound
        # is played there, we don't need to test separately for start().

    def test_play_queue_with_callback(self):
        """If an animation has an associated callback, it will be called after
        the animation has played out."""
        test_func_mock = Mock()
        a.anim.edit_queue("walking_queue", callback=test_func_mock)
        a.anim.play_queue("walking_queue")
        multitick(0.25, 8)
        test_func_mock.assert_called_once()

    def test_play_queue_with_new_base(self):
        """If an animation should set a new base animation after playing, it
        does so."""
        self.assertIsNone(a.anim.base_animation)
        a.anim.edit_queue("walking_queue", new_base="walk_up")
        a.anim.play_queue("walking_queue")
        multitick(0.25, 8)
        self.assertEqual(a.anim.base_animation, "walk_up")

    def test_play_queue_with_override_sound(self):
        """If an animation playback is done with overriden sound, the sound
        plays correctly."""
        a.anim.play_queue("walking_queue", sound=sounds.powerup)
        sounds_powerup_play.assert_called_once()

    def test_play_queue_with_override_callback(self):
        """If an animation is called with an override callback, it is called
        after the animation has run."""
        test_func_mock = Mock()
        a.anim.play_queue("walking_queue", callback=test_func_mock)
        multitick(0.25, 8)
        test_func_mock.assert_called_once()

    def test_play_queue_with_override_new_base(self):
        """If an animation is played with overriden new_base set, it's set
        after playing out."""
        self.assertIsNone(a.anim.base_animation)
        a.anim.play_queue("walking_queue", new_base="walk_up")
        multitick(0.25, 8)
        self.assertEqual(a.anim.base_animation, "walk_up")

    def test_play_queue_with_override_sound_no_base_sound(self):
        """If an animation playback is done with overriden sound, the sound
        plays correctly and any original set sound for the animation does
        not."""
        # powerup is the normally set sound for the animation, should not play
        a.anim.edit_queue("walking_queue", sound=sounds.powerup)
        # powerdown is the override which should play
        a.anim.play_queue("walking_queue", sound=sounds.powerdown)
        sounds_powerdown_play.assert_called_once()
        sounds_powerup_play.assert_not_called()

    def test_play_queue_with_override_callback_no_base_callback(self):
        """If an queue is called with an override callback, it is called
        after the queue has run and any originally set callback is not
        called."""
        test_func_mock_no_call = Mock()
        test_func_mock_should_call = Mock()
        # no_call is the mock original callback supplied to the animation
        a.anim.edit_queue("walking_queue", callback=test_func_mock_no_call)
        # play() overrides the callback with should_call
        a.anim.play_queue("walking_queue", callback=test_func_mock_should_call)
        multitick(0.25, 8)
        test_func_mock_should_call.assert_called_once()
        test_func_mock_no_call.assert_not_called()

    def test_play_queue_with_override_new_base_no_base_new_base(self):
        """If a queue is played with overriden new_base set, it's set
        after playing out and any original new_base setting is not applied."""
        self.assertIsNone(a.anim.base_animation)
        # walk_up is the normal setting for the new base after playing
        a.anim.edit_queue("walking_queue", new_base="walk_up")
        # play() overrides it to be walking_queue instead
        a.anim.play_queue("walking_queue", new_base="walk_down")
        multitick(0.25, 8)
        self.assertEqual(a.anim.base_animation, "walk_down")

    def test_start_animation_queue(self):
        """We can play animation queues and calling it again will restart the
        queue."""
        a.anim.start_queue("walking_queue")
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        multitick(0.25, 2)
        # Now we restart the queue in the middle of the first animation.
        a.anim.start_queue("walking_queue")
        # We check everything again, this time staying just like the test for
        # play_queue().
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertIsNone(a._a_image)

    def test_start_animation_queue_with_starting_position(self):
        """We can start playing animation queues from other indices as well
        and calling it again restarts the queue."""
        a.anim.start_queue("walking_queue", 1)
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        # The queue has correctly started at the second animation.
        self.assertEqual(a._a_image, walk_up_frames[0])
        multitick(0.25, 2)
        # Calling start_queue() again restarts playback, again from the second
        # animation.
        a.anim.start_queue("walking_queue", 1)
        clock.tick(0.1)
        # Because we restarted, we are still in the animation after two more
        # ticks of 0.25.
        multitick(0.25, 2)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[2])
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        # Only after two more ticks is the queue done.
        multitick(0.25, 2)
        self.assertIsNone(a.anim._current_animation)
        self.assertIsNone(a.anim._current_queue)

    def test_starting_queue_with_negative_index(self):
        """When starting queues not from the start, negative indices also
        work."""
        a.anim.start_queue("walking_queue", -1)
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        multitick(0.25, 2)
        a.anim.start_queue("walking_queue", -1)
        clock.tick(0.1)
        multitick(0.25, 2)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[2])
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        multitick(0.25, 2)
        self.assertIsNone(a.anim._current_animation)
        self.assertIsNone(a.anim._current_queue)

    def test_wrong_index_for_playing_queues_errors(self):
        """If the user gives an invalid index for playing or starting a queue
        at, a descriptive error is raised."""
        with self.assertRaises(IndexError):
            a.anim.play_queue("walking_queue", 5)
        # This is necessary as the exception being raised in the last test
        # messes slightly with the anim state. This is not a problem for
        # end users since the error should stop their game running.
        a.anim._current_queue = None
        with self.assertRaises(IndexError):
            a.anim.play_queue("walking_queue", -5)
        # Since both play_queue() and start_queue() call _run_queue() and
        # the descriptive error is thrown there, we don't have to check them
        # separately.

    def test_pause(self):
        """We can pause animation playback."""
        a.anim.play("walk_down")
        clock.tick(0.1)
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've started playing the animation.
        self.assertEqual(a._a_image, walk_down_frames[1])
        # Now we pause, it, a._a_image should not advance.
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, walk_down_frames[1])

    def test_pause_then_play(self):
        """We can play animations normally after having paused before."""
        a.anim.play("walk_down")
        clock.tick(0.1)
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[1])
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, walk_down_frames[1])
        # We can start playing again however we want with no interference.
        a.anim.play("walk_down")
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])

    def test_unpause(self):
        """We can resume playback from a paused state with unpause."""
        a.anim.play("walk_down")
        clock.tick(0.1)
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[1])
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[1])
        # We can resume the previous playback with animation progress retained.
        a.anim.unpause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[2])

    def test_pause_queue(self):
        """We can also pause queues with no problem."""
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        # Now the frame should not advance further.
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, walk_down_frames[0])
        # The whole queue should also not advance its animation once the
        # current one would have been done.
        multitick(0.25, 4)
        a._manage_frame_advancement()
        # We've stayed on the same frame.
        self.assertEqual(a._a_image, walk_down_frames[0])

    def test_pause_queue_then_play(self):
        """We can also play a queue after a pause."""
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        a.anim.play_queue("walking_reversed")
        # This is the first frame of "walking_up" this time.
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_up"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_reversed"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        # We've correctly changed the animation image.
        self.assertEqual(a._a_image, walk_up_frames[0])

    def test_unpause_queue(self):
        """We can also unpause queues and retain their previous state."""
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim._current_animation,
                         a.anim._animation_pool["walk_down"])
        self.assertEqual(a.anim._current_queue,
                         a.anim._queue_pool["walking_queue"])
        clock.tick(0.1)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        a.anim.pause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        multitick(0.25, 4)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_down_frames[0])
        # Now we should resume playback normally.
        a.anim.unpause()
        clock.tick(0.25)
        a._manage_frame_advancement()
        # Here should be the second frame of the first animation.
        self.assertEqual(a._a_image, walk_down_frames[1])
        multitick(0.25, 3)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[0])
        clock.tick(0.25)
        a._manage_frame_advancement()
        self.assertEqual(a._a_image, walk_up_frames[1])

    def test_get_animation_pool_names(self):
        """The user can get all the valid loaded animation names."""
        self.assertEqual(a.anim.animation_pool, ("walk_down", "walk_up"))

    def test_get_current_animation_name(self):
        """The user can get the name of the currently playing animation."""
        a.anim.play("walk_down")
        self.assertEqual(a.anim.current, "walk_down")
        clock.tick(0.1)
        self.assertEqual(a.anim.current, "walk_down")
        multitick(0.25, 4)
        self.assertIsNone(a.anim.current)

    def test_get_base_animation_name(self):
        """The user can get the name of the currently set base animation."""
        a.anim.set_base("walk_down")
        self.assertEqual(a.anim.base_animation, "walk_down")

    def test_get_playing_base_boolean(self):
        """The user can get the boolean of whether the base animation is
        playing right now."""
        self.assertFalse(a.anim.playing_base)
        a.anim.set_base("walk_down")
        self.assertTrue(a.anim.playing_base)

    def test_get_queue_pool_names(self):
        """The user can get all the valid loaded animation names."""
        self.assertEqual(a.anim.queue_pool,
                         ("walking_queue", "walking_reversed"))

    def test_get_current_queue_name(self):
        """The user can get the name of the currently playing queue."""
        self.assertIsNone(a.anim.current_queue)
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.current_queue, "walking_queue")

    def test_get_paused_state(self):
        a.anim.play("walk_down")
        clock.tick(0.1)
        self.assertFalse(a.anim.paused)
        a.anim.pause()
        clock.tick(0.1)
        self.assertTrue(a.anim.paused)
        a.anim.unpause()
        clock.tick(0.1)
        self.assertFalse(a.anim.paused)

    def test_get_current_animation_type(self):
        """We can get the type of currently playing animation as a string."""
        self.assertIsNone(a.anim.current_type)
        a.anim.set_base("walk_up")
        a.anim.play("walk_down")
        self.assertEqual(a.anim.current_type, "single")
        clock.tick(0.1)
        multitick(0.25, 4)
        self.assertEqual(a.anim.current_type, "base")
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.current_type, "queue")

    def test_stop_nothing(self):
        """Stopping when nothing is playing does not cause an error."""
        a = Actor("ninja")
        try:
            a.anim.stop()
            a.anim.stop_all()
        except Exception:
            self.fail("Stopping without playing crashed.")

    def test_stop_single_animation(self):
        a.anim.play("walk_down")
        self.assertEqual(a.anim.current, "walk_down")
        clock.tick(0.1)
        a.anim.stop()
        self.assertIsNone(a.anim.current)

    def test_stop_single_to_base(self):
        """If a base animation is set, stop() will return to playing it."""
        a.anim.set_base("walk_up")
        a.anim.play("walk_down")
        self.assertEqual(a.anim.current, "walk_down")
        clock.tick(0.1)
        a.anim.stop()
        self.assertEqual(a.anim.current, "walk_up")

    def test_stop_queue_animation(self):
        """We can stop a running queue as well."""
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.current_queue, "walking_queue")
        clock.tick(0.1)
        a.anim.stop()
        self.assertIsNone(a.anim.current_queue)

    def test_stop_base_animation(self):
        """We can also stop everything playing including the base animation."""
        a.anim.set_base("walk_up")
        a.anim.play("walk_down")
        self.assertEqual(a.anim.current, "walk_down")
        clock.tick(0.1)
        a.anim.stop_all()
        self.assertIsNone(a.anim.current)
        self.assertIsNone(a.anim.base_animation)

    def test_remove_animation(self):
        """We can remove animations from the animation pool."""
        self.assertEqual(a.anim.animation_pool, ("walk_down", "walk_up"))
        a.anim.remove("walk_down")
        self.assertEqual(a.anim.animation_pool, ("walk_up",))

    def test_remove_animation_while_running(self):
        """The to be removed animation playing will stop playback."""
        a.anim.play("walk_down")
        self.assertEqual(a.anim.animation_pool, ("walk_down", "walk_up"))
        self.assertEqual(a.anim.current, "walk_down")
        clock.tick(0.1)
        a.anim.remove("walk_down")
        self.assertEqual(a.anim.animation_pool, ("walk_up",))
        self.assertIsNone(a.anim.current)

    def test_remove_base_animation_while_running(self):
        """The to be removed animation playing will stop playback."""
        a.anim.set_base("walk_down")
        self.assertEqual(a.anim.animation_pool, ("walk_down", "walk_up"))
        self.assertEqual(a.anim.current, "walk_down")
        clock.tick(0.1)
        a.anim.remove("walk_down")
        self.assertEqual(a.anim.animation_pool, ("walk_up",))
        self.assertIsNone(a.anim.current)
        self.assertIsNone(a.anim.base_animation)

    def test_remove_animation_in_queue(self):
        """Removing an animation that's in a queue smoothly reshuffles the
        queue."""
        a.anim.remove("walk_up")
        self.assertEqual(a.anim._queue_pool["walking_queue"]._animations,
                         ("walk_down",))

    def test_remove_animation_in_queue_while_running(self):
        """Removing an animation while it is playing in a queue skips the
        queue to the following animation."""
        # We need a third queue here to have a third animation to skip to.
        a.anim.add_queue("walking_three",
                         ("walk_down", "walk_up", "walk_down"))
        a.anim.play_queue("walking_three")
        clock.tick(0.1)
        multitick(0.25, 4)
        # We are now in the second animation
        self.assertEqual(a.anim.current, "walk_up")
        a.anim.remove("walk_up")
        self.assertEqual(a.anim.current, "walk_down")
        clock.tick(0.1)
        multitick(0.25, 4)
        self.assertIsNone(a.anim.current)
        self.assertEqual(a.anim._queue_pool["walking_three"]._animations,
                         ("walk_down", "walk_down"))

    @patch("sys.stderr", new=StringIO())
    def test_remove_animation_on_pause(self):
        """Removing an animation that was paused will wipe the pause state."""
        a.anim.play("walk_down")
        clock.tick(0.1)
        a.anim.pause()
        self.assertIsNotNone(a.anim._pause_info)
        a.anim.remove("walk_down")
        self.assertIsNone(a.anim._pause_info)
        a.anim.unpause()
        self.assertIsNone(a.anim.current)

    def test_remove_queue(self):
        """We can remove queues as well."""
        self.assertEqual(a.anim.queue_pool,
                         ("walking_queue", "walking_reversed"))
        a.anim.remove_queue("walking_queue")
        self.assertEqual(a.anim.queue_pool, ("walking_reversed",))

    def test_remove_queue_while_running(self):
        """Also works while running the queue."""
        a.anim.play_queue("walking_queue")
        self.assertEqual(a.anim.current_queue, "walking_queue")
        clock.tick(0.1)
        a.anim.remove_queue("walking_queue")
        self.assertEqual(a.anim.queue_pool, ("walking_reversed",))
        self.assertIsNone(a.anim.current_queue)

    @patch("sys.stderr", new=StringIO())
    def test_remove_queue_on_pause(self):
        """Removing a queue that was paused will wipe the pause state."""
        a.anim.play_queue("walking_queue")
        clock.tick(0.1)
        a.anim.pause()
        self.assertIsNotNone(a.anim._pause_info)
        a.anim.remove_queue("walking_queue")
        self.assertIsNone(a.anim._pause_info)
        a.anim.unpause()
        self.assertIsNone(a.anim.current)
        self.assertIsNone(a.anim.current_queue)

    def test_actors_get_individual_animation_systems(self):
        """All actors get their own animation system and are unaffected by
        operations done to others'."""
        b = Actor("ninja")
        self.assertEqual(len(a.anim.animation_pool), 2)
        self.assertEqual(len(b.anim.animation_pool), 0)
