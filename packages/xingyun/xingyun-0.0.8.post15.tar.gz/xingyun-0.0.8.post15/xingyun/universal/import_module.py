from importlib import import_module as impo
from types import ModuleType
from typing import Union
import warnings 


def my_import_module(module_name: str) -> Union[ModuleType , None]:
    try:
        lib = impo(module_name)
    except:
        warnings.warn(f"module {module_name} does not exists.")
        return None

    return lib