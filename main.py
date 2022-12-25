import random
import sys

import pygame

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
pygame.display.set_caption('АвтоВАЗ_Гонки')
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)

animation_road = [pygame.transform.scale(pygame.image.load(f'spirities/roads/road{i}.png'), size) for i in range(16)]


class Car(pygame.sprite.Sprite):
    score = 0

    def __init__(self, name, *group):
        super(Car, self).__init__(*group)
        self.image = pygame.image.load(f'spirities/tazy/{name}')
        self.image = pygame.transform.scale(self.image, (200, 100))  # уменьшаем изображение
        self.image = pygame.transform.rotate(self.image, 180)

        self.rect = self.image.get_rect()
        self.rect.topleft = 20, 205
        surf = pygame.Surface((self.image.get_width(), self.image.get_height()))
        print(self.image.get_width(), self.image.get_height())

        pygame.draw.ellipse(surf, 'white', (self.image.get_rect()))  # тут фигня с модернизированной коллизией
        self.mask = pygame.mask.from_surface(surf)

        self.get_configurations()

        self.gudok = pygame.mixer.Sound('sounds/avtomobilnyiy-gudok.mp3')  # гудок
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
        for trafs in traffic_sprites:
            if pygame.sprite.collide_mask(car, trafs):
                terminate()
        if pygame.sprite.groupcollide(main_sprites, traffic_sprites, True, False):
            sys.exit()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:  # добавил ограничения
            self.rect.y -= self.turn_speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < HEIGHT:
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
        self.rect = self.image.get_rect()
        surf = pygame.Surface((self.image.get_width(), self.image.get_height()))
        pygame.draw.ellipse(surf, 'white', (self.image.get_rect()))
        self.mask = pygame.mask.from_surface(surf)

        self.line = random.randint(0, 3)  # задание полосы
        self.set_position(self.line)

    def set_position(self, line):  # напраление и место появления в зависимости от полосы
        if line in [0, 1]:
            self.rect.topleft = WIDTH + 100, random.randint(10 + 180 * line, 70 + 180 * line)
        if line in [2, 3]:
            self.rect.topleft = WIDTH + 100, random.randint(390 + 180 * (line // 2 - 1), 610 + 180 * (line // 2 - 1))
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():  # менюшка
    intro_text = ["Если ты зачетный парень, если выглядишь атас,",
                  "то наверное ты знаешь что такое АвтоВАЗ.",
                  "",
                  "Выбери любимый автомобиль:"]

    fon = pygame.transform.scale(pygame.image.load('spirities/fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'gray', (0, 0, 1280, 240))
    text_coord = 10

    for line in intro_text:
        string_rendered = my_font.render(line, True, 'red')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    record = my_font.render('Ваш рекорд: ' + '1млн.', True, 'green')
    screen.blit(record, (1000, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(10, 1280) \
                        and y in range(100, 720):  # ты сюда пока не смотри, это заготовка под стрелочки выбора машинки.
                    # а пока тут перемычка
                    return '2109.png'
        pygame.display.flip()
        clock.tick(50)


traffic_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()

road_n = 0
road_speed = 4
traffic_speed = 5
clock = pygame.time.Clock()
fps = 60

timer_interval = 1000  # 1 seconds
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, timer_interval)

taz = start_screen()
car = Car(taz, main_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == timer_event:
            car.score += 1 + (road_speed - 4) / 10
            print(car.score)

    screen.blit(animation_road[road_n // 4], (0, 0))
    road_n = (road_n + road_speed) % 60

    main_sprites.draw(screen)
    main_sprites.update()

    traffic_sprites.draw(screen)
    traffic_sprites.update(traffic_speed)
    spawn_traffic(random.randint(0, 50))

    text_surface = my_font.render('Счёт: ' + str(int(car.score)), True, 'red')
    screen.blit(text_surface, (1150, 0))

    # print(road_speed)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
