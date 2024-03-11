from pygame import *
from sys import exit
init()


class Sprite(sprite.Sprite):
    def __init__(self, w, h, file_name, x, y):
        super().__init__()
        self.image = transform.scale(image.load(file_name), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Sprite):
    def __init__(self, w, h, file_name, x, y):
        super().__init__(w, h, file_name, x, y)
        self.speed_x = 0
        self.speed_y = 0
    def update(self):
        # TODO: проблема с кнопками
        self.speed_y = 0
        self.speed_x = 0
        keys_press = key.get_pressed()
        if keys_press[K_w] and self.rect.y > 0:
            self.speed_y = -2
        if keys_press[K_s] and self.rect.y < H - 15:
            self.speed_y = 2
        if keys_press[K_w] and keys_press[K_s]:
            self.speed_y = 0
        self.rect.y += self.speed_y
        sprites = sprite.spritecollide(self, walls, False)
        for wall in sprites:
            if self.speed_y > 0:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
            if self.speed_y < 0:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        if keys_press[K_d] and self.rect.x < W - 15:
            self.speed_x = 2
        if keys_press[K_a] and self.rect.x > 0:
            self.speed_x = -2
        if keys_press[K_a] and keys_press[K_d]:
            self.speed_x = 0
        self.rect.x += self.speed_x
        sprites = sprite.spritecollide(self, walls, False)
        for wall in sprites:
            if self.speed_x > 0:
                self.rect.right = min(self.rect.right, wall.rect.left)
            if self.speed_x < 0:
                self.rect.left = max(self.rect.left, wall.rect.right)
class Enemy(Sprite):
    def __init__(self, w, h, file_name, x, y, left, right):
        super().__init__(w, h, file_name, x, y)
        self.left = left
        self.right = right
        self.side = 'left'
    def update(self):
        if self.side == 'left':
            self.rect.x -= 2
            if self.rect.x < self.left:
                self.side = 'right'
        if self.side == 'right':
            self.rect.x += 2
            if self.rect.x > self.right:
                self.side = 'left'


player = Player(15, 15, 'pictures/сердце.png', 20, 240)
cup = Sprite(20, 20, 'pictures/cup.png', 470, 10)


W = 500
H = 500
window = display.set_mode((W, H))
background = image.load('pictures/fon.jpg')
background = transform.scale(background, (W, H))
dead = image.load('pictures/kartinka.jpg')
dead = transform.scale(dead, (W, H))
vin = image.load('pictures/pobeda.png')
vin = transform.scale(vin, (W, H))
finish = False
restart = Sprite(60, 20, 'pictures/button.png', 220, 460)
myz_vin = mixer.Sound('music/myzvin.mp3')
myz_vin.set_volume(0.05)
myz_death = mixer.Sound('music/myzdeath.mp3')
myz_death.set_volume(0.05)


def restart_button():
    global finish
    player.rect.x = 20
    player.rect.y = 240
    finish = False


walls = sprite.Group(
    Sprite(20, 100, 'pictures/ctena.png', 150, 120),
            Sprite(20, 100, 'pictures/ctena.png', 350, 100),
            Sprite(320, 20, 'pictures/ctena.png', 150, 100),
            Sprite(20, 260, 'pictures/ctena.png', 252, 160),
            Sprite(375, 20, 'pictures/ctena.png', 0, 270),
            Sprite(100, 20, 'pictures/ctena.png', 350, 200),
            Sprite(20, 250, 'pictures/ctena.png', 450, 200),
            Sprite(450, 20, 'pictures/ctena.png', 20, 450),
            Sprite(130, 20, 'pictures/ctena.png', 340, 380),
            Sprite(20, 130, 'pictures/ctena.png', 200, 320),
            Sprite(20, 130, 'pictures/ctena.png', 150, 290),
            Sprite(20, 130, 'pictures/ctena.png', 100, 320),
            Sprite(70, 10, 'pictures/ctena.png', 30, 320),
            Sprite(70, 10, 'pictures/ctena.png', 0, 350),
            Sprite(70, 10, 'pictures/ctena.png', 30, 380),
            Sprite(70, 10, 'pictures/ctena.png', 0, 410),
            Sprite(100, 20, 'pictures/ctena.png', 400, 150),
            Sprite(450, 20, 'pictures/ctena.png', 50, 40),
            Sprite(150, 20, 'pictures/ctena.png', 0, 200),
            Sprite(70, 40, 'pictures/ctena.png', 30, 40),
            Sprite(70, 10, 'pictures/ctena.png', 0, 100),
            Sprite(70, 10, 'pictures/ctena.png', 30, 130),
            Sprite(70, 10, 'pictures/ctena.png', 0, 160),
            Sprite(20, 130, 'pictures/ctena.png', 100, 50)

)


enemys = sprite.Group(
            Enemy(60, 30, 'pictures/кость.png', 400, 200, 150, 300),
                    Enemy(60, 30, 'pictures/кость.png', 276, 300, 276, 400),
                    Enemy(60, 30, 'pictures/кость.png', 240, 400, 250, 387)
)

clock = time.Clock()



while True:
    for e in event.get():
        if e.type == QUIT:
            exit()
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            if restart.rect.collidepoint(x, y):
                restart_button()
    if not finish:
        window.blit(background, (0, 0))
        player.draw()
        player.update()
        walls.draw(window)
        enemys.draw(window)
        enemys.update()
        cup.draw()
        if sprite.spritecollide(player, enemys, False):
            finish = True
            window.blit(dead, (0, 0))
            restart.draw()
            myz_death.play()
        if sprite.collide_rect(player, cup):
            finish = True
            window.blit(vin, (0, 0))
            restart.draw()
            myz_vin.play()
    display.update()
    clock.tick(90)