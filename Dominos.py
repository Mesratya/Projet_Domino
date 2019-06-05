import random

"""
[Module secondaire]
Ce module est destiné à la définition des classes Domino, Hand et Talon car ces classes sont taille raisonable
"""

class Domino:
    """
    La classe domino modelise un domino par ses valeurs et la position des demi-dominos
    Initialement les dominos ne sont pas posé sur le plateau donc leurs positions sont à None
    On considère qu'un domino possède deux parties chacune ayant une valeur et une position
    Les lettres a et b distinguent les deux demi-dominos.

    """
    def __init__(self,vala,valb,posa =(None,None),posb =(None,None),couleur = None):
        self.vala=vala
        self.valb=valb
        self.posa=posa # stocker ici la position des demi-dominos permettera à l'IHM d'afficher les dominos simplement en les parcourant dans l'objet plateau sans avoir à parcourir la grille grid
        self.posb=posb
        self.couleur = couleur


    def __repr__(self):
        """ La repésentation d'un domino sous forme de chaine de caractère permet de jouer dans un terminal"""
        return ("[{0}|{1}]".format(self.vala,self.valb))


    def val_totale(self):
        """val_totale est la somme des points des deux parties d'un domino c'est
            c'est la valeur d'un domino
        """
        return(self.vala + self.valb)


    def __gt__(self, other):
        """On surcharge la méthode de comparaison en utilisant la valeur totale des dominos comme critère.
        Ainsi on pourra trier facilement des listes de dominos. Cela permet aussi d'appliquer la méthode max à une liste de domino
        et obtenir le domino de poids fort (cf. comportement de l'IA_max qui pose le plus grand domino)
        """
        if self.val_totale() > other.val_totale() :
            return(True)
        else : return (False)

    def inverser(self):
        """return un domino inversé"""
        return(Domino(self.valb,self.vala))


class Talon(list):
    """
    La classe Talon modélise le talon contenant tous les dominos au début d'une partie
    """
    def __init__(self,pt_max):
        """
        Le constructeur init remplit le talon en créant les dominos necessaires à la parti.
        La connaissance du nombre de points maximal (6 pour un jeu double-six) suffit à construire tout les dominos
        :param pt_max: nombre de points maximal sur un domino
        """
        for i in range(pt_max,-1,-1):
            for j in range(i,-1,-1):
                self.append( Domino(i,j) )

    def tirer(self):
        """
        Renvoie un domino au hasard et le supprime du talon
        """
        domino = self.pop(random.randint(0,len(self)-1))
        return(domino)


class Hand(list):
    """
    Cette classe modèlise à la fois un joueur et sa main de domino. Elle hérite de list. En effet hand contient tout les dominos de la main d'un joueur
    """
    def __init__(self,num,game,mode,name=None,couleur = None):
        """

        :param num: numéro (entier) attribué lors de l'enrengistrement du joueur au début du jeu
        :param game: référence à la l'instance game qui gère le jeu
        :param mode: Un joueur peut être human, IA_hasard, IA_max..., c'est une chaine de caractère. Elle doit appartenir à game.modes_disponibles
        :param name: Nom du joueur, chaine de caractère. Facultatif
        """
        self.num = num
        self.game = game
        self.etat_bloque = False # si la main ne peut definitivement plus jouer cette variable vaut True
        self.mode = mode # mode est la nature du joueur : human, IA (il peut y avoir plusieur type d'IA)
        self.name = name # le nom du joueur sert dans le cas de l'enrengistrement des scores
        self.couleur = couleur

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















