.. _reference_sounds:

Reference: sounds
==================

:ref:`Deep dive on sounds <deep_dive_sounds>`

Sound files are always accessed via ``sounds.filename``, where filename is a
file in the *sounds* resource directory of the game without the file
extension.


.. _reference_sounds_location_filenames_and_formats:

Location, filenames and formats
-------------------------------

The ``sounds`` builtin can access all valid sound files in a directory called
*sounds*, placed next to your game's main python file.

Filenames can consist of lowercase letters, numbers and underscores and must
start with a letter.

For example, these filenames are valid::

    beep.wav
    laser_charge.wav
    boom_4.wav

These filenames are not valid::

    Beep.wav
    BEEP.wav
    3.wav
    3beeps.wav
    my-sound.wav
    sam's dog.wav

The following sound file formats can be used for ``sounds``: ``.wav``,
``.mp3``, ``.ogg``, ``.oga``, ``.flac``, ``.opus``.


.. _reference_sounds_methods_on_sound_files:

Methods on sound files
----------------------

.. method:: sounds.filename.play([loops])

    Play the sound. If no argument is given, play once, otherwise loop it a
    number of times.

    :param loops: The number of times to loop. If you pass ``-1`` as the
                  number of times to loop, the sound will loop forever (or
                  until you call ``sounds.filename.stop()``).

.. method:: sounds.filename.stop()

    Stop playing the sound.

.. method:: sounds.filename.get_length()

    Get the duration of the sound in seconds.

.. method:: sounds.filename.set_volume(value)

    Sets the volume of the sound to a float between ``0.0`` and ``1.0``.

    *Note:* The internal value that volume gets set to might be slightly
    different from the one you set. This is because Pygame internally
    represents the volume with a value that has less precision than the float
    you used creating it.

    :param value: The volume to set the sound to in the range from ``0.0``
                  (silent) to ``1.0`` (full volume).

.. method:: sounds.filename.get_volume()

    Returns the volume the sound is set to.

    The same note about volume value precision above applies here too.

    A sound created with ``0.6`` as the volume for example might return
    ``0.59375`` when using ``.get_volume()``.


.. _reference_sounds_methods_on_sounds_builtin:

Methods on sounds builtin
-------------------------

There are two relevant methods that can be called on the ``sounds`` builtin
itself, instead of on a sound file:

.. method:: unload(filename)
    :no-index:

    Removes the sound file called `filename` from the ``sounds`` builtin cache.

    You should not usually need this unless your game is very large and starts
    consuming a lot of memory from all the cached resource files.

.. method:: unload_all()
    :no-index:

    Completely empties the ``sounds`` builtin cache.

    You should not usually need this unless your game is very large and starts
    consuming a lot of memory from all the cached resource files.


.. _reference_sounds_changelog:

Changelog
---------

* **1.4:** First release of PGTurbo after fork from PGZero.
