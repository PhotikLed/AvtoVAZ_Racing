import random

import pygame

pygame.init()
pygame.display.set_caption('АвтоВАЗ_Гонки')
screen = pygame.display.set_mode((1280, 720))

bg = pygame.image.load('spirities/trassa.png')  # фон


class Car(pygame.sprite.Sprite):
    image = pygame.image.load('spirities/2109.png')
    image = pygame.transform.scale(image, (200, 100))  # уменьшаем изображение

    def __init__(self, *group):
        super(Car, self).__init__(*group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.topleft = 1000, 210
        self.get_configurations()

    def get_configurations(self):
        # with open('configurations.txt', encoding='utf8') as conf:  # все что ниже будем брать из txt. пока затычка
        #     text = conf.readlines()

        self.turn_speed = 4  # скорость поворота
        self.max_speed = 100  # макс. скорость автомобиля
        self.coef_scep = 5  # коэффициент сцепления (про запас)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.y += self.turn_speed
        if keys[pygame.K_a]:
            self.rect.y -= self.turn_speed  # скорость поворота


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
