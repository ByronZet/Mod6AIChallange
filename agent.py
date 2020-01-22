from collections import defaultdict

import numpy as np
import math
from gameobjects import GameObject
from move import Move, Direction


class Node:
    def __init__(self, position):
        self.parent = None
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0


class Agent:

    def __init__(self):
        self.cost = 1
        self.start = None
        self.end = None
        self.path = []
        self.node_list = []
        self.score = 0
        """" Constructor of the Agent, can be used to set up variables """

    """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
            the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
            functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
            that much that it will explode). The starting direction of the snake will be North.

            :param board: A two dimensional array representing the current state of the board. The upper left most
            coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
            coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
            given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
            there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
            of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
            TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
            the boundaries of the array)

            :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
            When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
            words, the score describes the score of the current (alive) worm.

            :param turns_alive: The number of turns (as integer) the current snake is alive.

            :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
            reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
            is not enabled and the snake can not starve.

            :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
            Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
            straight is returned, the snake wil move one cell to the right.

            :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
            0]][head_position[1]] == GameObject.SNAKE_HEAD.

            :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
            represents the tail and the first element represents the body part directly following the head of the snake.

            :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
            going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
            snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
            Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
            move left is made, the snake will go one block to the left and change its direction to west.
            """

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
        # print(head_position)
        if self.score < score:
            print("New score: ", score)
            self.score = score
        northcoord = {(-1, 0): Move.STRAIGHT, (0, 1): Move.RIGHT, (0, -1): Move.LEFT}
        southcoord = {(1, 0): Move.STRAIGHT, (0, -1): Move.RIGHT, (0, 1): Move.LEFT}
        eastcoord = {(0, 1): Move.STRAIGHT, (1, 0): Move.RIGHT, (-1, 0): Move.LEFT}
        westcoord = {(0, -1): Move.STRAIGHT, (-1, 0): Move.RIGHT, (1, 0): Move.LEFT}
        dic_of_dics = {Direction.NORTH: northcoord, Direction.SOUTH: southcoord, Direction.WEST: westcoord, Direction.EAST: eastcoord}
        self.find_start_end_points(board)
        self.path = self.A_search(self.start, self.end, board)
        if not self.path:
            self.path = self.best_first(self.start, board)
        if not self.path:
            return Move.STRAIGHT


        next = self.path[0]
        # print("path initial", self.path)
        if board[next[0]][next[1]] != GameObject.EMPTY and board[next[0]][next[1]] != GameObject.FOOD:
            # print("Asta is eu si ma feresc")
            self.find_start_end_points(board)
            self.path = self.A_search(self.start, self.end, board)
            if not self.path:
                self.path = self.best_first(self.start, board)
            if not self.path:
                return Move.STRAIGHT
            next = self.path[0]
            # print("Ni path nou ", self.path)
        self.path.pop(0)
        # print("Obiectu care merg: ", board[next[0]][next[1]])
        futx = next[1]
        futy = next[0]
        curx = head_position[1]
        cury = head_position[0]
        # print("Sunt in mama lui cristi la directia ", direction, "si ma duc sa-mi bag pula in ea prin ", futy, " ",futx, "iar eu sun la", cury, " ", curx)
        # print("Astea mi-s coordonatele: ", futx - curx, futy - cury)
        dir_dic = dic_of_dics[direction]
        move_coord = (futx - curx, futy - cury)
        try:
            move = dir_dic[(futx - curx, futy - cury)]
        except KeyError:
            print("Caught KeyError, returning Move.STRAIGHT")
            return Move.STRAIGHT
        # print(move)
        return move



    def A_search(self, start, end, board):
        open_set = []
        start_node = Node(start)
        end_node = Node(end)
        open_set.append(start_node)
        cameFrom = dict()
        f_score = defaultdict(lambda : np.inf)
        g_score = defaultdict(lambda : np.inf)
        g_score[start_node] = 0
        f_score[start_node] = self.manhattan(start, end)
        iterations = 0
        max_iterations = 5000
        while len(open_set) > 0:
            iterations += 1
            # print(iterations)
            current_node = None
            min = np.inf

            for x in open_set:
                if f_score[x] < min:
                    current_node = x
                    min = f_score[x]

            if current_node.position == end_node.position or current_node.position==GameObject.FOOD:
                # print("found path")
                return self.reconstruct_path(cameFrom, current_node)

            if iterations > max_iterations:
                print("too many iterations, giving up")
                # return self.reconstruct_path(cameFrom, current_node)
                return self.best_first(self.start, board)
            open_set.remove(current_node)
            # print(len(open_set))
            neighbours = self.find_neighbours(current_node, board) # list of coordinates , eg (2,2)
            # print(neighbours)
            for x in neighbours:
                add = True
                test_gScore = g_score[current_node] + self.cost
                if test_gScore < g_score[x]:
                    cameFrom[x] = current_node
                    g_score[x] = test_gScore
                    f_score[x] = g_score[x] + self.manhattan(x.position, end_node.position)
                    for set_node in open_set:
                        if set_node.position == x.position:
                            add = False
                    # if x not in open_set:
                    #     open_set.append(x)
                    if add:
                        open_set.append(x)
        print("did not find path")
        return None

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from.keys():
            path.append(current.position)
            current = came_from[current]
        result = path[::-1]
        return result

    def find_start_end_points(self, board):
        cost = np.inf
        for i in range(np.shape(board)[1]):
            for j in range(np.shape(board)[0]):
                if board[i][j] == GameObject.SNAKE_HEAD:
                    self.start = (i, j)
                    break

        for i in range(np.shape(board)[1]):
            for j in range(np.shape(board)[0]):
                if board[i][j] == GameObject.FOOD:
                    this_cost = self.manhattan(self.start, (i, j))
                    if this_cost < cost:
                        cost = this_cost
                        self.end = (i, j)

    def find_neighbours(self, node, board):
        result = []
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]] # [1, 1], [-1, -1], [1, -1], [-1, 1]
        for k in directions:
            x = node.position[0] + k[0]
            y = node.position[1] + k[1]
            if (0 <= x < 25 and 0 <= y < 25) and (board[x][y] == GameObject.FOOD or board[x][y] == GameObject.EMPTY):
                result.append(Node((x, y)))
        return result

    def manhattan(self, start, end):
        return np.abs(start[0] - end[0]) + np.abs(start[1] - end[1])

    def euclidian(self, start, end):
        return math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)

    def best_first(self, start, board):
        start_node = Node(start)
        neighbours = self.find_neighbours(start_node, board)
        shortest_distance = np.inf
        path = []
        next_coord = None
        for node in neighbours:
            node_distance = self.manhattan(node.position, self.end)
            if node_distance < shortest_distance:
                shortest_distance = node_distance
                next_coord = node.position
        if next_coord:
            path.append(next_coord)

        # print("fac best first si merg la: ", path)
        return path

    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return True

    def on_die(self, head_position, board, score, body_parts):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """
