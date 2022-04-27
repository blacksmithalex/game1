import pygame
from random import randint
from math import sqrt
from time import sleep

# начинаем работу с PyGame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
FPS = 30

def distance(x1, y1, x2, y2):
    # функция возвращает расстояние между двумя точками
    return 0

class Character:
    def __init__(self, img, speed, x, y):
        self.img = pygame.image.load(img)
        self.speed = speed
        self.x = x
        self.y = y

    def show(self):
        screen.blit(self.img, (self.x, self.y))

    def move_up(self):
        if self.y > 0:
            self.y -= self.speed

    def move_down(self):
        if self.y < 360:
            self.y += self.speed

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < 550:
            self.x += self.speed


class Monster(Character):
    def move(self):
        var = randint(0, 3)
        if var == 0:
            self.move_up()
        elif var == 1:
            self.move_right()
        elif var == 2:
            self.move_down()
        else:
            self.move_left()

bg = pygame.image.load('img/bg.jpg')
bg_the_end = pygame.image.load('img/end.jpg')
#Ron = Character('ron.png', 2, 300, 200)
Spiders = []
for _ in range(15):
    Spiders.append(Monster('img/spider.png', randint(1, 7), randint(0, 600), randint(0,400)))

iteration = 0
game_time_sec = 0
# запускаем цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # управление кнопками
    keys = pygame.key.get_pressed()  # список кнопок, которые сейчас нажаты

    screen.blit(bg, (0, 0))  # устанавливаем фон
    #Ron.show()
    for Spider in Spiders:
        Spider.show()
        Spider.move()

    iteration = (iteration + 1) % 120
    # почему 120? берем отсчет итераций больше FPS, чтобы монстры не так часто меняли направление
    # это нужно, чтобы не переполнялась переменная итерации. Можно взять не 120, а 1234
    if iteration % FPS == 0:
        game_time_sec += 1  # вычисляем, сколько секунд длилась игра
    pygame.display.flip()

print("Вы продержались:", game_time_sec, "сек")

sleep(2)  # даём пользователю посмотреть на результат
pygame.quit()  # закрываем окно
