import pygame
import math
from config import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from pygame import mixer

# Load and scale images
pingu_front = pygame.image.load("images/pingu/pingu_idle.png")
pingu_front = pygame.transform.scale(pingu_front, (45, 45))
pingu_front_breathe = pygame.image.load("images/pingu/pingu_idle_stop.png")
pingu_front_breathe = pygame.transform.scale(pingu_front_breathe, (45, 45))
pingu_front_move_1 = pygame.image.load("images/pingu/pingu_move_1.png")
pingu_front_move_1 = pygame.transform.scale(pingu_front_move_1, (45, 45))
pingu_front_move_2 = pygame.image.load("images/pingu/pingu_move_2.png")
pingu_front_move_2 = pygame.transform.scale(pingu_front_move_2, (45, 45))
pingu_side_move_1 = pygame.image.load("images/pingu/pingu_move_side_1.png")
pingu_side_move_1 = pygame.transform.scale(pingu_side_move_1, (45, 45))
pingu_side_move_2 = pygame.image.load("images/pingu/pingu_move_side_2.png")
pingu_side_move_2 = pygame.transform.scale(pingu_side_move_2, (45, 45))
pingu_back_move_1 = pygame.image.load("images/pingu/pingu_move_back_1.png")
pingu_back_move_1 = pygame.transform.scale(pingu_back_move_1, (45, 45))
pingu_back_move_2 = pygame.image.load("images/pingu/pingu_move_back_2.png")
pingu_back_move_2 = pygame.transform.scale(pingu_back_move_2, (45, 45))


class Player:
    def __init__(self, x, y):
        self.index = 0
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        self.walk_music = pygame.mixer.Sound("music/gameplay/walk.mp3")
        self.walk_music.set_volume(1000.2)
        self.counter = 0
        self.direction = 0

        self.image = pingu_front
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0
        self.was_on_door_tile = False

        self.idle_images = [pingu_front, pingu_front_breathe]
        self.front_images = [pingu_front_move_1, pingu_front_move_2]
        self.back_images = [pingu_back_move_1, pingu_back_move_2]
        self.side_images = [pingu_side_move_1, pingu_side_move_2]

        self.idle_cooldown = 20  # Slower cooldown for idle animation
        self.walk_cooldown = 5  # Faster cooldown for walking animation

    def check_collision(self, dx, dy, world):
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy
        corners = [
            (new_rect.left, new_rect.top),
            (new_rect.right, new_rect.top),
            (new_rect.left, new_rect.bottom),
            (new_rect.right, new_rect.bottom),
        ]
        for corner in corners:
            if world.get_tile_at(*corner) == " ":
                return True
        return False

    def on_portal_tile(self, world):
        return world.get_tile_at(self.rect.centerx, self.rect.centery) == "P"

    def on_door_tile(self, world):
        return world.get_tile_at(self.rect.centerx, self.rect.centery) == "D"

    def stepped_off_door_tile(self, world):
        return world.get_tile_at(self.rect.centerx, self.rect.centery) != "D"

    def is_door_tile(self, world, x, y):
        tile = world.get_tile_at(x, y)
        return tile == "D"

    def update(self, world, screen, camera_x, camera_y):
        dx = 0
        dy = 0
        move_speed = 5

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if self.walk_music.get_num_channels() == 0:
                self.walk_music.play()
            dx -= move_speed
            self.direction = -1
        if key[pygame.K_RIGHT]:
            if self.walk_music.get_num_channels() == 0:
                self.walk_music.play()
            dx += move_speed
            self.direction = 1
        if key[pygame.K_UP]:
            if self.walk_music.get_num_channels() == 0:
                self.walk_music.play()
            dy -= move_speed
            self.direction = 2
        if key[pygame.K_DOWN]:
            if self.walk_music.get_num_channels() == 0:
                self.walk_music.play()
            dy += move_speed
            self.direction = 3

        if dx == 0 and dy == 0:
            self.counter += 1
            if self.counter > self.idle_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.idle_images)
                self.image = self.idle_images[self.index]
        else:
            self.counter += 1
            if self.counter > self.walk_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % 2
                if self.direction == 1:
                    self.image = self.side_images[self.index]
                elif self.direction == -1:
                    self.image = pygame.transform.flip(
                        self.side_images[self.index], True, False
                    )
                elif self.direction == 2:
                    self.image = self.back_images[self.index]
                elif self.direction == 3:
                    self.image = self.front_images[self.index]

        if not self.check_collision(dx, 0, world):
            self.rect.x += dx
        if not self.check_collision(0, dy, world):
            self.rect.y += dy

        if self.on_door_tile(world):
            world.open_door(
                self.rect.centerx // TILE_SIZE * TILE_SIZE,
                self.rect.centery // TILE_SIZE * TILE_SIZE,
            )
            self.was_on_door_tile = True
            self.x_door = self.rect.centerx // TILE_SIZE * TILE_SIZE
            self.y_door = self.rect.centery // TILE_SIZE * TILE_SIZE
        elif self.was_on_door_tile:
            world.close_door(self.x_door, self.y_door)
            self.was_on_door_tile = False

        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        # Draw vision mask after the player and world
