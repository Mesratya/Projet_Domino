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
    def __init__(self,num,game):
        self.num = num
        self.game = game
        self.etat_bloque = False # si la main ne peut definitivement plus jouer cette variable vaut true

    def domino_jouable(self):
        '''Renvoie les dominos de la main qui sont posables sur le plateau'''
        dom_jouab = []
        extr_a = self.game.plateau.extr_a
        extr_b = self.game.plateau.extr_b
        for domino in self :
            if domino.vala == extr_a or domino.valb == extr_a or domino.vala == extr_b or domino.valb == extr_b :
                dom_jouab.append(domino)
        return(dom_jouab)

    def domino_jouable_left_side(self):
        '''Renvoie les dominos de la main qui sont posables du coté gauche du plateau'''
        dom_jouab_left_side = []
        extr_a = self.game.plateau.extr_a
        extr_b = self.game.plateau.extr_b
        for domino in self:

            if (domino.vala == extr_a or domino.valb == extr_a) and domino.vala != extr_b and domino.valb != extr_b:
                dom_jouab_left_side.append(domino) # le domino n'est jouable que sur extr_a

        return (dom_jouab_left_side)

    def domino_jouable_right_side(self):
        '''Renvoie les dominos de la main qui sont posables sur un unique coté du plateau'''
        dom_jouab_right_side = []
        extr_a = self.game.plateau.extr_a
        extr_b = self.game.plateau.extr_b
        for domino in self:

            if (domino.vala == extr_b or domino.valb == extr_b) and domino.vala != extr_a and domino.valb != extr_a:
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



class plateau(list):
    """Pour l'instant les domino sont posés en ligne sans considerer les virages"""

    def __init__(self,game):
        self.grid = [[(None,None)]*game.size]*game.size # cette grille permettera le stockage de la position 2D des dominos
        self.extr_a = None
        self.extr_b = None
        self.game = game

    def poser(self,domino,extr = None):
        """ajoute le domino au plateau à l'extremité souhaité"""

        if self.game.premiere_pose :
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
            self.Joueurs.append(hand(i,self))
        self.distribuer()
        self.Partie()




    def distribuer(self):

        for joueur in self.Joueurs:
            for i in range (self.nb_dominoparjoueur):
                joueur.append(self.talon.tirer())

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
        else :
            domino_jouable = joueur.domino_jouable()
            if  domino_jouable == [] : # Aucun domino n'est jouable
                if len(self.talon) > 0 : # il peut piocher donc il pioche et passe son tour
                    domino_pioche = self.talon.tirer()
                    joueur.append(domino_pioche)
                    print("Joueur {0} ne peut pas jouer, il pioche {1} et passe son tour".format(joueur.num,domino_pioche))
                else :
                    joueur.etat_bloque = True # il ne peut pas piocher, le talon est vide, il est définitvement bloqué
                    print("Le talon est vide : Joueur {0} ne peut définitivement plus jouer".format(joueur.num))
            else : # le joueur peut jouer, il joue
                print("Plateau : {0}".format(self.plateau))
                print("Joueur {0} : {1}".format(joueur.num,joueur))
                domino_choisit = domino_jouable[int(input("Dominos jouables : {0} /n Quel domino souhaitez vous posez ? (rang de ce domino) :".format(domino_jouable)))]

                if domino_choisit in joueur.domino_jouable_left_side() :
                    extr_choisit = self.plateau.extr_a
                elif domino_choisit in joueur.domino_jouable_right_side() :
                    extr_choisit = self.plateau.extr_b
                else :
                    extr_choisit = input("De quel coté poser ce domino ? /n Tapez gauche ou droite")
                    if extr_choisit == "gauche" or extr_choisit == "Gauche":
                        extr_choisit = self.plateau.extr_a
                    elif extr_choisit == "droite" or extr_choisit == "Droite":
                        extr_choisit = self.plateau.extr_b

                joueur.remove(domino_choisit)
                self.plateau.poser(domino_choisit,extr_choisit)

                if len(joueur) == 0 :
                    self.Jeu_en_cours = False # le joueur à posé son dernier domino, arrêter le jeu




    def Partie(self):
        """La partie est gérée dans cette méthode jusqu'a la fin du jeu"""
        self.Jeu_en_cours = True
        self.premiere_pose = True

        while self.Jeu_en_cours :
            for joueur in self.Joueurs :
                if self.Jeu_en_cours :
                    self.jouer_tour(joueur)
            if [joueur.etat_bloque for joueur in self.Joueurs] == [True]*4 :
                self.Jeu_en_cours = False # Tout les joueurs sont bloqués, arrêter le jeu

        self.fin_de_partie()

    def fin_de_partie(self):
        gagnant = self.Joueurs[0]
        for joueur in self.Joueurs :
            if joueur.pt_restant() < gagnant.pt_restant() :
                gagnant = joueur
        print("Le gagnant est : Joueur {0}".format(gagnant.num))



if __name__ == "__main__":
    Game = game()





