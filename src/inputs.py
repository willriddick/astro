import os
import json
import pygame
from src.util import Vec2

INPUTS_FILE = 'inputs.json'

class InputManager:
    def __init__(self):
        self._inputs = {}
        self.reset_defaults()
        self.load()

    def get(self, action: str, just_pressed=False) -> bool:
        """Returns the state of the given action."""
        if action not in self._inputs:
            raise ValueError(f'Invalid input key: {action}')
        
        keys = pygame.key.get_just_pressed() if just_pressed else pygame.key.get_pressed()
        return keys[self._inputs[action]]

    def get_dir(self, just_pressed=False) -> Vec2:
        """Returns a vector based on the directional input keys."""
        keys = pygame.key.get_just_pressed() if just_pressed else pygame.key.get_pressed()

        up = keys[self.get_input('up')]
        down = keys[self.get_input('down')]
        left = keys[self.get_input('left')]
        right = keys[self.get_input('right')]

        return Vec2((right) - int(left), int(down) - int(up))

    def get_next_keydown(self) -> int | None:
        """Returns the first key that was just pressed, or None if no key was pressed."""
        just_pressed = pygame.key.get_just_pressed()
        for key in range(len(just_pressed)):  
            if just_pressed[key]: return key  
        return None

    def get_input(self, action: str) -> int:
        """Returns the key code for the given action."""
        if action not in self._inputs:
            raise ValueError(f'Invalid input action: {action}')
        return self._inputs[action]

    def set_input(self, action: str, value: int) -> bool:
        """Updates the action with the provided value."""
        if action not in self._inputs:
            raise ValueError(f'Invalid input action: {action}')
        
        # Allow pressing 'Escape' to cancel input mapping
        if self.get_input(action) == value:
            return True

        # Prevent multiple actions from being bound to the same key
        if value in self._inputs.values():
            return False
        
        self._inputs[action] = value
        return True

    def save(self, filename=INPUTS_FILE):
        """Saves the input mappings to a file."""
        with open(filename, "w") as f:
            json.dump(self._inputs, f, indent=4)

    def load(self, filename=INPUTS_FILE):
        """Loads input mappings from a file, resetting on error."""
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    content = f.read().strip()
                    if content:
                        self._inputs.update(json.loads(content))
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading inputs: {e}, resetting to defaults.")
            self.save(filename)

    def reset_defaults(self):
        """Resets input bindings to default values."""
        self._inputs = {
            "up": 119,       # W
            "down": 115,     # S
            "left": 97,      # A
            "right": 100,    # D
            "jump": 32,      # Space
            "select": 13,    # Enter
            "escape": 27     # Escape
        }


INPUTS = InputManager()
