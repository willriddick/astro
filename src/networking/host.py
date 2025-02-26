from .network import NetworkNode, Address, MsgType, generate_join_code
from src.util import Timer


class Host(NetworkNode):
    def __init__(self, username: str, ip: str = '', port: int = 0):
        super().__init__(username, ip, port)
        self.join_code = ''
        self.id = 0
        self.next_id = 1

        self.client_ping: dict[int, Timer] = {}

    def start_session(self):
        self.join_code = generate_join_code(self.get_address())
        #self.join_code = generate_join_code(self.public_ip, self.port)
        self.add_client(self.id, self.username, (self.ip, self.port))
    
    def disconnect(self):
        self.broadcast_message(
            MsgType.DISCONNECT,
            (self.id,)
        )
        self.clients = {}

    def handle_message(self, type, data, addr):
        match type:
            case MsgType.JOIN:
                self.handle_join(data, addr)
                print(data, addr)
            case MsgType.DISCONNECT:
                self.handle_disconnect(data)        
            case MsgType.CHAT:
                self.handle_chat(data)
            case MsgType.UPDATE:
                self.update_queue.put(data)
            case MsgType.PING:
                self.update_ping(data[0])
            case _:
                print(f'Unknown message type: {type}')
    
    def update_ping(self, client_id: int):
        self.client_ping[client_id].start(1000 * 10)
        for cur_id, timer in self.client_ping.items():
            if timer.is_done:
                print(f'{self.clients[cur_id][0]} ({cur_id}) timed out')
    
    def handle_chat(self, data: tuple):
        username = self.clients[data[0]][0]
        print(f'{username}: {data[1].rstrip('\x00')}')
    
    def handle_disconnect(self, data: tuple):
        client_id = data[0]
        print(f'{self.clients[client_id][0]} ({client_id}) disconnected')
        self.remove_client(client_id)

        self.broadcast_message(
            MsgType.DISCONNECT,
            (client_id,)
        )

    def handle_join(self, data: tuple, address: Address):
        if len(data) > 0:
            client_id = self.next_id
            self.next_id += 1
            username = data[0].rstrip('\x00')
            print(f'{username} ({client_id}) joined')

            # notify the new client of all existing clients
            for cur_id, cur_data in self.clients.items():
                cur_username = cur_data[0]
                cur_ip = cur_data[1][0] 
                cur_port = cur_data[1][1]
                
                self.send_message(
                    MsgType.ADD_CLIENT,
                    (cur_id, cur_username, cur_ip, cur_port),
                    address
                )
            
            # add client to host list
            self.add_client(client_id, username, address)

            # notify all clients of the new client, including the new client
            # the new client will use this message to set its ID
            self.broadcast_message(
                MsgType.ADD_CLIENT,
                (client_id, username, address[0], address[1])
            )
