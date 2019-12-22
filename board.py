from random import randint
from gameobjects import *


class Board:
    max_random_tries = 5

    def __init__(self, board_width, board_height, canvas_width, canvas_height, snake, max_nr_food, nr_walls,
                 test_config):
        self.snake = snake
        self.width = board_width
        self.height = board_height
        self.board = [[GameObject.EMPTY for x in range(board_width)] for y in range(board_height)]
        self.block_width = canvas_width / board_width
        self.block_height = canvas_height / board_height
        self.max_nr_food = max_nr_food
        self.wall_pos_not_allowed = [(0, 1), (1, 0), (self.width - 2, 0), (self.width - 1, 1), (self.width - 1, self.height - 2),
                           (self.width - 2, self.height - 1), (0, self.height - 2), (1, self.height - 1)]
        if not test_config:
            for i in range(nr_walls):
                self.spawn_wall()
        else:
            self.set_game_object_at(7, 5, GameObject.WALL)
            self.set_game_object_at(15, 8, GameObject.WALL)

        for i in range(max_nr_food):
            self.spawn_new_food()

    def get_game_object_at(self, x, y):
        if self.board[x][y] is None:
            return GameObject.EMPTY
        if self.snake.contains_head(x, y):
            return GameObject.SNAKE_HEAD
        if self.snake.contains_body(x, y):
            return GameObject.SNAKE_BODY
        return self.board[x][y]

    def is_wall_at(self, x, y):
        return self.board[x][y] == GameObject.WALL

    def set_game_object_at(self, x, y, game_object):
        self.board[x][y] = game_object

    def draw(self, canvas):
        for x in range(0, self.width):
            for y in range(0, self.height):
                draw_x = x * self.block_width
                draw_y = y * self.block_height
                canvas.create_rectangle(draw_x, draw_y, draw_x + self.block_width, draw_y + self.block_height,
                                        fill=self.get_game_object_at(x, y).getColor(), outline="")

    def eat_food(self, x, y):
        self.board[x][y] = GameObject.EMPTY
        self.spawn_new_food()

    def get_copy(self):
        copy = [[GameObject.EMPTY for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                copy[x][y] = self.get_game_object_at(x, y)
        return copy

    def get_copy_without_snake(self):
        copy = [[GameObject.EMPTY for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                if not self.board[x][y] is None:
                    copy[x][y] = self.board[x][y]
        return copy

    def spawn_new_food(self):
        # self.set_game_object_at(0,0, GameObject.FOOD)
        self.spawn_random_object(GameObject.FOOD)

    def spawn_wall(self):
        # self.spawn_random_object(GameObject.WALL)
        new_x, new_y = self.get_free_xy()
        while (new_x, new_y) in self.wall_pos_not_allowed:
            new_x, new_y = self.get_free_xy()
        self.set_game_object_at(new_x, new_y, GameObject.WALL)

    def spawn_random_object(self, gameObjectType):
        new_x, new_y = self.get_free_xy()
        self.set_game_object_at(new_x, new_y, gameObjectType)

    def get_free_xy(self):
        new_x = randint(0, self.width - 1)
        new_y = randint(0, self.height - 1)
        count = 0
        # try to find a random position
        while not (self.get_game_object_at(new_x, new_y) == GameObject.EMPTY) and count < self.max_random_tries:
            count += 1
            new_x = randint(0, self.width - 1)
            new_y = randint(0, self.height - 1)

        # if no random position could be guessed, try a more decent approach
        if not self.get_game_object_at(new_x, new_y) == GameObject.EMPTY:
            available = []
            for x in range(self.width):
                for y in range(self.height):
                    if self.get_game_object_at(x, y) == GameObject.EMPTY:
                        available.append((x, y))

            if len(available) == 0:
                raise RuntimeError("Congratulations, you broke the game by filling each cell of the board!")
            else:
                new_x, new_y = available[randint(0, len(available) - 1)]

        return new_x, new_y
