##################################################### B I B L I O T H E Q U E S ##################################################

import pyxel as p
import random as r
import time as t
from os import chdir
 
################################################ V A R I A B L E S    G L O B A L E S ###################################################

FRAME_REFRESH = 60 
x_grenouille = 10 #Position de départ de la grenouille en x
y_grenouille = 100 #Position de départ de la grenouille en y
Sur_le_nenuphar = False #Booléen pour savoir si la grenouille est sur un nénuphar ou pas
vitesse = 1 #Variable qui définit la vitesse à laquelle les nénuphars vont bouger
poids = 1 #Variable qui définit la vitesse à laquelle la grenouille va tomber
nenuphars = [] #Liste qui va contenir les coordonnées x et y de tous les nénuphars à l'écran
terre = [0, 175] #Coordonnées x et y de la terre, qui permet à la grenouille de ne pas tomber dans l'eau au lancement du jeu
HEIGHT = 200 #La fenetre fait 280 pixels de largeur et 200 pixels de hauteur
WIDTH = 280
largeur_g = 20 #Largeur de la grenouille
hauteur_g = 21 #Hauteur de la grenouille
largeur_n = 27 #Largeur des nénuphars
hauteur_n = 4 #Hauteur des nénuphars
vie = 3 #Nombre de vies de la grenouille
coeur = [[5,2],[17,2],[30,2]] #Liste qui va contenir les coordonnées x et y des coeurs à l'écran
En_saut = False #Booléen qui indique si la grenouille est en train de sauter ou pas
taille_saut = 5 #Nombre de pixels que la grenouille va sauter à chaque saut
vitesse_saut = 5 #Vitesse à laquelle la grenouille va sauter
eau_coordonée = [[0,58],[250,58]] #Coordonnées x et y de l'eau à l'écran
ciel_coordonée = [[0,0],[250,0]]
score1= 0 #Score intermédiaire qui permet de gérer l'ajout de points au score final en fonction du temps sur le nénuphar
score = 0 #Score final du joueur
piecepartie = 0 #le nombre de piece qu'on a : par defaut c'est 0 mais cette donné est mise a jour via la lecure de gichier plus tard
chapeau = False  #si un chapeau est equiper ou pas sur la grenouille
Choix_chapeau = 100  #Prendra une valeur plus tard de 0 à 7 en fonction de qu'elle chapeau est choisis (100 car pour l'istant aucun)
nenupharacceuil = [[20,50],[190,58],[200,170],[30,170]] #liste contenant les positions des graphismes de nenuphars au debut
nenupharacceuilfleur = [[45,98],[130,5],[230,90],[140,185]] #pareil qu'au dessus mais c'est ceux avec des fleurs
meilleurscore = 0 #Meilleur score enregistré
articles = [[50,40,50,0], [50,80,100,0],[50,120,200,0], [124,40,50,0], [200,40,50,0], [200,80,100,0],[200,120,200,0]]#une liste contenant chaque article avec leurs coordonnés x et y dans le shop, leurs prix et si ils sont déja acheté (1) ou pas (0)
p.init(WIDTH,HEIGHT) #Initialisation de la fenetre Pyxel de taille WIDTH x HEIGHT
p.load("images.pyxres", True, False, True, False) #Chargement du fichier contenant les images utilisées pour le jeu

########################################## F O N C T I O N S  G E N E R A L E S #########################################################

def update_acceuil():
    """
    entre : none
    permet d'acceder au jeu et au shop
    sortie : none
    """
    fichier()
    if p.btnp(p.KEY_Q):
        p.quit() #appuyer sur Q pour quitter le jeu
    if 169 >= p.mouse_x >= 110 and 128 >= p.mouse_y >= 100 and p.btnp(p.MOUSE_BUTTON_LEFT) :
        p.run(update, draw) #pouvoir cliquer sur le bouton play pour lancer une partie
    if 169 >= p.mouse_x >= 110 and 156 >= p.mouse_y >= 138 and p.btnp(p.MOUSE_BUTTON_LEFT):
        p.run(updateshop, drawshop)#pouvoir acceder au shop en cliquant dessus

