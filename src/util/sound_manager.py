import os
import numpy as np
import pygame
import src.game.settings as settings
from .sound import Sound

SOUND_PATH = os.path.join('assets', 'audio')

class SoundManager:
    def __init__(self):
        self.sounds: dict[str, list[Sound]] = {}
    
    @property
    def master_volume(self) -> float:
        return settings.get('master_volume') / 10
    
    @property
    def sfx_volume(self) -> float:
        return (settings.get('sfx_volume') / 10)  * self.master_volume

    @property
    def music_volume(self) -> float:
        return (settings.get('music_volume') / 10) * self.master_volume
    
    def update_sounds(self):
        """
        Update the volume of all sounds in the dictionary based on current volume settings.
        """
        for sound in self.sounds.values():
            if sound.category == 0:
                sound.update_volume(self.sfx_volume)
            elif sound.category == 1:
                sound.update_volume(self.music_volume)
            
    def get(self, name: str) -> Sound:
        """Get a sound from the dictionary."""
        assert name in self.sounds, f'Sound "{name}" not found'
        return self.sounds[name]
    
    def play(self, name: str, pitch_index: int = None, loops: int = 0):
        """
        Play a sound from the dictionary.

        Args:
            name (str): The name of the sound.
            pitch_index (int): The index of the pitch-shifted sound to play. If 
                None, a random sound is played.
        """
        self.get(name).play(pitch_index, loops)
    
    def add(self,  
            name: str, 
            path: str = '',
            category: int = 0,
            vol: float = 0.5,
            p_min: float = 0.9,
            p_max: float = 1.1,
            p_step: float = 0.05
        ):
        """
        Add a sound to the dictionary with optional pitch shifting.

        Args:
            name (str): The name of the sound.
            path (str): The path to the sound file, by default, this is the same as the name.
            vol (float): The volume of the sound.
            p_min (float): The minimum pitch shift factor.
            p_max (float): The maximum pitch shift factor.
            p_step (float): The step size between pitch
        """
        base_sound = load_sound(name if path == '' else path)
        sounds = []

        if p_min == p_max or p_step == 0:
            new_sound = change_pitch(base_sound, p_min)
            new_sound.set_volume(vol)
            sounds.append(new_sound)
        else:
            for pitch in np.arange(p_min, p_max, p_step):
                new_sound = change_pitch(base_sound, pitch)
                new_sound.set_volume(vol)
                sounds.append(new_sound)

        self.sounds[name] = Sound(name, sounds, category, vol, p_min, p_max, p_step)
    
def load_sound(name: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(os.path.join(SOUND_PATH, f'{name}.wav'))

def change_pitch(sound: pygame.mixer.Sound, pitch_factor: float) -> pygame.mixer.Sound:
    """ Change pitch of a pygame sound by resampling the NumPy array. """
    sound_array = pygame.sndarray.array(sound)
    
    # Ensure the array is 2D (stereo)
    if sound_array.ndim == 1:
        sound_array = np.column_stack((sound_array, sound_array))  # duplicate for stereo
    
    num_samples = int(len(sound_array) / pitch_factor)  # adjust length
    new_sound_array = np.zeros((num_samples, 2), dtype=np.int16)

    # apply pitch shift independently to both channels
    for i in range(2):
        new_sound_array[:, i] = np.interp(
            np.linspace(0, len(sound_array), num_samples),
            np.arange(len(sound_array)),
            sound_array[:, i]
        ).astype(np.int16)
    
    return pygame.sndarray.make_sound(new_sound_array)
