import pygame
from sys import exit
from player import Player
from game_grid import GameGrid
from button import Button

#  This constant variable is used to manage the game states in order to manage the game correctly
GAME_STATE = {
    "launching": "launching",
    "playing": "playing",
    "ending": "ending",
}


class ConnectFour:
    def __init__(self):
        # This dictionary contains information about both players
        self.player = {
            "1": Player(1, (242, 95, 92)),  # Red player
            "2": Player(2, (255, 224, 102))  # Yellow player
        }

        # Game parameters
        self.played = False  # This bool will help to know if a player has played or not
        self.current_player = self.player["1"].key  # Red player always starts

        # Dynamic widget of the game
        self.grid = GameGrid()  # Creation of the logical grid of the game
        self.reset_button = Button(16, 202, 373, 436)  # Creation of the reset button to restart the game

        # Aesthetic parameters
        self.background_color = (251, 241, 222)

        # Launching the game
        pygame.init()
        screen = pygame.display.set_mode((900, 500))
        pygame.display.set_caption('Connect Four')
        icon = pygame.image.load('resources/image/icon.png')
        pygame.display.set_icon(icon)
        self.game_state = GAME_STATE["launching"]  # We start the game with the launching state
        self.launching_screen(screen)

    # This method is used to play the game and show the modification on the screen.
    def play(self, screen):
        self.update_background(screen)  # Dynamic modification of the background with the game state
        self.draw_grid(screen)  # Draw the dynamic grid on the screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If user wants to quit the game
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:  # If user moves the mouse
                    mouse_position = event.pos
                    self.show_move(mouse_position, screen)  # Preview of the user's movement linked to his color
                if event.type == pygame.MOUSEBUTTONDOWN:  # If user clicks on the screen
                    mouse_position = event.pos
                    if self.reset_button.is_clicked(mouse_position):  # If reset button is clicked, we restart the game
                        self.reset_game(screen)
                    # If the game state is playing (not ending) and if the grid has been focused during the click
                    elif self.game_state == GAME_STATE["playing"] and self.grid.is_focused(mouse_position[0]):
                        # Convert the click into int that can be processed by the program
                        column_click = self.grid.convert_click_to_column(mouse_position[0])
                        # Find the good row simulating the effect of gravity
                        row = self.find_first_free_row(self.current_player, column_click, screen)
                        self.draw_piece(column_click, row, screen)  # Draw the new piece on the screen
                        if self.played:  # If the move is valid (column isn't full)
                            if self.grid.game_is_over(self.current_player):  # Check if the game is over
                                self.game_ended(screen)
                            self.next_player()  # Change the current player
                            self.show_move(mouse_position, screen)  # Update the preview of the move with the good color
            pygame.display.update()  # Update the screen

    # This method handles when the game is over
    def game_ended(self, screen):
        self.game_state = GAME_STATE["ending"]  # Change the game state to prevent players to play again
        police = pygame.font.Font('resources/font/ArcadeClassic.ttf', 65)
        if self.grid.draw:  # If the game is a draw
            winner_output = police.render(f"Oh ! Draw ...",
                                          True,
                                          (255, 255, 255))
        else:  # If there is a winner
            winner_output = police.render(f"Player {self.current_player} won!",
                                          True,
                                          self.player[f"{self.current_player}"].color)
        screen.blit(winner_output, (280, 0))
        pygame.display.flip()  # Update the text

    # This function displays a preview of a move at the specified mouse position on the screen.
    def show_move(self, mouse_position, screen):
        # Draw a rectangle representing the game grid
        pygame.draw.rect(screen, self.background_color, (
            self.grid.left_side, 80 - self.grid.box_size // 2, self.grid.column_count * self.grid.box_size,
            self.grid.box_size))

        # If the mouse is focusing the game grid, draw a circle representing the column of the current player's move
        if self.grid.is_focused(mouse_position[0]):
            pygame.draw.circle(screen,
                               self.player[f"{self.current_player}"].color,
                               (mouse_position[0], 80),
                               self.grid.radius
                               )

    # This function switches the current player to the other player in the game.
    def next_player(self):
        # If the current player is player 1, switch to player 2. Otherwise, switch to player 1.
        if self.current_player == self.player["1"].key:
            self.current_player = self.player["2"].key
        else:
            self.current_player = self.player["1"].key

        # Reset the "played" flag to False for the new current player.
        self.played = False

    def draw_grid(self, screen):  # This function draws the game grid on the specified screen.
        # Iterate over each column and row of the grid, drawing a rectangle and an empty circle for each cell.
        for column in range(self.grid.column_count):
            for row in range(self.grid.row_count):
                pygame.draw.rect(screen, self.grid.color,
                                 (self.grid.left_side + column * self.grid.box_size,
                                  self.grid.top_side + self.grid.box_size * (row + 1),
                                  self.grid.box_size,
                                  self.grid.box_size))
                pygame.draw.circle(screen, (0, 0, 0, 0),
                                   (self.grid.left_side + int(
                                       column * self.grid.box_size + self.grid.box_size / 2),
                                    self.grid.top_side + int(
                                        row * self.grid.box_size + self.grid.box_size + self.grid.box_size / 2)),
                                   self.grid.radius)

        # Update the screen to display the grid.
        pygame.display.update()

    # This method is used to launch the game
    def launching_screen(self, screen):
        # Update the screen background.
        self.update_background(screen)

        # Keep looping until the user clicks on the mouse button.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If user wants to quit
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # If the user clicks on the mouse button, start the game.
                    self.game_state = GAME_STATE["playing"]
                    self.play(screen)

    # Load the appropriate background image based on the current game state.
    def update_background(self, screen):
        background_image = pygame.image.load(f'resources/image/{self.game_state}_background.png')
        background_image = background_image.convert()
        screen.blit(background_image, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def reset_game(self, screen):
        # Reset the game by re-initializing the game state and clearing the grid.
        self.__init__()

    # Draw a piece on the screen at the specified column and row, using the current player's color.
    def draw_piece(self, column_click, row, screen):
        pygame.draw.circle(screen, self.player[f"{self.current_player}"].color,
                           (self.grid.left_side + int(
                               column_click * self.grid.box_size + self.grid.box_size / 2),
                            self.grid.bottom_side + int(
                                row * self.grid.box_size + self.grid.box_size + self.grid.box_size / 2)),
                           self.grid.radius)

    # This method searches the first free line in the column of the move in order to simulate the action of gravity
    def find_first_free_row(self, current_player, column, screen):
        if 0 <= column <= 6:
            # Get the column from the grid and iterate over it to find the first free row.
            row = self.grid.grid[:, column]
            find_place = False
            free_place_index = 0
            while not find_place and free_place_index >= -6:
                free_place_index -= 1
                if row[free_place_index] == 0:
                    find_place = True
            if free_place_index >= -6:   # If a free row is found, update the grid and set the played flag to True.
                row[free_place_index] = self.current_player
                self.played = True
            return free_place_index  # Return the index of the first free row in the column.
