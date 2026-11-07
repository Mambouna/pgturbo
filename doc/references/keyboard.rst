.. _reference_keyboard:

Reference: keyboard
====================

:ref:`Deep dive on the keyboard builtin <deep_dive_keyboard>`

The ``keyboard`` builtin has no methods, only properties for all keys that
return whether the key is held down at the moment when the property is read.

``True`` means the key is held down, ``False`` means it is not.

The following are all available keys that can be checked:

.. attribute:: backspace
.. attribute:: tab
.. attribute:: clear
   :no-index:
.. attribute:: return
.. attribute:: pause
.. attribute:: escape
.. attribute:: space
.. attribute:: exclaim
.. attribute:: quotedbl
.. attribute:: hash
.. attribute:: dollar
.. attribute:: ampersand
.. attribute:: quote
.. attribute:: leftparen
.. attribute:: rightparen
.. attribute:: asterisk
.. attribute:: plus
.. attribute:: comma
.. attribute:: minus
.. attribute:: period
.. attribute:: slash
.. attribute:: k_0
.. attribute:: k_1
.. attribute:: k_2
.. attribute:: k_3
.. attribute:: k_4
.. attribute:: k_5
.. attribute:: k_6
.. attribute:: k_7
.. attribute:: k_8
.. attribute:: k_9
.. attribute:: colon
.. attribute:: semicolon
.. attribute:: less
.. attribute:: equals
.. attribute:: greater
.. attribute:: question
.. attribute:: at
.. attribute:: leftbracket
.. attribute:: backslash
.. attribute:: rightbracket
.. attribute:: caret
.. attribute:: underscore
.. attribute:: backquote
.. attribute:: a
.. attribute:: b
.. attribute:: c
.. attribute:: d
.. attribute:: e
.. attribute:: f
.. attribute:: g
.. attribute:: h
.. attribute:: i
.. attribute:: j
.. attribute:: k
.. attribute:: l
.. attribute:: m
.. attribute:: n
.. attribute:: o
.. attribute:: p
.. attribute:: q
.. attribute:: r
.. attribute:: s
.. attribute:: t
.. attribute:: u
.. attribute:: v
.. attribute:: w
.. attribute:: x
   :no-index:
.. attribute:: y
   :no-index:
.. attribute:: z
.. attribute:: delete
.. attribute:: kp0
.. attribute:: kp1
.. attribute:: kp2
.. attribute:: kp3
.. attribute:: kp4
.. attribute:: kp5
.. attribute:: kp6
.. attribute:: kp7
.. attribute:: kp8
.. attribute:: kp9
.. attribute:: kp_period
.. attribute:: kp_divide
.. attribute:: kp_multiply
.. attribute:: kp_minus
.. attribute:: kp_plus
.. attribute:: kp_enter
.. attribute:: kp_equals
.. attribute:: up
   :no-index:
.. attribute:: down
   :no-index:
.. attribute:: right
   :no-index:
.. attribute:: left
   :no-index:
.. attribute:: insert
.. attribute:: home
.. attribute:: end
.. attribute:: pageup
.. attribute:: pagedown
.. attribute:: f1
.. attribute:: f2
.. attribute:: f3
.. attribute:: f4
.. attribute:: f5
.. attribute:: f6
.. attribute:: f7
.. attribute:: f8
.. attribute:: f9
.. attribute:: f10
.. attribute:: f11
.. attribute:: f12
.. attribute:: f13
.. attribute:: f14
.. attribute:: f15
.. attribute:: numlock
.. attribute:: capslock
.. attribute:: scrollock
.. attribute:: rshift
.. attribute:: lshift
.. attribute:: rctrl
.. attribute:: lctrl
.. attribute:: ralt
.. attribute:: lalt
.. attribute:: rmeta
.. attribute:: lmeta
.. attribute:: lsuper
.. attribute:: rsuper
.. attribute:: mode
.. attribute:: help
.. attribute:: print
.. attribute:: sysreq
.. attribute:: break
.. attribute:: menu
.. attribute:: power
.. attribute:: euro
.. attribute:: last


.. _reference_keyboard_constants:

Key constants for event hooks
-----------------------------

