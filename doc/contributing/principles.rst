Principles of Pygame Turbo
==========================


Please read the following carefully before contributing.

Because Pygame Turbo is aimed at beginners we must take extra care to avoid
introducting hurdles for programmers who have not yet learned to deal with
them.


.. _accessibility:

Make it accessible
------------------

The main aim of Pygame Turbo is to be accessible to beginner programmers.
The design of the API is, of course, influenced by this.

This also applies to things like hardware requirements: Normal size projects
in Pygame Turbo should run on most any hardware so that no one is excluded by
what computer they are running on.


Be conservative
---------------

Early in the development of Pygame Zero (of which Pygame Turbo is a fork), the
developers went backwards and forwards over various features. We put them in,
tried them and took them out again.

Features should be rejected if they are too experimental, or if they might
cause confusion.

This also applies to things like OS support: we disallow filenames that are
not likely to be compatible across operating systems.


One preferred solution
----------------------

In game development broadly, any problem can be tackled in a number of
different ways. Since Pygame Turbo is aimed at people with little experience
however, it should normally offer one clear way to accomplish something
distinct with its API.

As an example, an actor can be moved by changing its ``.x`` property. Because
this is the preferred way in PGTurbo, there should not be a method
``.move_horizontal()`` as well on actors.

In contrast to this, the ``.move_forward()`` and related methods all do
movement relative to the ``.angle`` of an actor, so they accomplish a distinct
purpose and don't interfere with the question "How do I move the actor on the
X axis?"


Just Work
---------

Pygame Turbo wraps Pygame almost completely - but we don't expose all the
features. We expose only the features that work really well without extra fuss,
and hide some of the other features that work less well or need extra steps.


Minimise runtime cost
---------------------

At the end of the day, Pygame Turbo is a games framework and performance is an
issue.

Doing expensive checking every frame to catch a potential pitfall is not really
acceptable. Instead, we might check at start up time, or check only when an
exception is raised to diagnose it and report more information.


Error clearly
-------------

When exceptions are thrown by Pygame Turbo, they should have clear error
messages that explain the problem. It is also preferable for an error to 
occurr during development than for a system to silenty fail in the background,
because a relevant problem might not be discovered that way.


Document well
-------------

Like all projects, Pygame Turbo needs good documentation. Pull requests are more
likely to be accepted if they include the necessary documentation.

Try to avoid complicated sentences and technical terms in the documentation, so
that it is more easily readable by inexperienced programmers.


Minimise breaking changes
-------------------------

In educational environments, users don't always have control of the version of
a library they use. They don't know how to install or upgrade to the latest
version.

It is more important to get the features right first time than in many other
projects.
