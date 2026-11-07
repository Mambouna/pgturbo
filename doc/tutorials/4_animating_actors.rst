.. _tutorial_animating_actors:

Tutorial: Animating actors
==========================

The last really big feature most games have that we haven't covered yet are
animations. Instead of static images moving around on the screen, animations
play out so that character appear properly alive. PGTurbo has a flexible and
powerful sprite animation system for actors, which we'll use to liven up our
ninja player character.

As in the last tutorial, you first need to download
:download:`this archive file </_downloads/4_animating_actors_assets.zip>` which
contains the animation sprites we are going to use. Extract the archive and
copy the *animations* folder next to your other resource folders like *images*
and *music*.

The *animations* folder works as follows: It contains one folder for each
animation resource. Each of those single animation folders in turn contain a
number of images, which make up the animation. The sorting order of the
images in the folders determine the order of frames for the animation, so
always make sure to name your files so everything is in the correct order.

As an example, the *animations* folder contains the folder *walk_up*. This
means PGTurbo will find an animation resource named ``walk_up``. In this folder
there are four image files, named the same except for numbering, to make sure
they are in the correct order. So the animation resource found by PGTurbo has
four frames in the animation.

With that out of the way, let's get our animations into the game::

    # player = Actor("ninja") is above here

    player.anim.add("walk_up")
    player.anim.add("walk_down")
    player.anim.add("walk_left")
    player.anim.add("walk_right")

    # player.pos = (WIDTH / 2, HEIGHT / 2) is below here

#. The ``Actor.anim`` component manages everything to do with actor animations.
   This is because there's quite a few methods and properties associated with
   animations, so accessing them all through ``Actor.anim`` is tidy.
#. The ``Actor.anim.add(animation_name)`` method loads an animations resource
   from the *animations* resource folder into the actor the method is called
   on, making it ready to use.
#. Since we have four animation, one for each direction the actor can move in,
   we need to call this four times to load all the animations.

Importantly, adding animations does not automatically play them. As such, it's
recommended to add all the necessary animations for an actor in your game's
startup code or when it is being created, so you can safely and easily use them
all later.

Now we just have to play each animation based on the movement direction of the
ninja::


        # player.x = player.x - 5 is above here

        player.anim.play("walk_left")

    # if keyboard.right: is below here

        # player.x = player.x + 5 is above here

        player.anim.play("walk_right")

    # if keyboard.up: is below here

        # player.y = player.y - 5 is above here

        player.anim.play("walk_up")

    # if keyboard.down: is below here
        
        # player.y = player.y + 5 is above here

        player.anim.play("walk_down")


    # i = 0 is below here

#. ``Actor.anim.play(animation_name)`` starts playing an animation if it is
   not already playing. This makes it perfect for circumstances like this.
   If the player is pressing a new movement key, we start playing the correct
   animation. But if they are just holding down the same key, we don't restart
   the animation until is has played out fully once, at which point it is
   started again the next frame.
#. Since it's no problem for a different animation to start on the same frame,
   simply overwriting the previously set one, we also don't have to worry about
   getting into conflicts from moving both up and left at the same time for
   example.
#. The only snag is that if the player stops holding down any movement keys,
   the last active animation will still play out fully. This can be fixed in a
   number of different ways with different benefits and drawbacks.

**Now we're well and truly done with the game!**

Or are we? There's certainly a lot that could be improved upon, but we'll let
you figure that out yourself if you want to. One big thing would be to have a
way for the game to end. A few ideas might be a timer that runs out, a target
number of points to gather before it's over or to have some of the food be
rotten, with the game ending when such a food item is mistakenly eaten.

Of course, any other ideas you have to improve on this are a great as well.
Learning is always done best by doing, so start doing by tinkering with this
project or start a new one yourself.

For resources, you can find the :ref:`PGTurbo overview page here <overview>`.
Each section in the overview links to deep dives that explore the different
options of PGTurbo in a lot more depth than was possible in these short
tutorials.
