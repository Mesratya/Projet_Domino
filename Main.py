from Dominos import *
from Plateau import *
from PyQt5 import QtCore
from time import sleep
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ____                  _                ____
|  _ \  ___  _ __ ___ (_)_ __   ___    / ___| __ _ _ __ ___   ___
| | | |/ _ \| '_ ` _ \| | '_ \ / _ \  | |  _ / _` | '_ ` _ \ / _ \
| |_| | (_) | | | | | | | | | | (_) | | |_| | (_| | | | | | |  __/
|____/ \___/|_| |_| |_|_|_| |_|\___/   \____|\__,_|_| |_| |_|\___|

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[Module principale]
Ce module est le coeur du Jeu de Domino. Pour jouer il suffit de lancer ce module. En effet le __main__ instanciera un objet game ce qui lancera automatiquement
le jeu avec les paramètres par défauts. Pour rejouer relancez le module ou instanciez un objet game.
Ce Module n'est pas indépendant !
La présence des modules Dominos et Plateau dans le même repertoire est necessaire ainsi que les fichiers txt score, game_opening et game_ending

Le jeu est en mode console. Il suffit de suivre les instructions de la console. L'état de la chaine de domino, la positon spatiale des valeurs 
et toute information utile sera donné en console. Les erreurs de frappe sont géré par le jeu. 

Source Github:
Notre projet à jour est disponile sur le dépot github : https://github.com/Mesratya/Projet_Domino


Warning :
La seul manière de faire planter le jeu est de modifier
les paramètres d'instanciation dans le main (ces derniers ne sont pas encore protégé par des setteur)
c'est le seul endroit ou l'enclapsulation à une utilité puisque, tout autre interaction avec l'utilisateur
se fait en controlant les données reçu.
Par défaut la partie se fait à deux, avec un jeu double-six (six points max sur un domino) et 7 domino par joueurs. Ces paramètres sont modifiable lors de l'instanciation
"""
class Game:
    """
    Classe principale du Jeu. Elle  gère le déroulement du jeu et utilise les autres classes.
    """

    def __init__(self,pt_max = 6,nb_joueur = 2,nb_dominoparjoueur = 7,scoring = False,thread = None,Nb_ligne = 15,Nb_colonne = 15):
        """
        On récupère les paramètres de la partie et on lance la partie avec self.jouer_partie
        Ainsi instancier un objet game lance automatiquement la partie.
        :param pt_max: pt_max est le nombre de points maximal sur un domino
        :param nb_joueur:
        :param nb_dominoparjoueur:
        :param scoring:
        A faire : utiliser un setteur pour assurer l'integrité des données entrée
        """


        self.nb_joueur = nb_joueur
        self.pt_max = pt_max
        self.nb_domino = (pt_max+1)*(pt_max+2)/2
        self.nb_dominoparjoueur=nb_dominoparjoueur
        self.Nb_ligne = Nb_ligne
        self.Nb_colonne = Nb_colonne
        self.modes_disponibles = ["human","IA_max","IA_hasard","IA_equilibre_restreint","IA_equilibre_global"] # mode de jeu des joueurs
        self.couleurs_disponibles = ["orange","vert","bleu","bordeau"]
        self.scoring = scoring
        self.thread = thread

        #self.jouer_partie() # Pour l'instant(pré-IHM) on lance la partie dès l'instanciation de game.





    def initialiser(self):
        """
        Cette méthode permet d'initialiser ou ré-initialiser la partie en créant les différants objets nécessaires.
        Cette procédure n'est pas effectuer dans l'init car on peut lancer plusieurs partie dans un même game (recommancement...)
        :return:
        """
        self.plateau = Plateau(self) # le plateau est initialement vide
        self.talon = Talon(self.pt_max) # le talon se remplit automatiquement
        self.Joueurs = [] # liste des joueurs (objets hand) de la partie

        self.thread.go()

        with open("game_opening") as f: # Ascii art (voir self.fin_de_partie() pour les références)
            game_opening = f.read()
        print(game_opening)




        self.thread.message_box("Choisissez le mode de jeu des participants (humain ou IA)")
        for i in range(self.nb_joueur):  # création des mains

            # on récupère le mode de jeu de chaque joueur
            #mode = input("Donnez le mode du joueur {0} (choisissez parmi {1}) ".format(i,self.modes_disponibles))

            mode = self.thread.choix_mode(num = i)
            while mode not in self.modes_disponibles :
                print("---Saisie Incorrecte Veuillez Recommencer ---")
                #mode = input("Donnez le mode du joueur {0} (choisissez parmi {1}) ".format(i,self.modes_disponibles))
                mode = self.thread.choix_mode(num = i)

            # Dans le cas ou self.scoring = True on demande le pseudo du joueur sinon
            # on s'en tient à son mode de jeu
            hand_name = None
            if self.scoring and mode == "human" :
                #hand_name = input("Donnez votre Pseudo")
                hand_name = self.thread.choix_pseudo()
            else:
                hand_name = mode

            couleur = self.couleurs_disponibles[i]
            self.Joueurs.append(Hand(i, self, mode,hand_name,couleur=couleur))
        print("\n")

        # on remplit chaque main en tirant dans le talon
        for joueur in self.Joueurs:
            for i in range (self.nb_dominoparjoueur):
                joueur.append(self.talon.tirer())

        # on positionne le joueur ayant le plus grand domino en tête de la liste Joueurs
        self.rang_premier_joueur = 0  # position dans la liste Joueurs du joueur ayant le plus fort domino au début du jeu
        for i in range(len(self.Joueurs)):
            if self.Joueurs[i].max_domino() > self.Joueurs[self.rang_premier_joueur].max_domino():
                self.rang_premier_joueur = i

        premier_joueur = self.Joueurs.pop(self.rang_premier_joueur)
        self.Joueurs.insert(0,premier_joueur)


    def jouer_tour(self,joueur):
        """
        Description générale :
        Le joueur joue son tour en fonction de son mode de jeu (human,hasard...)
        Il s'agit de choisir quel domino jouer parmit ce qui sont jouables(en prenant en compte les contraintes topologiques),
        de choisir l'extremité de la chaine si il y'as ambiguité et choisir l'orientation du domino

        Remarque:
        On pourra probablement optimiser cette partie en employant pattern design de type stratégie

        :param joueur: joueur qui joue le tour
        :return: ne renvoie rien
        """
        if joueur.cinq_meme_famille() :
            """
            Si le joueur en question possède 5 domino de la même famille. On déclare la partie fini (self.Jeu_en_cours = False) et on déclare
            le recommencement de la partie nécessaire (self.recommencer = True)
            En effet un joueur n'as pas le droit d'être dans cette situation, il faut tout recommencer !
            """
            self.Jeu_en_cours = False
            self.recommencer = True
            # on prévient tout le monde de la situation
            #print("Le joueur {0} possède 5 dominos de la même famille, il faut recommencer la partie !".format(joueur.num))
            self.thread.message_box("Le joueur {0} possède 5 dominos de la même famille, il faut recommencer la partie !".format(joueur.num))
        else :
            if self.premiere_pose:
                """
                Cette section est executé lors du premier tour (premiere_pose == True) par le joueur en début liste (c'est celui possèdant le 
                plus grand domino). Il va ici poser son plus grand domino comme exigé par les règles du jeu.
                
                """
                max_domino = joueur.max_domino()
                joueur.remove(max_domino)
                self.plateau.poser(max_domino,couleur = joueur.couleur)
                self.premiere_pose = False # on ne repassera plus par cette section

            # A partir d'ici (tour 2 et suivant) on distingue le mode de jeu du joueur pour jouer un tour


            else:
                domino_jouable = joueur.domino_jouable()
                if domino_jouable == []:  # Aucun domino n'est jouable
                    """
                    On traite ici le cas du joueur bloqué et on pense à enrengistrer la situation du joueur
                    si il est définitivement bloqué (bloqué + talon vide)
                    """
                    if len(self.talon) > 0:  # il peut piocher donc il pioche et passe son tour
                        domino_pioche = self.talon.tirer()
                        joueur.append(domino_pioche)
                        #print("Joueur {0} ne peut pas jouer, il pioche {1} et passe son tour \n".format(joueur.num,
                        #                                                                               domino_pioche))
                        self.thread.message_box("Joueur {0} [{1}] ne peut pas jouer, il pioche {2} et passe son tour \n".format(joueur.num,joueur.name,domino_pioche),joueur.mode)
                    else:
                        joueur.etat_bloque = True  # il ne peut pas piocher, le talon est vide, il est définitvement bloqué
                        #print("Le talon est vide : Joueur {0} ne peut définitivement plus jouer \n".format(joueur.num))
                        self.thread.message_box("Le talon est vide : Joueur {0} ne peut définitivement plus jouer \n".format(joueur.num),joueur.mode)
                else:  # le joueur n'est pas bloqué, donc il joue
                    print("Plateau : {0}".format(self.plateau))
                    print(self.plateau.grid)
                    print("Joueur {0} [{1}] : {2}".format(joueur.num,joueur.name, joueur))
                    self.thread.signal_refresh_plateau.emit()
                    self.thread.signal_main.emit(joueur.num,joueur.name,joueur,joueur.couleur)
                    if joueur.mode == "human" or joueur.mode == "Human":
                        """
                        Dans le cas d'un joueur human il choisit le domino, l'extremité de la chaine et l'orientation
                        en fonction de qui est disponible
                        """

                        print("Dominos jouables : {0}\n".format(domino_jouable))
                        rang_domino_choisit = -1
                        while rang_domino_choisit < 0 or rang_domino_choisit > len(domino_jouable)-1:
                            rang_domino_choisit = self.thread.choix_domino(joueur)
                            #rang_domino_choisit = input("Quel domino souhaitez vous posez ? (rang de ce domino) ")

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
                                #rang_extr_choisit = input("Choisissez l'extrémité du plateau 0: {0} ou 1: {1} en tapant 0 ou 1".format(self.plateau[0],self.plateau[-1]))
                                rang_extr_choisit = self.thread.choix_extremite(self.plateau)
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


                        #orientation_choisit = input("Quel orientation pour votre domino ? (Orientations possibles : {0})".format(self.orientations_legales(extr_choisit)))
                        orientation_choisit = self.thread.choix_orientation(extr_choisit)
                        while orientation_choisit not in self.orientations_legales(extr_choisit) :

                            print("Saisie incorrecte tapez seulement une lettre parmi celle proposées")
                            #orientation_choisit = input("Orientations possibles : {0}".format(self.orientations_legales(extr_choisit)))
                            orientation_choisit = self.thread.choix_orientation(extr_choisit)


                    if joueur.mode != "human" :
                        sleep(0.5)


                    if joueur.mode == "IA_hasard":
                        """
                        L'inteliigence artificielle IA_hasard choisit au hasard son domino parmit
                        ceux qui sont jouables
                        """
                        domino_choisit = domino_jouable[random.randint(0, len(domino_jouable) - 1)]
                        if domino_choisit in joueur.domino_jouable_left_side():
                            extr_choisit = "a"
                        elif domino_choisit in joueur.domino_jouable_right_side():
                            extr_choisit = "b"
                        else:
                            # si ambiguité on choisit au hasard l'extremité
                            random_side = random.randint(0, 1)
                            if random_side == 0:
                                extr_choisit = "a"
                            elif random_side == 1:
                                extr_choisit = "b"

                        orientations_possibles = self.orientations_legales(extr_choisit)
                        orientation_choisit = random.choice(orientations_possibles)


                    if joueur.mode == "IA_max":
                        """
                        L'inteliigence artificielle IA_max se débarasse du domino
                        ayant le nombre de points le plus important. En cas de blocage définitif du jeu
                        celui ayant le moins de points à gagné. Cette stratégie est "préventive" dans le sens
                        ou elle se focalise sur la victoire en cas de blocage.
                        """
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

                        orientation_choisit = random.choice(orientations_possibles)

                    if joueur.mode == "IA_equilibre_restreint":
                        """
                        Cette Inteligence artificielle est plus élaboré que les précédentes (et son nom est plus compliqué
                        à taper...) 
                        Cette algo favorise la divesité dans la main afin d'être réactif au prochain tour
                        Elle consiste à choisir de poser le domino qui permet d'avoir une main contenant le plus de type de points 
                        (le plus de familles de points). Dans la version restreinte on favorise la diversité seulement parmit les dominos
                        actuellement jouables (voir IA_equilibre_global pour une divesrité dans toute la main)
                        
                        """

                        domino_jouable = joueur.domino_jouable()

                        Nb_famille_dominos = [] # Cette liste contient pour chaque domino le nombre de famille de points restant dans la main jouable une fois le domino correspondant posé

                        for domino in domino_jouable: # Supposons que l'on pose le domino domino


                            dominos_restant = domino_jouable.copy()
                            dominos_restant.remove(domino) # il restera les autres dominos jouables (ici on utilise seulement les dominos jouables !)

                            # on va compter combien il y'as de membre de chaque famille dans les dominos restant
                            count_pt = [0] * (self.pt_max + 1) # chaque case correspond à une famille

                            for domino_restant in dominos_restant: # on parcourt chaque domino restant

                                if domino_restant.vala == domino_restant.valb:
                                    count_pt[domino_restant.vala] += 1
                                else:
                                    count_pt[domino_restant.vala] += 1
                                    count_pt[domino_restant.valb] += 1

                            nb_famille = 0 # nombre de famille donne le nombre de famille de domino (1 pour chaque famille représenté)

                            for pt in count_pt : # on compte les familles présentes
                                if pt > 0 :
                                    nb_famille += 1

                            Nb_famille_dominos.append(nb_famille)

                        nb_famille_max = max(Nb_famille_dominos) # on récupère le meuilleur score
                        dominos_equilibres = []
                        for rang_domino in range(len(domino_jouable)) : # on cherche le ou les dominos à l'origine de ce meuilleur score

                            if Nb_famille_dominos[rang_domino] == nb_famille_max :

                                dominos_equilibres.append(domino_jouable[rang_domino])
                        domino_choisit = max(dominos_equilibres) # si plusieurs dominos induisent de la diversité on prend celui qui à le plus de point (priorité à la prévention en cas de blocage)



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

                    if joueur.mode == "IA_equilibre_global":
                        """
                        Ce référer à la docstring de IA_equilibre_restreint. On procède simplement à une généralisation
                        C'était l'algo prévu initialement mais la version restreinte à été obtenue par erreur. Cependant
                        Il semble l'equilibre restreint soit plus performant (le hasard fait bien les choses)
                        """

                        domino_jouable = joueur.domino_jouable()

                        Nb_famille_dominos = [] # Cette liste contient pour chaque domino le nombre de famille restant dans la main une fois le domino correspondant posé

                        for domino in domino_jouable: # Supposons que l'on pose le domino domino


                            dominos_restant = joueur.copy()
                            dominos_restant.remove(domino) # il restera les autres dominos


                            count_pt = [0] * (self.pt_max + 1)  # on compte combien il y'as de membre de chaque famille dans les dominos restant

                            for domino_restant in dominos_restant:

                                if domino_restant.vala == domino_restant.valb:
                                    count_pt[domino_restant.vala] += 1
                                else:
                                    count_pt[domino_restant.vala] += 1
                                    count_pt[domino_restant.valb] += 1

                            nb_famille = 0

                            for pt in count_pt :
                                if pt > 0 :
                                    nb_famille += 1

                            Nb_famille_dominos.append(nb_famille)

                        nb_famille_max = max(Nb_famille_dominos)

                        dominos_equilibres = []
                        for rang_domino in range(len(domino_jouable)) :

                            if Nb_famille_dominos[rang_domino] == nb_famille_max :

                                dominos_equilibres.append(domino_jouable[rang_domino])

                        domino_choisit = max(dominos_equilibres) # si deux dominos induisent la diversité on prend celui qui à le plus de point (priorité à la defense)



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

                    joueur.remove(domino_choisit)
                    self.plateau.poser(domino_choisit, extr_choisit,orientation_choisit,couleur=joueur.couleur)
                    print("\n")

                    if len(joueur) == 0:
                        self.Jeu_en_cours = False  # le joueur à posé son dernier domino, arrêter le jeu

    def opposite_orientation(self,orientation):
        """
        :param orientation: orientation ("N","S","W","E")
        :return: renvoie l'orientation opposée (à 180°)
        """
        if orientation == "N" :
            return("S")
        elif orientation == "S" :
            return("N")
        elif orientation == "W" :
            return("E")
        elif orientation == "E" :
            return("W")

    def orientations_legales(self,extr_choisit):
        """
        Pour l'extremité du plateau choisit ("a" ou "b") renvoie les orientations légales.
        :param extr_choisit: "a" ou "b"
        :return: listes des orientations légales pour cette extrémité
        """

        # on récupère la position et l'orientation du demi-domino à l'extremité
        if extr_choisit == "a" :
            pos_extr = self.plateau.pos_extr_a
            extr_orientation = self.plateau.orientation_extr_a
        elif extr_choisit == "b":
            pos_extr = self.plateau.pos_extr_b
            extr_orientation = self.plateau.orientation_extr_b

        orientation_possibles = ["N", "S", "E", "W"] # au départ...
        orientations_legales = []

        for orientation_a_tester in orientation_possibles : # Pour chaque orientation à tester on récupère les positions correspondantes et on verifie que la place est libre (" ")
            (pos_a_checker_1,pos_a_checker_2) = self.plateau.position_demi_domino(pos_extr,extr_orientation,orientation_a_tester)
            if self.plateau.grid[pos_a_checker_1] == " " and self.plateau.grid[pos_a_checker_2] == " " and orientation_a_tester != self.opposite_orientation(extr_orientation) :
                orientations_legales.append(orientation_a_tester)

        return(orientations_legales)






    def jouer_partie(self):
        """
        La partie est gérée dans cette méthode jusqu'a la fin de la partie
        Cette méthode est RECURSIVE. En effet, suite à la boucle while on appel self.fin_de_partie() qui rappel jouer_partie
        à moins que l'on soit dans le cas de base (cad que self.recommencer == False en fin de partie)
        :return:
        """
        self.initialiser() # initialisation ou remise à zéro
        self.Jeu_en_cours = True
        self.recommencer = False
        self.premiere_pose = True

        self.thread.signal_background_sound.emit()
        
        while self.Jeu_en_cours :

            for joueur in self.Joueurs :
                if self.Jeu_en_cours :
                    self.jouer_tour(joueur)
            # A la fin du tour on regarde si tout le monde est bloqué
            if [joueur.etat_bloque for joueur in self.Joueurs] == [True]*self.nb_joueur :
                self.Jeu_en_cours = False # Tout les joueurs sont bloqués, arrêter le jeu

        self.fin_de_partie()

    def fin_de_partie(self):

        if self.recommencer == True : # le cas de base n'est pas vérifié donc on appelle self.jouer_partie

            print("Nouvelle Partie")
            self.thread.message_box("Nouvelle Partie")
            self.thread.init_main()
            self.jouer_partie()
        else :
            # le fameux cas de base : la partie n'as pas à être recommencé donc on ne rappel pas self.jouer_partie
            gagnant = self.Joueurs[0]
            for joueur in self.Joueurs:
                if joueur.pt_restant() < gagnant.pt_restant():
                    gagnant = joueur

            # le score du gagnant est le nombre de points des autres joueurs
            score_gagnant = 0
            for joueur in self.Joueurs:
                if joueur != gagnant :
                    score_gagnant += joueur.pt_restant()

            #print("Le gagnant est Joueur {0} [{1}] avec un score de {2} points !".format(gagnant.num,gagnant.name,score_gagnant))
            self.thread.signal_sound_fx.emit("sounds/effect/win.wav")
            self.thread.message_box("Le gagnant est Joueur {0} [{1}] avec un score de {2} points !".format(gagnant.num,gagnant.name,score_gagnant))


            if self.scoring :
                # on récupère le nom des heureux perdants...
                Perdants = self.Joueurs.copy()
                Perdants.remove(gagnant)
                Perdants_name = []
                for perdant in Perdants:
                    Perdants_name.append(perdant.name)

                with open("score",mode='a') as f:
                    f.write("{0} gagne face a {1} Score ==> {2} points".format(gagnant.name,Perdants_name,score_gagnant))
                    f.write("\n")

            self.thread.init_main()
            self.recommencer = self.thread.demande_recommencer()
            if self.recommencer in ["Yes","Maybe","can you repeat the question ?"]:
                self.thread.message_box("Nouvelle Partie")
                self.jouer_partie()


            with open("game_ending") as f: # L'auteur des ascii arts dominos est David Riley et ils proviennent de http://ascii.co.uk/
                game_ending = f.read()
            print(game_ending)

            # Consultation_score = input("Voulez-vous consulter la Table des Scores ? [répondre par oui ou par non]")
            # while Consultation_score not in ["oui","non"]:
            #     print("-------Réponse incorrecte-------")
            #     Consultation_score = input("Voulez-vous consulter la Table des Scores ? [répondre par oui ou par non]")
            # if Consultation_score == "oui":
            #     with open("score") as f:
            #         score = f.read()
            #     print(score)



if __name__ == "__main__":
    """
    Cette section ne se lance quand lancant Main.py
    On modifier cette section en instanciant plusieurs game avec des paramères différants de ceux par défaut
    """

    Game = Game(scoring=False,nb_joueur=2)
