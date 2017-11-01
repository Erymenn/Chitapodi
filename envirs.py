import pygame
import copy
from pygame.locals import *
from constantes import *
from fonctions import afficher_bronze, afficher_tmptexte, photographier

class Texte(pygame.sprite.Sprite):
	
	def __init__(self, nom, xtxt, ytxt):
		self.nom = nom
		self.xtxt = xtxt
		self.ytxt = ytxt
		pygame.sprite.Sprite.__init__(self)
		
		
	def initialiser(self, joueur, biblio):
		"""creer la surface correspondante sur la surface tmptxt de la biblio
		"""
		biblio.texte_to_tmptxt(self.nom, joueur.options.langue, left = self.xtxt, top = self.ytxt)

	def afficher(self, fenetre, joueur, biblio): pass



class Bouton(Texte):
	"""
	"""

	def __init__(self, nom, x, y, l, h, xtxt = None, ytxt = None, verrou = False, image = None):
		"""cree une zone clicable de nom nom, de dimension (l,h), de position (x,y) et pouvant contenir un texte a la position (xtxt, ytxt) ou une image de verrou si verrou=True
		"""
		self.nom = nom
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(x,y,l,h)
		self.verrou = verrou
		self.xtxt = xtxt#-1 indique absence de texte
		self.ytxt = ytxt
		self.image = image
		self.visible = False


	def initialiser(self, joueur, biblio):
		"""creer la surface correspondant au texte sur la surface tmptxt de la biblio si le bouton n'est pas verrouille'
		"""
		if self.xtxt != -1 and not self.verrou: 
			kwargs = {}
			if self.xtxt: kwargs['left'] = self.xtxt
			else: kwargs['centerx'] = self.rect.centerx
			if self.ytxt: kwargs['top'] = self.ytxt
			else: kwargs['centery'] = self.rect.centery
			biblio.texte_to_tmptxt(self.nom, joueur.options.langue, **kwargs)


	def afficher(self, fenetre, joueur, biblio):
		if self.verrou: fenetre.blit(biblio.menus['verrou'], (self.rect.centerx-25, self.rect.centery-25))
		elif self.image and self.visible: fenetre.blit(biblio.menus[self.image], self.rect)



class Environnement:
	"""
	"""

	def __init__(self): pass

	def update(self, joueur, biblio): pass
		
	def clic(self, event, joueur, biblio): pass

	def touche(self, event, joueur, biblio): pass

	def afficher(self, fenetre, joueur, biblio): pass
		

class Menu(Environnement):
	"""
	"""

	def update(self, joueur, biblio):
		"""si etat=initialiser, lancer la musique si elle n'est pas deja la et mettre les boutons a jour
		"""
		if joueur.etat == INITIALISER or joueur.etat == REPRENDRE:
			#musique: si c'est celle du menu continuer, si il n'y en a pas ou c'est une autre, mettre celle du menu
			joueur.jouer(biblio, 'instinct')
			biblio.nettoyer_tmptxt()
			for b in self.group: b.initialiser(joueur, biblio)
			joueur.etat = None
		
	def cible_clic(self, joueur):
		cible = None
		for b in (i for i in self.group if isinstance(i, Bouton)):
			if not b.verrou and b.rect.collidepoint(joueur.poscurseur): cible = b.nom
		return cible		

	def clic(self, event, joueur, biblio):
		cible = Menu.cible_clic(self, joueur)
		if cible:
			if cible == "quitter": joueur.etat = QUITTER
			elif cible == 'reprendre': joueur.envir, joueur.etat = joueur.lastenvir, REPRENDRE
			else: 
				joueur.envir = cible
				joueur.etat = INITIALISER

	@afficher_tmptexte
	def afficher(self, fenetre, joueur, biblio):
		"""affiche le fond du menu et les textes des boutons dans la langue choisie
		"""
		fenetre.blit(biblio.menus[self.__class__.__name__[5:]], (0,0))
		for b in self.group: b.afficher(fenetre, joueur, biblio)


