import os
import numpy as np
import pygame

SOUND_PATH = os.path.join('assets', 'sounds')

class Sounds:
    def __init__(self):
        self.sounds: dict[str, list[pygame.mixer.Sound]] = {}
    
    def play(self, name: str, pitch_index: int = None):
        assert name in self.sounds, f'Sound "{name}" not found'
        sound_list = self.sounds[name]

        if len(sound_list) == 1:
            sound_list[0].play()
            return

        if pitch_index is None:
            sound_list[np.random.randint(0, len(sound_list))].play()
            return
    
        index = min(pitch_index, len(sound_list) - 1)
        sound_list[index].play()
    
    def add(self, name: str, volume: float = 1.0, pitch_min: float = 1.0, pitch_max: float = 1.0, pitch_step: float = 1.0):
        sound = load_sound(name)

        if pitch_min == 1 and pitch_max == 1:
            sound.set_volume(volume)
            self.sounds[name] = [sound]
            return

        list = []
        for pitch in np.arange(pitch_min, pitch_max, pitch_step):
            new_sound = change_pitch(sound, pitch)
            new_sound.set_volume(volume)
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
