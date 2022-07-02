import pygame
from pygame.locals import *
import time
import random
size = 50
BGC = (0, 0, 0)
speed = 0.3


class Game:
    def __init__(self):
        pygame.init()
        self.Surface = pygame.display.set_mode((1000, 750))
        pygame.display.set_caption('Star Eater Snake - The Game')
        pygame.mixer.init()
        self.Play_BGM()
        self.Surface.fill(BGC)
        self.galaxy = Galaxy(self.Surface, 1)
        self.galaxy.draw()
        self.star = Star(self.Surface)
        self.star.draw()

    def play(self):
        self.render_bg()
        self.galaxy.fly()
        self.star.draw()
        self.score()
        pygame.display.flip()

        if self.is_collision(self.galaxy.x[0], self.galaxy.y[0], self.star.x, self.star.y):
            self.play_music("correct")
            self.galaxy.increase_lenght()
            self.star.move()

        if self.galaxy.x[0] < 0 or self.galaxy.x[0] > 950 or self.galaxy.y[0] < 0 or self.galaxy.y[0] > 700:
            self.play_music("error")
            time.sleep(1)
            raise ValueError("Game over")

        for i in range(3, self.galaxy.lenght):
            if self.is_collision(self.galaxy.x[0], self.galaxy.y[0], self.galaxy.x[i], self.galaxy.y[i]):
                self.play_music("error")
                time.sleep(1)
                raise ValueError("Game over")

    def run(self):
        run = True
        Pause = False
        while run:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                    if event.key == K_RETURN:
                        Pause = False
                        pygame.mixer.music.unpause()
                        self.reset()
                    if not Pause:
                        if event.key == K_UP:
                            self.galaxy.move_up()
                        if event.key == K_DOWN:
                            self.galaxy.move_down()
                        if event.key == K_LEFT:
                            self.galaxy.move_left()
                        if event.key == K_RIGHT:
                            self.galaxy.move_right()
                elif event.type == QUIT:
                    run = False
            try:
                if not Pause:
                    self.play()
            except ValueError:
                self.game_over()
                Pause = True

            if self.galaxy.lenght > 15:
                time.sleep(0.1)
            else:
                time.sleep(0.2)

    def game_over(self):
        self.render_bg()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(
            f'Score: {self.galaxy.lenght}', True, (218, 230, 7))
        self.Surface.blit(line1, (200, 100))
        line2 = font.render(
            f'To play again press', True, (255, 255, 255))
        self.Surface.blit(line2, (200, 200))
        line3 = font.render(
            f'Enter.', True, (41, 242, 10))
        self.Surface.blit(line3, (200, 250))
        line4 = font.render(
            f'To exit press', True, (255, 255, 255))
        self.Surface.blit(line4, (200, 350))
        line5 = font.render(
            f'Escape', True, (245, 5, 5))
        self.Surface.blit(line5, (200, 400))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.galaxy = Galaxy(self.Surface, 1)
        self.star = Star(self.Surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f'Score: {self.galaxy.lenght}', True, (255, 255, 255))
        self.Surface.blit(score, (800, 50))

    def Play_BGM(self):
        pygame.mixer.music.load("resources/bg_music.wav")
        pygame.mixer.music.play()

    def play_music(self, sound):
        sound = pygame.mixer.music.load(f"resources/{sound}.wav")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.2)

    def render_bg(self):
        bg = pygame.image.load("resources/bg.jpg").convert()
        self.Surface.blit(bg, (0, 0))


class Galaxy:
    def __init__(self, parent_screen, lenght):
        self.lenght = lenght
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.png").convert()
        self.backstar = pygame.image.load("resources/back_star.png").convert()
        self.x = [size]*lenght
        self.y = [size]*lenght
        self.direction = "right"

    def increase_lenght(self):
        self.lenght += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):

        for i in range(self.lenght):
            self.parent_screen.blit(self.backstar, (self.x[i], self.y[i]))
            self.parent_screen.blit(self.block, (self.x[0], self.y[0]))
        pygame.display.flip()

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def fly(self):

        for i in range(self.lenght - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "left":
            self.x[0] -= size
        if self.direction == "right":
            self.x[0] += size
        if self.direction == "up":
            self.y[0] -= size
        if self.direction == "down":
            self.y[0] += size

        self.draw()


class Star:
    def __init__(self, parent_screen):
        self.food = pygame.image.load("resources/star.png").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(0, 19)*size
        self.y = random.randint(0, 14)*size

    def draw(self):
        self.parent_screen.blit(self.food, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 19)*size
        self.y = random.randint(0, 14)*size


if __name__ == "__main__":
    game = Game()
    game.run()
