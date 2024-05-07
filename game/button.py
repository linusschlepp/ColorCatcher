import pygame
import game_utils


class Button:
    """
    Button-class
    """
    def __init__(self, x, y, picture_active, picture_inactive, width, height, WIN):

        if type(picture_active) is not pygame.Surface:
            picture_active = game_utils.resize_img(picture_active, width, height)
            picture_active = game_utils.convert_image(picture_active)
        mouse_pos = pygame.mouse.get_pos()
        self.check = False
        click = pygame.mouse.get_pressed()

        if x + picture_inactive.get_width() > mouse_pos[0] > x and y + picture_inactive.get_height() > mouse_pos[1] > y:
            WIN.blit(picture_active, (x, y))
            if click[0]:
                self.check = True
        else:
            WIN.blit(picture_inactive, (x, y))