from random import randrange

class Board:
    # static class variables
    ship_names_to_size = {
        "carrier" : 5,
        "battleship": 4,
        "cruiser": 3,
        "submarine": 3,
        "destroyer": 2
    }

    cell_value_to_print_value = { **{
        None: " ",
        "hit": "!",
        "miss": "x",
    }, **{ ship_name: "s" for ship_name in ship_names_to_size }
    }

    direction_name_to_direction = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0)
    }

    board_size = 10

    def __init__(self):
        self.grid = []
        for row in range(Board.board_size):
            self.grid.append([None] * Board.board_size)
    
    @staticmethod
    def getRandomDirection():
        # a direction is represented by a (x,y) offset
        direction_names = list(Board.direction_name_to_direction.keys())
        direction_index = randrange(4)
        return Board.direction_name_to_direction[direction_names[direction_index]]

    def canPlaceShip(self, start_x, start_y, direction, length):
        end_x = (length - 1) * direction[0] + start_x
        end_y = (length - 1) * direction[1] + start_y

        if end_x < 0 or end_x >= Board.board_size or end_y < 0 or end_y >= Board.board_size:
            return False # boat will go off the board in this direction
        for ship_segment in range(length):
            current_x = ship_segment * direction[0] + start_x
            current_y = ship_segment * direction[1] + start_y

            if self.grid[current_y][current_x] is not None:
                return False
        return True

    def placeShip(self, start_x, start_y, direction, length, ship_name):
        for ship_segment in range(length):
            current_x = ship_segment * direction[0] + start_x
            current_y = ship_segment * direction[1] + start_y

            self.grid[current_y][current_x] = ship_name


    def placeRandomShips(self):
        for ship_name in Board.ship_names_to_size:
            while True:
                random_x_cor = randrange(Board.board_size)
                random_y_cor = randrange(Board.board_size)
                direction = Board.getRandomDirection()
                if self.canPlaceShip(random_x_cor, random_y_cor, direction, Board.ship_names_to_size[ship_name]):
                    self.placeShip(random_x_cor, random_y_cor, direction, Board.ship_names_to_size[ship_name], ship_name)
                    break

    # Display function to print board and helper numbers
    def printBoard(self, show_ships, name):
        print("\n")
        print(name)
        print("".join(['  '] + list(map(str, range(Board.board_size)))))
        for y in range(len(self.grid)):
            row = [str(y) + "|"]
            for x in range(len(self.grid[0])):
                # Hide ship if we do not want to print it
                row.append(Board.cell_value_to_print_value[self.grid[y][x]]) if show_ships or self.grid[y][x] not in Board.ship_names_to_size else row.append(Board.cell_value_to_print_value[None])
            print("".join(row))

    @staticmethod
    def validateCoordinate(raw_input):
        try:
            coordinate_value = int(raw_input)
            if coordinate_value < 0 or coordinate_value >= Board.board_size:
                return None
        except ValueError:
            return None
        return coordinate_value

    # Used for determining win/loss condition
    def doesBoardHaveAnyShips(self):
        for ship_name in Board.ship_names_to_size:
            if self.doesBoardHaveShip(ship_name):
                return True
        return False

    def doesBoardHaveShip(self, ship_name):
        for y_cor in range(Board.board_size):
            for x_cor in range(Board.board_size):
                if self.grid[y_cor][x_cor] == ship_name:
                    return True
        print("{} has sunk".format(ship_name))
        return False

    def checkGuess(self, x_cor, y_cor):
        if x_cor is not None and y_cor is not None and self.grid[y_cor][x_cor] != "hit" and self.grid[y_cor][x_cor] != "miss":
            # guess is valid
            if self.grid[y_cor][x_cor] in Board.ship_names_to_size:
                return "hit", self.grid[y_cor][x_cor]
            else:
                return "miss", None
        raise ValueError("Invalid guess")

    # Helper function to check for a ship on the board while ignoring
    # the guess coordinate.
    # The AI class does not mutate boards, but we need to
    # mark our last guess in order to know if we are about
    # to sink a ship.
    def doesBoardHaveShipWithGuess(self, x_cor_guess, y_cor_guess, ship_name):
        for y_cor in range(Board.board_size):
            for x_cor in range(Board.board_size):
                if x_cor_guess == x_cor and y_cor_guess == y_cor:
                    pass
                if self.grid[y_cor][x_cor] == ship_name:
                    return True
        print("{} has sunk".format(ship_name))
        return False
