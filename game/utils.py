import random
import time
from typing import Tuple

import pygame
import constants
from game_object import GameObject
from item_type import Type


def update_score(WIN, score_count: int):
    """
    Updates score on screen

    :param WIN: Window/ screen
    :param score_count: Current score
    """
    font = pygame.font.SysFont('Consolas', 25)
    text = font.render('Score:' + str(score_count), True, constants.BLACK)
    WIN.blit(text, (0, 0))


def time_run_out(time_delta, time_stamp) -> bool:
    """
    Checks if the time has run out and a color change occurs

    :param time_delta: Delta for change
    :param time_stamp: Timestamp when last color-change was conducted
    :return: True if time has run out, false if not
    """
    return round(time.time() * 1000) - time_delta > time_stamp


def reassign_object(game_object: GameObject) -> GameObject:
    """
    Reassigns position of given game object

    :param game_object: GameObject of which the position is reassigned
    :return: GameObject with reassigned position and color
    """
    ran_index = random.randint(0, len(constants.GAME_OBJECTS) - 1)
    ran_color = constants.COLORS[random.randint(0, len(constants.COLORS) - 1)][0]

    game_object.coord_y = random.randint(-1500, -350)
    game_object.coord_x = random.randrange(0, constants.MAX_WIDTH - 25)
    game_object.b_image = color_image_game_object(constants.GAME_OBJECTS[ran_index][0],
                                                  ran_color, constants.GAME_OBJECTS[ran_index][1])
    game_object.color = ran_color
    game_object.type = constants.GAME_OBJECTS[ran_index][1]
    game_object.coord_y = random.randint(-(constants.MAX_HEIGHT * 2), -350)
    game_object.coord_x = random.randrange(0, constants.MAX_WIDTH - 25)

    return game_object


def evaluate_object(game_object: GameObject, player_platform: GameObject, live_count: int, score_count: int) -> tuple[
    int, int]:
    """
    Evaluates different types of GameObject. Determines if it's good are bad
    :param score_count: Score of player
    :param live_count: Lives of player
    :param player_platform: GameObject, which represents player
    :param game_object: GameObject, which collides with player
    """
    if game_object.type == Type.HEART:
        pygame.mixer.Sound(constants.PLUS_POINTS_SOUND).play()
        live_count += 1
    elif game_object.type == Type.MINUS_TEN_POINTS:
        pygame.mixer.Sound(constants.MINUS_POINTS_SOUND).play()
        if score_count <= 10:
            score_count = 0
        else:
            score_count -= 10
    elif game_object.type == Type.TEN_POINTS:
        pygame.mixer.Sound(constants.PLUS_POINTS_SOUND).play()
        score_count += 10
    elif player_platform.color == game_object.color:
        pygame.mixer.Sound(constants.CORRECT_CHOICE_SOUND).play()
        if game_object.type == Type.RHOMBUS:
            score_count += 20
        elif game_object.type == Type.SQUARE:
            score_count += 15
        elif game_object.type == Type.STAR:
            score_count += 10
    else:
        pygame.mixer.Sound(constants.MINUS_POINTS_SOUND).play()
        live_count -= 1

    return live_count, score_count


def check_detection(game_object: GameObject, player_platform: GameObject) -> bool:
    """
    Returns true if player hits GameObject (enemy or item), false if not

    :param game_object: Specific GameObject
    :param player_platform: Player
    :return: True if player collides with GameObject, false if not
    """
    return abs(game_object.coord_y - player_platform.coord_y) < 40 and abs(
        player_platform.coord_x - game_object.coord_x) < 40


def text_objects(text, font):
    text_surface = font.render(text, True, constants.RED)
    return text_surface, text_surface.get_rect()


def handle_movement_player(keys_pressed, player_platform: GameObject):
    """
    Handles the movement of the player

    :param keys_pressed: Current keys pressed
    :param player_platform:  GameObject, representing the player
    """
    if keys_pressed[pygame.K_a] and player_platform.coord_x >= 0:
        player_platform.coord_x -= constants.VEL + 5
    if keys_pressed[pygame.K_d] and player_platform.coord_x <= constants.MAX_WIDTH - constants.WIDTH:
        player_platform.coord_x += constants.VEL + 5


