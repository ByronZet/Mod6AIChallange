from enum import Enum


class Move(Enum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def get_new_direction(self, move):
        """
        Used to get the new direction given the move. For instance: when facing North and then going right will
        result in facing East.

        :param move: The given move to make. This can be Either Move.LEFT, Move.STRAIGHT or Move.RIGHT.

        :return: The new direction after making this move.
        """
        return Direction((self.value + move.value) % 4)

    def get_xy_manipulation(self):
        """
        Used to get the x, y manipulation of a given directory when facing the given direction and going straight.
        This function can be used to easily calculate the new x and y values in combination with the
        get_new_direction() function.

        Example: Direction is West and you want to know what the new x and y values will be when going right. This
        can be calculated by: "man_x, man_y = direction.get_new_direction(Move.RIGHT).get_xy_manipulation() new_x,
        new_y = x + new_x, y + new_y "

        :return: A tuple with the x and y manipulation when going straight given the direction. The x value is the
        first element and the y value the second element.
        """
        m = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }
        return m[self]

    def get_xy_moves(self):
        """
        Used to retrieve all possible moves given the direction. For instance, when facing North, the available moves
        are going North, going East or going West.

        :return: A list containing all available x y manipulations given the direction.
        """
        m = {
            Direction.NORTH: [Direction.NORTH.get_xy_manipulation(), Direction.EAST.get_xy_manipulation(),
                              Direction.WEST.get_xy_manipulation()],
            Direction.EAST: [Direction.NORTH.get_xy_manipulation(), Direction.EAST.get_xy_manipulation(),
                             Direction.SOUTH.get_xy_manipulation()],
            Direction.SOUTH: [Direction.SOUTH.get_xy_manipulation(), Direction.EAST.get_xy_manipulation(),
                              Direction.WEST.get_xy_manipulation()],
            Direction.WEST: [Direction.NORTH.get_xy_manipulation(), Direction.WEST.get_xy_manipulation(),
                             Direction.SOUTH.get_xy_manipulation()],
        }
        return m[self]
