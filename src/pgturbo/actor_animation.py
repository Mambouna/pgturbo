from . import loaders
from .clock import clock


"""
Manages animations for actor objects.
"""


class ActorAnimationSystem:
    """
    Management class. Each actor holds an instance of this class in the
    property anim. Direct write access to the important properties is
    restricted and use of anim should
    """

    def __init__(self):
        """Initializes the system with an empty state. This is always the
        starting point that a new actor gets."""
        self._animation_pool = {}
        self._current_animation = None
        self._queue_pool = {}
        self._current_queue = None
        self._queue_index = None
        self._base_animation = None
        self._paused = False
        self._pause_info = None

    # Properties are defined to allow reading of values but not setting them.
    # Some of these include aliases for properties to allow easier or more
    # intuitive use.
    @property
    def animation_pool(self):
        return tuple(self._animation_pool.keys())

    animations = animation_pool

    @property
    def current(self):
        return self._current_animation

    current_animation = current
    running = current

    @property
    def current_queue(self):
        return self._current_queue

    @property
    def queue_pool(self):
        return tuple(self._queue.keys())

    @property
    def base_animation(self):
        if self._base_animation:
            return self._base_animation.name
        else:
            return None

    @base_animation.setter
    def base_animation(self, name):
        # Check if the former base animation is currently running.
        swap = self._current_animation == self._base_animation
        # If the name is in the pool, set the base animation.
        if name in self._animation_pool:
            # Run this animation if base animation was running
            # or no animation was running.
            if swap or not self._current_animation:
                self._run(name)
            # Update the base animation.
            self._base_animation = self._animation_pool[name]
        # If None was set, do that too.
        elif name is None:
            # If the former base animation was running, stop it.
            if swap:
                self.stop_all()
            # stop_all() already sets the base animation to None
            # so this can be in an else block.
            else:
                self._base_animation = None
        # Otherwise raise the same error as check_animation_name().
        # Since base_animation can be None, check_animation_name() cannot be
        # used here to validate the given name.
        else:
            raise ValueError("Given animation name '{}' is not part of the "
                             "available animation pool. Valid animation names "
                             "are the following: {}"
                             .format(name, ", ".join(self._animation_pool)))

    base = base_animation

    @property
    def paused(self):
        return self._paused

    @property
    def current_type(self):
        if (self._base_animation
                and self._current_animation == self._base_animation.name):
            return "base"
        elif self._current_queue:
            return "queue"
        elif self._current_animation:
            return "single"
        else:
            return None

    # Checks whether the given name is actually a key for the animation pool.
    # If not, an error is raised that also lists available animations.
    def check_animation_name(self, name):
        if name not in self._animation_pool:
            raise ValueError("Given animation name '{}' is not part of the "
                             "available animation pool. Valid animation names "
                             "are the following: {}"
                             .format(name, ", ".join(self._animation_pool)))

    # Checks whether the given name is actually a key for the queue pool.
    # If not, an error is raised that also lists available queues.
    def check_queue_name(self, name):
        if name not in self._queue_pool:
            raise ValueError("Given queue name {} is not part of the "
                             "available queue pool. Valid queue names "
                             "are the following: {}"
                             .format(name, ", ".join(self._queue_pool)))

    def _process_durations(self, durations, num_frames):
        # If multiple durations were supplied, check if their number
        # matches the number of frames and error if not.
        if isinstance(durations, (list, tuple)):
            num_durations = len(durations)
            if num_durations != num_frames:
                raise ValueError("Number of supplied durations {} does "
                                 "not match number of animation frames {}."
                                 .format(num_durations, num_frames))
            # Ensure datatype is tuple on return if it wasn't before.
            return tuple(durations)
        # If a single duration was supplied, divide it equally among
        # all frames.
        else:
            each_duration = durations / num_frames
            return tuple([each_duration] * num_frames)

    def _process_offsets(self, offsets, num_frames):
        # The length of offsets is used either to check whether the correct
        # number of individual offsets were given or if the single offset
        # tuple contains the correct number of values (2).
        num_offsets = len(offsets)
        # Basically same check for offsets but the condition checks whether the
        # first element of offsets is also a tuple, since a single offset would
        # already satisfy the condition otherwise.
        if isinstance(offsets[0], tuple):
            if num_offsets != num_frames:
                raise ValueError("Number of supplied offsets {} does "
                                 "not match number of animation frames {}."
                                 .format(num_offsets, num_frames))
            # Check each offset for correct number of values.
            for o in offsets:
                lo = len(o)
                if lo != 2:
                    raise ValueError("Offset tuples must have exactly two "
                                     "integer values for x and y, not {} "
                                     "values.".format(lo))
            # Ensure datatype is tuple on return if it wasn't before.
            return tuple(offsets)
        # If only a single tuple was supplied, also check number of values.
        elif num_offsets != 2:
            raise ValueError("Offset tuples must have exactly two integer "
                             "values for x and y, not {} values."
                             .format(num_offsets))
            # No return here since it's a failure state.
        # If a single offset was supplied, give it to every frame.
        else:
            return tuple([offsets] * num_frames)

    def _add_animation(self, name, frames, durations, offsets,
                               callback):
        """Helper function to not repeat code unnecessarily. Both add() and
        add_spritesheet() just call this once they got the animation frames by
        their individual ways."""
        num_frames = len(frames)
        durations = self._process_durations(durations, num_frames)
        offsets = self._process_offsets(offsets, num_frames)

        # Create the new animation and add it to the available pool.
        a = ActorAnimation(self, name, frames, durations, offsets, callback)
        self._animation_pool[name] = a

    # Managing animations in the pool
    def add(self, name, durations=1.0, offsets=(0, 0), callback=None):
        """Adds a given animation to the animation pool by its name.

        :param name: Name of the animation to be added.
        """
        # Load the animation frames via ResourceLoader
        frames = loaders.animations.load(name)
        # Call the helper function to actually add the animation.
        self._add_animation(name, frames, durations, offsets, callback)

    def add_spritesheet(self, name, frame_width, frame_height, vertical=False,
                        durations=1.0, offsets=(0, 0), callback=None):
        """Adds a given animation from a spritesheet to the animation pool by
        its name.

        :param name: Name of the animation to be added.
        """
        # Load the animation frames via ResourceLoader
        frames = loaders.spritesheets.load(name, vertical, frame_width,
                                           frame_height)
        # Call the helper function to actually add the animation.
        self._add_animation(name, frames, durations, offsets, callback)

    def add_queue(self, name, animations, callback=None, new_base=None):
        """Adds a new queue to the animation system. All animations that are
        part of the queue must already be valid animations in the system.

        :param name: Name of the new queue to be added.
        :param animations: List or tuple of the animations in the queue.
        :param callback: What function to call once the queue finishes playing.
        :param new_base: What to set the systems base animation to once the
                         queue finishes playing.
        """
        for a in animations:
            self.check_animation_name(a)

        # TODO: Makes sense to cast to tuple here or just leave it?
        q = ActorAnimationQueue(self, name, tuple(animations), callback,
                                new_base)
        self._queue_pool[name] = q

    def remove(self, name):
        """Removes the named animation from the animation pool.

        :param name: Name of the animation to be removed.
        """
        # If the animation is part of the pool, remove it an unload the
        # cached animation frames.
        self.check_animation_name(name)

        del self._animation_pool[name]
        loaders.animations.unload(name)

    def remove_queue(self, name):
        """Removes the named queue from the queue pool.

        :param name: Name of the queue to be removed.
        """
        self.check_queue_name(name)
        del self._queue_pool[name]

    # Playing animations
    def _run(self, name, resume=False):
        # If an animation is currently running, unschedule its
        # frame advancement.
        if self._current_animation:
            clock.unschedule(self._current_animation._next_frame)
        # Set the new currently running animation.
        self._current_animation = self._animation_pool[name]
        # If an animation should not be started but resumed,
        # get the remaining information from the pause state
        # and call the animations function to resume playing.
        if resume:
            self._current_animation._resume_frame(self._pause_info[1])
        # Otherwise, reset the progress states of the animation
        # in case they hadn't been already and run it.
        else:
            self._current_animation._frame_index = None
            self._current_animation._new_frame = False

            self._current_animation._next_frame()

        # Reset pause state.
        self._paused = False
        self._pause_info = None

    def _run_queue(self, name, resume=False):
        # If an animation is currently running, unschedule its
        # frame advancement.
        if self._current_animation:
            clock.unschedule(self._current_animation._next_frame)
        self._current_queue = self._queue_pool[name]
        # Set the new currently running animation.
        self._current_animation = self._current_queue._animations[0]
        # If a queue should not be started but resumed,
        # get the remaining information from the pause state
        # and call the queue function to resume playing.
        if resume:
            # TODO: How does pause info look again?
            self._current_animation._resume_animation(self._pause_info[1],
                                                      self._pause_info[2])
        # Otherwise, reset the progress states of the queue
        # in case they hadn't been already and run it.
        else:
            self._current_queue._animation_index = None
            self._current_queue._new_animation = False

            self._current_queue._next_animation()

        # Reset pause state.
        self._paused = False
        self._pause_info = None

    def play(self, name):
        # Check if the animation name is valid.
        self.check_animation_name(name)

        # If we aren't running anything, run the animation.
        if not self._current_animation:
            self._run(name)
        # If we were running something different before, record that and run
        # the new thing.
        elif self._current_animation.name != name:
            self._record_interruption()
            self._run(name)
        # If neither, the only other options is we were already running this,
        # so nothing needs to be done.

    def play_queue(self, name):
        # Check if the queue name is valid.
        self.check_queue_name(name)

        # Same logic as above.
        if not self._current_queue:
            self._run_queue(name)
        elif self._current_queue.name != name:
            self._record_interruption()
            self._run_queue(name)

    def start(self, name):
        # Check if the animation name is valid.
        self.check_animation_name(name)
        # If something was playing before, check what and all info to be able
        # to resume it later.
        self._record_interruption()
        # Start the given animation, even if it was already running.
        self._run(name)

    def start_queue(self, name):
        # Check if the queue name is valid.
        self.check_queue_name(name)
        self._record_interruption()
        # Start the given queue, even if it was already running.
        self._run_queue(name)

    def _record_interruption(self):
        # If nothing was running, nothing was interrupted either.
        if not self._current_animation:
            self._pause_info = None
            return
        # Calculate the remaining time the frame should be shown after
        # unpausing. Same for the animation if it's in a queue.
        paused = clock.time
        frame_started = self._current_animation._frame_started
        remaining_frame = paused - frame_started
        if self._current_queue:
            queue_name = self._current_queue._name
            animation_started = self._current_queue._animation_started
            remaining_animation = paused - animation_started
        else:
            queue_name = None
            animation_started = None
            remaining_animation = None

        self._pause_info = {"animation_name": self._current_animation._name,
                            "queue_name": queue_name,
                            "remaining_frame": remaining_frame,
                            "remaining_animation": remaining_animation,
                            "type": self.current_type}

    # Pausing animations
    def pause(self):
        # If we are paused, do nothing.
        if self._paused:
            return

        # Otherwise, record the state before the pause and then reset.
        self._paused = True
        # Saves all info in _pause_info to resume later.
        self._record_interruption()
        # Unschedule advancing the current animation.
        clock.unschedule(self._current_animation._next_frame)
        if self._current_queue:
            clock.unschedule(self._current_queue._next_animation)
        self._current_animation = None
        self._current_queue = None

    def unpause(self):
        # If we aren't paused, do nothing.
        if not self._paused:
            return
        # Otherwise, resume the former state.
        # Get the name of the animation before the pause.
        prev_animation_name = self._pause_info["animation_name"]
        prev_queue_name = self._pause_info["queue_name"]

        # Makes sure the animation that should be unpaused is still
        # in the animation pool.
        self.check_animation_name(prev_animation_name)
        # If we were playing a queue before, check and resume that.
        if prev_queue_name:
            self._check_queue_name(prev_queue_name)
            self._run_queue(prev_queue_name, True)
        # Otherwise just resume the single animation.
        else:
            # Running _run() with True makes it resume the animation
            # instead of starting it from scratch.
            self._run(prev_animation_name, True)

    # Base animation
    # set_base() is a courtesy function to make working with anim easier.
    # Since the user mostly makes something happen with anim through
    # functions, the base animation can also be manipulated with functions.
    def set_base(self, name):
        self.base_animation = name

    def remove_base(self, name):
        self.base_animation = None

    # Animation queue
    def current_queue_position(self):
        """Returns the current position in the queue. None means no queue is
        currently running, 0 is the first and so on."""
        if self._current_queue is not None:
            return self._current_queue._animation_index
        return None

    # TODO: Better name for this function?
    def jump_to_queue_animation(self, position):
        # Jump to a specific animation in the queue by position.
        index = position - 1
        # Error descriptively in case of a bad given position.
        if index < 0 or index >= len(self._queue):
            raise ValueError("Position {} to jump to is not in the queue. "
                             "Minimum position is 1 and maximum position is"
                             " currently {}".format(position, len(self._queue)))

        # If the queue is currently playing, reset the animation and
        # play from where the new position is.
        if self._current_queue:
            self._queue[self._queue_index].reset()

            self._queue_index = index - 1
            self._advance_queue()
        # Otherwise, only set the position without starting to play.
        # TODO: Should this be changed? Should queue_jump always play?
        else:
            # TODO: IMPORTANT! This means that until the queue is played,
            # queue_position will report the wrong value to the user.
            self._queue_index = index - 1

    def _check_queue_steps(self, steps=1, forward=True):
        """Function to check whether a given amount of steps to change
        the queue position by is in bounds based on the direction to move."""
        if self._current_queue is None:
            raise ValueError("No queue is currently playing so it's animation"
                             " can't be advanced.")
        if steps < 1:
            raise ValueError("start_next_queue_animation() accepts only "
                             "positive integer values (the number of "
                             "animations to go forward in the queue), not {}."
                             .format(steps))
        new_index = self._current_queue._animation_index + steps
        queue_len = len(self._current_queue._animations)
        if forward and new_index >= queue_len:
            max_steps = queue_len - self._current_queue._animation_index - 1
            raise IndexError("Given steps {} go out of bounds of the animation"
                             " queue, maximum steps forward at this point "
                             "would be {}.".format(steps, max_steps))
        # TODO: Should this compare to -1 or 0?
        if self._current_queue._animation_index - steps < -1:
            max_steps = self._current_queue._animation_index
            raise IndexError("Given steps {} go out of bounds of the animation"
                             " queue, maximum steps backward at this point "
                             "would be {}.".format(steps, max_steps))

    def start_next_queue_animation(self, steps=1):
        # Catch possible bad value for steps.
        self._check_queue_steps(steps)

        # Reset the currently playing animation.
        self._current_animation._reset()
        # Since _next_animation() already increments the index by
        # one, we reduce it by one here to have more intuitive
        # values to use with the function.
        self._current_queue._animation_index += steps - 1
        self._current_queue._next_animation()

    def start_previous_queue_animation(self, steps=1):
        # Catch possible bad value for steps.
        self._check_queue_steps(steps, False)
        # Same as above but with a minus instead of a plus.
        self._current_animation._reset()
        self._current_queue._animation_index -= steps - 1
        self._current_queue._next_animation()

    # Ending animations
    def _done(self):
        """Function called by the running animation when it finishes."""
        # If there's a base animation, play it.
        if self._base_animation:
            self._run(self._base_animation.name)
        # If not, stop animating (returns to the static image of the actor).
        else:
            self._current_animation = None

    # Ending queues
    def _done_queue(self):
        """Function called by the running queue when it finishes."""
        # If the queue included a new base animation to set, do so now.
        if self._current_queue._new_base:
            self._base_animation = self._current_queue._new_base
        # Play the base animation if present otherwise stop animating.
        if self._base_animation:
            self._run(self._base_animation.name)
        else:
            self._current_animation = None
        self._current_queue = None

    def stop(self):
        # If no animations are running or we are running the base
        # animation, do nothing.
        if (not self._current_animation
                or self._current_animation == self._base_animation):
            return

        # Reset the state of the running animation and unschedule it.
        self._current_animation._reset()
        # If we were running a queue, stop it and reset it.
        if self._current_queue:
            self._current_queue._reset()
            self._current_queue = None
        # If there is a base animation, return to playing it.
        if self._base_animation:
            self._run(self._base_animation.name)
        else:
            self._current_animation = None

    def stop_all(self):
        # If no animations are running, do nothing.
        if not self._current_animation:
            return
        # Reset the state of the running animation and unschedule it.
        self._current_animation._reset()
        # If we were running a queue, stop it and reset it.
        if self._current_queue:
            self._current_queue._reset()
            self._current_queue = None
        self._current_animation = None
        self._base_animation = None

    def __repr__(self):
        return "<ActorAnimationSystem={}>".format(self.__dir__())


