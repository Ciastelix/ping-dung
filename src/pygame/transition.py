import math
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

transition_start_time = 0
transition_time = 1000
transition_start_time = None

transition_text = "You go deeper..."
font = pygame.font.Font("menu.otf", 55)


def start_transition():
    global transition, transition_start_time
    transition = True
    transition_start_time = pygame.time.get_ticks()


def draw_transition(screen, elapsed_time):
    progress = elapsed_time / transition_time
    alpha = math.sin(progress * math.pi / 2)  # Ease-in and ease-out
    black_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    black_surface.fill((0, 0, 0))
    black_surface.set_alpha(int(alpha * 255))

    screen.blit(black_surface, (0, 0))

    if elapsed_time < transition_time / 2:
        alpha_text = alpha * 2  # Ease-in for the text
    else:
        alpha_text = (1 - alpha) * 2  # Ease-out for the text

    text_surface = font.render(transition_text, True, (255, 255, 255))
    text_surface.set_alpha(int(alpha_text * 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
