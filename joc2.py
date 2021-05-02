import pygame
import random
import sys
from collections import deque


#from connection import Connection
pygame.init()

import global_variables as g

#de sters, o sa fie initializat in main game
#g.screen = pygame.display.set_mode([1600, 900])

class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y): #, text_center, text_string):
        pygame.sprite.Sprite.__init__(self)
        self.size = 60
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.score = 1000
        self.gravitation = 10
        self.y_speed = 0
        self.x_speed = 300
        self.touched_left = False
        self.touched_right = False
        self.jump_sound = pygame.mixer.Sound("sunete/jump_sound.wav")
        """
        self.text_center = text_center
        self.text_string = text_string
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render(self.text_string + str(self.score), True, g.white, False)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.text_center
        """

    def Update(self, dt):
        self.y_speed = self.y_speed + self.gravitation * dt
        self.rect.x += self.x_speed * dt
        self.rect.y += self.y_speed 
        if self.rect.right >= g.surface_size:
            self.touched_right = True
            self.x_speed = -1 * self.x_speed
        if self.rect.left <= 0:
            self.touched_left = True
            self.x_speed = abs(self.x_speed)
        if self.rect.bottom >= g.surface_size:
            self.y_speed = -1 * self.y_speed
        if self.rect.top <= 0:
            self.y_speed = abs(self.y_speed)

    def Up_Key_Event(self):
        self.y_speed = -self.gravitation / 2

    def Blit(self, surface):
        surface.blit(self.image, self.rect)

    def Update_Text (self):
        self.text = self.font.render(self.text_string + str(self.score), True, g.white, False)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.text_center

class Spike(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagini/spike.png")
        self.image = pygame.transform.smoothscale(self.image, (50, 50)) 
        self.rect = self.image.get_rect()
        self.rect.centery = y
        if x == 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.left = 0
        else:
            self.rect.right = g.surface_size

    def Blit(self, surface):
        surface.blit(self.image, self.rect)

class Second_Game():
    def __init__(self, port):
        g.variables_initialization()
        #generare random, seed pt multiplayer, screen
        random.seed(port)
        self.surface_size = g.surface_size
        self.surface = pygame.Surface((self.surface_size, self.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (800, 450)
        self.running = True
        self.player = Player(g.white, 400, 400)# (g.surface_size/4, 50), "white score:")
        self.player2 = Player(g.brown, 400, 400)#,(g.surface_size/4 * 3, 50), "brown score: ")
        self.spikes_right = pygame.sprite.Group()
        self.spikes_left = pygame.sprite.Group()
        self.test_spike = Spike(100, 400)
        self.spikes_right.add(self.test_spike)
        self.spike_size = 100
        self.time = 0
        self.lost = 1
        pygame.mixer.music.load('sunete/2.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.background = pygame.image.load("imagini/first.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400,400)

    def Blit_Images(self):
        self.surface.blit(self.background, self.background_rect)
        self.player.Blit(self.surface)
        self.player2.Blit(self.surface)
        self.spikes_right.draw(self.surface)
        self.spikes_left.draw(self.surface)
        #self.surface.blit(self.player.text, self.player.text_rect)
        #self.surface.blit(self.player2.text, self.player2.text_rect)
        g.screen.blit(self.surface, self.surface_rect)
        pygame.display.flip()
    
    def Spike_Generation(self, side):
        if side == "right":
            self.spikes_right = pygame.sprite.Group()
        else:
            self.spikes_left = pygame.sprite.Group()
        for i in range(1, 8):
            generate_spike = bool(random.getrandbits(1))
            if generate_spike == True:
                if side == "right":
                    spike = Spike(g.surface_size, self.spike_size * i + self.spike_size / 2 )
                    self.spikes_right.add(spike)
                else:
                    spike = Spike(0, self.spike_size * i + self.spike_size / 2 )
                    self.spikes_left.add(spike)

    def Check_Sprite_Collision(self, q_listen, q_send):
        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.spikes_right, False)
        if blocks_hit_list :
            self.player.score = 0
            packet = ("close", self.player.rect.center, self.player.score, False)
            for i in range (0, 5):
                q_send.append(packet)
            self.running = False
            self.lost = 0
        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.spikes_left, False)
        if blocks_hit_list :
            self.player.score = 0
            packet = ("close", self.player.rect.center, self.player.score, False)
            for i in range (0, 5):
                q_send.append(packet)
            self.lost = 0
            self.running = False

    def Update(self, q_listen, q_send):
        dt = g.clock.tick(60) / 1000
        if self.player.touched_left == True:
            self.player.score += 1
            side = "right"
            self.Spike_Generation(side)
            self.player.touched_left = False
            self.player.x_speed += self.player.x_speed * 0.01
            self.player.gravitation += self.player.gravitation * 0.01
            #self.player.Update_Text()
        if self.player.touched_right == True:
            side = "left"
            self.player.score += 1
            self.Spike_Generation(side)
            self.player.touched_right = False
            self.player.x_speed += self.player.x_speed * 0.01
            self.player.gravitation += self.player.gravitation * 0.01
            #self.player.Update_Text()
        self.player.Update(dt)
        #------------------------connection
        self.time += dt
        if self.time >= 0.03:
            packet = ("minigame", self.player.rect.center, self.player.score, True)
            q_send.append(packet)
            self.time = 0
        if q_listen:
            data = q_listen[0]
            if data[0] == "minigame":
                self.player2.rect.center = data[1]
                self.player2.score = data[2]
                self.running = data[3]
                #self.player2.Update_Text()
                q_listen.popleft()
            else:
                if data[0] == "close":
                    self.running = False
                else:
                    q_listen.popleft()
    
    def Check_Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.Up_Key_Event()

    def Loop(self, q_listen, q_send):
        while self.running == True:
            self.Check_Events()
            self.Update(q_listen, q_send)
            self.Check_Sprite_Collision(q_listen, q_send)
            self.Blit_Images()
        return self.lost
        pygame.mixer.music.stop()

#connection = Connection()
#second_game = Second_Game(connection.port)
#second_game.Loop(connection)

