import math
import random
import pygame
from src.util import draw_rect
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
        color = Button.HOVERED_COLOR if id_ == node.id else Button.DEFAULT_COLOR
        username = client[1][0].upper()
        palette = 0
        draw_player_card(display, username, palette, color, (BUFFER + i * SLOT, 64), id_ == node.id)


def draw_player_card(display, username, palette_index, color, position, show_controls=True):
    card_surf = pygame.Surface((SLOT, SLOT), pygame.SRCALPHA)
    center = SLOT // 2

    background_color = graphics.PALETTE[15]
    outline_color = graphics.PALETTE[14]
    text_color = graphics.PALETTE[13]
    background_color.a = 150
    outline_color.a = 150
    text_color.a = 150

    # draw background
    draw_rect(
        card_surf, (0, 0), card_surf.get_rect(), 
        fill_color=background_color, line_width=3, outline_color=outline_color
    )

    # draw username
    username_surf = graphics.FONT.render(username, antialias=False, color=color)
    card_surf.blit(
        username_surf, 
        (center - (username_surf.width // 2), 16)
    )

    # draw instructions
    if show_controls:
        controls_surf = graphics.FONT.render('Cycle with A / D', antialias=False, color=text_color)
        card_surf.blit(
            controls_surf, 
            (center - (controls_surf.width // 2), SLOT - 16)
        )
    
    # draw player icon
    icon = pygame.transform.scale_by(graphics.ICON_VARIANTS[palette_index], 3)
    card_surf.blit(
        icon,
        (center - (icon.width // 2), 32)
    )

    display.blit(card_surf, position)


Y_BUFFER = random.randint(10, 20)
BASE_AMPLITUDE = random.randint(6, 10)

def draw_wave_lines(surface):
    wave_colors = [
        graphics.PALETTE[15],
        graphics.PALETTE[14],
        graphics.PALETTE[13],
        graphics.PALETTE[12],
    ]

    lines = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    for i in range(40):
        points = []
        offset = CLOCK.ticks * (0.0002 + i * 0.00003)
        amplitude = BASE_AMPLITUDE + i * 0.3
        frequency = 0.01 + i * 0.001
        y_base = i * Y_BUFFER 

        for x in range(0, DISPLAY_WIDTH, 4):
            y = y_base + math.sin(x * frequency + offset) * amplitude
            points.append((x, int(y)))

        color = wave_colors[i % len(wave_colors)]
        width = 1 + (i % 2) 
        pygame.draw.lines(lines, color, False, points, width)
    
    lines.set_alpha(100)
    surface.blit(lines, (0, 0))
