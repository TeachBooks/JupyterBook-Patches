import importlib
import inspect
from pkgutil import iter_modules

from jupyterbook_patches import patches


def load_patches() -> dict[str, type[patches.BasePatch]]:
    loaded_patches = {}

    for submodule in iter_modules(patches.__path__):
        module = importlib.import_module("." + submodule.name, package=patches.__name__)
        for _name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, patches.BasePatch)
                and obj != patches.BasePatch
            ):
                loaded_patches[obj.name] = obj

    return loaded_patches
