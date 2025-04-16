import math
import pygame
from src.util import Vec2
from src.menu import Button
from src.clock import CLOCK
from src.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from src.networking import Host
import src.graphics as graphics


BUFFER = 32
SLOT = (DISPLAY_WIDTH - (BUFFER * 2)) / Host.MAX_CLIENTS


def render_clients(display, node):
    if not node:
        return
    
    for i, client in enumerate(node.clients.items()):
        id_ = client[0]
        username = client[1][0].upper()
        color = Button.HOVERED_COLOR if id_ == node.id else Button.DEFAULT_COLOR
    
        display.blit(
            graphics.FONT.render(username, antialias=False, color=color),
            Vec2(BUFFER + (i * SLOT), DISPLAY_HEIGHT/2)
        )


def draw_wave_lines(surface):
    wave_colors = [
        graphics.PALETTE[15],
        graphics.PALETTE[14],
        graphics.PALETTE[13],
        graphics.PALETTE[12],
    ]

    for i in range(30):
        points = []
        offset = CLOCK.ticks * (0.0002 + i * 0.00003)
        amplitude = 6 + i * 0.3
        frequency = 0.01 + i * 0.001
        y_base = 40 + i * 10 

        for x in range(0, DISPLAY_WIDTH, 4):
            y = y_base + math.sin(x * frequency + offset) * amplitude
            points.append((x, int(y)))

        color = wave_colors[i % len(wave_colors)]
        width = 1 + (i % 3) 
        pygame.draw.lines(surface, color, False, points, width)
