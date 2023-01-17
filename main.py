import random
import sys
import sqlite3
import time
import pygame

from database_work import *
from dialogs import *

pygame.init()
pygame.font.init()
small_font = pygame.font.SysFont('Comic Sans MS', 20)
my_font = pygame.font.SysFont('Comic Sans MS', 30)
middle_font = pygame.font.SysFont('Comic Sans MS', 35)
big_font = pygame.font.SysFont('Comic Sans MS', 70)
vaz_font = pygame.font.SysFont('Impact', 50)
pygame.display.set_caption('АвтоВАЗ_Гонки')
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)


class Car(pygame.sprite.Sprite):
    # score = 0

    def __init__(self, name: str, *group):
        super(Car, self).__init__(*group)
        self.score = 0
        self.name = name.split('.')[0]

        self.image = pygame.image.load(f'spirities/tazy/{name}')
        self.image = pygame.transform.scale(self.image, (200, 100))  # уменьшаем изображение
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        x1, y1, x2, y2 = self.image.get_rect()
        pygame.draw.rect(surf, 'white',
                         (x1 + 25, y1 + 25, x2 - 25, y2 - 25))  # тут фигня с модернизированной коллизией
        self.mask = pygame.mask.from_surface(surf)
        self.rect.topleft = 20, 400

        self.get_configurations(name.split('.')[0])

        self.gudok = pygame.mixer.Sound('sounds/avtomobilnyiy-gudok.mp3')  # гудок
        self.gudok.set_volume(0.1)
        pygame.mixer.music.load('TazMusic/yakuba.mp3')

    def get_configurations(self, name):  # узнаем характеристики автомобиля

        params = get_tuning_by_name(name)

        self.coef_scep = params[1]  # коэффициент сцепления (про запас)

        self.has_fco = params[2]
        self.has_migalka = params[3]
        self.has_nitro = params[4]
        self.has_turbo = params[5]

        self.turn_speed = params[6]  # скорость поворота
        self.min_speed = params[7]
        self.max_speed = params[8]  # макс. скорость автомобиля
        self.glohnet = params[9]

    def update(self):
        # global traffic_speed, road_speed
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:  # добавил ограничения
            self.rect.y -= self.turn_speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < HEIGHT:
            self.rect.y += self.turn_speed  # скорость поворота
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # скорость машины
            if screener.traffic_speed < self.max_speed:
                screener.traffic_speed += 1
                screener.road_speed += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if screener.traffic_speed > self.min_speed:
                screener.traffic_speed -= 1
                screener.road_speed -= 1
        if keys[pygame.K_b]:  # бибикалка
            self.gudok.play()
        if keys[pygame.K_z]:
            Screens().end_screen()


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
        pygame.draw.rect(surf, 'white', (x1 + 25, y1 + 25, x2 - 25, y2 - 25))
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
            # коллизия
            if pygame.sprite.collide_mask(trafs, car):
                save_record_and_money(car.score)
                Screens().end_screen()
                terminate()
        if not self.reverse:
            self.rect.x -= 15 + speed
        if self.reverse:
            self.rect.x -= speed

        if self.rect.right < 0:
            pygame.sprite.Sprite.kill(self)


def spawn_traffic(n):
    if n in [1, 2]:
        Traffic_car(0, traffic_sprites)  # встречка
    if n == 0:
        Traffic_car(1, traffic_sprites)  # поток


def get_balance():  # узнаем текущий баланс
    with open('sysparams/money.txt', encoding='utf8') as balans:
        balans = balans.readline()
        return balans


def get_record():  # узнаем текущий рекорд
    with open('sysparams/record.txt', encoding='utf-8') as record:
        record = record.readline()
        return record


def save_record_and_money(rec):  # сохраняем рекорд и плюсуем деньги
    with open('sysparams/record.txt', encoding='utf-8') as shet:
        shet = int(float(shet.readline()))
        rec = int(float(rec))
    if shet < rec:
        with open('sysparams/record.txt', encoding='utf-8', mode='w+') as new_record:
            new_record.write(str(rec))

    cur_money = get_balance()
    with open('sysparams/money.txt', encoding='utf-8', mode='w+') as new_money:
        new_money.write(str(int(cur_money) + rec))


def update_balance():
    cur_balance = get_balance()
    balance = my_font.render('Ваш баланс: ' + cur_balance + '$', True, 'gold')

    pygame.draw.rect(screen, 'black', (0, 40, 480, 50))
    screen.blit(balance, (1, 40))


