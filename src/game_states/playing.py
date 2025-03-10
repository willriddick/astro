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
            for client, (username, _) in self.node.clients.items():
                # dont create a ghost for the current player
                if client == self.owner.network_node.id:
                    continue

                new_ghost = Ghost(username)
                self.ghosts[client] = new_ghost
        
    def update(self):
        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 

        if self.node:
            updates = self.node.get_updates()
            for update in updates:
                ghost = self.ghosts.get(update[0])
                if ghost:
                    ghost.update(
                        new_pos=pygame.Vector2(update[1], update[2]),
                        current_anim=update[3],
                        flip_x=bool(update[4]),
                        flash=bool(update[5]),
                        alpha=bool(update[6])
                    )
            
            if self.update_timer.is_done:
                player = LEVEL_MANAGER.player
                self.node.broadcast_message(
                    MsgType.UPDATE,
                    (
                        self.node.id, 
                        int(player .position.x), 
                        int(player.position.y),
                        int(player.sprite.current.value),
                        bool(player.sprite.flip_x),
                        bool(player.sprite.flash_timer.is_active),
                        bool(player.sprite.alpha_timer.is_active)
                    )
                )
                self.update_timer.start()

        CAMERA.move_to(LEVEL_MANAGER.player.center)

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        for ghost in self.ghosts.values():
            ghost.render(display, offset)
