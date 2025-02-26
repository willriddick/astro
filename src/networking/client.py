from .network import NetworkNode, MsgType, decode_join_code, Address, generate_join_code


class Client(NetworkNode):
    def __init__(self, username: str, ip: str = '', port: int = 0):
        super().__init__(username, ip, port)
        self.host_addr: Address = None
   
    def join(self, join_code: str):
        print(join_code)
        self.host_addr = decode_join_code(join_code)
        print('Decoded join code:')
        print(f'Host address: {self.host_addr}')
        self.send_message(MsgType.JOIN, (self.username,), self.host_addr)
    
    def join_addr(self, host_addr: tuple[str, int]):
        self.host_addr = host_addr
        self.send_message(MsgType.JOIN, (self.username,), self.host_addr)

    def get_join_code(self) -> str:
        return generate_join_code(self.get_address())
    
    def disconnect(self):
        if self.clients.get(0):
            self.send_message(MsgType.DISCONNECT, (self.id,), self.host_addr )
        self.host_addr= None
        self.clients = {}
        
    def ping(self):
        self.send_message(MsgType.PING, (self.id,), self.host_addr)
    
    def handle_message(self, type: MsgType, data: tuple, addr: Address):
        match type:
            case MsgType.ADD_CLIENT:
                self.handle_add_client(data) 
            case MsgType.DISCONNECT:
                self.handle_disconnect(data)
            case MsgType.CHAT:
                self.handle_chat(data)
            case MsgType.UPDATE:
                self.update_queue.put(data)
            case MsgType.JOIN:
                print(f'Received join message from: {addr}')
            case _:
                print(f'Unknown message type: {type}')

    def handle_chat(self, data: tuple):
        username = self.clients[data[0]][0]
        print(f'{username}: {data[1].rstrip('\x00')}')
    
    def handle_disconnect(self, data: tuple):
        client_id = data[0]
        username = self.clients[client_id][0] 
        print(f'{username} ({client_id}) disconnected')
        self.remove_client(client_id)

        # if host disconnected, stop
        if client_id == 0:
            self.disconnect()
    
    def handle_add_client(self, data: tuple):
        client_id = data[0]
        username = data[1].rstrip('\x00')
        address = (data[2].rstrip('\00'), data[3])
        self.add_client(client_id, username, address)

        if self.get_address() == address:
            self.id = client_id
            print(f'Joined {self.clients[0][0]}\'s session')
    