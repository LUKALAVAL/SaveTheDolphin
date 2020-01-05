import tkinter as tk
import random as rd
import time

largeur = 100
hauteur = largeur

nbIle = 20

eau = 0
terre = 1
plage = 2

posInitIle = [(rd.randint(0,largeur-1),rd.randint(0,hauteur-1)) for i in range(nbIle)]
probAppTerre = 0.7

carte = [[eau for i in range(largeur)] for j in range(hauteur)]

moinsProb = 1-probAppTerre

for x,y in posInitIle[:nbIle]:
	carte[y][x] = terre
	
def creaIle(coord,prob):
	if prob > 0:
		x,y = coord
		for i in range(-1,2):
			for j in range(-1,2):
				if (x+i in list(range(0,largeur))) and (y+j in list(range(0,hauteur))) and carte[y+j][x+i] == eau:
					if rd.random() < prob:
						creaIle((x+i,y+j),prob-moinsProb)
						carte[y+j][x+i] = terre
						
for coord in posInitIle[:nbIle]:
	creaIle(coord,probAppTerre)
	
for x in range(largeur):
	for y in range(hauteur):
		if carte[y][x] == terre:
			for i in range(-1,2):
				for j in range(-1,2):
					if (x+i in list(range(0,largeur))) and (y+j in list(range(0,hauteur))) and carte[y+j][x+i] == eau :
						carte[y+j][x+i] = plage



def trouverDistance(coord1,coord2):
	x1,y1 = coord1
	x2,y2 = coord2
	return ((x1-x2)**2+(y1-y2)**2)**0.5
	
def trouverDroite(coord1,coord2):
	x1,y1 = coord1
	x2,y2 = coord2
	if x1 != x2:
		a = (y1-y2)/(x1-x2)
		b = y2-x2*a
		def droite(x,y):
			return a*x+b
	else:
		def droite(x,y):
			return y
	return droite

def obstacle(coord1,coord2):
	droite = trouverDroite(coord1,coord2)
	x1,y1 = coord1
	x2,y2 = coord2
	add = 0
	if x1 == x2: add = 1
	for x in range(min(x1,x2),max(x1,x2) + add): #car list(range(x,x)) = []
		borne1 = int(droite(x,y1))
		borne2 = int(droite(x+1,y2))
		for y in range(min(borne1,borne2),max(borne1,borne2)+1):
			if carte[y][x] == terre or carte[y][x] == plage:
				return True
	#can.create_line(x1*pas,y1*pas,x2*pas,y2*pas,fill = "gray50",dash=(5,6))
	return False
	


#ARRIÈRE PLAN------------------------------------------------------------------------------
pas = 900//largeur
largeurCanvas = largeur*pas
hauteurCanvas = hauteur*pas

fen = tk.Tk()
fen.title("Save The Dolphin")

can = tk.Canvas(fen, width = largeurCanvas, height = hauteurCanvas)
can.pack(side=tk.LEFT, padx=5, pady=5)
	
condition = [eau,terre,plage]
couleur = ['cornflower blue', 'sea green','bisque2']

def trouverCouleur(coord):
	y,x = coord
	return couleur[carte[y][x]]

def carre(ordonnee, abscisse, couleur):
	can.create_rectangle(abscisse, ordonnee, abscisse + pas, ordonnee + pas, fill=couleur, outline = couleur)

for ordonnee in range(hauteur):
	for abscisse in range(largeur):
		carre(ordonnee*pas,abscisse*pas,trouverCouleur((ordonnee,abscisse)))


#PROCEDURES SECONDAIRES--------------------------------------------------------------------
#score
score = 0
def scoring():
	affichageScore.configure(text = "SCORE : " + str(score))
affichageScore = tk.Label(fen)
affichageScore.pack(side=tk.BOTTOM,padx=2,pady=5)

#menu
tk.Button(fen, text ='Restart').pack(side=tk.TOP, padx=10, pady=5)
tk.Button(fen, text ='  Quit  ',command=fen.destroy).pack(side=tk.TOP, padx=10, pady=5)
#trainée d'écume

