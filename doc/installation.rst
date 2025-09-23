Installing Pygame Turbo
=======================

On desktop systems
~~~~~~~~~~~~~~~~~~

::

    pip install pgturbo

This will also install Pygame. Pre-compiled Pygame packages are available to pip
for Windows & Linux (32-bit and 64-bit), and for Mac OS (64-bit only). If you
have a different system, you'll need to find a way to install pygame first. Make
sure you are using Python 3 not Python 2.

Mac
'''

In a Terminal window, type

::

   pip install pgturbo


Note that there are currently no Wheels for Pygame that support python 3.4 for Mac,
so you will need to upgrade Python to >=3.6 (or use python 2.7) in
order to be able to install pygame. For a list of available Wheels, please visit
`pyPI_`

.. _pyPI: https://pypi.org/project/Pygame/#files

Linux
'''''

In a terminal window, type

::

   sudo pip install pgturbo


Some Linux systems call it ``pip3``; if the above command printed something
like ``sudo: pip: command not found`` then try::

    sudo pip3 install pgturbo

Sometimes pip is not installed and needs to be installed. If so try this before
running the above commands again::


    sudo python3 -m ensurepip


For flake8/pyflakes
~~~~~~~~~~~~~~~~~~~

Checkers like Pyflakes are unaware of Pygame Turbo's extra builtins.

If you use ``flake8``, you can add Pygame Turbo's list of builtins to your
`flake8 configuration file <https://flake8.pycqa.org/en/latest/user/configuration.html>`_:

.. code-block:: ini

    [flake8]
    builtins = Actor,Rect,ZRect,animate,clock,exit,images,keyboard,keymods,keys,mouse,music,screen,sounds,storage,tone

If you use `pyflakes` directly then this is configured using the environment
variable ``$PYFLAKES_BUILTINS``. On Linux and Mac you could write this in your
terminal or put it in your shell configuration file (like ``~/.bashrc``)

.. code-block:: bash

    PYFLAKES_BUILTINS=Actor,Rect,ZRect,animate,clock,exit,images,keyboard,keymods,keys,mouse,music,screen,sounds,storage,tone
    export PYFLAKES_BUILTINS

On Windows:

.. code-block:: none

    set PYFLAKES_BUILTINS=Actor,Rect,ZRect,animate,clock,exit,images,keyboard,keymods,keys,mouse,music,screen,sounds,storage,tone
