import random
import time


import button
import db_operations
import game_utils
from item_type import Type
import game_constants
from game_object import GameObject
import pygame
from input_box import InputBox

pygame.init()

WIN = pygame.display.set_mode((game_constants.MAX_WIDTH, game_constants.MAX_HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption('ColorCatcher')

current_movement = False

ran_index = random.randint(0, len(game_constants.COLORS) - 1)
ran_color = game_constants.COLORS[ran_index][0]
player_platform = GameObject(game_utils.color_image_game_object(game_constants.PLAYER_PLATFORM[0], ran_color, Type.PLAYER), 4, random.randrange(0, game_constants.MAX_WIDTH - 20),
                             random.randrange(-2000, -1000), 55, 100, game_constants.PLAYER_PLATFORM[1],
                             ran_color)

time_stamp = round(time.time() * 1000)
time_delta = round(random.randint(4000, 25000))

# Sets up database if not already initialized
db_operations.set_up_db()


def enter_player_name() -> None:
    """
    Enables the player to enter his/her name
    """
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

        WIN.fill(game_constants.WHITE)
        input_box.draw(WIN)

        WIN.blit(pygame.image.load(game_constants.ENTER_NAME_IMAGE_PATH), (game_constants.MAX_WIDTH / 5, game_constants.MAX_HEIGHT / 5))
        start_button = button.Button(280, 300, game_constants.IMAGE_START_ACTIVE, game_constants.IMAGE_START_INACTIVE, WIN)
        check_score_button = button.Button(280, 400, game_constants.IMAGE_DASHBOARD_ACTIVE,
                                           game_constants.IMAGE_DASHBOARD_INACTIVE, WIN)
        if start_button.check:
            if len(player_name) < 4:
                show_error_text = True
            else:
                db_operations.add_new_player(player_name)
                start_game()
        if check_score_button.check:
            list_score()
        if show_error_text:
            WIN.blit(
                pygame.font.SysFont('Consolas', 15).render('Your name needs to have at least 4 characters', True,
                                                           game_constants.RED), (200, 490))

        pygame.display.update()
        CLOCK.tick(15)


def list_score() -> None:
    """
    Lists the scores of the players on the screen
    """
    menu = True
    players = db_operations.fetch_data()
    players.sort(key=lambda p: p[1], reverse=True)

    font = pygame.font.SysFont('Consolas', 10)

    while menu:
        start_y = 150
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        WIN.fill(game_constants.WHITE)

        go_back_button = button.Button(0, 0, game_constants.IMAGE_GO_BACK_ACTIVE, game_constants.IMAGE_GO_BACK_INACTIVE, WIN)
        for index, player in enumerate(players):
            WIN.blit(font.render('{}. {} {}'.format(str(index + 1), player[0], str(player[1])), True,
                                 game_constants.BLACK),
                     (game_constants.MAX_WIDTH / 2, start_y))
            start_y += 20

        if go_back_button.check:
            enter_player_name()

        pygame.display.update()
        CLOCK.tick(15)


def update_lives() -> None:
    """
    Updates life_score of player on and loads corresponding image
    """
    if live_count == 3:
        WIN.blit(pygame.image.load(game_constants.THREE_HEART_IMAGE_PATH), (game_constants.MAX_WIDTH - 150, 0))
    elif live_count > 3:
        WIN.blit(pygame.image.load(game_constants.MORE_HEART_IMAGE_PATH), (game_constants.MAX_WIDTH - 150, 0))
    elif live_count == 2:
        WIN.blit(pygame.image.load(game_constants.TWO_HEART_IMAGE_PATH), (game_constants.MAX_WIDTH - 150, 0))
    elif live_count == 1:
        WIN.blit(pygame.image.load(game_constants.ONE_HEART_IMAGE_PATH), (game_constants.MAX_WIDTH - 150, 0))
    elif live_count < 1:
        restart_game()


def restart_game():
    font = pygame.font.SysFont('Consolas', 25)
    text_score = font.render('Score: {}'.format(str(score_count)), True,
                             game_constants.BLACK) if db_operations.is_high_score(player_name, score_count) == '' \
        else font.render(db_operations.is_high_score(player_name, score_count), True, game_constants.RED)
    db_operations.check_scores(player_name, score_count)

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        WIN.fill(game_constants.WHITE)
        died_image = pygame.image.load(game_constants.YOU_DIED_IMAGE_PATH)
        WIN.blit(died_image, died_image.get_rect(center=(game_constants.MAX_WIDTH / 2, 160)))
        retry_button = button.Button(280, 240, game_constants.IMAGE_ACTIVE, game_constants.IMAGE_INACTIVE, WIN)
        main_menu_button = button.Button(280, 320, game_constants.IMAGE_DASHBOARD_ACTIVE,
                                         game_constants.IMAGE_DASHBOARD_INACTIVE, WIN)
        WIN.blit(text_score, text_score.get_rect(center=(game_constants.MAX_WIDTH / 2, 210)))
        if retry_button.check:
            start_game()
        if main_menu_button.check:
            enter_player_name()
        pygame.display.update()
        CLOCK.tick(15)


def start_game() -> None:
    """
    Starts the actual game
    """
    global score_count, live_count, current_movement, time_stamp, time_delta, player_platform
    enemies = game_utils.create_game_objects()
    live_count = 3
    score_count = 0

    run = True

    while run:
        WIN.fill(game_constants.WHITE)
        CLOCK.tick(game_constants.FPS)
        for enemy in enemies:
            WIN.blit(game_utils.convert_image(enemy.b_image), (enemy.coord_x, enemy.coord_y))
        WIN.blit(game_utils.convert_image(player_platform.b_image),
                 (player_platform.coord_x, player_platform.coord_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        game_utils.handle_movement_player(keys_pressed, player_platform)
        player_platform.coord_y = game_constants.MAX_HEIGHT - 50

        for enemy in enemies:
            if enemy.type == Type.RHOMBUS:
                enemy, current_movement = game_utils.movement_rhombus(enemy, current_movement)

            enemy.coord_y += enemy.speed + 0.005 * score_count

            # enemy is out of scope and gets reassigned
            if enemy.coord_y > game_constants.MAX_HEIGHT - 10:
                enemy = game_utils.reassign_object(enemy)
            # enemy is caught by player and gets reassigned
            if game_utils.check_detection(enemy, player_platform):
                live_count, score_count = game_utils.evaluate_object(enemy, player_platform, live_count, score_count)
                game_utils.reassign_object(enemy)
        # check if time has run out, if so assign different color to player
        if game_utils.time_run_out(time_delta, time_stamp):
            time_stamp, time_delta, player_platform = \
                game_utils.reset_timer(player_platform)

        game_utils.update_score(WIN, score_count)
        update_lives()
        pygame.display.update()


enter_player_name()
