import random
import sys

import pygame

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
big_font = pygame.font.SysFont('Comic Sans MS', 70)
pygame.display.set_caption('АвтоВАЗ_Гонки')
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)


class Car(pygame.sprite.Sprite):
    score = 0

    def __init__(self, name, *group):
        super(Car, self).__init__(*group)
        self.image = pygame.image.load(f'spirities/tazy/{name}')
        self.image = pygame.transform.scale(self.image, (200, 100))  # уменьшаем изображение
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        x1, y1, x2, y2 = self.image.get_rect()
        pygame.draw.rect(surf, 'white',
                         (x1 + 30, y1 + 30, x2 - 30, y2 - 30))  # тут фигня с модернизированной коллизией
        self.mask = pygame.mask.from_surface(surf)
        self.rect.topleft = 20, 400

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

        self.coef_scep = 5  # коэффициент сцепления (про запас)
        self.has_fco = True
        self.has_migalka = False
        self.has_nitro = True
        self.has_turbo = True

    def update(self):
        global traffic_speed, road_speed
        keys = pygame.key.get_pressed()
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

    def __init__(self, reverse, *groups):
        super(Traffic_car, self).__init__(*groups)
        self.reverse = reverse
        self.image = pygame.transform.rotate(Traffic_car.image, 180) if reverse else Traffic_car.image
        self.rect = self.image.get_rect()
        surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        x1, y1, x2, y2 = self.image.get_rect()
        pygame.draw.rect(surf, 'white', (x1 + 30, y1 + 30, x2 - 30, y2 - 30))
        self.mask = pygame.mask.from_surface(surf)

        self.set_position()

    def set_position(self):
        line = random.randint(0, 1)
        # while len(pygame.sprite.spritecollide(self, traffic_sprites, False)) > 1:
        if not self.reverse:
            self.rect.topleft = WIDTH + 100, random.randint(5 + 165 * line, 60 + 170 * line)
        else:
            self.rect.topleft = WIDTH + 100, random.randint(390 + 165 * line, 445 + 165 * line)

    def update(self, speed):
        for trafs in traffic_sprites:
            if pygame.sprite.collide_mask(trafs, car):  # не работает
                terminate()
        if not self.reverse:
            self.rect.x -= 15 + speed
        if self.reverse:
            self.rect.x -= speed

        if self.rect.right < 0:
            pygame.sprite.Sprite.kill(self)


def render_road(shift):  # отрисовка дороги
    road = pygame.surface.Surface(size)
    road.fill((90, 90, 90))
    pygame.draw.rect(road, 'white', (0, 338, 1280, 15))
    pygame.draw.rect(road, 'black', (0, 338, 1280, 15), 1)
    pygame.draw.rect(road, 'white', (0, 367, 1280, 15))
    pygame.draw.rect(road, 'black', (0, 367, 1280, 15), 1)
    for n in range(8):
        pygame.draw.rect(road, 'white', (200 * n - shift * road_speed, 162, 100, 15))
        pygame.draw.rect(road, 'black', (200 * n - shift * road_speed, 162, 100, 15), 1)

        pygame.draw.rect(road, 'white', (200 * n - shift * road_speed, 535, 100, 15))
        pygame.draw.rect(road, 'black', (200 * n - shift * road_speed, 535, 100, 15), 1)

    return road


def spawn_traffic(n):
    if n in [1, 2]:
        Traffic_car(0, traffic_sprites)  # встречка
    if n == 0:
        Traffic_car(1, traffic_sprites)  # поток


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
    start = big_font.render('Старт', True, 'white')

    strelka = pygame.image.load('spirities/knopki/yellow_strlelka.png')
    # right_button = pygame.transform.scale(strelka, (100, 20))
    right_button = strelka
    left_button = pygame.transform.rotate(right_button, 180)

    pygame.draw.rect(screen, 'red', (1000, 600, 1280, 720))
    screen.blit(start, (1040, 600))

    screen.blit(record, (1000, 50))
    screen.blit(right_button, (1050, 400))
    screen.blit(left_button, (30, 400))

    car = '2101.png'

    jiga01 = pygame.image.load('spirities/tazy/2101.png')
    jiga01 = pygame.transform.rotate(jiga01, 180)
    jiga01 = pygame.transform.scale(jiga01, (400, 200))

    jiga09 = pygame.image.load('spirities/tazy/2109.png')
    jiga09 = pygame.transform.rotate(jiga09, 180)
    jiga09 = pygame.transform.scale(jiga09, (200, 100))

    screen.blit(jiga01, (400, 400))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(1000, 1280) and \
                        y in range(600, 720):
                    return car

                if y in range(400, 550):
                    if x in range(1050, 1280):

                        car = '2109.png'
                    elif x in range(10, 310):
                        car = '2101.png'
        pygame.display.flip()
        clock.tick(fps)


traffic_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()

road_shift = 0
road_speed = 8
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
            car.score += 1 + (traffic_speed - 5) / 10
            print(car.score)

    screen.blit(render_road(road_shift), (0, 0))  # блит дороги
    road_shift = (road_shift + 1) % (200 / road_speed)

    main_sprites.draw(screen)
    main_sprites.update()

    traffic_sprites.draw(screen)
    traffic_sprites.update(traffic_speed)

    spawn_traffic(random.randint(0, 100 - traffic_speed))

    text_surface = my_font.render('Счёт: ' + str(int(car.score)), True, 'red')
    screen.blit(text_surface, (1150, 0))
    text_surface = my_font.render('Скорость: ' + str(traffic_speed), True, 'red')
    screen.blit(text_surface, (0, 0))

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
