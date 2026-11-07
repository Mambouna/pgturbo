.. _deep_dive_audio:

Deep dive: audio
================


.. _deep_dive_sounds:

Sounds
------

:ref:`Reference page on the sounds builtin <reference_sounds>`

The ``sounds`` builtin is a resource loader for audio files. In short, audio
files placed in a folder named *sounds* next to your game's ``.py`` file can be
automatically loaded by PGTurbo vie their file name without the file extension.
For more details on resource folders, read the reference page linked above.

Let's assume a file structure as follows for our game ``game.py``::

    .
    ├── sounds/
    │   └── beep.wav
    └── game.py

With this setup, you can play the sound *beep.wav* by calling
``sounds.beep.play()``. You can access any sound file with ``sounds.filename``
and then have a number of methods available to start or stop playing those
sounds, set their volume and other settings:

* ``sounds.filename.play()`` plays the sound once. If you call the method with
  a number as an argument, then the sound will play on loop for the given
  number of times. For example: ``sounds.beep.play(3)`` will loop three times.
* ``sounds.filename.stop()`` interrupts a sound if it is being played.
* ``sounds.filename.get_length()`` will return the duration of the sound file
  in seconds.
* ``sounds.filename.set_volume(value)`` will set the loudness of the sound when
  it is played between ``0.0`` (silent) and ``1.0`` (full volume).
* ``sounds.filename.get_volume()`` returns what volume a sound is currently
  set to, although the value might be a bit off from what you last set. That is
  because Pygame internally represents sound volume with less precision than a
  full ``float`` value allows.

*Note: Sound loudness is not perceived linearly by humans, so a volume value
half that of another will not sound half as loud to your ears. Experiment to
see what values work best for you.*

Up to eight sounds can play at the same time and PGTurbo automatically manages
dropping previously started sounds when a new one that would go over that limit
is called to play. Here's an example where multiple sounds will play at once::

    def on_key_down(key):
        if key == keys.SPACE:
            # ... Actor movement, animations, etc. ...
            sounds.swing_sword.play()

            if hero_sword.colliderect(enemy):
                sounds.enemy_hurt.play()

Here, the sound effect ``swing_sword`` is always played when the space key is
pressed and only if an enemy is hit also ``enemy_hurt``. When this happens, the
first sound effect is not finished yet though, but that's not an issue.

You should avoid using the ``sounds`` builtin to play longer audio files.
Because the sound system will fully load the audio file into memory before
playing it, this can use a lot of memory, as well as introducing a delay while
the audio is being loaded.


.. _deep_dive_music:

Music
-----

:ref:`Reference page on the music builtin <reference_music>`

Instead, when you want to player longer audio files (usually music for your
game), use the ``music`` builtin instead. Just like ``sounds``, ``music`` is
a resource loader.

Any audio files you place in a folder called *music* next to your game's main
``.py`` file will be available via ``music.filename``. Details on the resource
folder are again found in the reference page linked above.

The ``music`` builtin is suited to playing long audio files because it loads
tracks into memory in small chunks, avoiding large memory use and delays during
costly loading operations for whole files.

Expanding the file structure example above, we could introduce a piece of
music like this::

    .
    ├── music/
    │   ├── main_theme.wav
    │   └── scary.wav
    ├── sounds/
    │   └── beep.wav
    └── game.py

With this, we can play a piece of music with ``music.main_theme.play()``.

There are a few differences between ``music`` and ``sounds`` you should be
aware of:

#. Only one music track can play at a time. If you call ``.play()`` on a music
   file while another is running, the previous one is stopped and the new one
   started.
#. Music tracks loop indefinitely by default, while sounds are played only once
   by default.
#. There's a number of methods on the ``music`` builtin directly to control
   playback settings instead of for each file individually like with
   ``sounds``.


Playing music
"""""""""""""

The following methods are available to play a piece of music:

* ``music.filename.play()`` will start a piece of music and keep looping it
  indefinitely.
* ``music.filename.play_once()`` will instead only run a piece of music once.
* ``music.filename.queue()`` will prepare this music track to play once when
  the previous one has finished. This only really makes sense if you used
  ``play_once()`` before since if the previous music is looping forever, the
  queued piece of music will never play.

The queue of the music system allows you to prepare multiple pieces of music
in advance. Let's say there's a tense section coming up in your game. You can
first play an appropriate piece of music to set the mood before returning to
another one::

    music.scary.play_once()
    music.main_theme.queue()

