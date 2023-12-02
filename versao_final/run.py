from controllers.game import GameController

from states.init import InitState

if __name__ == "__main__":
    game = GameController()
    game.change_state(InitState)
    game.run()
