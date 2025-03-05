import pygame
from src.util import State, Timer
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.networking import MsgType
from .game_states import GameStates


class Playing(State):
    def __init__(self):
        super().__init__(GameStates.PLAYING)

    def on_enter(self):
        LEVEL_MANAGER.new_level(1)

        self.update_timer = Timer(20)
        self.update_timer.start()

        from src.player.ghost import Ghost
        self.ghosts: dict[int, Ghost] = {} 

        self.node = self.owner.network_node
        if self.node:
            for client in self.node.clients.keys():
                # dont create a ghost for the current player
                if client == self.owner.network_node.id:
                    continue

                new_ghost = Ghost()
                self.ghosts[client] = new_ghost
        
    def update(self):
        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 

        if self.node:
            updates = self.node.get_updates()
            for update in updates:
                ghost = self.ghosts[update[0]]
                ghost.update(pygame.Vector2(update[1], update[2]))
            
            if self.update_timer.is_done:
                self.node.broadcast_message(
                    MsgType.UPDATE,
                    (self.node.id, int(LEVEL_MANAGER.player.position.x), int(LEVEL_MANAGER.player.position.y))
                )
                self.update_timer.start()

        CAMERA.move_to(LEVEL_MANAGER.player.center)

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        for ghost in self.ghosts.values():
            ghost.render(display, offset)
