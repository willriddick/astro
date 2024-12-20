import pygame

class Sprite:
    def __init__(self, pos: tuple[int, int], image_offset: tuple[int, int]):
        self.pos = pygame.math.Vector2(pos)
        self.offset = image_offset

        self.animations: dict[str, tuple[list[pygame.Surface, int]]] = {} # name: (frames, frame_rate)
        self.current = ''
        self.frame = 0
        self.subindex = 0
        self.flip = False

        self.last_update_time = pygame.time.get_ticks()
    
    def update(self, pos: pygame.math.Vector2):
        self.pos = pos

        frames, frame_rate = self.get_animation()
        if len(frames) != 1 and frame_rate != 0:
            current_time = pygame.time.get_ticks()
            time_per_frame = 1000 // frame_rate  # Convert FPS to milliseconds per frame
            if current_time - self.last_update_time >= time_per_frame:
                self.last_update_time = current_time
                self.frame = (self.frame + 1) % len(frames)        
    
    def add_animation(self, name: str, frames: list[pygame.Surface], frame_rate: int):
        self.animations[name] = (frames, frame_rate)
    
    def set_animation(self, name: str, frame: int = 0):
        assert name in self.animations, f'Animation {name} not found'
        if self.current != name:
            self.frame = frame
            self.current = name
    
    def get_animation(self) -> tuple[list[pygame.Surface], int]:
        return self.animations.get(self.current)

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
