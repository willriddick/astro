import pygame
from src.util import State, Timer
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.clock import CLOCK
from src.level_gen import CONFIGS
from src.ui import UserInterface
from src.networking import MsgType, NetworkNode
from .game_states import GameStates
from .singleplayer import manage_fuel_cells


TRANSITION_DURATION = 2000


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

        self.ui = UserInterface(palette_index=LEVEL_MANAGER.palette_index)
        self.ui.reset()

        from src.player.ghost import Ghost
        self.ghosts: dict[int, Ghost] = {} 

    def on_enter(self):
        self.node = self.owner.network_node
        self.update_timer.start()
        self.ui.reset()
        CAMERA.transition(1000, focus=1, fade=-1)
        self.create_ghosts()

    def update(self):
        self.duration += CLOCK.dt

        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 
        CAMERA.move_to(LEVEL_MANAGER.player.center)

        self.fuel_cells_collected = manage_fuel_cells()

        self.ui.update(
            self.duration,
            self.fuel_cells_collected, 
            len(LEVEL_MANAGER.current.fuel_cells),
            self.level_index
        )

        self.handle_events()
        self.broadcast_update()
        self.handle_rocket()
                
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        for ghost in self.ghosts.values():
            ghost.render(display, offset)
        self.ui.render(display, offset)
    
    def broadcast_update(self) -> None:
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
        for event in self.node.get_events():
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
                    CAMERA.transition(TRANSITION_DURATION, 0, -1)  # fade the screen
                    seed, index = event.data
                    self.level_index = index + 1 
                    LEVEL_MANAGER.new_level(seed, index)
                case _:
                    print(f'Unknown event: {event}')
    
    def create_ghosts(self) -> None:
        from src.player.ghost import Ghost
        for client, (username, _, palette_index) in self.node.clients.items():
            # dont create a ghost for the current player
            if client == self.node.id:
                continue

            new_ghost = Ghost(username, palette_index)
            self.ghosts[client] = new_ghost
    
    def new_level(self) -> None:
        self.level_index += 1
        seed = int(LEVEL_MANAGER.seed)
        index = self.level_index - 1
        self.node.broadcast_message(MsgType.NEW_LEVEL, (seed, index))
        LEVEL_MANAGER.new_level(seed, index)
    
    def handle_rocket(self) -> None:
        # check if rocket has been collected (make sure next is false so this only triggers once)
        if LEVEL_MANAGER.current.rocket.collected and not self.next:
            self.next = True
            self.next_timer.start()  # start the timer until next level is created
            CAMERA.transition(TRANSITION_DURATION * 2, 0)  # fade the screen

            player = LEVEL_MANAGER.player  # pause the player for rocket animation
            player.visible = False
            player.velocity = pygame.Vector2(0, 0)
            player.pause(TRANSITION_DURATION)
        
        # if next timer is done
        if self.next_timer.is_done and self.next:
            # if there are more levels to play
            if self.level_index < len(CONFIGS):
                self.new_level()
                self.next = False
            else:
                self.owner.state_machine.switch(GameStates.MAIN_MENU)
                self.next = False
    