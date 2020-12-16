import pygame as pg
import random
from pprint import pprint
from funcs import *
from Game import *
from consts import *

game = Game(SIZE)
game.loadData()

# ladowanie przyciskow
pause = Button((30, 30), 50, img=game.pause_img)
buttons = [pause]

# rysowanie
run = True
while run:
    #przyklejenie do fps
    game.clock.tick(FPS)
    if not game.started:
        run = game.startScreen()
    else:
        # EVENTS
        game.highlight(pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
    # jezeli przycisk exit jest nacisniety
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
    # ruchy graczy
                game.tick(pg.mouse.get_pos())
                if pause.triggered(channel=game.click_sound_channel,
                                   sound=game.click_sound,
                                   playing=game.sound_state):
                    run = game.pauseScreen()

    # highlighted przycisków
        for button in buttons:
            button.highlighted()

            #rzeczy
        game.screen.blit(game.bg_img, (0, 0))
        game.showGrid()
        for button in buttons:
            button.show(game.screen)
        if game.checkWin():
            run = game.GOScreen(game.checkWin())
    # podwojne przetwarzanie
    pg.display.flip()

pg.quit()
