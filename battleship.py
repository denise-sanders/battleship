from random import randrange
from ai import AI
from board import Board

"""
    Class to run the battleship gameloop and handle human interaction.
"""
class Battleship:

    def printBoards(self):
        self.player_board.printBoard(True, "Player board")
        self.ai_board.printBoard(False, "AI board")

    # Handles player input for placing boats
    @staticmethod
    def getPlayerInputForCoordinatesAndDirection(ship_name):
        raw_x = input("What would you like the x coordinate of your {} (length {}) to be? ".format(ship_name, Board.ship_names_to_size[ship_name]))
        raw_y = input("What would you like the y coordinate of your {} (length {}) to be? ".format(ship_name, Board.ship_names_to_size[ship_name]))
        direction_name = input("Which direction {} would you like your boat to be in, relative to the coordinate? ".format(Board.direction_name_to_direction.keys()))

        if direction_name not in Board.direction_name_to_direction:
            direction_name = None

        start_x = Board.validateCoordinate(raw_x)
        start_y = Board.validateCoordinate(raw_y)
        return (start_x, start_y, direction_name)


    # control loop for a player placing boats in valid place
    def playerPlaceShips(self):
        print("Welcome captain! Your board today is {}x{}, so please enter coordinates between 0-{}".format(Board.board_size, Board.board_size, Board.board_size - 1))
        for ship_name in Board.ship_names_to_size:
            while True:
                start_x, start_y, direction_name = Battleship.getPlayerInputForCoordinatesAndDirection(ship_name)
                if (start_x is not None and start_y is not None and direction_name is not None):
                    if self.player_board.canPlaceShip(start_x, start_y, Board.direction_name_to_direction[direction_name], Board.ship_names_to_size[ship_name]):
                        self.player_board.placeShip(start_x, start_y, Board.direction_name_to_direction[direction_name], Board.ship_names_to_size[ship_name], ship_name)
                        self.player_board.printBoard(True, "Player board")
                        print("Your {} was successfully placed!\n".format(ship_name))
                        break
                    else:
                        print("Your ship cannot be placed there, it must not go out of bounds or be on top of one of your other ships\n")
                else:
                    print("You need to enter a number between 0-{} for your x and y coordinates, and a valid direction. Please try again.\n".format(Board.board_size - 1))



    def aiTurn(self):
        result = None
        while result is None:
            x_cor, y_cor = self.ai.getNextGuess(self.player_board, Board.board_size)

            try:
                result, ship_name_if_hit = self.player_board.checkGuess(x_cor, y_cor)
                self.player_board.grid[y_cor][x_cor] = result
                if result == "hit":
                    print("Avast! Your opponent struck you at ({},{})".format(x_cor, y_cor))
                    if ship_name_if_hit is not None and not self.player_board.doesBoardHaveShip(ship_name_if_hit):
                        print("Your opponent has sunk your {}".format(ship_name_if_hit))
                else:
                    print("Your opponent missed you at ({},{})".format(x_cor, y_cor))
            except ValueError:
                pass

    def playerTurn(self):
        result = None
        while result is None:
            raw_x = input("What is the x coordinate of the cell you want to hit? ")
            raw_y = input("What is the y coordinate of the cell you want to hit? ")
            x_cor = Board.validateCoordinate(raw_x)
            y_cor = Board.validateCoordinate(raw_y)

            try:
                result, ship_name_if_hit = self.ai_board.checkGuess(x_cor, y_cor)
                self.ai_board.grid[y_cor][x_cor] = result
                print("\n")
                print("You have a {}!".format(result))
                if ship_name_if_hit is not None and not self.ai_board.doesBoardHaveShip(ship_name_if_hit):
                    print("You have sunk your opponent's {}".format(ship_name_if_hit))

            except ValueError:
                print("\n")
                print("Your guess must be a number between 0-{} that you have not already guessed.".format(Board.board_size))

    def gameLoop(self):
        while True:
            print("-"*100)
            self.playerTurn()
            if not self.ai_board.doesBoardHaveAnyShips():
                print("\n")
                print("Congratulations captain! You have destroyed your opponent's navy")
                break
        
            self.aiTurn()
            if not self.player_board.doesBoardHaveAnyShips():
                print("\n")
                print("Argh! Your navy has been destroyed")
                break

            self.printBoards()
    
    # Initialize game and start loop
    def __init__(self):
        self.ai = AI()
        self.player_board = Board()
        
        self.ai_board = Board()
        self.ai_board.placeRandomShips()
        
        self.player_board = Board()
        self.playerPlaceShips()
        # self.player_board.placeRandomShips() # for debugging

        self.gameLoop()     

if __name__ == "__main__":
    b = Battleship()
