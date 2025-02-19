import argparse
import asyncio
from src.game import Game
from src.tilemap.editor import Editor

def main():
    parser = argparse.ArgumentParser(description='Run the game or the editor.')
    parser.add_argument('-e', '--editor', action='store_true', help='Run the editor.')
    args = parser.parse_args()

    if args.editor:
        Editor().run()
    else:
        game = Game()
        asyncio.run(game.run())

if __name__ == "__main__":
    main()
