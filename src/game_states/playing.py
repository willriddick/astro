import pygame
from src.util import State, Timer
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.networking import Message, MsgType
from .game_states import GameStates


class Playing(State):
    def __init__(self):
        super().__init__(GameStates.PLAYING)

    def on_enter(self):
        seed = 5
        config_index = 0
        LEVEL_MANAGER.new_level(seed, config_index)

        self.update_timer = Timer(20)
        self.update_timer.start()

        from src.player.ghost import Ghost
        self.ghosts: dict[int, Ghost] = {} 

        self.node = self.owner.network_node
        if self.node:
            if self.node.is_host:
                self.node.broadcast_message(
                    MsgType.NEW_LEVEL,
                    (seed, config_index)
                )
                print('Broadcasted new level')

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
            events: list[Message] = self.node.get_events()

            for event in events:
                match event.type:
                    case MsgType.UPDATE:
                        print(event)
                        ghost = self.ghosts.get(event.data[0])
                        if ghost:
                            ghost.update(
                                new_pos=pygame.Vector2(event.data[1], event.data[2]),
                                current_anim=event.data[3],
                                flip_x=bool(event.data[4]),
                                flash=bool(event.data[5]),
                                alpha=bool(event.data[6])
                            )
                    case MsgType.NEW_LEVEL:
                        seed, config_index = event.data
                        LEVEL_MANAGER.new_level(seed, config_index)
            
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
