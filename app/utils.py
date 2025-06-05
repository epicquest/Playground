import os

def env_true(var_name: str, default: bool = False) -> bool:
    return os.getenv(var_name, str(int(default))).lower() in ("1", "true", "yes")