from enum import Enum

class Status(Enum):
    """
    Represents the connection status of an adjacent room  .
    Attributes:
        symbol (str): A string symbol representing the status.
    """
    EMPTY    = '□'
    UNLINKED = '○'
    LINKED   = '●'

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol
