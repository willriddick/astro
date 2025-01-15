import pygame
from .assets import Assets
from .draw import draw_transparent_rect

class CommandPrompt:
    def __init__(self):
        self.enabled = False
        self.input = ''
        self.history: list[str] = []
        self.history_index = 0
    
    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
        self.input = ''
        self.history_index = -1
    
    def render(self, display: pygame.Surface):
        if self.enabled: 
            draw_transparent_rect(
                display, 
                rect=pygame.Rect(0, display.get_height() - 12, display.get_width(), 12),
                color=(0, 0, 0), 
                alpha=128
            )
            text_surf = Assets.FONT.render(f'/{self.input}', antialias=False, color=(255, 255, 255))
            display.blit(text_surf, (4, display.get_height() - 8))  
    
    def handle_event(self, event: pygame.Event):
        # Handle commands if enabled
        if self.enabled and event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RETURN:
                    if self.input:
                        print(self.input)
                    self.disable()
                case pygame.K_ESCAPE:
                    self.disable()
                case pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                case _:
                    self.input += event.unicode

        # Toggle prompt with K_SLASH
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SLASH:
            self.toggle()
       