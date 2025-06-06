"""
Utilities module.

This script contains various helpers.
"""
import os

def env_true(var_name: str, default: bool = False) -> bool:
    """
        Returns True if the environment variable `var_name` is set to a truthy value.

        Truthy values are "1", "true", or "yes" (case-insensitive).
        If the variable is not set, returns the `default` value.
        """
    return os.getenv(var_name, str(int(default))).lower() in ("1", "true", "yes")
