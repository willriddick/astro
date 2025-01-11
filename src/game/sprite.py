import pygame

class Sprite:
    def __init__(self, pos: tuple[int, int], image_offset: tuple[int, int]):
        self.pos = pygame.math.Vector2(pos)
        self.offset = image_offset

        self.animations: dict[int, tuple[list[pygame.Surface, int]]] = {} # id: (frames, frame_rate)
        self.current = 0
        self.frame = 0
        self.subindex = 0
        self.flip = False

        self.animation_timer = 0
        self.next_animation = None

        self.last_update_time = pygame.time.get_ticks()
    
    def update(self, pos: pygame.math.Vector2):
        self.pos = pos

        self.animation_timer = max(0, self.animation_timer - 1)
        if self.animation_timer == 1 and self.next_animation:
            self.set_animation(self.next_animation)
            self.next_animation = None

        frames, frame_rate = self.get_animation()
        if len(frames) != 1 and frame_rate != 0:
            current_time = pygame.time.get_ticks()
            time_per_frame = 1000 // frame_rate  # Convert FPS to milliseconds per frame
            if current_time - self.last_update_time >= time_per_frame:
                self.last_update_time = current_time
                self.frame = (self.frame + 1) % len(frames)        
    
    def add_animation(self, id_: int, frames: list[pygame.Surface], frame_rate: int, range_: tuple[int, int]=None):
        if range_:
            start, stop = range_
            if not (0 <= start < len(frames) and 0 < stop <= len(frames) and start < stop):
                raise ValueError(f"Invalid range_: {range_} for frames length {len(frames)}")
            self.animations[id_] = (frames[start:stop], frame_rate)
        else:
            self.animations[id_] = (frames, frame_rate)
    
    def set_animation(self, id_: str, frame: int = 0):
        assert id_ in self.animations, f'Animation {id_} not found'
        if self.current != id_:
            self.frame = frame
            self.current = id_

            self.animation_timer = 0
            self.next_animation = None
    
    def get_animation(self) -> tuple[list[pygame.Surface], int]:
        return self.animations.get(self.current)
    
    def animate(self, id_: int, duration: int, next_id: int=None):
        self.set_animation(id_)
        self.animation_timer = duration + 1
        if next_id:
            self.next_animation = next_id
    
    def queue_animation(self, id_: int):
        if self.animation_timer:
            self.next_animation = id_
        else:
            self.set_animation(id_)
  
    def get_surface(self) -> pygame.Surface:
        return pygame.transform.flip(
            self.get_animation()[0][self.frame],
            self.flip, 
            False
        )

    def render(self, display: pygame.Surface, offset=(0, 0)):
        display.blit( 
            self.get_surface(),
            (self.pos.x - self.offset[0] + offset[0], 
             self.pos.y - self.offset[1] + offset[1])
        )
