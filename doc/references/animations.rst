.. _reference_animations:

Reference: animations
=====================

:ref:`Deep dive on actor animation <deep_dive_actors_animation>`

The *animations* resource directory is exclusively used by actors through their
``anim`` component for sprite animation. In contrast to ``images`` or
``sounds``, there is no direct use case for manipulating animation resources.

Because of this, the *animations* resource directory is not accessible through
a builtin. All interactions with it happen through ``Actor.anim.add()`` or
``Actor.anim.add_spritesheet()``.


.. _reference_animations_location_filenames_and_formats:

Location, filenames and formats
--------------------------------

The *animations* resource directory finds all valid animation spritesheet files
or animation folders in a directory called *animations*, placed next to your
game's main python file.

Animation resources can be represented in two different ways:

#. One folder in the main *animations* folder for one animation with the folder
   containing single images that make up the animation frames. The alphabetical
   order of image names determines the order of frames in the animation.
#. One spritesheet file for one animation directly in the main *animations*
   folder with the image containing all individual frames for the animation
   ordered either from left to right or top to bottom and with each frame
   having the same dimensions.

Filenames and folder names can consist of lowercase letters, numbers and
underscores and must start with a letter. This goes for single spritesheet
animation files, folders containing single animations and individual frame
files in the folders.

For example, these filenames and folder names are valid::

    alien_walk_spritesheet.png
    alien_hurt/
    alien_hurt/alien_hurt_7.png

These filenames and folder names are not valid::

    Alien_walk_spritesheet.png
    ALIEN_SPRITESHEET.png
    3/
    3/4.png
    my-cat/
    sam's dog running.png

The following file formats can be used for animation resources: ``.png``,
``.gif``, ``.jpg``, ``.jpeg``, ``.bmp``, ``.webp``.

Any other files or folders inside animation resource folders are ignored.


.. _reference_animations_changelog:

Changelog
---------

* **1.16:** Added ``.webp`` format for animation resource frame images and
  spritesheets. Also fixed a bug where other files and directories present in
  an animation folder would cause warnings or errors.
* **1.4:** First release of PGTurbo after fork from PGZero.
