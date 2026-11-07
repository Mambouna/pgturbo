.. _reference_music:

Reference: music
=================

:ref:`Deep dive on music <deep_dive_music>`

*Note:* Since methods can be used either directly on the ``music`` builtin or
on individual music files, all methods are shown here with their full call
text (so ``music`` is not implied before each method but rather it is always
explicit).

.. _reference_music_methods_on_files:

Methods on music files
----------------------

.. method:: music.filename.play()

    Play the music track, looping indefinitely.

    This replaces the currently playing track and cancels any tracks previously
    queued with ``queue()``.

    You do not need to include the extension in the track name; for example, to
    play the file ``handel.mp3`` on a loop::

        music.handel.play()

.. method:: music.filename.play_once()

    Similar to ``play()``, but the music will stop after playing through once.

.. method:: music.filename.queue()

    Prepares the track to be played once after the current track finishes
    playing. This only makes sense to use if you used ``play_once()`` before.
    If you have the current music looping indefinitely, the queued track will
    never play.


.. _reference_music_general_methods:

General music methods
---------------------

.. method:: music.stop()

    Stop music playback.

.. method:: music.pause()

    Pause the music temporarily. It can be resumed by calling ``unpause()``.

.. method:: music.unpause()

    Unpause music playback that was previously paused.

.. method:: music.is_playing()

    Returns ``True`` if music is currently playing, ``False`` otherwise.

.. method:: music.is_paused()

    Returns ``True`` only if there is a current music track but it is paused,
    ``False`` otherwise.

.. method:: music.fadeout(duration)

    Fade out and eventually stop the current music playback.

    :param duration: The duration in seconds over which the sound will be faded
                     out. For example, to fade out over half a second, call
                     ``music.fadeout(0.5)``.

.. method:: music.set_volume(value)

    Set the volume of the music system between ``0.0`` and ``1.0``.

    By default, the music volume is set to ``0.75``.

    *Note:* The internal value that volume gets set to might be slightly
    different from the one you set. This is because Pygame internally
    represents the volume with a value that has less precision than the float
    you used creating it.

    :param value: The volume to set the music system to in the range from
                  ``0.0`` (silent) to ``1.0`` (full volume). Values outside the
                  range are clamped to zero and one.

.. method:: music.get_volume()

    Get the current volume of the music system.


.. _reference_music_deprecated_methods:

Deprecated general methods
--------------------------

Currently, it is recommended to interact with music files via
``music.filename.method()``. For backwards compatibility, the following methods
are still available to use with the ``music`` builtin directly:

.. method:: play(name)

    Play the music track, looping indefinitely.

    This replaces the currently playing track and cancels any tracks previously
    queued with ``queue()``.

    You do not need to include the extension in the track name; for example, to
    play the file ``handel.mp3`` on a loop::

        music.play("handel")

    :param name: String name of the music file to play without the file
                 extension.

.. method:: play_once(name)

    Similar to ``play()``, but the music will stop after playing through once.

    :param name: String name of the music file to play without the file
                 extension.

.. method:: queue(name)

    Prepares the track to be played once after the current track finishes
    playing. This only makes sense to use if you used ``play_once()`` before.
    If you have the current music looping indefinitely, the queued track will
    never play.

    :param name: String name of the music file to play without the file
                 extension.


.. _reference_music_changelog:

Changelog
---------

* **1.12:** Music system rework with backward compatibility retained.
* **1.4:** First release of PGTurbo after fork from PGZero.
