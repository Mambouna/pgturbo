.. _tutorial_images_sounds_and_music:

Tutorial: Images, sounds and music
==================================

Now that we've got the playing part figured out, it would be nice if the
look and feel of our game improved. Programming first with rough shapes and
outlines before spending time on art assets can be a good strategy, because
you'll likely change many things before being happy with your game's mechanics.
If you started with the art you might have to redo a lot of effort multiple
times. Instead, we are happy with how the game works, so now we can focus on
making it prettier.

To do that, first download
:download:`this archive file </_downloads/3_images_sounds_and_music_assets.zip>`
and extract it somewhere. Then copy the folders *images*, *sounds* and *music*
next to your game's ``.py`` file.

These specific folder names put next to your game's main file are automatically
recognized by PGTurbo as resource folders, allowing you to easily load and use
the assets in them.

First, we'll just replace our current ellipse player actor with one that uses
the image of a ninja. For this, replace the line creating the player actor with
the following::

    # Previously: player = Actor.Ellipse(40, 60, "lightblue")
    player = Actor("ninja")

Run the game again and you'll see the image of a ninja in blue clothes instead
of the previous ellipse.

#. First, notice that there's no second word after ``Actor`` anymore. Actors
   that use simple shapes are handy, but they are usually placeholders. So
   defining a "normal" actor just works via ``Actor(imagename)``.
#. Second, how does the string ``"ninja"`` put an image in the game? This has
   two parts. Because there is a folder named *images* next to our game ``.py``
   file, PGTurbo knows to look there if we need to do anything to do with image
   files. PGTurbo also automatically handles file extensions for us, so you
   never have to write out ``ninja.png`` or ``apple.jpg``, just ``ninja`` or
   ``apple``. So PGTurbo knows where it can find image files. The other part is
   that actors always need an image, so when we just use ``Actor()`` to create
   one, PGTurbo knows the first argument we give is a string representing an
   image file.
#. The rest of the program can stay the same, because other than displaying an
   image, simple shape actors and normal ones behave exactly the same.

Next, the food our ninja eats should also look nicer. But if everything was the
same, it might be a bit repetitive. Instead, let's randomly choose an image
from a selection of options for each new food item::

    # food_items = [] is above here    

    food_images = ["apple", "pumpkin", "potato", "carrot"]

    # def new_food(): is below here

            # Previously: fresh_food = Actor.Triangle(30, 30, "orange")
            food_image = random.choice(food_images)
            fresh_food = Actor(food_image)
            fresh_food.scale = 2.0

            # fresh_food.x = random.randint(20, WIDTH - 20) is below here

Now each food item comes with one of four different images.

#. We define a simple list of strings to use for random images. Since we just
   give ``Actor()`` a string to lookup for the image, we can just use one out
   of a selection to have different images for actors.
#. We can pick a random element from a list with ``random.choice(list)``, so we
   do so before creating the new actor instance for fresh food.
#. Since the food images are a little small, we double their size with
   ``fresh_food.scale = 2.0``. Actors at normal scale (``1.0``) always display
   their images exactly at their original pixel size. To make the actor have
   the right relative size in your game, you can either scale the original
   image file up or down, or use the ``.scale`` parameter of actors.

So the game looks more interesting, but we can still do more. Feedback to
player actions is important for any game, so eating a food item could play a
sound to underscore it::

    # player.data["score"] = player.data["score"] + 1 is above here
    
                if player.data["score"] % 10 == 0:
                    sounds.powerup.play()
                else:
                    sounds.bite.play()

    # else: is below here

Each eaten item will play a short bite sound and every ten scored points a
triumphant sound rings out.

#. Working with sonds looks a bit different than images, because those are so
   often used as part of an actor. This is a better example of how accessing
   resource files directly looks like. With ``sounds.filename`` we can act on
   any audio files in a *sounds* folder next to our game's ``.py`` file.
#. To then play a sound, we simply call ``.play()`` on it. This will
   play the sound once without repeating it.
#. To be able to access resources via ``resource_loader.filename``, the names
   of those resource files must follow certain rules. In general, you must name
   any file you want to use as a resource for your game such that it could also
   be the name of a variable in Python. ``3beeps.wav`` for example would not
   work, because it starts with a number.

The ``sounds`` builtin is well suited for playing short sound effects. Music
for games often has far larger files however, so to play them, a different
builtin is used::

    # def new_food(): is below here

    music.set_volume(0.35)
    music.chill.play()

    # def new_food(): is below here

Now the game has a nice soundtrack.

#. The ``music`` builtin allows us to access files in the *music* folder, just
   like ``sounds`` does for files in the *sounds* folder.
#. A key difference is that while many sounds can play at once, only one piece
   of music can play at a time. If you start playing something while another
   track is running, it will stop and the new one begins.
#. Before starting to play a track, we set the general music volume with
   ``music.set_volume(0.35)``. The values are between ``0.0`` (silent) and
   ``1.0`` (full volume).
#. Then we play the track we want with ``music.chill.play()``.

   A difference to ``sounds`` is that music tracks automatically loop when you
   call ``.play()`` on them. This way, if you set one track, it will keep
   playing unless you specifically stop it or set a different piece to play.

**Now our game has a soundtrack, sound effects and images moving on screen.**

Although it could be said the images aren't properly *moving* yet.
:ref:`The last follow-along tutorial on animating actors <tutorial_animating_actors>`
remedies this.

:ref:`The overview page <overview>` is an alternate place to learn more about
the different options in PGTurbo.