class Ecran_titre(Environnement):
	"""si etat=initialiser, lancer la musique
	si une touche ou bouton a ete touche, estomper l'ecran
	"""

	def __init__(self):
		"""
		"""
		self.testompe = 1*TIC#(en frames)
		self.noir = None

	def update(self, joueur, biblio):
		"""
		"""
		if joueur.etat == INITIALISER or joueur.etat == REPRENDRE: 
			joueur.jouer(biblio, 'instinct')
			self.noir = pygame.Surface(joueur.options.taillefenetre)
			self.noir.fill(NOIR)
			joueur.etat = CHARGER
			joueur.lastenvir = "ecran_titre"
			biblio.tmpimage = biblio.menus["ecran_titre"]
		elif joueur.etat == CHARGER:
			biblio.charger_skins('khan_classique')#toutes les skins debloquees
			biblio.charger_decors('defaut')#toutes les decors debloquees
			biblio.associer_decor_ambiance('defaut', 'cave1')
			biblio.charger_textes('menus')
			joueur.etat = None
		elif joueur.etat == ESTOMPER:
			joueur.tempo += 1
			self.noir.set_alpha(int(float(joueur.tempo)/self.testompe*255))
			if joueur.tempo == self.testompe:
				joueur.envir = 'principal'
				joueur.etat = INITIALISER
		
		
	def clic(self, event, joueur, biblio):
		"""si une touche ou bouton a ete touche, estomper l'ecran
		"""
		if not joueur.etat:
			joueur.etat = ESTOMPER
			joueur.tempo = 0

	def touche(self, event, joueur, biblio):
		"""si une touche ou bouton a ete touche, estomper l'ecran
		"""
		if not joueur.etat:
			joueur.etat = ESTOMPER
			joueur.tempo = 0

	def afficher(self, fenetre, joueur, biblio):
		fenetre.blit(biblio.menus["ecran_titre"], (0,0))
		if joueur.etat == ESTOMPER: fenetre.blit(self.noir, (0,0))
	
	
	
class Menu_principal(Menu):
	"""donne acces aux 3 emplacements de sauvegardes, aux modes de jeu, aux options, aux credits et aux ecrans de succes et de collections
	quand on arrive de l'ecran titre ou qu'on passe a un autre menu, la musique est conservee
	quand on arrive de pause, la musique est lancee
	lorsque la langue change, les textes des boutons aussi
	en appuyant sur un bouton on change de menu
	"""

	def __init__(self):
		self.group = pygame.sprite.Group(
			Bouton('quitter',945,21,47,47,-1),
			Bouton('aide',876,21,47,47,-1),
			Bouton('emplacement_1',70,70,335,107,90,90),
			Bouton('emplacement_2',70,210,335,107,90,230),
			Bouton('emplacement_3',70,350,335,107,90,370),
			Bouton('credits',38,507,180,54),
			Bouton('succes',490,410,216,100, verrou = True),
			Bouton('collections',730,410,216,100, verrou = True),
			Bouton('options',846,153,146,116),
			Bouton('jeu_libre',468,90,336,106),
			Bouton('mode_histoire',468,250,336,106, verrou = True)
			)		

	def update(self, joueur, biblio):
		if joueur.etat == INITIALISER: joueur.lastenvir = "principal"
		Menu.update(self, joueur, biblio)


	def clic(self, event, joueur, biblio):
		if event.type == MOUSEBUTTONUP:
			cible = Menu.cible_clic(self, joueur)
			if cible:
				if cible == 'quitter': joueur.etat = QUITTER
				elif cible[:-2] == 'emplacement':
					joueur.sauvegarder()
					joueur.charger(cible[-1])
					biblio.update_options(joueur.options)
					joueur.envir = 'principal'
					joueur.etat = INITIALISER
				else: 
					joueur.envir = cible
					joueur.etat = INITIALISER