class ActorAnimationQueue:

    def __init__(self, anim_system, name, animations, callback, new_base):
        # Actor the queue is attached to.
        self._anim_system = anim_system
        # Name of the animation queue.
        self._name = name
        # List of all the animations in the queue.
        self._animations = animations
        # Index of the current animation in the queue.
        self._animation_index = None
        # Indicator whether the next animation in the queue should be started.
        self._new_animation = False
        # Time when this animation started playing.
        self._animation_started = None
        # What function to call when the queue finishes.
        self._callback = callback
        # What to set the actors base animation to once the queue finishes.
        self._new_base = new_base

    # Function to advance the current animation and schedule the next
    # advancement
    def _next_animation(self):
        if self._animation_index is not None:
            self._animation_index += 1
        else:
            self._animation_index = 0

        # If the queue has finished, reset the animation counter and call
        # the function telling the animation manager that the queue is done.
        if self._animation_index >= len(self._animations):
            self._animation_index = None
            # TODO: Necessary? Counterproductive? : self._new_animation = False
            self._anim_system._done_queue()
            # If there was a function callback set for the animation, call it.
            if self._callback:
                self._callback()
        # If the animation is not done, schedule the next frame advancement.
        else:
            # Indicates actor.draw() should get the new frame.
            self._new_animation = True
            # Records when this animation was started.
            self._animation_started = clock.time

            # Resets and starts the proper animation in the queue.
            self._animations[self._animation_index]._reset()
            # Call up to the animation manager to run the next animation.
            self._anim_system._run(self._animations[self._animation_index])

            # How long the entire animation will take to play out.
            timeout = self._animations[self._animation_index].total_duration
            # Schedules the next animation advancement.
            clock.schedule(self._next_animation, timeout)

    def _resume_animation(self, remaining_frame, remaining_queue):
        self._new_animation = True
        self._animation_started = clock.time
        # Resumes the animation in the queue that was playing when paused.
        self._animations[self._animation_index]._resume_frame(remaining_frame)
        # Schedules the advancement of the queue with the remaining duration
        # for it.
        clock.schedule(self._next_animation, remaining_queue)

    # Function to reset the state of the queue and unschedule its advance-
    # ment if it was running.
    def _reset(self):
        # Unscheduling does not error even if _next_frame was not scheduled.
        clock.unschedule(self._next_animation)
        # Reset the tracking values for queue progress.
        self._animation_index = None
        self._new_animation = False
        self._animation_started = None

    @property
    def name(self):
        return self._name

    @property
    def animations(self):
        return self._animations

    @property
    def animation(self):
        if self._animation_index:
            return self._animations[self._animation_index]
        return None

    @property
    def callback(self):
        return self._callback

    @property
    def new_base(self):
        return self._new_base

    def __repr__(self):
        return "<ActorAnimationQueue={}>".format(self.__dir__())