def draw_acceuil():
    """
    entre : none
    dessine l'ecran d'acceuil avec grenouilles + nenuphars + boutons play et shop
    sortie : none
    """
    p.mouse(visible=True)
    draw_water_acceuil()  #le fond est de l'eau
    p.blt(110, 40,1,0,103, 65, 45,7)
    if 169 >= p.mouse_x >= 110 and 128 >= p.mouse_y >=100 :
        p.blt(110, 100,1,0,191, 59, 28) #dessine le bouton play qui change de couleur quand on passe la souris devant
    else :
        p.blt(110, 100,1,0,151, 59, 28)
    if 169 >= p.mouse_x >= 110 and 156 >= p.mouse_y >= 138 :
        p.blt(110, 130,1,80,191, 59, 28)#dessine le bouton shop qui change de couleur quand on passe la souris devant
    else :
        p.blt(110, 130,1,80,151, 59, 28)

    for nenuphar in nenupharacceuil : #dessine tous les grenouilles et nenuphars sur la page d'acceuil 
        if (nenuphar[0]+6) >= p.mouse_x >= (largeur_g) and (nenuphar[1]-hauteur_g+3) >= p.mouse_y >= (hauteur_g): #changer la forme des grenouilles en deplacant la souris
            p.blt(nenuphar[0],nenuphar[1],1 , 0, 0,  32 , 15, 12)
            p.blt(nenuphar[0]+6,nenuphar[1]-hauteur_g+3,0 ,0,22, 20, 26,12) #dessine la grenouille au position x et y
            p.blt(nenuphar[0]+9,nenuphar[1]-hauteur_g-4,0,32, 35, 16,9,0)
        else:
            p.blt(nenuphar[0],nenuphar[1],1 , 0, 0,  32 , 15, 12)
            p.blt(nenuphar[0]+6,nenuphar[1]-hauteur_g+3,0 ,0,0, largeur_g, hauteur_g, 12) #fenetre de base sans chercher les grenouilles
    
    for nenuphar in nenupharacceuilfleur :#dessine tous les nénuphars avec fleurs sur la page d'acceuil 
        p.blt(nenuphar[0],nenuphar[1],1 ,40, 0,  31 , 12, 12)

def updateshop():
    """
    entre : none
    permet d'acheter different chapeau et de les porter pendant la partie
    sortie : none
    """
    global piecepartie, chapeau, Choix_chapeau, articles
    if p.btnp(p.KEY_Q):
        p.quit() #appuyer sur Q pour quitter le jeu
    if 169>=p.mouse_x>=110 and 108>=p.mouse_y>=80 and p.btnp(p.MOUSE_BUTTON_LEFT):
        p.run(update, draw)#lancer une partie si on clique sur le bouton play
    if p.btnp(p.KEY_A):
        p.run(update_acceuil, draw_acceuil) #aller a l'acceuil si on appuie sur a
    for article in articles : 
        if article[0]+40>=p.mouse_x>=article[0] and article[1]+16>=p.mouse_y>=article[1] and p.btnp(p.MOUSE_BUTTON_LEFT) and piecepartie>=article[2] and article[3] ==0:
            piecepartie-=article[2]  #permet d'acheter un article dans le shop quand on clique dessus
            article[3] = 1  #change la valeur pour dire qu'on le possedent (l'artice)
    for i in range(len(articles)) :
        if articles[i][0]+40>=p.mouse_x>=articles[i][0] and articles[i][1]+16>=p.mouse_y>=articles[i][1] and p.btnp(p.MOUSE_BUTTON_LEFT) and articles[i][3] == 1:
            chapeau = True #permet de choisir et d'equiper un aricle
            Choix_chapeau = i #= le numero du chapeau equiper
    info[0]= piecepartie     #stoquent toutes les modifications dans la liste info pour les sauvegarder ensuite dans un fichier
    info[1]= articles[0][3]
    info[2]= articles[1][3]
    info[3]= articles[2][3]
    info[4]= articles[3][3]
    info[5]= articles[4][3]
    info[6]= articles[5][3]
    info[7]= articles[6][3]

    chdir("./")
    with open("piece.txt",'w') as file : #ouvre le fichier pour noter nos modifications et sauvegarder les informations d'une partie sur l'autre
        for ligne in info :
            file.write(str(ligne)) #ecris tout ce qui a dans info
            file.write("\n")     #separent les informations par un retour à la ligne
    file.close()

