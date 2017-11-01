import pygame
from pygame.locals import *
from constantes import *
from envirs import Environnement
from fonctions_grilles import creer_n_trous_accretion, autour_rayon, autour, autour_direct, autour_accessible

def dessiner_terminal(func): 
	def f(liste): 
		for j in xrange(self.h):
			print "".join(liste)+"\n"
	return f
	

class Pti():#point d'interet'

	def __init__(self):
		pass
	
	def clic_gauche(self, joueur): pass
	
	def afficher(self, fenetre, joueur, biblio, pos): pass
	

class Porte(Pti):

	def __init__(self, verssalle, versposg, restiction = None):
		"""
		"""
		self.verssalle = verssalle
		self.versposg = versposg
		self.restiction = restiction
		
	def clic_gauche(self, joueur, biblio):
		"""si le personage est restreint, ecrire la bulle correspondante
			sinon deplacer le personnage a la salle et la position prevue
		"""
		joueur.set_sallecour(self.verssalle)
		joueur.posg = self.posg
		pygame.mixer.play(biblio.sons['porte'])
		
			
		
class Collectable(Pti):

	def __init__(self, nom):
		self.nom = nom
		self.proprio = None

	def clic_gauche(self, joueur, biblio):
		"""si le personage est restreint, ecrire la bulle correspondante
			sinon deplacer le personnage a la salle et la position prevue
		"""
		joueur.progression.collectables[self.proprio].append(self.nom)
		pygame.mixer.play(biblio.sons['getobj'])
		#jouer la cinematique de rammassage et bloquer les clics
		
	def afficher(self, fenetre, joueur, biblio, pos):
		fenetre.blit(biblio.collectables[self.nom], pos)
		
		
		
class Monnaie(Pti):

	def __init__(self, montant):
		self.montant = montant
		
	def clic_gauche(self, joueur, biblio):
		"""si le personage est restreint, ecrire la bulle correspondante
			sinon deplacer le personnage a la salle et la position prevue
		"""
		joueur.progression.monnaie += self.montant
		pygame.mixer.play(biblio.sons['getobj'])
		#jouer la cinematique de rammassage et bloquer les clics
		
	def afficher(self, fenetre, joueur, biblio, pos):
		fenetre.blit(biblio.collectables[self.montant], pos)
		
class Decor(Pti):

	def __init__(self, cle):
		self.cle = cle
		
	def afficher(self, fenetre, joueur, biblio, pos):
		fenetre.blit(biblio.decors[joueur.decor]['elements'][cle], pos)


