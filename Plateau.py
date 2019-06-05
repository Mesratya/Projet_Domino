import numpy as np

"""
[Module secondaire]
Ce module est destiné à la définition de la classe plateau
"""

class Plateau(list):
    """La classe plateau modélise un plateau de jeu. Elle hérite de list. Ainsi la liste plateau est la chaîne de dominos posés.
    La gestion de l'espace de jeu et des contraintes topologique se fait à l'aide du tableau numpy grid contenant des caractères(cf. attribut grid dans l'init)
    """

    def __init__(self,game):
        """
        On crée la grille de jeu. La grille de jeu possède les dimensions maximales atteignables par un joueur qui alignerait volontairement tout les dominos
        Ainsi, aucun gestion des effets de bords n'est nécessaire.Initialement On remplit la grille de "x" signifiant que la case n'est pas jouable.
        :param game: référence au jeu en cours
        """
        self.Nb_ligne = game.Nb_ligne
        self.Nb_colonne  = game.Nb_colonne
        self.grid = np.array([["x"]*(self.Nb_colonne+2)]*(self.Nb_ligne+2)) # cette grille permet de lier les valeurs des demi-domino à leurs position réel sur le plateau, elle ne sert pas à l'IHM mais à la recherche de "contrainte topologique locale"

        for i in range(1,self.Nb_ligne+1): # on choisit une dimension jouables qui puisse être affiché dans la console python
            for j in range(1,self.Nb_colonne+1):
                self.grid[i,j] = " " # une case vide " " est une case jouable sur laquel un demi-domino peut se poser, tout autre caractère est un obstacle
        self.extr_a = None # valeurs des extrémitées de la chaîne de dominos
        self.extr_b = None
        self.pos_extr_a = None # position des extremitées de la chaine sur le plateau
        self.pos_extr_b = None
        self.orientation_extr_a = None # orientation des extrémitées
        self.orientation_extr_b = None
        self.game = game
        self.game.thread.signal_init_grid.emit()


    def position_demi_domino(self,pos_extr,extr_orientation,domino_orientation):
        """
        Fonctionnement:
        Calcul de la position des deux demi domino en fonction de la position et de l'orientation
        de l'extremité et de l'orientation du domino à poser.

        Détails:
        On peut poser un domino dans 3 orientation possibles et le domino à l'extrémité de
        la chaine possède aussi une orientation. Il est necessaire de distingué proprement les cas. Un schéma expiquant la manière dont les indices
        ont été calculés sera disponible dans le rapport

        :param pos_extr: position de l'extrémité de chaine considéré
        :param extr_orientation: orientation de l'extrémité de chaine considéré
        :param domino_orientation: orientation du domino choisit
        :return: position des deux demi dominos
        """
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

    def poser(self,domino,extr = None,orientation = None,couleur = "orange"):
        """
        ajoute le domino au plateau à l'extremité souhaité et selon l'orientation choisit (North,South,East,West)


        :param domino: domnio à poser
        :param extr: extremité choisit pour la pose (facultatif, dans le cas d'une première pose par ex.)
        :param orientation: orientation choisit (idem facultatif)
        :return: ne renvoie rien...
        """

        if self.game.premiere_pose : # Cette section concerne la toute première pose de domino
            nb_domino = self.game.nb_domino

            domino.posa = (int(self.Nb_ligne//2),int(self.Nb_colonne//2)) # On place le premier domino horizontalement au centre du plateau
            domino.posb = (int(self.Nb_ligne//2),int(self.Nb_colonne//2)+1)
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
                domino = domino.inverser()

            if orientation == self.game.opposite_orientation(self.orientation_extr_a) : # si le joueur exige l'orientation impossible convertir en son opposé
                orientation = self.orientation_extr_a # on inverse l'orientation (par ex W-E n'est pas possible donc W-W)


            # c'est le demi domino b qui est collé ici on le met donc en premier dans le tuple
            domino.posb , domino.posa = self.position_demi_domino(self.pos_extr_a,self.orientation_extr_a,orientation)


            self.grid[domino.posa] = int(domino.vala)  # à la position du demi domino on place sa valeur
            self.grid[domino.posb] = int(domino.valb)  # idem

            self.insert(0,domino)

            self.extr_a = domino.vala
            self.pos_extr_a = domino.posa
            self.orientation_extr_a = orientation


        elif extr == "b" :

            if domino.valb == self.extr_b :
                domino = domino.inverser()

            if orientation == self.game.opposite_orientation(self.orientation_extr_b) : # si le joueur exige l'orientation impossible convertir en son opposé
                orientation = self.orientation_extr_b # on inverse l'orientation (par ex W-E n'est pas possible donc W-W)

            # c'est le demi domino a qui est collé ici on le met donc en premier dans le tuple
            domino.posa , domino.posb = self.position_demi_domino(self.pos_extr_b, self.orientation_extr_b,orientation)



            self.grid[domino.posa] = int(domino.vala)  # à la position du demi domino on place sa valeur
            self.grid[domino.posb] = int(domino.valb)  # idem

            self.append(domino)

            self.extr_b = domino.valb
            self.pos_extr_b = domino.posb
            self.orientation_extr_b = orientation

        domino.couleur = couleur
        self.game.thread.signal_poser.emit(domino)