def draw_characteristik(tunings: list, index):  # рисуем характеристики автомобиля в основном окошке
    pygame.draw.rect(screen, 'black', (840, 0, 520, 335))

    caracteristik = my_font.render("Характеристики автомобиля:", True, 'red')
    screen.blit(caracteristik, (850, 0))

    upgrade_button = pygame.image.load('spirities/knopki/upgrade.png')
    upgrade_button = pygame.transform.scale(upgrade_button, (30, 30))

    rus_bool = {0: 'Нет',
                1: 'Да'}

    params_text = ["Коэф. сцепления",
                   "Вспышки ФСО",
                   "Мигалки",
                   "Нитро",
                   "Турбина",
                   "Скорость поворота",
                   "Мин. скорость",
                   "Макс. скорость",
                   "Глохнет"]

    text_coord = 35
    for i in range(len(tunings[index]) - 1):
        if tunings[index][i + 1] <= 1:
            string_rendered = small_font.render(params_text[i] + ': ' + rus_bool[tunings[index][i + 1]], True, 'white')
        else:
            string_rendered = small_font.render(params_text[i] + ': ' + str(tunings[index][i + 1]), True, 'white')
        intro_rect = string_rendered.get_rect()
        text_coord += 3
        intro_rect.top = text_coord
        intro_rect.x = 850
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        screen.blit(upgrade_button, (1060, text_coord - 30))


def terminate():
    pygame.quit()
    sys.exit()


