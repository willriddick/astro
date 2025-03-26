import os
import json


SETTINGS_FILE = 'settings.json'

class SettingsManager:
    """Manages game settings with load/save functionality."""
    
    def __init__(self):
        """Initialize settings with default values and load from file."""
        self._settings = {}
        self.reset_defaults()
        self.load()

    def set_key(self, key: str, value: any) -> None:
        """Set a key-value pair in the settings."""
        self._settings[key] = value

    def get(self, key: str):
        """Get a value from settings."""
        return self._settings.get(key)

    def save(self, filename=SETTINGS_FILE) -> None:
        """Save settings to a file."""
        with open(filename, "w") as f:
            json.dump(self._settings, f, indent=4)

    def load(self, filename=SETTINGS_FILE) -> None:
        """Load settings from a file or reset on error."""
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    content = f.read().strip()
                    if content:
                        self._settings.update(json.loads(content))
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading settings: {e}, resetting to defaults.")
            self.save(filename)

    def reset_defaults(self) -> None:
        """Reset settings to default values."""
        self._settings = {
            "show_fps": False,
            "show_gamertag": True,
            "fullscreen": True,
            "window_scale": 3,
            "master_volume": 10,
            "sfx_volume": 5,
            "music_volume": 5,
            "fuel_ui_alpha": 5
        }


SETTINGS = SettingsManager()
