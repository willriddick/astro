import os
import json
from dataclasses import dataclass, asdict

@dataclass
class Settings:
    fullscreen: bool = False
    screen_width: int = 1280
    screen_height: int = 720
    master_volume: int = 5
    sfx_volume: int = 5
    music_volume: int = 5
    fuel_ui_alpha: int = 3

    _instance = None  # Class-level variable to hold the instance

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @staticmethod
    def save(filename="settings.json"):
        if Settings._instance is None:
            Settings._instance = Settings()
        with open(filename, "w") as f:
            json.dump(Settings._instance.to_dict(), f, indent=4)

    @classmethod
    def load(cls, filename="settings.json"):
        if cls._instance is None:
            cls._instance = cls()
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                print(f"Loaded data: {data}")
                for key, value in data.items():
                    setattr(cls._instance, key, value)
        else:
            print(f"{filename} not found, using default settings.")
        
        return cls._instance

    # Getter methods
    @classmethod
    def get_fullscreen(cls):
        return cls._instance.fullscreen

    @classmethod
    def get_screen_width(cls):
        return cls._instance.screen_width

    @classmethod
    def get_screen_height(cls):
        return cls._instance.screen_height

    @classmethod
    def get_master_volume(cls):
        return cls._instance.master_volume

    @classmethod
    def get_sfx_volume(cls):
        return cls._instance.sfx_volume

    @classmethod
    def get_music_volume(cls):
        return cls._instance.music_volume
    
    @classmethod
    def get_fuel_ui_alpha(cls):
        return cls._instance.fuel_ui_alpha

    # Setter methods
    @classmethod
    def set_fullscreen(cls, value: bool):
        cls._instance.fullscreen = value

    @classmethod
    def set_screen_width(cls, value: int):
        cls._instance.screen_width = value

    @classmethod
    def set_screen_height(cls, value: int):
        cls._instance.screen_height = value

    @classmethod
    def set_master_volume(cls, value: int):
        cls._instance.master_volume = value

    @classmethod
    def set_sfx_volume(cls, value: int):
        cls._instance.sfx_volume = value

    @classmethod
    def set_music_volume(cls, value: int):
        cls._instance.music_volume = value

    @classmethod
    def set_fuel_ui_alpha(cls, value: int):
        cls._instance.fuel_ui_alpha = value