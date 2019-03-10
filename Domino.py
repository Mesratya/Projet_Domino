import random

class domino:
    def __init__(self,vala,valb,posa=None,posb=None):
        self.vala=vala
        self.valb=valb
        self.posa=posa
        self.posb=posb

    def __repr__(self):
        return ("[{0}|{1}]".format(self.vala,self.valb))


    def val_totale(self):
        return(self.vala + self.valb)

    def side_val(self,side):
        if side == 0 :
            return(self.val_a)
        else :
            return(self.val_b)

    def __gt__(self, other):
        if self.val_totale() > other.val_totale() :
            return(True)
        else : return (False)

    def inverted(self):
        """return the inverted domino"""
        return(domino(self.valb,self.vala))


class talon(list):
    def __init__(self,pt_max):
        for i in range(pt_max,-1,-1):
            for j in range(i,-1,-1):
                self.append( domino(i,j) )

    def tirer(self):
        domino = self.pop(random.randint(0,len(self)-1))
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

    def max_domino(self):
        """Renvoie le plus grand domino de la main"""
        return(max(self))



class plateau(list):
    """Pour l'instant les domino sont posés en ligne sans considerer les virages"""

    def __init__(self,game):
        self.grid = [[(None,None)]*game.size]*game.size # cette grille permettera le stockage de la position 2D des dominos
        self.extr_a = None
        self.extr_b = None
        self.game = game

    def poser(self,domino,extr = None):
        """ajoute le domino au plateau à l'extremité souhaité"""

        if game.premiere_pose :
            self.append(domino)
            self.extr_a = domino.vala
            self.extr_b = domino.valb

        if extr == self.extr_a :
            if domino.valb == self.extr_a :
                self.insert(0,domino)
                self.extr_a = domino.vala
            else :
                self.insert(0,domino.inverted())
                self.extr_a = domino.valb

        if extr == self.extr_b :
            if domino.vala == self.extr_b :
                self.append(domino)
                self.extr_b = domino.valb
            else :
                self.append(domino.inverted())
                self.extr_b = domino.vala



class game:

    def __init__(self,pt_max = 6,nb_joueur = 2,nb_dominoparjoueur = 7):
        '''pt_max est le nombre de points maximal sur un domino'''
        self.nb_joueur = nb_joueur
        self.pt_max = pt_max
        self.nb_domino = (pt_max+1)*(pt_max+2)/2
        self.nb_dominoparjoueur=nb_dominoparjoueur
        self.size = int(self.nb_domino * 2) # On s'assure que tous les dominos peuvent être alignés sur le plateau
        self.plateau =  plateau(self)
        self.talon = talon(self.pt_max)
        self.Joueurs = []
        for i in range(self.nb_joueur): # création des mains
            self.Joueurs.append(hand(i))
        self.distribuer()




    def distribuer(self):

        for hand in self.Joueurs:
            for i in range (self.nb_dominoparjoueur):
                hand.append(self.talon.tirer())
        self.rang_premier_joueur = 0  # position dans la liste Joueurs du joueur ayant le plus fort domino au début du jeu
        for i in range(len(self.Joueurs)):
            if self.Joueurs[i].max_domino() > self.Joueurs[self.rang_premier_joueur].max_domino():
                self.rang_premier_joueur = i
        premier_joueur = self.Joueurs.pop(self.rang_premier_joueur)
        self.Joueurs.insert(0,premier_joueur)


    def jouer_tour(self,joueur): # le joueur joue son tour
        if self.premiere_pose :
            max_domino = joueur.max_domino()
            joueur.remove(max_domino)
            self.plateau.poser(max_domino)
            self.premiere_pose = False


    def Partie(self):
        """La partie est gérée dans cette méthode jusqu'a la fin du jeu"""
        self.Jeu_en_cours = True
        self.premiere_pose = True

        while self.Jeu_en_cours :
            for joueur in self.Joueurs :
                if self.Jeu_en_cours :
                    self.jouer_tour(joueur)

        self.fin_de_partie()

    def fin_de_partie(self):
        pass



if __name__ == "__main__":
    Game = game()





