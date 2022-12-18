import random

import pygame

pygame.init()
pygame.display.set_caption('АвтоВАЗ_Гонки')
screen = pygame.display.set_mode((1280, 720))

bg = pygame.image.load('spirities/trassa.png')  # фон


class Car(pygame.sprite.Sprite):
    image = pygame.image.load('spirities/2109.png')
    image = pygame.transform.scale(image, (200, 100))  # уменьшаем изображение
    image = pygame.transform.rotate(image, 180)

    def __init__(self, *group):
        super(Car, self).__init__(*group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.topleft = 20, 205
        self.get_configurations()
        self.gudok = pygame.mixer.Sound('sounds/avtomobilnyiy-gudok.mp3')
        self.gudok.set_volume(0.1)
        pygame.mixer.music.load('TazMusic/yakuba.mp3')

    def get_configurations(self):
        # with open('configurations.txt', encoding='utf8') as conf:  # все что ниже будем брать из txt. пока затычка
        #     text = conf.readlines()

        self.turn_speed = 4  # скорость поворота
        self.max_speed = 100  # макс. скорость автомобиля
        self.coef_scep = 5  # коэффициент сцепления (про запас)
        self.has_fco = True
        self.has_migalka = False
        self.has_nitro = True
        self.has_turbo = True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.y += self.turn_speed
        if keys[pygame.K_a]:
            self.rect.y -= self.turn_speed  # скорость поворота
        if keys[pygame.K_b]:  # бибикалка
            self.gudok.play()


class Traffic_car(pygame.sprite.Sprite):
    image = pygame.image.load('traffic_spirities/traf1.png')
    image = pygame.transform.scale(image, (200, 100))
    image = pygame.transform.rotate(image, 180)

    def __init__(self, *groups):
        super(Traffic_car, self).__init__(*groups)
        self.image = Traffic_car.image
        self.rect = self.image.get_rect()
        self.rect.topleft = random.randint(900, 1100), random.randint(10, 545)

    def update(self, current_speed):
        self.rect.x -= 3


traffic_sprites = pygame.sprite.Group()
for i in range(5):
    Traffic_car(traffic_sprites)

main_sprites = pygame.sprite.Group()
car = Car(main_sprites)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg, (0, 0))

    main_sprites.draw(screen)
    main_sprites.update()

    traffic_sprites.draw(screen)
    traffic_sprites.update(10)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
