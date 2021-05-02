import pygame
import sys
import math
import random
from connection import Connection
pygame.init()


import global_variables as g

#de sters, o sa fie initializat in main game
g.screen = pygame.display.set_mode([1600, 900])

class Sprint_Bar(pygame.sprite.Sprite):
    def __init__(self):
        self.size = 100
        self.image = pygame.Surface((self.size, 30))
        self.image.fill(g.green)
        self.rect = self.image.get_rect()
        self.rect.left = 50
        self.rect.centery = 750
        self.sprinting = False
    
    def Update(self):
        self.image = pygame.Surface((self.size, 30))
        self.image.fill(g.green)
        self.rect = self.image.get_rect()
        self.rect.left = 50
        self.rect.centery = 750


class Heart(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagini/heart.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = 100

class Spike(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.size = 40
        self.image = pygame.image.load("imagini/narwal_spike.png")
        self.image = pygame.transform.smoothscale(self.image, (self.size, 10))
        self.rect = self.image.get_rect()
        self.rect.centery = y 
        self.rect.left = x
        self.new_image = self.image

    def Zoom(self):
        self.size += 5
        self.image = pygame.transform.smoothscale(self.image, (self.size, 10))
    
    def Blit(self, surface):
        surface.blit(self.new_image, self.rect)
    
    def Update(self, pos, player_x, player_y, angle, sin, cos):
        pos_x = pos[0] - 400
        pos_y = pos[1] - 50
        
        self.new_image = pygame.transform.rotate(self.image, angle)
        self.rect = self.new_image.get_rect()

        self.rect.centery = player_y + sin * self.size * 0.7
        cos = math.cos(math.radians(angle))
        self.rect.centerx = player_x + cos * self.size * 0.7
    
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.size = 10
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(g.green)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        if color == g.white:
            self.image = pygame.image.load("imagini/narwal.png")
        else: 
            self.image = pygame.image.load("imagini/brown_narwal.png")
        self.heart_image = pygame.image.load("imagini/heart.png")
        self.image = pygame.transform.smoothscale(self.image, (100, 45))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.spike = Spike(self.rect.centery, self.rect.right)
        self.angle = 0
        self.new_image = self.image
        self.speed = 130
        self.sin  = 0
        self.cos = 1
        self.life = pygame.sprite.Group()
    
    def Blit(self, surface):
        self.spike.Blit(surface)
        surface.blit(self.new_image, self.rect)

    def Update(self, pos, dt):
        pos_x = pos[0] - 400
        pos_y = pos[1] - 50
        if pos_x != self.rect.centery and pos_y != self.rect.centery:
            if pos_x >= self.rect.centerx and pos_y >= self.rect.centery:
                x = pos_x - self.rect.centerx
                y = pos_y - self.rect.centery
                self.sin = math.sqrt(x * x + y * y)
                if self.sin == 0:
                    self.sin  = 1
                self.sin  =  y / self.sin 
                self.angle = 360 - math.degrees(math.asin(self.sin )) 
            else:
                if pos_x <= self.rect.centerx and pos_y <= self.rect.centery:
                    x = self.rect.centerx - pos_x
                    y = self.rect.centery - pos_y
                    self.sin = math.sqrt(x * x + y * y)
                    self.sin  =  y / self.sin 
                    self.angle = 180 - math.degrees(math.asin(self.sin ))
                else:
                    if pos_x > self.rect.centerx and pos_y < self.rect.centery:
                        x = pos_x - self.rect.centerx
                        y = self.rect.centery - pos_y
                        self.sin  = math.sqrt(x * x + y * y)
                        self.sin =  y / self.sin
                        self.angle =  math.degrees(math.asin(self.sin))
                    else: 
                        if pos_x < self.rect.centerx and pos_y > self.rect.centery:
                            y = pos_y - self.rect.centery
                            x = self.rect.centerx - pos_x
                            self.sin  = math.sqrt(x * x + y * y)
                            self.sin  =  y / self.sin 
                            self.angle =  180 + math.degrees(math.asin(self.sin))
                        else:
                            self.angle = 0
            self.new_image = pygame.transform.rotate(self.image, self.angle)
            self.cos = math.cos(math.radians(self.angle))
            rect = self.new_image.get_rect()
            rect.centerx = self.rect.centerx
            rect.centery = self.rect.centery
            self.rect = rect
            if pos_y < self.rect.centery:
                self.sin *= -1
            self.rect.centery += self.sin * self.speed * dt
            
            self.rect.centerx += self.cos * self.speed * dt

        self.spike.Update(pos, self.rect.centerx, self.rect.centery, self.angle, self.sin, self.cos)
        #self.spike.Zoom()

    def Check_Collision(self, food_collided):
        if self.rect.right > g.surface_size:
            self.rect.right = g.surface_size
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > g.surface_size:
            self.rect.bottom = g.surface_size
        for food in food_collided:
            self.spike.Zoom()
    
    def multiplayer_update(self):
        self.spike.image = pygame.transform.smoothscale(self.spike.image, (self.spike.size, 10))
        self.new_image = pygame.transform.rotate(self.image, self.angle)
        rect = self.new_image.get_rect()
        rect.center = self.rect.center
        self.rect = rect
        self.spike.new_image = pygame.transform.rotate(self.spike.image, self.angle)
        rect = self.spike.new_image.get_rect()
        rect.center = self.spike.rect.center
        self.spike.rect = rect



class Forth_Game():
    def __init__(self, port):
        g.variables_initialization()
        random.seed(port)
        self.surface_size = g.surface_size
        self.surface = pygame.Surface((self.surface_size, self.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (800, 450)
        self.running = True
        self.player = Player(g.white, 400, 400)
        self.player2 = Player(g.brown, 400, 400)
        self.dt = 0

        self.all_food = pygame.sprite.Group()
        self.spawn_time = 0
        self.time = 0
        self.invincibility = 3

        self.knockback_time = 0
        
        self.heart_image = pygame.image.load("imagini/heart.png")
        heart = Heart(50)
        self.player.life.add(heart)
        heart = Heart(100)
        self.player.life.add(heart)
        heart = Heart(150)
        self.player.life.add(heart)

        heart = Heart(650)
        self.player2.life.add(heart)
        heart = Heart(700)
        self.player2.life.add(heart)
        heart = Heart(750)
        self.player2.life.add(heart)

        self.enemy_life = []
        self.sprint_bar = Sprint_Bar()

        pygame.mixer.music.load('sunete/3.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.background = pygame.image.load("imagini/forth.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400,400)

        self.score = 1
    def Blit_Images(self, pos):
        self.surface.blit(self.background, self.background_rect)
        self.all_food.draw(self.surface)
        self.player.life.draw(self.surface)
        for heart in self.enemy_life:
            self.surface.blit(self.heart_image, (heart[0]+ 500, heart[1]))
        self.surface.blit(self.sprint_bar.image, self.sprint_bar.rect)
        self.player.Blit(self.surface)
        self.player2.Blit(self.surface)
        g.screen.blit(self.surface, self.surface_rect)
        pygame.display.flip()
    
    def Update(self, pos, q_send, q_listen):
        if self.knockback_time > 0:
            self.knockback_time -= self.dt
            self.player.speed = -1 * abs(self.player.speed)
        else:
            self.player.speed = abs(self.player.speed)
        self.spawn_time += self.dt
        self.time += self.dt
        self.sprint_bar.Update()
        if self.sprint_bar.sprinting:
            if self.sprint_bar.size > 0:
                    self.player.speed = 300
                    self.sprint_bar.size -= self.dt * 60
            else:
                self.player.speed = 130
        if self.sprint_bar.size < 100 and self.sprint_bar.sprinting == False:
            self.sprint_bar.size += 20 * self.dt
        if self.invincibility > 0:
            self.invincibility -= self.dt
        if self.spawn_time > 1:
            self.spawn_time = 0
            x = random.randrange(0, g.surface_size)
            y = random.randrange(0, g.surface_size)
            food = Food(x, y)
            self.all_food.add(food)
        if self.time > 0.03:
            send_heart_rect = []
            for heart in self.player.life:
                send_heart_rect.append(heart.rect.center)

            packet = ("minigame", self.player.rect.center, self.player.spike.rect.center, self.player.angle, self.player.spike.size, send_heart_rect)
            q_send.append(packet)
            self.time = 0
        if q_listen:
            data = q_listen[0]

            if data[0] == "minigame":
                self.player2.angle = data[3]
                self.player2.rect.center = data[1]
                self.player2.spike.rect.center = data[2]
                self.player2.spike.size = data[4]
                self.enemy_life = data[5]
                self.player2.multiplayer_update()
            else:
                if data[0] == "close":
                    self.running = False
            q_listen.popleft()

        self.player.Update(pos, self.dt)
        food_collided = pygame.sprite.spritecollide(self.player, self.all_food, True)
        enemy_food_collided = pygame.sprite.spritecollide(self.player2, self.all_food, True)
        if self.player.spike.rect.colliderect(self.player2.spike.rect):
            self.knockback_time = 0.5
        for food in enemy_food_collided:
            food.kill()
        if self.player.rect.colliderect(self.player2.spike.rect):
            if self.invincibility <= 0:
                self.invincibility = 2
                all_hearts = self.player.life.sprites()
                if len (all_hearts) > 1:
                    for heart in self.player.life:
                        heart.kill()
                        break
                else:
                    self.score = 0
                    q_send.clear()
                    packet = ("close", False)
                    q_send.append(packet)
                    q_send.append(packet)
                    q_send.append(packet)
                    q_send.append(packet)
                    self.running = False
        self.player.life.draw(self.surface)
        self.player.Check_Collision(food_collided)
    
    def Check_Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.sprint_bar.sprinting = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.sprint_bar.sprinting = False
                self.player.speed = 130
                
    def Loop(self, q_listen, q_send):
        while self.running == True:
            pos = pygame.mouse.get_pos()
            self.dt = g.clock.tick(60) / 1000
            self.Check_Events()
            self.Update(pos, q_send, q_listen)
            self.Blit_Images(pos)
        return self.score
        pygame.mixer.music.stop()

#connection = Connection()
#forth_game = Forth_Game(connection.port)
#forth_game.Loop(connection.q_listen, connection.q_send)

