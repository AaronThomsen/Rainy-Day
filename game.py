import pygame
import objects

FRAMES = 30
WIDTH = 846
HEIGHT = 564
START_DROPS = 15
MAX_DROPS = 40

class Game:
    def __init__(self):
        self.running = True
        self.platform = objects.Platform()
        self.player = objects.Player(WIDTH, self.platform)
        self.drops = [objects.WaterDrop(WIDTH, HEIGHT) for x in range(START_DROPS)]
        self.amount_of_drops = START_DROPS
        self.lives = 5
        self.title_running = True
        self.count = 0
        self.time = 0

    def run(self):
        pygame.init()
        pygame.display.set_caption("Emi's Rainy Day")

        clock = pygame.time.Clock()

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("tahoma", 30, True)
        self.font2 = pygame.font.SysFont("tahoma", 20, True)
        self.images()

        while self.running:
            clock.tick(FRAMES)
            if self.title_running:
                self.handle_events()
                self.start_keys()
                self.start()
                pygame.display.flip()
            else:
                self.handle_events()
                self.handle_keys()
                self.add_water_drops()
                self.draw()

        pygame.quit()

    def draw(self):
        if self.lives > 0:
            self.count += 1
            self.time += 1 / FRAMES

            self.surface.blit(self.BACK, (0,0))
            self.player.draw(self.surface, self.CHAR, self.CHAR2)

            self.platform.draw(self.surface, self.PLATFORM)

            #Draw water drops on surface
            for drop in self.drops:
                self.collide(drop, self.player)
                drop.draw(self.surface, self.DROP)

            self.text = self.font.render("Lives Left: " + str(self.lives), 1, (0, 0, 0))
            self.text2 = self.font2.render("Time Elapsed: " + str(round(self.time, 1)), 1, (0, 0, 0))
            self.surface.blit(self.text, (340, 10))
            self.surface.blit(self.text2, (650, 10))
        else:
            self.game_over()

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player.move_left()

        if keys[pygame.K_RIGHT]:
            self.player.move_right()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.player.is_jumping = True
            self.player.jump()

    def collide(self, one, two):
        if one.y + one.height > two.y + 20 and one.y + one.height < two.y + two.height + 15:
            if two.x < one.x < two.x + two.width or two.x < one.x + one.width < two.x + two.width:
                one.hit()
                self.lives -= 1

    def add_water_drops(self):
        if self.amount_of_drops <= MAX_DROPS and self.count >= FRAMES * 5:
            self.drops.append(objects.WaterDrop(WIDTH, HEIGHT))
            self.drops.append(objects.WaterDrop(WIDTH, HEIGHT))
            self.amount_of_drops += 2
            self.count = 0

    def start(self):
        self.surface.blit(self.start_back, (0, 0))

        font = pygame.font.SysFont("tahoma", 50, True)
        font2 = pygame.font.SysFont("tahoma", 20, True)
        text = font.render("Emi's Rainy Day", 1, (5, 160, 160))
        text2 = font2.render("Press ENTER to begin...", 1, (250, 250, 25))
        self.surface.blit(text, (220, 20))
        self.surface.blit(text2, (290, 300))

    def start_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.title_running = False

    def game_over(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont("tahoma", 50, True)
        text = font.render("GAME OVER", 1, (200, 10, 10))
        self.surface.blit(text, (270, 240))

        font = pygame.font.SysFont("tahoma", 35, True)
        text = font.render("Time: " + str(round(self.time, 1)), 1, (200, 10, 10))
        self.surface.blit(text, (340, 330))

    def images(self):
        self.start_back = pygame.image.load('images/startResize.jpg').convert()
        self.BACK = pygame.image.load('images/utc.jpg').convert()
        self.CHAR = pygame.image.load('images/idleResize.png').convert_alpha()
        self.CHAR2 = pygame.image.load('images/idleResizeflip.png').convert_alpha()
        self.DROP = pygame.image.load('images/dropResize.png').convert_alpha()
        self.WATER = pygame.image.load('images/waterResize.png').convert_alpha()
        self.PLATFORM = pygame.image.load('images/planeResize.png').convert_alpha()

        self.RUNNING_RIGHT = [pygame.image.load('images/run0.png').convert_alpha(),
                            pygame.image.load('images/run1.png').convert_alpha(),
                            pygame.image.load('images/run2.png').convert_alpha(),
                            pygame.image.load('images/run3.png').convert_alpha(),
                            pygame.image.load('images/run4.png').convert_alpha(),
                            pygame.image.load('images/run5.png').convert_alpha(),
                            pygame.image.load('images/run6.png').convert_alpha(),
                            pygame.image.load('images/run7.png').convert_alpha(),
                            pygame.image.load('images/run8.png').convert_alpha(),
                            pygame.image.load('images/run9.png').convert_alpha()]

        self.RUNNING_LEFT = [pygame.image.load('images/run0flip.png').convert_alpha(),
                             pygame.image.load('images/run1flip.png').convert_alpha(),
                             pygame.image.load('images/run2flip.png').convert_alpha(),
                             pygame.image.load('images/run3flip.png').convert_alpha(),
                             pygame.image.load('images/run4flip.png').convert_alpha(),
                             pygame.image.load('images/run5flip.png').convert_alpha(),
                             pygame.image.load('images/run6flip.png').convert_alpha(),
                             pygame.image.load('images/run7flip.png').convert_alpha(),
                             pygame.image.load('images/run8flip.png').convert_alpha(),
                             pygame.image.load('images/run9flip.png').convert_alpha()]

        self.player.rr = self.player.run(self.RUNNING_RIGHT)
        self.player.rl = self.player.run(self.RUNNING_LEFT)


if __name__ == '__main__':
    Game().run()