import pygame
from enemy import Enemy

tile_size = 50

brick = pygame.image.load("brick.png")
brick = pygame.transform.scale(brick, (tile_size, tile_size))
frame = pygame.image.load("frame.png")
frame = pygame.transform.scale(frame, (tile_size, tile_size))


class World:
    def __init__(self, data):
        self.world_data = data
        self.tile_list = []
        self.starting_position = (0, 0)
        self.cobra_group = pygame.sprite.Group()
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "E":  # Entrance tile
                    self.starting_position = (
                        col_count * tile_size,
                        row_count * tile_size,
                    )
                if tile == "R":  # Room tile
                    img = brick
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == ".":  # Corridor tile
                    img = frame
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                # elif tile == "3":  # Enemy tile
                #     enemy = Enemy(col_count * tile_size, row_count * tile_size)
                #     self.cobra_group.add(enemy)
                elif tile == "D":
                    # Create a red surface for "D" tiles
                    red_img = pygame.Surface((tile_size, tile_size))
                    red_img.fill((255, 0, 0))  # Fill surface with red color
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (red_img, img_rect)
                    self.tile_list.append(tile)
                elif tile == "E":
                    # Create a red surface for "D" tiles
                    red_img = pygame.Surface((tile_size, tile_size))
                    # yellow
                    red_img.fill((255, 255, 0))
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (red_img, img_rect)
                    self.tile_list.append(tile)
                elif tile == "P":
                    # Create a red surface for "D" tiles
                    red_img = pygame.Surface((tile_size, tile_size))
                    # blue
                    red_img.fill((0, 0, 255))
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (red_img, img_rect)
                    self.tile_list.append(tile)
                elif tile == " ":
                    red_img = pygame.Surface((tile_size, tile_size))
                    # blue
                    red_img.fill((255, 255, 255))
                    img_rect = red_img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
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
            return self.world_data[y // tile_size][x // tile_size]
        except IndexError:
            return " "

    @property
    def get_group(self):
        return self.cobra_group

    @property
    def get_starting_position(self):
        return self.starting_position