def drawshop():
    """
    entre : none
    dessine le shop avec chapeaux + prix + visuel grenouille avec les differents chapeaux  +  bouton play 
    sortie : none
    """
    global piecepartie, articles, Choix_chapeau
    p.mouse(visible=True) #permet d'afficher la souris 
    draw_water_acceuil() #cree le fond
    p.text(WIDTH-100, 5, f"pieces : {piecepartie}", 0) #affiche les informations du nombre de pieces
    p.text(80, 180, "Press A to go to the Home Page", 0) 
    p.blt(135,140,0 ,0,0, largeur_g, hauteur_g, 12) #dessine la grenouille de visualisation 
    if Choix_chapeau == 0 :
        p.blt(135,130,0 ,48,32,16,15,0) #dessine tout les chapeaux sur la grenouille si ils sont equiper (chapeaux allant de 0 a 7)
    elif Choix_chapeau == 1 :
        p.blt(135,135,0 ,32, 49,16,6,7)
    elif Choix_chapeau == 2 :
        p.blt(135,133,0 ,32,35,16,9,0)
    elif Choix_chapeau == 3 :
        p.blt(135,136,0 ,48,50,16,5,0)
    elif Choix_chapeau == 4 :
        p.blt(135,133,0 ,48,56,16,16,0)
    elif Choix_chapeau == 5 :
        p.blt(135,128,0 ,32,72,16,14,0)
    elif Choix_chapeau == 6 :
        p.blt(135,130,0 ,32,58,16,12,0)

    if 169>=p.mouse_x>=110 and 108>=p.mouse_y>=80 :
        p.blt(110, 80,1,0,191, 59, 28) #dessine le bouton play qui change de couleur quand on passe la souris devant
    else :
        p.blt(110, 80,1,0,151, 59, 28)

    for article in articles : #dessine le prix en dessous de chaque article en fonction du prix précisé
        p.blt(article[0],article[1],1 , 0, 0,  32 , 15, 12)
        if article[2] == 50 and article[3] == 0:
            p.blt(article[0],article[1]+20,0, 81,0,40,16,0)
        elif article[3] == 1 :
            p.blt(article[0],article[1]+20,0, 80,16,40,16)
        elif article[2] == 100 : 
            p.blt(article[0]-5,article[1]+20,0, 72,32,48,16,0)
        elif article[2] == 200 : 
            p.blt(article[0]-5,article[1]+20,0, 72,48,48,16,0)
    
    
    p.blt(articles[0][0]+8,articles[0][1]-5,0, 48,32,16,15,0) #dessine tout les articles a leurs coordonnées 
    p.blt(articles[3][0]+8,articles[3][1]+2,0, 48,50,16,5,0)
    p.blt(articles[4][0]+8,articles[4][1]-5,0, 48,56,16,16,0)
    p.blt(articles[1][0]+8,articles[1][1]+2,0, 32, 49,16,6,7)
    p.blt(articles[5][0]+8,articles[5][1]-5,0, 32,72,16,14,0)
    p.blt(articles[2][0]+8,articles[2][1],0, 32,35,16,9,0)
    p.blt(articles[6][0]+8,articles[6][1]-5,0, 32,58,16,12,0)


def update():
    """
    entre : none
    fait fonctionner le jeu avec les variables secondaires
    sortie : none
    """
    if p.btnp(p.KEY_Q):
        p.quit() #appuyer sur Q pour quitter le jeu
    grenouille_deplacement()
    grenouille_gravite()
    nenuphar_creations()
    nenuphars_deplacement()
    collisions_grenouille_nenuphars()
    mortgrenouille()
    acceleration()
    graphique()