class Menu_pause(Menu):
	"""la musique s'arrete (pause)
	l'ecran sur lequel on peut reprendre s'affiche en fond
	"""

	def __init__(self):
		self.group = pygame.sprite.Group(
			Bouton('reprendre',362,130,300,70),
			Bouton('options',362,220,300,70),
			Bouton('principal',362,310,300,70),
			Bouton('quitter',362,400,300,70)
			)

	def update(self, joueur, biblio):
		"""
		"""
		if joueur.etat == INITIALISER: 
			biblio.nettoyer_tmptxt()
			for b in self.group: b.initialiser(joueur, biblio)
			joueur.channelambiance.pause()
			joueur.etat = PHOTOGRAPHIER
			
	@photographier
	@afficher_tmptexte
	@afficher_bronze
	def afficher(self, fenetre, joueur, biblio):
		"""affiche le fond du menu et les textes des boutons dans la langue choisie
		"""
		fenetre.blit(biblio.menus['pause'], (332,100))


class Menu_credits(Menu):

	def __init__(self):
		self.group = pygame.sprite.Group(
			Bouton('principal',945,21,47,47,-1),
			Texte('txt_credits',100,100)
			)


class Menu_aide(Menu):

	def __init__(self):
		self.group = pygame.sprite.Group(
			Bouton('reprendre',945,21,47,47,-1)
			)


