#!/usr/bin/python3
# -*- coding: Utf-8 -*

import pygame
import pyganim
import csv
import os
from fonctions_grilles import ligne_naif, plus_court_chemin
from constantes import *
from fonctions import itersplit, planche_to_liste, unicode_csv_reader


class Biblio():
	"""Classe rassemblant toutes les images, sons et textes
	Chargee au fur et a mesure
	"""

	def __init__(self, custom = None):
		#CHARGEMENT DES LANGUES
		self.langues = [ENG,FR]
		#CHARGEMENT DU CURSEUR
		self.curseur = pygame.image.load(os.path.join("data", "images", "curseur.png")).convert_alpha()
		#DEFINITION D'UNE IMAGE DE FOND TEMPORAIRE (PAUSE)
		self.tmpimage = None
		self.tmptxt = None#pygame.Surface(joueur.options.taillefenetre)
		self.noir = None
		self.bronze = None
		#CREATION D'ATTRIBUTS VIDES
		for att in itersplit("skins succes txtsucces menus txtmenus decors collectables"): 
			setattr(self, att, {})#peut-etre a transformer en liste avec une liste des cles en supplement (surtout decor et skins)
		#CREATION DES DEPLACEMENTS POUR LES ANIMS (dans l'ordre TPS, PLUSX, PLUSY pour N, NE, E...)
		self.deplacements = [None,
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]],
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]],
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]],
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]],
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]],
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]],
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]],
			[[200,200,200,200,200], [12, 16, 22, 18, 12], [8, 12, 16, 14, 10]]
			]
		#CHARGEMENT DES MUSIQUES ET SONS
		self.ambiances = {
			'horror':pygame.mixer.Sound(os.path.join("data", 'sons', 'Horror_Ambiance-Mike_Koenig-1992154342.wav')),
			'scary':pygame.mixer.Sound(os.path.join("data", 'sons', 'Scary_Ambiance-SoundBible.com-1778419064.wav')),
			'instinct':pygame.mixer.Sound(os.path.join("data", 'sons', 'bensound-instinct.wav')),
			"cave1":pygame.mixer.Sound(os.path.join("data", 'sons', '177958__sclolex__water-dripping-in-cave.wav')),
			"cave2":pygame.mixer.Sound(os.path.join("data", 'sons', '199515__everythingsounds__cave-drips.wav')),
			"cave3":pygame.mixer.Sound(os.path.join("data", 'sons', '270387__littlerobotsoundfactory__ambience-cave-00.wav'))
			}
		self.sons = {
			'pas':pygame.mixer.Sound(os.path.join("data", 'sons', 'Footsteps-SoundBible.com-534261997.wav')),
			'depoussiere':pygame.mixer.Sound(os.path.join("data", 'sons', 'karate_kid_punch-Mike_Koenig-732906088.wav')),
			'eboulement':pygame.mixer.Sound(os.path.join("data", 'sons', 'Rock_Slide-SoundBible.com-2065164739.wav')),
			'gagne':pygame.mixer.Sound(os.path.join("data", 'sons', 'A-Tone-His_Self-1266414414.wav')),
			'porte':pygame.mixer.Sound(os.path.join("data", 'sons', '386876__connorm94__footstep-rock.wav'))
			}
		#CHARGEMENTS DES POLICES
		self.font = pygame.font.Font(os.path.join("data", 'polices', 'diogenes.ttf'), 30)


	def update_options(self, options):
		for s in self.ambiances: self.ambiances[s].set_volume(options.volambiances)
		for s in self.sons: self.sons[s].set_volume(options.volsons)
		self.noir = pygame.Surface(options.taillefenetre)
		self.noir.fill(NOIR)
		self.bronze = pygame.Surface(options.taillefenetre)
		self.bronze.fill(BRONZESOMBRE)
		self.bronze.set_alpha(180)
		self.tmptxt = pygame.Surface(options.taillefenetre)
		self.tmptxt.fill(VERT)
		self.tmptxt.set_colorkey(VERT)
		
		
	def texte_to_tmptxt(self, nom, langue, **kwargs):
		interligne = 50
		for i, ligne in enumerate(self.txtmenus[nom][langue].split('\n')):
			surf = self.font.render(ligne, True, BRONZESOMBRE, BRONZE)
			left, y = surf.get_rect(**kwargs).topleft
			top = y + i*interligne
			self.tmptxt.blit(surf,(left, top))
			
			
	def nettoyer_tmptxt(self):
		self.tmptxt.fill(VERT)


	def charger_images(self, attribut, *noms):
		"""
		noms et nomscles peuvent etre des iterateurs
		"""
		if not noms: noms = (f[:-4] for f in os.listdir(os.path.join("", "data", "images", attribut)))
		d = getattr(self, attribut)
		d.update({i:pygame.image.load(os.path.join("data", "images", attribut, i+".png")).convert_alpha() for i in noms})
		

	def charger_images_noalpha(self, attribut, *noms):
		"""
		noms et nomscles peuvent etre des iterateurs
		"""
		d = getattr(self, attribut)
		d.update({i:pygame.image.load(os.path.join("data", "images", attribut, i+".png")).convert() for i in noms})


	def charger_textes(self, attribut):
		"""charger les textes de l'attribut attribut'
		"""
		with open(os.path.join("data", 'textes', attribut+'.csv'), 'rb') as f: 
			lecteur = unicode_csv_reader(f, delimiter=',')
			lecteur.next()
			setattr(self, 'txt'+attribut, {l[0]:[l[langue] for langue in self.langues] for l in lecteur})
		
		
	def charger_skins(self, *noms):
		tpspas = [200,200,200,200,200]
		for n in noms:
			self.skins[n] = {}
			img = planche_to_liste(os.path.join("data", "images", "skins", n+".png"), 20, 3)
			self.skins[n][IDLE] = pyganim.PygAnimation(zip(img[:2],(1200,800)))
			self.skins[n][N] = pyganim.PygAnimation(zip(img[20:25],tpspas))
			self.skins[n][NE] = pyganim.PygAnimation(zip(img[25:30],tpspas))
			self.skins[n][E] = pyganim.PygAnimation(zip(img[30:35],tpspas))
			self.skins[n][SE] = pyganim.PygAnimation(zip(img[35:40],tpspas))
			self.skins[n][S] = pyganim.PygAnimation(zip(img[40:45],tpspas))
			self.skins[n][SW] = pyganim.PygAnimation(zip(img[45:50],tpspas))
			self.skins[n][W] = pyganim.PygAnimation(zip(img[50:55],tpspas))
			self.skins[n][NW] = pyganim.PygAnimation(zip(img[55:],tpspas))
			
			
	def charger_decors(self, *noms):
		for n in noms:
			path = os.path.join("", "data", "images", "decors", n)
			self.decors[n] = {}
			for k in (f for f in os.listdir(path) if f.endswith(".png")):
				self.decors[n][k] = pygame.image.load(os.path.join(path, k)).convert_alpha()
			for d in (i for i in os.listdir(path) if isdir(os.join(path, i))):
				self.decors[n][d] = {}
				if d == 'sols':
					for k in (f for f in os.listdir(path) if f.endswith(".png")):
						self.decors[n][d][k] = pygame.image.load(os.path.join(path, d, k)).convert()
				else: 
					for k in (f for f in os.listdir(path) if f.endswith(".png")):
						self.decors[n][d][k] = pygame.image.load(os.path.join(path, d, k)).convert_alpha()
							
				
	def associer_decor_ambiance(self, decor, ambiance):
		self.decors[decor]['ambiance'] = ambiance

"""a coder:
- des bulles pour le texte
- menu deroulant pour le choix de perso et de decors etc..."""
