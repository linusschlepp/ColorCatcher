import random
import time

import button
import utils
from color import Color
from type import Type
from operator import itemgetter
import constants
from pymongo import MongoClient
from config import MONGODB_URL
from game_object import GameObject
import dns.resolver

# dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
# dns.resolver.default_resolver.nameservers = ['8.8.8.8']
import pygame
from input_box import InputBox

db_cluster = MongoClient(MONGODB_URL)
# Name of cluster
db = db_cluster['test']
# Name of collection
collection = db['Cluster0']

pygame.init()

WIN = pygame.display.set_mode((constants.MAX_WIDTH, constants.MAX_HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption('ColorCatcher')

current_movement = False

ran_index = random.randint(0, len(constants.IMAGES) - 1)
player_platform = GameObject(constants.IMAGES[ran_index][0], 4, random.randrange(0, constants.MAX_WIDTH - 20),
                             random.randrange(-2000, -1000), 55, 100, constants.IMAGES[ran_index][1],
                             constants.IMAGES[ran_index][2])

time_stamp = round(time.time() * 1000)
time_delta = round(random.randint(4000, 25000))


def enter_player_name():
    global player_name
    menu = True
    input_box = InputBox(250, 260, 140, 32)
    show_error_text = False

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            player_name = input_box.handle_event(event)

        input_box.update()

        WIN.fill(constants.WHITE)
        input_box.draw(WIN)

        WIN.blit(pygame.image.load(constants.IMAGE_ENTER_NAME), (constants.MAX_WIDTH / 5, constants.MAX_HEIGHT / 5))
        start_button = button.Button(280, 300, constants.IMAGE_START_ACTIVE, constants.IMAGE_START_INACTIVE, WIN)
        check_score_button = button.Button(280, 400, constants.IMAGE_DASHBOARD_ACTIVE,
                                           constants.IMAGE_DASHBOARD_INACTIVE, WIN)
        if start_button.check:
            if len(player_name) < 4:
                show_error_text = True
            else:
                start_game()
        if check_score_button.check:
            list_score()
        if show_error_text:
            WIN.blit(
                pygame.font.SysFont('Consolas', 15).render('Your name needs to have at least 4 characters', True,
                                                           constants.RED), (200, 490))

        pygame.display.update()
        CLOCK.tick(15)


def list_score():
    users = collection.find({})
    menu = True
    #users = sorted(users, key=itemgetter('score'), reverse=True)

    font = pygame.font.SysFont('Consolas', 10)

    while menu:
        start_y = 150
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        WIN.fill(constants.WHITE)

        go_back_button = button.Button(0, 0, constants.IMAGE_GO_BACK_ACTIVE, constants.IMAGE_GO_BACK_INACTIVE, WIN)
        for index, user in enumerate(users):
            WIN.blit(font.render('{}. {} {}'.format(str(index + 1), user['name'], str(user['score'])), True,
                                 constants.BLACK),
                     (constants.MAX_WIDTH / 2, start_y))
            start_y += 20

        if go_back_button.check:
            enter_player_name()

        pygame.display.update()
        CLOCK.tick(15)


def update_lives() -> None:
    """
    Updates life_score of player on screen, loads individual image
    """
    if live_count == 3:
        WIN.blit(pygame.image.load(constants.IMAGE_THREE_HEART), (constants.MAX_WIDTH - 150, 0))
    elif live_count > 3:
        WIN.blit(pygame.image.load(constants.IMAGE_MORE_HEART), (constants.MAX_WIDTH - 150, 0))
    elif live_count == 2:
        WIN.blit(pygame.image.load(constants.IMAGE_TWO_HEART), (constants.MAX_WIDTH - 150, 0))
    elif live_count == 1:
        WIN.blit(pygame.image.load(constants.IMAGE_ONE_HEART), (constants.MAX_WIDTH - 150, 0))
    elif live_count < 1:
        restart_game()


def restart_game():
    #TODO: Uncomment this stuff
    font = pygame.font.SysFont('Consolas', 25)
    # text_score = font.render('Score: {}'.format(str(score_count)), True,
    #                          constants.BLACK) if not utils.is_high_score(collection, player_name, score_count) else font.render(
    #     'Congrats, NEW HIGHSCORE: {}'.format(score_count), True, constants.RED)
   # utils.db_operations(collection, player_name, score_count)

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        WIN.fill(constants.WHITE)
      #  pygame.display.flip()
        died_image = pygame.image.load(constants.IMAGE_YOU_DIED)
        WIN.blit(died_image, died_image.get_rect(center=(constants.MAX_WIDTH / 2, 160)))
        retry_button = button.Button(280, 240, constants.IMAGE_ACTIVE, constants.IMAGE_INACTIVE, WIN)
        main_menu_button = button.Button(280, 320, constants.IMAGE_DASHBOARD_ACTIVE,
                                         constants.IMAGE_DASHBOARD_INACTIVE, WIN)
       # WIN.blit(text_score, text_score.get_rect(center=(constants.MAX_WIDTH / 2, 210)))
        if retry_button.check:
            start_game()
        if main_menu_button.check:
            enter_player_name()
        pygame.display.update()
        CLOCK.tick(15)


def evaluate_object(game_object: GameObject) -> None:
    """
    Evaluates different game object. Determines if it's good are bad
    :param game_object: Object, which collides with player
    """
    global live_count, score_count
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


def start_game():
    global score_count, live_count, current_movement, time_stamp, time_delta, player_platform
    enemies = utils.create_enemies()
    live_count = 3
    score_count = 0

    run = True

    while run:
        WIN.fill(constants.WHITE)
        CLOCK.tick(constants.FPS)
        for enemy in enemies:
            WIN.blit(enemy.b_image, (enemy.coord_x, enemy.coord_y))
        WIN.blit(player_platform.b_image, (player_platform.coord_x, player_platform.coord_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        utils.handle_movement_player(keys_pressed, player_platform)
        player_platform.coord_y = constants.MAX_HEIGHT - 50

        for enemy in enemies:
            if enemy.type == Type.RHOMBUS:
                enemy, current_movement = utils.movement_rhombus(enemy, current_movement)

            enemy.coord_y += enemy.speed + 0.005 * score_count

            if enemy.coord_y > constants.MAX_HEIGHT - 10:
                enemy = utils.reassign_object(enemy)
            if utils.check_detection(enemy, player_platform):
                evaluate_object(enemy)
                utils.reassign_object(enemy)

        if utils.time_run_out(time_delta, time_stamp):
            time_stamp, time_delta, player_platform = \
                utils.reset_timer(time_stamp, time_delta, player_platform)

        utils.update_score(WIN, score_count)
        update_lives()
        pygame.display.update()


enter_player_name()
