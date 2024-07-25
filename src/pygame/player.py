import pygame
from PIL import Image, ImageSequence
from config import SCREEN_HEIGHT, SCREEN_WIDTH


def gif_to_frames(filename):
    with Image.open(filename) as gif:
        frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    pygame_frames = []
    for frame in frames:
        frame_pygame = pygame.image.fromstring(
            frame.tobytes(), frame.size, frame.mode
        ).convert_alpha()
        pygame_frames.append(frame_pygame)
    return pygame_frames


class Player:
    def __init__(self, x, y):
        self.vision_mask = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        images = gif_to_frames("doux.gif")
        self.index = 0
        self.counter = 0
        self.images_right = []
        self.images_left = []
        self.direction = 0
        for i in range(1, 11):
            img_right = images[i]
            img_right = pygame.transform.scale(img_right, (40, 45))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_x = 0
        self.vel_y = 0
        self.direction = 0

    def check_collision(self, dx, dy, world):
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy
        # Check all four corners
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

    def update(self, world, screen, camera_x, camera_y):
        dx = 0
        dy = 0
        move_speed = 5
        walk_cooldown = 5

        # Get key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= move_speed
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += move_speed
            self.direction = 1
        if key[pygame.K_UP]:
            dy -= move_speed
        if key[pygame.K_DOWN]:
            dy += move_speed

        # Handle animation
        if dx != 0 or dy != 0:  # Update animation if moving
            self.counter += 1
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
        else:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # Check collisions and update position
        if not self.check_collision(dx, 0, world):
            self.rect.x += dx
        if not self.check_collision(0, dy, world):
            self.rect.y += dy

        # Draw player onto screen with camera offset
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        self.vision_mask.fill((0, 0, 0, 128))  # Semi-transparent fill
        pygame.draw.circle(
            self.vision_mask,
            (0, 0, 0, 0),
            (self.rect.x - camera_x + 20, self.rect.y - camera_y + 20),
            100,
        )  # Transparent circle
        screen.blit(self.vision_mask, (0, 0))
