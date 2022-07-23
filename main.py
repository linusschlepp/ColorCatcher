import math
import random
import time
from enum import Enum

import pygame


class GameObject():
    def __init__(self, b_image, speed, coord_x, coord_y, hitbox_x, hitbox_y, type, color):
        self.b_image = b_image
        self.speed = speed
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y
        self.type = type
        self.color = color


class Color(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3


class Type(Enum):
    STAR = 1
    RHOMBUS = 2
    SQUARE = 3
    PLAYER = 4
    HEART = 5
    MINUS_HEART = 6
    PLUS_TEN_POINTS = 7
    MINUS_TEN_POINTS = 8
    TEN_POINTS = 9


pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WIDTH = 55
HEIGHT = 40
MAX_HEIGHT = 750
MAX_WIDTH = 750

WIN = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

pygame.display.set_caption("ColorCatcher")

STAR = pygame.image.load('assets/star.png')
# STAR = pygame.transform.scale(STAR, (WIDTH, HEIGHT))

RHOMBUS = pygame.image.load('assets/rhombus.png')
# RHOMBUS = pygame.transform.scale(RHOMBUS, (WIDTH, HEIGHT))

SQUARE = pygame.image.load('assets/square.png')
# SQUARE = pygame.transform.scale(SQUARE, (WIDTH, HEIGHT))

PLAYER_PLATFORM = pygame.image.load('assets/player_platform.png')
# PLAYER_PLATFORM = pygame.transform.scale(SQUARE, (WIDTH, HEIGHT))

FPS = 60
VEL = 5

current_movement = False

live_count = 3

objects_1 = [(pygame.image.load('assets/red_star.png'), Type.STAR, Color.RED),
             (pygame.image.load('assets/yellow_star.png'), Type.STAR, Color.YELLOW),
             (pygame.image.load('assets/green_star.png'), Type.STAR, Color.GREEN),
             (pygame.image.load('assets/red_rhombus.png'), Type.RHOMBUS, Color.RED),
             (pygame.image.load('assets/green_rhombus.png'), Type.RHOMBUS, Color.GREEN),
             (pygame.image.load('assets/yellow_rhombus.png'), Type.RHOMBUS, Color.YELLOW),
             (pygame.image.load('assets/red_square.png'), Type.SQUARE, Color.RED),
             (pygame.image.load('assets/green_square.png'), Type.SQUARE, Color.GREEN),
             (pygame.image.load('assets/yellow_square.png'), Type.SQUARE, Color.YELLOW),
             (pygame.image.load('assets/one_heart.png'), Type.HEART, Color.RED),
             (pygame.image.load('assets/ten_points.png'), Type.TEN_POINTS, Color.RED),
             (pygame.image.load('assets/minus_ten_points.png'), Type.MINUS_TEN_POINTS, Color.RED),
             (pygame.image.load('assets/minus_heart.png'), Type.MINUS_HEART, Color.RED)]

images = [(pygame.image.load('assets/player_platform_yellow.png'), Type.PLAYER, Color.YELLOW),
          (pygame.image.load('assets/player_platform_red.png'), Type.PLAYER, Color.RED),
          (pygame.image.load('assets/player_platform_green.png'), Type.PLAYER, Color.GREEN)]

ran_index = random.randint(0, len(images) - 1)
player_platform = GameObject(images[ran_index][0], 4, random.randrange(0, MAX_WIDTH - 20),
                             random.randrange(-2000, -1000), 55, 100, images[ran_index][1], images[ran_index][2])

score_count = 0

time_stamp = round(time.time() * 1000)
time_delta = round(random.randint(4000, 25000))


def update_window(rect, rect_1, rect_3, rect_4, player_platform):
    WIN.fill(WHITE)
    WIN.blit(PLAYER_PLATFORM, (player_platform.x, player_platform.y))
    WIN.blit(STAR, (rect.x, rect.y))
    WIN.blit(SQUARE, (rect_1.x, rect_1.y))
    WIN.blit(RHOMBUS, (rect_3.x, rect_3.y))
    WIN.blit(SQUARE, (rect_4.x, rect_4.y))
    pygame.display.update()


def handle_movement_player(keys_pressed, player_platform):
    if keys_pressed[pygame.K_a]:
        if player_platform.coord_x >= 0:
            player_platform.coord_x -= VEL + 5
    if keys_pressed[pygame.K_d]:
        if player_platform.coord_x <= MAX_WIDTH - WIDTH:
            player_platform.coord_x += VEL + 5


def update_score():
    font = pygame.font.SysFont('Consolas', 25)
    text = font.render("Score:" + str(score_count), True, BLACK)
    WIN.blit(text, (0, 0))


def text_objects(text, font):
    text_surface = font.render(text, True, RED)
    return text_surface, text_surface.get_rect()


def update_lives():
    if live_count == 3:
        WIN.blit(pygame.image.load('assets/three_hearts.png'), (MAX_WIDTH - 150, 0))
    elif live_count > 3:
        WIN.blit(pygame.image.load('assets/more_hearts.png'), (MAX_WIDTH - 150, 0))
    elif live_count == 2:
        WIN.blit(pygame.image.load('assets/two_hearts.png'), (MAX_WIDTH - 150, 0))
    elif live_count == 1:
        WIN.blit(pygame.image.load('assets/one_heart.png'), (MAX_WIDTH - 150, 0))
    elif live_count < 1:
        large_text = pygame.font.Font("freesansbold.ttf", 46)
        text_surf, text_rect = text_objects('U dead', large_text)
        text_rect.center = ((MAX_WIDTH / 2), (MAX_HEIGHT / 2))
        WIN.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(2)
        # game_loop()
        pygame.quit()


def evaluate_object(object):
    global live_count, score_count
    if object.type == Type.MINUS_HEART:
        pygame.mixer.Sound('assets/wrong-buzzer-6268.wav').play()
        live_count = live_count - 1
    elif object.type == Type.HEART:
        pygame.mixer.Sound('assets/good-6081.wav').play()
        live_count = live_count + 1
    elif object.type == Type.MINUS_TEN_POINTS:
        pygame.mixer.Sound('assets/wrong-buzzer-6268.wav').play()
        if score_count <= 10:
            score_count = 0
        else:
            score_count = score_count - 10
    elif object.type == Type.TEN_POINTS:
        pygame.mixer.Sound('assets/good-6081.wav').play()
        score_count = score_count + 10
    elif player_platform.color == object.color:
        pygame.mixer.Sound('assets/correct-choice-43861.wav').play()
        score_count = score_count + 1
        print(score_count)
    else:
        pygame.mixer.Sound('assets/wrong-buzzer-6268.wav').play()
        live_count = live_count - 1


def check_detection(object):
    return abs(object.coord_y - player_platform.coord_y) < 40 and abs(
        player_platform.coord_x - object.coord_x) < 40


def reset_timer():
    global time_stamp, time_delta
    pygame.mixer.Sound('assets/start-13691.wav').play()
    time_stamp = round(time.time() * 1000)
    time_delta = round(random.randint(4000, 25000))
    ran_index = random.randint(0, len(images) - 1)
    player_platform.b_image = images[ran_index][0]
    player_platform.color = images[ran_index][2]

def time_run_out():
    return round(time.time() * 1000) - time_delta > time_stamp


def main():
    global score_count, live_count
    objects = []

    for number in range(0, 40):
        ran_index = random.randint(0, len(objects_1) - 1)
        objects.append(
            GameObject(objects_1[ran_index][0], 5, random.randrange(0, MAX_WIDTH - 20),
                       random.randint(-1000, 0), random.randint(0, 50), random.randint(0, 70), objects_1[ran_index][1],
                       objects_1[ran_index][2]))
    clock = pygame.time.Clock()
    run = True

    while run:

        WIN.fill(WHITE)
        clock.tick(FPS)
        for object in objects:
            WIN.blit(object.b_image, (object.coord_x, object.coord_y))
        WIN.blit(player_platform.b_image, (player_platform.coord_x, player_platform.coord_y))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        handle_movement_player(keys_pressed, player_platform)

        player_platform.coord_y = MAX_HEIGHT - 50

        for object in objects:
            if object.type == Type.RHOMBUS:
                object = movement_rhombus(object)

            object.coord_y += object.speed + 0.005 * score_count

            if object.coord_y > MAX_HEIGHT - 10:
                object = reassign_object(object)
            if check_detection(object):
                evaluate_object(object)
                print(object.type, object.color)
                object = reassign_object(object)
                print(object.type, object.color)

        if time_run_out():
            reset_timer()

        update_score()
        update_lives()
        pygame.display.update()


def reassign_object(object):
    ran_index = random.randint(0, len(objects_1) - 1)
    object.coord_y = random.randint(-1500, -350)
    object.coord_x = random.randrange(0, MAX_WIDTH - 25)
    object.b_image = objects_1[ran_index][0]
    object.color = objects_1[ran_index][2]
    object.type = objects_1[ran_index][1]
    object.coord_y = random.randint(-(MAX_HEIGHT * 2), -350)
    object.coord_x = random.randrange(0, MAX_WIDTH - 25)

    return object


def movement_rhombus(object):
    global current_movement
    if object.coord_x > MAX_WIDTH:
        object.coord_x = MAX_WIDTH
        current_movement = False
    if object.coord_x < 0:
        object.coord_x = 0
        current_movement = True

    if not current_movement:
        object.coord_x -= object.speed + 1.2 * 2
    else:
        object.coord_x += object.speed + 1.2 * 2

    return object


if __name__ == "__main__":
    main()
