import pygame, sys, time
import first_game
import second_game
import third_game
import forth_game
import fifth_game
import global_variables as g
from pygame.locals import *
from connection import Connection
import pygame_textinput

from joc1 import First_Game as Joc1
from joc2 import Second_Game as Joc2
from joc3 import Third_Game as Joc3
from joc4 import Forth_Game as Joc4
from joc5 import Fifth_Game as Joc5

pygame.init()
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

#sper sa va placa jocul meu ^^

class Player():
    def __init__(self, color):
        if color == "white":
            self.player_image = pygame.image.load("imagini/white_player/idle0.png")
        else:
            self.player_image = pygame.image.load("imagini/brown_player/idle0.png")
        self.player_image = pygame.transform.smoothscale(self.player_image, (250, 400))
        self.player_rect = self.player_image.get_rect()
        self.player_rect.center = (800,600)
        self.frame_number_right = 0
        self.frame_number_left = 0
        self.moving_left = False
        self.moving_right = False
        self.frame_number = 0
        self.score = 0
        if color == "white":
            path_left = "imagini/white_player/walk_right/walking"
            path_right = "imagini/white_player/walk_left/walking"

        else:
            path_left = "imagini/brown_player/walk_right/walking"
            path_right = "imagini/brown_player/walk_left/walking"
        #animatie miscare spre dreapta
        self.walk_right = []
        for i in range (0,8):
            self.nume_img = path_left + str(i) + ".png"
            self.img = pygame.image.load(self.nume_img)
            self.img= pygame.transform.smoothscale(self.img, (250, 400))
            self.walk_right.append(self.img)
        
        #animatie miscare spre stanga
        self.walk_left = []
        for i in range (0,8):
            self.nume_img = path_right + str(i) + ".png"
            self.img = pygame.image.load(self.nume_img)
            self.img= pygame.transform.smoothscale(self.img, (250, 400))
            self.walk_left.append(self.img)

    def Move(self, dt):
        if self.moving_left == True and self.player_rect.x >= 0:
            self.player_rect.x -= 200 * dt
            self.frame_number_left +=0.5
            if self.frame_number_left == 8:
                self.frame_number_left = 0
        
        if self.moving_right == True and self.player_rect.x <= SCREEN_WIDTH - 250:
            self.player_rect.x += 200 * dt
            self.frame_number_right +=0.5
            if self.frame_number_right == 8:
                self.frame_number_right = 0
    def Events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_right = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_right = False
                self.frame_number_right = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_left = False
                self.frame_number_left = 0

        