class ActorAnimation:

    def __init__(self, anim_sys, name, frames, durations, offsets, callback):
        # Actor object that holds the animation.
        self._anim_system = anim_sys
        # Name of the animation.
        self._name = name
        # Tuple of frames of the animation.
        self._frames = frames
        # Index of the current frame.
        self._frame_index = None
        # Indicator whether draw() of the actor should load the current image.
        self._new_frame = False
        # Time when this frame started being shown.
        self._frame_started = None
        # Tuple of frame durations.
        self._durations = durations
        self._total_duration = sum(durations)
        # Tuple of spacial offsets for frames.
        self._offsets = offsets
        # Callback function for the animation.
        self._callback = callback

    # Function to advance the current frame and schedule the next advancement
    def _next_frame(self):
        if self._frame_index is not None:
            self._frame_index += 1
        else:
            self._frame_index = 0

        # If the animation has finished, reset the frame counter and call
        # the function telling the animation manager that the animation is done.
        if self._frame_index >= len(self._frames):
            self._frame_index = None
            # TODO: Necessary? Counterproductive? : self._new_frame = False
            self._anim_system._done()
            # If there was a function callback set for the animation, call it.
            if self._callback:
                self._callback()
        # If the animation is not done, schedule the next frame advancement.
        else:
            # Indicates actor.draw() should get the new frame.
            self._new_frame = True
            # Records when this frame was started to be shown.
            self._frame_started = clock.time
            # Schedules the next frame advancement.
            # Note: This approach has the downside that if a clock.tick()
            # spanned more time than the frame should have been displayed for,
            # the entire animation is lengthened by the difference since it
            # can only advance by one frame for every tick at most.
            clock.schedule(self._next_frame, self._durations[self._frame_index])

    def _resume_frame(self, remaining_duration):
        self._new_frame = True
        self._frame_started = clock.time
        clock.schedule(self._next_frame, remaining_duration)

    # Function to reset the state of the animation and unschedule its advance-
    # ment if it was running.
    def _reset(self):
        # Unscheduling does not error even if _next_frame was not scheduled.
        clock.unschedule(self._next_frame)
        # Reset the tracking values for animation progress.
        self._frame_index = None
        self._new_frame = False
        self._frame_started = None

    @property
    def name(self):
        return self._name

    @property
    def frames(self):
        return self._frames

    @property
    def frame(self):
        # TODO: What's the best behaviour when the user asks for
        # info about the current frame when the animation isn't
        # running? Currently, some return None and others neutral
        # values for their operations. Better ideas?
        if self._frame_index:
            return self._frames[self._frame_index]
        # We return the first frame of the animation even if it's not running
        # so that frame offset calculations remain correct in the short time
        # between transitioning animations.
        # TODO: Does that actually work generally or only in the case that an
        # animation is looping itself?
        return self._frames[0]

    @property
    def durations(self):
        return self._durations

    @property
    def duration(self):
        if self._frame_index:
            return self._durations[self._frame_index]
        return None

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def offsets(self):
        return self._offsets

    @property
    def offset(self):
        if self._frame_index:
            return self.offsets[self._frame_index]
        return (0, 0)

    @property
    def offset_x(self):
        if self._frame_index:
            return self._offsets[self._frame_index][0]
        return 0

    @property
    def offset_y(self):
        if self._frame_index:
            return self._offsets[self._frame_index][1]
        return 0

    @property
    def callback(self):
        return self._callback

    def __repr__(self):
        return "<ActorAnimation={}>".format(self.__dir__())