class Screens:

    def __init__(self):
        self.car_name = '2101'

        self.road_shift = 0
        self.road_speed = 8
        self.traffic_speed = 5
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.timer_interval = 1000  # 1 seconds
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, self.timer_interval)

        self.upgrade_buttons = [
            'coef_scpleniya',
            'fco',
            'police_lights',
            'nitro',
            'turbo',
            'turn_speed',
            'min_speed',
            'max_speed',
            'glohnet',
            'glohnet'
        ]

    def render_road(self, shift):  # отрисовка дороги
        road = pygame.surface.Surface(size)
        road.fill((90, 90, 90))
        pygame.draw.rect(road, 'white', (0, 338, 1280, 15))
        pygame.draw.rect(road, 'black', (0, 338, 1280, 15), 1)
        pygame.draw.rect(road, 'white', (0, 367, 1280, 15))
        pygame.draw.rect(road, 'black', (0, 367, 1280, 15), 1)
        for n in range(8):
            pygame.draw.rect(road, 'white', (200 * n - shift * self.road_speed, 162, 100, 15))
            pygame.draw.rect(road, 'black', (200 * n - shift * self.road_speed, 162, 100, 15), 1)

            pygame.draw.rect(road, 'white', (200 * n - shift * self.road_speed, 535, 100, 15))
            pygame.draw.rect(road, 'black', (200 * n - shift * self.road_speed, 535, 100, 15), 1)

        return road

    def start_screen(self):  # стартовое окошко

        fon = pygame.transform.scale(pygame.image.load('spirities/fon.png'), (WIDTH, HEIGHT))  # делаем фон
        screen.blit(fon, (0, 0))

        car_filename = '2101.png'

        cur_balance = get_balance()
        record = my_font.render('Ваш рекорд: ' + get_record(), True, 'green')  # всякий текст
        balance = my_font.render('Ваш баланс: ' + cur_balance + '$', True, 'gold')

        start = big_font.render('Старт', True, 'white')
        buy = big_font.render('Купить', True, 'white')

        right_button = strelka = pygame.image.load('spirities/knopki/yellow_strlelka.png')  # стрелочки
        left_button = pygame.transform.rotate(strelka, 180)

        pygame.draw.rect(screen, 'red', (1000, 600, 1280, 720))  # кнопка старт
        screen.blit(start, (1040, 600))

        beton = pygame.image.load('spirities/roads/beton.png')  # то, но чем стоит таз
        beton = pygame.transform.scale(beton, (450, 300))
        screen.blit(beton, (410, 345))

        pygame.draw.rect(screen, 'black', (0, 0, 480, 90))  # менюшка с балансом и т.д.
        screen.blit(record, (1, 0))
        screen.blit(balance, (1, 40))

        screen.blit(right_button, (1050, 400))
        screen.blit(left_button, (30, 400))

        jiga01 = pygame.image.load('spirities/tazy/2101.png')  # рендерим жиги
        jiga01 = pygame.transform.rotate(jiga01, 180)
        jiga01 = pygame.transform.scale(jiga01, (400, 200))

        jiga09 = pygame.image.load('spirities/tazy/2109.png')
        jiga09 = pygame.transform.rotate(jiga09, 180)
        jiga09 = pygame.transform.scale(jiga09, (400, 200))

        priora = pygame.image.load('spirities/tazy/priora.png')
        priora = pygame.transform.rotate(priora, 180)
        priora = pygame.transform.scale(priora, (400, 200))

        cars = [jiga01, jiga09, priora]
        names_cars = ['2101.png', '2109.png', 'priora.png']
        real_name_cars = ['2101', '2109', 'priora']
        blits_cars = [vaz_font.render(n.split('.')[0].capitalize(), True, 'orange') for n in names_cars]
        index = 0

        tunings = get_tuning()
        draw_characteristik(tunings, index)

        screen.blit(jiga01, (435, 400))
        screen.blit(blits_cars[index], (480, 345))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in range(1000, 1280) and \
                            y in range(600, 720):
                        if has_bought(self.car_name):
                            return car_filename  # старт игры
                        else:
                            price = get_cost(self.car_name)  # покупка автомобиля
                            if price <= int(cur_balance):
                                with open('sysparams/money.txt', encoding='utf-8', mode='w+') as balance:
                                    balance.write(str(int(cur_balance) - price))
                                set_bought(self.car_name)

                                update_balance()

                                pygame.draw.rect(screen, 'red', (1000, 600, 1280, 720))
                                screen.blit(start, (1040, 600))

                    if y in range(400, 550):  # листание машинок
                        if x in range(1050, 1280):
                            index = (index + 1) % 3
                        elif x in range(10, 310):
                            index = abs((index - 1) % 3)
                        screen.blit(beton, (410, 345))
                        screen.blit(cars[index], (435, 400))
                        screen.blit(blits_cars[index], (480, 345))
                        car_filename = names_cars[index]
                        self.car_name = real_name_cars[index]
                        draw_characteristik(tunings, index)

                        pygame.draw.rect(screen, 'red', (1000, 600, 1280, 720))  # отрисовка кнопки Старт\Купить
                        if has_bought(self.car_name):
                            screen.blit(start, (1040, 600))
                        else:
                            screen.blit(buy, (1020, 600))

                            cena = small_font.render(str(get_cost(self.car_name)) + '$', True, 'gold')
                            screen.blit(cena, (1100, 690))

                    if x in range(1060, 1090):  # кнопки тюнинга
                        if y in range(35, 320):
                            tuning_dialog(self.upgrade_buttons[(y - 35) // 30], self.car_name)

            pygame.display.flip()
            self.clock.tick(self.fps)

    def game_screen(self):  # сам геймплей
        running_game = True
        while running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_record_and_money(car.score)
                    terminate()
                if event.type == self.timer_event:
                    car.score += 1 + (self.traffic_speed - 5) / 10
                    # print(car.score)

            screen.blit(self.render_road(self.road_shift), (0, 0))  # блит дороги
            self.road_shift = (self.road_shift + 1) % (200 / self.road_speed)

            main_sprites.draw(screen)
            main_sprites.update()

            traffic_sprites.draw(screen)
            traffic_sprites.update(self.traffic_speed)

            spawn_traffic(random.randint(0, 100 - self.traffic_speed))

            text_surface = my_font.render('Счёт: ' + str(int(car.score)), True, 'red')
            screen.blit(text_surface, (1150, 0))
            text_surface = my_font.render('Скорость: ' + str(self.traffic_speed), True, 'red')
            screen.blit(text_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(self.fps)

        save_record_and_money(car.score)
        screener.end_screen()

    def end_screen(self):  # финальное окно
        for sprite in traffic_sprites:
            if isinstance(sprite, Traffic_car):
                sprite.kill()
        time.sleep(0.4)
        fon = pygame.transform.scale(pygame.image.load('spirities/gai.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        zanovo = my_font.render('Начать заново', True, 'white')
        menu = my_font.render('Выйти в меню', True, 'white')
        vyhod = my_font.render('Выйти из игры', True, 'white')

        pygame.draw.rect(screen, 'black', (500, 300, 218, 50))
        pygame.draw.rect(screen, 'black', (500, 360, 218, 50))
        pygame.draw.rect(screen, 'black', (500, 420, 218, 50))

        screen.blit(zanovo, (500, 300))
        screen.blit(menu, (500, 360))
        screen.blit(vyhod, (500, 420))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if x in range(500, 718):
                        if y in range(300, 350):
                            self.game_screen()  # вот тут не понимаю как сделать чтобы всё заново начиналось
                        elif y in range(360, 410):
                            start()

                            # и тут тоже никак не пойму

                        elif y in range(420, 470):
                            terminate()

            pygame.display.flip()
            self.clock.tick(self.fps)


def start():
    traffic_sprites = pygame.sprite.Group()
    main_sprites = pygame.sprite.Group()

    screener = Screens()

    taz = screener.start_screen()
    car = Car(taz, main_sprites)
    screener.game_screen()


if __name__ == '__main__':
    traffic_sprites = pygame.sprite.Group()
    main_sprites = pygame.sprite.Group()

    screener = Screens()

    taz = screener.start_screen()
    car = Car(taz, main_sprites)
    screener.game_screen()
