# -*- coding: utf-8 -*-

"""
Root of all devices

This will initialize the plugins in the local directory, bypassing modules
prefixed with `_`, adding them to the __all__ variable.
"""

import os
import sys

import inspect
import importlib
import pkgutil


for (module_loader, name, ispkg) in pkgutil.iter_modules([__name__.replace('.',
    '/')]):
    importlib.import_module(f".{name}", __package__)

__all__ = []
local_mods = [m for m in sys.modules if m.startswith(__name__) and not m ==
        __name__]
print(f"MODS: {local_mods}")

classes = []
for a in [inspect.getmembers(sys.modules[mod], inspect.isclass) for mod in
        local_mods]:
    print(f"MEMBERS: {a}")
    for mod in a:
        print(f"MOD: {mod}")
        __all__.append(mod[0])

print(f"ALL: {__all__}")
__all__.sort()