class Salle:

	def __init__(self, l, h, pti, fichier = None):
		"""Cree une salle
		l: int: longueur, nombre de cases a l'horizontale
		h: int: hauteur, nombre de cases a la verticale
		origine: [int, int]: coin superieur gauche, peut etre hors de la fenetre
		pti: {(int, int): Pti}: dictionnaire des points d'interets presents, les deux entiers marquent la position dans la salle
		murs: [[int, int, int]]:
		sol: [[]] l+1xh+1: None ou False si la case est horssalle, True si dans la salle mais masquee par un grand sol, int = cle du sol
		"""
		self.l = l
		self.h = h
		self.charger_fond(fichier)
		self.pti = pti
		self.originex = LORIGINE
		self.originey = HORIGINE#top left of the grid (could be negative)
		#creer des points d'interet si les coordonnees ne sont pas precisees
		#prevoir restriction pour avoir pti sur bord (entree et sortie)
		#creer des chemins reliants les points d'interet (au moins 2 pti)
		#relier_points_interet(self, pti)
		
	def charger_fond(self, fichier = None):
		if not fichier: 
			self.murs = [0, -3, "11x3"]
			self.sol = [["1x1" for j in xrange(h+1)] for i in xrange(l+1)]
			for i in xrange(l): self.horssalle[i][h] = None
			for j in xrange(h+1): self.horssalle[l][j] = None
		else: pass
		
	def pos_to_posg(self, x, y):
		return (x-self.originex)//LCASE, (y-self.originey)//HCASE
		
	def posg_to_pos(self, xg, yg):
		return xg*LCASE + self.originex, yg*HCASE + self.originey

	def posg_to_posperso(self, xg, yg):
		return xg*LCASE + self.originex, yg*HCASE + self.originey-120
		
	def posperso_to_posg(self, x, y):
		return (xg-self.originex)//LCASE, (yg-self.originey+120)//HCASE

	def cases_ensalle(self):
		"""renvoie une liste des cases dans la salle non horssalle
		"""
		return [(i,j) for j in xrange(self.h) for i in xrange(self.l) if self.sol[i][j]]

	def cases_accessibles(self):
		"""renvoie une liste des cases visibles et non trouees
		"""
		return [(i,j) for j in xrange(self.h) for i in xrange(self.l) if self.sol_accessible((i, j))]

	def cases_ensalle_non_pti(self):
		"""renvoie une liste des cases dans la salle non horssalle et non pti
		"""
		return [(i,j) for j in xrange(self.h) for i in xrange(self.l) if self.sol[i][j] and (i, j) not in self.pti]
		
	def itercases_ensalle(self):
		"""renvoie une liste des cases dans la salle non horssalle
		"""
		return ((i,j) for j in xrange(self.h) for i in xrange(self.l) if self.sol[i][j])

	def itercases_accessibles(self):
		"""renvoie une liste des cases accessibles
		"""
		return ((i,j) for j in xrange(self.h) for i in xrange(self.l) if self.sol_accessible((i, j)))

	def itercases_ensalle_non_pti(self):
		"""renvoie une liste des cases dans la salle non horssalle et non pti
		"""
		return ((i,j) for j in xrange(self.h) for i in xrange(self.l) if self.sol[i][j] and (i, j) not in self.pti)

	@dessiner_terminal
	def dessiner_horssalle_terminal(self):
		return (str(self.sol[i][j]) for i in xrange(self.l))
		
	def afficher(self, fenetre, joueur, biblio):
		#afficher les murs
		for xg, yg, cle in self.murs:
			fenetre.blit(biblio.decors[joueur.decor]['murs'][cle], self.posg_to_pos(xg, yg))
		#afficher les sols
		for yg in xrange(self.sallecour.h):
			for xg in xrange(self.sallecour.l):
				if isinstance(self.sallecour[xg][yg], int): #si None ou False, horssalle, si True, masque par grand sol
					fenetre.blit(biblio.decors[joueur.decor][sol][self.sallecour.sol[xg][yg]], self.posg_to_pos(xg, yg))
		#afficher les pti
		for (xg, yg), pti in self.pti.iteritems():
			pti.afficher(fenetre, joueur, biblio, self.posg_to_pos(xg, yg))


		

