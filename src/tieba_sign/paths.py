import os

from pathlib import Path

__all__ = ["get_config_dir"]

def get_config_dir() -> Path:
    if os.name == 'posix':
        return Path(os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config')))
    elif os.name == 'nt':
        return Path(os.getenv('APPDATA'))
    else:
        raise NotImplementedError(f"Unsupported OS: {os.name}")
