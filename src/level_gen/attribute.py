from enum import Enum


class Attribute(Enum):
    """"""
    ENTRANCE = '☆'
    EXIT     = '★'
    BRANCH   = '╳'
    BRIDGE   = '╲'
    ITEM_ONE = 'i'
    ITEM_TWO = 'i'

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self):
        return self.symbol
