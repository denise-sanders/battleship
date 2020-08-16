from random import randrange
from board import Board

"""
    AI to choose next move to make for the computer-controlled player.
    The algorithm is:
        Guess randomly until we hit a ship.
        Once we hit a ship, mark that hit as a "pivot" and try the squares around it
        If we get another hit, continue in that direction until the ship is 
        sunk, or else start going in the vertical direction.

        Randomly guess again.

        State Values:
        pivot: the (x,y) coordinates of a hit we have made, and will be guessing in all directions around.
        exhaused_directions: every direction we have tried to find another hit in
        successful_direction: if we have made a hit in a certain direction, we save that so we can use it again.
        offset: the distance from the pivot we will place our next guess
"""
class AI:

    def __init__(self):
        # initially we have no information for guessing
        self.clearState()

    # called to represent when we have no information about our next move
    def clearState(self):
        self.pivot = None
        self.exhausted_directions = set()
        self.successful_direction = None
        self.offset = None

    @staticmethod
    def directions():
        return list(Board.direction_name_to_direction.values())

    def chooseNextDirection(self):
        if self.successful_direction is not None: 
            # we had a hit in this direction, so we want to try the direction directly oppposite if it has not already been tried
            candidate_direction = (self.successful_direction[0] * -1, self.successful_direction[1] * -1)
            if candidate_direction in self.exhausted_directions:
                candidate_direction = list(set(AI.directions()).difference(self.exhausted_directions))[0]
            return candidate_direction
        else:
            # if we do not already have another hit around this pivot, we choose any untried direction
            return list(set(AI.directions()).difference(self.exhausted_directions))[0]

    # When we send a move to the game, we need to update our internal state to know
    # what move to make next
    def setStateBasedOnGuess(self, board, x_cor, y_cor, result, ship_name_if_hit, current_direction):
        if self.pivot is None:
            # We tried a random guess
            if result == "miss":
                # continue random guessing
                return
            if result == "hit": # we have a hit, mark pivot
                if not board.doesBoardHaveShipWithGuess(x_cor, y_cor, ship_name_if_hit):
                    # I believe there is an edge case if ships are placed next to each other
                    # that can result in a ship getting hit here.
                    # If we just sank a ship here, we shouldn't set state to guess this point's neighbors
                    return
                else:
                    # add state to guess adjacent to this point, there is still part of this ship nearby!
                    self.pivot = (x_cor, y_cor)
                    self.offset = 1
        else: 
            if result == "miss":
                if self.offset > 1:
                    # we have made a hit in this last direction, so we want to bias towards opposite direction
                    self.successful_direction = self.chooseNextDirection()
                self.offset = 1
            else:
                if not board.doesBoardHaveShipWithGuess(x_cor, y_cor, ship_name_if_hit):
                    # the ship is sunk!
                    # we go back to randomly guessing
                    self.clearState()
                else:
                    # keep guessing in this direction
                    self.successful_direction = current_direction
                    self.offset += 1 

    # Function called by battleship to recieve the next guess from the AI
    def getNextGuess(self, board, board_size):
        x_cor, y_cor, current_direction = None, None, None
        
        try:
            if self.pivot and len(self.exhausted_directions) != len(AI.directions()):
                current_direction = self.successful_direction
                if current_direction is None:
                    current_direction = self.chooseNextDirection()
                    self.exhausted_directions.add(current_direction)

                x_cor = self.offset*current_direction[0] + self.pivot[0]
                y_cor = self.offset*current_direction[1] + self.pivot[1]

                if x_cor < 0 or x_cor >= board_size or y_cor < 0 or y_cor >= board_size:
                    self.successful_direction = None
                    self.offset = 1
                    raise ValueError("Coordinates are out of range")
            elif len(self.exhausted_directions) == len(AI.directions()):
                # we have exhausted every direction from this pivot point, go back to randomly guessing
                # TODO: we could extend this to try offsets farther away
                self.clearState()
                raise ValueError("No direction is valid from this pivot")

            else: # randomly guess a point
                x_cor = randrange(Board.board_size)
                y_cor = randrange(Board.board_size)

            # If we already have guessed this square, mark successful_direction as None
            # so we stop searching along here.
            if board.grid[y_cor][x_cor] == "hit" or board.grid[y_cor][x_cor] == "miss":
                self.successful_direction = None

            result, ship_name_if_hit = board.checkGuess(x_cor, y_cor)
            self.setStateBasedOnGuess(board, x_cor, y_cor, result, ship_name_if_hit, current_direction)
            
            return x_cor, y_cor
        except ValueError:
            return self.getNextGuess(board, board_size)


