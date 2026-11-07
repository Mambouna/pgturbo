.. _deep_dive_resources_and_storage:

Deep dive: resources and storage
================================


.. _deep_dive_resources:

Resource folders
----------------

To use outside resources in your game like images, audio files and different
fonts, you use resources folders. PGTurbo automatically handles file management
for you, so as long as you put your files in the right place and name them
correctly, you can use them easily.

A resource folder is a folder with a set name that will be detected by PGTurbo
if present and used to fetch resource files for you. These folders must always
be placed in the same directory as you game's main ``.py`` file.

The following folders will be detected and used by PGTurbo: *images*, *sounds*,
*music*, *animations*, *fonts*.

The following is an example of a valid folder structure to allow PGTurbo to
find your resource files::

    .
    ├── animations/
    │   ├── ninja_walk_down/
    │   │   ├── wd_1.png
    │   │   └── wd_2.png
    │   ├── ninja_walk_left/
    │   │   ├── wl_1.png
    │   │   └── wl_2.png
    │   ├── ninja_walk_right/
    │   │   ├── wr_1.png
    │   │   └── wr_2.png
    │   ├── ninja_walk_up/
    │   │   ├── wu_1.png
    │   │   └── wu_2.png
    │   └── ninja_jump.png
    ├── fonts/
    │   ├── viga_bold.ttf
    │   ├── viga_italic.ttf
    │   └── viga_normal.ttf
    ├── images/
    │   ├── ninja.png
    │   └── squirrel.png
    ├── music/
    │   └── main_theme.flac
    ├── sounds/
    │   ├── beep.wav
    │   └── boop.ogg
    └── my_game.py

In this example, all five resource folders are used. If you don't have
resources of all types, you don't need to worry. PGTurbo does not complain if
a resource folder doesn't exist, as long as you don't try to load something
from it.


Filename rules
""""""""""""""

The same rules apply for all filenames used for resource files in PGTurbo
games. They are set so that no matter on which operating system your
game is played, there won't be any issues.

The rules are as follows:

* Only use lower case letters, numbers and underscores in filenames.
* Start all filenames with a lower case letter.

As such, the following are all valid filenames::

    wd_1.png
    viga_bold.ttf
    ninja.png
    main_theme.flac
    beep.wav

In contrast, the following are all invalid filenames that could not be used in
a PGTurbo game::

    1.png
    viga-bold.ttf
    Ninja.png
    _main_theme.flac
    sam's beeps.wav

Here are the reasons each is invalid:

#. Starts with a number.
#. Contains the invalid character ``-``.
#. Contains a capital letter.
#. Starts with an underscore.
#. Contains multiple invalid characters (``'`` and a space).

**Important:** In PGTurbo, filenames are ALWAYS given without file extensions.
To access the file *ninja.png*, you always simply write ``ninja``, discarding
the file extension after the period in a full filename.

This also means you cannot have resource files of the same type (two images for
example) that share the same basename but are different file types. There would
be no way to differentiate ``ninja.png`` and ``ninja.jpg`` in the *images*
folder. Having ``ninja.png`` in the *images* folder and ``ninja.ogg`` in the
sounds folder is no problem however, since the resources are not of the same
type.


