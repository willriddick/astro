from src.util import Vec2
from src.menu import Button
from src.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
import src.graphics as graphics


BUFFER = 32
SLOT = (DISPLAY_WIDTH - (BUFFER * 2)) / 4


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