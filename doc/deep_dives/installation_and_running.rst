.. _deep_dive_installation_and_running:

Deep dive: Installation and running a game
==========================================


.. _deep_dive_installation_python:

Optional: installing Python
---------------------------

To develop games with PGTurbo, you first have to make sure Python is installed
on your system. If you already have Python installed, you can skip to the next
section.

If you aren't sure of this, open a terminal or command prompt and type
``python`` before hitting enter. If you have Python installed, an interactive
console should appear that shows at the top ``Python`` and a version number. To
quit the interactive console, type ``exit()`` and hit enter again.

If instead you got some sort of error, it's likely Python is not installed on
your system. In this case, there are different options for installation based
on your operating system:

* Windows: Install the *Python Install Manager* from the Microsoft Store and
  follow the instructions to install Python system wide and on PATH.
* MacOS: Go to the `Python website <https://www.python.org/downloads>`__ and
  download the ``.pkg`` installer of the current Python version for MacOS.
  After the download is complete, execute the installer and follow the
  instructions to complete the installation.
* Linux: Most modern Linux distributions come with Python pre-installed. If
  your system does not have it however, install the ``python3`` package with
  your system's package manager.

To check if everything is working correctly, restart your system, open another
terminal or command prompt and execute the ``python`` command again. If
installation was successful, the interactive Python shell should now appear and
you can quit it with the ``exit()`` command.


.. _deep_dive_installation:

Installing PGTurbo
------------------

With Python installed, you can install python packages with the PIP package
manager. To install PGTurbo, just run the following command::

    python -m pip install pgturbo

This will install PGTurbo as well as its dependencies ``pygame-ce`` and
``numpy``. ``pygame-ce`` is the base Pygame package that PGTurbo builds all
its convenient features on top of. ``numpy`` is a very popular and
comprehensive Python package around numbers, maths and anything related to
those that PGTurbo uses to synthesize waves for tone generation. It's often
already installed, but not always.

To test that installation was successful, open a terminal or command prompt
and execute the following command: ``pgtrun``. This should print a line
of text starting with ``pygame-ce`` and then a version number, followed by
an error message telling you that an argument named *game* is required.

While an error is usually bad, in this case it tells us that PGTurbo is
successfully installed on the system. The next section will show you how to
actually run a game with a ``.py`` file as its code.


.. _deep_dive_running:

Running a game
--------------

First, navigate to somewhere on your file system you want to store your games
at, maybe somewhere in the user *Documents* folder. Once there, create an empty
text file called ``game.py``.

Then open a terminal or command prompt in the same location and run the
following command::

    pgtrun game.py

This should open a black window with nothing happening in it. Congratulations,
you're running your first PGTurbo game!

You can quit the game by clicking on the window's close button or by pressing
``Ctrl-Q`` (``⌘-Q`` on Mac). If the game stops responding for any reason, you
may need to terminate it by pressing ``Ctrl-C`` in the terminal or command
prompt you used to run the game.

That worked because everything in Pygame Turbo is optional. A blank file is a
valid PGTurbo script.


.. _deep_dive_running_pgtrun:

Running via pgtrun
""""""""""""""""""

The above method (``pgtrun GAMESCRIPT``) is one of two ways you can execute
a Pygame Turbo game program. The first is the terminal command ``pgtrun``
followed by a file path to the main ``.py`` file of your game.

Alternatively, you can keep your game project in its own project folder (for
example a folder named ``my_game``) and then run the game with ``pgtrun
FOLDERPATH`` instead. As long as the main ``.py`` file of your game in the
project folder is either named the same as the folder itself or is named
``main.py``, PGTurbo will find it and correctly run it.


.. _deep_dive_running_python:

Running with python
"""""""""""""""""""

If you are not as familiar with command prompts or usually work in an IDE with
its own "Run program" button or similar, there's another easy way to run your
games.

Place ``import pgtrun`` at the top of your game's main ``.py`` file and put
``pgtrun.go()`` at the bottom of the same file. With this done, you can run
PGTurbo games through normal python script execution.

That could be pressing the "Run program" button in your IDE or also from the
command line with ``python game.py``. The only downside to this is that you
have to run the main script directly, ``python FOLDERPATH`` will not work.

To expand on your game's code then, you place all of the game logic between
the first and last lines (``import pgtrun`` and ``pgtrun.go()``). This is so
there's nothing of the game code that Pygame Turbo misses when executing.

If you've used the above method, you can still run the game with
``pgtrun game.py``, but the other way around does not work. You cannot run
PGTurbo by just placing your game logic in a Python file and then directly
executing it with Python.


.. _deep_dive_running_project_structure:

Recommended project structure
-----------------------------

It's usually a good idea to put each game project in its own folder. This is
because beside the main Python file you run to start your game, you will likely
create other Python files to use. Additionally, your game will need graphics
like image files and audio files for sound or music. These resources need to
be placed in specific folders next to your main game file.

If you were to put different main game files directly next to each other, their
resource folders would all get mixed up. The details of how exactly those
folders need to look is not relevant for this deep dive. You can find out more
about it in the :ref:`deep dive on resources <deep_dive_resources>`.

When putting your game projects in their own folders, just make sure that the
main ``.py`` file is either named the same as the folder or is named
``main.py``, so that PGTurbo can find it if you use ``pgtrun`` to execute it.

The following is an example of valid folder structure for a game project
called "ninja_hideaway"::

    .
    └── ninja_hideaway/
        └── main.py

Or alternatively::

    .
    └── ninja_hideaway/
        └── ninja_hideaway.py