class Single_Player_Main_Game: 
    def __init__(self):
        self.background = pygame.image.load("imagini/background.png")
        self.background = pygame.transform.smoothscale(self.background, (1600, 900))
        self.minigames_button = pygame.image.load("imagini/minigames_menu_button.png")
        self.minigames_button = pygame.transform.smoothscale(self.minigames_button, (500,500))
        self.minigames_button_rect = self.minigames_button.get_rect()
        self.minigames_button_rect.top = 50
        self.minigames_button_rect.centerx = 800 
        self.minigames_menu = pygame.image.load("imagini/minigames_menu.png")
        self.minigames_menu = pygame.transform.smoothscale(self.minigames_menu, (500,500))
        self.minigames_menu_rect = self.minigames_menu.get_rect()
        self.minigames_menu_rect.top = 50
        self.minigames_menu_rect.centerx = 800
        self.exit_button = pygame.image.load("imagini/exit_button.png")
        self.exit_button = pygame.transform.smoothscale(self.exit_button,(100,100))
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_rect.x = 1500
        self.exit_button_rect.y = 770
        self.minigames_button_clicked = False
        self.player1 = Player("white")
        self.event_list = []
        self.file = open("scores.txt", "r")

        self.running = True

        self.scores = []
        for score in self.file:
            self.scores.append(int(score))
        self.file.close()

        self.text1 = Text(800,243,"",15)
        self.text1.Update(self.scores[0])

        self.text2 = Text(937, 243, "", 15)
        self.text2.Update(self.scores[1])

        self.text3 = Text(800, 345, "", 15)
        self.text3.Update(self.scores[2])
        self.click_sound = pygame.mixer.Sound("sunete/button.wav")


    def Blit_Images(self):
        g.screen.blit(self.background,(0,0))
        g.screen.blit(self.exit_button, self.exit_button_rect)
        if self.player1.moving_right == True:
            g.screen.blit(self.player1.walk_right[int(self.player1.frame_number_right)], self.player1.player_rect)
        else:
            if self.player1.moving_left == True:
                g.screen.blit(self.player1.walk_left[int(self.player1.frame_number_left)], self.player1.player_rect)
            else:
                g.screen.blit(self.player1.player_image, self.player1.player_rect)
        if self.minigames_button_clicked == False:
            g.screen.blit(self.minigames_button,self.minigames_button_rect)
        else:
            g.screen.blit(self.minigames_menu, self.minigames_menu_rect)
            g.screen.blit(self.text1.text, self.text1.rect)
            g.screen.blit(self.text2.text, self.text2.rect)
            g.screen.blit(self.text3.text, self.text3.rect)

    def Loop(self):
        while self.running:
            dt = g.clock.tick(60) / 1000
            self.event_list = pygame.event.get()
            for event in self.event_list:
                self.player1.Events(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.minigames_button_clicked == True:
                        if pos[0] >= 980 and pos[0] <= 1030 and pos[1] >= 480 and pos[1] <= 540:
                            self.minigames_button_clicked = False
                            pygame.mixer.Sound.play(self.click_sound)
                        if pos[0] >= 615 and pos[0] <= 725 and pos[1] >= 150 and pos[1] <= 225:
                            pygame.mixer.Sound.play(self.click_sound)
                            pygame.mixer.music.stop()
                            jump_game = first_game.Jump_Game()
                            jump_game.Loop()
                            pygame.mixer.music.load('sunete/main_theme.wav')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                        if pos[0] >= 750 and pos[0] <= 860 and pos[1] >= 150 and pos[1] <= 225:
                            pygame.mixer.Sound.play(self.click_sound)
                            pygame.mixer.music.stop()
                            spikes_game = second_game.Second_Game()
                            score = spikes_game.Loop()
                            if score > self.scores[0]:
                                self.scores[0] = score
                                self.file = open("scores.txt", "w")
                                self.file.write(str(score))
                                self.file.close()
                                self.file = open("scores.txt", "a")
                                self.file.write('\n')
                                self.file.write(str(self.scores[1]))
                                self.file.write('\n')
                                self.file.write(str(self.scores[2]))
                                self.text1.Update(score)
                                self.file.close()
                            pygame.mixer.music.load('sunete/main_theme.wav')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                        if pos[0] >= 880 and pos[0] <= 995 and pos[1] >= 150 and pos[1] <= 225:
                            pygame.mixer.Sound.play(self.click_sound)
                            pygame.mixer.music.stop()
                            circle_game = third_game.Third_Game()
                            score = circle_game.Loop()
                            if score > self.scores[1]:
                                self.scores[1] = score
                                self.file = open("scores.txt", "w")
                                self.file.write(str(self.scores[0]))
                                self.file.close()
                                self.file = open("scores.txt", "a")
                                self.file.write('\n')
                                self.file.write(str(self.scores[1]))
                                self.file.write('\n')
                                self.file.write(str(self.scores[2]))
                                self.text2.Update(score)
                                self.file.close()
                            pygame.mixer.music.load('sunete/main_theme.wav')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                        if pos[0] > 615 and pos[0] <= 715 and pos[1] > 260 and pos[1] < 335:
                            pygame.mixer.Sound.play(self.click_sound)
                            pygame.mixer.music.stop()
                            narwal_game = forth_game.Forth_Game()
                            narwal_game.Loop()
                            pygame.mixer.music.load('sunete/main_theme.wav')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                        if pos[0] > 750 and pos[0] <= 860 and pos[1] > 260 and pos[1] < 335:
                            pygame.mixer.Sound.play(self.click_sound)
                            pygame.mixer.music.stop()
                            pac_game = fifth_game.Fifth_Game()
                            score = pac_game.Loop()
                            if score > self.scores[2]:
                                self.scores[2] = score
                                self.file = open("scores.txt", "w")
                                self.file.write(str(self.scores[0]))
                                self.file.close()
                                self.file = open("scores.txt", "a")
                                self.file.write('\n')
                                self.file.write(str(self.scores[1]))
                                self.file.write('\n')
                                self.file.write(str(self.scores[2]))
                                self.text3.Update(score)
                                self.file.close()
                            pygame.mixer.music.load('sunete/main_theme.wav')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                    elif self.minigames_button_clicked == False and pos[0] >= 550 and pos[0] <= 1050  and pos[1] >= 50 and pos[1] <= 125:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.minigames_button_clicked = True
                    if pos[0] >= 1515 and pos[0] <= 1585 and pos[1] >=785 and pos[1] <= 859:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.running = False
            self.player1.Move(dt)
            self.Blit_Images()
            pygame.display.update()

# --------------------------------------------------------------------
class Text():
    def __init__(self,x , y, string, size):
        self.x = x
        self.y = y
        self.string = string
        self.size = size
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        self.text = self.font.render(self.string, False, g.white, False)
        self.rect = self.text.get_rect()
        self.rect.left = self.x
        self.rect.centery = self.y
        self.data = ""
    
    def Update(self, data):
        self.data = str(data)
        self.text = self.font.render(self.string + self.data, False, g.white, False)
        self.rect = self.text.get_rect()
        self.rect.left = self.x
        self.rect.centery = self.y



class Multiplayer_Main_Game():
    def __init__(self):
        self.background = pygame.image.load("imagini/background.png")
        self.background = pygame.transform.smoothscale(self.background, (1600, 900))
        self.player1 = Player("white")
        self.player2 = Player("brown")
        self.event_list = []
        self.running = True
        self.trying_to_connect_image = pygame.image.load("imagini/trying_to_connect.png")
        self.trying_to_connect_rect = self.trying_to_connect_image.get_rect()
        self.trying_to_connect_rect.center = (800, 450)
        self.time = 0
        self.chat_image = pygame.image.load("imagini/chat.png")
        self.chat_image = pygame.transform.smoothscale(self.chat_image, (500, 200))
        self.chat_image_rect = self.chat_image.get_rect()
        self.chat_image_rect.left =10
        self.chat_image_rect.top = 10
        self.chatting = False
        self.send_string = ""
        self.receive_string = ""
        self.exit_button = pygame.image.load("imagini/exit_button.png")
        self.exit_button = pygame.transform.smoothscale(self.exit_button,(100,100))
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_rect.x = 1500
        self.exit_button_rect.y = 770
        self.click_sound = pygame.mixer.Sound("sunete/button.wav")
        

        self.text5 = Text(35, 77, "", 15)
        self.text4 = Text(35, 95, "", 15)
        self.text3 = Text(35, 113, "", 15)
        self.text2 = Text(35, 131, "", 15)
        self.text1 = Text(35, 149, "", 15)


        self.player_score = Text(400, 100, "Your score: ", 35)
        self.enemy_score = Text(900, 100, "Brown's score: ", 35 )

        self.text_input = pygame_textinput.TextInput(text_color = g.white, font_size = 25 , cursor_color = g.white)
        g.screen.blit(self.trying_to_connect_image, self.trying_to_connect_rect)
        pygame.display.update()
        
        self.connection = Connection()
        if not self.connection.q_end:
            self.port = self.connection.port
        self.wait_time = -1
        self.game_number = 1

    def text_swap(self):
        self.text5.string = self.text4.string
        self.text4.string = self.text3.string
        self.text3.string = self.text2.string
        self.text2.string = self.text1.string
        self.text5.Update(self.text4.data)
        self.text4.Update(self.text3.data)
        self.text3.Update(self.text2.data)
        self.text2.Update(self.text1.data)
    

    def Blit_Images(self):
        g.screen.blit(self.background,(0,0))
        g.screen.blit(self.chat_image, self.chat_image_rect)
        g.screen.blit(self.text1.text, self.text1.rect)
        g.screen.blit(self.text2.text, self.text2.rect)
        g.screen.blit(self.text3.text, self.text3.rect)
        g.screen.blit(self.text4.text, self.text4.rect)
        g.screen.blit(self.text5.text, self.text5.rect)
        g.screen.blit(self.player_score.text, self.player_score.rect)
        g.screen.blit(self.exit_button, self.exit_button_rect)
        g.screen.blit(self.enemy_score.text, self.enemy_score.rect)
        if self.chatting:
            g.screen.blit(self.text_input.get_surface(), (35, 177))
        if self.player2.moving_right:
            g.screen.blit(self.player2.walk_right[int(self.player2.frame_number)], self.player2.player_rect)
        else:
            if self.player2.moving_left:
                g.screen.blit(self.player2.walk_left[int(self.player2.frame_number)], self.player2.player_rect)
            else:
                g.screen.blit(self.player2.player_image, self.player2.player_rect)
        if self.player1.moving_right:
            g.screen.blit(self.player1.walk_right[int(self.player1.frame_number_right)], self.player1.player_rect)
        else:
            if self.player1.moving_left:
                g.screen.blit(self.player1.walk_left[int(self.player1.frame_number_left)], self.player1.player_rect)
            else:
                g.screen.blit(self.player1.player_image, self.player1.player_rect)
    
    def Update(self):
        if self.connection.q_end:
            self.running = False
        self.player_score.Update(self.player1.score)
        dt = g.clock.tick(60) / 1000
        self.time += dt
        if self.wait_time != -1:
            self.wait_time += dt
        else: 
            self.wait_time = 0
        if self.wait_time >= 15:
            self.player1.moving_right = False
            self.player1.moving_left = False
            if self.game_number == 1:
                joc2 = Joc2(self.port)
                self.player1.score += joc2.Loop(self.connection.q_listen, self.connection.q_send)
                pygame.mixer.music.load('sunete/main_theme.wav')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            if self.game_number == 2:
                joc1 = Joc1(self.port)
                self.player1.score += joc1.Loop(self.connection.q_listen, self.connection.q_send)
                pygame.mixer.music.load('sunete/main_theme.wav')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            if self.game_number == 3:
                joc3 = Joc3(self.port)
                self.player1.score += joc3.Loop(self.connection.q_listen, self.connection.q_send)
                pygame.mixer.music.load('sunete/main_theme.wav')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            if self.game_number == 4:
                joc4 = Joc4(self.port)
                self.player1.score += joc4.Loop(self.connection.q_listen, self.connection.q_send)
                pygame.mixer.music.load('sunete/main_theme.wav')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            if self.game_number == 5:
                joc5 = Joc5(self.port)
                self.player1.score += joc5.Loop(self.connection.q_listen, self.connection.q_send)
                pygame.mixer.music.load('sunete/main_theme.wav')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            if self.game_number == 6:
                self.running = False
            self.game_number += 1
            self.wait_time = 0
        if self.connection.q_listen:
            if self.wait_time == -1:
                self.wait_time = 0
            data = self.connection.q_listen[0]
            if data[0] != "minigame" and data[0] != "close" :
                if data[1] == -1:
                    self.player2.moving_left = False
                    self.player2.moving_right = False
                else:
                    self.player2.frame_number = data[1]
                    if data[0]:
                        self.player2.moving_left = True
                    else:
                        self.player2.moving_right = True
                self.player2.player_rect.x = data [2]
                if data[3] != self.receive_string:
                    self.text_swap()
                    self.text1.string = "Brown: "
                    self.text1.Update(data[3])
                    self.receive_string = data[3]
                self.player2.score = data[4]
                self.enemy_score.Update(self.player2.score)
            self.connection.q_listen.popleft()
            
        if self.chatting:
            if self.text_input.update(self.event_list):
                self.send_string = self.text_input.get_text()
                self.text_input.clear_text()
                self.chatting = False
                self.text_swap()
                self.text1.string = "White: "
                self.text1.Update(self.send_string)
        self.player1.Move(dt)
        if self.time > 0.03:
            if self.player1.moving_right == True:
                frame_number = int(self.player1.frame_number_right)
            else:
                if self.player1.moving_left:
                    frame_number = int(self.player1.frame_number_left)
                else:
                    frame_number = -1
            packet = (int(self.player1.moving_left), frame_number, self.player1.player_rect.x, self.send_string, self.player1.score)
            self.connection.q_send.append(packet)
            self.time = 0

    def Events(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    #print(pos)
                    if pos[0] >= 1515 and pos[0] <= 1585 and pos[1] >=785 and pos[1] <= 859:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.connection.q_end.append("end")
                        self.running = False
                    if pos[0] > 20 and pos[0] < 413 and pos[1] > 172 and pos[1] < 201:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.chatting = True
                        self.player1.moving_left = False
                        self.player1.moving_right = False
                    if self.chatting:
                        if pos[0] > 330 and pos[0] < 405 and pos[1] > 140 and pos[1] < 180:
                            pygame.mixer.Sound.play(self.click_sound)
                            self.send_string = self.text_input.get_text()
                            self.text_input.clear_text()
                            self.chatting = False
                            self.text_swap()
                            self.text1.string = "White: "
                            self.text1.Update(self.send_string)
            if not self.chatting:
                self.player1.Events(event)

    def Loop(self):
        while self.running:
            self.event_list = pygame.event.get()
            self.Events(self.event_list)
            self.Blit_Images()
            self.Update()
            pygame.display.update()
#----------------------------------------------------------------------------------

class Tutorial:
    def __init__(self):
        self.tutorial_image = pygame.image.load("imagini/tutorial0.png")
        self.rect = self.tutorial_image.get_rect()
        self.image_number = 0
        self.rect.left = 0
        self.rect.top = 0
        self.tutorial1_image = pygame.image.load("imagini/tutorial1.png")
        self.tutorial2_image = pygame.image.load("imagini/tutorial2.png")
        self.tutorial3_image = pygame.image.load("imagini/tutorial3.png")
        self.tutorial4_image = pygame.image.load("imagini/tutorial4.png")
        self.tutorial5_image = pygame.image.load("imagini/tutorial5.png")
        self.exit_button = pygame.image.load("imagini/exit_button.png")
        self.exit_button = pygame.transform.smoothscale(self.exit_button,(100,100))
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_rect.x = 1500
        self.exit_button_rect.y = 770
        self.running = True
        self.click_sound = pygame.mixer.Sound("sunete/button.wav")

    def Events(self):
        for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[0] >= 1515 and pos[0] <= 1585 and pos[1] >=785 and pos[1] <= 859:
                        self.running = False
                        pygame.mixer.Sound.play(self.click_sound)
                    if pos[0] > 965 and pos[0] < 1163 and pos[1] > 265 and pos[1] < 405:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.image_number = 1
                    if pos[0] > 1250 and pos[0] < 1450 and pos[1] > 265 and pos[1] < 405:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.image_number = 2
                    if pos[0] > 1113 and pos[0] < 1310 and pos[1] > 440 and pos[1] < 585:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.image_number = 3
                    if pos[0] > 970 and pos[0] < 1169 and pos[1] > 623 and pos[1] < 765:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.image_number = 4
                    if pos[0] > 1255 and pos[0] < 1455 and pos[1] > 623 and pos[1] < 765:
                        pygame.mixer.Sound.play(self.click_sound)
                        self.image_number = 5

    def Blit(self):
        if self.image_number == 0:
            g.screen.blit(self.tutorial_image, self.rect)
        if self.image_number == 1:
            g.screen.blit(self.tutorial1_image, self.rect)
        if self.image_number == 2:
            g.screen.blit(self.tutorial2_image, self.rect)
        if self.image_number == 3:
            g.screen.blit(self.tutorial3_image, self.rect)
        if self.image_number == 4:
            g.screen.blit(self.tutorial4_image, self.rect)
        if self.image_number == 5:
            g.screen.blit(self.tutorial5_image, self.rect)
        g.screen.blit(self.exit_button, self.exit_button_rect)
        pygame.display.update()
        
    def Loop(self):
        while self.running:
            self.Blit()
            self.Events()
            
#----------------------------------------------------------------------------------

class Menu:
    def __init__(self):
        g.variables_initialization()
        pygame.mixer.music.load('sunete/main_theme.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        g.screen = pygame.display.set_mode([1600, 900])
        self.menu_image = pygame.image.load("imagini/meniu.png")
        self.menu_image = pygame.transform.smoothscale(self.menu_image, (1600, 900))
        self.pos = [0,0]
        self.disconnected_image = pygame.image.load("imagini/disconnected.png")
        self.disconnected_image = pygame.transform.smoothscale(self.disconnected_image, (1600, 900))
        self.disconnected_image_rect = self.disconnected_image.get_rect()
        self.disconnected_image_rect.center = (800, 450)
        self.tutorial = Tutorial()
        self.click_sound = pygame.mixer.Sound("sunete/button.wav")
        self.loading_image = pygame.image.load("imagini/loading.png")

        self.won_image = pygame.image.load("imagini/win.png")
        self.lost_image = pygame.image.load("imagini/lost.png")


    def Draw(self):
        g.screen.blit(self.menu_image,(0,0))
    def Loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    if self.pos[0] > 100 and self.pos[0] < 410 and self.pos[1] > 495 and self.pos[1] < 530:
                        pygame.mixer.Sound.play(self.click_sound)
                        g.screen.blit(self.loading_image,self.disconnected_image_rect)
                        pygame.display.flip()
                        singleplayer_main_game = Single_Player_Main_Game()
                        singleplayer_main_game.Loop()
                    if self.pos[0] > 105 and self.pos[0] < 375 and self.pos[1] > 400 and self.pos[1] < 433:
                        pygame.mixer.Sound.play(self.click_sound)
                        g.screen.blit(self.loading_image,self.disconnected_image_rect)
                        pygame.display.flip()
                        multiplayer_main_game = Multiplayer_Main_Game()
                        multiplayer_main_game.Loop()
                        if multiplayer_main_game.connection.q_end:
                            g.screen.blit(self.disconnected_image, self.disconnected_image_rect)
                            pygame.display.update()
                            time.sleep(5)
                        else:
                            if multiplayer_main_game.player1.score >= multiplayer_main_game.player2.score:
                                g.screen.blit(self.won_image, self.disconnected_image_rect) 
                                pygame.display.update()
                            else:
                                g.screen.blit(self.lost_image, self.disconnected_image_rect) 
                                pygame.display.update()
                            time.sleep(5)
                    if self.pos[0] > 105 and self.pos[0] < 305 and self.pos[1] > 590 and self.pos[1] < 625:
                        pygame.mixer.Sound.play(self.click_sound)
                        g.screen.blit(self.loading_image,self.disconnected_image_rect)
                        pygame.display.flip()
                        self.tutorial.number = 0
                        self.tutorial.Loop()
                    if self.pos[0] >= 1385 and self.pos[0] <= 1475 and self.pos[1] >=800 and self.pos[1] <= 835:
                        pygame.quit()
                        sys.exit()
            self.Draw()
            pygame.display.update()

menu = Menu()
menu.Loop()

