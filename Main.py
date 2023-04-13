import pyxel 
import random
import time

class Jeu():
    def __init__(self):
        pyxel.init(256, 256, title="RPG", quit_key=pyxel.KEY_M, fps=30)
        pyxel.load("custom.pyxres")
        self.x = 16
        self.y = 16
        self.x_bastien = 64
        self.y_bastien = 256
        self.close_to_bastien = 0
        self.speed = 4
        self.map_x = 0
        self.map_y = 0
        self.move_up = 1
        self.move_down = 1
        self.move_left = 1
        self.move_right = 1
        self.talk_to = ""
        self.text = []
        self.dash = False
        self.bastienT = False
        self.l_zombie = []
        self.dash_cooldown = 15
        self.spawn_zombie = 120
        #Liste des dialogue
        self.speech_bastien1 = "Salutations jeune aventurier !"


        #Status du jeu:
        self.game_status = 0
        #0 = Menu de start
        #1 = En jeu
        #2 = En pause
        #3 = A propos
        #4 = Dans un dialogue


        self.inventory = []
        self.selected_option = 0
        
        pyxel.run(self.update, self.draw)
    def mouvements(self):
        if pyxel.btn(pyxel.KEY_Z):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                for i in range(25):
                    if self.y > 16:
                        self.y += -self.speed
            else:
                if self.y > 16 and self.move_up == 1:
                    self.y += -self.speed
            # if self.map_y < 0:
            #     self.map_y += self.speed
        if pyxel.btn(pyxel.KEY_Q):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                for i in range(25):
                    if self.x > 16:
                        self.x += -self.speed
            else:
                if self.x > 16 and self.move_left == 1:
                    self.x += -self.speed
                # if self.map_x < 0:
            #     self.map_x += self.speed
        if pyxel.btn(pyxel.KEY_S):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                for i in range(25):
                    if self.y < 2000:
                        self.y += self.speed
            else:
                if self.y < 2000 and self.move_down == 1:
                    self.y += self.speed
            # self.map_y += -self.speed
        if pyxel.btn(pyxel.KEY_D):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                    for i in range(25):
                        if self.x < 2018:
                            self.x += self.speed
            else:
                if self.x < 2018 and self.move_right == 1:
                    self.x += self.speed
            # if self.map_x < -(4096+512):
            #     self.map_x += -self.speed
    def dash(self):
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            for i in range(10):
                if self.y > 16:
                    self.y += -self.speed
        if pyxel.btn(pyxel.KEY_Q) and pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            for i in range(10):
                if self.x > 16:
                    self.x += -self.speed
        if pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            for i in range(10):
                if self.y < 2000:
                    self.y += self.speed
        if pyxel.btn(pyxel.KEY_D) and pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            for i in range(10):
                if self.x < 2018:
                    self.x += self.speed

    def camera(self):
        pyxel.camera(self.x+6-128, self.y+8-128)
        
    def starting_menu(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_option -= 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_option += 1
        elif pyxel.btnp(pyxel.KEY_RETURN):
            if self.selected_option%3 == 2:
                pyxel.quit()
            elif self.selected_option%3 == 1:
                self.game_status = 3
            elif self.selected_option%3 == 0:
                self.game_status = 1
    def pause(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            if self.game_status == 1:
                pyxel.camera(0, 0)
                self.game_status = 2
            elif self.game_status == 2:
                self.game_status = 1
                
    def spawn_zombie(self):
        if self.bastienT:
            if pyxel.frame_count%self.spawn_zombie==0:
                co = random.randint(1, 4)
                if co == 1:
                    self.l_zombie.append(self.x+60, self.y)
                elif co == 2:
                    self.l_zombie.append(self.x-60, self.y)
                elif co ==3:
                    self.l_zombie.append(self.x, self.y+60)
                elif co ==4:
                    self.l_zombie.append(self.x, self.y-60)
    def pause_menu(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_option -= 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_option += 1
        elif pyxel.btnp(pyxel.KEY_RETURN):
            if self.selected_option%2 == 1:
                pyxel.quit()
            elif self.selected_option%2 == 0:
                self.game_status = 1
    def dash_cooldown(self):
        if self.dash == False:
            if self.dash_cooldown ==0:
                self.dash = True
            else:
                self.dash_cooldown -=1
    def credit(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.game_status = 0
    def talking(self):
        if pyxel.btn(pyxel.KEY_T):
            if self.close_to_bastien == 1:
                self.game_status = 4
                self.talk_to = "bastien"
                self.text = self.speech_bastien1
                self.bastienT = True
                # for i in range(len(self.speech_bastien)):
                #     self.text = self.speech_bastien[0:i]
    def continue_speech(self):
        if self.talk_to == "bastien":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.game_status = 1
    def interaction(self):
        #MODELE DE COLLISION DES PERSO DE 12 sur 24     #####################################################################
        self.close_to_bastien = 0
        if self.y > self.y_bastien-28 and self.y < self.y_bastien+24 and self.x < self.x_bastien+12 and self.x > self.x_bastien-12:
            self.move_down = 0
            self.close_to_bastien = 1
        else:
            self.move_down = 1
        if self.y < self.y_bastien+28 and self.y > self.y_bastien-24 and self.x < self.x_bastien+12 and self.x > self.x_bastien-12:
            self.move_up = 0
            self.close_to_bastien = 1
        else:
            self.move_up = 1
        if self.x < self.x_bastien+16 and self.x > self.x_bastien-12 and self.y < self.y_bastien+24 and self.y > self.y_bastien-24:
            self.move_left = 0
            self.close_to_bastien = 1
        else:
            self.move_left = 1
        if self.x > self.x_bastien-16 and self.x < self.x_bastien+12 and self.y < self.y_bastien+24 and self.y > self.y_bastien-24:
            self.move_right = 0
            self.close_to_bastien = 1
        else:
            self.move_right = 1
        ####################################################################################################################
    def update(self):
        if self.game_status == 0:
            self.starting_menu()
        elif self.game_status == 1:
            self.interaction()
            self.mouvements()
            self.camera()
            self.pause()
            self.talking()
            self.spawn_zombie()
            #self.dash()
            #self.dash_cooldown()
        elif self.game_status == 2:
            self.pause_menu()
            self.pause()
        elif self.game_status == 3:
            self.credit()
        elif self.game_status == 4:
            self.continue_speech()
    def draw(self):
        if self.game_status == 0:
            pyxel.cls(4)
            if self.selected_option%3 == 0:
                pyxel.text(100, 100, "> Commencer", pyxel.frame_count%15)
                pyxel.text(100, 120, "A propos", 0)
                pyxel.text(100, 140, "Quitter", 0)
            elif self.selected_option%3 == 1:
                pyxel.text(100, 100, "Commencer", 0)
                pyxel.text(100, 120, "> A propos", 7)
                pyxel.text(100, 140, "Quitter", 0)
            elif self.selected_option%3 == 2:
                pyxel.text(100, 100, "Commencer", 0)
                pyxel.text(100, 120, "A propos", 0)
                pyxel.text(100, 140, "> Quitter", 8)
        elif self.game_status == 1:
            #Spawn de toute les entités
            pyxel.cls(3)
            pyxel.bltm(self.map_x, self.map_y, 0, 0, 0, 4096, 4096)
            pyxel.blt(self.x_bastien, self.y_bastien, 0, 34, 16, 12, 24, 3)
            
            #Spawn du joueur
            pyxel.blt(self.x, self.y, 0, 18, 16, 12, 24, 3)
            
            pyxel.blt(33*10, 33*10, 0, 48, 0, 16, 32,0)
            pyxel.blt(33*9, 33*10, 0, 48, 0, 16, 32,0)
            #Texte
            if self.close_to_bastien == 1:
                pyxel.text(self.x_bastien-20, self.y_bastien-7, "Press 'T' to talk", 9)
            for z in self.l_zombie:
                pyxel.blt(z[0], z[1], 0, 18, 16, 12, 24, 3)
            #Message ou autre qui arrive sous certaine condition
        elif self.game_status == 2:
            pyxel.cls(4)
            if self.selected_option%2 == 0:
                pyxel.text(100, 100, "> Continuez", 7)
                pyxel.text(100, 120, "Quitter", 0)
            elif self.selected_option%2 == 1:
                pyxel.text(100, 100, "Continuez", 0)
                pyxel.text(100, 120, "> Quitter", 8)
        elif self.game_status == 3:
            pyxel.cls(4)
            pyxel.text(100, 40, "A propos", 0)
            pyxel.text(40, 80, "****** est un RPG sans but defini pour l instant", 0)
            pyxel.text(120, 100, "Credit:", 1)
            pyxel.text(30, 110, "- Devloppement:", 1)
            pyxel.text(50, 120, "Rutabaga", 1)
            pyxel.text(50, 130, "YOTTA", 1)
            pyxel.text(50, 140, "Thib", 1)
        elif self.game_status == 4:
            pyxel.blt(self.x-110, self.y+50, 0, 0, 48, 231, 79, 0)
            pyxel.text(self.x-100, self.y+60, self.text, 0)


Jeu()
