.. _reference_storage:

Reference: storage
===================

:ref:`Deep dive on data storage <deep_dive_storage>`


.. _reference_dict:

Storage as a dict
-----------------

Accessing values in ``storage`` works the same as with a dictionary:

.. method:: storage[key] = value

    Set a value in the storage.

.. method:: storage[key]

    Get a value from the storage. Raise ``KeyError`` if there is no such key
    in the storage.


.. _reference_attributs:

Attributes
----------

``storage`` has a single attribute you can get the value of:

.. attribute:: path

    The actual file path to which the save data will be written.


.. _reference_methods:

Methods
-------

.. method:: load()

    Loads the data from a file on disk and into the ``storage`` dictionary.

    Note this erases any data that was in ``storage`` before.

.. method:: save()

    Saves the data in ``storage`` to disk.

.. method:: setdefault(key, value)

    Insert a default `value` into the storage, only if no value already
    exists for this `key`.

.. method:: setup(defaults)

    Loads the data saved on disk into ``storage`` and then runs
    ``setdefault()`` for every key value pair in the given `defaults`
    dictionary.

    This means existing key value pairs are left alone while new ones
    are inserted into ``storage`` from the provided key value pairs.

    Use this as a shorthand for the following::

        storage.load()
        storage.setdefault(key1, value1)
        storage.setdefault(key2, value2)
        # ...

.. method:: overwrite(new_state)

    Erases all data in ``storage`` and then fills it with the key value
    pairs from the given `new_state` dictionary.

    The difference to ``setup()`` is that this will not leave existing
    key value pairs alone but instead forces the ``storage`` data to be
    exactly the same as that of `new_state` after being run.

.. method:: clear()
    :no-index:

    Remove all stored values. Use this if you get into a bad state somehow.

    Note you still have to save after using ``clear()`` if you want the
    bad state to be removed from the file on disk as well.

.. method:: get(key, [default])

    Get a value from the storage. If there is no such `key`, return
    the value of `default` or ``None`` if no default was given.

    If you set up your storage well at the start of the program, this
    method should not usually be needed.


.. _reference_storage_changelog:

Changelog
---------

* **1.13:** Full ``storage`` builtin rework with convenience methods and proper
  saving, loading and autosave mode.
* **1.4:** First release of PGTurbo after fork from PGZero.
