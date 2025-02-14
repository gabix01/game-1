import pygame as pg
import sys
from os import path
from math import sqrt
from consts import *
from funcs import *
from Button import *

class Game:
    def __init__(self, size):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.size = size
        self.setTileSize()
        self.state = [[0 for _ in range(self.size)] for __ in range(self.size)]
        self.origin = Point(W/2 - (H/2-50)/sqrt(3), 50)
        self.move = 1
        self.started = False
        self.sound_state = True

    def loadData(self):
        # ladowanie wszystkich danych
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        doc_folder = path.join(game_folder, 'docs')
                # zdjecia
        #self.tile_img = pg.image.load(path.join(img_folder, TILE_IMG)).convert_alpha()
        #self.tile_img = pg.transform.scale(self.tile_img, (2*self.tile_size+1, int(self.tile_size*sqrt(3))+1))

        self.bg_img = pg.image.load(path.join(img_folder, BG_IMG)).convert_alpha()
        self.pause_img = pg.image.load(path.join(img_folder, PAUSE_IMG)).convert_alpha()
        self.back_img = pg.image.load(path.join(img_folder, BACK_IMG)).convert_alpha()
        self.up_img = pg.image.load(path.join(img_folder, UP_IMG)).convert_alpha()
        self.down_img = pg.image.load(path.join(img_folder, DOWN_IMG)).convert_alpha()

                #muzyka
        self.bg_music = pg.mixer.Sound(path.join(doc_folder, BACKGROUND_MUSIC))
        self.bg_music_channel = pg.mixer.Channel(1)
        self.bg_music_channel.play(self.bg_music, loops=-1)
        self.bg_music_channel.set_volume(0.5)
        self.click_sound = pg.mixer.Sound(path.join(doc_folder, CLICK_SOUND))
        self.click_sound_channel = pg.mixer.Channel(2)

                #tekst
        with open(path.join(doc_folder, RULES), 'r') as f:
            self.rules_text = ''.join(f.readlines())

    def setTileSize(self):
        self.tile_size = 4*(H/2-50)/3/sqrt(3)/(self.size-1)

    def coords(self, r, c):
                # zmiana kordów z grid na realne
        x = self.origin .x + c*3/2*self.tile_size
        y = self.origin.y + (c+2*r)*self.tile_size*sqrt(3)/2
        return int(x), int(y)
                # po kliknięciu zmiana statusu gry
    def tick(self, pos):

        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                if inHex(pos, x, y, self.tile_size) and self.state[r][c] != 2\
                                                    and self.state[r][c] != 1:
                    if self.sound_state:
                        self.click_sound_channel.play(self.click_sound)
                    self.state[r][c] = self.move
                    self.move = 3-self.move

    def highlight(self, pos):
            # highlight hexagonu ktory jest pod myszka
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                if self.state[r][c] == 0 and inHex(pos, x, y, self.tile_size):
                    self.state[r][c] = self.move + 2
                elif self.state[r][c] > 2 and not inHex(pos, x, y, self.tile_size):
                    self.state[r][c] = 0

    def showGrid(self):

        # draw mape
        A = (self.origin.x-self.tile_size, self.origin.y-self.tile_size*sqrt(3))
        B = (self.origin.x-self.tile_size/2*(1-3*self.size),\
             self.origin.y+self.tile_size*sqrt(3)/2*(self.size-2)+self.tile_size*sqrt(3)/6)
        C = (self.origin.x-self.tile_size/2*(1-3*self.size), self.origin.y+self.tile_size*sqrt(3)/2*(2*self.size+self.size-1))
        D = (self.origin.x-self.tile_size, self.origin.y+self.tile_size*sqrt(3)*(self.size-1/2)-self.tile_size*sqrt(3)/6)
        M = ((A[0]+B[0])/2, (B[1]+C[1])/2)
        pg.draw.polygon(self.screen, GREEN, [A, B, M])
        pg.draw.polygon(self.screen, GREEN, [C, D, M])
        pg.draw.polygon(self.screen, BLUE, [B, C, M])
        pg.draw.polygon(self.screen, BLUE, [D, A, M])
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                # rysowanie tytulu
                #self.screen.blit(self.tile_img, (x-self.tile_size, y-self.tile_size))
                # draw graczy
                if self.state[r][c] == 1:
                    drawHex(self.screen, GREEN, LIGHTYELLOW, (x, y), self.tile_size)
                elif self.state[r][c] == 2:
                    drawHex(self.screen, BLUE, LIGHTYELLOW, (x, y), self.tile_size)
                elif self.state[r][c] == 3:
                    drawHex(self.screen, LIGHTGREEN, LIGHTYELLOW, (x, y), self.tile_size)
                elif self.state[r][c] == 4:
                    drawHex(self.screen, LIGHTBLUE, LIGHTYELLOW, (x, y), self.tile_size)
                else:
                    drawHex(self.screen, DARKRED, LIGHTYELLOW, (x, y), self.tile_size)

    def checkWin(self):
        # sprawdzanie wygranego
        for y in range(self.size):
            if self.state[y][0] == 2:
                if DFS(Point(y, 0), self.state, lambda v: (v.Y == self.size-1), 2):
                    return 2

        for x in range(self.size):
            if self.state[0][x] == 1:
                if DFS(Point(0, x), self.state, lambda v: (v.X == self.size-1), 1):
                    return 1
        return 0

    def shadow(self):
        shadow = pg.Surface((W, H))
        shadow.set_alpha(200)
        self.screen.blit(shadow, (0, 0))

    def startScreen(self):
        # pokazadnie ekranu startowego, zwraca prawde jesli gra sie zaczela
        start = True
        # guziki
        play = Button((W/2, 2*H/3), 80, 'Play')
        settings = Button((150, H-75), 50, 'Settings')
        rules = Button((W-100, H-75), 50, 'Rules')
        buttons = [play, settings, rules]
        while start:
            # fps
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # jezeli exit jest nacisniety
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # jezeli jest klikniety przycisk sprawdza
                    if play.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.__init__(self.size)
                        self.started = True
                        return True
                    if rules.triggered(channel=self.click_sound_channel,
                                       sound=self.click_sound,
                                       playing=self.sound_state):
                        start = self.rulesScreen()
                    if settings.triggered(channel=self.click_sound_channel,
                                          sound=self.click_sound,
                                          playing=self.sound_state):
                        start = self.settingsScreen()
            # highlight przycisk
            for button in buttons:
                button.highlighted()
            # rzeczy
            self.screen.blit(self.bg_img, (0, 0))
            textOut(self.screen, 'HEX', 200, ORANGE, (W/2, H/3))
            # pokazanie przyciskow
            for button in buttons:
                button.show(self.screen)
            # podwojnie przetwarzanie
            pg.display.flip()

    def rulesScreen(self):

        start = True
        # przyciski
        back = Button((30, 30), 50, img=self.back_img)
        buttons = [back]
        while start:
            # fps
            self.clock.tick(FPS)
            # zdarzenia
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # jezeli exit jest klikniety
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # jezeli sprawdzenia guzik
                    if back.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        return True
            # highlight przycisk
            for button in buttons:
                button.highlighted()
            # rzeczy
            self.screen.blit(self.bg_img, (0, 0))
            textOut(self.screen, 'Rules', 100, ORANGE, (W/2, H/3))
            textOutMultiline(self.screen, self.rules_text, 30, BLACK, (W/2, H/3))
            # pokazanie
            for button in buttons:
                button.show(self.screen)

            pg.display.flip()

    def settingsScreen(self):

        start = True
        #guuuzkiki
        back = Button((30, 30), 50, img=self.back_img)
        up = Button((2*W/3+60, H/2-25), 50, img=self.up_img)
        down = Button((2*W/3+60, H/2+25), 50, img=self.down_img)
        music_state = 'On' if self.bg_music_channel.get_busy() else 'Off'
        sound_state = 'On' if self.sound_state else 'Off'
        music_switch = Button((2*W/3-50, H/2+60), 50, music_state, col=DARKRED)
        sound_switch = Button((2*W/3-50, H/2+120), 50, sound_state, col=DARKRED)
        buttons = [back, up, down, music_switch, sound_switch]
        while start:
            # fps
            self.clock.tick(FPS)
            # zdarzenia
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # wyjscie
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # inne
                    if back.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        return True
                    if up.triggered(channel=self.click_sound_channel,
                                    sound=self.click_sound,
                                    playing=self.sound_state):
                        self.size = min(MAX_BOARD_SIZE, self.size+1)
                    if down.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.size = max(MIN_BOARD_SIZE, self.size-1)
                    if music_switch.triggered(channel=self.click_sound_channel,
                                              sound=self.click_sound,
                                              playing=self.sound_state):
                        if music_switch.text == 'On':
                            self.bg_music_channel.stop()
                            music_switch.text = 'Off'
                        else:
                            self.bg_music_channel.play(self.bg_music, loops=-1)
                            music_switch.text = 'On'
                    if sound_switch.triggered(channel=self.click_sound_channel,
                                              sound=self.click_sound,
                                              playing=self.sound_state):
                        if sound_switch.text == 'On':
                            self.sound_state = False
                            sound_switch.text = 'Off'
                        else:
                            self.sound_state = True
                            sound_switch.text = 'On'
            # przyciski
            for button in buttons:
                button.highlighted()
            # rzeczy
            self.screen.blit(self.bg_img, (0, 0))
            textOut(self.screen, 'Settings', 100, ORANGE, (W/2, H/4))
            textOut(self.screen, 'Board size:', 50, BLACK, (W/3, H/2))
            textOut(self.screen, self.size, 50, BLACK, (2*W/3, H/2))
            textOut(self.screen, 'Music:', 50, BLACK, (W/3, H/2+60))
            textOut(self.screen, 'Sound:', 50, BLACK, (W/3, H/2+120))

            # guziki pokazanie
            for button in buttons:
                button.show(self.screen)

            pg.display.flip()

    def pauseScreen(self):

        start = True
        # guziki
        resume = Button((W/2, H/3), 80, 'Resume', col=ORANGE)
        home = Button((W/2, H/2), 50, 'Home', col=WHITE)
        buttons = [home, resume]
        while start:
            # fps
            self.clock.tick(FPS)
            # -rzeczy
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # guzik wyjscia
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # guzkiki
                    if home.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.started = False
                        return True
                    if resume.triggered(channel=self.click_sound_channel,
                                        sound=self.click_sound,
                                        playing=self.sound_state):
                        return True
            # highlight guzik
            for button in buttons:
                button.highlighted()
            # rzeczy
            # guziki
            self.screen.blit(self.bg_img, (0, 0))
            self.showGrid()
            self.shadow()
            for button in buttons:
                button.show(self.screen)

            pg.display.flip()

    def GOScreen(self, winner):

        go = True
        home = Button((W/2, 2*H/3), 50, 'Home', col=WHITE)
        while go:

            self.clock.tick(FPS)
            # rzeczy
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # wyjscie
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # xd
                    if home.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.started = False
                        return True
            home.highlighted()
            # rzeczy
            self.screen.blit(self.bg_img, (0, 0))
            self.showGrid()
            self.shadow()
            textOut(self.screen, 'GAME OVER', 80, ORANGE, (W/2, H/3))
            if winner == 2:
                textOut(self.screen, 'Blue won', 60, BLUE, (W/2, H/2))
            else:
                textOut(self.screen, 'Green won', 60, GREEN, (W/2, H/2))
            home.show(self.screen)

            pg.display.flip()
