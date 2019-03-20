import numpy as np

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