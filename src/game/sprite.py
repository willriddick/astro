from enum import Enum
import pygame
from src.util import Vec2

class Sprite:
    def __init__(self, pos: pygame.Vector2, image_offset = Vec2(0, 0)):
        self.pos = pygame.math.Vector2(pos)
        self.offset = image_offset

        self.animations: dict[int, tuple[list[pygame.Surface], int]] = {} # id: (frames, frame_rate)
        self.current = 0
        self.frame = 0
        self.flip = False

        self.next_timer = 0
        self.next_animation = None

        self.last_update_time = pygame.time.get_ticks()
    
    def update(self, pos: pygame.math.Vector2):
        self.pos = pos

        self.next_timer = max(0, self.next_timer - 1)
        if self.next_timer == 1 and self.next_animation:
            self.set_animation(self.next_animation)
            self.next_animation = None

        frames, frame_rate = self.get_animation()
        if len(frames) != 1 and frame_rate != 0:
            current_time = pygame.time.get_ticks()
            time_per_frame = 1000 // frame_rate  # Convert FPS to milliseconds per frame
            if current_time - self.last_update_time >= time_per_frame:
                self.last_update_time = current_time
                self.frame = (self.frame + 1) % len(frames)        
    
    def add_animation(self, id_: Enum, frames: list[pygame.Surface], frame_rate: int = 0, range_: tuple[int, int]=None):
        if range_:
            start, stop = range_
            if not (0 <= start < len(frames) and 0 < stop <= len(frames) and start < stop):
                raise ValueError(f"Invalid range_: {range_} for frames length {len(frames)}")
            self.animations[id_] = (frames[start:stop], frame_rate)
        else:
            self.animations[id_] = (frames, frame_rate)
    
    def set_animation(self, id_: Enum, frame: int = 0):
        assert id_ in self.animations, f'Animation {id_} not found'
        if self.current != id_:
            self.current = id_
            self.frame = frame
            self.next_timer = 0
            self.next_animation = None
    
    def set_frame(self, frame: int):
        self.frame = frame
    
    def get_animation(self) -> tuple[list[pygame.Surface], int]:
        return self.animations.get(self.current)
    
    def set_animation_duration(self, id_: Enum, duration: int, next_id: int=None):
        self.set_animation(id_)
        self.next_timer = duration + 1
        if next_id:
            self.next_animation = next_id
    
    def set_next(self, id_: Enum):
        if self.next_timer:
            self.next_animation = id_
        else:
            self.set_animation(id_)
    
    def get_surface(self) -> pygame.Surface:
        return pygame.transform.flip(
            self.get_animation()[0][self.frame],
            self.flip, 
            False
        )

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        display.blit( 
            self.get_surface(),
            (
                self.pos.x - self.offset.x + offset.x, 
                self.pos.y - self.offset.y + offset.y
            )
        )