Only one piece of music can be queued at a time. If you call ``.queue()`` on
a track while another one was in the queue already, it will replace the
previous one.


Interrupting music playback
"""""""""""""""""""""""""""

Since only one piece of music can play at a time, the methods to stop playback
don't sit with each individual music file, but the ``music`` builtin itself:

* ``music.stop()`` will interrupt music playback and stop it completely.
* ``music.pause()`` will also interrupt it but keep a record of where the music
  was left at to be able to unpause it later.
* ``music.unpause()`` does just that. If playback was previously paused, it
  picks back up exactly where it was left.
* ``music.fadeout(duration)`` will turn down the volume of the currently
  playing music track over the given duration in seconds before stopping
  playback.

You can check the current playback state with two more methods:
``music.is_playing()`` and ``music.is_paused()``. The first will return
``True`` if playback is currently happening and ``False`` if not, no matter if
due to a pause or just no music being in play. The second will return ``True``
only if playback is currently paused, but ``False`` is music is either playing
or no music is in playback at all.


Volume
""""""

Where you can set the volume for each sound effect individually, the settings
for music playback are also centralized in ``music.set_volume(value)`` and
``music.get_volume()``.

Other than being part of the ``music`` builtin itself, they work the same way
volume methods worked for sound effects with values between ``0.0`` and ``1.0``
and returned values possibly being slightly off from what you set due to
internal representation precision.


On_music_end
""""""""""""

Lastly, there is an event hook associated with the music system:
``on_music_end()``. It will be triggered whenever music stops playing, so both
when you stop playback explicitely with ``music.stop()`` but also when a track
you played with ``music.filename.play_once()`` is done. 

It does NOT trigger when a looping track finishes playing through once and
begins to play again.

You can read more about event hooks in the
:ref:`relevant deep dive on the topic <deep_dive_hooks_general_hooks>`.


.. _deep_dive_tone:

Tone generation
---------------

:ref:`Reference page on tone generation <reference_tone>`

If you don't have audio files to use for sound effects yet, you can also let
Pygame Turbo generated simple sine wave tones for you. These sound rather
artificial, so you'll likely want to use them mostly as placeholders until you
have proper assets to use.

You generate and play these synthesized sounds via the ``tone`` builtin. Here's
a simple example::

    tone.play(440, 1.5)

This will generate and immediately play a sine wave at 440 Hertz for one and a
half seconds. The first argument for ``tone.play()`` determines the pitch of
the note, the second the duration in seconds.

The pitch can be given as a simple number of Hertz to use for the frequency or
instead a special kind of string representing a musical note. To generate the
same note as above with this string representation, you would call
``tone.play("A4", 1.5)``.

The special string is made up of two or three characters as follows:

#. An uppercase letter giving the chroma of the note (C, D, E, F, G, A, B as in
   musical scales).
#. Optionally the characters ``#`` or ``b`` to raise or lower the note by a
   half step.
#. A number to indicate the octave for the note.

As such, ``"A4"`` is the standard note used for tuning many instruments at
``440`` Hertz, while middle C would be ``"C4"`` at ``261.626`` Hertz.

As an optional argument, you can also specify with what volume the generated
tone should play: ``tone.play("Eb3", 1.0, 0.5)``. The third argument here is
a volume value and works the same way they do for sound effects and music.

**Important:** Because synthesizing audio on the fly is expensive, no sounds
longer than four seconds can be generated. Trying to do so will cause an error
and crash the game.


Saving tones
""""""""""""

If you plan to use a single sound effect multiple times, it can be wasteful to
keep generating, using and then discarding it again. Instead, you can have the
tone be generated and store it in a variable to use how ever many times you
wish later::

    warning_sound = tone.create("A#3", 1.0)

    def on_key_down():
        warning_sound.play()

The sound effects generated by ``tone`` are the same type of object that the
``sounds`` builtin uses, meaning all the same methods are available on them:

* ``.play()`` with optional number argument for how many times to loop.
* ``.stop()`` to interrupt a playing sound.
* ``.get_length()`` to check the duration in seconds.
* ``.set_volume(value)`` to set loudness which defaults to ``0.75``.
* ``.get_volume()`` to check loudness with some imprecision.

The ``tone.create()`` method also allows you to set the volume directly at
creation of a sound object: ``warning_sound = tone.create("A#3", 1.0, 1.0)``.
This would have created the warning sound with full volume already set.
