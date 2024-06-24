import pygame
import constants


class Scoreboard:
    """
    Clase Scoreboard, permite llevar un seguimiento de la puntuación del Player.
    """
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def update_score(self, points):
        self.score += points

    def render(self, screen):
        scoreboard = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        text_rect = scoreboard.get_rect()
        text_rect.center = (constants.WIDTH // 2, 700)
        screen.blit(scoreboard, text_rect)
