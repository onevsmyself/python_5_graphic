# Выполнил Давидовский Кирилл Группа ИУ7-24Б
# Нужно было придумать и реализовать с использованием
# библиотеки pygame циклическую анимацию с сюжетом


from pygame import *
from random import randint
from math import sin, cos, radians
import sys

from funcs import *

clock = time.Clock()


# Цвета
GREY = 125, 125, 125
BIRD = 0, 0, 0
SKIN = 127, 42, 42
SKIN_DARK = 90, 30, 30
SUN = 255, 226, 0
SKY = 127, 199, 255
SKY_N = 0, 0, 153
BIRD_N = 153, 255, 153

# Скорость анимации
FPS = 45

# Дисплей
size = width, height = 1000, 600
screen = display.set_mode(size)
display.set_caption('Время на природе')

# Координаты человеческого центра
man = {'x': 500, 'y': 200}

# Состояние дня/ночи
is_day = True

# Птицы
st_angle = 35
birds_count = 0
birds_limit = 10
birds = [{'here': False, 'x': 0, 'y': 0, 'size': 20, 'speed': 0,
          'fly': st_angle, 'direction': 1, 'k': 1} for i in range(birds_limit)]
spawn_r_s, spawn_r_f = 50, 250
size_r_s, size_r_f = 20, 35


# функция для прорисовки человека
def human(x, y, status):
    MY_SKIN = SKIN if status else SKIN_DARK
    draw.circle(screen, MY_SKIN, (x, y - 40), 30)
    draw.line(screen, MY_SKIN, (x, y + 10), (x, y + 160), 20)
    draw.lines(screen, MY_SKIN, 0, ((x - 50, y + 110), (x, y + 1), (x + 50, y + 120)), 10)
    draw.lines(screen, MY_SKIN, 0, ((x - 40, y + 280), (x, y + 120), (x + 40, y + 280)), 20)


# функция для прорисовки птицы по размеру и углу наклона крыльев
def bird(x, y, size, angle):
    x1 = x + size * cos(radians(180 - angle))
    x2 = x - size * cos(radians(180 - angle))
    y1 = y - size * sin(radians(angle))

    draw.lines(screen, BIRD, 0, ((x1, y1), (x, y), (x2, y1)), 6)
    draw.lines(screen, BIRD, 0, ((x1, y1), (x, y - 4), (x2, y1)), 3)
    draw.circle(screen, BIRD, (x, y - 7), 5)


# функция прорисовки светлячков
def firefly(x, y):
    size = randint(2, 5)
    draw.circle(screen, BIRD_N, (x, y), size)


# функция для появления новых птиц
def spawn():
    for i in range(len(birds)):
        if not (birds[i]['here']):
            birds[i]['here'] = True   # существует
            birds[i]['direction'] = 1 if randint(0, 1) else -1   # направление
            birds[i]['x'] = -40 if (birds[i]['direction'] == 1) else width + 40   # место появления X
            birds[i]['y'] = randint(spawn_r_s, spawn_r_f)   # место появления Y
            birds[i]['size'] = randint(size_r_s, size_r_f)   # размер
            birds[i]['speed'] = randint(1, 7)   # скорость
            birds[i]['fly'] = st_angle   # размах крыльев
            birds[i]['k'] = 1   # скорость взмаха крыльев
            break


# "Небесное тело - солнце или луна"
globe = {
    'length_orbit': 400,
    'angle_orb': 180,
    'speed_orb': calc_speed_orb(10, FPS),
    'speed_self': 1,
    'image': image.load("./images/5.png")
}

# координаты центра, от которого будет вращаться небесное тело
center_x = 500
center_y = 425

while True:
    # скорость анимации
    clock.tick(FPS)
    for e in event.get():
        # если выход
        if e.type == QUIT:
            print('Возращайтесь!')
            quit()
            sys.exit()
    # если небесное тело зашло за горизонт, то сменяется день и ночь
    if globe['angle_orb'] > 360:
        globe['angle_orb'] = 180
        is_day = not is_day

    # координаты видимого небесного тела
    globe_x = center_x + cos(radians(globe['angle_orb'])) * globe['length_orbit']
    globe_y = center_y + sin(radians(globe['angle_orb'])) * globe['length_orbit']
    
    # Фон
    if is_day:
        screen.fill(SKY)   # создаём фоном чистое небо

        draw.circle(screen, SUN, (globe_x, globe_y), 70)   # создаём солнце

        grass_p = image.load("./images/3.jpg")   # картинка травы
        grass_rect = grass_p.get_rect(topleft=(0, height - 200))
        screen.blit(grass_p, grass_rect)

        globe['angle_orb'] += globe['speed_orb']  # Вращение планеты по окружности

    else:
        screen.fill(SKY_N)   # создаём фоном ночное небо

        draw.circle(screen, GREY, (globe_x, globe_y), 70)   # создаём луну

        grass_p = image.load("./images/9.jpg")   # картинка травы
        grass_rect = grass_p.get_rect(topleft=(0, height - 200))
        screen.blit(grass_p, grass_rect)

        globe['angle_orb'] += globe['speed_orb']  # Вращение планеты по окружности

    # создание человека
    human(man['x'], man['y'], is_day)

    # создание птиц
    if birds_count < birds_limit:
        if (randint(0, 100) <= 5):
            birds_count += 1
            spawn()

    # прорисовка птиц
    for i in birds:
        if i['here']:
            i['y'] = bird_fly(i['x'], i['y'], is_day)
            # соприкосновение с человеком
            if ((man['x'] - 25 <= i['x'] <= man['x'] + 25) and
                    (man['y'] - 65 <= i['y'])):
                birds_count -= 1
                i['here'] = False
                continue
            
            # движение крыльев
            if (i['fly'] >= 80) or (i['fly'] <= 30):
                i['k'] *= -1
            i['fly'] += 5 * i['k']

            # вылет за экран
            if -40 <= i['x'] <= width + 40:
                i['x'] += i['speed'] * i['direction']
            else:
                i['x'] = -40 if i['direction'] == 1 else width + 40
            
            # если день - птички, иначе - светляки
            if is_day:
                bird(i['x'], i['y'], i['size'], i['fly'])
            else:
                firefly(i['x'], i['y'])

    display.flip()   # обновление экрана
    