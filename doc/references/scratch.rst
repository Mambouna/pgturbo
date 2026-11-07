.. DIFFERENCES TO MAKE EXPLAINERS FOR?

    1. Code structure / organization
    2. Angles are 0 when pointing straight right instead of up.

.. _reference_scratch_pgturbo_comparison:

Reference: Scratch compared to PGTurbo
======================================

:ref:`Tutorial on transitioning from Scratch to PGTurbo <tutorial_from_scratch>`

This reference page contains comparisons of different Scratch features to those
of PGTurbo. It is not exhaustive but tries to cover some of the most widely
used aspects of Scratch.


Scratch blocks in PGTurbo
-------------------------

This section lists Scratch blocks and their counterpart instructions in
Pygame Turbo.

*Note:* All instructions with a \* next to them (anything to do with
randomness) require ``import random`` to be placed at the top of a python file
to work.


Motion block category
"""""""""""""""""""""

.. list-table::
    :header-rows: 0

    *  - .. image:: /_static/scratch/reference_blocks/motion/1_move_10_steps.png
       - ``Actor.move_forward(10)``
    *  - .. image:: /_static/scratch/reference_blocks/motion/2_turn_cw_degrees.png
       - ``Actor.angle -= 15``
    *  - .. image:: /_static/scratch/reference_blocks/motion/3_turn_ccw_degrees.png
       - ``Actor.angle += 15``
    *  - .. image:: /_static/scratch/reference_blocks/motion/4_go_to_random_position.png
       - ``Actor.pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))`` \*
    *  - .. image:: /_static/scratch/reference_blocks/motion/5_go_to_mouse_pointer.png
       - ``Actor.pos = mouse.pos``
    *  - .. image:: /_static/scratch/reference_blocks/motion/6_go_to_x_y.png
       - ``Actor.pos = (30, 0)``
    *  - .. image:: /_static/scratch/reference_blocks/motion/7_glide_secs_to_random_position.png
       - ``animate(Actor, 1.0, pos=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))`` \*
    *  - .. image:: /_static/scratch/reference_blocks/motion/8_glide_secs_to_mouse_pointer.png
       - ``animate(Actor, 1.0, pos=mouse.pos)``
    *  - .. image:: /_static/scratch/reference_blocks/motion/9_glide_secs_to_x_y.png
       - ``animate(Actor, 1.0, pos=(30, 0))``
    *  - .. image:: /_static/scratch/reference_blocks/motion/10_point_in_direction.png
       - ``Actor.angle = 0``
    *  - .. image:: /_static/scratch/reference_blocks/motion/11_point_towards_mouse_pointer.png
       - ``Actor.angle = Actor.angle_to(mouse.pos)``
    *  - .. image:: /_static/scratch/reference_blocks/motion/12_change_x_by.png
       - ``Actor.x += 10``
    *  - .. image:: /_static/scratch/reference_blocks/motion/13_change_y_by.png
       - ``Actor.y += 10``
    *  - .. image:: /_static/scratch/reference_blocks/motion/14_set_x_to.png
       - ``Actor.x = 30``
    *  - .. image:: /_static/scratch/reference_blocks/motion/15_set_y_to.png
       - ``Actor.y = 0``
    *  - .. image:: /_static/scratch/reference_blocks/motion/16_if_on_edge_bounce.png
       - No direct equivalent. Vertical angle reflection can be done with ``Actor.angle *= -1``, horizontal reflection with ``Actor.angle = 180 - Actor.angle``.
    *  - .. image:: /_static/scratch/reference_blocks/motion/17_set_rotation_style_left_right.png
       - PGTurbo has no different styles of rotation.
    *  - .. image:: /_static/scratch/reference_blocks/motion/20_check_x_position.png
       - ``Actor.x``
    *  - .. image:: /_static/scratch/reference_blocks/motion/21_check_y_position.png
       - ``Actor.y``
    *  - .. image:: /_static/scratch/reference_blocks/motion/22_check_direction.png
       - ``Actor.angle``


Looks block category
""""""""""""""""""""

.. list-table::
    :header-rows: 0

    *  - .. image:: /_static/scratch/reference_blocks/looks/1_say_for_seconds.png
       - There is no single function in PGTurbo that creates drawn text at the position of an actor.
    *  - .. image:: /_static/scratch/reference_blocks/looks/3_think_for_seconds.png
       - There is no single function in PGTurbo that creates drawn text at the position of an actor.
    *  - .. image:: /_static/scratch/reference_blocks/looks/5_switch_costume_to.png
       - ``Actor.image = "costume2"``
    *  - .. image:: /_static/scratch/reference_blocks/looks/6_next_costume.png
       - There is no single instruction to switch between a set rotation of images for an actor.
    *  - .. image:: /_static/scratch/reference_blocks/looks/7_switch_backdrop_to.png
       - ``screen.blit("backdrop1", (0, 0))``
    *  - .. image:: /_static/scratch/reference_blocks/looks/8_next_backdrop.png
       - There is no single instruction to switch between a set rotation of images for screen blitting.
    *  - .. image:: /_static/scratch/reference_blocks/looks/9_change_size_by.png
       - ``Actor.width += 10`` and ``Actor.height += 10``
    *  - .. image:: /_static/scratch/reference_blocks/looks/10_set_size_to.png
       - ``Actor.scale = 1.0``
    *  - .. image:: /_static/scratch/reference_blocks/looks/11_change_color_effect_by.png
       - PGTurbo allows tinting and shading actors with two properties: ``.tint_color`` and ``.tint_value``.
    *  - .. image:: /_static/scratch/reference_blocks/looks/13_set_color_effect_to.png
       - PGTurbo allows tinting and shading actors with two properties: ``.tint_color`` and ``.tint_value``.
    *  - .. image:: /_static/scratch/reference_blocks/looks/15_clear_graphic_effects.png
       - ``Actor.tint_value = 0.0``
    *  - .. image:: /_static/scratch/reference_blocks/looks/16_show.png
       - ``Actor.opacity = 1.0``
    *  - .. image:: /_static/scratch/reference_blocks/looks/17_hide.png
       - ``Actor.opacity = 0.0``
    *  - .. image:: /_static/scratch/reference_blocks/looks/18_go_to_front_layer.png
       - PGTurbo does not have display layers. What is shown in front of something else is decided by draw order.
    *  - .. image:: /_static/scratch/reference_blocks/looks/20_go_forward_layers.png
       - PGTurbo does not have display layers. What is shown in front of something else is decided by draw order.
    *  - .. image:: /_static/scratch/reference_blocks/looks/22_costume_number.png
       - Images aren't numbered in PGTurbo.
    *  - .. image:: /_static/scratch/reference_blocks/looks/23_costume_name.png
       - ``Actor.image``
    *  - .. image:: /_static/scratch/reference_blocks/looks/24_backdrop_number.png
       - There is no single set background image in PGTurbo. It is usually drawn first to the game window with ``screen.blit()``.
    *  - .. image:: /_static/scratch/reference_blocks/looks/26_check_size.png
       - ``Actor.scale`` (retur


Sound block category
""""""""""""""""""""

.. list-table::
    :header-rows: 0

    *  - .. image:: /_static/scratch/reference_blocks/sound/1_play_sound.png
       - ``sounds.meow.play()``
    *  - .. image:: /_static/scratch/reference_blocks/sound/3_stop_all_sounds.png
       - PGTurbo has no way to stop all sounds at once. Individual sounds are stopped like so: ``sounds.meow.stop()``.
    *  - .. image:: /_static/scratch/reference_blocks/sound/4_change_pitch.png
       - PGTurbo has no way to change pitch or pan effects of playing sounds.
    *  - .. image:: /_static/scratch/reference_blocks/sound/10_set_volume.png
       - PGTurbo has individual volume settings for each sound file. They are changed like so: ``sounds.meow.set_volume(1.0)``.
    *  - .. image:: /_static/scratch/reference_blocks/sound/11_check_volume.png
       - PGTurbo has individual volume settings for each sound file. They can be gotten like so: ``sounds.meow.get_volume()``


Events block category
"""""""""""""""""""""

.. list-table::
    :header-rows: 0

    *  - .. image:: /_static/scratch/reference_blocks/events/1_when_flag_clicked.png
       - In PGTurbo code is run at program start, so there is no separate "start" point.
    *  - .. image:: /_static/scratch/reference_blocks/events/2_when_key_pressed.png
       - Define the ``on_key_down(key)`` event hook function and check which key was pressed with ``if key == keys.SPACE:``.
    *  - .. image:: /_static/scratch/reference_blocks/events/3_when_this_sprite_clicked.png
       - Define the ``on_mouse_down(pos)`` event hook function and check if the butten press hit an actor with ``if actor.collidepoint(pos):``.
    *  - .. image:: /_static/scratch/reference_blocks/events/4_when_backdrop_switches_to.png
       - PGTurbo has no single background image to track changes on.
    *  - .. image:: /_static/scratch/reference_blocks/events/6_when_timer_gt.png
       - Schedule function calls to happen after a delay with ``clock.schedule()``.
    *  - .. image:: /_static/scratch/reference_blocks/events/7_when_i_receive_message.png
       - PGTurbo has no signal system. If something happens that should affect multiple different actors or game systems, change their values manually or call the functions that manage them directly.
