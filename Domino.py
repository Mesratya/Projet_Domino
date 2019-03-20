import random
import numpy as np

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




class plateau(list):
    """Pour l'instant les domino sont posés en ligne sans considerer les virages"""

    def __init__(self,game):
        self.Nb_colonne  = int((4 * game.nb_domino) - 2)
        self.Nb_ligne = int((4 * game.nb_domino) - 1)
        self.grid = np.array([["x"]*self.Nb_colonne]*self.Nb_ligne) # cette grille permet de lier les valeurs des demi-domino à leurs position réel sur le plateau, elle ne sert pas à l'IHM mais à la recherche de "contrainte topologique locale"
        for i in range(46,63+1):
            for j in range(48,63+1):
                self.grid[i,j] = " "
        self.extr_a = None
        self.extr_b = None
        self.pos_extr_a = None # position des extremitées sur le plateau
        self.pos_extr_b = None
        self.orientation_extr_a = None
        self.orientation_extr_b = None
        self.game = game

    def position_demi_domino(self,pos_extr,extr_orientation,domino_orientation):
        '''calcul de la position des deux demi domino en fonction de la position et de l'orientation de l'extremité et de l'orientation du domino à poser'''
        (i,j) = pos_extr
        #print("(i,j) = ({0},{1})".format(i,j))
        (i,j) = (int(i),int(j))
        #print("(int(i),int(j)) = ({0},{1})".format(i,j))
        #print(extr_orientation,domino_orientation)


        if extr_orientation == "W":
            if domino_orientation == "W" or domino_orientation == "E" :
                return((i,j-1),(i,j-2))
            elif domino_orientation == "N":
                return ((i,j-1),(i-1,j-1))
            elif domino_orientation == "S":
                return ((i,j-1),(i+1,j-1))

        if extr_orientation == "E":
            if domino_orientation == "E" or domino_orientation == "W" :
                return((i,j+1),(i,j+2))
            elif domino_orientation == "N":
                return ((i,j+1),(i-1,j+1))
            elif domino_orientation == "S":
                return ((i,j+1),(i+1,j+1))

        if extr_orientation == "N": #à faire
            if domino_orientation == "N" or domino_orientation == "S":
                return ((i-1, j), (i-2, j))
            elif domino_orientation == "W":
                return ((i -1 , j), (i-1, j-1))
            elif domino_orientation == "E":
                return ((i - 1, j), (i-1, j+1))

        if extr_orientation == "S": # à faire
            if domino_orientation == "S" or domino_orientation == "N":
                return ((i+1, j), (i+2, j))
            elif domino_orientation == "W":
                return ((i+1, j), (i + 1, j - 1))
            elif domino_orientation == "E":
                return ((i+1, j), (i + 1, j + 1))

    def poser(self,domino,extr = None,orientation = None):
        """ajoute le domino au plateau à l'extremité souhaité et selon l'orientation choisit (North,South,East,West)"""

        if self.game.premiere_pose :
            nb_domino = self.game.nb_domino

            domino.posa = (int(2*nb_domino-2),int(2*nb_domino-2)) # On place le premier domino horizontalement au centre du plateau
            domino.posb = (int(2*nb_domino-2),int(2*nb_domino-1))
            self.pos_extr_a = domino.posa
            self.pos_extr_b = domino.posb

            self.grid[domino.posa] = int(domino.vala) # à la position du demi domino on place sa valeur
            self.grid[domino.posb] = int(domino.valb) # idem

            self.extr_a = domino.vala
            self.extr_b = domino.valb

            self.orientation_extr_a = "W"
            self.orientation_extr_b = "E"

            self.append(domino)

        # A ce stade, l'extremité du plateau est fixé, il s'agit de collé correctement le domino en le retournant si necessaire et en respectant l'orientation lors du positionnement dans le plan
        if extr == "a" :

            if domino.vala == self.extr_a :
                domino = domino.inverted()

            if orientation == self.game.opposite_orientation(self.orientation_extr_a) : # si le joueur exige l'orientation impossible convertir en son opposé
                orientation = self.orientation_extr_a # on inverse l'orientation (par ex W-E n'est pas possible donc W-W)


            # c'est le demi domino b qui est collé ici on le met donc en premier dans le tuple
            domino.posb , domino.posa = self.position_demi_domino(self.pos_extr_a,self.orientation_extr_a,orientation)
            print("pos(a) = {0} and pos(b) = {1} b is locked".format(domino.posa,domino.posb))

            self.grid[domino.posa] = int(domino.vala)  # à la position du demi domino on place sa valeur
            self.grid[domino.posb] = int(domino.valb)  # idem

            self.insert(0,domino)

            self.extr_a = domino.vala
            self.pos_extr_a = domino.posa
            self.orientation_extr_a = orientation


        elif extr == "b" :

            if domino.valb == self.extr_b :
                domino = domino.inverted()

            if orientation == self.game.opposite_orientation(self.orientation_extr_b) : # si le joueur exige l'orientation impossible convertir en son opposé
                orientation = self.orientation_extr_b # on inverse l'orientation (par ex W-E n'est pas possible donc W-W)

            # c'est le demi domino a qui est collé ici on le met donc en premier dans le tuple
            domino.posa , domino.posb = self.position_demi_domino(self.pos_extr_b, self.orientation_extr_b,orientation)
            print("pos(a) = {0} and pos(b) = {1} a is locked".format(domino.posa, domino.posb))


            self.grid[domino.posa] = int(domino.vala)  # à la position du demi domino on place sa valeur
            self.grid[domino.posb] = int(domino.valb)  # idem

            self.append(domino)

            self.extr_b = domino.valb
            self.pos_extr_b = domino.posb
            self.orientation_extr_b = orientation



