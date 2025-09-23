Pygame Turbo
============

A quicker moving fork of the zero-boilerplate games programming framework
Pygame Zero, based on Pygame.

The documentation for Pygame Turbo is found here:
https://pgturbo.readthedocs.io/

The documentation for Pygame Zero is found here:
https://pygame-zero.readthedocs.io/en/stable/index.html

The GitHub of Pygame Zero is found here: 
https://github.com/lordmauve/pgzero


Switching to Pygame Turbo
-------------------------

If you've been working with Pygame Zero so far and want to use some of the
new features in Pygame Turbo, it's easy to switch over.

First, install the ``pgturbo`` pip-package::

    pip install pgturbo

If you've been running your game with the command ``pgzrun`` from the command
line, you can simply switch to running it with the command ``pgtrun`` instead.

If you've been using ``import pgzrun`` and ``pgzrun.go()`` in your main script,
you only have to change these to ``import pgtrun`` and ``pgtrun.go()``.

That's it!


Divergence to Pygame Zero
-------------------------

This is a changelog which keeps track of which changes exist in respect to the
main Pygame Zero project. If and when those features are added to Pygame Zero,
they will be removed from the running list.


New features
''''''''''''

* A proper ``mouse`` builtin to get the state of different mouse properties
  like positions, relative movements, state of buttons being pressed and
  more. Also allows changing of visibility, cursor shape and others.


Feature enhancements
''''''''''''''''''''

* Pixel perfect collision check between two actors via
  ``actor1.collidemask(actor2)``.
* Angle and target-based movement functions for Actors, similar to what is
  possible in Scratch and other environments.
* Velocity property and movement function for Actors that only move in
  straigth lines. Also includes an intercept function to calculate necessary
  velocity to meet a target actor that also has a constant velocity.
* Create Actors from simple shapes without needing an image, via
  ``Actor.Rectangle(width, height, color)``,
  ``Actor.Ellipse(width, height, color)`` and
  ``Actor.Triangle(width, height, color)``.
* Function to check if an actor is currently withing the screen bounds:
  ``.is_onscreen()``.


Bug fixes
'''''''''

* Fixed ``music.is_playing()`` requiring an argument.
* Made actor ``width`` and ``height`` read-only properties while no solution
  for scaling actors is implemented.

Integrated changes
''''''''''''''''''

These former divergences between Pygame Turbo and Pygame Zero have been
introduced to Pygame Zero itself:

None so far.
