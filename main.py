import random
import sys

import pygame

pygame.init()
pygame.display.set_caption('АвтоВАЗ_Гонки')
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

animation_road = [pygame.transform.scale(pygame.image.load(f'spirities/roads/road{i}.png'), size) for i in range(16)]


class Car(pygame.sprite.Sprite):
    image = pygame.image.load('spirities/2109.png')
    image = pygame.transform.scale(image, (200, 100))  # уменьшаем изображение
    image = pygame.transform.rotate(image, 180)

    score = 0
    def __init__(self, *group):
        super(Car, self).__init__(*group)
        self.image = Car.image

        self.rect = self.image.get_rect()
        self.rect.topleft = 20, 205
        self.mask = pygame.mask.from_surface(self.image)

        self.get_configurations()

        self.gudok = pygame.mixer.Sound('sounds/avtomobilnyiy-gudok.mp3')
        self.gudok.set_volume(0.1)
        pygame.mixer.music.load('TazMusic/yakuba.mp3')

    def get_configurations(self):
        # with open('configurations.txt', encoding='utf8') as conf:  # все что ниже будем брать из txt. пока затычка
        #     text = conf.readlines()

        self.turn_speed = 5  # скорость поворота
        self.max_speed = 50  # макс. скорость автомобиля
        self.min_speed = 5
        self.current_speed = 5

        self.coef_scep = 5  # коэффициент сцепления (про запас)
        self.has_fco = True
        self.has_migalka = False
        self.has_nitro = True
        self.has_turbo = True

    def update(self):
        global traffic_speed, road_speed
        keys = pygame.key.get_pressed()
        if pygame.sprite.groupcollide(main_sprites, traffic_sprites, True, False):
            sys.exit()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:  # добавил ограничения
            self.rect.y -= self.turn_speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < height:
            self.rect.y += self.turn_speed  # скорость поворота
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # скорость машины (пока без ограничений)
            if traffic_speed < self.max_speed:
                traffic_speed += 1
                road_speed += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if traffic_speed > self.min_speed:
                traffic_speed -= 1
                road_speed -= 1
        if keys[pygame.K_b]:  # бибикалка
            self.gudok.play()


class Traffic_car(pygame.sprite.Sprite):
    image = pygame.image.load('traffic_spirities/traf1.png')
    image = pygame.transform.scale(image, (200, 100))

    def __init__(self, *groups):
        super(Traffic_car, self).__init__(*groups)
        self.image = Traffic_car.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.line = random.randint(0, 3)  # задание полосы
        self.set_position(self.line)

    def set_position(self, line):  # напраление и место появления в зависимости от полосы
        if line in [0, 1]:
            self.rect.topleft = width + 100, random.randint(10 + 180 * line, 70 + 180 * line)
        if line in [2, 3]:
            self.rect.topleft = width + 100, random.randint(390 + 180 * (line // 2 - 1), 610 + 180 * (line // 2 - 1))
            self.image = pygame.transform.rotate(self.image, 180)

    def update(self, speed):
        if self.line in [0, 1]:
            self.rect.x -= 15 + speed
        if self.line in [2, 3]:
            self.rect.x -= speed

        if self.rect.right < 0:
            pygame.sprite.Sprite.kill(self)


def spawn_traffic(n):  # спавнится машина, если выпадет карта
    if n == 0:
        Traffic_car(traffic_sprites)


traffic_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()
car = Car(main_sprites)

road_n = 0
road_speed = 4
traffic_speed = 5
clock = pygame.time.Clock()
fps = 60

timer_interval = 1000  # 1 seconds
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, timer_interval)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == timer_event:
            car.score += 1
            print(car.score)

    screen.blit(animation_road[road_n // 4], (0, 0))
    road_n = (road_n + road_speed) % 60

    main_sprites.draw(screen)
    main_sprites.update()

    traffic_sprites.draw(screen)
    traffic_sprites.update(traffic_speed)
    spawn_traffic(random.randint(0, 50))

    # print(road_speed)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
