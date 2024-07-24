import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Simplified initialization
        self.images = []
        self.counter = 1
        self.step = 0
        for i in range(1, 5):
            image = pygame.image.load(f"cobra_{i}.png")
            image = pygame.transform.scale(image, (30, 50))
            if i == 1:  # Initialize rect only once
                self.rect = image.get_rect(x=x, y=y)
            self.images.append(image)
        self.image = self.images[0]  # Set initial image

    def update(self):
        # Animation logic
        self.step += 1
        if self.step >= 10:
            self.step = 0
            self.counter += 1
            if self.counter >= len(self.images):
                self.counter = 0
            self.image = self.images[self.counter]

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
