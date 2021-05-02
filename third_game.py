import pygame
import sys
import random

pygame.init()

import global_variables as g



class Cursor (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagini/cursor.png")
        self.image = pygame.transform.smoothscale(self.image, (50, 50))
        self.rect = self.image.get_rect()

    def Blit (self, surface):
        pos = pygame.mouse.get_pos()
        self.rect.centerx = pos[0] - (1600 - g.surface_size) / 2
        self.rect.centery = pos[1] - (900 - g.surface_size) / 2
        surface.blit(self.image, self.rect)

class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagini/circle.png")
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.circle = pygame
        self.circle_radius = 50 + 60
        self.circle_speed = speed
        self.points = 0

    
    def Update(self, dt):
        self.circle_radius -= self.circle_speed * dt
        self.points = 110 - self.circle_radius
        if self.circle_radius <= 48:
            self.kill()

    def Clicked(self):
        self.kill()
        self.poitns = self.points
        return self.points

    def Blit (self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.circle(surface, g.green, self.rect.center, self.circle_radius, 3)
    



class Third_Game():
    def __init__(self):
        g.variables_initialization()
        pygame.mixer.music.load('sunete/circle_song.wav')
        pygame.mixer.music.play(0)
        self.surface_size = g.surface_size
        self.surface = pygame.Surface((self.surface_size, self.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (800, 450)
        self.running = True
        self.cursor = Cursor()
        self.time = 0

        self.last_time = 0
        self.new_time = 0

        self.circle_group = pygame.sprite.Group()

        self.points = 0

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.score = 0
        self.text = self.font.render("Score: " + str(self.points), True, g.white, False)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (g.surface_size/2, 50)

        self.last_point = self.font.render(str(self.points), True, g.white, False)
        self.last_point_rect = self.last_point.get_rect()
        self.last_point_rect.center = (-100, -100)
        #generare seed random, de scos
        random.seed(a=None, version=2)
        self.circle_speed = 60

        self.circle_hit_sound = pygame.mixer.Sound("sunete/circle_hit.wav")
        self.background = pygame.image.load("imagini/third.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400,400)
    
    def Blit_Images(self):
        self.surface.blit(self.background, self.background_rect)
        self.cursor.Blit(self.surface)
        self.surface.blit(self.last_point, self.last_point_rect)
        self.surface.blit(self.text, self.text_rect)
        for circle in self.circle_group:
            circle.Blit(self.surface)
        g.screen.blit(self.surface, self.surface_rect)
        pygame.display.flip()
    
    def Update(self):
        dt = g.clock.tick(60) / 1000
        self.time += dt
        if self.time > 2 and self.time < 58:
            if int(self.time) == 20:
                self.circle_speed = 80
            if int(self.time) == 30:
                self.circle_speed = 120
            if int(self.time) == 40:
                self.circle_speed = 150
            if int(self.time) == 50:
                self.circle_speed = 160
            self.new_time = int(self.time)
            if self.last_time != self.new_time:
                self.last_time = self.new_time
                circle = Circle(random.randrange(100,700),random.randrange(100,700), self.circle_speed)
                self.circle_group.add(circle)
        else:
            if self.time > 60:
                self.running = False
        
        for circle in self.circle_group:
            circle.Update(dt)
    
    def Check_Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                circle_pressed = pygame.sprite.spritecollide(self.cursor, self.circle_group, True)
                for circle in circle_pressed:
                    pygame.mixer.Sound.play(self.circle_hit_sound)
                    center = circle.rect.center
                    points = circle.Clicked()
                    points = int(points)
                    self.text = self.font.render("Score: " + str(self.points), True, g.white, False)
                    self.text_rect = self.text.get_rect()
                    self.text_rect.center = (g.surface_size/2, 50)
                    self.last_point = self.font.render(str(points), False, g.white, False)
                    self.last_point_rect = self.last_point.get_rect()
                    self.last_point_rect.center = (center)
                    self.points += points
                pos = pygame.mouse.get_pos()
                if pos[0] >= 1515 and pos[0] <= 1585 and pos[1] >=785 and pos[1] <= 859:
                        self.running = False
    def Loop(self):
        while self.running:
            self.Check_Events()
            self.Update()
            self.Blit_Images()
        pygame.mixer.music.stop()
        return self.points



#third_game = Third_Game()
#third_game.Loop()

