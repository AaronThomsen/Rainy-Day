import random

BASE_Y = 500

class Player:
    def __init__(self, sur_width, platform):
        self.x = 50
        self.y = BASE_Y
        self.width = 38
        self.height = 65
        self.speed = 10
        self.sur_width = sur_width
        self.is_jumping = False
        self.jump_counter = 10
        self.is_running_right = False
        self.is_running_left = False
        self.facing_right = True
        self.rr = 0 #generator right
        self.rl = 0 #gnerator left
        self.platform = platform

    def move_left(self):
        self.is_running_left = True
        self.facing_right = False
        if self.x > self.speed:
            self.x -= self.speed

    def move_right(self):
        self.is_running_right = True
        self.facing_right = True
        if self.x < self.sur_width - self.speed - self.width:
            self.x += self.speed

    def jump(self):
        if self.jump_counter >= -10:
            self.y -= (self.jump_counter * abs(self.jump_counter))/3
            self.jump_counter -= 1
        else:
            self.jump_counter = 10
            self.is_jumping = False


    def draw(self, surface, image, image2):
        self.platform_collision()
        if self.is_running_left == False and self.is_running_right == False:
            if self.facing_right:
                surface.blit(image, (self.x, self.y))
            else:
                surface.blit(image2, (self.x, self.y))
        elif self.is_running_right:
            surface.blit(next(self.rr), (self.x, self.y))
            self.is_running_right = False
        else:
            surface.blit(next(self.rl), (self.x, self.y))
            self.is_running_left = False
        if self.is_jumping == True:
            self.jump()

    def run(self, image_list):
        while True:
            for i in image_list:
                yield i

    def platform_collision(self):
        if self.platform.x - 15 < self.x < self.platform.x + self.platform.width - 15:
            if self.platform.on_platform == False and self.jump_counter < -1:
                self.jump_counter = 10
                self.is_jumping = False
                self.y = self.platform.y - 25
                self.platform.on_platform = True
        elif self.is_jumping == False:
            self.platform.on_platform = False
            if self.y < BASE_Y:
                self.y += 30
                if self.y > BASE_Y:
                    self.y = BASE_Y


class WaterDrop():
    def __init__(self, sur_width, sur_height):
        self.x = random.randint(0, sur_width)
        self.y = random.randint(-150, -5)
        self.width = 25
        self.height = 40
        self.speed = random.uniform(3,6)
        self.sur_height = sur_height
        self.sur_width = sur_width

    def move(self):
        if self.y > self.sur_height + self.height:
            self.reset()
        else:
            self.y += self.speed

    def reset(self):
        self.x = random.randint(0, self.sur_width)
        self.y = -5
        self.speed = random.uniform(3.5, 6.5)

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))
        self.move()

    def hit(self):
        self.reset()

class Platform():
    def __init__(self):
        self.x = 300
        self.y = 420
        self.width = 180
        self.height = 55
        self.on_platform = False

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))