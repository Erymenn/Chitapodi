import pygame
import pickle
import csv
import copy
import os


class Options:
	"""
	"""

	def __init__(self):
		"""Charge les options sauvegardees sinon charge les options par defaut (directement sauvegardable avec pickle)
		"""
		self.langue = 'eng'
		self.curseur = True
		self.volambiances = 1.#entre 0 et 1
		self.volsons = 1.#entre 0 et 1
		self.fullscreen = False
		self.taillefenetre = (1024, 600)
		self.zoom = 0
		self.nb_trous = 1
		self.autozoom = False
		
class Progression:
	"""objet contenant la progression du joueur (directement sauvegardable avec pickle)
	"""
	
	def __init__(self):
		self.niveaux = []#liste des niveaux entames dans leur etat d'avancement actuel (niveaux communs a tous perso)
		self.piece_persos = {s : None for s in 'khan fiona baudouin momie'.split()}
		self.monnaie = 0
		self.succes = []#liste de noms des succes gagnes 
		self.libre_fonds = []#liste de noms des fonds debloques pour le jeu libre 
		self.skins_persos = ['khan_classique', 'baudouin_classique', 'fiona_classique']#liste de noms des skins de persos debloques
		self.collectables = {s : [] for s in 'khan fiona baudouin momie'.split()}#liste de noms des collectables recuperes par perso


class Joueur:
	"""
	"""

	def __init__(self, fichier = None, emplacement = 1):
		if fichier:
			with open(os.path.join("data", "saves", fichier+".pickle"), "rb") as f: 
				self.emplacement, self.perso, self.options, self.progression, self.progavdestruction = pickle.load(f)
		else:
			self.emplacement = emplacement
			self.perso = 'khan_classique'
			self.options = Options()
			self.progression = None
			self.progavdestruction = None#la sauvegarde a recuperer en cas de destruction du monde a la fin du jeu
		self.envir = "ecran_titre"
		self.etat = 'initialiser'
		self.poscurseur = [0,0]
		self.channelambiance = pygame.mixer.Channel(1)
		self.lastenvir = None#utilise en cas de pause, options, etc
		self.lastimage = None#utilise en cas de pause, options, etc
		self.pos = [0,0]
		self.persoetat = "idle"
		self.decor = "defaut"
		

	def init_succes(self, biblio):
		self.succes = {[(i, False) for i in biblio.succes]}
		
	def set_piececour(self,nompiece): 
		self.progression.piece_persos[self.perso] = nompiece
		
	def get_piececour():
		return self.progression.piece_persos[self.perso]

	def sauver_last(self, fenetre):
		"""sauvegarder le dernier environnement visite
		"""
		self.lastenvir = self.envir

	def sauvegarder(self):
		"""sauvegarde la progression et les options, etc. en binaire dans le fichier save/emplacementself.emplacement.pickle
		"""
		with open(os.path.join("data", "saves", "emplacement"+str(self.emplacement)+".pickle"), "wb") as f: 
			pickle.dump((self.emplacement, self.perso, self.options, self.progression, self.progavdestruction), f, -1)

	def jouer(self, biblio, music):
		if not self.channelambiance.get_busy(): self.channelambiance.play(biblio.ambiances[music], loops = -1)
		else: 
			self.channelambiance.unpause()
			if self.channelambiance.get_sound() != biblio.ambiances[music]:
				self.channelambiance.stop()
				self.channelambiance.play(biblio.ambiances[music], loops = -1)

