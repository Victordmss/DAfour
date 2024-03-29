import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7


class GameGrid:
    def __init__(self):

        # Grid parameters
        self.row_count = ROW_COUNT
        self.column_count = COLUMN_COUNT
        self.grid = np.zeros((self.row_count, self.column_count))   # Logical grid
        self.draw = True

        # Geometric parameters
        self.box_size = 50
        self.radius = int(self.box_size / 2 - 5)
        self.grid_size = (self.column_count * self.box_size, self.row_count * self.box_size)

        # Borders
        self.left_side = 450 - (self.box_size * self.column_count) // 2
        self.top_side = 210 - (self.box_size * self.row_count) // 2
        self.bottom_side = 210 + (self.box_size * self.row_count) // 2
        self.right_side = 450 + (self.box_size * self.column_count) / 2

        # Aesthetic parameters
        self.color = (10, 36, 120)

    # This method is used to know id the game is over (draw or victory)
    def game_is_over(self, piece):
        self.draw = True
        for c in range(self.column_count):
            for r in range(self.row_count):
                if self.grid[r][c] == 0:
                    self.draw = False  # If there is still at least one 0, the grid isn't full, no draw
        for c in range(self.column_count - 3):   # check for horizontal win
            for r in range(self.row_count):
                if self.grid[r][c] == piece and self.grid[r][c + 1] == piece \
                        and self.grid[r][c + 2] == piece and \
                        self.grid[r][c + 3] == piece:
                    self.draw = False
                    return True
        for c in range(self.column_count):   # check for vertical win
            for r in range(self.row_count - 3):
                if self.grid[r][c] == piece and self.grid[r + 1][c] == piece \
                        and self.grid[r + 2][c] == piece and \
                        self.grid[r + 3][c] == piece:
                    self.draw = False
                    return True
        for c in range(self.column_count - 3):    # check for diagonal win (bottom left to top right)
            for r in range(self.row_count - 3):
                if self.grid[r][c] == piece and self.grid[r + 1][c + 1] == piece and \
                        self.grid[r + 2][c + 2] == piece and self.grid[r + 3][c + 3] == piece:
                    self.draw = False
                    return True
        for c in range(self.column_count - 3):    # check for diagonal win (top left to bottom right)
            for r in range(3, self.row_count):
                if self.grid[r][c] == piece and self.grid[r - 1][c + 1] == piece and \
                        self.grid[r - 2][c + 2] == piece and self.grid[r - 3][c + 3] == piece:
                    self.draw = False
                    return True
        return self.draw

    # This method checks if the grid is currently focused by the user
    def is_focused(self, mouse_position):
        return self.left_side + self.box_size // 2 - 5 < mouse_position < self.right_side - self.box_size // 2 + 5

    # This method converts a click into a valid column for the grid
    def convert_click_to_column(self, mouse_position):
        return int(round((mouse_position - (self.left_side + self.box_size // 2)) / self.box_size, 0))