def draw():
    """
    entre : none
    dessine l'ecran de jeu tout au long de la partie
    sortie : none
    """
    global x_grenouille, y_grenouille, nenuphars, terre, eau_coordonée, taille_saut, ciel_coordonée
    p.cls(12)#fond bleu
    p.mouse(visible=False)#la souris n'est plus visible
    for ciel in ciel_coordonée : #dessine le ciel et le fais bouger avec les coordonnées 
        p.blt(ciel[0],ciel[1],2,0,180, 250, 100, 10)
    p.text(WIDTH-50, 5, f"score : {score}", 6) #ecrit la variable score
    p.text(WIDTH-100, 5, f"pieces : {piecepartie}", 6)#ecrit la variable piece
    draw_water()#appelle la fonction pour dessiner l'eau
    for eau in eau_coordonée : #fait  bouger la terre au dessus de l'eau
        p.blt(eau[0],eau[1], 2, 0,0, 250,39,0)

    p.blt(terre[0], terre[1],2,0,0, 230, 25, 0)#dessine la terre pour le debut du jeu
    
    p.blt(120,2,0,128,0,23,8) #dessine la barre de chargement de saut vide
    if taille_saut <= 6 : #fait augmenter la taille de chargement en fonction de la taille du saut
        p.blt(120,2,0,128,0,23,8)
    elif taille_saut<= 30 :
        p.blt(120, 2, 0, 48,0,5,8)
    elif taille_saut<= 50 :
        p.blt(120, 2, 0, 48,0,10,8)
    elif taille_saut<= 75 :
        p.blt(120, 2, 0, 48,0,14,8)
    elif taille_saut<= 100 :
        p.blt(120, 2, 0, 48,0,17,8)
    else :
        p.blt(120, 2, 0, 48,0,23,8)

    for c in coeur : #dessine les coeurs correspondant u vies
        p.blt(c[0],c[1],1 , 0, 24,  9 , 8,7)

    for nenuphar in nenuphars : #dessine les nenuphars 
        p.blt(nenuphar[0],nenuphar[1],1 , 0, 0,  32 , 15, 12) #dessine les nenuphars au position x et y de chaque nenuphar
        if nenuphar[2] == 1 : #dessine la piéce si les nenuphares possédent des piéces
            p.blt(nenuphar[0]+8, nenuphar[1]-8, 0, 32,0,15,15,0)
    if Sur_le_nenuphar == True :#dessine la grenouille assise quand elle est sur le nenuphare
        p.blt(x_grenouille,y_grenouille,0 ,0,0, largeur_g, hauteur_g, 12) #dessine la grenouille au position x et y
        if chapeau == True : #affiche les chapeaux sur la grenouille en fonction de celui qui est equipé
            if Choix_chapeau == 0 :
                p.blt(x_grenouille,y_grenouille-10,0 ,48,32,16,15,0)
            elif Choix_chapeau == 1 :
                p.blt(x_grenouille,y_grenouille-5,0 ,32, 49,16,6,7)
            elif Choix_chapeau == 2 :
                p.blt(x_grenouille,y_grenouille-7,0 ,32,35,16,9,0)
            elif Choix_chapeau == 3 :
                p.blt(x_grenouille,y_grenouille-4,0 ,48,50,16,5,0)
            elif Choix_chapeau == 4 :
                p.blt(x_grenouille,y_grenouille-7,0 ,48,56,16,16,0)
            elif Choix_chapeau == 5 :
                p.blt(x_grenouille,y_grenouille-12,0 ,32,72,16,14,0)
            elif Choix_chapeau == 6 :
                p.blt(x_grenouille,y_grenouille-10,0 ,32,58,16,12,0)

    else :
        p.blt(x_grenouille,y_grenouille,0 ,0,22, 20, 26,12) #dessine la grenouille debout au position x et y
        if chapeau == True :#affiche les chapeaux sur la grenouille en fonction de celui qui est equipé
            if Choix_chapeau == 0 :
                p.blt(x_grenouille+2,y_grenouille-8,0 ,48,32,16,15,0)
            elif Choix_chapeau == 1 :
                p.blt(x_grenouille+2,y_grenouille-3,0 ,32, 49,16,6,7)
            elif Choix_chapeau == 2 :
                p.blt(x_grenouille+2,y_grenouille-5,0 ,32,35,16,9,0)
            elif Choix_chapeau == 3 :
                p.blt(x_grenouille+2,y_grenouille-2,0 ,48,50,16,5,0)
            elif Choix_chapeau == 4 :
                p.blt(x_grenouille+2,y_grenouille-5,0 ,48,56,16,16,0)
            elif Choix_chapeau == 5 :
                p.blt(x_grenouille+2,y_grenouille-10,0 ,32,72,16,14,0)
            elif Choix_chapeau == 6 :
                p.blt(x_grenouille+2,y_grenouille-8,0 ,32,58,16,12,0)


