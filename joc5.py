import pygame
import sys
import random
from connection import Connection
pygame.init()

import global_variables as g

#de sters, o sa fie initializat in main game
g.screen = pygame.display.set_mode([1600, 900])

class Text():
    def __init__(self, x, y, points, player):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.player = player
        self.x = x
        self.y = y
        self.text = self.font.render(self.player + " score: " + str(points), True, g.white, False)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
    
    def Update(self, points):
        self.text = self.font.render(self.player + " score: " + str(points), True, g.white, False)
        self.rect = self.text.get_rect()
        self.rect.center = (self.x, self.y)
    
    def Draw(self, surface):
        surface.blit(self.text, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__ (self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.size = 32
        self.image = pygame.image.load("imagini/map_tile.png")
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

class Coin(pygame.sprite.Sprite):
    def __init__ (self, x, y, platform_size):
        pygame.sprite.Sprite.__init__(self)
        self.size = 10
        self.image = pygame.image.load("imagini/coin.png")
        self.rect = self.image.get_rect()
        self.rect.centery = y + platform_size / 2
        self.rect.centerx = x + platform_size / 2

class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.size = 25
        if color == g.white:
            self.image = pygame.image.load("imagini/pacman_white.png")
        else:
            self.image = pygame.image.load("imagini/pacman_brown.png")
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        self.speed = 150
    
    def Draw(self, surface):
        if self.rect.right >= 70 and self.rect.right <= 730:
            surface.blit(self.image, self.rect)
    
    def Update(self, dt):
        if self.rect.right < 64:
            self.rect.left = 736
        if self.rect.left > 736:
            self.rect.left = 64
        if self.moving_left:
            self.rect.centerx -= self.speed * dt
        if self.moving_right:
            self.rect.centerx += self.speed * dt
        if self.moving_up:
            self.rect.centery -= self.speed * dt
        if self.moving_down:
            self.rect.centery += self.speed * dt

class Ghost(pygame.sprite.Sprite):
    def __init__ (self, x, y, id1):
        pygame.sprite.Sprite.__init__(self)
        self.size = 25
                                        #            ^
        self.direction = 1              #          1sus
                                        # < 2 stanga    dreapta 4 >
                                        #         3 jos
                                        #           V
        self.id = id1
        if self.id == 1:
            self.image = pygame.image.load("imagini/green_ghost.png")
        if self.id == 2:
            self.image = pygame.image.load("imagini/red_ghost.png")
        if self.id == 3:
            self.image = pygame.image.load("imagini/pink_ghost.png")
        if self.id == 4:
            self.image = pygame.image.load("imagini/blue_ghost.png")
        
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y  

        self.speed = 150
    
    def Update(self, dt):
        if self.direction == 1 :
            self.rect.centery -= self.speed * dt
        if self.direction == 2:
            self.rect.centerx -= self.speed * dt
        if self.direction == 3:
            self.rect.centery += self.speed * dt
        if self.direction == 4:
            self.rect.centerx += self.speed * dt
    
    def Change_Direction(self):
        self.direction = random.randrange(1, 5)
        

class Fifth_Game():
    def __init__(self, port):
        g.variables_initialization()
        pygame.mixer.music.load('sunete/pac_theme.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        random.seed(port)
        self.surface_size = g.surface_size
        self.surface = pygame.Surface((self.surface_size, self.surface_size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (900, 450)
        self.running = True
        self.dt = 0
        self.background = pygame.image.load("imagini/pac_background.png")
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (400, 400)
        self.coin_sound = pygame.mixer.Sound("sunete/circle_hit.wav")
        self.crash_sound = pygame.mixer.Sound("sunete/crash.wav")

        self.platform_size = 32
        self.player = Player(g.white, 384, 640)
        self.player2 = Player(g.brown, 384, 640)
        self.invincibility = 0

        self.map = []
        self.map.append(['m', 'm', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', 'm', '#', ' ', '#', 'm', '#', ' ', '#', ' ', '#', 'm', '#', ' ', '#', 'm', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', '#', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', '#', '#', 'm', 'm'])
        self.map.append(['m', 'm', 'm', 'm', 'm', 'm', '#', ' ', '#', ' ', ' ', ' ', 'm', ' ', ' ', ' ', '#', ' ', '#', 'm', 'm', 'm', 'm', 'm', 'm'])
        self.map.append(['m', 'm', 'm', 'm', 'm', 'm', '#', ' ', '#', ' ', '#', 'm', 'm', 'm', '#', ' ', '#', ' ', '#', 'm', 'm', 'm', 'm', 'm', 'm'])
        self.map.append(['@', '@', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', 'm', 'm', 'm', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '@', '@'])
        self.map.append(['@', 'm', 'm', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'm', 'm', 'm', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'm', 'm', '@'])
        self.map.append(['@', '@', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '@', '@'])
        self.map.append(['m', 'm', 'm', 'm', 'm', 'm', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', 'm', 'm', 'm', 'm', 'm', 'm'])
        self.map.append(['m', 'm', 'm', 'm', 'm', 'm', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', 'm', 'm', 'm', 'm', 'm', 'm'])
        self.map.append(['m', 'm', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'm', 'm'])
        self.map.append(['m', 'm', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', 'm', 'm'])


        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

        ghost = Ghost(380,380,1)
        self.ghosts.add(ghost)
    
        ghost = Ghost(390,430,2)
        self.ghosts.add(ghost)
        
        ghost = Ghost(400,410,3)
        self.ghosts.add(ghost)

        """
        ghost = Ghost(400,370,4)
        self.ghosts.add(ghost)
        """
        

        x = 0
        y = 0

        for i in self.map:
            for j in i:
                if j == '#':
                    platform = Platform(x * self.platform_size, y * self.platform_size, g.blue)
                    self.platforms.add(platform)
                if j == '@':
                    platform = Platform(x * self.platform_size, y * self.platform_size, g.black)
                    self.platforms.add(platform)
                if j == ' ':
                    coin = Coin(x * self.platform_size, y* self.platform_size, self.platform_size)
                    self.coins.add(coin)

                x += 1
            y += 1
            x = 0
        
        self.points = 0
        self.enemy_points = 0
        self.text = Text(200, 25, self.points, "White")
        self.enemy_text = Text(600, 25, self.points, "Brown")
        self.time = 0


    
    def Blit_Images(self):
        self.surface.blit(self.background, self.background_rect)
        self.player2.Draw(self.surface)
        self.player.Draw(self.surface)
        self.coins.draw(self.surface)
        self.ghosts.draw(self.surface)
        self.platforms.draw(self.surface)
        self.text.Draw(self.surface)
        self.enemy_text.Draw(self.surface)
        g.screen.blit(self.surface, self.surface_rect)
        pygame.display.flip()
    
    def Update(self, q_send, q_listen):
        self.time += self.dt
        if self.time > 0.03:
            packet = ("minigame", self.player.rect.center, self.points)
            self.time = 0
            q_send.append(packet)
        if q_listen:
            data = q_listen[0]
            if data[0] == "close":
                self.running = False
            else:
                if data[0] == "minigame":
                    self.player2.rect.center = data[1]
                    self.enemy_points = data[2]
                q_listen.popleft()
        self.text.Update(self.points)
        self.enemy_text.Update(self.enemy_points)
        if self.invincibility > 0:
            self.invincibility -= self.dt
        self.player.Update(self.dt)
        for ghost in self.ghosts:
            ghost.Update(self.dt)
        if not self.coins:
            q_send.append(("close",""))
            q_send.append(("close",""))
            q_send.append(("close",""))
            q_send.append(("close",""))
            self.running = False

    def Check_Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.moving_up = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.moving_right = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.moving_left = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.moving_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.moving_left  = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.moving_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.moving_down = False
    
    def Check_Collision(self):
        for platform in self.platforms:
            if platform.rect.colliderect(self.player.rect):
                if self.player.rect.bottom - 5  > platform.rect.top and self.player.rect.top < platform.rect.bottom - 5:
                    if self.player.rect.left < platform.rect.right and self.player.rect.centerx > platform.rect.centerx:
                        self.player.rect.left = platform.rect.right + 1
                    if self.player.rect.right > platform.rect.left and self.player.rect.centerx < platform.rect.centerx:
                        self.player.rect.right = platform.rect.left - 1
                else:
                    if self.player.rect.top <= platform.rect.bottom and self.player.rect.centery >= platform.rect.centery:
                        self.player.rect.top = platform.rect.bottom + 1
                    if self.player.rect.bottom >= platform.rect.top and self.player.rect.centery <= platform.rect.centery:
                        self.player.rect.bottom = platform.rect.top - 1
        for ghost in self.ghosts:
            if self.invincibility <= 0:
                if self.player.rect.colliderect(ghost.rect):
                    pygame.mixer.Sound.play(self.crash_sound)
                    self.points -= 5
                    self.invincibility = 0.3
            for platform in self.platforms:
                if platform.rect.colliderect(ghost.rect):
                    if ghost.rect.bottom - 5  > platform.rect.top and ghost.rect.top < platform.rect.bottom - 5:
                        if ghost.rect.left < platform.rect.right and ghost.rect.centerx > platform.rect.centerx:
                            ghost.rect.left = platform.rect.right + 1
                            ghost.Change_Direction()
                        elif ghost.rect.right > platform.rect.left and ghost.rect.centerx < platform.rect.centerx:
                            ghost.rect.right = platform.rect.left - 1
                            ghost.Change_Direction()
                    else:
                        if ghost.rect.top <= platform.rect.bottom and ghost.rect.centery >= platform.rect.centery:
                            ghost.rect.top = platform.rect.bottom + 1
                            ghost.Change_Direction()
                        elif ghost.rect.bottom >= platform.rect.top and ghost.rect.centery <= platform.rect.centery:
                            ghost.rect.bottom = platform.rect.top - 1
                            ghost.Change_Direction()
        pygame.sprite.spritecollide(self.player2, self.coins, True)
        coins_taken = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coins_taken:
            pygame.mixer.Sound.play(self.coin_sound)
            self.points += 1

    def Loop(self, q_listen, q_send):
        while self.running == True:
            self.dt = g.clock.tick(60) / 1000
            self.Check_Events()
            self.Update(q_send, q_listen)
            self.Check_Collision()
            self.Blit_Images()
        pygame.mixer.music.stop()
        if self.points > self.enemy_points:
            return 1
        else:
            return 0



#connection = Connection()
#fifth_game = Fifth_Game(connection.port)
#fifth_game.Loop(connection.q_listen, connection.q_send)