def movement_rhombus(rhombus_object: GameObject, current_movement: bool) -> (GameObject, bool):
    """
    Handles movement of a GameObject representing a rhombus

    :param rhombus_object: GameObject representing a rhombus
    :param current_movement: flag, indicating if rhombus has reached end of scope and needs to turn around
    :return: GameObject (rhombus) with new position, new direction indicator (bool-flag)
    """
    if rhombus_object.coord_x > constants.MAX_WIDTH:
        rhombus_object.coord_x = constants.MAX_WIDTH
        current_movement = False
    if rhombus_object.coord_x < 0:
        rhombus_object.coord_x = 0
        current_movement = True

    if not current_movement:
        rhombus_object.coord_x -= rhombus_object.speed + 1.2 * 2
    else:
        rhombus_object.coord_x += rhombus_object.speed + 1.2 * 2

    return rhombus_object, current_movement


def reset_timer(player_platform: GameObject) -> [int, int, GameObject]:
    """
    Resets internal timer and gives player platform a new color

    :param player_platform: Platform
    """
    pygame.mixer.Sound(constants.START_SOUND).play()
    time_stamp = round(time.time() * 1000)
    time_delta = round(random.randint(4000, 25000))
    ran_index = random.randint(0, len(constants.COLORS) - 1)
    ran_color = constants.COLORS[ran_index][0]
    player_platform.b_image = color_image_game_object(constants.PLAYER_PLATFORM[0], ran_color, Type.PLAYER)
    player_platform.color = ran_color

    return time_stamp, time_delta, player_platform


def create_game_objects() -> list:
    """
    Creates list of different GameObjects, which represent the different enemies/items in the game

    :return: List of GameObjects
    """
    game_objects = []
    for _ in range(0, 40):
        ran_index = random.randint(0, len(constants.GAME_OBJECTS) - 1)
        ran_color = constants.COLORS[random.randint(0, len(constants.COLORS) - 1)][0]
        game_objects.append(
            GameObject(color_image_game_object(constants.GAME_OBJECTS[ran_index][0], ran_color,
                                               constants.GAME_OBJECTS[ran_index][1]), 5,
                       random.randrange(0, constants.MAX_WIDTH - 20),
                       random.randint(-1000, 0), random.randint(0, 50), random.randint(0, 70),
                       constants.GAME_OBJECTS[ran_index][1],
                       ran_color))

    return game_objects


def color_image_game_object(game_object_image, color: tuple, type: Type):
    """
    Takes the default image of the enemy or player and colors it according to passed color(r,g,b) tuple

    :param game_object_image: Standard image of enemy/ player
    :param color: Color-tuple in which the image is colored (uses rgb values)
    :param type: Type of the given Game-object
    :return: Image of game object with new color
    """

    # if the type is just an item leave the function
    if type != Type.RHOMBUS and type != Type.STAR and type != Type.SQUARE and type != Type.PLAYER:
        return game_object_image

    game_object_image_temp = game_object_image.copy()
    width, height = game_object_image.size

    # Processes every pixel
    for x in range(width):
        for y in range(height):
            current_color = game_object_image_temp.getpixel((x, y))
            if current_color != 0:
                game_object_image_temp.putpixel((x, y), color)

    return game_object_image_temp


def convert_image(pil_image) -> pygame.Surface:
    """
    Converts PIL.Image to pygame.Surface

    :param pil_image: PIL.Image to convert
    :return: pygame.Surface, which represents the converted PIL.Image
    """
    str_format = 'RGBA'
    pil_image = pil_image.convert(str_format)
    raw_str = pil_image.tobytes('raw', str_format)
    new_img = pygame.image.fromstring(raw_str, pil_image.size, str_format)

    return new_img