class Salle_demineur(Salle):

	def __init__(self, l, h, pti, ntrous, fichier = None):
		"""Cree une salle
		l: int: longueur, nombre de cases a l'horizontale
		h: int: hauteur, nombre de cases a la verticale
		origine: [int, int]: coin superieur gauche, peut etre hors de la fenetre
		pti: [[int, int, Pti]]: liste des points d'interets presents, les deux entiers marquent la position dans la salle
		murs: [[int, int, int]]:
		sol: [[]] l+1xh+1: None ou False si la case est hors salle, True si dans la salle mais masquee par un grand sol, int = cle du sol
		chiffres: [[]] lxh: chiffre[i][j] = nombre de trous autour de la case (i,j), si -1, c'est un trou
		poussiere: [[]] lxh: poussiere[i][j] = True s'il y a de la poussiere, sinon = None 
		marques: [[]] lxh: marques[i][j] = True s'il y a une marque, sinon = None
		"""
		Salle.__init__(self, l, h, pti, fichier)
		#creer des points d'interet si les coordonnees ne sont pas precisees
		#if isinstance(pti, int): creer_n_points_interet(self, pti)
		#creer des chemins reliants les points d'interet (au moins 2 pti)
		#relier_points_interet(self, pti)
		#ajouter les trous
		
		#completer la salle
		#if pleine: 
		#	for i in range(self.l):
		#		for j in range(self.h): 
		#			if not self.salle[i][j]: self.salle[i][j] = 1
		#else: None#a faire
		#creer la salle du nombre de trous a proximite
		#pas de marquage initial
		self.marques = [[None for j in xrange(h)] for i in xrange(l)]
		#initialiser les trous et les chiffres
		self.chiffres = [[None for j in xrange(h)] for i in xrange(l)]
		creer_n_trous_accretion(self, ntrous)
		for i in xrange(l):
			for j in xrange(h):
				self.chiffres[i][j] = sum(1 for (a, b) in autour(self, (i,j)) if self.chiffres[a][b] == -1)
		#creer la grille de poussiere qui masque les chiffres/trous/pti
		self.poussiere = [[bool(self.sol[i][j]) for j in xrange(h)] for i in xrange(l)]
		for (i, j, pti) in self.pti: self.poussiere[i][j] = False

	def sol_accessible(self, (xg, yg)):
		"""renvoie vrai si le sol existe, est depoussiere, non troue et non utilise par un pti
		"""
		return self.sol[xg][yg] and not self.poussiere[xg][yg] and self.chiffres[xg][yg] != -1 and (xg, yg) not in self.pti#!pti

	@dessiner_terminal
	def dessiner_chiffres_terminal(self):
		return (str(self.chiffres[i][j]) for i in xrange(self.l))

	@dessiner_terminal
	def dessiner_poussiere_terminal(self):
		return ('s' if self.poussiere[i][j] else '_' for i in xrange(self.l))

	@dessiner_terminal
	def dessiner_marques_terminal(self):
		return ('P' if self.marques[i][j] else '_' for i in xrange(self.l))

	@dessiner_terminal
	def dessiner_tout_terminal(self):
		"""
		"""
		res = ''	
		for i in xrange(self.l):
			if self.marques[i][j]: res+"P"
			elif self.poussiere[i][j]: res+"s"
			elif self.chiffres[i][j]: res+"O"
			elif self.chiffres[i][j]: res+str(self.chiffres[i][j])
			elif not self.sol[i][j]: res+" "
			elif (i, j) in self.pti: res+"X"
			else: res+"."


	def clic_droit(self, xg, yg):
		"""marque la case si elle ne l'est pas deja et la demarque sinon
		"""
		if self.poussiere[xg][yg]: 
			if self.marques[xg][yg]: self.marques[xg][yg] = None
			else: self.marques[xg][yg] = True


	def clic_gauche(self, xg, yg, joueur, biblio):
		"""retourne False si la case est marquee, retourne True si un trou est touche, retourne False et le clic gauche du pti si pti, retourne False et decouvre les cases vides attenantes sinon
		"""
		if self.marques[xg][yg]: return False
		elif self.chiffres[xg][yg] == -1: 
			self.poussiere[xg][yg] = False
			return True
		try: 
			self.pti[(xg, yg)].clic_gauche(joueur, biblio)
			return False
		except KeyError: pass
		def decouvrir_autour(i, j):
			"""retire la poussiere autour de la case tant que la bordure de zone decouverte comporte encore une case sans chiffre"""
			self.poussiere[i][c[1]] = False
			if self.chiffres[i][c[1]]: return False
			for (a, b) in autour(self, i, j):
				if self.poussiere[a][b]: decouvrir_autour(a, b)
		decouvrir_autour(xg, yg)
		return False

	def finie(self):
		"""retourne True si la salle est completee, False sinon
		"""
		return all((not self.poussiere[i][j]) ^ (self.chiffres[i][j] == -1) for i in xrange(self.l) for j in xrange(self.h))
		
	def afficher(self, fenetre, joueur, biblio):
		#afficher les murs
		for xg, yg, cle in self.murs:
			fenetre.blit(biblio.decors[joueur.decor]['murs'][cle], self.posg_to_pos(xg, yg))
		#afficher les sols
		for yg in xrange(self.sallecour.h):
			for xg in xrange(self.sallecour.l):
				if isinstance(self.sallecour.sol[xg][yg], int): #si None ou False, horssalle, si True, masque par grand sol
					fenetre.blit(biblio.decors[joueur.decor][sol][self.sallecour[xg][yg]], self.posg_to_pos(xg, yg))
				if self.sallecour.poussiere[xg][yg]: fenetre.blit(biblio.decors[joueur.decor]["poussiere"], pos)
				elif self.sallecour.chiffres[xg][yg]: fenetre.blit(biblio.decors[joueur.decor][str(self.sallecour.chiffres[xg][yg])], pos)
				if self.sallecour.marques[xg][yg]: fenetre.blit(biblio.decors[joueur.decor]["marque"], pos)
		#afficher les pti visibles
		for xg, yg, pti in self.pti:
			if not self.sallecour.poussiere[xg][yg]: pti.afficher(fenetre, biblio, self.posg_to_pos(xg, yg))
		

