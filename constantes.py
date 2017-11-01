#!/usr/bin/python3
# -*- coding: Utf-8 -*

LORIGINE = 90
HORIGINE = 182

TIC = 60

#DONNEES FENETRE
LFENETRE = 1024
HFENETRE = 600
DIMFENETRE = (LFENETRE, HFENETRE)
ICONE = ""
TITRE = "Les cavernes de Chitapodi"

#DONNEES CASES
LCASE = 80
HCASE = 60
HPERSO = 180

#DONNES DEPLACEMENTS
TPS, PLUSX, PLUSY = xrange(3)

#LANGUES
ENG, FR = xrange(2)

#ETAT JOUEUR
QUITTER, INITIALISER, REPRENDRE, AGIR, DEPLACER, DEPLACER_CAMERA, CHARGER, ESTOMPER, REVISER_JEU, REVISER_VOLUME, PHOTOGRAPHIER, CHANGER_FULLSCREEN = xrange(12)

#ETATPERSO
IDLE, N, NE, E, SE, S, SW, W, NW = xrange(9)


#DONNEES PERSONNAGES
DIRECTIONS = {x: i for i,x in enumerate(((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)), 1)}
VECTEURS = [None, (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]#IDLE, N, NE, E, SE, S, SW, W, NW
#DIRECTIONSRUN = {(0, -1):'Nrun', (1, -1):'NErun', (1, 0):'Erun', (1, 1):'SErun', (0, 1):'Srun', (-1, 1):'SWrun', (-1, 0):'Wrun', (-1, -1):'NWrun'}
#FRAMESPARPAS = 3
#DUREEPAS = TIC
#DUREEPASRUN = int(2.*TIC/3)

#COULEURS
BLEURENARD = (1,22,65)
BLEUCLAIR = (3,179,232)
NOIR = (0,0,0)
BRONZE = (193,143,22)
BRONZESOMBRE = (45,34,8)
BLANC = (255,255,255)
GRISPOP = (100,100,100)
VERT = (0,255,0)

ALPHAPOP = 0.6

#STYLES DE TEXTE
BULLE = {'name':'Arial', 'size':14, 'antialias':True, 'color':NOIR, 'bg': BLANC}


