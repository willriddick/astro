import os
import json
from dataclasses import dataclass, field, asdict
import pygame

@dataclass
class Settings:
    _instance = None  # singleton instance

    fullscreen: bool = True
    window_scale: int = 4
    master_volume: int = 5
    sfx_volume: int = 5
    music_volume: int = 5
    fuel_ui_alpha: int = 5

    input_map: dict[str, list[int]] = field(default_factory=lambda: {
        'up': [pygame.K_w, pygame.K_UP],
        'down': [pygame.K_s, pygame.K_DOWN],
        'left': [pygame.K_a, pygame.K_LEFT],
        'right': [pygame.K_d, pygame.K_RIGHT],
        'space': pygame.K_SPACE,
        'enter': pygame.K_RETURN,
        'esc': pygame.K_ESCAPE,
    })

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize settings from file only once."""
        if not hasattr(self, "_initialized"):
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
                for key, value in data.items():
                    setattr(self, key, value)