class Jeu(Environnement):
	"""
	"""

	def __init__(self):
		"""
		"""
		self.salles = []
		self.sallecour = None
		self.posg = (0,0)
		self.chemin = None
		self.boutonsouris = []#clic droit ou gauche et case
		self.plusxperfr = None#sequence de 0 et 1 a additionne a chaque frame (generateur) (sequence de la sequence de direction)
		self.plusyperfr = None#sequence de 0 et 1 a additionne a chaque frame (generateur)
		self.inddir = None#indice dans la sequence de la direction
		
	def charger_niveau(self): pass
		
		
	def creer_sequenceperfr(self, maxpix, tps):#le temps est en ms, la sequence est un generateur/queue (first in, first out)
		"""cree un generateur d'entiers qui donne le nombre de pixels a avancer a chaque frame
		"""
		nbfr = TIC*tps/1000
		assert isinstance(nbfr, int)
		plus = float(maxpix)/nbfr
		reste = plus		
		for i in xrange(nbfr):
			yield int(reste)#TIC*tps/1000 est le nombre de frames, peut etre supp ou inf a maxpix
			reste -= int(reste)
			reste += plus
			
			
	def charger_next_in_direction(self, biblio, joueur):
		"""charger la direction a partir de la premiere entree du chemin (qui est un generateur)
		"""
		self.inddir += 1
		try:
			past = biblio.deplacements[joueur.persoetat][TPS][inddir]
			self.plusxperfr = self.creer_sequenceperfr(biblio.deplacements[joueur.persoetat][PLUSX][inddir], past)
			self.plusyperfr = self.creer_sequenceperfr(biblio.deplacements[joueur.persoetat][PLUSY][inddir], past)
		except IndexError:
			self.inddir = 0
			try:
				joueur.persoetat = self.chemin.next()
				past = biblio.deplacements[joueur.persoetat][TPS][0]
				self.plusxperfr = self.creer_sequenceperfr(biblio.deplacements[joueur.persoetat][PLUSX][0], past)
				self.plusyperfr = self.creer_sequenceperfr(biblio.deplacements[joueur.persoetat][PLUSY][0], past)
			except StopIteration:
				joueur.persoetat = IDLE
				joueur.etat = AGIR
				biblio.sons['pas'].stop()
		
		
	def update(self, joueur, biblio):
		if joueur.etat == INITIALISER:
			joueur.channelambiance.fadeout(1)
			joueur.channelambiance.play(biblio.ambiances[biblio.decors[joueur.decor]['ambiance']], loops = -1)
			joueur.persoetat = IDLE
			biblio.skins[joueur.perso][joueur.persoetat].play()
			joueur.pos = self.posg_to_posperso((0,0))
			joueur.etat = None
		elif joueur.etat == REPRENDRE: pass
		elif joueur.etat == DEPLACER: 
			try:
				joueur.pos[0] += self.plusxperfr.next()
				joueur.pos[1] += self.plusyperfr.next()
			except StopIteration:
				biblio.skins[joueur.perso][joueur.persoetat].stop()
				self.charger_next_in_direction(biblio,joueur)
				biblio.skins[joueur.perso][joueur.persoetat].play()	
		elif joueur.etat == DEPLACER_CAMERA:
			sourisrel = pygame.mouse.get_rel()
			self.origine = [self.origine[i] + sourisrel[i] for i in xrange(2)]
			joueur.pos = [joueur.pos[i] + sourisrel[i] for i in xrange(2)]
		elif joueur.etat == AGIR:
			xg, yg = (self.pos_to_posg(joueur.poscurseur))
			#clic gauche
			if self.boutonsouris == 1: 
				perdu = self.salles[self.sallecour].clic_gauche((xg, yg), joueur, biblio)
				if perdu: biblio.sons['eboulement'].play()
			#clic droit
			elif self.boutonsouris == 3: self.salles[self.sallecour].clic_droit((xg, yg))
			if self.salles[self.sallecour].finie(): 
				biblio.sons['gagne'].play()
			joueur.etat = None
		
		
	def clic(self, event, joueur, biblio):
		if event.type == MOUSEBUTTONDOWN:
			if joueur.etat == None: 
				joueur.etat = DEPLACER_CAMERA
				self.originesouris = joueur.poscurseur
				pygame.mouse.get_rel()
				return
		elif event.type == MOUSEBUTTONUP:
			if joueur.etat == DEPLACER_CAMERA: joueur.etat = None
			self.boutonsouris = event.button
			#si le perso est en train de se deplacer, interrompre le mouvement a la prochaine case
			if joueur.etat == DEPLACER: 
				self.chemin = (x for x in [])#generateur vide
				return
			xg, yg = (self.pos_to_posg(joueur.poscurseur))
			#verifier qu'on clique bien sur la salle et pas sur un trou visible sinon rien
			if xg < -1 or xg > self.salles[self.sallecour].l \
				or yg < -1 or yg > self.salles[self.sallecour].h \
				or (self.salles[self.sallecour].salle[xg][yg] == -1 and not self.salles[self.sallecour].poussiere[xg][yg]): 
				return
			#sinon, si le perso n'est pas a cote, le perso se deplace, les actions sont reportees
			#si c'est vide (sans poussiere, trou, objet, porte) et accessible, le perso y va
			if self.posperso_to_posg(joueur.pos) not in autour_visible(self.salles[self.sallecour], (xg, yg)) and self.salles[self.sallecour].sol_visible((xg, yg)): 
				chemin = cases_to_direc(plus_court_chemin(salle, perso.case, (xg, yg)))
				joueur.etat = DEPLACER
				biblio.sons['pas'].play(loops = -1)
				return
			#sinon, si le perso est a cote, les actions sont effectuees
			joueur.etat = AGIR
		
		
	def afficher(self, fenetre, joueur, biblio):
		self.salles[self.sallecour].afficher(self, fenetre, joueur, biblio)
		biblio.skins[joueur.perso][joueur.persoetat].blit(fenetre, joueur.pos)
		fenetre.blit(biblio.decors[joueur.decor]['avantplan'], (0,0))

		

