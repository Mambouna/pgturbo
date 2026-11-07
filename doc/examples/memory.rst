.. _example_memory:

Example game: Memory
====================

:ref:`Back to the overview <examples_overview_memory>`

.. image:: /_static/examples/memory.png
   :alt: Memory
   :height: 500
   :align: center

:download:`Download the project archive here </_downloads/memory.zip>`

This explainer will go into detail on how the code of the *memory* example game
works.

*If you want to learn from it, it's recommended you first have a look through
the source code yourself. Try to understand the overall structuring of the
project and then see if you can understand what the different parts of the code
do. You can also make changes and run the project a couple of times to see how
they affect the game.*

Once you've done so, feel free to read through this explainer to clear up any
confusion or misunderstandings.


Structure
---------

This general structuring is shared by all the example projects:

#. Imports (usually for PGTurbo and getting random values)
#. Definitions of game window global variables and game mechanics constants
#. Different sections setting up all the actors and their functions for the
   project
#. Event hook function definitions
#. Game loop function definitions (for update and drawing)

In the *memory* project, the section defining game window globals is placed
under the one defining game mechanic constants. This is because the width and
height of the game window are determined by the values of some constants.
Because of this, the constants have to be defined before the game window
variables::

    COLUMNS = 4
    ROWS = 3
    GRID_SIZE = 200

    # ... More constants here ...

    WIDTH = COLUMNS * GRID_SIZE
    HEIGHT = ROWS * GRID_SIZE


Game window global variables
----------------------------

.. code::

    TITLE = "Memory"
    WIDTH = COLUMNS * GRID_SIZE
    HEIGHT = ROWS * GRID_SIZE

As shown above, the ``WIDTH`` and ``HEIGHT`` are set from some game mechanics
constants. The way their values are calculated effectively makes it so the game
window contains a grid of exactly ``COLUMNS`` grid cells across and ``ROWS``
grid cells from top to bottom. Each grid cell has width and height
``GRID_SIZE``.

Doing it this way allows using the constants to change how complex the game
gets and how large each card in the *memory* game is without always having to
manually check how large the resulting grid will be and adjusting ``WIDTH`` and
``HEIGHT`` yourself.

It's generally recommended to use game mechanics constants for any values that
affect gameplay and you might want to change on the fly to adjust how the game
feels. Not all games will need to use them even for the game window properties,
but there is no reason you can't if necessary.


Game mechanics constants
------------------------

.. code::

    COLUMNS = 4
    ROWS = 3
    GRID_SIZE = 200
    CARD_SIZE_RATIO = 0.90

    CARD_COLOR = "lightcoral"
    NORMAL_COLOR = "black"
    SUCCESS_COLOR = "green"
    FAILURE_COLOR = "red"

    CARD_FLIP_TIME = 0.1
    FAIL_SHOW_TIME = 1.0

We've already mentioned ``COLUMNS``, ``ROWS`` and ``GRID_SIZE``. The first two
together determine how many cards there are in the memory game. This also means
their multiplication always has to give an even number (since for *memory* all
numbers need to appear exactly twice). If you try setting them such that
multiplying them gives an uneven number, you'll see the game errors since there
is no valid way to create the numbers to arrange for an uneven number of cards.

``GRID_SIZE`` is the width and height in pixels for each grid cell and in turn
determines the size of the cards. ``CARD_SIZE_RATIO`` sets how large the cards
are in comparison to the grid size. If it was ``1.0``, then there would be no
gap at all between cards.

``CARD_COLOR``, ``NORMAL_COLOR``, ``SUCCESS_COLOR`` and ``FAILURE_COLOR`` are
all what they seem to be at first glance: color definitions for the card backs
as well as text display of the numbers under the cards under different
conditions.

Lastly, ``CARD_FLIP_TIME`` determines how long the animation to flip a card
takes and ``FAIL_SHOW_TIME`` sets how long numbers should stay visible before
being covered again after a failed guessing attempt.


Card setup
----------

This is the most complex part of the code. First, we create a rectangular
actors for each grid cell and place it correctly, saving all the actors in a
list. Then, we generate the numbers that should get distributed between the
cards and then assign one random number of the ones we generated to each card.


