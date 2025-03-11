import socket
import struct
import base64
import threading
import queue
import http.client
import time
from .message import Address, Message, MsgType, MsgFormat


class NetworkNode:
    """
    Represents a network node for sending and receiving UDP messages.
    """
    def __init__(self, username: str, ip: str = "", port: int = 0):
        """
        Initialize the network node.
        Args:
            ip (str): The IP address to bind the socket. Defaults to the machine's local IP.
            port (int): The port to bind the socket. Defaults to 0, which assigns an ephemeral port.
        """
        self.username = username
        self.ip = ip
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.get_address())
        self.socket.settimeout(1.0) 
        self.port = self.socket.getsockname()[1]
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.public_ip = self.get_public_ip()
        
        self.id = -1
        self.clients: dict[int, (str, Address)] = {}

        self.running = False
        self.receive_thread: threading.Thread = None
        self.process_thread: threading.Thread = None
        self.message_queue = queue.Queue()
        self.event_queue = queue.Queue()

    def __str__(self) -> str:
        return f'Public IP: {self.public_ip}, Address: {self.get_address()}, ID: {self.id}'
    
    @property
    def is_host(self) -> bool:
        """
        Check if this network node is a host.
        """
        return self.id == 0 
    
    def punch(self, address: Address):
        """
        Send a message to the server to establish a connection.
        """
        start_time = time.time()
        while time.time() - start_time < 60:
            self.send_message(MsgType.JOIN, (self.username), address)
            time.sleep(1)  # sends every second for 60 seconds
    
    def start(self):
        """
        Start the network node to begin sending and receiving messages.
        """
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        self.process_thread = threading.Thread(target=self.process_messages)
        self.process_thread.start()
    
    def stop(self):
        """
        Stop the network node from sending and receiving messages.
        """
        self.running = False
        if self.receive_thread:
            self.receive_thread.join()
        if self.process_thread:
            self.process_thread.join()
    
    def receive_messages(self):
        """
        Continuously receive messages from the network.
        """
        while self.running:
            try:
                type, data, address = self.receive_message()
                self.message_queue.put(Message(type, data, address))
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error in receive thread: {e}")
                break
    
    def process_messages(self):
        """
        Continuously process messages from the queue.
        """
        while self.running or not self.message_queue.empty():
            try:
                message = self.message_queue.get(timeout=1)
                self.handle_message(message)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing message: {e}, Data: {message.data}, Type: {message.type}, From: {message.address}")
   
    def handle_message(self, message: Message):
        """
        Handle a received message based on its type.
        """
        raise NotImplementedError("handle_message method must be implemented in a subclass.")
    
    def get_events(self) -> list[Message]:
        """
        Get all event messages from the queue.
        """
        events = []
        while not self.event_queue.empty():
            events.append(self.event_queue.get())

        return events
    
    def add_client(self, client_id: int, username: str, address: Address):
        """
        Add a client to the list of clients.
        """
        if client_id not in self.clients:
            self.clients[client_id] = (username, address)
    
    def remove_client(self, client_id: int):
        """
        Remove a client from the list of clients.
        """
        if client_id in self.clients:
            del self.clients[client_id]
    
    def broadcast_message(self, type: MsgType, data: tuple, exclude: list[int]=[]): 
        """
        Send a message to all clients except the sender and those in the exclude list.
        """
        for client_id, info in self.clients.items():
            if client_id != self.id and client_id not in exclude:
                address = info[1]
                self.send_message(type, data, address)
    
    def get_address(self) -> Address:
        """
        Get the address (IP and port) of this network node.
        Returns:
            Address: A tuple of the IP address and port.
        """
        return self.ip, self.port
    
    def get_public_ip(self) -> str: 
        try: 
            conn = http.client.HTTPSConnection("api.ipify.org") 
            conn.request("GET", "/") 
            response = conn.getresponse() 
            return response.read().decode() 
        except Exception as e: 
            print(f"Error: {e}")  
    
    def send_message(self, msg_type: MsgType, data: tuple, target_addr: Address):
        """
        Send a message to a target address.
        Args:
            msg_type (MsgType): The type of message to send.
            target_addr (Address): The address of the recipient.
            data (tuple): The data to send with the message, packed as a tuple.
        Raises:
            ValueError: If the message type is invalid.
        """
        # ensure data is always a tuple
        if not isinstance(data, tuple):
            data = (data,)
        packed_data = self.pack_message(msg_type, data)
        self.socket.sendto(packed_data, target_addr)

    def receive_message(self, buffer_size: int = 1024) -> tuple[MsgType, tuple, Address]:
        """
        Receive a message from the socket.
        Args:
            buffer_size (int): The maximum size of the buffer to read data. Defaults to 1024.
        Returns:
            tuple[MsgType, tuple, Address]: A tuple containing the message type, data, and sender's address.
        Raises:
            ValueError: If the received message type is invalid.
        """
        packed_data, address = self.socket.recvfrom(buffer_size)
        msg_type, data = self.unpack_message(packed_data)
        return msg_type, data, address
    
    @staticmethod
    def pack_message(msg_type: MsgType, data: tuple) -> bytes:
        """
        Pack the message type and data into binary format.
        Args:
            msg_type (MsgType): The type of message to pack.
            data (tuple): The data to send, provided as a tuple.
        Returns:
            bytes: The packed message ready to be sent over the network.
        """
        fmt = MsgFormat[msg_type]
        
        # check if the data contains a single element that should be packed differently
        encoded_data = [d.encode() if isinstance(d, str) else d for d in data]

        try:
            # use the format string and pack the message
            packed_data = struct.pack(f'i{fmt}', msg_type.value, *encoded_data)  # Packing message type and data
        except Exception as e:
            raise ValueError(f'Error packing message {msg_type.name}: {e}')
        
        return packed_data

    @staticmethod
    def unpack_message(packed_data: bytes) -> tuple[MsgType, tuple]:
        """
        Unpack a byte sequence into a message type and its data.
        Args:
            packed_data (bytes): The packed byte sequence received.
        Returns:
            tuple[MsgType, tuple]: A tuple containing the message type and the unpacked data.
        Raises:
            ValueError: If the message type is invalid.
        """
        # extract message type from the first 4 bytes
        msg_type = MsgType(struct.unpack('i', packed_data[:4])[0]) 
        if msg_type not in MsgFormat:
            raise ValueError("Invalid message type")
        
        # get the format string and unpack the rest of the data
        fmt = MsgFormat[msg_type]
        encoded_data = struct.unpack(fmt, packed_data[4:])
        
        # convert byte values to strings where applicable
        data = tuple(d.decode().rstrip('\00') if isinstance(d, bytes) else d for d in encoded_data)

        return msg_type, data

