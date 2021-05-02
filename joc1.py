import pygame
import sys
import random
import global_variables as g
from connection import Connection
import math

pygame.init()

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
        self.new_image = self.image
    
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

class Heart(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagini/heart.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = 100

class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.size = 60
        if color == g.white:
            self.image = pygame.image.load("imagini/white_tank.png")
        else:
            self.image = pygame.image.load("imagini/brown_tank.png")
        self.rect = self.image.get_rect()
        self.rect.center=(200, 150)
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
        self.padding = 20

        self.collision = True
        self.life = pygame.sprite.Group()
        self.invincibility = 3


    def Jump(self):
        self.y_speed = -850
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
        if self.collision:
            for platform in platforms_collided:
                if self.rect.right > platform.rect.left or self.rect.left < platform.rect.right:
                    if self.rect.bottom < platform.rect.top + self.padding:
                        self.rect.bottom = platform.rect.top
                        self.jumped = False
                        self.y_speed = 0
#................................

class Platform_Surface (pygame.sprite.Sprite):
    def __init__ (self, top, platform_group):
        pygame.sprite.Sprite.__init__(self)
        global surface_size
        self.n = 4
        self.n_size = g.surface_size // self.n

        self.image = pygame.Surface((g.surface_size, self.n_size))

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

class First_Game():
    def __init__(self, port):
        #generarea seedului pt random. In varianta multiplayer o sa fie trimis de server
        random.seed(port)
        g.variables_initialization()
        self.surface = pygame.Surface((g.surface_size, g.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (800, 450)
        self.player = Player(g.white)
        heart = Heart(50)
        self.player.life.add(heart)
        heart = Heart(100)
        self.player.life.add(heart)
        heart = Heart(150)
        self.player.life.add(heart)

        self.player2 = Player(g.brown)
        heart = Heart(650)
        self.player2.life.add(heart)
        heart = Heart(700)
        self.player2.life.add(heart)
        heart = Heart(750)
        self.player2.life.add(heart)
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
        self.enemy_bullets = []

        self.platform_surface = Platform_Surface(600 , self.platform_group)
        self.surface_group.add(self.platform_surface)
    

        self.running = True
        self.platform_group.add(Platform(200, 200))
        self.dt = 0
        self.time = 0
        
        self.enemy_life = []

        self.bullet_image = pygame.image.load("imagini/bullet.png")
        self.heart_image = pygame.image.load("imagini/heart.png")

        self.background = pygame.image.load("imagini/second.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400,400)

        self.score = 1
        self.scroll_speed = 0
        pygame.mixer.music.load('sunete/1.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def Blit_Images(self, q_send):
        #de la main game
        #g.screen.fill(g.white)
        #de la joc
        self.surface.blit(self.background, self.background_rect)
        self.surface.blit(self.bottom.image, self.bottom.rect)
        self.platform_group.draw(self.surface)
        self.player2.Blit(self.surface)
        self.player.Blit(self.surface)
        for bullet in self.enemy_bullets:
            bullet_rect = self.bullet_image.get_rect()
            bullet_rect.center = bullet
            if bullet_rect.colliderect(self.player.rect):
                all_hearts = self.player.life.sprites()
                if self.player.invincibility <= 0:
                    if len(all_hearts) > 1:
                        for heart in self.player.life:
                            heart.kill()
                            break
                        self.player.invincibility = 1
                    else:
                        q_send.clear()
                        q_send.append(("close",""))
                        q_send.append(("close",""))
                        q_send.append(("close",""))
                        self.running = False
                        self.score = 0
            self.surface.blit(self.bullet_image, bullet_rect)
        for heart in self.enemy_life:
            self.surface.blit(self.heart_image, (heart[0]+500, heart[1]))
        self.player.life.draw(self.surface)
        g.screen.blit(self.surface, self.surface_rect)

    
    def Check_Collisions(self, q_send):
        if pygame.sprite.collide_rect(self.player, self.bottom):
            q_send.clear()
            q_send.append(("close", ""))
            q_send.append(("close", ""))
            q_send.append(("close", ""))
            q_send.append(("close", ""))
            q_send.append(("close", ""))
            self.running = False
            self.score = 0
            #self.player.rect.bottom = 799
            #self.jumped = False
        self.platforms_collided = pygame.sprite.spritecollide(self.player, self.platform_group, False)
        for platform in self.platform_group:
            pygame.sprite.spritecollide(platform, self.player.gun.bullets, True)
        self.player.Platform_Collision(self.platforms_collided)
    

    def Updates(self, pos, q_send, q_listen):
        self.time += self.dt
        if self.player.invincibility > 0:
            self.player.invincibility -= self.dt
        self.player.Update(self.dt,pos)
        self.Check_Collisions(q_send)
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
        if self.time > 0.03:
            send_bullets_rect = []
            send_heart_rect = []
            for heart in self.player.life:
                send_heart_rect.append(heart.rect.center)
            for bullet in self.player.gun.bullets:
                send_bullets_rect.append(bullet.rect.center)
            packet = ("minigame", self.player.rect.center, self.player.gun.angle, send_bullets_rect, send_heart_rect)
            q_send.append(packet)
            self.time = 0
        if q_listen:
            data = q_listen[0]
            if data[0] == "minigame":
                angle = data[2]
                self.player2.gun.new_image = pygame.transform.rotate(self.player2.gun.image, angle)
                self.player2.gun.rect = self.player2.gun.new_image.get_rect()
                self.player2.rect.center = data[1]
                self.player2.gun.rect.center = data[1]
                self.enemy_bullets = data[3]
                self.enemy_life = data[4]
            elif data[0] == "close":
                self.running = False
            q_listen.popleft()
        

    def Quit_Event(self, event):
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def Keydown_Events(self,event):
        if (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE) and self.player.jumped == False :
            self.player.Jump()
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.move_right = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.move_left = True
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.player.collision = False
    
    def Keyup_Events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.player.move_right = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.player.move_left = False
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.player.collision = True

    def Events(self):
        for event in pygame.event.get():
            self.Quit_Event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player.gun.wait_to_fire <= 0:
                    self.player.gun.Fire()
                    self.player.gun.wait_to_fire = 0.7
            if event.type == pygame.KEYDOWN:
                self.Keydown_Events(event)
            if event.type == pygame.KEYUP:
                self.Keyup_Events(event)

    def Loop(self, q_listen, q_send):
        while self.running:
            pos = pygame.mouse.get_pos()
            self.dt = g.clock.tick(60) / 1000
            self.Events()
            self.Updates(pos, q_send, q_listen)
            self.Blit_Images(q_send)
            pygame.display.flip()
        return self.score
        pygame.mixer.music.stop()


#connection = Connection()     
#first_game = First_Game()
#first_game.Loop(connection.q_listen, connection.q_send)
