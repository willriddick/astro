import pygame
from src.util import State, Timer
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.clock import CLOCK
from src.ui import UserInterface
from src.networking import Message, MsgType, NetworkNode
from .game_states import GameStates
from .singleplayer import manage_rocket


TRANSITION_DURATION = 3000


class Multiplayer(State):
    def __init__(self):
        super().__init__(GameStates.MULTIPLAYER)
        self.node: NetworkNode = None

        self.level_index = 1
        self.next_timer = Timer(TRANSITION_DURATION)
        self.next = False

        self.update_timer = Timer(40)

        self.duration = 0.0
        self.fuel_cells_collected = 0

        self.ui = UserInterface()

        from src.player.ghost import Ghost
        self.ghosts: dict[int, Ghost] = {} 

    def on_enter(self):
        from src.player.ghost import Ghost
        self.node = self.owner.network_node
        self.update_timer.start()
        CAMERA.transition(1000, focus=1, fade=-1)
        LEVEL_MANAGER.new_level()

        for client, (username, _) in self.node.clients.items():
            # dont create a ghost for the current player
            if client == self.node.id:
                continue

            new_ghost = Ghost(username)
            self.ghosts[client] = new_ghost
    
    def update(self):
        self.duration += CLOCK.dt

        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 
        CAMERA.move_to(LEVEL_MANAGER.player.center)

        self.fuel_cells_collected = manage_rocket()

        self.ui.update(
            self.duration,
            self.fuel_cells_collected, 
            len(LEVEL_MANAGER.current.fuel_cells),
            self.level_index
        )

        self.handle_events()
        self.broadcast_update()

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        for ghost in self.ghosts.values():
            ghost.render(display, offset)
        self.ui.render(display, offset)
    
    def broadcast_update(self) -> None:
        if not self.node:
            return 

        if self.update_timer.is_done:
            player = LEVEL_MANAGER.player
            self.node.broadcast_message(
                MsgType.UPDATE,
                (
                    self.node.id, 
                    int(player.position.x), 
                    int(player.position.y),
                    int(player.sprite.current.value),
                    bool(player.sprite.flip_x),
                    bool(player.sprite.flash_timer.is_active),
                    bool(player.sprite.alpha_timer.is_active)
                )
            )
            self.update_timer.start()
    
    def handle_events(self) -> None:
        if not self.node:
            return

        events: list[Message] = self.node.get_events()

        for event in events:
            match event.type:
                case MsgType.UPDATE:
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
 