import asyncio
from .network import NetworkNode, MsgType, decode_join_code, Address, generate_join_code, Message


class Client(NetworkNode):
    def __init__(self, username: str, ip: str = '', port: int = 0):
        super().__init__(username, ip, port)
        self.host_addr: Address = None
        self.join_event = asyncio.Event()
   
    async def join(self, join_code: str, timeout=5) -> bool:
        try: 
            self.host_addr = decode_join_code(join_code)
            print(f'Decoded join code to host address: {self.host_addr}')
            self.send_message(MsgType.JOIN, (self.username,), self.host_addr)

            try:
                await asyncio.wait_for(self.join_event.wait(), timeout)
                return True  # successfully joined
            except asyncio.TimeoutError:
                print("Join attempt timed out: No response from host.")
                return False  # failed to join
        except:
            return False
    
    def get_join_code(self) -> str:
        return generate_join_code(self.get_address())
    
    def disconnect(self):
        if self.clients.get(0):
            self.send_message(MsgType.DISCONNECT, (self.id,), self.host_addr )
        self.host_addr= None
        self.clients = {}
        
    def handle_message(self, msg: Message):
        match msg.type:
            case MsgType.ADD_CLIENT:
                self.handle_add_client(msg.data) 
            case MsgType.DISCONNECT:
                self.handle_disconnect(msg.data)
                self.event_queue.put(msg)
            case MsgType.CHAT:
                self.handle_chat(msg.data)
            case MsgType.UPDATE:
                self.event_queue.put(msg)
            case MsgType.NEW_LEVEL:
                self.event_queue.put(msg)
            case MsgType.JOIN:
                print(f'Received join message from: {msg.addr}')
            case _:
                print(f'Unknown message type: {msg.type}')

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
            self.join_event.set()
            print(f'Joined {self.clients[0][0]}\'s session')
    