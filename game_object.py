class GameObject:
    def __init__(self, b_image, speed, coord_x, coord_y, hit_box_x, hit_box_y, enemy_type, enemy_color):
        self.b_image = b_image
        self.speed = speed
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.hit_box_x = hit_box_x
        self.hit_box_y = hit_box_y
        self.type = enemy_type
        self.color = enemy_color