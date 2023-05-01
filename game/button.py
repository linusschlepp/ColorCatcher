import pygame


class Button:
    def __init__(self, x, y, picture_active, picture_inactive, WIN):

        global player_name
        mouse_pos = pygame.mouse.get_pos()
        self.check = False
        click = pygame.mouse.get_pressed()

        if x + picture_inactive.get_width() > mouse_pos[0] > x and y + picture_inactive.get_height() > mouse_pos[1] > y:
            WIN.blit(picture_active, (x, y))
            if click[0]:
                self.check = True
        else:
            WIN.blit(picture_inactive, (x, y))