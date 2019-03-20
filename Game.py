from Dominos import *
from Plateau import *


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