import tomllib
from pathlib import Path
from typing import Any

from .paths import get_config_dir

__all__ = ["Config"]

class Config:
    _instance: "Config | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(
        self,
        config_path: str | Path = get_config_dir() / "tieba-sign/config.toml",
        **defaults
    ):
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)
            self.config = self._recursive_update(defaults, config_data)

    @staticmethod
    def _recursive_update(defaults: dict[str, Any], new: dict[str, Any]):
        result = defaults.copy()
        for k, v in new.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = Config._recursive_update(result[k], v)
            else:
                result[k] = v
        return result
