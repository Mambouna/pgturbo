"""Tone generator for Pygame Turbo.

This tone generator uses numpy to generate sine waves to play through
Pygames own mixer. Tones are kept in a LRU cache which in typical applications
will reduce the number of times they need to be regenerated.

To minimise the extent that pauses affect gameplay, the ``play()`` function
offloads tone generation to a separate thread. Because tones are generated
with numpy operations this should allow at least part of this work to happen
on another CPU core, if present.

NOTE: This module used to use the pyfxr package but this was replaced with
custom code to remove the dependency.

"""
from functools import lru_cache
from collections import namedtuple
from threading import Thread, Lock
from queue import Queue

import pygame

# Valid octave characters, dumb but functional.
OCTAVES = ("0", "1", "2", "3", "4", "5", "6", "7", "8")
# The frequencies for all chromas at octave 4.
CHROMAS = {"C": 261.63, "C#": 277.18, "Db": 277.18, "D": 293.66, "D#": 311.13,
           "Eb": 311.13, "E": 329.63, "F": 349.23, "F#": 369.99, "Gb": 369.99,
           "G": 392, "G#": 415.3, "Ab": 415.3, "A": 440.0, "A#": 466.16,
           "Bb": 466.16, "B": 493.88}
SAMPLERATE = 22050


# Custom note string validation as that came from pyfxr before.
def note_to_hertz(note_string):
    length = len(note_string)
    chroma_string = note_string[:-1]
    octave_string = note_string[-1]

    # Validation of note string in one step.
    if (length < 2 or length > 3 or chroma_string not in CHROMAS
            or octave_string not in OCTAVES):
        raise ValueError("Notestrings must be either of length 2 or 3 in the"
                         " pattern note chroma (F-A), an accidental (#/b) or "
                         "none and the octave (0-8).")

    # How many times we need to double or halve the frequency.
    octave_difference = int(octave_string) - 4
    # If the octave is higher, we double for each octave difference,
    # otherwise halve.
    base_multiplier = 2 if octave_difference >= 0 else 0.5
    # Final adjustment necessary because of the octave difference.
    final_multiplier = base_multiplier ** abs(octave_difference)
    # Calculation of the actual hertz. First getting the frequency for octave 4
    # and then adjusting for octave.
    hertz = CHROMAS[chroma_string] * final_multiplier
    return hertz


__all__ = (
    'play',
    'create',
)


# Longest note to allow
MAX_DURATION = 4


ToneParams = namedtuple('ToneParams', 'hz duration volume')


# lru_cache isn't threadsafe until Python 3.7, so protect it ourselves
# https://bugs.python.org/issue28969
cache_lock = Lock()
note_queue = Queue()
player_thread = None


def _play_thread():
    """Play any notes requested by the game thread.

    Multithreading is useful because numpy releases the GIL while performing
    many C operations.

    """
    while True:
        params = note_queue.get()
        with cache_lock:
            note = _create(params)
        note.play()


def create(*args, **kwargs):
    """Create a tone of a given duration at the given pitch.

    Return a Sound which can be played later.

    """
    params = _convert_args(*args, **kwargs)
    with cache_lock:
        return _create(params)


@lru_cache()
def _create(params):
    """Actually create a tone."""
    # Import numpy here so it doesn't hog resources if it's not used.
    import numpy
    # Numpy magic to generate a sine wave with the right parameters.
    mono_tone = numpy.array([
        4096 * numpy.sin(2.0 * numpy.pi * params.hz * x / SAMPLERATE)
        for x in range(0, SAMPLERATE)
    ]).astype(numpy.int16)
    # The wave is mono but the next call expects stereo audio so we just
    # put the same wave on both channels.
    stereo_tone = numpy.c_[mono_tone, mono_tone]
    # This generates the actual sound object from the waveform.
    sound = pygame.sndarray.make_sound(stereo_tone)
    sound.set_volume(params.volume)
    return sound


def _convert_args(pitch, duration, *, volume=0.8):
    """Convert the given arguments to _create parameters."""
    if duration > MAX_DURATION:
        raise ValueError(
            'Note duration %ss is too long: notes may be at most %ss long' %
            (duration, MAX_DURATION)
        )
    if not duration:
        raise ValueError("Note has zero duration")
    if isinstance(pitch, str):
        # Replaced pyfxr call with custom logic.
        pitch = note_to_hertz(pitch)
    return ToneParams(pitch, duration, volume)


def play(*args, **kwargs):
    """Plays a tone of a certain length from a note or frequency in hertz.

    Tones have a maximum duration of 4 seconds. This limitation is imposed to
    avoid accidentally creating sounds that take too long to generate and
    require a lot of memory.

    To work around this, create the sounds you want to use up-front with
    create() and hold onto them, perhaps in an array.

    """
    global player_thread
    params = _convert_args(*args, **kwargs)
    if not player_thread or not player_thread.is_alive():
        pygame.mixer.init()
        player_thread = Thread(target=_play_thread, daemon=True)
        player_thread.start()
    note_queue.put(params)
