#!/usr/bin/python3
# -*- coding: Utf-8 -*

import random


def autour_direct(salle, xg, yg):
	"""(Salle, (int)) -> None
	renvoie un iterateur des coordonnees des premiers voisins directs de coords en excluant les cases hors de la salle
	"""
	for i,j in ((xg-1, yg),(xg+1, yg),(xg, yg-1),(xg, yg+1)):
		if salle.sol[i][j]: yield (i,j)

def autour(salle, xg, yg):
	"""(Salle, (int)) -> None
	renvoie un iterateur des coordonnees des premiers voisins (direct et en diagonal) de coords en excluant les cases hors de la salle
	"""
	for i in autour_direct(salle, xg, yg): yield i
	for i,j in ((xg-1, yg-1),(xg+1, yg+1),(xg+1, y-1),(xg-1, yg+1)):	
		if not salle.sol[i][j]: yield (i,j)

def autour_accessible(salle, xg, yg):
	"""(Salle, (int)) -> None
	renvoie un iterateur des coordonnees des premiers voisins (direct et en diagonal) qui on un sol depoussiere et not occupe
	"""
	return (case for case in autour(salle, xg, yg) if salle.sol_accessible(xg, yg))

def autour_rayon(salle, xg, yg, rayon):
	"""(Salle, (int), int) -> None
	renvoie un iterateur des coordonnees des voisins (direct et en diagonal) dans un rayon rayon de coords en excluant les cases hors de la salle ou trouees
	"""
	xr, yr = xg-rayon, yg-rayon
	for i in (xr+k for k in xrange(2*rayon+1)):
		for j in (yr+k for k in xrange(2*rayon+1)):
			try:
				if salle.sol[i][j] and salle.chiffres[i][j] != -1: 
					yield (i,j)
			except IndexError: pass

def creer_n_trous_aleatoire(salle, n):
	"""(SalleDemineur, int) -> None
	creer n trous dans la salle de maniere aleatoire
	"""
	coords = salle.cases_ensalle_non_pti()
	coordtrous = random.sample(coords, n)
	for (i,j) in coordtrous: salle.chiffres[i][j] = -1

def creer_n_trous_accretion(salle, n, rayon = 3):
	"""(SalleDemineur, int, int) -> None
	creer n trous dans la salle de maniere semi-aleatoire (chaines discontinues a partir de radicaux)
	"""
	coordrad = random.sample(salle.cases_ensalle_non_pti(), n//6)
	compt = 0
	while compt < n:
		nextcoordrad = []
		for (i, j) in coordrad:
			compt += 1
			salle.chiffres[i][j] = -1
			if compt != n:
				nextcoordrad.append(random.choice(((a, b) for a, b in autour_rayon(salle, i, j, rayon) if (a,b) not in salle.pti)))
		coordrad = nextcoordrad

def creer_n_points_interet(salle, n):
	#on suppose que la salle non pleine se cree par accretion a partir des chemins entre points d'interet
	coordpti = random.sample([(i,j) for j in xrange(salle.h) for i in xrange(salle.l)])
	for (i,j) in coordtrous: salle.salle[i][j] = 2

		

#def relier_points_interet(salle, pti):#en construction
#	pointe = pti[0]
#	but = pti[1]
#	fpti = pti[1:]
#	chemin = set([pointe])
	#creer un chemin entre les deux premiers pti
#	while but not in tourpointe:
#		vecbut = (pointe[])
	
	#creer un chemin entre les pti restants et le chemin existant
#	if len(pti)>2:
#		for ptiinit in pti[2:]:
#			while not tourpointe.union(chemin):


#def poscase_to_posperso(poscase):
#	return poscase[0]*LCASE + LORIGINE, (poscase[1]-2)*HCASE + HORIGINE

#def poscase_to_pos(poscase):
#	return poscase[0]*LCASE + LORIGINE, poscase[1]*HCASE + HORIGINE

def cases_to_direc(chemin, run = False):
	"""renvoie une liste de directions a partir d'une liste de cases
	"""
	direcs = []
	for i in range(len(chemin)-1):
		vec = (chemin[i+1][0] - chemin[i][0], chemin[i+1][1] - chemin[i][1])
		direcs.append(DIRECTIONS[vec])		
	return direcs

#def ligne(salle, a, b):
#	"""(Salle, (int), (int)) -> [(int)]
#	renvoie la liste de cases creant une ligne de a a b (algo de Bresenham)
#	"""
#	xa, xb, ya, yb = a[0], b[0], a[1], b[1]
#	derr = abs(float(yb - ya)/(xb - xa))
#	ligne = []
#	err = 0.
#	#cas 1er octant
#	y = ya
#	for x in range(xa, xb+1):
#		ligne.append((x, y))
#		err = err + derr
#		if derr >= 0.5:
#			y += 1
#			err -= 1
#	return ligne

def ligne_naif(salle, a, b):
	"""Salle, (int), (int)) -> [(int)]
	renvoie la liste de cases creant une ligne de a a b (algo naif)
	"""
	#cas des lignes vertic et horiz
	if b[0]-a[0] == 0: 
		signe = (b[1]-a[1])/abs(b[1]-a[1])
		return [(a[0], y) for y in range(a[1], b[1] + signe, signe)]
	signe = (b[0]-a[0])/abs(b[0]-a[0])
	if b[1]-a[1] == 0: return [(x, a[1]) for x in range(a[0], b[0] + signe, signe)]
	#cas des autres
	pente = float((b[1]-a[1]))/(b[0]-a[0])
	abspente = abs(pente)
	print pente, abspente, signe
	if abspente <= 1: return [(x, a[1]+int(pente*(x-a[0]))) for x in range(a[0], b[0] + signe, signe)]
	else: 
		invpente = 1./pente
		return [(a[0]+int(invpente*(y-a[1])), y) for y in range(a[1], b[1] + signe, signe)]

def plus_court_chemin(salle, a, b):
	"""Salle, (int), (int)) -> [(int)]
	renvoie la liste de cases constituant le plus court chemin de a a b (test ligne puis Djiskra si horssalle)
	"""
	if isinstance(b, tuple):
		ligne = ligne_naif(salle, a, b)
		#si toutes les cases de la ligne sont visibles, renvoie la ligne
		if all([salle.sol_visible(case) for case in ligne]): return ligne
		else: b = list(b)
	#sinon renvoie resultat de Djikstra
	#based on code from Janne Karila https://codereview.stackexchange.com/questions/79025/dijkstras-algorithm-in-python	
	A = {c: None for c in salle.cases_visibles()}
	queue = [(0, a, a)]
	while queue:
	    path_len, v, prec = heappop(queue)
	    if A[v] is None: # v is unvisited
	        A[v] = (path_len, prec)
	        for w in autour_visible(salle, v):
	            if A[w] is None: # w is unvisited and can be walked on
					#print queue, v, w
					heappush(queue, (path_len + 1, w, v))
					if w in b: break
	#reconstituer le chemin
	chemin = [w]
	while chemin[-1] != a:
		w = A[w][1]
		chemin.append(w)
	chemin.reverse()
	return chemin


if __name__ == '__main__':
	SalleDemineur(20, 5, 2, 30).dessiner_terminal()
