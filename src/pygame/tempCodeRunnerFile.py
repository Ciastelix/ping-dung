import pygame.display
import pygame.image
import pygame.key
from pygame.locals import *
import pygame.rect
import pygame.transform
import pygame
from world import World
from world_data import world_data
from player import Player

pygame.init()
clock = pygame.time.Clock()
fps = 60
# set screen type to full window
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# play music in background
pygame.mixer.music.load("music.mp3")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marrio")
bg_image = pygame.image.load("bg.webp")
# Assuming SCREEN_WIDTH and SCREEN_HEIGHT are the dimensions of your screen
darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
darken_surface.fill((0, 0, 0))
darken_surface.set_alpha(128)

world = World(world_data)
player = Player(100, 120)
group = world.get_group

# Camera position
camera_x = 0
camera_y = 0

run = True
while run:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    screen.blit(bg_image, (0, 0))

    # Update camera position based on player position
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_y = player.rect.y - SCREEN_HEIGHT // 2

    world.draw(screen, camera_x, camera_y)
    for enemy in group:
        enemy.update()
    player.update(world, screen, SCREEN_HEIGHT, camera_x, camera_y)

    # Overlay the darken surface to make the screen darker
    screen.blit(darken_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
