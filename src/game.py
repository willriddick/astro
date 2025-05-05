import asyncio
import sys
import pygame
from src.util import CommandPrompt, StateMachine
from src.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, ASPECT_RATIO
from src.debug import DEBUG
from src.clock import CLOCK
from src.camera import CAMERA
from src.settings import SETTINGS
from src.sounds import SOUNDS
from src.inputs import INPUTS
from src.level_manager import LEVEL_MANAGER
from src.game_states import GameStates, MainMenu, LobbySingleplayer, Singleplayer, LobbyHost, LobbyJoin, Multiplayer
from src.networking import Host, Client, NetworkNode, MsgType
import src.graphics as graphics


class Game:
    """Main class that handles the game loop state machine."""

    def __init__(self):
        pygame.init()
        self.running = False
        scale = SETTINGS.get('window_scale')
        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * scale, DISPLAY_HEIGHT * scale),
            pygame.SCALED
        )
        self.set_fullscreen(SETTINGS.get('fullscreen'))

        graphics.load()
        pygame.display.set_caption('Astro')
        pygame.display.set_icon(graphics.ICON)

        self.events: list[pygame.event.Event] = []  
        self.command_prompt = CommandPrompt()

        self.state_machine = StateMachine(self, [
            MainMenu(), LobbySingleplayer(), Singleplayer(),
            LobbyHost(), LobbyJoin(), Multiplayer()
        ])
        self.network_node: NetworkNode = None

    async def run(self):
        """Main game loop that handles events, updates, and rendering."""
        self.running = True
        SOUNDS.play('music/track1', loops=-1)

        while self.running:
            DEBUG.update()

            if SETTINGS.get('show_fps') or DEBUG.enabled:
                DEBUG.add_display(f'fps: {CLOCK.fps}')

            INPUTS.disabled = True if self.command_prompt.enabled else False

            self.events = pygame.event.get()
            for event in self.events:
                self.handle_event(event)
                self.command_prompt.handle_event(event)

            self.state_machine.update()
            CAMERA.update()

            # handle commmands and draw command prompt
            self.handle_commands()
            self.command_prompt.render(CAMERA.display)

            try:
                self.window.blit(pygame.transform.scale(CAMERA.display, self.window.get_size()))
                pygame.display.flip()
                CLOCK.update()
            except KeyboardInterrupt:
                self.running = False
            
            await asyncio.sleep(0)

        if self.network_node:
            self.network_node.stop()

        pygame.quit()
        sys.exit()

    def handle_commands(self):
        """Handle commands from the command prompt."""
        command = self.command_prompt.pop_command()
        if command == '': 
            return

        player = LEVEL_MANAGER.player
        match command.split():
            case ['d']:
                DEBUG.toggle()
            case ['q']:
                self.running = False
            case ['g']:
                if player:
                    player.toggle_ghost()
            case ['n']:
                LEVEL_MANAGER.new_level()
            case ['n', seed]:
                LEVEL_MANAGER.new_level(seed=seed)
            case ['r']:
                if player:
                    player.spawn(player.spawn_position)
            case ['tp', x, y]:
                if player:
                    player.set_position(pygame.Vector2(int(x), int(y)))
                    SOUNDS.play('teleport')
            case ['f']:
                self.toggle_fullscreen()
            case ['gs', state]:
                self.state_machine.switch(list(GameStates)[int(state)])
            case ['q1']:
                self.network_node = Host('will', port=45678)
                self.network_node.start()
                self.network_node.start_session()
                self.state_machine.switch(GameStates.LOBBY_HOST)
            case ['q2']:
                async def join():
                    self.network_node = Client('drew')
                    self.network_node.start()
                    joined = await self.network_node.join('YCUADU5SNY')
                    if joined:
                        self.state_machine.switch(GameStates.LOBBY_JOIN)
                
                asyncio.create_task(join())
            case ['info']:
                if self.network_node:
                    print(self.network_node)
            case ['msg', msg]:
                if self.network_node:
                    self.network_node.broadcast_message(MsgType.CHAT, (self.network_node.id, msg))
            case ['join', join_code]:
                if isinstance(self.network_node, Client):
                    print(f'Joining session with {join_code}')
                    self.network_node.join(join_code)
                else:
                    print('Node is not client')
            case ['disconnect']:
                if self.network_node:
                    print('Disconnecting')
                    self.network_node.disconnect()
            case ['clients']:
                if self.network_node:
                    print('Clients:')
                    print(self.network_node.clients)
            case _:
                print(f'Unknown command: {command}')
    
    def handle_event(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(event.w, event.h)
        if event.type == pygame.FULLSCREEN:
            self.toggle_fullscreen
    
    def handle_resize(self, width, height):
        new_width = width
        new_height = int(new_width / ASPECT_RATIO)
        if new_height > height:
            new_height = height
            new_width = int(new_height * ASPECT_RATIO)
        self.window = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
    
    def toggle_fullscreen(self):
        self.set_fullscreen(not SETTINGS.get('fullscreen'))

    def set_fullscreen(self, value: bool):
        SETTINGS.set_key('fullscreen', value)
        if value:
            size = (0, 0)
            mode = pygame.FULLSCREEN
        else:
            scale = SETTINGS.get('window_scale')
            size = (DISPLAY_WIDTH * scale, DISPLAY_HEIGHT * scale)
            mode = pygame.RESIZABLE

        self.window = pygame.display.set_mode(size, mode)
    