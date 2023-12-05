from controllers.game import GameController

if __name__ == "__main__":
    game = GameController()
    game.set_init_state()
    game.run()
