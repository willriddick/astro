from enum import IntEnum


Address = tuple[str, int]

class MsgType(IntEnum):
    """Enumeration for message types."""
    JOIN = 0
    ADD_CLIENT = 1
    DISCONNECT = 2
    CHAT = 3
    PING = 4
    UPDATE = 5
    NEW_LEVEL = 6
    PALETTE = 7

MsgFormat = {
    MsgType.JOIN: '16s',  # 16 character username
    MsgType.ADD_CLIENT: 'i 16s 45s i',  # id, 16 character username, 45 character IP, port number 
    MsgType.DISCONNECT: 'i',  # id
    MsgType.CHAT: 'i 64s',  # id, 64 character message
    MsgType.PING: 'i',  # id
    MsgType.UPDATE: 'i iiii???',  # id, x, y, current_anim, current_particle, flip_x, flash, alpha
    MsgType.NEW_LEVEL: 'ii',  # seed, config
    MsgType.PALETTE: 'ii',  # id, palette index
}


class Message:
    def __init__(self, type: MsgType, data: tuple, address: Address):
        self.type = type
        self.data = data
        self.address = address
    
    def __str__(self):
        return f'{self.type.name}: {self.data}, {self.address}'
