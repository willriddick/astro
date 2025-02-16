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
        
        return keys[option]
    
    def set_input(self, key: str, value: int) -> bool:
        if key not in self.settings.input_map:
            raise ValueError(f'Invalid input key: {key}')
        
        # if the new value is the current value for this input, return True
        # this will happen if the player uses 'Escape' to cancel the input as well
        if self.settings.input_map[key] == value:
            return True

        # if the new value is already in the input map, return False
        if any(v == value for v in self.settings.input_map.values()):
            return False

        # otherwise, update the input map and save the settings
        self.settings.input_map[key] = value
        self.settings.save()
        return True
    
    def get_dir(self, just_pressed=False) -> Vec2:
        """Returns the movement direction vector based on input keys."""
        keys = pygame.key.get_just_pressed() if just_pressed else pygame.key.get_pressed()
        
        right = keys[self.settings.input_map['right']]
        left = keys[self.settings.input_map['left']]
        down = keys[self.settings.input_map['down']]
        up = keys[self.settings.input_map['up']]
        
        return Vec2(int(right) - int(left), int(down) - int(up))
    
    def get_next_keydown(self) -> int | None:
        """Returns the first key that was just pressed, or None if no key was pressed."""
        keys = pygame.key.get_just_pressed()
        for key in range(len(keys)):  
            if keys[key]: return key  
        return None
