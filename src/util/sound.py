import pygame
from random import randint

class Sound:
    def __init__(self,
            name: str, 
            sounds: list[pygame.mixer.Sound] = [],
            category: int = 0,
            default_volume: float = 1.0,
            pitch_min: float = 1.0,
            pitch_max: float = 1.0,
            pitch_step: float = 0.0
        ):
        self.name = name
        self.sounds = sounds
        self.default_volume = default_volume
        self.category = category
        self.pitch_min = pitch_min
        self.pitch_max = pitch_max
        self.pitch_step = pitch_step
    
    def get_count(self) -> int:
        return len(self.sounds)
    
    def play(self, pitch_index: int = None, loops: int = 0):
        selection = None

        if pitch_index is None:
            if len(self.sounds) == 1:
                selection = self.sounds[0]
            else:
                selection = self.sounds[randint(0, len(self.sounds) - 1)]
        else: 
            index = min(pitch_index, len(self.sounds) - 1)
            selection = self.sounds[index]
        
        for sound in self.sounds:
            sound.stop()
        
        selection.play(loops)
   
    def update_volume(self, multipler: float = 1.0):
        """
        Updates the volume of all sounds in the sound object to 
        the default volume multiplied by the given multiplier.
        """
        for sound in self.sounds:
            sound.set_volume(self.default_volume * multipler)