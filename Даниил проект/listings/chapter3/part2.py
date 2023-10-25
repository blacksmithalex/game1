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