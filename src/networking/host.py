from .network import NetworkNode, Address, Message, MsgType, generate_join_code


class Host(NetworkNode):

    MAX_CLIENTS = 4

    def __init__(self, username: str, ip: str = '', port: int = 0):
        super().__init__(username, ip, port)
        self.join_code = ''
        self.id = 0
        self.next_id = 1

    def start_session(self):
        self.join_code = generate_join_code(self.get_address())
        self.add_client(self.id, self.username, (self.ip, self.port))
    
    def disconnect(self):
        self.broadcast_message(
            MsgType.DISCONNECT,
            (self.id,)
        )
        self.clients = {}

    def handle_message(self, msg: Message):
        match msg.type:
            case MsgType.JOIN:
                self.handle_join(msg.data, msg.address)
            case MsgType.DISCONNECT:
                self.handle_disconnect(msg.data)        
            case MsgType.CHAT:
                self.handle_chat(msg.data)
            case MsgType.UPDATE:
                self.event_queue.put(msg)
            case _:
                print(f'Unknown message type: {msg.type}')
   
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
        if len(self.clients) > self.MAX_CLIENTS:
            print('Session full')
            return

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
