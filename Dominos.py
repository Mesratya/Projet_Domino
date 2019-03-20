import random

class domino:
    def __init__(self,vala,valb,posa =(None,None),posb =(None,None)):
        self.vala=vala
        self.valb=valb
        self.posa=posa # stocker ici la position des demi-dominos permettera à l'IHM d'afficher les dominos simplement en les parcourant dans l'objet plateau sans avoir à parcourir la grille grid
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
    def __init__(self,num,game,mode):
        self.num = num
        self.game = game
        self.etat_bloque = False # si la main ne peut definitivement plus jouer cette variable vaut true
        self.mode = mode # mode est la nature du joueur : human, IA (il peut y avoir plusieur type d'IA)

    def domino_jouable(self):
        '''Renvoie les dominos de la main qui sont posables sur le plateau'''
        dom_jouab = []
        extr_a = self.game.plateau.extr_a
        extr_b = self.game.plateau.extr_b
        legal_a = self.game.orientations_legales("a")
        legal_b = self.game.orientations_legales("b")
        for domino in self :
            if ((domino.vala == extr_a or domino.valb == extr_a) and legal_a != []) or ((domino.vala == extr_b or domino.valb == extr_b)  and legal_b != []) :
                dom_jouab.append(domino)

        return(dom_jouab)

    def domino_jouable_left_side(self):
        '''Renvoie les dominos de la main qui sont posables du coté a du plateau au sens des valeurs et de la place disponible'''
        dom_jouab_left_side = []
        extr_a = self.game.plateau.extr_a
        extr_b = self.game.plateau.extr_b
        legal_a = self.game.orientations_legales("a")
        legal_b = self.game.orientations_legales("b")
        for domino in self:

            if (domino.vala == extr_a or domino.valb == extr_a) and legal_a != [] and ((domino.vala != extr_b and domino.valb != extr_b) or legal_b == []) :
                dom_jouab_left_side.append(domino) # le domino n'est jouable que sur extr_a

        return (dom_jouab_left_side)

    def domino_jouable_right_side(self):
        '''Renvoie les dominos de la main qui sont posables du coté b au sens des valeurs et de la place disponible'''
        dom_jouab_right_side = []
        extr_a = self.game.plateau.extr_a
        extr_b = self.game.plateau.extr_b
        legal_a = self.game.orientations_legales("a")
        legal_b = self.game.orientations_legales("b")
        for domino in self:

            if (domino.vala == extr_b or domino.valb == extr_b) and legal_b != [] and ((domino.vala != extr_a and domino.valb != extr_a) or legal_a == []):
                dom_jouab_right_side.append(domino)  # le domino n'est jouable que sur extr_b

        return (dom_jouab_right_side)

    def max_domino(self):
        """Renvoie le plus grand domino de la main"""
        return(max(self))

    def pt_restant(self): # renvoie le nombre de point que totalise les dominos de la main, il s'agit de minimiser ce total
        pt_total = 0
        for domino in self :
            pt_total += domino.val_totale()
        return (pt_total)

    def cinq_meme_famille(self): # vérifie que la main ne contient pas 5 dominos de la même famille (possedant un nombre en commun)
        count_control = [0] * (self.game.pt_max + 1)
        for domino in self : # un domino appartient à deux famille si val_a et val_b sont différent, à une unique famille si val_a et val_b sont égaux
            if domino.vala == domino.valb :
                count_control[domino.vala] += 1
            else :
                count_control[domino.vala] += 1
                count_control[domino.valb] += 1
        for card_famille in count_control : # on controle le cardinal de chaque famille de points
            if card_famille > 5 :
                return(True)
        return(False)















