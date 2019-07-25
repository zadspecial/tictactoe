import os     # to centre the screen
import sys    # to exit the program gracefully

import pygame as pg

from random import randrange

CAPTION = "Snake"
SCREEN_SIZE = (480, 800)

CHARCOAL = (54, 69, 79)
WHITE = (255, 255, 255)

# DIRECT_DICT = {
#     # 'i': (1, 0),  # iniial
#     'u': (0, -1),
#     'd': (0, 1),
#     'l': (-1, 0),
#     'r': (1, 0)
# }


class Snake(object):
    INITIAL_SNAKE_SIZE = (60, 5)

    def __init__(self):
        self.speed = 10
        self.dir = 'r'
        self.body_coords = []
        self.populate_body_coords()
        # self.rect = pg.Rect((0, 0), self.INITIAL_SNAKE_SIZE)
        # self.rect.center = tuple(i//2 for i in SCREEN_SIZE)

    def get_rect(self, coord):
        return pg.Rect(coord, (self.speed, self.speed))

    def populate_body_coords(self):
        x = randrange(3*self.speed, SCREEN_SIZE[0])
        y = randrange(0,SCREEN_SIZE[1])
        for i in range(3):
            self.body_coords.append((x + i * self.speed, y))

    def draw(self, surface):
        for coord in self.body_coords:
            snake_segment = self.get_rect(coord)
            surface.fill(WHITE, snake_segment)

    # def bound_rect(self, surface):
    #     """Prevents the snake from going beyond the screen. Called in update()"""
    #     bounding_rect = surface.get_bounding_rect()
    #     self.rect.clamp_ip(bounding_rect)

    def update_dir(self, keys):
        if keys[pg.K_UP] and self.dir != 'u':
            self.dir = 'u'
        elif keys[pg.K_DOWN] and self.dir != 'd':
            self.dir = 'd'
        elif keys[pg.K_LEFT] and self.dir != 'l':
            self.dir = 'l'
        elif keys[pg.K_RIGHT] and self.dir != 'r':
            self.dir = 'r'

    def update(self, keys):
        # self.bound_rect(surface)
        self.update_dir(keys)

        # code to turn the snake
        # if keys[pg.K_UP]:
        #     if self.dir not in ('u', 'd'):
        #         Control(self, self.speed).turn_up()
        # elif keys[pg.K_DOWN]:
        #     if self.dir not in ('u', 'd'):
        #         Control(self, self.speed).turn_down()
        # elif keys[pg.K_LEFT]:
        #     if self.dir not in ('i', 'l', 'r'):
        #         Control(self, self.speed).turn_left()
        # elif keys[pg.K_RIGHT]:
        #     if self.dir not in ('i', 'l', 'r'):
        #         Control(self, self.speed).turn_right()

        # code to keep it moving

        if self.dir == 'u':
            Control(self).go_up()
        elif self.dir == 'd':
            Control(self).go_down()
        elif self.dir == 'l':
            Control(self).go_left()
        elif self.dir == 'r':
            Control(self).go_right()

        self.body_coords.pop()  # remove the tail

        # for direction in DIRECT_DICT:
        #     if self.dir == direction:
        #         (x, y) = (i * self.speed for i in DIRECT_DICT[direction])
        #         self.rect.move_ip(x, y)


class Control(object):
    def __init__(self, snake):
        self.snake = snake
        self.speed = snake.speed
        self.body_coords = snake.body_coords

    def go_up(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        y -= self.speed
        self.body_coords.insert(0, (x, y))

    def go_down(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        y += self.speed
        self.body_coords.insert(0, (x, y))

    def go_left(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        x -= self.speed
        self.body_coords.insert(0, (x, y))

    def go_right(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        x += self.speed
        self.body_coords.insert(0, (x, y))

    # def turn_up(self):
    #     if self.snake.dir in ('i', 'r'):
    #         self.snake.rect.x += (self.snake.rect.width - self.snake.rect.height)
    #     (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
    #     self.snake.dir = 'u'
    #
    # def turn_down(self):
    #     if self.snake.dir in ('i', 'r'):
    #         self.snake.rect.x -= (self.snake.rect.height - self.snake.rect.width)
    #         self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
    #     elif self.snake.dir == 'l':
    #         self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
    #     (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
    #     self.snake.dir = 'd'
    #
    # def turn_left(self):
    #     if self.snake.dir == 'd':
    #         self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
    #     (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
    #     self.snake.dir = 'l'
    #
    # def turn_right(self):
    #     if self.snake.dir == 'u':
    #         self.snake.rect.x -= (self.snake.rect.height - self.snake.rect.width)
    #
    #     elif self.snake.dir == 'd':
    #         self.snake.rect.x -= (self.snake.rect.height - self.snake.rect.width)
    #         self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
    #     (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
    #     self.snake.dir = 'r'


class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface()  # just gives you the reference code
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.color = CHARCOAL
        self.snake = Snake()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        self.screen.fill(self.color)
        # all drawing goes here
        self.snake.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.snake.update(self.keys)
            self.render()
            self.clock.tick(self.fps)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # centre screen
    pg.init()

    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    App().main_loop()

    pg.quit()
    sys.exit()  # fancy exit


if __name__ == "__main__":
    main()
