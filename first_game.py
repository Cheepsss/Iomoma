import pygame
import sys
import random
import global_variables as g
import math

#pygame.init()

#g.screen = pygame.display.set_mode([1600, 900])

class Bottom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((g.surface_size, 10))
        self.image.fill((128,255,40))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = g.surface_size - 2


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagini/platform.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def Update_Position(self, add, dt):
        if add < 0:
            self.rect.centery+= -(add * dt)
    
    def Update_Position(self, add, dt):
        if add < 0:
            self.rect.centery+= -(add * dt)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, player_x, player_y):
        pygame.sprite.Sprite.__init__(self)
        radians = math.radians(angle)
        self.image = pygame.image.load("imagini/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (player_x, player_y)
        self.angle = angle
        self.sin = math.sin(radians)
        self.cos = math.cos(radians)
        self.size = 5
    
    def Update(self, dt):
        self.rect.centery -= self.sin * self.size 
        self.rect.centerx += self.cos * self.size 
        self.size += 2 * dt
        if self.rect.centerx > 800 or self.rect.centerx < 0 or self.rect.centery > 800 or self.rect.centery < 0:
            self.kill()



class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):  
        pygame.sprite.Sprite.__init__(self)    
        self.image = pygame.image.load("imagini/gun.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = 0
        self.bullets = pygame.sprite.Group()
        self.wait_to_fire = 0.5
        self.new_image = 0
    
    def Fire(self):
        bullet = Bullet(self.angle, self.rect.centerx, self.rect.centery)
        self.bullets.add(bullet)

    def Update(self, pos, player_x, player_y, dt):
        for bullet in self.bullets:
            bullet.Update(dt)
        pos_x = pos[0] - 400
        pos_y = pos[1] - 50
        if pos_x >= player_x and pos_y >= player_y:
            x = pos_x - player_x
            y = pos_y - player_y
            sin = math.sqrt(x * x + y * y)
            sin =  y / sin
            self.angle = 360 - math.degrees(math.asin(sin)) 
        else:
            if pos_x <= player_x and pos_y <= player_y:
                x = player_x - pos_x
                y = player_y - pos_y
                sin = math.sqrt(x * x + y * y)
                sin =  y / sin
                self.angle = 180 - math.degrees(math.asin(sin))
            else:
                if pos_x > player_x and pos_y < player_y:
                    x = pos_x - player_x
                    y = player_y - pos_y
                    sin = math.sqrt(x * x + y * y)
                    sin =  y / sin
                    self.angle =  math.degrees(math.asin(sin))
                else: 
                    if pos_x < player_x and pos_y > player_y:
                        y = pos_y - player_y
                        x = player_x - pos_x
                        sin = math.sqrt(x * x + y * y)
                        sin =  y / sin
                        self.angle =  180 + math.degrees(math.asin(sin))
                    else:
                        self.angle = 0

        self.new_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.new_image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.size = 60
        self.image = pygame.image.load("imagini/white_tank.png")
        self.rect = self.image.get_rect()
        self.rect.center=(500, 500)
        self.y_acceleration = 1500 #acceleratia gravitationala
        self.y_speed = 10
        self.starting_y_speed = 10
        self.starting_x_speed = 300
        self.x_speed = 0
        self.jumped = True
        self.move_left = False
        self.move_right = False
        self.friction = 0.2
        self.gun = Gun(400, 400)

        self.y_change = 0
        self.padding = 10

    def Jump(self):
        self.y_speed = -700
        self.jumped = True

    def Update(self, dt, pos):
        self.gun.Update(pos, self.rect.centerx, self.rect.centery, dt)
        if self.gun.wait_to_fire > 0:
            self.gun.wait_to_fire -= dt
        self.x_speed *= self.friction
        if int(self.x_speed) == 0:
            self.x_speed = 0
        if self.move_right == True:
            self.x_speed = self.starting_x_speed * dt
        if self.move_left == True:
            self.x_speed = -self.starting_x_speed * dt
        self.rect.centerx +=self.x_speed 
        self.y_speed += self.y_acceleration * dt
        self.y_change = self.y_speed * dt 
        self.rect.centery += self.y_change

        if self.move_right and self.rect.right > 800:
            self.rect.right = 800
        
        if self.move_left and self.rect.left < 0:
            self.rect.left = 0
    
    def Blit(self, surface):
        surface.blit(self.image, self.rect)
        self.gun.rect.center = self.rect.center
        surface.blit(self.gun.new_image, self.gun.rect)
        self.gun.bullets.draw(surface)

    def Platform_Collision(self, platforms_collided):
            for platform in platforms_collided:
                if self.rect.right > platform.rect.left or self.rect.left < platform.rect.right:
                    if self.rect.bottom < platform.rect.top + self.padding:
                        self.rect.bottom = platform.rect.top
                        self.jumped = False
                        self.y_speed = 0
                    elif self.rect.top >= platform.rect.bottom - self.padding:
                        self.rect.top = platform.rect.bottom
                        self.y_speed = -self.y_speed
                if (platform.rect.top < self.rect.bottom and platform.rect.top > self.rect.top) or (platform.rect.bottom < self.rect.bottom and platform.rect.bottom > self.rect.top):
                    if self.rect.right > platform.rect.left and self.rect.left < platform.rect.left and self.move_right == True:
                        self.rect.right = platform.rect.left
                        self.y_speed = 0 
                        self.jumped = False
                    elif self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                        self.rect.left = platform.rect.right
                        self.y_speed = 0 
                        self.jumped = False

#................................

class Platform_Surface (pygame.sprite.Sprite):
    def __init__ (self, top, platform_group):
        pygame.sprite.Sprite.__init__(self)
        global surface_size
        self.n = 4
        self.n_size = g.surface_size // self.n

        self.image = pygame.Surface((g.surface_size, self.n_size))
        #self.image.fill((115, 198, 0)) # verde

        self.rect = self.image.get_rect()
        self.rect.centerx = g.surface_size / 2
        self.rect.top = top


        for i in range (0, self.n):
            self.x = random.randrange(20, self.n_size - 20)
            self.y = random.randrange(20, self.n_size - 20)
            self.x += i * self.n_size
            self.y += self.rect.top
            self.p = Platform(self.x, self.y)
            platform_group.add(self.p)

    def Update(self, add):
        self.rect.y += add 


#....................... 

class Jump_Game():
    def __init__(self):
        #generarea seedului pt random. In varianta multiplayer o sa fie trimis de server
        random.seed(a=None, version=2)
        g.variables_initialization()
        self.surface = pygame.Surface((g.surface_size, g.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (800, 450)
        self.player = Player(g.gray)
        self.bottom = Bottom()
        
        self.platform_group = pygame.sprite.Group()
        self.platforms_collided = pygame.sprite.Group()

        #temporar
        self.surface_group = pygame.sprite.Group()

        self.platform_surface = Platform_Surface(-200, self.platform_group)
        self.surface_group.add(self.platform_surface)

        self.platform_surface = Platform_Surface(0 , self.platform_group)
        self.surface_group.add(self.platform_surface)

        self.platform_surface = Platform_Surface(200 , self.platform_group)
        self.surface_group.add(self.platform_surface)

        self.platform_surface = Platform_Surface(400 , self.platform_group)
        self.surface_group.add(self.platform_surface)


        self.platform_surface = Platform_Surface(600 , self.platform_group)
        self.surface_group.add(self.platform_surface)
    

        self.running = True
        self.platform_group.add(Platform(500, 700))
        self.scroll_speed = 100
        self.dt = 0
        pygame.mixer.music.load('sunete/1.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.background = pygame.image.load("imagini/first.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400,400)

    def Blit_Images(self):
        #de la main game
        #g.screen.fill(g.white)
        #de la joc
        self.surface.blit(self.background, self.background_rect)
        self.surface.blit(self.bottom.image, self.bottom.rect)
        self.platform_group.draw(self.surface)
        self.player.Blit(self.surface)
        g.screen.blit(self.surface, self.surface_rect)
    
    def Check_Collisions(self):
        if pygame.sprite.collide_rect(self.player, self.bottom):
            self.running = False
            #self.player.rect.bottom = 799
            #self.jumped = False
        self.platforms_collided = pygame.sprite.spritecollide(self.player, self.platform_group, False)
        for platform in self.platform_group:
            pygame.sprite.spritecollide(platform, self.player.gun.bullets, True)
        self.player.Platform_Collision(self.platforms_collided)
    

    def Updates(self, pos):
        
        self.player.Update(self.dt,pos)
        self.Check_Collisions()
        add = self.scroll_speed * self.dt
        for p in self.platform_group:
            p.rect.y += add
            if p.rect.top > 800:
                self.platform_group.remove(p)
        for surface in self.surface_group:
            surface.Update(add)
            if surface.rect.top >= 800:
                self.platform_surface = Platform_Surface(-800 / 4, self.platform_group)
                self.surface_group.add(self.platform_surface)
                self.surface_group.remove(surface)

    def Quit_Event(self, event):
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def Keydown_Events(self,event):
        if (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE) and self.player.jumped == False:
            self.player.Jump()
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.move_right = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.move_left = True
    
    def Keyup_Events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.move_right = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.move_left = False

    def Events(self):
        for event in pygame.event.get():
            self.Quit_Event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 1515 and pos[0] <= 1585 and pos[1] >=785 and pos[1] <= 859:
                        self.running = False
                if self.player.gun.wait_to_fire <= 0:
                    self.player.gun.Fire()
                    self.player.gun.wait_to_fire = 1
            if event.type == pygame.KEYDOWN:
                self.Keydown_Events(event)
            if event.type == pygame.KEYUP:
                self.Keyup_Events(event)

    def Loop(self):
        while self.running:
            pos = pygame.mouse.get_pos()
            self.dt = g.clock.tick(60) / 1000
            self.Events()
            self.Updates(pos)
            self.Blit_Images()
            pygame.display.flip()
        pygame.mixer.music.stop()

        
#jump_game = Jump_Game()
#jump_game.Loop()