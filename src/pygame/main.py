import pygame
from world import World
from player import Player
from a import generate_dungeon

pygame.init()
clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marrio")

bg_image = pygame.image.load("bg.webp")
darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
darken_surface.fill((0, 0, 0))
darken_surface.set_alpha(128)

# Replace this with your world data generation
world_data = generate_dungeon()  # Make sure this returns the correct format

# Create the world and get the starting position
world = World(world_data[0])
starting_position = world.get_starting_position

# Create the player at the starting position
player = Player(*starting_position)

# Initialize other game variables
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
    for enemy in world.get_group:
        enemy.update()
    player.update(world, screen, camera_x, camera_y)

    # Overlay the darken surface to make the screen darker
    screen.blit(darken_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
