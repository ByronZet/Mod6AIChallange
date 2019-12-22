Before starting, make sure you have the latest python version working (the game is tested on python 3.6.3 64bit).

  _______ _             _____
 |__   __| |           / ____|
    | |  | |__   ___  | |  __  __ _ _ __ ___   ___
    | |  | '_ \ / _ \ | | |_ |/ _` | '_ ` _ \ / _ \
    | |  | | | |  __/ | |__| | (_| | | | | | |  __/
    |_|  |_| |_|\___|  \_____|\__,_|_| |_| |_|\___|

The game is the famous snake game (which is a well known game if you ever owned an Nokia 3310). The goal of the game is
to score as high as possible. In the game you play a snake which can move either to the left, the right or straight
ahead. You can score points by eating a food block. By eating, not only your score is increased, but also the size of
the body of the snake. You die whenever you hit your own body, go outside the boundaries of the board or hit a wall.

To test (and run) the game two ways are possible. The first one involves installing a proper IDE (like PyCharm) and
run main.py. The second one is to open a command line (or terminal) in the folder where the game files are located and
typing: "python main.py" (make sure you are running the game with python 3 and not 2, some Linux distributions may
(still) use python to run python 2). Both ways should start the game properly and a screen with a simple user
interface with some blocks should appear.

    Each colored block represents a type of block. The orange block represents the
head of the snake. Whenever the snake eats a block, it will grow in size. The body of the snake has a different kind of
orange than the head. The purple blocks represent a food block. The black blocks represent a wall.

    Furthermore two different user interface elements can be noted. The slider below regulates the update speed of the
game. To be more precise, the number on the slider indicates the number of updates per second the game runs. It can
also be chosen to put the slider to zero. This means no updates will take place (unless the slider is set to a number
higher than zero. It then can be chosen to update the game by pressing the button with the label: "Next Step".

    Last but not least, the score achieved will be printed to the console. It also mentions the number of turns it took
to achieve this score.



  _______ _    _ ______    _____ ____  _____  ______
 |__   __| |  | |  ____|  / ____/ __ \|  __ \|  ____|
    | |  | |__| | |__    | |   | |  | | |  | | |__
    | |  |  __  |  __|   | |   | |  | | |  | |  __|
    | |  | |  | | |____  | |___| |__| | |__| | |____
    |_|  |_|  |_|______|  \_____\____/|_____/|______|

Various python files are used to run the game. All are important for running, only some are important for you. These are
 listed below:

- agent.py: this is the ONLY python file you should edit. This python file represents the agent which controls the snake.
Documentation in the file should be clear enough to get started.

- main.py: This is the main python file and used to run the game. This file also contains the game settings. If you
would like to see how your agent behaves with different settings, you can change them there. When wanting to test
your agent with more walls, you need to put test_config to False.

- move.py: This python file contains some functions to help you managing the movement system used in the game. It is not
 obligated to use these, but may prove useful while developing your agent.

- gameobjects.py: This python file contains all possible game objects used in the game. What this is used for is
explained in the documentation of agent.py.


   _____ _
  / ____| |
 | |    | |__   __ _ _ __   __ _  ___  ___
 | |    | '_ \ / _` | '_ \ / _` |/ _ \/ __|
 | |____| | | | (_| | | | | (_| |  __/\__ \
  \_____|_| |_|\__,_|_| |_|\__, |\___||___/
                            __/ |
                           |___/

Some changes have been made to the game to make it easier for you to implement the reinforcement learning exercises.
These changes are "backwards compatible". The quotation marks are there as you do need to do some work to get your
previous agent working in this version. You need to copy everything that was listed in the get_move function to the new
version of agent.py. Furthermore, you also need to copy any help functions, the contents of on_die if used and
imports. Now your agent should work as it used to do.

But what exactly has been changed? The things changed are listed below:

- function get_move (in agent.py) has extra parameters. The new parameters include head_position and body_parts. What
these parameters are, is explained in the documentation.

- function on_die (in agent.py) has extra parameters. The new parameters include head_position, board, score and
body_parts. What these parameters are, is explained in the documentation.

- function should_redraw_board (in agent.py) is added. What this function does is explained in the documentation.

- function should_grow_on_food_collision (in agent.py) is added. What this function does is explained in the
documentation.

- variable print_score_not_on_non_redraw (in main.py) is added. This variable indicates whether the score should not be
printed when the board is not redrawn (this saves some spam in the console).


