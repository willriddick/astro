import pygame
from random import randint

class Sound:
    """
    A class which handles playing sounds with different pitches.

    Attributes:
        name (str): The name of the sound object.
        path (str): The path to the sound file, if empty, name is used.
        category (int): The category of the sound object.
        default_volume (float): The default volume of the sound object.
        pitch (tuple[float, float, float]): Min pitch, max pitch, pitch step.
        sounds (list[pygame.mixer.Sound]): A list of the sound objects. If pitch is not specified,
            the list will contain a single sound object.
        last_played (pygame.mixer.Sound): The last sound object played, so we can stop it before playing
            a new one.
    """
    def __init__(self,
            name: str, 
            path: str = '', 
            category: int = 0,
            default_volume: float = 1.0,
            pitch: tuple[float, float, float] = (1.0, 1.0, 0.0)
        ):
        self.name = name
        self.path = path
        self.default_volume = default_volume
        self.category = category
        self.pitch = pitch

        self.sounds: pygame.mixer.Sound = []
        self.sound_count = 0

        self.last_played: pygame.mixer.Sound = None
    
    def set_sounds(self, sounds: list[pygame.mixer.Sound]):
        self.sounds = sounds
        self.sound_count = len(sounds)

    def play(self, pitch_index: int = None, loops: int = 0):
        """
        Play a sound from the dictionary.

        Args:
            pitch_index (int): The index of the pitch-shifted sound to play. 
            If None, a random sound is played.
            loops: The number of times to play the sound, -1 for infinite, 0 for once, and n for n+1 times.
        """
        index: int = 0  # if we have only one pitch

        if pitch_index is None:
            if self.sound_count > 0:
                index = randint(0, len(self.sounds) - 1)  # get a random pitch
        else:
            index = min(self.sound_count - 1, pitch_index)  # ensure index is within bound
        
        # stop the last played sound
        if self.last_played:
            self.last_played.stop() 

        # play the sound, update last played
        selection = self.sounds[index]
        selection.play(loops)
        self.last_played = selection
    
    def stop(self):
        """Stop the last played sound."""
        self.last_played.stop()
   
    def update_volume(self, multipler: float = 1.0):
        """
        Updates the volume of all sounds in the sound object to 
        the default volume multiplied by the given multiplier.
        """
        for sound in self.sounds:
            sound.set_volume(self.default_volume * multipler)
    
    def get_count(self) -> int:
        return self.sound_count
