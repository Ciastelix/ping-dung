import pygame
from enemy import Enemy
from config import TILE_SIZE

brick = pygame.image.load("brick.png")
brick = pygame.transform.scale(brick, (TILE_SIZE, TILE_SIZE))
frame = pygame.image.load("frame.png")
frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))


class World:
    def __init__(self, data):
        self.world_data = data
        self.tile_list = []
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
                    red_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    red_img.fill((255, 0, 0))
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (red_img, img_rect)
                    self.tile_list.append(tile)
                elif tile == "E":
                    red_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    red_img.fill((255, 255, 0))
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (red_img, img_rect)
                    self.tile_list.append(tile)
                elif tile == "P":
                    red_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    red_img.fill((0, 0, 255))
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (red_img, img_rect)
                    self.tile_list.append(tile)
                elif tile == " ":
                    red_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    red_img.fill((255, 255, 255))
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (red_img, img_rect)
                    self.tile_list.append(tile)

                col_count += 1
            row_count += 1

    def draw(self, screen, camera_x, camera_y):
        for tile in self.tile_list:
            screen.blit(tile[0], (tile[1].x - camera_x, tile[1].y - camera_y))
        for enemy in self.cobra_group:
            enemy.draw(screen, camera_x, camera_y)

    def get_tile_at(self, x, y):
        try:
            return self.world_data[y // TILE_SIZE][x // TILE_SIZE]
        except IndexError:
            return " "

    @property
    def get_group(self):
        return self.cobra_group

    @property
    def get_starting_position(self):
        return self.starting_position

    def get_valid_enemy_positions(self):
        return self.rooms_and_corridors

    def spawn_enemy(self, position):
        enemy_x, enemy_y = position
        enemy = Enemy(enemy_x, enemy_y)
        self.cobra_group.add(enemy)
