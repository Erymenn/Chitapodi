#!/usr/bin/python3
# -*- coding: Utf-8 -*
 
"""
Jeu Demineur stade 1

Script Python
Fichiers : tapodi.py, grilles.py, constantes.py, joueur.py, personnages.py
Dossiers : images, sons, saves
"""

import pygame
import pyganim
import copy
import csv
import os
import pickle
import datetime
from pygame.locals import *
from heapq import heappop
from constantes import *
from envirs_jeu import Jeu_libre
from biblio import Biblio
from joueur import Joueur
from envirs import *


#INITIALISATION DES MODULES
pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()

#CREATION OU LECTURE DU JOUEUR
with open(os.path.join("data", 'saves', 'last.txt'),'r') as fich: lastsave = fich.readline()
joueur = Joueur(lastsave)

#CREATION DE LA FENETRE
if joueur.options.fullscreen: fenetre = pygame.display.set_mode(joueur.options.taillefenetre, pygame.FULLSCREEN)
else: fenetre = pygame.display.set_mode(joueur.options.taillefenetre)
pygame.display.set_caption(TITRE)
#icone = pygame.image.load(ICONE).convert_alpha()
#pygame.display.set_icon(icone)

#CHARGEMENT DES DONNEES !!!charger l'essentiel des donnees apres l'ecran titre
biblio = Biblio()
biblio.update_options(joueur.options)
if joueur.options.curseur: pygame.mouse.set_visible(False)

#CHARGEMENT DES ENVIRONNEMENTS
envirs = {'ecran_titre':Ecran_titre(), 'principal':Menu_principal(), 'pause':Menu_pause(), 'credits':Menu_credits(), "aide":Menu_aide(), 'options':Menu_options(), "jeu_libre":Jeu_libre()}

#CHARGEMENT DES IMAGES DES MENUS
biblio.charger_images_noalpha("menus", "aide", "credits", "ecran_titre", "options", "pause", "principal")
biblio.charger_images("menus", "bouton10x30", "bouton20x20", "verrou")



#grille = GrilleDemineur(11, 6, [(0,0)], 20)
#perso = Personnage('Khan', (0,0))
#perso.pos = poscase_to_posperso((0, 0))
#afficher_grille(grille)



#INITIALISATION DE LA BOUCLE DE JEU
finboucle = False

#BOUCLE DE JEU
while not finboucle:

	#MISE A JOUR DE LA POSITION DU CURSEUR (gestion de la vitesse de souris!)
	joueur.poscurseur = pygame.mouse.get_pos()

	#MISE A JOUR DE L'ENVIRONNEMENT
	envirs[joueur.envir].update(joueur, biblio)

	#AFFICHAGE DE L'ECRAN ET DU CURSEUR (ici sinon prob de changement d'envir)
	if joueur.etat != 'initialiser': envirs[joueur.envir].afficher(fenetre, joueur, biblio)
	if joueur.options.curseur: fenetre.blit(biblio.curseur, joueur.poscurseur)

	#PRISE EN COMPTE DES EVENEMENTS:
	events = pygame.event.get()
	
	for event in events:
		#CLIC
		if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP: envirs[joueur.envir].clic(event, joueur, biblio)

		#CLAVIER
		if event.type == KEYDOWN: 
			envirs[joueur.envir].touche(event, joueur, biblio)
			#GESTION DE LA PAUSE
			if event.key==K_ESCAPE or event.key==K_PAUSE: 
				if joueur.envir == 'pause': joueur.envir, joueur.etat = joueur.lastenvir, 'reprendre'
				else: joueur.envir, joueur.etat = 'pause', 'initialiser'
			#GESTION DE L'IMPRIMECRAN
			if event.key==K_PRINT: 
				biblio.sons['gagne'].play()
				pygame.image.save(fenetre, os.path.join("", "data", "screenshots", "chitapodi_"+str(datetime.datetime.now())[:-7]+".jpg"))
			


		#FERMETURE
		if event.type == QUIT or joueur.etat == 'quitter':
			joueur.sauvegarder()
			finboucle = True

	#LIMITATION DE LA VITESSE DE LA BOUCLE
	clock.tick(TIC)

	#RAFRAICHISSEMENT DE LA FENETRE
	pygame.display.flip()

	
	
