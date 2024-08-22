import pygame
import random
from world import World
from player import Player
from world_gerenation import generate_dungeon
from button import Button
from pygame import mixer
from transition import draw_transition, start_transition
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marrio")
menu = pygame.image.load("menu.png")
menu = pygame.transform.scale(menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_music = pygame.mixer.Sound("menu.mp3")


menu_music.set_volume(0.2)
game_music = pygame.mixer.Sound("game.mp3")
game_music.set_volume(0.2)
bg_image = pygame.image.load("bg.webp")
play_button_image = pygame.image.load("play.png")

play_button_image = pygame.transform.scale(
    play_button_image,
    (play_button_image.get_width() * 3, play_button_image.get_height() * 3),
)
darken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
darken_surface.fill((0, 0, 0))
darken_surface.set_alpha(128)

world_data = generate_dungeon()

world = World(world_data[0])
starting_position = world.get_starting_position
main_menu = True

player = Player(*starting_position)
play_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, play_button_image)
level = 1
font = pygame.font.Font("menu.otf", 55)
camera_x = 0
camera_y = 0
run = True
transition = False
transition_time = 1000
transition_active = False

enemy_spawn_time = 4000  # 4 seconds
last_spawn_time = pygame.time.get_ticks()


def draw_level_counter(screen, level):
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))


def load_next_level():
    global world, player, world_data, transition, level
    transition = False
    world_data = generate_dungeon()
    world = World(world_data[0])
    starting_position = world.get_starting_position
    player.rect.x, player.rect.y = starting_position
    level += 1


def spawn_enemy_in_random_location():
    current_time = pygame.time.get_ticks()
    global last_spawn_time
    if current_time - last_spawn_time >= enemy_spawn_time:
        last_spawn_time = current_time
        valid_positions = world.get_valid_enemy_positions()
        if valid_positions:
            random_position = random.choice(valid_positions)
            if not player_is_in_position(random_position):
                world.spawn_enemy(random_position)


def player_is_in_position(position):
    player_rect = player.rect
    return player_rect.colliderect(
        pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)
    )


def calculate_walking_animation_duration(player, fps=60):
    number_of_frames = len(player.images_right)
    walk_cooldown = 5
    duration = (number_of_frames * walk_cooldown) / fps
    return duration


menu_music.play(-1)
while run:
    clock.tick(fps)
    spawn_enemy_in_random_location()

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
            menu_music.stop()

    else:

        if game_music.get_num_channels() == 0:
            game_music.play()
        screen.blit(bg_image, (0, 0))
        camera_x = player.rect.x - SCREEN_WIDTH // 2
        camera_y = player.rect.y - SCREEN_HEIGHT // 2

        world.draw(screen, camera_x, camera_y)
        for enemy in world.get_group:
            enemy.update()
        player.update(world, screen, camera_x, camera_y)
        if player.on_portal_tile(world):
            transition_active = True
            transition_start_time = pygame.time.get_ticks()

        screen.blit(darken_surface, (0, 0))
        draw_level_counter(screen, level)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
