# utils/__init__.py
"""
Utility functions for Gaming Bot
All helper functions are collected here so they can be
imported anywhere in the project easily.
"""

import random
import logging
import re

# ------------------------------
# Name Formatting
# ------------------------------
def pretty_name(name: str) -> str:
    """
    Clean and format a name string.
    Example:
        '   nexxa ' -> 'Nexxa'
    """
    if not name:
        return ""
    return name.strip().title()


# ------------------------------
# Logging Helper
# ------------------------------
def get_logger(name: str) -> logging.Logger:
    """
    Create and return a logger instance with standard format.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# ------------------------------
# Random Utilities
# ------------------------------
def pick_random(items: list):
    """
    Return a random item from a list.
    """
    return random.choice(items) if items else None


# ------------------------------
# Text Utilities
# ------------------------------
def sanitize_text(text: str) -> str:
    """
    Remove unwanted characters and normalize spaces.
    """
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()
