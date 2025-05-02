from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#font
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 51))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

lost = 0
score = 0
max_lost = 3
goal = 15
life = 3

img_back = 'galaxy.jpg'
img_P1 = 'rocket_P_1.png'
img_P2 = 'rocket_P_2.png'
img_bullet = 'bullet.png'
img_enemy = 'alien.png'
img_ast = 'asteroid.png'

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    
    def update_P1(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 600:
            self.rect.x += self.speed

    def update_P2(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 500:
            self.rect.x -= self.speed
        if keys [K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 1000
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship_P1 = Player(img_P1, 5, win_height - 100, 80, 100, 10)
ship_P2 = Player(img_P2, 925, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 10):
    monster = Enemy(img_enemy, randint(40, win_width - 30), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()


finish = False

run = True

rel_time = False
num_fire = 0

while run:
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    ship_P1.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_f:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    ship_P2.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_m:
                mixer_music.set_volume(0.0)
                fire_sound.set_volume(0.0)
            if e.key == K_u:
                mixer_music.set_volume(100.0)
                fire_sound.set_volume(100.0)

    if not finish:

        window.blit(background, (0, 0))

        text = font2.render('Score:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Missed:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship_P1.update_P1()
        ship_P2.update_P2()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship_P1.reset()
        ship_P2.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (450, 460))
            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(40, win_width - 30), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship_P1, monsters, False) or sprite.spritecollide(ship_P1, asteroids, False):
            sprite.spritecollide(ship_P1, monsters, True)
            sprite.spritecollide(ship_P1, asteroids, True)
            life = life - 1
            
        if sprite.spritecollide(ship_P2, monsters, False) or sprite.spritecollide(ship_P2, asteroids, False):
            sprite.spritecollide(ship_P2, monsters, True)
            sprite.spritecollide(ship_P2, asteroids, True)
            life = life - 1

        if life == 0 or lost > max_lost:
            finish = True
            window.blit(lose, (370, 200))
        
        if sprite.spritecollide(ship_P1, monsters, False) or sprite.spritecollide(ship_P2, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (370, 200))

        if score >= goal:
            finish = True
            window.blit(win, (370, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (950, 10))

        display.update()
        #automatic restart of the game
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 10):
            monster = Enemy(img_enemy, randint(40, win_width - 30), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

    time.delay(50)
