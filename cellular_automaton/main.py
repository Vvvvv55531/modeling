from game_of_life import *


if __name__ == "__main__":

    print("\nУправление:",)
    print(*CONTROL, sep="\n")

    game = GameLife(800, 800, 13, 30, WHITE, BLACK, GRAY)
    game.run()
