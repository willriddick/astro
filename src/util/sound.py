import numpy as np
import pygame

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