def updatefin():
    """
    entre : none
    remet a jour toutes les variables et permet de refaire touner le jeu (touche = espace) ou d'afficher l'ecran d'acceuil 
    (touche = A)
    sortie : none
    """
    global x_grenouille, y_grenouille, Sur_le_nenuphar, vitesse, poids, nenuphars, terre, vie, coeur, En_saut, taille_saut
    global  vitesse_saut, eau_coordonée, score, score1
    if p.btnp(p.KEY_SPACE):#remet d'abord toutes les variables comme a l'initial
        x_grenouille = 10 #Position de départ de la grenouille en x
        y_grenouille = 100 #Position de départ de la grenouille en y
        Sur_le_nenuphar = False #Booléen pour savoir si la grenouille est sur un nénuphar ou pas
        vitesse = 1 #Variable qui définit la vitesse à laquelle les nénuphars vont bouger
        poids = 1 #Variable qui définit la vitesse à laquelle la grenouille va tomber
        nenuphars = [] #Liste qui va contenir les coordonnées x et y de tous les nénuphars à l'écran
        terre = [0, 175] #Coordonnées x et y de la terre, qui permet à la grenouille de ne pas tomber dans l'eau au lancement du jeu
        vie = 3 #Nombre de vies de la grenouille
        coeur = [[5,2],[17,2],[30,2]] #Liste qui va contenir les coordonnées x et y des coeurs à l'écran
        En_saut = False #Booléen qui indique si la grenouille est en train de sauter ou pas
        taille_saut = 5 #Nombre de pixels que la grenouille va sauter à chaque saut
        vitesse_saut = 5 #Vitesse à laquelle la grenouille va sauter
        eau_coordonée = [[0,58],[250,58]] #Coordonnées x et y de l'eau à l'écran
        score1= 0 #Score intermédiaire qui permet de gérer l'ajout de points au score final en fonction du temps sur le nénuphar
        score = 0 #Score final du joueur
        p.run(update, draw)#relance une partie
    if p.btnp(p.KEY_A):
        p.run(update_acceuil, draw_acceuil)#retourne a l'acceuil

def drawfin ():
    """
    entre : none
    dessine la page de fin (game over + grenouilles + nenuphars + piece + score + meilleur score)
    sortie : none
    """
    p.cls(5)#met le fond en bleu
    p.blt(110, 84,1,0,41, 61, 40,7)#dessine le game over
    p.text(WIDTH-50, 5, f"score : {score}", 6) #ecrit le score
    p.text(4, 5, f"meilleur score : {meilleurscore}", 6)  #ecrit le meilleur score  
    p.text(WIDTH-110, 5, f"pieces : {piecepartie}", 6)#ecrit les pieces
    p.text(90, 144, "Press space to play again", 6) #affiches les informations pour les touches 
    p.text(80, 154, "Press A to go to the Home Page", 6)
    for nenuphar in nenupharacceuil : #places les nenuphars pour le design
        p.blt(nenuphar[0],nenuphar[1],1 , 0, 0,  32 , 15, 12)
    
    for nenuphar in nenupharacceuilfleur :  #places les nenuphars avec des fleurs pour le design
        p.blt(nenuphar[0],nenuphar[1],1 ,40, 0,  31 , 12, 12)

################################ F O N C T I O N S   S E C O N D A I R E S #########################################################

def draw_water_acceuil():
    """
    entre : none
    bruit de perlin pour l'acceuil (rendu plus realiste et bouge moins vite que sur le jeu)
    sortie : none
    """
    for y in range(HEIGHT): 
        for x in range(WIDTH): #on fait passer chacun des pyxels de la zone dans cette boucle
            n = p.noise(x / 10 , y / 10 , p.frame_count / 80)# renvois le nombre de bruit de perlin compris entre -1 et 1  (une sorte de synthese des pyxels environants)
            if n > 0.4: # on adapte donc la couleur du pyxel en fonction de ses alentours pour un rendu plus realiste
                col = 7
            elif n > 0:
                col = 6
            elif n > -0.4:
                col = 12
            else:
                col = 5 
            p.pset(x, y, col) # on applique la nouvelle couleur au pyxel

