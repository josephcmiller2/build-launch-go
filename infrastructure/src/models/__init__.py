import os
import importlib
import pkgutil
from .data_object import DataObject  # Import base class first

# Get the directory containing this __init__.py file
models_dir = os.path.dirname(__file__)

# Dictionary to store all model classes
__all__ = []

# Dynamically import all modules in this package
for (_, module_name, _) in pkgutil.iter_modules([models_dir]):
    # Don't import __init__ itself
    if module_name != "__init__" and module_name != "data_object":
        module = importlib.import_module(f".{module_name}", __package__)
        __all__.append(module_name)

# Now register all classes that inherit from DataObject
for cls in DataObject.__subclasses__():
    cls.register_class()
