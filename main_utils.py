# main_utils.py
import os
import importlib
import pkgutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_games_package(app, db, package="games"):
    """
    Import every module in the games package and call register(app, db)
    Each game module should implement register(app, db)
    """
    base = Path(package)
    if not base.exists():
        logger.warning("Games folder not present: %s", package)
        return []

    loaded = []
    # iterate through package modules
    for finder, name, ispkg in pkgutil.iter_modules([str(base)]):
        mod_name = f"{package}.{name}"
        try:
            m = importlib.import_module(mod_name)
            if hasattr(m, "register"):
                m.register(app, db)
                loaded.append(name)
                logger.info("Loaded game module: %s", name)
            else:
                logger.warning("Module %s has no register(app, db) function", mod_name)
        except Exception as e:
            logger.exception("Failed to import %s: %s", mod_name, e)
    return loaded