#JOUEUR------------------------------------------------------------------------------------
x0,y0 = rd.randint(0,largeur-1),rd.randint(0,hauteur-1)
while carte[y0][x0] != eau:
	x0,y0 = rd.randint(0,largeur-1),rd.randint(0,hauteur-1)
x0,y0 = x0*pas,y0*pas

def placerJoueur():
	can.create_rectangle(x0,y0,x0+pas,y0+pas,fill="tomato",tags="joueur")
	
def supprimerJoueur():
	can.delete(fen,"joueur")

def mouvementJoueur(event):
	global x0,y0,score
	x,y = x0,y0
	if event.char in ["a","q"]:
		x -= pas
	elif event.char == "d":
		x += pas
	elif event.char in ["w","z"]:
		y -= pas
	elif event.char == "s":
		y += pas
	elif event.char == " ": #teleportation
		x,y = rd.randint(0,largeur-1),rd.randint(0,hauteur-1)
		while carte[y][x] != eau:
			x,y = rd.randint(0,largeur-1),rd.randint(0,hauteur-1)
		x,y = x*pas,y*pas
		
	if ((x>= 0 and x < largeurCanvas) and (y >= 0 and y < hauteurCanvas) and carte[y//pas][x//pas] == eau):
		supprimerJoueur()
		x0,y0 = x,y
		placerJoueur()



#BOT----------------------------------------------------------------------------------------
nbBot = 5
probaMouv = 0.7

coordBot = []

def initBot():
	global coordBot
	xBot,yBot = rd.randint(0,largeur-1),rd.randint(0,hauteur-1)
	while carte[yBot][xBot] != eau:
		xBot,yBot = rd.randint(0,largeur-1),rd.randint(0,hauteur-1)
	coordBot += [(xBot*pas,yBot*pas)]

def placerBot(numBot,activite):
	xBot,yBot = coordBot[numBot]
	if activite :
		couleur = "yellow"
	else:
		couleur = "yellow3"
	can.create_rectangle(xBot,yBot,xBot+pas,yBot+pas,fill=couleur,tags="bot"+str(numBot))
	
def supprimerBot(numBot):
	can.delete(fen,"bot"+str(numBot))
	
def mouvementBot(numBot):
	global coordBot,score
	xBot,yBot = coordBot[numBot]
	if rd.random() < probaMouv:
		if obstacle((x0//pas,y0//pas),(xBot//pas,yBot//pas)):
			activite = False
			i,j = rd.choice([-pas,0,pas]),rd.choice([-pas,0,pas])
			while (xBot+i < 0 or xBot+i >= largeurCanvas) or (yBot+j < 0 or yBot+j >= hauteurCanvas) or carte[(yBot+j)//pas][(xBot+i)//pas] in [terre,plage]:
				i,j = rd.choice([-pas,0,pas]),rd.choice([-pas,0,pas])
			x,y = xBot+i,yBot+j
		else:
			activite = True
			score += 1
			dist = trouverDistance((x0,y0),(xBot,yBot))
			for i in [-pas,0,pas]:
				for j in [-pas,0,pas]:
					if (xBot+i >= 0 and xBot+i<largeurCanvas) and (yBot+j >= 0 and yBot+j < hauteurCanvas) and not(carte[(yBot+j)//pas][(xBot+i)//pas] in [terre,plage]) and trouverDistance((x0,y0),(xBot+i,yBot+j)) <= dist:
						x,y = xBot+i,yBot+j
						dist = trouverDistance((x0,y0),(x,y))
		supprimerBot(numBot)
		coordBot[numBot] = (x,y)
		placerBot(numBot,activite)



	
	
def gameOver():
	global coordBot
	if (x0,y0) in coordBot:
		time.sleep(0.5)
		fen.destroy()
		print("SCORE : " + str(score))
	
def main(event):
	mouvementJoueur(event)
	
	for i in range(nbBot):
		mouvementBot(i)
	
	scoring()
	gameOver()
	



	
	
for i in range(nbBot):
	initBot()
	
for i in range(nbBot):
	xBot,yBot = coordBot[i]
	activite = True
	if obstacle((x0//pas,y0//pas),(xBot//pas,yBot//pas)):
		activite = False
	placerBot(i,activite)

placerJoueur()






fen.bind("<Key>",main)

fen.mainloop()


