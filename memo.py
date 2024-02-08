from tkinter import *
from random import *
import time
from tkinter.font import Font
from timeit import default_timer

def rect():
    Mafenetre.destroy()

def updateTime():
    now = default_timer() - start
    minutes, seconds = divmod(now, 60)
    hours, minutes = divmod(minutes, 60)
    str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
    Canevas.itemconfigure(text_clock, text=str_time)
    Mafenetre.after(1000, updateTime)

def card_clicked(card_id):
    global card_list
    
    for card in card_list:
        if card[1] == card_id:
            Canevas.itemconfigure(card[1], image="blanc.gif")
            
            Canevas.delete(card[1])
            card_list.remove(card)
            break

def return_cards():
    global card_list
    for i, card in enumerate(card_list):
        Canevas.itemconfigure(card[1], image=card[0])

def remove_cards():
    global card_list
    same_cards = []
    for i, card in enumerate(card_list):
        for j, other_card in enumerate(card_list):
            if i != j and card[0] == other_card[0]:
                same_cards.append(card)
                same_cards.append(other_card)
                break
                
    for card in same_cards:
        Canevas.delete(card[1])
        card_list.remove(card)

Couleur=["black","red","blue"]

########################################################

Mafenetre = Tk()
Mafenetre.title("Le jeu du Memory")
Canevas = Canvas(Mafenetre, width=700, height=640, bg='white')

cards = ["carte-{}.gif".format(i) for i in range(21)]
shuffle(cards)

card_list = []

x = 100
y = 100

for i, card in enumerate(cards[:12]):
    fichier = PhotoImage(file=card)
    card_id = Canevas.create_image(x, y, image=fichier)
    card_list.append((fichier, card_id))
    Canevas.tag_bind(card_id, "<Button-1>", lambda event, card_id=card_id: card_clicked(card_id))
    
    if (i+1) % 3 == 0:
        x = 100
        y += 150
    else:
        x += 150


Canevas.create_rectangle(500,0,500,650,fill='red')

bouton = Button(Mafenetre, text="Quitter",height= 2, width=7,font=("Calibri",18,"bold"), command=rect)
bouton.place(x=550,y=500)

Caligraphie = Font(family='bold' 'Calibri', size=40)
Canevas.create_text(600,70,text="Score :",fill="black",font=Caligraphie)

start = default_timer()
text_clock = Canevas.create_text(675,635)

updateTime()

Canevas.pack()
font = Font(family='Liberation Serif', size=200) 

Mafenetre.mainloop()