Card actors
"""""""""""

.. code::

    cards = []
    for i in range(COLUMNS):
        for k in range(ROWS):
            pos = (GRID_SIZE / 2 + GRID_SIZE * i, GRID_SIZE / 2 + GRID_SIZE * k)
            card = Actor.Rectangle(GRID_SIZE * CARD_SIZE_RATIO,
                                   GRID_SIZE * CARD_SIZE_RATIO, CARD_COLOR, pos)
            card.data["text_color"] = NORMAL_COLOR
            cards.append(card)

First, we prepare a list to keep track of all the card actors in: ``cards``.

Then, we use two nested ``for`` loops to go through each grid cell and create
an actor for it. ``i`` always contains the current column of the grid cell
minus one and ``k`` the same for rows. With them being one less than the
logical row, they act similarly to how list indices start from zero too.

For each grid cell, we calculate where they should be as follows::

    pos = (GRID_SIZE / 2 + GRID_SIZE * i, GRID_SIZE / 2 + GRID_SIZE * k)

``GRID_SIZE / 2`` for X and Y puts the basic placement in the middle of the
first grid cell. ``+ GRID_SIZE * i`` or ``* k`` then shift that middle position
to the correct number of columns and rows.

Here, it's handy that the ``range()`` function we used for the ``for`` loops
starts counting at zero and ends at one before the final number. For the first
column or row, this means the positions stays exactly at ``GRID_SIZE / 2``
since ``* 0`` is always zero as well. One number less than the final one as the
end point also means that the last numbers are shifted to the final grid cells
since the basic position is already at the first one.

After calculating the position, we simply create an actor from a rectangle with
the dimensions ``GRID_SIZE * CARD_SIZE_RATIO`` as explained above with
``CARD_COLOR`` as the color and the position as calculated.

Each card then gets the color with which it should display its number when
flipped in the ``.data`` dictionary, starting with ``NORMAL_COLOR``

Lastly, each actor is added to the list of ``cards``.


Assigning numbers to cards
""""""""""""""""""""""""""

We have cards in all grid cells, but they haven't got their numbers for the
actual *memory* mechanic yet. This comes next::

    numbers = []
    for i in range(COLUMNS * ROWS // 2):
        numbers.append(str(i + 1))
        numbers.append(str(i + 1))

    for card in cards:
        card.data["number"] = numbers.pop(random.randint(0, len(numbers) - 1))

First, we go through the numbers 0 to one less than ``COLUMNS * ROWS // 2``
with a ``for`` loop. For each of those numbers, we put the number one greater
into the list of numbers twice.

We go through half the number of grid cells because each number is in the game
twice, so we need half as many numbers as there are grid cells. We then add
each of those numbers twice to the same list, giving us an ordered list with
all the numbers in the game.

We then go through each card in the game and set their number by picking a
random one from the remaining numbers. By using the ``pop()`` method, we can
remove a list element at the same time as we are getting it. That means each
loop, we remove one element from the list of numbers, so there is no way it
could be picked again.

Because there are exactly as many numbers in the ``numbers`` list as cards in
the ``cards`` list, we can be sure that once the loop is done, all numbers have
been distributed among the cards randomly.


State and general setup
-----------------------

Another pattern found in many of the example projects is using a dictionary to
keep track of global game state. We do so here as well in the ``state``
dictionary::

    state = {"phase": "game", "first_picked": None, "second_picked": None,
             "pairs_to_find": COLUMNS * ROWS / 2, "tries": 0}

``"phase"`` is just there to keep track of whether the game is over or not,
``"first_picked"`` and ``"second_picked"`` will track what cards where clicked
on when selecting pairs, ``"pairs_to_find"`` tracks how many pairs there are
left to uncover and ``"tries"`` counts up how many pairs have been opened by
the player.

Beside the ``state`` dictionary, this is also where we define the functions
needed to manipulate cards after two have been picked.


unflip_picked_pair()
""""""""""""""""""""

.. code::

    def unflip_picked_pair():
        state["first_picked"].data["text_color"] = NORMAL_COLOR
        state["second_picked"].data["text_color"] = NORMAL_COLOR
        state["first_picked"].scale_x = 1.0
        state["second_picked"].scale_x = 1.0

        state["first_picked"] = None
        state["second_picked"] = None

This short function is called after a short delay when a picked pair was not
a number match, meaning they have to flip back to the covered state.

Remember that the picked cards are saved in the ``state`` dictionary, so the
function simply does the same two things for both of them:

#. Set their text display color back to normal.
#. Set their horizontal scale back to ``1.0`` so that they are displayed again.

Afterwards, the ``state`` dictionary wipes their tracked status, meaning
afterwards the player can pick to new cards again.


check_pair()
""""""""""""

.. code::
        
    def check_pair():
        first = state["first_picked"]
        second = state["second_picked"]
        state["tries"] += 1

        if first.data["number"] == second.data["number"]:
            first.data["text_color"] = SUCCESS_COLOR
            second.data["text_color"] = SUCCESS_COLOR
            state["pairs_to_find"] -= 1

            if state["pairs_to_find"] == 0:
                state["phase"] = "won"

            state["first_picked"] = None
            state["second_picked"] = None
            
            sounds.success.play()
        else:
            first.data["text_color"] = FAILURE_COLOR
            second.data["text_color"] = FAILURE_COLOR
            clock.schedule(unflip_picked_pair, 1.0)

            sounds.failure.play()

This is where a lot of the magic happens. At the start, we put the first and
second picked cards in individual variables to make the rest of the function
easier to write and also increment the ``state["tries"]`` counter by one since
the player picked two cards.

Then we check whether both picked cards have the same number.

* If yes, we set both their text display colors to green and decrement the
  counter keeping track of how many pairs are left to find (since one was
  found).

    If there are no more pairs left, we set ``state["phase"] = "won"`` to
    indicate the game is over.

    We also unset the picked card tracking in state and play the *success*
    sound effect.

* If not, we set the text display color of both cards to red and schedule the
  cards to be flipped back over to the covered state in a second. We also play
  the *failure* sound.


Event hook functions
--------------------

.. code::

    def on_mouse_down(pos):
        if state["first_picked"] and state["second_picked"]:
            return

        for card in cards:
            if card.collidepoint(pos) and card.scale_x == 1.0:
                sounds.flip.play()
                animate(card, duration=CARD_FLIP_TIME, scale_x=0.0)
                if state["first_picked"]:
                    state["second_picked"] = card
                    check_pair()
                else:
                    state["first_picked"] = card

Since *memory* is played by clicking on the cards with the mouse, we only need
one event hook: ``on_mouse_down()``. At the start, if there are currently two
picked cards, we ignore any mouse clicks. This won't cause a problem because
both a success or failure in picking two cards will eventually wipe the
tracking for the two picked cards, at which time mouse clicks will be processed
properly again.

If a mouse click gets processed, we go through all cards and check if the mouse
click hit one of them. On a hit, we play the *flip* sound for audio feedback
and animate the card being flipped by reducing its horizontal scaling to zero
over a short period.

This is not a very convincing animation, but it doesn't have to be to spice the
game up just a little bit.

Then we react differently based on whether it's the first or second card in a
pair to be picked. If it is the first (meaning ``state["first_picked"]`` is
``None`` and so ``if state["first_picked"]`` will be ``False``) then we simply
track it as such.

If not, it was the second, which we also track. Additionally however, we call
the ``check_pair()`` function to process whether the picked pair was a match
or not and then proceed accordingly.


Game loop functions
-------------------

.. code::

    def draw():
        screen.fill("white")
        for card in cards:
            card.draw()
            if card.scale_x == 0.0:
                screen.draw.text(card.data["number"],
                                 center=(card.x, card.y + GRID_SIZE / 10),
                                 fontsize=GRID_SIZE, color=card.data["text_color"])
            else:
                screen.draw.text("?", center=(card.x, card.y + GRID_SIZE / 10),
                                 fontsize=GRID_SIZE, color=NORMAL_COLOR)

        if state["phase"] == "won":
            screen.draw.text("SOLVED IN\n{} TRIES".format(state["tries"]),
                             center=(WIDTH / 2, HEIGHT / 2), color=NORMAL_COLOR,
                             fontsize=GRID_SIZE*0.6, owidth=0.75, ocolor="white")

First of all, there is no ``update()`` function! That's because there are no
inputs, actor movements or other game mechanics that have to be processed
continuously each frame. The only input we need is on a mouse click, which
we've handled above with ``on_mouse_down()``. Because of this, we don't even
need to define the ``update()`` function.

For drawing the game, we fill the screen with white and then go through each
card in the game, drawing them.

Depending on whether or not they are currently flipped open (if the
``.scale_x`` is zero, then they are open), we draw their number at their
location in their current text color.

For all covered cards, we draw a ``?`` the same way but always with the
``NORMAL_COLOR``.

Lastly, if the game is over, we also draw a text telling the player how many
pairs they picked before finishing the game as a measure of how well they did.
For this, we give the text a small special effect with ``owidth`` and
``ocolor``. Setting these properties will give the text display a shadow.

:ref:`Back to the overview <examples_overview_memory>`