#	
#	#afficher le perso
#	if deplacement:
#	#le chemin est une liste de directions, les souschemins sont des tuples
#	#on a un compteur qui se remet a zero a chaque souspas
#	#12 frames par souspas et 5 souspas par pas
#	#un nombre indetermine de pas par chemin
#		if initdep:
##			#initier le prochain pas
##			direc = heappop(chemin)
##			pas = perso.anim[direc]
##			maxpas = len(pas)
##			comptpas = 0
##			#initier le prochain sspas
##			maxsspas, xplus, yplus, img = pas[0]
##			perso.pos = perso.pos[0] + xplus, perso.pos[1] + yplus
##			comptsspas = 0
##			initdep = False
##		if comptsspas == maxsspas:
##			#fin du souspas actuel
##			comptpas += 1
##			if comptpas == maxpas:
##				perso.case = (perso.case[0] + VECTEURS[direc][0], perso.case[1] + VECTEURS[direc][1])
##				if interrompre:
##					interrompre = False
##					deplacement, initdep = False, True
##					sonpas.stop()
##				elif not chemin:
##					deplacement, initdep = False, True
##					sonpas.stop()
##				else:
##					direc = heappop(chemin)
##					pas = perso.anim[direc]
##					maxpas = len(pas)
##					comptpas = 0
##			if comptpas != maxpas:
##				maxsspas, xplus, yplus, img = pas[comptpas]
##				perso.pos = perso.pos[0] + xplus, perso.pos[1] + yplus
##				comptsspas = 0
#		#temporaire
##		if not img: fenetre.blit(khan, perso.pos)
##		else: fenetre.blit(img, perso.pos)
##		comptsspas += 1	
##	else: 
##		frame = clock.time%3


	def touche(self, event, joueur, biblio):
		pass
		

class Jeu_libre(Jeu):
	"""
	"""
	
	def __init__(self):
		Jeu.__init__(self)
		
	def charger_niveau(self, nbsalles, l, h, prctrous):
		ntrous = int(l*h*prctrous)
		self.salles = [Salle_demineur(l, h, {(0,0): Pti(), (5,5): Porte(i+1, (0,0))}, ntrous) for i in xrange(nbsalles)]
		
	def update(self, joueur, biblio):
		if joueur.etat == INITIALISER: self.charger_niveau(2, 11, 6, 0.2)
		Jeu.update(self, joueur, biblio)
		
		



