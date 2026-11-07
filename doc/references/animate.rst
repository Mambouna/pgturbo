.. _reference_animate:

Reference: animate
===================

:ref:`Deep dive on property animation <deep_dive_property_animation>`

Generally, the ``animate()`` function can be used to change properties of any
object over time, but is mostly used with actors.

.. function:: animate(object, tween="linear", duration=1.0, on_finished=None, absolute=False, **targets)

    .. Comment to disable wrong syntax highlighting.**

    Animate the attributes on object from their current value to that
    specified in the targets keywords.

    This function returns an ``Animation`` object, which can be used to control
    it while running. Details on this are found below under the section
    tweening options.

    :param tween: The type of *tweening* to use. The possible options are
                  listed below. Default is ``"linear"``.
    :param duration: The duration of the animation in seconds. Default is
                     ``1.0``.
    :param on_finished: Callback function that will be called once the property
                        animation has finished. Default is ``None``, meaning
                        nothing will be run once the animation is done.
    :param absolute: Boolean of whether the property animation should play out
                     while respecting ``clock.timescale`` or not. Defaults to
                     ``False``, meaning property animations are affected by
                     timescale. Calling ``animate()`` with ``absolute=True``
                     will mean the animation plays out at normal speed
                     regardless of ``clock.timescale``.
    :param targets: The target values for the attributes to animate. Each value
                    is a pair in the form of ``property=value``. The property
                    must be an exact match for an existing object attribute.
                    The value must be a valid value for that attribute, as
                    otherwise an error will be raised.


.. _reference_animate_tweening_options:

Tweening options
-----------------

+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'linear'           | Animate at a constant speed from start to finish     | .. image:: /_static/animate_plots/linear.png           |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'accelerate'       | Start slower and accelerate to finish                | .. image:: /_static/animate_plots/accelerate.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'decelerate'       | Start fast and decelerate to finish                  | .. image:: /_static/animate_plots/decelerate.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'accel_decel'      | Accelerate to mid point and decelerate to finish     | .. image:: /_static/animate_plots/accel_decel.png      |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'in_elastic'       | Give a little wobble at the start                    | .. image:: /_static/animate_plots/in_elastic.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'out_elastic'      | Give a little wobble at the end                      | .. image:: /_static/animate_plots/out_elastic.png      |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'in_out_elastic'   | Give a wobble at both ends                           | .. image:: /_static/animate_plots/in_out_elastic.png   |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'bounce_end'       | Accelerate to the finish and bounce there            | .. image:: /_static/animate_plots/bounce_end.png       |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'bounce_start'     | Bounce at the start                                  | .. image:: /_static/animate_plots/bounce_start.png     |
+--------------------+------------------------------------------------------+--------------------------------------------------------+
| 'bounce_start_end' | Bounce at both ends                                  | .. image:: /_static/animate_plots/bounce_start_end.png |
+--------------------+------------------------------------------------------+--------------------------------------------------------+


.. _reference_animate_animation_objects:

Animation objects
------------------

The ``animate()`` function always returns an ``Animation`` object. This object
can be used to interrupt a running property animation, check whether it is
still running or change its ``on_finished`` callback:

.. method:: stop(complete=False)

    Stop the animation, optionally completing the transition to the final
    property values.

    :param complete: Set the animated attribute to the target value. Default is
                     ``False``.

.. attribute:: running

    This will be ``True`` if the animation is running. It will be ``False``
    when the duration has run or the ``stop()`` method was called before
    then.

.. attribute:: on_finished

    Returns the callable that was set to be run when the animation finishes or
    ``None`` if nothing was set to run.

    Can be set after the property animation starts to change the previously set
    value.

    The callable is NOT called if the animation was stopped via ``stop()``
    instead of running out normally.

    The function set to be called must not take any arguments.


.. _reference_animate_changelog:

Changelog
---------

* **1.15:** Property animations follow ``clock.timescale`` by default. Added
  ``absolute`` as a keyword argument to change if desired.
* **1.4:** First release of PGTurbo after fork from PGZero.
