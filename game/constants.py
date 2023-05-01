import pygame

from color import Color
from item_type import Type
from PIL import Image

MINUS_POINTS_SOUND = 'assets/sounds/minus_points.wav'

START_SOUND = 'assets/sounds/start_sound.wav'

PLUS_POINTS_SOUND = 'assets/sounds/plus_points.wav'

CORRECT_CHOICE_SOUND = 'assets/sounds/correct_choice.wav'

IMAGE_THREE_HEART = 'assets/images/three_hearts.png'

IMAGE_ONE_HEART = 'assets/images/one_heart.png'

IMAGE_MORE_HEART = 'assets/images/more_hearts.png'

IMAGE_TWO_HEART = 'assets/images/two_hearts.png'

IMAGE_YOU_DIED = 'assets/images/you_died.png'

IMAGE_ENTER_NAME = 'assets/images/enter_name.png'

IMAGE_RETRY_ACTIVE = 'assets/images/retry_active.png'

MAIN_MENU_ACTIVE = 'assets/images/go_main_menu_active.png'

MAIN_MENU_INACTIVE = 'assets/images/go_main_menu_inactive.png'

IMAGE_RETRY_INACTIVE = 'assets/images/retry_inactive.png'

NAME_DATA_BASE = 'colorCatcher.db'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WIDTH = 55
HEIGHT = 40
MAX_HEIGHT = 750
MAX_WIDTH = 750

FPS = 60
VEL = 5

current_movement = False

live_count = 3


GAME_OBJECTS = [(Image.open('assets/images/star.png'),  Type.STAR),
                (Image.open('assets/images/rhombus.png'), Type.RHOMBUS),
                (Image.open('assets/images/square.png'), Type.SQUARE),
                (Image.open('assets/images/minus_ten_points.png'), Type.MINUS_TEN_POINTS),
                (Image.open('assets/images/minus_heart.png'), Type.MINUS_HEART)]

# PLAYER_PLATFORMS = [(pygame.image.load('assets/images/player_platform_yellow.png'), Type.PLAYER, Color.YELLOW),
#                     (pygame.image.load('assets/images/player_platform_red.png'), Type.PLAYER, Color.RED),
#                     (pygame.image.load('assets/images/player_platform_green.png'), Type.PLAYER, Color.GREEN)]
PLAYER_PLATFORM = (Image.open('assets/images/player_platform.png'), Type.PLAYER)

# colors and their corresponding rgb values
COLORS = [((250, 253, 15), Color.YELLOW), ((255, 0, 0), Color.RED), ((0, 255, 0), Color.GREEN)]

IMAGE_GO_BACK_ACTIVE = pygame.image.load('assets/images/go_back_active.png')
IMAGE_GO_BACK_ACTIVE = pygame.transform.scale(IMAGE_GO_BACK_ACTIVE, (50, 25))
IMAGE_GO_BACK_INACTIVE = pygame.image.load('assets/images/go_back_inactive.png')
IMAGE_GO_BACK_INACTIVE = pygame.transform.scale(IMAGE_GO_BACK_INACTIVE, (50, 25))

IMAGE_INACTIVE = pygame.image.load(IMAGE_RETRY_INACTIVE)
IMAGE_INACTIVE = pygame.transform.scale(IMAGE_INACTIVE, (150, 75))
IMAGE_ACTIVE = pygame.image.load(IMAGE_RETRY_ACTIVE)
IMAGE_ACTIVE = pygame.transform.scale(IMAGE_ACTIVE, (150, 75))
IMAGE_DASHBOARD_INACTIVE = pygame.image.load(MAIN_MENU_INACTIVE)
IMAGE_DASHBOARD_INACTIVE = pygame.transform.scale(IMAGE_DASHBOARD_INACTIVE, (200, 75))
IMAGE_DASHBOARD_ACTIVE = pygame.image.load(MAIN_MENU_ACTIVE)
IMAGE_DASHBOARD_ACTIVE = pygame.transform.scale(IMAGE_DASHBOARD_ACTIVE, (200, 75))

IMAGE_START_INACTIVE = pygame.image.load('assets/images/lets_go.png')
IMAGE_START_INACTIVE = pygame.transform.scale(IMAGE_START_INACTIVE, (150, 75))
IMAGE_START_ACTIVE = pygame.image.load('assets/images/lets_go_active.png')
IMAGE_START_ACTIVE = pygame.transform.scale(IMAGE_START_ACTIVE, (150, 75))
IMAGE_DASHBOARD_ACTIVE = pygame.image.load('assets/images/dashboard_active.png')
IMAGE_DASHBOARD_ACTIVE = pygame.transform.scale(IMAGE_DASHBOARD_ACTIVE, (150, 75))
IMAGE_DASHBOARD_INACTIVE = pygame.image.load('assets/images/dashboard_inactive.png')
IMAGE_DASHBOARD_INACTIVE = pygame.transform.scale(IMAGE_DASHBOARD_INACTIVE, (150, 75))