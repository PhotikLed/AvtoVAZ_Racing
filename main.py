import random

import pygame

pygame.init()
pygame.display.set_caption('АвтоВАЗ_Гонки')
screen = pygame.display.set_mode((1280, 720))
bg = pygame.image.load('spirities/trassa.png')


class Car(pygame.sprite.Sprite):
    image = pygame.image.load('spirities/2101.png')
    image = pygame.transform.scale(image, (200, 100))

    def __init__(self, *group):
        super(Car, self).__init__(*group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.topleft = 1000, 210

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.y += 3
        if keys[pygame.K_a]:
            self.rect.y -= 3


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
car = Car(all_sprites)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
