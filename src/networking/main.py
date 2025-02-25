import argparse, threading
from .host import Host
from .client import Client
from .network import MsgType, Address


class Main:
    def __init__(self, username: str, host: bool):
        self.node = Host(username) if host else Client(username)
        self.running = True
        self.command_thread = threading.Thread(target=self.handle_commands)
        self.command_thread.start()
        self.node.start()
        print(self.node)
    
    def handle_commands(self):
        try:
            while self.running:
                command = input().split(' ')
                match command:
                    case ['/s']:
                        if isinstance(self.node, Host):
                            self.node.start_session()
                            print('Starting session')
                            print(f'Join code: {self.node.join_code}')
                        else:
                            print('Node is not host')
                    case ['/i']:
                        print(self.node)
                    case ['/j', join_code]:
                        if isinstance(self.node, Client):
                            print(f'Joining session with {join_code}')
                            self.node.join(join_code)
                        else:
                            print('Node is not client')
                    case ['/jw', address, port]:
                        if isinstance(self.node, Client):
                            print(f'Joining session with {address}:{port}')
                            self.node.join_addr(Address(str(address), int(port)))
                        else:
                            print('Node is not client')
                    case ['/p', ip, port]:
                        self.node.punch((str(ip), int(port)))
                    case ['/code']:
                        print(f'Join code: {self.node.get_join_code()}')
                    case ['/d']:
                        print('Disconnecting')
                        self.node.disconnect()
                    case ['/c']:
                        print('Clients:')
                        print(self.node.clients)
                    case ['/q']:
                        print('Exiting')
                        self.node.stop()
                        self.running = False
                    case _:
                        msg = ' '.join(command)
                        self.node.broadcast_message(MsgType.CHAT, (self.node.id, msg))
        except KeyboardInterrupt:
            pass
        except EOFError:
            pass
        finally:
            self.running = False
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start or host a client')
    parser.add_argument('-u', '--username', required=True, type=str, help='Username')
    parser.add_argument('-H', '--host', action='store_true', help='Host a session')
    args = parser.parse_args()
    Main(args.username, args.host)
