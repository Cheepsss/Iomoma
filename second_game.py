import pygame
import random
import sys
pygame.init()

import global_variables as g


class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.size = 60
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.gravitation = 10
        self.y_speed = 0
        self.x_speed = 300

        self.touched_left = False
        self.touched_right = False
        
        self.jump_sound = pygame.mixer.Sound("sunete/jump_sound.wav")

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
        pygame.mixer.Sound.play(self.jump_sound)

    def Blit(self, surface):
        surface.blit(self.image, self.rect)

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
    def __init__(self):
        g.variables_initialization()
        #generare random, seed pt multiplayer, screen
        random.seed(a=None, version=2)
        self.surface_size = g.surface_size
        self.surface = pygame.Surface((self.surface_size, self.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (900, 450)
        self.running = True
        self.player = Player(g.white, 400, 400)
        self.spikes_right = pygame.sprite.Group()
        self.spikes_left = pygame.sprite.Group()
        self.test_spike = Spike(100, 400)
        self.spikes_right.add(self.test_spike)
        self.exit_button = pygame.image.load("imagini/exit_button.png")
        self.exit_button = pygame.transform.smoothscale(self.exit_button,(100,100))
        self.exit_button_rect = self.exit_button.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.score = 0
        self.text = self.font.render("Score: " + str(self.score), True, g.white, False)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (g.surface_size/2, 50)

        self.spike_size = 100
        pygame.mixer.music.load('sunete/2.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.background = pygame.image.load("imagini/second.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400,400)

    def Blit_Images(self):
        self.surface.blit(self.background, self.background_rect)
        self.player.Blit(self.surface)
        self.spikes_right.draw(self.surface)
        self.spikes_left.draw(self.surface)
        self.surface.blit(self.text, self.text_rect)
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

    def Check_Sprite_Collision(self):
        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.spikes_right, False)
        if blocks_hit_list :
            self.running = False
        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.spikes_left, False)
        if blocks_hit_list :
            self.running = False

    def Update(self):
        dt = g.clock.tick(60) / 1000
        self.Check_Sprite_Collision()
        if self.player.touched_left == True:
            self.score += 1
            side = "right"
            self.Spike_Generation(side)
            self.player.touched_left = False
            self.player.x_speed += self.player.x_speed * 0.01
            self.player.gravitation += self.player.gravitation * 0.01
            #update text
            self.text = self.font.render("Score: " + str(self.score), True, g.white, False)
            self.text_rect = self.text.get_rect()
            self.text_rect.center = (g.surface_size/2, 50)
        if self.player.touched_right == True:
            side = "left"
            self.score += 1
            self.Spike_Generation(side)
            self.player.touched_right = False
            self.player.x_speed += self.player.x_speed * 0.01
            self.player.gravitation += self.player.gravitation * 0.01
            #update text
            self.text = self.font.render("Score: " + str(self.score), True, g.white, False)
            self.text_rect = self.text.get_rect()
            self.text_rect.center = (g.surface_size/2, 50)
        self.player.Update(dt)
    
    def Check_Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    self.player.Up_Key_Event()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 1515 and pos[0] <= 1585 and pos[1] >=785 and pos[1] <= 859:
                        self.running = False
    def Loop(self):
        while self.running == True:
            self.Check_Events()
            self.Update()
            self.Blit_Images()
        pygame.mixer.music.stop()
        return self.score