Resource access
"""""""""""""""

Resource files are accessed in different ways based on their type, but there
are broadly two types:

#. Direct access via the resource loader builtin: *images*, *sounds*, *music*
#. Special acces via other methods that automatically handle loading in the
   background: *images* (actor creation), *animations* (actor animation
   methods), *fonts* (screen builtin text drawing methods)


Direct access
'''''''''''''

To access resources directly, use the builtin named the same as the resource
folder and access a property on it named the same as a resource file without
the file extension::

    images.ninja
    sounds.beep
    music.main_theme

Based on the type of resource, different methods are then available on them::

    images.ninja.get_width()
    sounds.beep.play()
    music.main_theme.play_once()


Special access
''''''''''''''

Actor images are loaded automatically from the *images* resource folder when
you create an actor object::

    player = Actor("ninja", (150, 50))

In this case, the image name is written the same as in the direct access method
but must be a string argument for actor creation.

In a similar manner, animations are loaded automatically from the *animations*
resource folder when adding them to the ``anim`` component of an actor::

    player.anim.add("ninja_walk_down")

As before, filenames are written the same, but as a string argument for the
method.

Lastly, font resources are automatically loaded from the *fonts* resource
folder and can only be used by the following two methods::

    screen.draw.text("Hello World!", center=(50, 50), fontname="viga_bold")
    screen.draw.textbox("Hi...", ((25, 25), (50, 50)), fontname="viga_normal")

Again, filenames are written the same, but are here values for the `fontname`
keyword argument for the text drawing methods of the ``screen`` builtin.


Resource folder references
--------------------------

Since resources of different types do not all share the same purpose and use
they are not all covered in detail here. Instead, the reference pages and
relevant deep dives dealing with resources of that type and supported file
types are given below:

* *images* resource folder:
    * :ref:`Reference page on the images builtin <reference_images>`
    * :ref:`Deep dive on actors <deep_dive_actors>` and
      :ref:`deep dive on the screen builtin <deep_dive_screen>`
    * Supported file formats: ``.png``, ``.gif``, ``.jpg``, ``.jpeg``,
      ``.bmp``, ``.webp``
    * Access resources directly through the ``images`` builtin.
* *sounds* resource folder:
    * :ref:`Reference page on the sounds builtin <reference_sounds>`
    * :ref:`Deep dive on audio <deep_dive_sounds>`
    * Supported file formats: ``.wav``, ``.mp3``, ``.ogg``, ``.oga``,
      ``.flac``, ``.opus``
    * Access resources directly through the ``sounds`` builtin.
* *music* resource folder:
    * :ref:`Reference page on the music builtin <reference_music>`
    * :ref:`Deep dive on audio <deep_dive_music>`
    * Supported file formats: ``.wav``, ``.mp3``, ``.ogg``, ``.oga``,
      ``.flac``, ``.opus``
    * Access resources directly through the ``music`` builtin.
* *animations* resource folder:
    * :ref:`Reference on the animations resource directory <reference_animations>`
    * :ref:`Deep dive on actor animation <deep_dive_actors_animation>`
    * Supported file formats: ``.png``, ``.gif``, ``.jpg``, ``.jpeg``,
      ``.bmp``, ``.webp``
    * Resources cannot be accessed directly, only through
      ``Actor.anim.add()`` and ``Actor.anim.add_spritesheet()``.
    * **Note:** This is a special resource folder in that it not only allows
      single files but also folders. Animations can be loaded either from
      single files containing a spritesheet for an entire animation or from a
      folder containing all the frames for a single animation. More details can
      be found in the reference page and deep dive linked above.
* *fonts* resource folder:
    * :ref:`Reference on the fonts resource folder <reference_fonts>`
    * :ref:`Deep dive on the screen builtin <deep_dive_screen_draw_text>`
    * Supported file formats: ``.ttf``
    * Resources cannot be accessed directly, only through
      ``screen.draw.text()`` and ``screen.draw.textbox()``.


.. _deep_dive_storage:

Data storage
------------

:ref:`Reference page on data storage <reference_storage>`

Many games save data between play sessions, like player progress or
configuration data. To allow this, PGTurbo has the ``storage`` builtin. It
behaves just like a Python dictionary but its contents can be preserved across
game sessions by saving them to a file.

The values you assign to storage will be saved as JSON_, which means you can
only store certain types of objects in it: ``list``/``tuple``, ``dict``,
``str``, ``float``/``int``, ``bool``, and ``None``.

.. _JSON: https://en.wikipedia.org/wiki/JSON


Setting up storage
""""""""""""""""""

The ``storage`` for a game is initially empty. So first, you will want to see
if there is any data that can be loaded from disk::

    storage.load()

This will check if there is saved data associated with your game and if there
is, it will load its contents into the ``storage`` builtin.

If a file was loaded and none of the keys have changed, this is everything you
need. But what if there was no file? You don't want to have to check whether
a key is in storage every time you need to access something in your game.

To help with this, you can use ``storage.setdefault(key, value)``. This method
checks if ``key`` is already in ``storage``. If yes, it does nothing. Only if
the key doesn't exist yet, ``setdefault()`` will put it in ``storage`` and save
the associated ``value`` for that key.

To make sure we can always access a score from ``storage`` for example, we
could put the following code at the start of our game program::

    storage.load()
    storage.setdefault("highscore", 0)

First, we load from disk. If there was a file storing a previous highscore, it
is now loaded and won't be overwritten by ``setdefault()``. But if there was
no file before, we now have ``highscore`` with the value ``0`` in ``storage``
and can safely access ``storage["highscore"]`` anywhere in our game.

To setup your game's persistent data, you could use ``setdefault()`` multiple
times, once for each key and value that should be stored::

    storage.load()
    storage.setdefault("highscore", 0)
    storage.setdefault("player_name", "Unnamed")
    storage.setdefault("last_scores", [])

This is a good way to initialize your ``storage``, but since it can be a lot of
typing, there is a simpler way::

    storage.setup({
        "highscore": 0,
        "player_name": "Unnamed",
        "last_scores": [],
    })

``storage.setup(defaults)`` is a convenience method that just makes the process
of loading and then using ``setdefault()`` multiple times above a bit easier.
It takes a dictionary of keys and values as an argument, loads from disk and
then just runs ``setdefault()`` once for each key value pair in the dictionary.


Manipulating and reading storage
""""""""""""""""""""""""""""""""

After ``storage`` is properly initialized, it's used just like a dictionary
as mentioned above. For example, we can easily update some values::

    if player.colliderect(mushroom):
        score += 5
        if score > storage["highscore"]:
            storage["highscore"] = score

Reading the current value of some item in storage is just as easy::

    def draw():
        # ...
        screen.draw.text("Highscore: " + str(storage["highscore"]), ...)

If a key does not exist in storage, trying to read it will cause an error.
If you want to ensure this doesn't happen, you can also use ``storage.get()``::

    storage.get("highscore", 0)

This would get the value of the highscore if there is one in storage, but if
not, it will return ``0`` instead. If you don't give a second argument, then if
a key is not found, ``None`` is returned.

While this can be handy, it should usually not be necessary if you setup your
storage well at the beginning.


Saving to disk
""""""""""""""

At a checkpoint or based on some other factor in the game, you'll want to save
the current state of the ``storage`` dict back to disk::

    storage.save()

That's it, simple as could be.

In many cases, it's fine to save manually, but sometimes you might want to
save any change to disk immediately. For this, you can enable autosave mode for
``storage``::

    storage.autosave = True

This is best done at the start of the program, for example directly before or
after ``storage.setup()``. When ``storage.autosave`` is ``True``, whenever a
value is set with ``storage[key] = value``, a save is automatically triggered
right afterwards.


Setting a specific storage state
""""""""""""""""""""""""""""""""

We know how to load, setup, change and save ``storage``, but what if we need
to set all its contents to a specific state? For example, a new game was
started so everything should go back to a starting point.

We can't use ``setup()`` or ``setdefault()`` for this, since they won't change
values that already exist in ``storage``. Instead, we can use another method::

    storage.overwrite({
        "highscore": 0,
        "player_name": "Unknown",
        "last_scores": [],
    })

This looks very similar to using ``setup()`` above. The difference is that
``storage.overwrite(new_state)`` erases everything that was previously in
``storage`` and then fills it with the data from the dictionary argument given.

* For getting everything ready at the start of the game: ``storage.setup()``.
* For resetting the state of ``storage`` to a specific point while deleting
  everything previously saved: ``storage.overwrite()``.

If you ever get the state of ``storage`` mixed up in some way with old keys
and values hanging around or are otherwise stumped, you can always completely
erase everything with ``storage.clear()``. Note this does not save
automatically, so if you want to reset the file on disk as well you'll need to
do the following::

    storage.clear()
    storage.save()
