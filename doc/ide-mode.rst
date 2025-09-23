Running Pygame Turbo in IDLE and other IDEs
===========================================

.. versionadded:: 1.2

Pygame Turbo is usually run using a command such as::

    pgtrun my_program.py

Certain programs, such as integrated development environments like IDLE and
Edublocks, will only run ``python``, not ``pgtrun``.

Pygame Turbo includes a way of writing a full Python program that can be run
using ``python``. To do it, put ::

    import pgtrun

as the very first line of the Pygame Turbo program, and put ::

    pgtrun.go()

as the very last line.


Example
-------

Here is a Pygame Turbo program that draws a circle. You can run this by pasting
it into IDLE::


    import pgtrun


    WIDTH = 800
    HEIGHT = 600

    def draw():
        screen.clear()
        screen.draw.circle((400, 300), 30, 'white')


    pgtrun.go()
