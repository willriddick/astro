import pygame
from src.util import Vec2
from src.game.settings import Settings

class Input:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.settings = Settings()
            self._initialized = True
    
    def get(self, key: str, just_pressed=False) -> bool:
        if key not in self.settings.input_map:
            raise ValueError(f'Invalid input key: {key}')
        
        option = self.settings.input_map[key]

        if just_pressed:
            keys = pygame.key.get_just_pressed()
        else:
            keys = pygame.key.get_pressed()
        
        if isinstance(option, list):
            return any(keys[k] for k in option)
        else:
            return keys[option]
    
    def get_dir(self, just_pressed=False) -> Vec2:
        """Returns the movement direction vector based on input keys."""
        keys = pygame.key.get_just_pressed() if just_pressed else pygame.key.get_pressed()
        
        right = any(keys[key] for key in self.settings.input_map['right'])
        left = any(keys[key] for key in self.settings.input_map['left'])
        down = any(keys[key] for key in self.settings.input_map['down'])
        up = any(keys[key] for key in self.settings.input_map['up'])
        
        return Vec2(int(right) - int(left), int(down) - int(up))