def generate_join_code(address: Address) -> str:
    """
    Generate a join code by encoding IP, port, and session ID into a Base32 string.
    Args:
        ip (str): The IPv4 address in dotted-decimal notation (e.g., "192.168.1.1").
        port (int): The port number to encode.
    Returns:
        str: A Base32-encoded string representing the join code, with padding removed.
    Raises:
        socket.error: If the provided IP address is invalid.
        struct.error: If the input data cannot be packed due to size or format issues.
    """
    ip, port = address
    ip_int = struct.unpack('!I', socket.inet_aton(ip))[0]
    packed = struct.pack('!IH', ip_int, port)

    return base64.b32encode(packed).decode().rstrip('=')

def decode_join_code(code: str) -> Address:
    """
    Decode a join code to retrieve the original IP, port, and session ID.
    Args:
        code (str): The Base32-encoded join code, without padding.
    Returns:
        tuple[Address, int]: A tuple containing:
            - Address: The decoded IPv4 address as a dotted-decimal string (e.g., "192.168.1.1") 
              and port number (int).
    Raises:
        ValueError: If the input code is malformed or cannot be decoded.
        struct.error: If the decoded binary data is not in the expected format.
    """
    code += '=' * (-len(code) % 8)  # restore padding for decoding
    packed = base64.b32decode(code)
    ip_int, port = struct.unpack('!IH', packed)
    ip = socket.inet_ntoa(struct.pack('!I', ip_int))

    return ip, port