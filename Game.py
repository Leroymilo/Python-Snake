# -*- coding: utf-8 -*-

import numpy as np
import random as rd
import pygame
from pygame.locals import *
import os
import sys

#Fonctions :

def newFruit():
    """
    Génère un nouveau fruit.
    """
    xf, yf = rd.randint(0, w-1), rd.randint(0, h-1)
    while (xf, yf) in snake :
        xf, yf = rd.randint(0, w-1), rd.randint(0, h-1)
    return(xf, yf)
    
def snakeAndFruitInGrille(grille, snake, xf, yf):
    """
    Nettoie la grille et réinsère le serpet et le fruit à leur place dans la grille.
    """
    grille = np.zeros((w, h), dtype = 'int')
    for part in snake :
        (j, i) = part
        grille[i][j] = 1
    grille[yf][xf] = 2
    return grille
    
def printin(grille):
    """
    Affiche le contenu du tableau principal sur l'écran.
    """
    Fenetre.fill((0, 0, 0))
    
    for i in range(h) :
        for j in range(w) :
            if grille[i][j] == 1 :
                Rect = pygame.Rect(j*delta, i*delta, delta-2, delta-2)
                pygame.draw.rect(Surface, (255, 255, 255), Rect)
                
            if grille[i][j] == 2 :
                pygame.draw.circle(Surface, (255, 0, 0), (j*delta + delta//2, i*delta + delta//2), delta//2)

    pygame.display.flip()
    return None

#Initialisation des variables :

Dir = 0
delta = 50
h, w = 13, 13
delay = 200
lose = False
restart = False

#Initialisation de pygame :

pygame.init()

Fenetre = pygame.display.set_mode((w*delta, h*delta))
Surface = pygame.display.get_surface()

continuer = True

pygame.key.set_repeat(50, 50)

#Préparation des textes :

all_fonts = pygame.font.get_fonts()
if "comicsansms" in all_fonts :
    font = pygame.font.SysFont("comicsansms", 24)
else :
    font = pygame.font.Font(None, 40)

losetext = font.render("You lost, press Spacebar to try again.", True, (127, 127, 127))
pausetext = font.render("Pause, press escape to return to the game.", True, (127, 127, 127))
wintext1 = font.render("You won !", True, (0, 0, 0))
wintext2 = font.render("Press Spacebar to play again.", True, (0, 0, 0))

#Initialisation du jeu :

grille = np.zeros((w, h), dtype = 'int')
x, y = 6, 6
snake = [(x, y)]
xf, yf = newFruit()
grille = snakeAndFruitInGrille(grille, snake, xf, yf)
printin(grille)

#Création de la boucle créant un délai de 0.8s et guettant les évènements :

while continuer:
    time = pygame.time.get_ticks()
    prevDir = Dir
    while pygame.time.get_ticks()-time < delay :
        event = pygame.event.get()
        
        if len(event) != 0 :
            event = event[0]

            if event.type == QUIT :
                continuer = False

            if event.type == KEYDOWN :
                move = False

#Changement de directions :
                
                if event.key == K_RIGHT and prevDir != 2:
                    Dir = 0
                    
                if event.key == K_DOWN and prevDir != 3:
                    Dir = 1
                    
                if event.key == K_LEFT and prevDir != 0:
                    Dir = 2
                    
                if event.key == K_UP and prevDir != 1:
                    Dir = 3

#Pause :
                    
                if event.key == K_ESCAPE :
                    Fenetre.blit(pausetext, ((w*delta-pausetext.get_width())//2, (h*delta-pausetext.get_height())//2))
                    pygame.display.flip()
                    pause = True
                    pygame.key.set_repeat(500, 100)
                    while continuer and pause :
                        event = pygame.event.get()
                        
                        if len(event) != 0 :
                            event = event[0]

                            if event.type == KEYDOWN :
                                if event.key == K_d :
                                    delay = int(input("Cheater! New delay in ms : "))

                            if event.type == QUIT :
                                continuer = False

                            if event.type == KEYDOWN :
                                if event.key == K_ESCAPE :
                                    pause = False
                    pygame.key.set_repeat(50, 50)
                    printin(grille)

#Changement du délai en jeu :

                if event.key == K_d :
                    delay = int(input("Cheater! New delay in ms : "))

                    #Pause automatique :

                    Fenetre.blit(pausetext, ((w*delta-pausetext.get_width())//2, (h*delta-pausetext.get_height())//2))
                    pygame.display.flip()
                    pause = True
                    pygame.key.set_repeat(500, 100)
                    while continuer and pause :
                        event = pygame.event.get()
                        
                        if len(event) != 0 :
                            event = event[0]

                            if event.type == QUIT :
                                continuer = False

                            if event.type == KEYDOWN :
                                if event.key == K_ESCAPE :
                                    pause = False
                    pygame.key.set_repeat(50, 50)
                    printin(grille)

#Application du changement de direction :
                                    
    prevx, prevy = x, y
    if Dir == 0 :
        x += 1
    if Dir == 1 :
        y += 1
    if Dir == 2 :
        x -= 1
    if Dir == 3 :
        y -= 1

#Vérification des collisions :
        
    if not (0 <= x <= w-1 and 0 <= y <= h-1):
        lose = True
        x, y = prevx, prevy

    elif grille[y][x] == 1 :
        lose = True
        x, y = prevx, prevy
        
    if not lose :

        snake.append((x, y))

        #Vérification de victoire :

        if len(snake) == w*h :
            Fenetre.blit(wintext1, ((delta*w-wintext1.get_width())//2, (delta*h)//2-wintext1.get_height))
            Fenetre.blit(wintext2, ((delta*w-wintext2.get_width())//2, (delta*h)//2))
            pygame.display.flip()
            while not restart :
                for event in pygame.event.get() :
                    if event.type == KEYDOWN :
                        if event.key == K_SPACE :
                            restart = True
                        if event.key == K_d :
                            delay = int(input("New delay in ms : "))
                    if event.type == QUIT :
                        pygame.quit()
                        sys.exit()

        else :
            #Vérification de collision avec le fruit :

            if (x, y) == (xf, yf) :
                xf, yf = newFruit()
            else :
                snake.pop(0)

            #Actualisation et affichage de la grille :

            grille = snakeAndFruitInGrille(grille, snake, xf, yf)
            printin(grille)
            
    else :

        #Affichage de la défaite et boucle de restart.
        
        Fenetre.blit(losetext, ((delta*w-losetext.get_width())//2, (delta*h-losetext.get_height())//2))
        pygame.display.flip()
        while not restart :
            for event in pygame.event.get() :
                if event.type == KEYDOWN :
                    if event.key == K_SPACE :
                        restart = True
                    if event.key == K_d :
                        delay = int(input("Cheater! New delay in ms : "))
                if event.type == QUIT :
                    pygame.quit()
                    sys.exit()

    #Réinitialisation du jeu :

    if restart :
        grille = np.zeros((w, h), dtype = 'int')
        x, y = 6, 6
        snake = [(x, y)]
        xf, yf = newFruit()
        grille = snakeAndFruitInGrille(grille, snake, xf, yf)
        printin(grille)
        lose = False
        restart = False
        
pygame.quit()
sys.exit()
