"""Module remembering/forgetting."""

import sys
from types import ModuleType

from py.code import compile

REMEMBERED_MODULES = []


def forget(module):
    """Remove module from sys.modules"""
    if module is None:
        return
    name = module.__name__
    if name in sys.modules:
        del sys.modules[name]
    if name in REMEMBERED_MODULES:
        REMEMBERED_MODULES.remove(module)


def from_string(name, source):
    """Return a named Python module containing source."""
    # Strip source to get rid of any trailing whitespace, then make
    # sure it ends with a newline.
    source = source.strip() + '\n'
    module = ModuleType(name)
    code = compile(source, name, 'exec')
    exec(code, module.__dict__)
    return module


def remember(module, complain=True):
    """Add a module to sys.modules, and remember it for later forgetting."""
    name = module.__name__
    if name in sys.modules.keys() and complain:
        raise ValueError('module conflicts with an existing one')
    sys.modules[name] = module
    REMEMBERED_MODULES.append(module)
    return module
