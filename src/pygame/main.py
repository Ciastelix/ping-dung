import pygame
from world import World
from player import Player
from a import generate_dungeon
from button import Button

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
# use comic font
font = pygame.font.Font("menu.otf", 55)
# font = pygame.font.SysFont(None, 55)
# Initialize other game variables
camera_x = 0
camera_y = 0
run = True


def draw_level_counter(screen, level):
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))


def load_next_level():
    global world, player, world_data
    world_data = generate_dungeon()  # Generate new level data
    world = World(world_data[0])  # Load new world
    starting_position = world.get_starting_position  # Get new starting position
    player.rect.x, player.rect.y = (
        starting_position  # Move player to new starting position
    )


while run:
    clock.tick(fps)
    if main_menu:
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
            load_next_level()
            level += 1
        draw_level_counter(screen, level)

        # Overlay the darken surface to make the screen darker
        screen.blit(darken_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
