.. _reference_tone:

Reference: tone
================

:ref:`Deep dive on tone generation <deep_dive_tone>`

.. _reference_tone_methods:

Methods
-------

.. method:: tone.play(tone, duration, [volume])

    Play a note with a certain pitch for the given `duration` in seconds.

    The `tone` can be specified as a number in which case it is the frequency
    of the note in hertz (the literal pitch).

    Alternatively, the `tone` can be specified as a string representing a note
    name and octave. For example:

    * ``"E4"`` would be E in octave 4.
    * ``"A#5"`` would be A-sharp in octave 5.
    * ``"Bb3"`` would be B-flat in octave 3.

    In this case, the actual pitch is computed from the given string.

    `volume` is a float between ``0.0`` and ``1.0`` and sets how loud the tone
    will be played. The default for `volume` if not provided is ``0.75``.

    Note that sound loudness is not perceived linearly by humans, so a
    `volume` value half that of another will not sound half as loud to
    your ears. Experiment to see what values work best for you.

    :param tone: The pitch of the tone, either a number that represents the
                 Hertz of the note or a string representation as explained
                 above.
    :param duration: The duration the played tone should last in seconds.
                     Maximum for `duration` is 4 seconds, since generation of
                     long sounds can degrade performance.
    :param volume: Optionally the volume to play the sound at. Default is
                   ``0.75``.

.. method:: tone.create(tone, duration, [volume])

    Create and return a ``Sound`` object, for example to store in a variable
    to play repeatedly later.

    Sound objects act the same way as ``sounds.filename`` objects to.

    :param tone: The pitch of the generated tone, either a number that
                 represents the Hertz of the note or a string representation
                 of a note (see ``tone.play()`` above).
    :param duration: The duration the generated tone should last in seconds
                     when played later. Maximum for `duration` is 4 seconds,
                     since generation of long sounds can degrade performance.
    :param volume: Optionally the volume setting to create the sound object
                   with. Default is ``0.75``.

.. _reference_tone_sound_methods:

Methods for Sound objects
-------------------------

``Sound`` objects are the same as ``sounds.filename`` objects, meaning all
functions available to use on them are available here as well:

.. method:: Sound.play([loops])

    Play the sound. If no argument is given, play once, otherwise loop it a
    number of times.

    :param loops: The number of times to loop. If you pass ``-1`` as the
                  number of times to loop, the sound will loop forever (or
                  until you call ``Sound.stop()``).

.. method:: Sound.stop()

    Stop playing the sound.

.. method:: Sound.get_length()

    Get the duration of the sound in seconds.

.. method:: Sound.set_volume(value)

    Sets the volume of the sound to a float between ``0.0`` and ``1.0``.

    *Note:* The internal value that volume gets set to might be slightly
    different from the one you set. This is because Pygame internally
    represents the volume with a value that has less precision than the float
    you used creating it.

    :param value: The volume to set the sound to in the range from ``0.0``
                  (silent) to ``1.0`` (full volume).

.. method:: Sound.get_volume()

    Returns the volume the sound is set to.

    The same note about volume value precision above applies here too.

    A sound created with ``0.6`` as the volume for example might return
    ``0.59375`` when using ``.get_volume()``.


.. _reference_tone_changelog:

Changelog
---------

* **1.13:** Fixed and reworked tone generation on the backend.
* **1.4:** First release of PGTurbo after fork from PGZero.
