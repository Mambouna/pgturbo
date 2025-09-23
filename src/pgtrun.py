"""Runner system for Pygame Turbo.

By importing this module, the __main__ module is populated with the builtins
provided by Pygame Turbo.

When pgtrun.go() is called, the __main__ module is run as a Pygame Turbo
script (we enter the game loop, calling draw() and update() etc as defined in
__main__).

"""
import sys
from pgturbo.runner import prepare_mod, run_mod


mod = sys.modules['__main__']
if not getattr(sys, '_pgtrun', None):
    if not getattr(mod, '__file__', None):
        raise ImportError(
            "You are running from an interactive interpreter.\n"
            "'import pgtrun' only works when you are running a Python file."
        )
    prepare_mod(mod)


def go():
    """Run the __main__ module as a Pygame Turbo script."""
    if getattr(sys, '_pgtrun', None):
        return

    run_mod(mod)
