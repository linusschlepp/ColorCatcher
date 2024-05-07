import pygame

from color import Color
from item_type import Type
from PIL import Image

MINUS_POINTS_SOUND_PATH = 'assets/sounds/minus_points.wav'

START_SOUND_PATH = 'assets/sounds/start_sound.wav'

PLUS_POINTS_SOUND_PATH = 'assets/sounds/plus_points.wav'

CORRECT_CHOICE_SOUND_PATH = 'assets/sounds/correct_choice.wav'

THREE_HEART_IMAGE_PATH = 'assets/images/three_hearts.png'

ONE_HEART_IMAGE_PATH = 'assets/images/one_heart.png'

MORE_HEART_IMAGE_PATH = 'assets/images/more_hearts.png'

TWO_HEART_IMAGE_PATH = 'assets/images/two_hearts.png'

YOU_DIED_IMAGE_PATH = 'assets/images/you_died.png'

ENTER_NAME_IMAGE_PATH = 'assets/images/enter_name.png'

MAIN_MENU_IMAGE_PATH = 'assets/images/go_main_menu.png'

RETRY_IMAGE_PATH = 'assets/images/retry.png'

GO_BACK_IMAGE_PATH = 'assets/images/go_back.png'

STAR_IMAGE_PATH = 'assets/images/star.png'

RHOMBUS_IMAGE_PATH = 'assets/images/rhombus.png'

SQUARE_IMAGE_PATH = 'assets/images/square.png'

MINUS_POINTS_IMAGE_PATH = 'assets/images/minus_ten_points.png'

MINUS_HEART_IMAGE_PATH = 'assets/images/minus_heart.png'

PLAYER_PLATFORM_IMAGE_PATH = 'assets/images/player_platform.png'

LETS_GO_IMAGE_PATH = 'assets/images/lets_go.png'

SCORE_LIST_IMAGE_PATH = 'assets/images/score_list.png'

NAME_DATA_BASE = 'colorCatcher.db'

# Colors used within color catcher
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (250, 253, 15)
GREEN = (0, 255, 0)

WIDTH = 55
HEIGHT = 40
MAX_HEIGHT = 750
MAX_WIDTH = 750

FPS = 60
VEL = 5

# Width for buttons
BUTTON_WIDTH = 280

CURRENT_MOVEMENT = False


GAME_OBJECTS = [(Image.open(STAR_IMAGE_PATH), Type.STAR),
                (Image.open(RHOMBUS_IMAGE_PATH), Type.RHOMBUS),
                (Image.open(SQUARE_IMAGE_PATH), Type.SQUARE),
                (Image.open(MINUS_POINTS_IMAGE_PATH), Type.MINUS_TEN_POINTS),
                (Image.open(MINUS_HEART_IMAGE_PATH), Type.MINUS_HEART),
                (Image.open(ONE_HEART_IMAGE_PATH), Type.HEART)]

PLAYER_PLATFORM = (Image.open(PLAYER_PLATFORM_IMAGE_PATH), Type.PLAYER)



# colors and their corresponding rgb values
COLORS = [(YELLOW, Color.YELLOW), (RED, Color.RED), (GREEN, Color.GREEN)]

IMAGE_GO_BACK = pygame.transform.scale(pygame.image.load(GO_BACK_IMAGE_PATH), (50, 25))

IMAGE_RETRY = pygame.transform.scale(pygame.image.load(RETRY_IMAGE_PATH), (150, 75))
IMAGE_MAIN_MENU = pygame.transform.scale(pygame.image.load(MAIN_MENU_IMAGE_PATH), (200, 75))

IMAGE_GAME_START = pygame.transform.scale(pygame.image.load(LETS_GO_IMAGE_PATH), (150, 75))
IMAGE_LIST_SCORE = pygame.transform.scale(pygame.image.load(SCORE_LIST_IMAGE_PATH), (150, 75))
