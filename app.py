import pygame
from sys import exit
from player import Player
from game_grid import GameGrid
from button import Button

#  This variable is used to manage the game states in order to manage the game correctly
GAME_STATE = {
    "launching": "launching",
    "playing": "playing",
    "ending": "ending",
}


class ConnectFour:
    def __init__(self):
        # Game parameters
        self.game_state = GAME_STATE["launching"]
        self.played = False
        self.player = {
            "1": Player(1, (242, 95, 92)),  # Red player
            "2": Player(2, (255, 224, 102))  # Yellow player
        }
        self.current_player = self.player["1"].key
        self.grid = GameGrid()
        self.reset_button = Button(16, 202, 373, 436)
        # Aesthetic parameters
        self.background_color = (251, 241, 222)

        pygame.init()
        screen = pygame.display.set_mode((900, 500))
        pygame.display.set_caption('Connect Four')
        icon = pygame.image.load('resources/image/icon.png')
        pygame.display.set_icon(icon)
        self.launching_screen(screen)

    def play(self, screen):
        self.update_background(screen)
        self.draw_grid(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = event.pos
                    self.show_move(mouse_position, screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = event.pos
                    if self.reset_button.is_clicked(mouse_position):
                        self.reset_game(screen)
                    elif self.grid.is_focused(mouse_position[0]) and self.game_state == GAME_STATE["playing"]:
                        column_click = self.grid.convert_click_to_column(mouse_position[0])
                        row = self.find_first_free_row(self.current_player, column_click, screen)
                        self.draw_piece(column_click, row, screen)
                        if self.grid.game_is_over(self.current_player):
                            self.game_ended(screen)
                        if self.played:
                            self.next_player()
                            self.show_move(mouse_position, screen)
            pygame.display.update()

    def game_ended(self, screen):
        self.game_state = GAME_STATE["ending"]
        police = pygame.font.Font('resources/font/ArcadeClassic.ttf', 65)
        winner_output = police.render(f"Player {self.current_player} won!",
                                      True,
                                      self.player[f"{self.current_player}"].color)
        screen.blit(winner_output, (280, 0))
        pygame.display.flip()

    def show_move(self, mouse_position, screen):
        pygame.draw.rect(screen, self.background_color, (
            self.grid.left_side, 80 - self.grid.box_size // 2, self.grid.column_count * self.grid.box_size,
            self.grid.box_size))
        if self.grid.is_focused(mouse_position[0]):
            pygame.draw.circle(screen,
                               self.player[f"{self.current_player}"].color,
                               (mouse_position[0], 80),
                               self.grid.radius
                               )

    def next_player(self):
        if self.current_player == self.player["1"].key:
            self.current_player = self.player["2"].key
        else:
            self.current_player = self.player["1"].key
        self.played = False

    def draw_grid(self, screen):
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
        pygame.display.update()

    def launching_screen(self, screen):
        self.update_background(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_state = GAME_STATE["playing"]
                    self.play(screen)

    def update_background(self, screen):
        fond = pygame.image.load(f'resources/image/{self.game_state}_background.png')
        fond = fond.convert()
        screen.blit(fond, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def reset_game(self, screen):
        self.__init__()

    def draw_piece(self, column_click, row, screen):
        pygame.draw.circle(screen, self.player[f"{self.current_player}"].color,
                           (self.grid.left_side + int(
                               column_click * self.grid.box_size + self.grid.box_size / 2),
                            self.grid.bottom_side + int(
                                row * self.grid.box_size + self.grid.box_size + self.grid.box_size / 2)),
                           self.grid.radius)

    def find_first_free_row(self, current_player, column, screen):
        if 0 <= column <= 6:
            row = self.grid.grid[:, column]
            find_place = False
            free_place_index = 0
            while not find_place and free_place_index >= -6:
                free_place_index -= 1
                if row[free_place_index] == 0:
                    find_place = True
            if free_place_index >= -6:
                row[free_place_index] = self.current_player
                self.played = True
            return free_place_index