import re
import pygame
from .vec2 import Vec2
from .assets import Assets
from .draw import draw_rect

RECT_COLOR = pygame.Color(0, 40, 80, 100)
OUTLINE_COLOR = pygame.Color(255, 255, 255, 100)
ALLOWED_CHARACTERS = re.compile(r'[a-zA-Z0-9/_. ]')

class CommandPrompt:
    def __init__(self):
        self.enabled = False
        self.input = ''
        self.history: list[str] = []
        self.history_index = 0
        self.last_command: str = ''
        self.cursor_index = 0
    
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
        self.cursor_index = 0

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
        if self.enabled and event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RETURN:
                    if self.input:
                        self.handle_command(self.input)
                    self.disable()
                case pygame.K_ESCAPE:
                    self.disable()
                case pygame.K_UP:
                    self.handle_up_arrow()
                case pygame.K_DOWN:
                    self.handle_down_arrow()
                case pygame.K_LEFT:
                    self.handle_left_arrow(event)
                case pygame.K_RIGHT:
                    self.handle_right_arrow(event)
                case pygame.K_BACKSPACE:
                    self.handle_backspace(event)
                case _:
                    self.handle_character_input(event)

        # Enabled prompt with K_SLASH
        if (not self.enabled 
            and event.type == pygame.KEYDOWN 
            and event.key == pygame.K_SLASH):
            self.enable()
    
    def handle_up_arrow(self):
        self.history_index = max(self.history_index - 1, 0)
        if len(self.history) > 0:
            self.input = self.history[self.history_index]
            self.cursor_index = len(self.input)

    def handle_down_arrow(self):
        self.history_index = min(self.history_index + 1, len(self.history))
        if self.history_index == len(self.history):
            self.input = ''
        else:
            self.input = self.history[self.history_index]
        self.cursor_index = len(self.input)

    def handle_left_arrow(self, event):
        if event.mod & pygame.KMOD_CTRL:
            self.cursor_index = 0
        else:
            self.cursor_index = max(self.cursor_index - 1, 0)

    def handle_right_arrow(self, event):
        if event.mod & pygame.KMOD_CTRL:
            self.cursor_index = len(self.input)
        else:
            self.cursor_index = min(self.cursor_index + 1, len(self.input))

    def handle_backspace(self, event):
        if event.mod & pygame.KMOD_CTRL:
            # Delete until the next word boundary (space or underscore)
            if self.cursor_index > 0:
                while self.cursor_index > 0 and self.input[self.cursor_index - 1] not in (' ', '_'):
                    self.input = self.input[:self.cursor_index - 1] + self.input[self.cursor_index:]
                    self.cursor_index -= 1
                # Remove the space or underscore if present
                if self.cursor_index > 0 and self.input[self.cursor_index - 1] in (' ', '_'):
                    self.input = self.input[:self.cursor_index - 1] + self.input[self.cursor_index:]
                    self.cursor_index -= 1
        else:
            if self.cursor_index > 0:
                self.input = self.input[:self.cursor_index - 1] + self.input[self.cursor_index:]
                self.cursor_index -= 1

    def handle_character_input(self, event):
        if ALLOWED_CHARACTERS.match(event.unicode):
            self.input = self.input[:self.cursor_index] + event.unicode + self.input[self.cursor_index:]
            self.cursor_index += 1

    def render(self, display: pygame.Surface):
        if self.enabled: 
            rect = pygame.Rect(0, display.get_height() - 12, display.get_width(), 12)
            draw_rect(
                display, 
                offset=pygame.Vector2(0, 0),
                rect=rect,
                fill_color=RECT_COLOR, 
                outline_color=OUTLINE_COLOR,
            )
            text = f'/{self.input[:self.cursor_index]}_{self.input[self.cursor_index:]}'
            text_surf = Assets.FONT.render(text, antialias=False, color=(255, 255, 255))

            display.blit(text_surf, (4, display.get_height() - 10))
    