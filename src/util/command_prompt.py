import time
import pygame
from .assets import Assets
from .draw import draw_transparent_rect

RECT_COLOR = (0, 40, 80)

class CommandPrompt:
    def __init__(self):
        self.enabled = False
        self.input = ''
        self.history: list[str] = []
        self.history_index = 0
        self.last_command: str = ''
    
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
        self.history_index = len(self.history)

    def handle_command(self, command: str):
        self.history.append(command)
        self.history_index = len(self.history)
        self.last_command = command
        self.input = ''

    def pop_command(self) -> str:
        last = self.last_command
        self.last_command = ''
        return last

    def handle_event(self, event: pygame.Event):
        # Handle commands if enabled
        if self.enabled and event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RETURN:
                    if self.input:
                        self.handle_command(self.input)
                case pygame.K_ESCAPE:
                    self.disable()
                case pygame.K_UP:
                    self.history_index = max(self.history_index - 1, 0)
                    if len(self.history) > 0:
                        self.input = self.history[self.history_index]
                case pygame.K_DOWN:
                    self.history_index = min(self.history_index + 1, len(self.history))
                    if self.history_index == len(self.history):
                        self.input = ''
                    else:
                        self.input = self.history[self.history_index]
                case pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                case _:
                    self.input += event.unicode

        # Toggle prompt with K_SLASH
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SLASH:
            self.toggle()

    def render(self, display: pygame.Surface):
        if self.enabled: 
            draw_transparent_rect(
                display, 
                rect=pygame.Rect(0, display.get_height() - 12, display.get_width(), 12),
                color=RECT_COLOR, 
                alpha=128
            )
            cursor = '_' if int(time.time() * 2) % 2 == 0 else ' '
            text_surf = Assets.FONT.render(f'/{self.input}{cursor}', antialias=False, color=(255, 255, 255))
            display.blit(text_surf, (4, display.get_height() - 8))  
    