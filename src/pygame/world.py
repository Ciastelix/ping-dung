import pygame
from enemy import Enemy
from config import TILE_SIZE
import numpy as np

brick = pygame.image.load("brick.png")
brick = pygame.transform.scale(brick, (TILE_SIZE, TILE_SIZE))
brick = pygame.transform.rotate(brick, 90)
stairs = pygame.image.load("stairs.png")
stairs = pygame.transform.scale(stairs, (TILE_SIZE, TILE_SIZE))
door = pygame.image.load("door.png")
door = pygame.transform.scale(door, (TILE_SIZE, TILE_SIZE))
opened_door = pygame.image.load("opened_door.png")
opened_door = pygame.transform.scale(opened_door, (TILE_SIZE, TILE_SIZE))

frame = pygame.image.load("frame.png")
black_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
black_img.fill((0, 0, 0))

RAYCASTING_DISTANCE = 1  # Increase to show more tiles
NUM_RAYS = 10000


class World:
    def __init__(self, data):
        self.world_data = data
        self.tile_list = []
        self.empty_tiles = []  # List to store empty tiles
        self.starting_position = (0, 0)
        self.cobra_group = pygame.sprite.Group()
        self.rooms_and_corridors = []  # List to store room and corridor positions

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "E":
                    self.starting_position = (
                        col_count * TILE_SIZE,
                        row_count * TILE_SIZE,
                    )
                if tile == "R":
                    img = brick
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.rooms_and_corridors.append(
                        (img_rect.x, img_rect.y)
                    )  # Add room position to list
                elif tile == ".":
                    img = frame
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.rooms_and_corridors.append(
                        (img_rect.x, img_rect.y)
                    )  # Add corridor position to list
                elif tile == "D":
                    img_rect = door.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (door, img_rect)
                    self.tile_list.append(tile)
                elif tile == "E":
                    img_rect = stairs.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (stairs, img_rect)
                    self.tile_list.append(tile)
                elif tile == "P":
                    img_rect = stairs.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (stairs, img_rect)
                    self.tile_list.append(tile)
                elif tile == " ":
                    self.empty_tiles.append((col_count, row_count))

                col_count += 1
            row_count += 1

    def draw(self, screen, camera_x, camera_y, player):
        screen.fill((0, 0, 0))
        visible_tiles = self.get_visible_tiles(player)

        # Draw all tiles except empty tiles
        for tile in self.tile_list:
            tile_x, tile_y = tile[1].x // TILE_SIZE, tile[1].y // TILE_SIZE
            if (tile_x, tile_y) in visible_tiles:
                screen.blit(tile[0], (tile[1].x - camera_x, tile[1].y - camera_y))
            else:
                # Render non-visible tiles as black
                img_rect = black_img.get_rect()
                img_rect.x = tile[1].x
                img_rect.y = tile[1].y
                screen.blit(black_img, (img_rect.x - camera_x, img_rect.y - camera_y))

        # Draw player
        player.update(self, screen, camera_x, camera_y)

        # Draw empty tiles as black
        for col_count, row_count in self.empty_tiles:
            if (col_count, row_count) not in visible_tiles:
                img_rect = black_img.get_rect()
                img_rect.x = col_count * TILE_SIZE
                img_rect.y = row_count * TILE_SIZE
                screen.blit(black_img, (img_rect.x - camera_x, img_rect.y - camera_y))

        # Draw enemies
        for enemy in self.cobra_group:
            enemy.draw(screen, camera_x, camera_y)

    def get_tile_at(self, x, y):
        try:
            return self.world_data[y // TILE_SIZE][x // TILE_SIZE]
        except IndexError:
            return " "

    def open_door(self, x, y):
        for i, tile in enumerate(self.tile_list):
            if tile[1].x == x and tile[1].y == y and tile[0] == door:
                self.tile_list[i] = (opened_door, tile[1])
                break

    def close_door(self, x, y):
        for i, tile in enumerate(self.tile_list):
            if tile[1].x == x and tile[1].y == y and tile[0] == opened_door:
                self.tile_list[i] = (door, tile[1])
                break

    @property
    def get_group(self):
        return self.cobra_group

    @property
    def get_starting_position(self):
        return self.starting_position

    def get_valid_enemy_positions(self):
        return self.rooms_and_corridors

    def spawn_enemy(self, position):
        pass

    def get_visible_tiles(self, player):
        player_x, player_y = player.rect.x // TILE_SIZE, player.rect.y // TILE_SIZE
        visible_tiles = set()

        for dx in range(-RAYCASTING_DISTANCE, RAYCASTING_DISTANCE + 1):
            for dy in range(-RAYCASTING_DISTANCE, RAYCASTING_DISTANCE + 1):
                target_x = player_x + dx
                target_y = player_y + dy

                if 0 <= target_x < len(self.world_data[0]) and 0 <= target_y < len(
                    self.world_data
                ):
                    line_of_sight = self.bresenham_line(
                        player_x, player_y, target_x, target_y
                    )
                    visible = True
                    for lx, ly in line_of_sight:
                        if self.world_data[ly][lx] == " ":
                            visible = False
                            break
                    if visible:
                        visible_tiles.add((target_x, target_y))

        return visible_tiles

    def bresenham_line(self, x0, y0, x1, y1):
        """Bresenham's Line Algorithm to get the points on a line between two points."""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

        return points