class Menu_options(Menu):
	"""
	"""

	def __init__(self):
		self.group = pygame.sprite.Group(
			Bouton('reprendre',682,50,50,50,-1),
			Bouton('aide',682,130,50,50,-1),
			Bouton('fr',342,490,86,60,-1),
			Bouton('eng',582,490,110,60,-1),
			Bouton('perso',292,200,80,180,-1),
			Bouton('fullscreen',682,230,20,20,-1,image = "bouton20x20"),
			Bouton('curseur',682,280,20,20,-1,image = "bouton20x20"),
			Bouton('autozoom',682,330,20,20,-1,image = "bouton20x20"),
			Texte('txt_fullscreen',422,225),
			Texte('txt_curseur',422,275),
			Texte('txt_zoom',422,325),
			Texte('txt_auto',597,325),
			Texte('txt_nb_trous',322,420),
			Bouton('no_ambiances',352,75,30,30,-1),
			Bouton('no_sons',352,125,30,30,-1)
			)
		for i in xrange(3):
			self.group.add(
				Bouton('zoom'+str(i),527+i*20,325,10,30,-1,image = "bouton10x30"),
				Bouton('nb_trous'+str(i),652+i*20,420,10,30,-1,image = "bouton10x30")
				)
		for i in xrange(10):
			self.group.add(
				Bouton('ambiances'+str(i),407+i*20,75,10,30,-1,image = "bouton10x30"),
				Bouton('sons'+str(i),407+i*20,125,10,30,-1,image = "bouton10x30")
				)

	def update(self, joueur, biblio):
		"""si etat=initialiser, lancer la musique si elle n'est pas deja la et mettre les boutons a jour
		"""
		if joueur.etat == INITIALISER: 
			biblio.skins[joueur.perso]['idle'].play()
			for b in self.group:
				tri = b.nom[:3]
				if b.nom in 'curseur autozoom fullscreen'.split():
					b.visible = getattr(joueur.options, b.nom)
				elif tri == "son" or tri == 'amb':
					b.visible = getattr(joueur.options,'vol'+b.nom[:-1])*10 >= int(b.nom[-1])+1
				elif tri == "zoo" or tri == 'nb_':
					b.visible = getattr(joueur.options, b.nom[:-1]) >= int(b.nom[-1])
		Menu.update(self, joueur, biblio)
		if joueur.etat == CHANGER_FULLSCREEN: 
			if joueur.options.fullscreen: fenetre = pygame.display.set_mode(joueur.options.taillefenetre, pygame.FULLSCREEN)
			else: fenetre = pygame.display.set_mode(joueur.options.taillefenetre)
			joueur.etat = None
		elif joueur.etat == REVISER_VOLUME: #bof, peut etre mieux avec joueur.channelambiance
			for s in biblio.ambiances: biblio.ambiances[s].set_volume(joueur.options.volambiances)
			for s in biblio.sons: biblio.sons[s].set_volume(joueur.options.volsons)
			joueur.etat = None
		elif joueur.etat == REVISER_JEU: pass


	def clic(self, event, joueur, biblio):
		if event.type == MOUSEBUTTONUP:
			cible = Menu.cible_clic(self, joueur)
			if cible:
				tri = cible[:3]
				if tri == "txt": pass
				elif cible == 'reprendre': joueur.envir, joueur.etat = joueur.lastenvir, REPRENDRE
				elif cible in biblio.langues:
					joueur.options.langue = cible
					joueur.etat = INITIALISER
				elif cible == 'autozoom':
					b = [sp for sp in self.group if sp.nom == cible][0]
					b.visible = not b.visible
					setattr(joueur.options, cible, b.visible)
				elif cible == 'curseur': 
					b = [sp for sp in self.group if sp.nom == cible][0]
					b.visible = not b.visible
					setattr(joueur.options, cible, b.visible)
					pygame.mouse.set_visible(not b.visible)
				elif cible == 'fullscreen':
					b = [sp for sp in self.group if sp.nom == cible][0]
					b.visible = not b.visible
					setattr(joueur.options, cible, b.visible)
					joueur.etat = CHANGER_FULLSCREEN#utiliser dans afficher
				elif tri == 'no_':
					for b in (sp for sp in self.group if sp.nom[:3] == cible[3:6]): b.visible = False
					setattr(joueur.options, "vol"+cible[3:], 0.)
					joueur.etat = REVISER_VOLUME
				elif tri == "son" or tri == 'amb':
					i = int(cible[-1])
					dic = {int(sp.nom[-1]) : sp for sp in self.group if sp.nom[:3] == tri}
					for d in dic: dic[d].visible = d<=i
					setattr(joueur.options, "vol"+cible[:-1], (i+1.)/10)
					joueur.etat = REVISER_VOLUME
				elif tri == "zoo" or tri == 'nb_':
					i = int(cible[-1])
					dic = {int(sp.nom[-1]) : sp for sp in self.group if sp.nom[:3] == tri}
					for d in dic: dic[d].visible = d<=i
					setattr(joueur.options, cible[:-1], i)
					joueur.etat = REVISER_JEU
				else: 
					joueur.envir = cible
					joueur.etat = INITIALISER


	@photographier
	@afficher_tmptexte
	@afficher_bronze
	def afficher(self, fenetre, joueur, biblio):
		"""affiche le fond du menu et les textes des boutons dans la langue choisie
		"""
		fenetre.blit(biblio.menus['options'], (260,20))
		biblio.skins[joueur.perso][IDLE].blit(fenetre, (292,200))
		for b in self.group: b.afficher(fenetre, joueur, biblio)


class Menu_jeu_libre(Menu):
	"""
	"""

	def __init__(self):
		"""etats possibles: initialiser
		"""
		self.fond = pygame.image.load("images/ecran_titre.png").convert()
		self.ambiance = pygame.mixer.Sound('sons/bensound-instinct.mp3')
		self.sons = {'clic':pygame.mixer.Sound('sons/')}
		
	def clic():
		pass

	def touche():
		pass


class Menu_succes(Menu):
	"""
	"""

	def __init__(self):
		"""etats possibles: initialiser
		"""
		self.fond = pygame.image.load("images/ecran_titre.png").convert()
		self.ambiance = pygame.mixer.Sound('sons/bensound-instinct.mp3')
		self.sons = {'clic':pygame.mixer.Sound('sons/')}
		
	def clic():
		pass

	def touche():
		pass


class Menu_collections(Menu):
	"""
	"""

	def __init__(self):
		"""etats possibles: initialiser
		"""
		self.fond = pygame.image.load("images/ecran_titre.png").convert()
		self.ambiance = pygame.mixer.Sound('sons/bensound-instinct.mp3')
		self.sons = {'clic':pygame.mixer.Sound('sons/')}
		
	def clic():
		pass

	def touche():
		pass


