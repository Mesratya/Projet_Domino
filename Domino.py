import random

class domino:
    def __init__(self,vala,valb,posa=None,posb=None):
        self.vala=vala
        self.valb=valb
        self.posa=posa
        self.posb=posb


    def val_totale(self):
        return(self.vala + self.valb)

    def side_val(self,side):
        if side == 0 :
            return(self.val_a)
        else :
            return(self.val_b)


class talon(list):
    def __init(self,game):
        for i in range(game.pt_max,-1,-1):
            for j in range(i,-1,-1):
                talon.append(domino(i,j))

    def tirer(self):
        domino = self.pop(random.randint(len(self)))
        return(domino)


class hand(list):
    def __init__(self,num):
        self.num = num


    def domino_jouable(self,extr_a,extr_b):
        '''Renvoie les dominos de la main qui sont posables sur le plateau'''
        dom_jouab = []
        for domino in self :
            if domino.vala == extr_a or domino.valb == extr_a or domino.vala == extr_b or domino.valb == extr_b :
                dom_jouab.append(domino)
        return(domino)





class game:

    def __init__(self,nb_domino,nb_joueur,nb_dominoparjoueur):
        self.nb_joueur = nb_joueur
        self.nb_domino = nb_domino
        self.nb_dominoparjoueur=nb_dominoparjoueur
        self.pt_max = (nb_domino+1)*(nb_domino+2)/2
        self.size = nb_domino/2
        self.plateau =  [[(None,None)]*self.size]*self.size
        self.talon = talon(self)
        self.Joueurs = []
        for i in range(self.nb_joueur):
            self.Joueurs.append(hand(i))
        self.distribuer()


    def distribuer(self):
        for hand in self.Joueurs:
            for i in range (self.nb_dominoparjoueur):
                hand.append(self.talon.tirer())

    def tour(self):
        # verifier si la partie est fini
        # si oui appeler fin de partie
        # sinon pour chaque joueur
        