When using hooks like ``on_key_down(key)`` to react to keyboard events, use
the ``keys`` enum constants to check which button was pressed. ``keyboard``
can't be used, since its properties just return booleans of whether something
is pressed.

Example: ``if key == keys.SPACE:``

.. attribute:: BACKSPACE
.. attribute:: TAB
.. attribute:: CLEAR
.. attribute:: RETURN
.. attribute:: PAUSE
.. attribute:: ESCAPE
.. attribute:: SPACE
.. attribute:: EXCLAIM
.. attribute:: QUOTEDBL
.. attribute:: HASH
.. attribute:: DOLLAR
.. attribute:: AMPERSAND
.. attribute:: QUOTE
.. attribute:: LEFTPAREN
.. attribute:: RIGHTPAREN
.. attribute:: ASTERISK
.. attribute:: PLUS
.. attribute:: COMMA
.. attribute:: MINUS
.. attribute:: PERIOD
.. attribute:: SLASH
.. attribute:: K_0
.. attribute:: K_1
.. attribute:: K_2
.. attribute:: K_3
.. attribute:: K_4
.. attribute:: K_5
.. attribute:: K_6
.. attribute:: K_7
.. attribute:: K_8
.. attribute:: K_9
.. attribute:: COLON
.. attribute:: SEMICOLON
.. attribute:: LESS
.. attribute:: EQUALS
.. attribute:: GREATER
.. attribute:: QUESTION
.. attribute:: AT
.. attribute:: LEFTBRACKET
.. attribute:: BACKSLASH
.. attribute:: RIGHTBRACKET
.. attribute:: CARET
.. attribute:: UNDERSCORE
.. attribute:: BACKQUOTE
.. attribute:: A
.. attribute:: B
.. attribute:: C
.. attribute:: D
.. attribute:: E
.. attribute:: F
.. attribute:: G
.. attribute:: H
.. attribute:: I
.. attribute:: J
.. attribute:: K
.. attribute:: L
.. attribute:: M
.. attribute:: N
.. attribute:: O
.. attribute:: P
.. attribute:: Q
.. attribute:: R
.. attribute:: S
.. attribute:: T
.. attribute:: U
.. attribute:: V
.. attribute:: W
.. attribute:: X
.. attribute:: Y
.. attribute:: Z
.. attribute:: DELETE
.. attribute:: KP0
.. attribute:: KP1
.. attribute:: KP2
.. attribute:: KP3
.. attribute:: KP4
.. attribute:: KP5
.. attribute:: KP6
.. attribute:: KP7
.. attribute:: KP8
.. attribute:: KP9
.. attribute:: KP_PERIOD
.. attribute:: KP_DIVIDE
.. attribute:: KP_MULTIPLY
.. attribute:: KP_MINUS
.. attribute:: KP_PLUS
.. attribute:: KP_ENTER
.. attribute:: KP_EQUALS
.. attribute:: UP
.. attribute:: DOWN
.. attribute:: RIGHT
.. attribute:: LEFT
.. attribute:: INSERT
.. attribute:: HOME
.. attribute:: END
.. attribute:: PAGEUP
.. attribute:: PAGEDOWN
.. attribute:: F1
.. attribute:: F2
.. attribute:: F3
.. attribute:: F4
.. attribute:: F5
.. attribute:: F6
.. attribute:: F7
.. attribute:: F8
.. attribute:: F9
.. attribute:: F10
.. attribute:: F11
.. attribute:: F12
.. attribute:: F13
.. attribute:: F14
.. attribute:: F15
.. attribute:: NUMLOCK
.. attribute:: CAPSLOCK
.. attribute:: SCROLLOCK
.. attribute:: RSHIFT
.. attribute:: LSHIFT
.. attribute:: RCTRL
.. attribute:: LCTRL
.. attribute:: RALT
.. attribute:: LALT
.. attribute:: RMETA
.. attribute:: LMETA
.. attribute:: LSUPER
.. attribute:: RSUPER
.. attribute:: MODE
.. attribute:: HELP
.. attribute:: PRINT
.. attribute:: SYSREQ
.. attribute:: BREAK
.. attribute:: MENU
.. attribute:: POWER
.. attribute:: EURO
.. attribute:: LAST


.. _reference_keyboard_changelog:

Changelog
---------

* **1.4:** First release of PGTurbo after fork from PGZero.
