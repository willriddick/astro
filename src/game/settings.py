import os
import json
from dataclasses import dataclass, asdict

@dataclass
class Settings:
    fullscreen: bool = True
    screen_width: int = 1280
    screen_height: int = 720
    volume: float = 0.5
    music_enabled: bool = True

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def save(self, filename="settings.json"):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load(cls, filename="settings.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return cls.from_dict(json.load(f))
        return cls()
