#!/usr/bin/python3
# -*- coding: Utf-8 -*

import re
import pygame
import copy
import csv
from constantes import *
from fonctions_grilles import autour, autour_accessible
from heapq import heappush, heappop

def itersplit(string):
	"""version iterateur de split
	repris de ninjagecko sur stack overflow
	"""
	return (x.group(0) for x in re.finditer(r"[A-Za-z']+", string))
    
def afficher_tmptexte(f):
	def wrapper(self,fenetre, joueur, biblio):
		f(self,fenetre, joueur, biblio)
		fenetre.blit(biblio.tmptxt,(0,0))
	return wrapper

def afficher_bronze(f):
	def wrapper(self,fenetre, joueur, biblio):
		fenetre.blit(biblio.tmpimage, (0,0))
		fenetre.blit(biblio.bronze, (0,0))
		f(self,fenetre, joueur, biblio)
	return wrapper
	
def photographier(f):
	def wrapper(self,fenetre, joueur, biblio):
		if joueur.etat == PHOTOGRAPHIER: 
			biblio.tmpimage = copy.copy(fenetre)
			joueur.etat = None
		f(self,fenetre, joueur, biblio)
	return wrapper

def planche_to_liste(fichier, col, lig):
	"""convertit une planche en liste de surfaces"""
	planche = pygame.image.load(fichier).convert()
	#planche.set_colorkey(VERT)
	r = planche.get_rect()
	w, h = r.w//col, r.h//lig
	res = []
	rect = pygame.Rect(0, 0, w, h)
	for j in xrange(lig):
		for i in xrange(col):
			rect.topleft = (i*w, j*h)
			res.append(pygame.Surface(rect.size))
			#res[-1].fill(VERT)
			res[-1].set_colorkey(VERT)
			res[-1].blit(planche, (0, 0), rect)
	return res
	
	
def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
	"""lit un document .csv encode en uft-8 ligne par ligne vers de l'unicode
	les caracteres \\n sont remplaces par des retours a la ligne
	base sur l'algo d'Alex Martelli
	
	"""
	csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
	for row in csv_reader:
		yield [unicode(cell, 'utf-8') for cell in row]


	

