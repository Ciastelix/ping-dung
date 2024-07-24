import pygame
from enemy import Enemy

tile_size = 50


class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load("frame.png")
        grass_img = pygame.image.load("brick.png")
        self.cobra_group = pygame.sprite.Group()
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    self.cobra_group.add(enemy)
                col_count += 1
            row_count += 1

    def draw(self, screen, camera_x, camera_y):
        for tile in self.tile_list:
            screen.blit(tile[0], (tile[1].x - camera_x, tile[1].y - camera_y))
        for enemy in self.cobra_group:
            enemy.draw(screen, camera_x, camera_y)

    @property
    def get_group(self):
        return self.cobra_group
