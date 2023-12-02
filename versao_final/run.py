from game import Game

from states.init import InitState

if __name__ == "__main__":
    game = Game()
    game.change_state(InitState)
    game.run()
