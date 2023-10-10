import pygame
from random import randint
from math import sqrt
from time import sleep
from time import time

# начинаем работу с PyGame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
FPS = 30

def distance(x1, y1, x2, y2):
    '''функция возвращает расстояние между двумя точками'''
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
class Character:
    def __init__(self, img, speed, x, y):
        self.img = pygame.image.load(img)
        self.speed = speed
        self.x = x
        self.y = y
        self.life = 3

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
class Player(Character):
    def run(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move_up()
        if keys[pygame.K_s]:
            self.move_down()
        if keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_d]:
            self.move_right()
    def show_life(self):
        if self.life == 3:
            screen.blit(pygame.image.load('img/heart3.png'), (20, 20))
        elif self.life == 2:
            screen.blit(pygame.image.load('img/heart2.png'), (20, 20))
        elif self.life == 1:
            screen.blit(pygame.image.load('img/heart1.png'), (20, 20))
    def to_center(self):
        self.x = 300
        self.y = 200


bg = pygame.image.load('img/bg.jpg')
bg_the_end = pygame.image.load('img/end.jpg')
Ron = Player('img/ron.png', 10, 300, 200)
Spiders = []
for _ in range(5):
    Spiders.append(Monster('img/spider.png', randint(1, 7), randint(0, 600), randint(0,400)))

iteration = 0
game_time_sec = 0
running = True
flagPotion = False
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # управление кнопками
    keys = pygame.key.get_pressed()  # список кнопок, которые сейчас нажаты

    screen.blit(bg, (0, 0))  # устанавливаем фон
    for Spider in Spiders:
        Spider.show()
        Spider.move()
    Ron.show()
    Ron.show_life()
    if not flagPotion:
        potion = screen.blit(pygame.image.load('img/potion1.png'), (40, 40))
    if Ron.life < 3 and distance(Ron.x, Ron.y, 40, 40) < 50:
        Ron.life += 1
        flagPotion = True
    for Spider in Spiders:
        if distance(Spider.x, Spider.y, Ron.x, Ron.y) < 50:
            Ron.life -= 1
            Ron.to_center()
            if Ron.life == 0:
                screen.blit(bg_the_end, (0, 0))
                f1 = pygame.font.SysFont(None, 40)
                text1 = f1.render('Вы продержались {} секунд'.format(game_time_sec), False, (255, 0, 0))
                screen.blit(text1, (100, 50))
                running = False
    Ron.run()
    iteration = (iteration + 1) % 120
    # почему 120? берем отсчет итераций больше FPS, чтобы монстры не так часто меняли направление
    # это нужно, чтобы не переполнялась переменная итерации. Можно взять не 120, а 1234
    if iteration % FPS == 0:
        game_time_sec += 1  # вычисляем, сколько секунд длилась игра
    pygame.display.flip()

print("Вы продержались:", game_time_sec, "сек")

sleep(2)  # даём пользователю посмотреть на результат
pygame.quit()  # закрываем окно
