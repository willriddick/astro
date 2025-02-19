import os
import json
import pygame
from src.util import Vec2

INPUTS_FILE = "inputs.json"

_inputs = {}

def get(action: str, just_pressed=False) -> bool:
    """Returns the state of the given action."""
    if action not in _inputs.keys():
        raise ValueError(f'Invalid input key: {action}')
    
    if just_pressed:
        keys = pygame.key.get_just_pressed()
    else:
        keys = pygame.key.get_pressed()
    
    return keys[_inputs[action]]

def get_dir(just_pressed=False) -> Vec2:
    """Returns a vector based on the directional input keys."""
    keys = pygame.key.get_just_pressed() if just_pressed else pygame.key.get_pressed()
    
    up = keys[get_input('up')]
    down = keys[get_input('down')]
    left = keys[get_input('left')]
    right = keys[get_input('right')]
    
    return Vec2((right) - int(left), int(down) - int(up))

def get_next_keydown() -> int | None:
    """Returns the first key that was just pressed, or None if no key was pressed."""
    just_pressed = pygame.key.get_just_pressed()
    for key in range(len(just_pressed)):  
        if just_pressed[key]: return key  
    return None

def get_input(action: str) -> int:
    """Returns the key code for the given action."""
    if action not in _inputs.keys():
        raise ValueError(f'Invalid input action: {action}')
    return _inputs[action]

def set_input(action: str, value: int) -> bool:
    """Updates the action with the provided value."""
    if action not in _inputs.keys():
        raise ValueError(f'Invalid input action: {action}')
    
    # if the new value is the current value for this input, return True
    # this will happen if the player uses 'Escape' to cancel the input as well
    if get_input(action) == value:
        return True

    # if the new value is already in the input map, return False
    # because we should not map an action to two input keys
    if any(v == value for v in _inputs.values()):
        return False
    
    # update the input map with the new value
    _inputs[action] = value
    return True

def save(filename=INPUTS_FILE):
    with open(filename, "w") as f:
        json.dump(_inputs, f, indent=4)

def load(filename=INPUTS_FILE):
    global _inputs
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read().strip()
                if content:
                    _inputs.update(json.loads(content))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading settings: {e}, resetting to defaults.")
        save(filename)

def reset_defaults():
    global _inputs
    _inputs = {
        "up": 119,
        "down": 115,
        "left": 97,
        "right": 100,
        "jump": 32,
        "select": 13,
        "escape": 27
    }


# load inputs on module import
reset_defaults()
load()
