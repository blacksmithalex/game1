import pygame
from random import randint
from math import sqrt
from time import sleep
from time import time

# начинаем работу с PyGame
pygame.init()
screen = pygame.display.set_mode((1000, 600))
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
        if self.y < 560:
            self.y += self.speed

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < 950:
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
    def check(self):
        if 380 < self.x < 480 or 200 < self.y < 300:
            self.x = randint(0, 1000)
            self.y = randint(0, 400)
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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

bg = pygame.image.load('img/bg.jpg')
bg_the_end = pygame.image.load('img/end.jpg')
Ron = Player('img/ron.png', 10, 455, 250)
Spiders = []
Big_monster = []
for _ in range(10):
    if randint(0, 1) == 0:
        Spiders.append(Monster('img/spider.png', randint(1, 7), randint(0, 650), randint(0,1200)))
    else:
        Spiders.append(Monster('img/mon1.png', randint(1, 7), randint(0, 650), randint(0, 1200)))

iteration = 0
game_time_sec = 0
active_game_time_sec = 0
running = True
flagPotionShow = False
flagPotionTake = False
f1 = pygame.font.SysFont(None, 30)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # управление кнопками
    keys = pygame.key.get_pressed()  # список кнопок, которые сейчас нажаты

    screen.blit(bg, (0, 0))  # устанавливаем фон
    screen.blit(pygame.image.load('img/extra.png'), (800, 210))
    screen.blit(pygame.image.load('img/ronstart.png'), (380, 200))
    for Spider in Spiders[:game_time_sec // 10]:
        Spider.show()
        Spider.move()
    Ron.show()
    Ron.show_life()
    if game_time_sec % 20 == 5:
        flagPotionShow = True
    if flagPotionShow:
        potion = screen.blit(pygame.image.load('img/potion1.png'), (848, 255))
    if flagPotionShow and Ron.life < 3 and distance(Ron.x, Ron.y, 848, 255) < 50:
        Ron.life += 1
        potion.x = 20000
        potion.y = 20000
        flagPotionShow = False

    for Spider in Spiders[:game_time_sec // 10]:
        Spider.check()
        if distance(Spider.x, Spider.y, Ron.x, Ron.y) < 50:
            screen.blit(pygame.image.load('img/regularExplosion01.png'), (Ron.x, Ron.y))
            screen.blit(pygame.image.load('img/regularExplosion02.png'), (Ron.x, Ron.y))
            screen.blit(pygame.image.load('img/regularExplosion03.png'), (Ron.x, Ron.y))
            screen.blit(pygame.image.load('img/regularExplosion04.png'), (Ron.x, Ron.y))
            screen.blit(pygame.image.load('img/regularExplosion05.png'), (Ron.x, Ron.y))
            screen.blit(pygame.image.load('img/regularExplosion06.png'), (Ron.x, Ron.y))
            screen.blit(pygame.image.load('img/regularExplosion07.png'), (Ron.x, Ron.y))
            Ron.life -= 1
            Ron.to_center()
            if Ron.life == 0:
                screen.blit(bg_the_end, (0, 0))
                text1 = f1.render('Вы продержались {} секунд'.format(game_time_sec), False, (255, 0, 0))
                screen.blit(text1, (324, 200))
                running = False
    Ron.run()
    iteration = (iteration + 1) % 120
    # почему 120? берем отсчет итераций больше FPS, чтобы монстры не так часто меняли направление
    # это нужно, чтобы не переполнялась переменная итерации. Можно взять не 120, а 1234
    if iteration % FPS == 0:
        game_time_sec += 1  # вычисляем, сколько секунд длилась игра
    if not (380 < Ron.x < 480 or 200 < Ron.y < 300) and iteration % FPS == 0:
        active_game_time_sec += 1
    texttime = f1.render('Прошло {} секунд'.format(active_game_time_sec), False, (255, 0, 0))
    screen.blit(texttime, (800, 20))
    pygame.display.flip()

print("Вы продержались:", game_time_sec, "сек")

sleep(2)  # даём пользователю посмотреть на результат
pygame.quit()  # закрываем окно