class game:

    def __init__(self,pt_max = 6,nb_joueur = 2,nb_dominoparjoueur = 7):
        '''pt_max est le nombre de points maximal sur un domino'''

        self.nb_joueur = nb_joueur
        self.pt_max = pt_max
        self.nb_domino = (pt_max+1)*(pt_max+2)/2
        self.nb_dominoparjoueur=nb_dominoparjoueur
        self.size = int(self.nb_domino * 2) # On s'assure que tous les dominos peuvent être alignés sur le plateau
        self.modes_disponibles = ["human","IA_max","IA_hasard"] # mode de jeu des joueurs

        self.jouer_partie()


    def initialiser(self):
        self.plateau = plateau(self)
        self.talon = talon(self.pt_max)
        self.Joueurs = []
        for i in range(self.nb_joueur):  # création des mains

            mode = input("Donnez le mode du joueur {0} (tapez human, IA_max ou IA_hasard) ".format(i))
            while mode not in self.modes_disponibles :
                print("---Saisie Incorrecte Veuillez Recommencer ---")
                mode = input("Donnez le mode du joueur {0} (tapez human, IA_max ou IA_hasard) ".format(i))

            self.Joueurs.append(hand(i, self, mode))
        print("\n")


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
        if joueur.cinq_meme_famille() :
            self.Jeu_en_cours = False
            self.recommencer = True
            print("Le joueur {0} possède 5 dominos de la même famille, il faut recommencer la partie !".format(joueur.num))
        else :
            if self.premiere_pose:
                max_domino = joueur.max_domino()
                joueur.remove(max_domino)
                self.plateau.poser(max_domino)
                self.premiere_pose = False
            else:
                domino_jouable = joueur.domino_jouable()
                if domino_jouable == []:  # Aucun domino n'est jouable
                    if len(self.talon) > 0:  # il peut piocher donc il pioche et passe son tour
                        domino_pioche = self.talon.tirer()
                        joueur.append(domino_pioche)
                        print("Joueur {0} ne peut pas jouer, il pioche {1} et passe son tour \n".format(joueur.num,
                                                                                                        domino_pioche))
                    else:
                        joueur.etat_bloque = True  # il ne peut pas piocher, le talon est vide, il est définitvement bloqué
                        print("Le talon est vide : Joueur {0} ne peut définitivement plus jouer \n".format(joueur.num))
                else:  # le joueur peut jouer, il joue
                    print("Plateau : {0}".format(self.plateau))
                    print(self.plateau.grid[45:65,47:65])
                    print("Joueur {0} : {1}".format(joueur.num, joueur))
                    if joueur.mode == "human" or joueur.mode == "Human": # l'usage de la boucle while combiné au test d'excpetion est inspiré du Zcasino (https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/231735-tp-tous-au-zcasino)

                        print("Dominos jouables : {0}\n".format(domino_jouable))
                        rang_domino_choisit = -1
                        while rang_domino_choisit < 0 or rang_domino_choisit > len(domino_jouable)-1:
                            rang_domino_choisit = input("Quel domino souhaitez vous posez ? (rang de ce domino) ")
                            try :
                                rang_domino_choisit = int(rang_domino_choisit)
                            except ValueError :
                                print("---Vous n'avez pas saisi un nombre---")
                                rang_domino_choisit = -1
                                continue
                            if rang_domino_choisit < 0 :
                                print(("---Ce nombre est négatif---"))
                            if rang_domino_choisit > len(domino_jouable)-1:
                                print("---Ce nombre est plus grand que le rang maximal des dominos jouables---")

                        domino_choisit = domino_jouable[rang_domino_choisit]


                        if domino_choisit in joueur.domino_jouable_left_side():
                            extr_choisit = "a"
                        elif domino_choisit in joueur.domino_jouable_right_side():
                            extr_choisit = "b"
                        else:
                            rang_extr_choisit = -1

                            while rang_extr_choisit < 0 or rang_extr_choisit > 1:
                                rang_extr_choisit = input("Choisissez de l'extrémité du plateau 0: {0} ou 1: {1} en tapant 0 ou 1".format(self.plateau[0],self.plateau[-1]))
                                try:
                                    rang_extr_choisit = int(rang_extr_choisit)
                                except ValueError:
                                    print("---Vous n'avez pas saisi un nombre---")
                                    rang_extr_choisit = -1
                                    continue
                                if rang_extr_choisit < 0:
                                    print(("---Ce nombre est négatif---"))
                                if rang_extr_choisit > 1:
                                    print("---Ce nombre est plus grand 1 ---")

                            if rang_extr_choisit == 0:
                                extr_choisit = "a"
                            elif rang_extr_choisit == 1:
                                extr_choisit = "b"


                        orientation_choisit = input("Quel orientation pour votre domino ? (Orientations possibles : {0})".format(self.orientations_legales(extr_choisit)))
                        while orientation_choisit not in self.orientations_legales(extr_choisit) :

                            print("Saisie incorrecte tapez seulement une lettre parmi celle proposées")
                            orientation_choisit = input("Orientations possibles : {0}".format(self.orientations_legales(extr_choisit)))





                    if joueur.mode == "IA_hasard":
                        domino_choisit = domino_jouable[random.randint(0, len(domino_jouable) - 1)]
                        if domino_choisit in joueur.domino_jouable_left_side():
                            extr_choisit = "a"
                        elif domino_choisit in joueur.domino_jouable_right_side():
                            extr_choisit = "b"
                        else:
                            random_side = random.randint(0, 1)
                            if random_side == 0:
                                extr_choisit = "a"
                            elif random_side == 1:
                                extr_choisit = "b"

                        orientations_possibles = self.orientations_legales(extr_choisit)
                        orientation_choisit = random.choice(orientations_possibles)


                    if joueur.mode == "IA_max":
                        domino_choisit = max(domino_jouable)
                        if domino_choisit in joueur.domino_jouable_left_side():
                            extr_choisit = "a"
                        elif domino_choisit in joueur.domino_jouable_right_side():
                            extr_choisit = "b"
                        else:
                            random_side = random.randint(0, 1)
                            if random_side == 0:
                                extr_choisit = "a"
                            elif random_side == 1:
                                extr_choisit = "b"

                        orientations_possibles = self.orientations_legales(extr_choisit)
                        print(orientations_possibles)
                        orientation_choisit = random.choice(orientations_possibles)

                    joueur.remove(domino_choisit)
                    self.plateau.poser(domino_choisit, extr_choisit,orientation_choisit)
                    print("\n")

                    if len(joueur) == 0:
                        self.Jeu_en_cours = False  # le joueur à posé son dernier domino, arrêter le jeu

    def opposite_orientation(self,orientation):
        if orientation == "N" :
            return("S")
        elif orientation == "S" :
            return("N")
        elif orientation == "W" :
            return("E")
        elif orientation == "E" :
            return("W")

    def orientations_legales(self,extr_choisit):

        if extr_choisit == "a" :
            pos_extr = self.plateau.pos_extr_a
            extr_orientation = self.plateau.orientation_extr_a
        elif extr_choisit == "b":
            pos_extr = self.plateau.pos_extr_b
            extr_orientation = self.plateau.orientation_extr_b

        orientation_possibles = ["N", "S", "E", "W"]
        orientations_legales = []

        for orientation_a_tester in orientation_possibles : # Pour chaque orientation on récupère les positions correspondantes et on verifie que la place est libre (" ")
            (pos_a_checker_1,pos_a_checker_2) = self.plateau.position_demi_domino(pos_extr,extr_orientation,orientation_a_tester)
            if self.plateau.grid[pos_a_checker_1] == " " and self.plateau.grid[pos_a_checker_2] == " " and orientation_a_tester != self.opposite_orientation(extr_orientation) :
                orientations_legales.append(orientation_a_tester)

        return(orientations_legales)






    def jouer_partie(self):
        """La partie est gérée dans cette méthode jusqu'a la fin du jeu"""
        self.initialiser() # initialisation ou remise à zéro
        self.Jeu_en_cours = True
        self.recommencer = False
        self.premiere_pose = True

        while self.Jeu_en_cours :
            for joueur in self.Joueurs :
                if self.Jeu_en_cours :
                    self.jouer_tour(joueur)
            if [joueur.etat_bloque for joueur in self.Joueurs] == [True]*self.nb_joueur :
                self.Jeu_en_cours = False # Tout les joueurs sont bloqués, arrêter le jeu

        self.fin_de_partie()

    def fin_de_partie(self):
        if self.recommencer :
            print("Nouvelle Partie")
            self.jouer_partie()
        else :
            gagnant = self.Joueurs[0]
            for joueur in self.Joueurs:
                if joueur.pt_restant() < gagnant.pt_restant():
                    gagnant = joueur
            print("Le gagnant est : Joueur {0}".format(gagnant.num))



if __name__ == "__main__":
    Game = game()
    print(Game.plateau, Game.plateau.grid)






