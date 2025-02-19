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
            pitch_index (int): The index of the pitch-shifted sound to play. If 
                None, a random sound is played.
            loops (int): The number of times to loop the sound (0 for once, -1 for infinite).
        """
        self.get(name).play(pitch_index, loops)
    
    def load(self, sound: Sound):
        # load sound using name if path is empty
        base_sound = load_sound(sound.name if sound.path == '' else sound.path)
        sounds = []

        # if pitch min == pitch max or pitch step is 0, only add one sound
        if sound.pitch[0] == sound.pitch[1] or sound.pitch[2] == 0:
            new_sound = change_pitch(base_sound, sound.pitch[0])
            new_sound.set_volume(sound.default_volume)
            sounds.append(new_sound)
        else:
            # otherwise, add multiple pitches of the same sound
            for pitch in np.arange(sound.pitch[0], sound.pitch[1], sound.pitch[2]):
                new_sound = change_pitch(base_sound, pitch)
                new_sound.set_volume(sound.default_volume)
                sounds.append(new_sound)

        # update the sound object and add it to our dictionary
        sound.set_sounds(sounds)
        self.sounds[sound.name] = sound
    
    def load_all(self, sounds: list[Sound]):
        for sound in sounds:
            self.load(sound)
        self.update_sounds()
    
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