def draw_water():
    """
    entre : none
    bruit de perlin pour le jeu (rendu plus realiste et bouge plus vite que l'acceuil)
    sortie : none
    """
    for y in range(83,200):
        for x in range(WIDTH): #on fait passer chacun des pyxels de la zone dans cette boucle
            n = p.noise(x / 10 , y / 10 , p.frame_count / 80)# renvois le nombre de bruit de perlin compris entre -1 et 1  (une sorte de synthese des pyxels environants)
            if n > 0.4 : # on adapte donc la couleur du pyxel en fonction de ses alentours pour un rendu plus realiste
                col = 7
            elif n > 0 :
                col = 6
            elif n > -0.4 :
                col = 12
            else:
                col = 5 
            p.pset(x, y, col)  # on applique la nouvelle couleur au pyxel

def grenouille_deplacement ():
    """
    entre : none
    Fonction qui gère tout les deplacements de la grenouille : son deplacement a gauche et a droite(avec les fleches),
    et le saut sur la touche espace (plus on apruit longtemps dessus plus elle saute haut)
    sortie : none
    """
    global x_grenouille, y_grenouille, Sur_le_nenuphar, En_saut, taille_saut, vitesse_saut, score1, vitesse, piecepartie, nenuphars
    #deplacement sur la gauche et la droite 
    if p.btn(p.KEY_LEFT) and x_grenouille>0 :
        x_grenouille -= vitesse*2 #la grenouille ce deplace a gauche 
    elif p.btn(p.KEY_RIGHT) and x_grenouille+10<280 :
        x_grenouille += vitesse*2 #la grenouille ce deplace a droite   
    
    ############saut avec la barre espace 
    if y_grenouille >= 50 and Sur_le_nenuphar == True :
        if p.btn(p.KEY_SPACE) and taille_saut <= 120 :
            for i in range(120):
                taille_saut+=0.1#permet de regler la taille du saut en augmentant un variable le plus longtemps tu appuis sur espace
    if p.btn(p.KEY_SPACE) == False : 
        En_saut = True #permet de sauter ensuite


    if En_saut == True and taille_saut>= 0:
        y_grenouille -= vitesse_saut #fait sauter la grenouille en reduisant ses coordonées y par la vitesse
        taille_saut -= vitesse_saut #reduit la variable de taille saut pour stopper le saut quand elle arive en haut 
    else :
        En_saut = False

def grenouille_gravite():
    """
    entre : none
    gravite sur la grenouille : elle se deplace vers le bas quand elle n'est pas sur un nenuphar
    sortie : none
    """
    global Sur_le_nenuphar, x_grenouille, vitesse, poids, y_grenouille
    if Sur_le_nenuphar == True : #regler a true lors d'une collisons avec un nenuphar
        x_grenouille -= vitesse  #la grenouille se deplace alors vers la gauche a la même vitesse que le nenuphar (=reste sur le nenuphar)
        y_grenouille == y_grenouille
    else : 
        y_grenouille += poids #la grenouille ne se deplace plus vers la gauche mais elle tombe de son poid 

def nenuphar_creations():
    """
    entre : none
    Fonction s'occupant de la generation aleatoire a une frequence donnée des nenuphars
    sortie : none
    """
    global nenuphars, FRAME_REFRESH
    if p.frame_count % FRAME_REFRESH == 0 : #Pour faire apparaitre un nenuphare (valeur reglable pour en faire apparaitre moins (=frame_refresh plus grand) ou plus (=frame_refresh plus petit))
        nenuphars.append([279, r.randint(120, 195), r.randint(1,2), 1]) #apparition aleatoire entre 120 et 195 (presque le bas de la page pour eviter qu'ils sortent)

