from enum import Enum


class Attribute(Enum):
    """"""
    ENTRANCE = '☆'
    EXIT     = '★'
    BRANCH   = '╳'
    BRIDGE   = '╲'
    COLLECTABLE = 'i'

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self):
        return self.symbol
