# Memory pour 2 joueurs humains

from tkinter import *
from random import randint, shuffle
import time
from timeit import default_timer


# ----- variables globales ---------------------------------------------------
images = []         # contient les liens aux fichiers images
cartes = []         # contient le lien vers l'image des différentes cartes
cartes_jouees = []  # contient les cartes jouées
nb_lignes, nb_colonnes = 5, 4
joueur_actuel = 0
score = [0,0]
fini = False
peut_jouer = True

# ------ Chrono --------------------------------------------------------------
def updateTime():
    now = default_timer() - start
    minutes, seconds = divmod(now, 60)
    hours, minutes = divmod(minutes, 60)
    str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
    canvas.itemconfigure(text_clock, text=str_time)
    fenetre.after(1000, updateTime)

# ----- Images ----------------------------------------------------------------
def charger_images():
    del images[:]   # vide la liste
    nb_images = 21  # l'image no 0 est le dos des cartes
    choixCartes = []
    choixCartes.append(0)
    i=0
    while i < nb_images-1:           # tirage au sort des cartes à utiliser
        x = randint(1, nb_images-1)
        if x not in choixCartes:
            choixCartes.append(x)
            i += 1          
    for i in range(nb_images):           # importation des images
        nom = 'carte-' + str(choixCartes[i]) + '.gif'
        image = PhotoImage(file = nom)
        images.append(image)


# ----- Melange des cartes -----------------------------------------------------
def melanger_cartes():
    global nb_colonnes, nb_lignes, cartes
    nb_cartes = nb_colonnes * nb_lignes
    cartes=list(range(1,nb_cartes//2+1))*2
    shuffle(cartes)


# ----- Retourne les deux cartes à la fin de la sélection ----------------------
def gerer_tirage():
    global cartes_jouees, joueur_actuel, score, fini, peut_jouer

    if cartes[cartes_jouees[0]-1] == cartes[cartes_jouees[1]-1]:
        # Les cartes sont identiques
        canvas.delete(cartes_jouees[0])
        canvas.delete(cartes_jouees[1])
        score[joueur_actuel] += 1
    else:
        # Les cartes sont différentes
        canvas.itemconfig(cartes_jouees[0], image=images[0])
        canvas.itemconfig(cartes_jouees[1], image=images[0])
        joueur_actuel = (joueur_actuel + 1) % 2

    cartes_jouees = []
    text1 = 'Joueur 1 : ' + str(score[0] * 2)
    text2 = 'Joueur 2 : ' + str(score[1] * 2)
    points_joueur1.config(text=text1)
    points_joueur2.config(text=text2)
    peut_jouer = True

    if joueur_actuel == 0:
        points_joueur1.config(bg='orange')
        points_joueur2.config(bg='white')
    else:
        points_joueur2.config(bg='orange')
        points_joueur1.config(bg='white')

    if score[0] + score[1] == (nb_colonnes * nb_lignes) // 2:
        fini = True
        if score[0] > score[1]:
            texte = "Le joueur 1 a gagné !"
        elif score[0] < score[1]:
            texte = "Le joueur 2 a gagné !"
        else:
            texte = "Egalité !"

        canvas.create_rectangle(0, 0, (110 * nb_colonnes) + 20, (110 * nb_lignes) + 20, fill='white')
        canvas.create_text((55 * nb_colonnes) + 10, (55 * nb_lignes) + 10, text=texte, font='Calibri 24', fill='black')

            
# ----- Retourne la carte sélectionnée -----------------------------------------
def cliquer_carte(event):
    global fini, plateau, cartes_jouees, peut_jouer
    if len(cartes_jouees) < 2:
        carteSel = canvas.find_closest(event.x, event.y)
        carteID = carteSel[0]
        if fini:
            fini = False
            reinit()
        else:
            canvas.itemconfig(carteID, image = images[cartes[carteID-1]]) # montre la carte
            if len(cartes_jouees) == 0:
                cartes_jouees.append(carteID)    # enregistre la carte jouée
            elif carteID != cartes_jouees[0]:    # ne pas cliquer 2x sur la même carte !
                cartes_jouees.append(carteID)
    if peut_jouer and len(cartes_jouees) == 2:
        peut_jouer = False                  # désactive l'effet du clic de la souris
        plateau.after(1500,gerer_tirage)    # patiente 1,5 secondes avant de continuer

            
# -----  Change la taille du plateau de jeu  -------------------------------------                

def jeu5x4():
    global nb_colonnes
    nb_colonnes = 4
    reinit()

def jeu5x6():
    global nb_colonnes
    nb_colonnes = 6
    reinit()

def jeu5x8():
    global nb_colonnes
    nb_colonnes = 8
    reinit()  
# ----- création des menus et sous-menus ------------------------------------------
def creer_menus(fen):
    top = Menu(fen)
    fen.config(menu=top)

    jeu = Menu(top, tearoff=False)
    top.add_cascade(label='Jeu', menu=jeu)


    jeu.add_command(label='Quitter', command=fen.destroy)

    
# ----- Création du canvas --------------------------------------------------------
def creer_canevas(fen, col, lig):
    return Canvas(fen, width=(110*col)+10, height=(110*lig)+10, bg='white')


# ----- Modifier le canvas --------------------------------------------------------
# Redémarre une partie et change éventuellement la difficulté
def reinit():
    global canvas, joueur_actuel, score, nb_lignes, nb_colonnes
    joueur_actuel = 0
    score =[0,0]
    del cartes[:]
    del cartes_jouees[:]
    canvas.destroy()
    canvas = creer_canevas(plateau, nb_colonnes, nb_lignes)
    canvas.pack(side = TOP, padx = 5, pady = 5)
    canvas.bind("<Button-1>", cliquer_carte)    # permet le clic sur les cartes
    melanger_cartes()
    for i in range(nb_colonnes):                # dessin des cartes retournées
        for j in range(nb_lignes):
            canvas.create_image((110*i)+60, (110*j)+60, image=images[0])
    text1 = 'Joueur 1 : ' + str(score[0]*2)
    text2 = 'Joueur 2 : ' + str(score[1]*2)
    points_joueur1.config(text = text1, bg = 'orange')
    points_joueur2.config(text = text2, bg = 'white')


# ----- Programme principal ----------------------------------------------------
fenetre = Tk()
fenetre.title("Memory Sohane Yanis")
creer_menus(fenetre)
# création du canvas dont la taille dépend du nombre de cartes
plateau = Frame(fenetre)
plateau.pack()
canvas=creer_canevas(plateau, nb_colonnes, nb_lignes)
canvas.pack(side = TOP, padx = 2, pady = 2)

start = default_timer()
text_clock = canvas.create_text(675,635)

updateTime()

charger_images()
melanger_cartes()
for i in range(nb_colonnes):                # dessin des cartes retournées
    for j in range(nb_lignes):
        canvas.create_image((110*i)+60, (110*j)+60, image = images[0])
canvas.bind("<Button-1>", cliquer_carte)    # permet le clic sur les cartes

fenetre.mainloop()

    
