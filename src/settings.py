import os
import json

SETTINGS_FILE = "settings.json"

_settings = {}

def set_key(key: str, value: any):
    _settings[key] = value

def get(key: str):
    return _settings.get(key)

def save(filename=SETTINGS_FILE):
    with open(filename, "w") as f:
        json.dump(_settings, f, indent=4)

def load(filename=SETTINGS_FILE):
    global _settings
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read().strip()
                if content:
                    _settings.update(json.loads(content))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading settings: {e}, resetting to defaults.")
        save(filename)

def reset_defaults():
    global _settings
    _settings = {
        "max_fps": 0,
        "fullscreen": True,
        "window_scale": 4,
        "master_volume": 5,
        "sfx_volume": 5,
        "music_volume": 5,
        "fuel_ui_alpha": 5
    }


# load settings on module import
reset_defaults()
load()
