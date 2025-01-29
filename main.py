import asyncio
from src.game import Game

def main():
    game = Game()
    asyncio.run(game.run())

if __name__ == "__main__":
    main()
