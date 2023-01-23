import random
import time

import pygame
import constants
from game_object import GameObject


def update_score(WIN, score_count):
    font = pygame.font.SysFont('Consolas', 25)
    text = font.render('Score:' + str(score_count), True, constants.BLACK)
    WIN.blit(text, (0, 0))


def time_run_out(time_delta, time_stamp):
    return round(time.time() * 1000) - time_delta > time_stamp


def reassign_object(game_object):
    ran_index = random.randint(0, len(constants.GAME_OBJECTS) - 1)
    game_object.coord_y = random.randint(-1500, -350)
    game_object.coord_x = random.randrange(0, constants.MAX_WIDTH - 25)
    game_object.b_image = constants.GAME_OBJECTS[ran_index][0]
    game_object.color = constants.GAME_OBJECTS[ran_index][2]
    game_object.type = constants.GAME_OBJECTS[ran_index][1]
    game_object.coord_y = random.randint(-(constants.MAX_HEIGHT * 2), -350)
    game_object.coord_x = random.randrange(0, constants.MAX_WIDTH - 25)

    return game_object


def check_detection(game_object, player_platform):
    return abs(game_object.coord_y - player_platform.coord_y) < 40 and abs(
        player_platform.coord_x - game_object.coord_x) < 40


def text_objects(text, font):
    text_surface = font.render(text, True, constants.RED)
    return text_surface, text_surface.get_rect()


def handle_movement_player(keys_pressed, player_platform):
    if keys_pressed[pygame.K_a] and player_platform.coord_x >= 0:
        player_platform.coord_x -= constants.VEL + 5
    if keys_pressed[pygame.K_d] and player_platform.coord_x <= constants.MAX_WIDTH - constants.WIDTH:
        player_platform.coord_x += constants.VEL + 5


def movement_rhombus(rhombus_object, current_movement):
    #global current_movement
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


def reset_timer(time_stamp, time_delta, player_platform):
    #global time_stamp, time_delta
    pygame.mixer.Sound(constants.START_SOUND).play()
    time_stamp = round(time.time() * 1000)
    time_delta = round(random.randint(4000, 25000))
    ran_index = random.randint(0, len(constants.IMAGES) - 1)
    player_platform.b_image = constants.IMAGES[ran_index][0]
    player_platform.color = constants.IMAGES[ran_index][2]

    return  time_stamp, time_delta, player_platform

def create_enemies():
    enemies = []
    for _ in range(0, 40):
        ran_index = random.randint(0, len(constants.GAME_OBJECTS) - 1)
        enemies.append(
            GameObject(constants.GAME_OBJECTS[ran_index][0], 5, random.randrange(0, constants.MAX_WIDTH - 20),
                       random.randint(-1000, 0), random.randint(0, 50), random.randint(0, 70),
                       constants.GAME_OBJECTS[ran_index][1],
                       constants.GAME_OBJECTS[ran_index][2]))

    return enemies

def db_operations(collection, player_name, score_count):
    # player_name is not yet registered in the db, insert it
    if len(list(collection.find({'name': player_name}))) == 0:
        collection.insert_one({'name': player_name, 'score': score_count})
    # Only update the player-score if the new score is higher than the previous one
    elif collection.find_one({'name': player_name})['score'] < score_count:
        collection.update_one({'name': player_name}, {'$set': {'score': score_count}})


def is_high_score(collection, player_name, score_count):
    try:
        return collection.find_one({'name': player_name})['score'] < score_count
    except TypeError:
        return True
