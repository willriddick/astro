import os
import json
from dataclasses import dataclass, asdict

@dataclass
class Settings:
    fullscreen: bool = False
    window_scale: int = 4
    master_volume: int = 5
    sfx_volume: int = 5
    music_volume: int = 5
    fuel_ui_alpha: int = 3

    _instance = None  # class-level singleton instance

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Load settings only once when the instance is first created."""
        if not hasattr(self, "_initialized"):  # prevent reloading on re-instantiation
            self.load()
            self._initialized = True

    def save(self, filename="settings.json"):
        """Save settings to a file."""
        with open(filename, "w") as f:
            json.dump(asdict(self), f, indent=4)

    def load(self, filename="settings.json"):
        """Load settings from a file, updating the instance attributes."""
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self.__dict__.update(data)