def nenuphars_deplacement():
    """
    entre : none
    fonction qui deplace tous les nenuphars vers la gauche en fonction de la vitesse "vitesse" : plus le nombre est haut
    plus la vitesse est rapide (augmente grace a fonction acceleration)
    sortie : none
    """
    global nenuphars, vitesse, terre
    nenuphar2 = []
    for nenuphar in nenuphars :
        nenuphar[0] -= vitesse #deplace tout les nenuphar vers la gauche a la vitesse "vitesse"
        if nenuphar[0] + largeur_n - 3 <= 0 :
           nenuphar2.append(nenuphar) #supprime les nenuphars qui sortent du cadre 
    for nenu2 in nenuphar2 :#pour retirer joliment des élements à une liste sans que ca bloque (previens certains bug)
        if nenu2 in nenuphars:
            nenuphars.remove(nenu2)
    if terre[0]>= -250 : #deplace la terre au debut 
        terre[0] -= vitesse
    
def collisions_grenouille_nenuphars():
    """
    entre : none
    Regarde si la grenouille arrive a se poser sur le dessus d'un nenuphar et si oui passe la variable "Sur_le_nenuphar" a "true"
    elle permet donc de detecter les collisions avec les nenuphars
    sortie : none
    """
    global x_grenouille, y_grenouille, nenuphars, Sur_le_nenuphar, terre, largeur_n, largeur_g, hauteur_g, hauteur_n, score, piecepartie, En_saut, score1
    for i in range(len(nenuphars)) :#test les collisons avec tout les nenuphars
        if ((nenuphars[i][0] <= x_grenouille <= nenuphars[i][0] + largeur_n or nenuphars[i][0] <= x_grenouille + largeur_g <= nenuphars[i][0] + largeur_n) and nenuphars[i][1] +poids >= y_grenouille + hauteur_g>= nenuphars[i][1] -poids ) :  #lles collisosns avec les nenphars
            if nenuphars[i][3] == 1:#augmente le score quand on arrive sur un nenuphar
                score1 += 1
                nenuphars[i][3] = 0 #evite que le score s'augmente plusieurs fois
            Sur_le_nenuphar = True #chage la variable pour gerer la gravite dans la fonctions grenouille_gravite
            #la grenouille se deplace alors vers la gauche a la même vitesse que le nenuphar (=reste sur le nenuphar)
            y_grenouille = nenuphars[i][1]-hauteur_g #place la grenouille sur le nenuphar
            if nenuphars[i][2] == 1 :#augmente les piéces si le nenuphar posséde des piéces 
                piecepartie += 1
                nenuphars[i][2] = 2#evite que les pieces s'augmente plusieurs fois
            break #arrete le programme (evite une boucle continue)
        if x_grenouille <= (terre[0]+250) and y_grenouille+12 >= terre[1] : #collisions avec la terre 
            Sur_le_nenuphar = True

        else : 
            Sur_le_nenuphar = False 

def acceleration():
    """
    entre : none
    permet l'acceleration au fur et a mesure du jeu au niveau de la vitesse de la gravite et de la generation de nenuphars
    sortie : none
    """
    global vitesse, score, vitesse_saut, poids, score1
    if score < score1 : # quand le score augmente on augmente la vitesse de deplacement et de saut de la genouille ainsi que la gravite 
        score = score1
        vitesse += 0.05
        vitesse_saut += 1
        poids += 0.05

def graphique():
    """
    entre : none
    permet de faire bouger la terre
    sortie : none
    """
    global eau_coordonée, ciel_coordonée
    for eau in eau_coordonée : #fait bouger l'eau(la terre au dessus) au coordoné qu'elles sont placés 
        eau[0] -= vitesse #en fonction de la vitesse pour aller aussi vite que les neuphars 
        if eau[0] <= -250 :
            eau_coordonée.remove(eau) #retire de la liste quand l'eau sors de l'ecran pour eviter de trop charger la liste 
    if eau_coordonée[len(eau_coordonée)-1][0] <= 30 :
        eau_coordonée.append([250,58]) #crée des nouveaux terre pour les faires passer = continue de rechrger pour avoir un deffilement continue 
    
    for ciel in ciel_coordonée :#fait bouger le ciel au coordoné qu'elles sont placés 
        a = ciel[0]
        a -= 0.2 #le ciel bouge tout doucement = dans une variable a part car nous avons besoins d'un float
        ciel[0] = a
        if ciel[0] <= -250 :
            ciel_coordonée.remove(ciel)#retire de la liste quand le ciel sors de l'ecran pour eviter de trop charger la liste 
    if ciel_coordonée[len(ciel_coordonée)-1][0] <= 30 :
        ciel_coordonée.append([250,0])#crée des nouveaux ciel pour les faires passer = continue de rechrger pour avoir un deffilement continue 

