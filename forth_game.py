import pygame
import sys
import math
import random
pygame.init()


import global_variables as g

#de sters, o sa fie initializat in main game
g.screen = pygame.display.set_mode([1600, 900])

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

        self.rect.centery = player_y + sin * self.size
        cos = math.cos(math.radians(angle))
        self.rect.centerx = player_x + cos * self.size
    
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
        self.image = pygame.image.load("imagini/narwal.png")
        self.image = pygame.transform.smoothscale(self.image, (100, 45))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.spike = Spike(self.rect.centery, self.rect.right)
        self.angle = 0
        self.new_image = self.image
        self.speed = 200
        self.sin  = 0
        self.cos = 1
    
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
            

class Forth_Game():
    def __init__(self):
        g.variables_initialization()
        random.seed(a=None, version=2)
        self.surface_size = g.surface_size
        self.surface = pygame.Surface((self.surface_size, self.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (800, 450)
        self.running = True
        self.player = Player(g.white, 400, 400)
        self.dt = 0

        self.all_food = pygame.sprite.Group()
        self.time = 0
        pygame.mixer.music.load('sunete/3.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.background = pygame.image.load("imagini/forth.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400,400)

    def Blit_Images(self, pos):
        #g.screen.fill(g.white)
        self.surface.blit(self.background, self.background_rect)
        self.all_food.draw(self.surface)
        self.player.Blit(self.surface)
        g.screen.blit(self.surface, self.surface_rect)
        pygame.display.flip()
    
    def Update(self, pos):
        self.time += self.dt
        if self.time > 5:
            self.time = 0
            x = random.randrange(0, g.surface_size)
            y = random.randrange(0, g.surface_size)
            food = Food(x, y)
            self.all_food.add(food)
        self.player.Update(pos, self.dt)
        food_collided = pygame.sprite.spritecollide(self.player, self.all_food, True)
        self.player.Check_Collision(food_collided)
    
    def Check_Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 1515 and pos[0] <= 1585 and pos[1] >=785 and pos[1] <= 859:
                        self.running = False
                
    def Loop(self):
        while self.running == True:
            pos = pygame.mouse.get_pos()
            self.dt = g.clock.tick(60) / 1000
            self.Check_Events()
            self.Update(pos)
            self.Blit_Images(pos)
        pygame.mixer.music.stop()


#forth_game = Forth_Game()
#forth_game.Loop()

