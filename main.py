import pygame
from pygame.font import Font
from pygame.time import Clock
import random
import sys


class Square:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.screen_width, self.screen_height = 600, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Square-Dodge")

        self.default_font: str = pygame.font.get_default_font()
        self.font: Font = pygame.font.Font(self.default_font, 26)

        self.WHITE: tuple = (255, 255, 255)
        self.BLACK: tuple = (0, 0, 0)
        self.RED: tuple = (134, 43, 13)
        self.BLUE: tuple = (116, 155, 194)

        self.player_size: int = 30
        self.player_pos: list[int] = [0, 0]

        self.enemy_size: int = 50
        self.ememy_pos: list[int] = []
        self.enemy_list = []
        self.ememy_speed: int = 3
        self.enemy_frequency: int = 20  # Low number = more enemies, High = less enemines

        self.clock: Clock = pygame.time.Clock()

        self.game_over: bool = False
        self.score: int = 0
        self.frame_count: int = 0

    def create_enemy(self):
        enemy_pos: list[int] = [random.randint(0, self.screen_width - self.enemy_size), -self.enemy_size]
        self.enemy_list.append(enemy_pos)

    def update_enemy_positions(self):
        if self.frame_count % self.enemy_frequency == 0:
            self.create_enemy()

        for idx, enemy_pos in enumerate(self.enemy_list):
            if -self.enemy_size <= enemy_pos[1] < self.screen_height:
                enemy_pos[1] += self.ememy_speed
            else:
                self.enemy_list.pop(idx)
                self.score += 1
                self.ememy_speed += 0.1

                if self.enemy_frequency > 10:
                    if self.score % 15 == 0:
                        self.enemy_frequency -= 2

    def detect_collision(self, player_pos: list[int], enemy_pos: list[int]) -> bool:
        px, py = player_pos
        ex, ey = enemy_pos

        if (px <= ex < (px + self.player_size)) or (ex <= px < (ex + self.enemy_size)):
            if (py <= ey < (py + self.player_size)) or (ey <= py < (ey + self.enemy_size)):
                return True
        return False

    def show_game_over(self):
        game_over_text = self.font.render('Game Over', True, self.WHITE)
        self.screen.blit(game_over_text, (self.screen_width // 2 - 70, self.screen_height // 2 - 16))

    # Replay the game
    def replay_game(self):
        """Reset everything to its initial state"""

        # Reset enemies
        self.enemy_list = []
        self.ememy_speed: float = 3
        self.enemy_frequency: int = 20

        # Reset game stats
        self.game_over: bool = False
        self.frame_count: int = 0
        self.score: int = 0

    def draw_character(self, color: tuple, position: list[int], size: int):
        pygame.draw.rect(self.screen, color, (position[0], position[1], size, size))

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # pygame.K_r = when the key r is pressed
                    if self.game_over and event.key == pygame.K_r:
                        self.replay_game()

                mouse_pos: tuple[int, int] = pygame.mouse.get_pos()

                # Update the player's position to follow the mouse
                self.player_pos[0] = mouse_pos[0] - self.player_size // 2
                self.player_pos[1] = mouse_pos[1] - self.player_size // 2

                # Make sure the player stays on the screen
                self.player_pos[0] = max(0, min(self.player_pos[0], self.screen_width - self.player_size))
                self.player_pos[1] = max(0, min(self.player_pos[1], self.screen_height - self.player_size))

            if not self.game_over:
                self.update_enemy_positions()

                for enemy_pos in self.enemy_list:
                    if self.detect_collision(self.player_pos, enemy_pos):
                        self.game_over = True

                self.screen.fill(self.BLACK)

                self.draw_character(self.WHITE, self.player_pos, self.player_size)

                for enemy_pos in self.enemy_list:
                    if self.score > 100:
                        self.draw_character(self.BLUE, enemy_pos, self.enemy_size)
                    else:
                        self.draw_character(self.RED, enemy_pos, self.enemy_size)

                score_text = self.font.render(f'Score: {self.score}', True, self.WHITE)
                self.screen.blit(score_text, [10, 10])

                # Increment the frame count
                self.frame_count += 1
            else:
                self.show_game_over()

                # Update the display
            pygame.display.update()

            # Frame rate
            self.clock.tick(60)


# Run the game
if __name__ == '__main__':
    game = Square()
    game.run_game()
