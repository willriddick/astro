import numpy as np
import pygame
from src.util.sound import Sound, load_sound, change_pitch
from src.settings import SETTINGS


class SoundManager:
    def __init__(self):
        self.sounds: dict[str, list[Sound]] = {}
    
    @property
    def master_volume(self) -> float:
        return SETTINGS.get('master_volume') / 10
    
    @property
    def sfx_volume(self) -> float:
        return (SETTINGS.get('sfx_volume') / 10)  * self.master_volume

    @property
    def music_volume(self) -> float:
        return (SETTINGS.get('music_volume') / 10) * self.master_volume
    
    def update_sounds(self):
        """
        Update the volume of all sounds in the dictionary based on current volume SETTINGS
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
    
    def load_sounds(self, sounds: list[Sound]):
        """Load a list of sounds into the dictionary."""
        for sound in sounds:
            self._load(sound)
        self.update_sounds()
    
    def _load(self, sound: Sound):
        # load sound using name if path is empty
        base_sound = load_sound(sound.name if sound.path == '' else sound.path)
        sounds = []

        # if pitch min == pitch max or pitch step is 0, only add one sound
        if sound.pitch is None or sound.pitch[0] == sound.pitch[1] or sound.pitch[2] == 0:
            # if pitch is not None, we wanted to change the default pitch
            if sound.pitch is not None:
                new_sound = change_pitch(base_sound, sound.pitch[0])
            else:
                new_sound = base_sound
            
            # update volume and add to Sound object
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
    

# initialize the SoundManager and load all sounds
pygame.mixer.init()
SOUNDS = SoundManager()
SOUNDS.load_sounds([
    Sound("jump", default_volume=0.15, pitch=[0.9, 1.1, 0.05]),
    Sound("wall_jump", path="jump", default_volume=0.1, pitch=[0.7, 1.8, 0.05]),
    Sound("wall", default_volume=0.6, pitch=[0.8, 1, 0.05]),
    Sound("land", default_volume=0.15, pitch=[0.8, 1.1, 0.05]),
    Sound("step", default_volume=0.3, pitch=[0.9, 1.1, 0.05]),
    Sound("boost", default_volume=0.5),
    Sound("cant_boost", default_volume=0.7),
    Sound("slide", default_volume=0.4),
    Sound("teleport", default_volume=0.2),
    Sound("hurt", default_volume=0.2),
    Sound("dead", default_volume=1.8),
    Sound("rocket", default_volume=0.15),
    Sound("spawn", default_volume=0.35),
    Sound("blip_pitch", path='blip', default_volume=0.8, pitch=[0.7, 1.2, 0.03]),
    Sound("blip", default_volume=0.8, pitch=[0.9, 1.1, 0.025]),
    Sound("select", default_volume=0.7, path="select2"),
    Sound("music/track1", default_volume=0.3, category=1),
])
