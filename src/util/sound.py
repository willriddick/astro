import os
import numpy as np
import pygame

SOUND_PATH = os.path.join('assets', 'sounds')

class SoundManager:
    """
    A class to manage loading and playing sounds.
    """
    def __init__(self):
        self.sounds: dict[str, list[pygame.mixer.Sound]] = {}
    
    def get_count(self, name: str) -> int:
        return len(self.sounds[name])
    
    def play(self, name: str, vol: float = None, pitch_index: int = None):
        """
        Play a sound from the dictionary.

        Args:
            name (str): The name of the sound.
            vol (float): Will play sound at volume, then reset to original volume.
            pitch_index (int): The index of the pitch-shifted sound to play. If 
                None, a random sound is played.
        """
        assert name in self.sounds, f'Sound "{name}" not found'
        sound_list = self.sounds[name]
        selection = None

        if pitch_index is None:
            if len(sound_list) == 1:
                selection = sound_list[0]
            else:
                selection = sound_list[np.random.randint(0, len(sound_list))]
        else: 
            index = min(pitch_index, len(sound_list) - 1)
            selection = sound_list[index]
        
        if vol is not None:
            orig_vol = selection.get_volume()
            selection.set_volume(vol)
            selection.play()
            selection.set_volume(orig_vol)
        else:
            selection.play()
        
    def add(self, 
            name: str, 
            path: str = '',
            vol: float = 1.0,
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
        sound = load_sound(name if path == '' else path)

        if p_min == 1 and p_max == 1:
            sound.set_volume(vol)
            self.sounds[name] = [sound]
            return

        list = []
        for pitch in np.arange(p_min, p_max, p_step):
            new_sound = change_pitch(sound, pitch)
            new_sound.set_volume(vol)
            list.append(new_sound)

        self.sounds[name] = list

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
