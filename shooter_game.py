#Create your own shooter

from pygame import *
from random import randint

win_width = 700
win_heigth = 500

window = display.set_mode((win_width, win_heigth))
display.set_caption('Catch')
#set scene background
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_heigth))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('LOSER...', True, (100, 0, 0))


font2 = font.Font(None, 36)

score = 0 
goal = 10
lost = 0
max_lost = 10
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width -80:
            self.rect.x += self.speed        

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_heigth:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

clock = time.Clock()
fps = 60

mc = Player('rocket.png', 5, win_heigth -100, 80, 100, 4)
bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1,3):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1,3))
    monsters.add(monster)


finish = False

game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                mc.fire()

    if not finish:
        window.blit(background,(0, 0))
        text_win = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(text_win, (10,20))

        text_lose = font2.render('Missed: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))


        mc.update()
        mc.reset()
        bullets.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(mc, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        display.update()
    clock.tick(fps)