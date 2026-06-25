import yaml
from pathlib import Path
from threading import Lock
from utils.logger import get_logger

logger = get_logger("ConfigManager")


class ConfigManager:
    """
    Centralized configuration loader for Osprey.
    - Loads YAML configs from /configs
    - Caches them in memory
    - Supports auto-reload
    - Provides typed access (cfg.api.host)
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigManager, cls).__new__(cls)
                cls._instance._cache = {}
                cls._instance._config_dir = (
                    Path(__file__).resolve().parents[2] / "configs"
                )
            return cls._instance

    # ---------------------------------------------------------
    # Load YAML file
    # ---------------------------------------------------------
    def load(self, name: str, force_reload: bool = False):
        if not force_reload and name in self._cache:
            return self._cache[name]

        path = self._config_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        self._cache[name] = data
        logger.info(f"Loaded config: {name}")
        return data

    # ---------------------------------------------------------
    # Typed access: cfg.api.host → value
    # ---------------------------------------------------------
    def get(self, config_name: str, *keys, force_reload=False):
        cfg = self.load(config_name, force_reload=force_reload)

        for key in keys:
            if key not in cfg:
                raise KeyError(f"Key '{key}' not found in {config_name}")
            cfg = cfg[key]

        return cfg

    # ---------------------------------------------------------
    # Clear cache (optional)
    # ---------------------------------------------------------
    def clear_cache(self):
        self._cache = {}
        logger.info("Config cache cleared.")

CONFIG_PATH = "config/train_config.json"

def load_config(path: str = CONFIG_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


