import pkgutil
import importlib

__all__ = []
for _loader, modname, _ispkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{modname}")
    globals()[modname] = module
    __all__.append(modname)

