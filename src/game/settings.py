import os
import json
import pygame

class Settings:
    _instance = None  # singleton instance

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize settings, loading from file if available."""
        if not hasattr(self, "_initialized"):
            self.reset_defaults()
            self.load()
            self._initialized = True

    def reset_defaults(self):
        """Reset settings to their default values."""
        instance = self._instance

        instance.fullscreen = True
        instance.window_scale = 4
        instance.master_volume = 5
        instance.sfx_volume = 5
        instance.music_volume = 5
        instance.fuel_ui_alpha = 5

        instance.input_map = {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_SPACE,
            'select': pygame.K_RETURN,
            'escape': pygame.K_ESCAPE,
        }
    
    def set_key(self, key: str, value: any):
        """Set a setting by key."""
        setattr(self._instance, key, value)
    
    def get_key(self, key: str):
        """Get a setting by key."""
        return getattr(self._instance, key)
    
    def set_input_key(self, key: str, value: int):
        """Set an input key by key."""
        self._instance.input_map[key] = value
    
    def get_input_key(self, key: str): 
        """Get an input key by key."""
        return self._instance.input_map[key]

    def save(self, filename="settings.json"):
        """Save settings to a file."""
        data = {key: value for key, value in self.__dict__.items() if not key.startswith("_")}
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, filename="settings.json"):
        """Load settings from a file, updating instance attributes."""
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    content = f.read().strip()
                    if content: 
                        data = json.loads(content)
                        for key, value in data.items():
                            setattr(self._instance, key, value)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading settings: {e}, resetting to defaults.")
            self.reset_defaults()
            self.save(filename)
