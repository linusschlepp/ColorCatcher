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
    BUTTON_GAME_START = 9
    BUTTON_SCORE_LIST = 10
    BUTTON_GO_BACK = 11
    BUTTON_RETRY = 12
    BUTTON_MAIN = 13
