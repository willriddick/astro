import pygame
from src.util import State
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.networking import MsgType
from .game_states import GameStates


class Playing(State):
    def __init__(self):
        super().__init__(GameStates.PLAYING)

    def on_enter(self):
        LEVEL_MANAGER.new_level()
        self.client = Client(pygame.Vector2(0, 0))

    def update(self):
        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 

        node = self.owner.network_node
        if node:
            updates = node.get_updates()
            for update in updates:
                self.client.position = pygame.Vector2(update[1], update[2])
            
            node.broadcast_message(
                MsgType.UPDATE,
                (node.id, int(LEVEL_MANAGER.player.position.x), int(LEVEL_MANAGER.player.position.y))
            )

        CAMERA.move_to(LEVEL_MANAGER.player.center)

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        pygame.draw.circle(CAMERA.display, (255, 0, 0), (self.client.position.x + offset.x, self.client.position.y + offset.y), 4)

class Client():
    def __init__(self, position: pygame.Vector2):
        self.position = position
