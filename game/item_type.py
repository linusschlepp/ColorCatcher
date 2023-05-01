from enum import Enum


class Type(Enum):
    """
    Class representing item-type
    """
    STAR = 1
    RHOMBUS = 2
    SQUARE = 3
    PLAYER = 4
    HEART = 5
    MINUS_HEART = 6
    PLUS_TEN_POINTS = 7
    MINUS_TEN_POINTS = 8
    TEN_POINTS = 9
