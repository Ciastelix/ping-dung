import pygame
from world import World
from player import Player
from a import generate_dungeon
from button import Button
import time
import math

pygame.init()
clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marrio")
menu = pygame.image.load("menu.png")
menu = pygame.transform.scale(menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.music.load(
    "menu.mp3"
)  # Replace "menu_music.mp3" with the path to your music file
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # Play the music indefinitely

bg_image = pygame.image.load("bg.webp")
play_button_image = pygame.image.load("play.png")

# scale the play button image times 3
play_button_image = pygame.transform.scale(
    play_button_image,
    (play_button_image.get_width() * 3, play_button_image.get_height() * 3),
)
darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
darken_surface.fill((0, 0, 0))
darken_surface.set_alpha(128)

# Replace this with your world data generation
world_data = generate_dungeon()  # Make sure this returns the correct format

# Create the world and get the starting position
world = World(world_data[0])
starting_position = world.get_starting_position
main_menu = True

# Create the player at the starting position
player = Player(*starting_position)
play_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, play_button_image)
level = 1
font = pygame.font.Font("menu.otf", 55)
camera_x = 0
camera_y = 0
run = True
transition = False
transition_start_time = 0
transition_time = 1000  # 1 second
transition_start_time = None
transition_active = False
transition_text = "You go deeper..."


def draw_level_counter(screen, level):
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))


def start_transition():
    global transition, transition_start_time
    transition = True
    transition_start_time = pygame.time.get_ticks()


def load_next_level():
    global world, player, world_data, transition, level
    transition = False
    world_data = generate_dungeon()  # Generate new level data
    world = World(world_data[0])  # Load new world
    starting_position = world.get_starting_position  # Get new starting position
    player.rect.x, player.rect.y = (
        starting_position  # Move player to new starting position
    )
    level += 1


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


# Step 1: Create a Circle Mask
def create_vision_mask(screen_width, screen_height, radius):
    # Create a surface with per-pixel alpha
    mask_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    # Fill with a semi-transparent black color
    mask_surface.fill((0, 0, 0, 128))
    # Draw a transparent circle in the middle
    pygame.draw.circle(
        mask_surface, (0, 0, 0, 0), (screen_width // 2, screen_height // 2), radius
    )
    return mask_surface


# Step 2: Position the Circle Around the Player
def update_vision_mask(mask_surface, player_x, player_y, screen_width, screen_height):
    # Clear the mask first
    mask_surface.fill((0, 0, 0, 128))
    # Calculate the circle's position based on the player's position
    circle_x = player_x - screen_width // 2
    circle_y = player_y - screen_height // 2
    # Draw the transparent circle around the player
    pygame.draw.circle(
        mask_surface, (0, 0, 0, 0), (-circle_x, -circle_y), 150
    )  # 150 is the radius


vision_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
radius = 100  # Vision radius


# In your main game loop
while run:
    clock.tick(fps)

    if transition_active:
        elapsed_time = pygame.time.get_ticks() - transition_start_time
        draw_transition(screen, elapsed_time)

        if elapsed_time >= transition_time:
            transition_active = False
            load_next_level()
            level += 1

    elif main_menu:
        screen.blit(menu, (0, 0))
        if play_button.draw(screen):
            main_menu = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load("game.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
    else:
        screen.blit(bg_image, (0, 0))

        # Update camera position based on player position
        camera_x = player.rect.x - SCREEN_WIDTH // 2
        camera_y = player.rect.y - SCREEN_HEIGHT // 2

        world.draw(screen, camera_x, camera_y)
        for enemy in world.get_group:
            enemy.update()
        player.update(world, screen, camera_x, camera_y)
        if player.on_portal_tile(world):
            transition_active = True
            transition_start_time = pygame.time.get_ticks()

        vision_mask.fill((0, 0, 0, 128))  # Semi-transparent fill
        pygame.draw.circle(
            vision_mask,
            (0, 0, 0, 0),
            (player.rect.x - camera_x + 20, player.rect.y - camera_y + 20),
            radius,
        )  # Transparent circle
        screen.blit(vision_mask, (0, 0))

        screen.blit(darken_surface, (0, 0))
        draw_level_counter(screen, level)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
