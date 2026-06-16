# We need sys to print warnings when pause state is wiped.
import sys

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
        self._run_info = None

    # Properties are defined to allow reading of values but not setting them.
    # Some of these include aliases for properties to allow easier or more
    # intuitive use.
    @property
    def animation_pool(self):
        return tuple(self._animation_pool.keys())

    animations = animation_pool

    @property
    def queue_pool(self):
        return tuple(self._queue_pool.keys())

    @property
    def current(self):
        if self._current_animation:
            return self._current_animation.name
        return None

    current_animation = current
    running = current

    @property
    def current_queue(self):
        if self._current_queue:
            return self._current_queue.name
        return None

    @property
    def current_queue_position(self):
        """Returns the current position in the queue. None means no queue is
        currently running, 0 is the first and so on."""
        if self._current_queue is not None:
            return self._current_queue._animation_index
        return None

    @property
    def base_animation(self):
        if self._base_animation:
            return self._base_animation.name
        else:
            return None

    @property
    def playing_base(self):
        return (self._current_animation
                and self._current_animation == self._base_animation)

    @base_animation.setter
    def base_animation(self, name):
        # If we set the same animation again, simply return.
        if self._base_animation and name == self._base_animation.name:
            return

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
        # Otherwise raise the same error as _check_animation_name().
        # Since base_animation can be None, _check_animation_name() cannot be
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
                and self._current_animation == self._base_animation):
            return "base"
        elif self._current_queue:
            return "queue"
        elif self._current_animation:
            return "single"
        else:
            return None

    # Checks whether the given name is actually a key for the animation pool.
    # If not, an error is raised that also lists available animations.
    def _check_animation_name(self, name):
        if name not in self._animation_pool:
            raise ValueError("Given animation name '{}' is not part of the "
                             "available animation pool. Valid animation names "
                             "are the following: {}"
                             .format(name, ", ".join(self._animation_pool)))

    # Checks whether the given name is actually a key for the queue pool.
    # If not, an error is raised that also lists available queues.
    def _check_queue_name(self, name):
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

    def _add_animation(self, name, frames, durations, offsets, sound, callback,
                       new_base):
        """Helper function to not repeat code unnecessarily. Both add() and
        add_spritesheet() just call this once they got the animation frames by
        their individual ways."""
        if name in self._animation_pool:
            raise ValueError("Animation {} already in pool. If you want to "
                             "change it, first remove('{}') and then add it"
                             "with the new settings again.".format(name, name))

        num_frames = len(frames)
        durations = self._process_durations(durations, num_frames)
        offsets = self._process_offsets(offsets, num_frames)

        # Create the new animation and add it to the available pool.
        a = ActorAnimation(self, name, frames, durations, offsets, sound,
                           callback, new_base)
        self._animation_pool[name] = a

    # Managing animations in the pool
    def add(self, name, durations=1.0, offsets=(0, 0), sound=None,
            callback=None, new_base=None):
        """Adds a given animation to the animation pool by its name.

        :param name: Name of the animation to be added.
        """
        # Load the animation frames via ResourceLoader
        frames = loaders.animations.load(name)
        # Call the helper function to actually add the animation.
        self._add_animation(name, frames, durations, offsets, sound, callback,
                            new_base)

    def add_spritesheet(self, name, frame_width, frame_height, durations=1.0,
                        offsets=(0, 0), sound=None, callback=None,
                        new_base=None, vertical=False):
        """Adds a given animation from a spritesheet to the animation pool by
        its name.

        :param name: Name of the animation to be added.
        """
        # Load the animation frames via ResourceLoader
        frames = loaders.spritesheets.load(name, vertical, frame_width,
                                           frame_height)
        # Call the helper function to actually add the animation.
        self._add_animation(name, frames, durations, offsets, sound, callback,
                            new_base)

    def add_queue(self, name, animation_names, sound=None, callback=None,
                  new_base=None):
        """Adds a new queue to the animation system. All animations that are
        part of the queue must already be valid animations in the system.

        :param name: Name of the new queue to be added.
        :param animation_names: List or tuple of the animation names in the
                                queue.
        :param sound: A PGTurbo sound object to play when the animation first
                      starts playing.
        :param callback: What function to call once the queue finishes playing.
        :param new_base: What to set the systems base animation to once the
                         queue finishes playing.
        """
        if name in self._queue_pool:
            raise ValueError("A queue with the name {} is already in the queue"
                             " pool. If you want to change it, first "
                             "remove_queue('{}') and then add it with your "
                             "chosen settings again.".format(name, name))

        for a in animation_names:
            self._check_animation_name(a)

        q = ActorAnimationQueue(self, name, tuple(animation_names), sound,
                                callback, new_base)
        self._queue_pool[name] = q

    # set_base() is a courtesy function to make working with anim easier.
    # Since the user mostly makes something happen with anim through
    # functions, the base animation can also be manipulated with functions.
    def set_base(self, name):
        self.base_animation = name

    def remove(self, name):
        """Removes the named animation from the animation pool.

        :param name: Name of the animation to be removed.
        """
        # If the animation is part of the pool, remove it an unload the
        # cached animation frames.
        self._check_animation_name(name)

        # If we are currently playing the animation to be removed in a queue,
        # skip to the next animation in the queue.
        if self._current_queue and name in self._current_queue._animations:
            i = self._current_queue._animations.index(name)
            if self._current_queue._animation_index == i:
                clock.unschedule(self._current_queue._next_animation)
                self._current_queue._next_animation()

        # If the animation to be removed is playing right now, stop it before
        # removal. If it's the base animation, stop everything, otherwise
        # return to the base animation if possible.
        if self._current_animation and self._current_animation.name == name:
            if self._base_animation and self._base_animation.name == name:
                self.stop_all()
            else:
                self.stop()

        # We remove the animation from any queues and if it was in the current
        # queue we adjust the running animation index accordingly.
        for queue in self._queue_pool.values():
            # If the name is in the queue, we remove it.
            if name in queue._animations:
                i = queue._animations.index(name)
                queue._animations = tuple(a for a in queue._animations
                                          if not a == name)
                # We only need to adjust the animation index if it was before
                # or at the removed animation.
                if (queue == self._current_queue
                        and i >= queue._animation_index):
                    queue._animation_index -= 1

        # If we were paused on the animation to be removed, remove the pause
        # state.
        if self._pause_info and self._pause_info["animation_name"] == name:
            print("WARNING: Animation was removed while it was paused, pause "
                  "state was wiped.", file=sys.stderr)
            self._pause_info = None

        del self._animation_pool[name]
        loaders.animations.unload(name)

    def remove_queue(self, name):
        """Removes the named queue from the queue pool.

        :param name: Name of the queue to be removed.
        """
        self._check_queue_name(name)

        # If we are playing the queue to be removed, stop it before removal.
        if self._current_queue and self._current_queue.name == name:
            self.stop()

        # If we were paused on the queue to be removed, remove the pause state.
        if self._pause_info and self._pause_info["queue_name"] == name:
            print("WARNING: Queue was removed while it was paused, pause state"
                  " was wiped.", file=sys.stderr)
            self._pause_info = None

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
            remaining_duration = self._pause_info["remaining_frame"]
            self._current_animation._resume_frame(remaining_duration)
        # Otherwise, reset the progress states of the animation
        # in case they hadn't been already and run it.
        else:
            self._current_animation._reset()
            if self._current_animation._sound:
                self._current_animation._sound.play()
            self._current_animation._next_frame()

        # Reset pause state.
        self._paused = False
        self._pause_info = None

    def _run_queue(self, name, position, resume=False):
        # If an animation is currently running, unschedule its
        # frame advancement.
        if self._current_animation:
            clock.unschedule(self._current_animation._next_frame)
        self._current_queue = self._queue_pool[name]
        # If a queue should not be started but resumed,
        # get the remaining information from the pause state
        # and call the queue function to resume playing.
        if resume:
            remaining_frame = self._pause_info["remaining_frame"]
            remaining_queue = self._pause_info["remaining_animation"]
            queue = self._current_queue
            anim_name = queue._animations[queue._animation_index]
            self._current_animation = self._animation_pool[anim_name]
            self._current_queue._resume_animation(remaining_frame,
                                                  remaining_queue)
        # Otherwise, reset the progress states of the queue
        # in case they hadn't been already and run it.
        else:
            # If the given position isn't valid, we just give a more
            # descriptive error message for the user.
            try:
                anim_name = self._current_queue._animations[position]
            except IndexError:
                max_index = len(self._queue_pool[name]._animations) - 1
                raise IndexError("Position {} to play the queue from is "
                                 "outside the valid indices for the queue "
                                 "(0-{}).".format(position, max_index))
            self._current_animation = self._animation_pool[anim_name]
            self._current_queue._reset()
            if position > 0:
                self._current_queue._animation_index = position - 1
            elif position < 0:
                num_anims = len(self._current_queue._animations)
                # We add here since position is negative in this branch.
                self._current_queue._animation_index = num_anims + position - 1
            else:
                # Only if the queue starts from the beginning we play its
                # associated sound.
                if self._current_sound._sound:
                    self._current_sound._sound.play()
            self._current_queue._next_animation()

        # Reset pause state.
        self._paused = False
        self._pause_info = None

    def play(self, name):
        # Check if the animation name is valid.
        self._check_animation_name(name)

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

    def play_queue(self, name, position=0):
        # Check if the queue name is valid.
        self._check_queue_name(name)

        # Same logic as above.
        if not self._current_queue:
            self._run_queue(name, position)
        elif self._current_queue.name != name:
            self._record_interruption()
            self._run_queue(name, position)

    def start(self, name):
        # Check if the animation name is valid.
        self._check_animation_name(name)
        # If something was playing before, check what and all info to be able
        # to resume it later.
        self._record_interruption()
        # Start the given animation, even if it was already running.
        self._run(name)

    def start_queue(self, name, position=0):
        # Check if the queue name is valid.
        self._check_queue_name(name)
        self._record_interruption()
        # Start the given queue, even if it was already running.
        self._run_queue(name, position)

    def _record_interruption(self):
        # If nothing was running, nothing was interrupted either.
        if not self._current_animation:
            self._pause_info = None
            return
        # Timestamp of the pause.
        paused = clock.time
        # Animation object that was running when pausing.
        anim = self._current_animation
        # How much time the frame has been displayed for so far.
        elapsed_frame = paused - anim._frame_started
        # How much display time is still remaining for the current frame.
        remaining_frame = anim._durations[anim._frame_index] - elapsed_frame
        if self._current_queue:
            # Queue object that was running when pausing.
            queue = self._current_queue
            queue_name = queue._name
            elapsed_animation = paused - queue._animation_started
            remaining_animation = anim._total_duration - elapsed_animation
        else:
            queue_name = None
            remaining_animation = None

        self._pause_info = {"animation_name": anim._name,
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

        # If we were paused but somehow lost the pause state (for example
        # because something that was paused was removed since pausing), we
        # play the base animation if there is one.
        if not self._pause_info:
            print("WARNING: Unpause was called while there was no valid pause "
                  "state, likely because an animation or queue was removed "
                  "while having been paused.", file=sys.stderr)
            if self._base_animation:
                self._run(self._base_animation)
            # We explicitely unpause here since it otherwise only happens
            # as part of _run(). But if there was no base animation, nothing
            # would have been run.
            self._paused = False
            return

        # Otherwise, resume the former state.
        # Get the name of the animation and queue before the pause.
        prev_animation_name = self._pause_info["animation_name"]
        prev_queue_name = self._pause_info["queue_name"]

        # Makes sure the animation that should be unpaused is still
        # in the animation pool.
        self._check_animation_name(prev_animation_name)
        # If we were playing a queue before, check and resume that.
        if prev_queue_name:
            self._check_queue_name(prev_queue_name)
            # If resume is True, the given position is ignored, so can be 0.
            self._run_queue(prev_queue_name, 0, True)
        # Otherwise just resume the single animation.
        else:
            # Running _run() with True makes it resume the animation
            # instead of starting it from scratch.
            self._run(prev_animation_name, True)

    # Ending animations
    def _done(self):
        """Function called by the running animation when it finishes."""
        # If there was a function callback set for the animation, call it.
        if self._current_animation._callback:
            self._current_animation._callback()
        # If the animation included a new base animation to set, do so now.
        if self._current_animation._new_base:
            new_base_name = self._current_animation._new_base
            self._base_animation = self._animation_pool[new_base_name]
        # If there's a base animation, play it.
        if self._base_animation:
            self._run(self._base_animation.name)
        # If not, stop animating (returns to the static image of the actor).
        else:
            self._current_animation = None

    # Ending queues
    def _done_queue(self):
        """Function called by the running queue when it finishes."""
        # If there was a function callback set for the queue, call it.
        if self._current_queue._callback:
            self._current_queue._callback()
        # If the queue included a new base animation to set, do so now.
        if self._current_queue._new_base:
            new_base_name = self._current_queue._new_base
            self._base_animation = self._animation_pool[new_base_name]
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

    def __init__(self, anim_system, name, animations, sound, callback,
                 new_base):
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
        # A sound object to play when the queue first starts playing.
        self._sound = sound
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
            self._anim_system._done_queue()
        # If the animation is not done, schedule the next frame advancement.
        else:
            # Indicates actor.draw() should get the new frame.
            self._new_animation = True
            # Records when this animation was started.
            self._animation_started = clock.time

            new_name = self._animations[self._animation_index]

            # Call up to the animation manager to run the next animation.
            self._anim_system._run(new_name)

            # How long the entire animation will take to play out.
            td = self._anim_system._animation_pool[new_name]._total_duration
            # Schedules the next animation advancement.
            clock.schedule(self._next_animation, td)

    def _resume_animation(self, remaining_frame, remaining_animation):
        self._new_animation = True
        self._animation_started = clock.time
        # Resumes the animation in the queue that was playing when paused.
        anim_name = self._animations[self._animation_index]
        anim_to_resume = self._anim_system._animation_pool[anim_name]
        anim_to_resume._resume_frame(remaining_frame)
        # Schedules the advancement of the queue with the remaining duration
        # for it.
        clock.schedule(self._next_animation, remaining_animation)

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

    def __init__(self, anim_sys, name, frames, durations, offsets, sound,
                 callback, new_base):
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
        # A sound object to play when the animation first starts.
        self._sound = sound
        # Callback function for the animation.
        self._callback = callback
        # What to set the actors base animation to once playing finishes.
        self._new_base = new_base

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
            self._anim_system._done()
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
