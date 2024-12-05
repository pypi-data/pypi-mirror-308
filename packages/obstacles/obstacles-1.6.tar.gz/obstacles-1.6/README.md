This is a prototype simple game. Simply you are the turtle and you need to avoid the obstacles to get to the target. Each time you get to the target the target gets to a different place and the number of obstacles increases by one. How many obstacles do you believe you can dodge?

The turtle can be moved with the arrow keys to get to the target. The score will be tracked on the Terminal rather than on the window, at least for now.

To import the actual game on a python file type:
from Obstacles import obstacles_game
...
obstacles_game()

To start directly from the Terminal:
obstacles-game

To install on Debian 12 and some other distributions do note that you need to use pipx instead of pip. To install it:
pipx install obstacles