def fichier():
    """
    entre : none
    releve en debut de partie les pieces accumulees et les chapeu deja obtenus
    sortie : none
    """
    global articles, info, piecepartie
    chdir("./")
    fichier = open("piece.txt",'r') #on ouvre le fichier pour relever les pieces et chapeau gagné lors des utilisation precedentes
    donne = fichier.readlines()
    fichier.close()
    info = []
    for element in donne : # on change du texte en nombre
        info.append(int(element))

    piecepartie = info[0] #on note toute les info dans les variable correspondantes
    articles[0][3] = info[1]
    articles[1][3] = info[2]
    articles[2][3] = info[3]
    articles[3][3] = info[4]
    articles[4][3] = info[5]
    articles[5][3] = info[6]
    articles[6][3] = info[7]
    
def mortgrenouille ():
    """ 
    entre : none
    A la mort de la grenouille cela retire un coeur et de reinitialise le jeu et apres trois morts il note le score et 
    remplce si necessaire le meilleur score de plus elle met a jour les piece gagnees et les chapeaux achetes 
    sortie : none
    """
    global vie, hauteur_g, largeur_g,terre, x_grenouille, y_grenouille, coeur, nenuphars, meilleurscore, piecepartie
    if y_grenouille + hauteur_g  >= HEIGHT or x_grenouille + largeur_g -1 >= WIDTH or x_grenouille + 1 <= 0 : # detecte les collisions avec le tour de l'ecran qui declanche la mort de la grenouille
        vie -=1
        d = len(coeur)
        del coeur[d-1] # supprime le dernier coeur
        p.play(0,4) # joue la musique de mort
        if vie <= 0 : #detecte la fin de la partie
            chdir("./")
            fichier = open("meilleurscore.txt",'r')
            meilleurscore = fichier.readlines()
            a = meilleurscore[0]
            a = int(a)
            fichier.close() # recupere le meilleur score
            if score > a : # compare le score et meilleur score, il change le meilleur score si besoin
                chdir("./")
                with open("meilleurscore.txt",'w') as file :
                    text = str(score)
                    file.write(text)    
                file.close()
                meilleurscore = score # pour afficher le meilleur sorce actuel
            else :
                meilleurscore = a  # pour afficher le meilleur sorce actuel
            p.run(updatefin,drawfin) # on lance la page de fin 
        else : # si les vie ne sont pas ecoulees on reinitialise le jeu pour la vie suivante
            terre = [0, 175] 
            x_grenouille = 10
            y_grenouille = 100
            nenuphar2 = []
            for nenuphar in nenuphars : # on supprime des nenuphars qui sont dans le meme espace que le cadre de depart
                if nenuphar[0] <= 250:
                    nenuphar2.append(nenuphar)
            for nenu2 in nenuphar2 :
                if nenu2 in nenuphars:
                    nenuphars.remove(nenu2)
        
        info[0]= piecepartie #met a jour les donnees sur les pieces et les chapeaux
        info[1]= articles[0][3]
        info[2]= articles[1][3]
        info[3]= articles[2][3]
        info[4]= articles[3][3]
        info[5]= articles[4][3]
        info[6]= articles[5][3]
        info[7]= articles[6][3]

        chdir("./") # met a jour le fichier des pieces et chapeaux pour actualiser les achats et les gains
        with open("piece.txt",'w') as file :
            for ligne in info :
                file.write(str(ligne))
                file.write("\n")    
        file.close()
            
        t.sleep(1) # attend une seconde avant de recommencer

################################################P R O G R A M M E  G E N E R A L ################################################

p.run(update_acceuil, draw_acceuil) # lance l'ecran d'acceuil
