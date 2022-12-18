import random
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
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:  # добавил ограничения
            self.rect.y -= self.turn_speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < height:
            self.rect.y += self.turn_speed  # скорость поворота
        if keys[pygame.K_b]:  # бибикалка
            self.gudok.play()


class Traffic_car(pygame.sprite.Sprite):
    image = pygame.image.load('traffic_spirities/traf1.png')
    image = pygame.transform.scale(image, (200, 100))

    def __init__(self, *groups):
        super(Traffic_car, self).__init__(*groups)
        self.image = Traffic_car.image
        self.rect = self.image.get_rect()
        self.line = random.randint(0, 3)  # задание полосы
        self.set_position(self.line)

    def set_position(self, line):  # напраление и место появления в зависимости от полосы
        if line in [0, 1]:
            self.rect.topleft = width + 100, random.randint(10 + 180 * line, 70 + 180 * line)
        if line in [2, 3]:
            self.rect.topleft = width + 100, random.randint(390 + 180 * (line // 2 - 1), 610 + 180 * (line // 2 - 1))
            self.image = pygame.transform.rotate(self.image, 180)

    def update(self, current_speed):
        if self.line in [0, 1]:
            self.rect.x -= 15
        if self.line in [2, 3]:
            self.rect.x -= 3

        if self.rect.right < 0:
            pygame.sprite.Sprite.kill(self)


def spawn_traffic(n):  # спавнится машина, если выпадет карта
    if n == 0:
        Traffic_car(traffic_sprites)


traffic_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()
car = Car(main_sprites)

road_n = 0
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(animation_road[road_n // 4], (0, 0))
    road_n += 1
    road_n = (road_n + 1) % 60

    main_sprites.draw(screen)
    main_sprites.update()

    traffic_sprites.draw(screen)
    traffic_sprites.update(10)
    spawn_traffic(random.randint(0, 100))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
