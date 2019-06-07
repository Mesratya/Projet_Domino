# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from interface import Ui_MainWindow
from Main import *
from PyQt5.QtMultimedia import QSound

class ClickableLabel(QtWidgets.QLabel):
    """
    label clicable inspiré de https://stackoverflow.com/questions/21354516/is-possible-to-put-an-image-instead-of-a-button-and-make-it-clickable
    """

    clicked = QtCore.pyqtSignal(str)

    def __init__(self,message):
        super(ClickableLabel, self).__init__()
        # pixmap = QtGui.QPixmap(width, height)
        # pixmap.fill(QtGui.QColor(color))
        # self.setPixmap(pixmap)
        # self.setObjectName(color)
        self.message = message

    def mousePressEvent(self, event):
        self.clicked.emit(self.message)

class UI(QtWidgets.QMainWindow):

    signal_choix_fait = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Configuration de l'interface utilisateur.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # Ajout du fond d'écran
        indice_background = str(np.random.randint(0,4))
        print(indice_background)
        self.setStyleSheet("QMainWindow{ background-image: url(images/textures/texture_"+ indice_background +"); }")


        self.put_sound = QSound("sounds/effect/put.wav")
        self.background_sound = QSound(None)


        # Création d'une partie
        #self.game = Game(UI = self)

        #création du thread gérant le jeu lui même
        self.thread = ThreadGame(UI = self)

        #connection des signaux provenant du thread
        self.thread.signal_init_grid.connect(self.init_grid_void)
        self.thread.signal_poser.connect(self.poser)
        self.thread.signal_main.connect(self.afficher_main)
        self.thread.signal_choix_domino.connect(self.calque_choix_domino)
        self.thread.signal_choix_extremite.connect(self.calque_choix_extremite)
        self.thread.signal_refresh_plateau.connect(self.refresh_plateau)
        self.thread.signal_choix_orientation.connect(self.calque_choix_orientation)
        self.thread.signal_choix_mode.connect(self.calque_choix_mode)
        self.thread.signal_choix_pseudo.connect(self.calque_choix_pseudo)
        self.thread.signal_message_box.connect(self.afficher_message_box)
        self.thread.signal_choix_recommencer.connect(self.choix_recommencer)
        self.thread.signal_init_main.connect(self.init_main)
        self.thread.signal_terminus.connect(self.terminus)
        self.thread.signal_background_sound.connect(self.init_background_sound)
        self.thread.signal_sound_fx.connect(self.sound_fx)
        self.thread.signal_nb_joueur.connect(self.choix_nombre_joueur)
        self.thread.signal_go.connect(self.go)




        #démarage du thread et donc de Game
        self.thread.start()

        #Liste des layouts de dominos de la main
        self.hand_layout_container = []

        # # on lance la musique du jeu !
        # self.background_sound.play()




    def init_grid_void(self,Nb_ligne,Nb_colonne):
        """
        initialisation d'une grille totalement transparante
        """
        print("Nettoyage")
        self.clearLayout(self.ui.gridlayout)
        self.ui.gridlayout.setSpacing(0)
        self.ui.gridlayout.setContentsMargins(0, 0, 0, 0)

        # initialisation de la grille
        for i in range(Nb_ligne):
            for j in range(Nb_colonne):
                pixmap = QtGui.QPixmap(None)
                label = QtWidgets.QLabel()
                label.setPixmap(pixmap)
                label.setFixedSize(30, 30)
                self.ui.gridlayout.addWidget(label, i, j)

    def init_grid(self):
        '''
        initialisation d'une grille avec des cases grises en transparance
        '''

        Nb_ligne = self.thread.game.plateau.Nb_ligne
        Nb_colonne = self.thread.game.plateau.Nb_colonne

        self.clearLayout(self.ui.gridlayout)
        self.ui.gridlayout.setSpacing(0)
        self.ui.gridlayout.setContentsMargins(0, 0, 0, 0)

        # initialisation de la grille
        for i in range(Nb_ligne):
            for j in range(Nb_colonne):
                pixmap = QtGui.QPixmap("images/calque_gris")
                label = QtWidgets.QLabel()
                label.setPixmap(pixmap)
                label.setFixedSize(49, 49)
                self.ui.gridlayout.addWidget(label, i, j)

    def refresh_plateau(self):
        plateau = self.thread.game.plateau
        self.init_grid()
        """
        Méthode permettant de réafficher l'état du plateau proprement, ce qui permet de ce debarasser des layout clickables et autres ajouts temporaires
        """
        for domino in plateau :
            self.poser(domino)

    def init_main(self):
        self.clearLayout(self.ui.handlayout)

    def terminus(self):
        self.close()


    def clearLayout(self,layout):
        """
        Méthode permettant de vider un layout de ces widgets
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def poser(self,domino):
        """
        Méthode permettant d'afficher un domino à l'ecran

        """

        pixmap = QtGui.QPixmap("images/"+str(domino.vala)+"/"+domino.couleur+".png")
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        label.setFixedSize(49, 49)
        self.ui.gridlayout.addWidget(label,domino.posa[0]-1, domino.posa[1]-1)

        pixmap = QtGui.QPixmap("images/" + str(domino.valb) + "/"+domino.couleur+".png")
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        label.setFixedSize(49, 49)
        self.ui.gridlayout.addWidget(label, domino.posb[0]-1, domino.posb[1]-1)

        self.put_sound.play()



    def afficher_main(self,num,name,main,couleur):

        self.clearLayout(self.ui.handlayout)
        self.hand_layout_container = []
        # self.ui.handlayout.setSpacing(0)
        # self.ui.handlayout.setContentsMargins(0, 0, 0, 0)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ui.handlayout.addItem(spacerItem)
        label = QtWidgets.QLabel("Joueur {0} [{1}]".format(num,name))
        label.setStyleSheet("QLabel { background-color : rgb(71,55,55,129); color : black; font: bold 20px;}")
        self.ui.handlayout.addWidget(label)



        for domino in main :
            dominowidget = QtWidgets.QWidget(self.ui.handwidget)
            dominowidget.setObjectName("widget_"+str(domino))
            domino_layout = QtWidgets.QVBoxLayout(dominowidget)
            domino_layout.setObjectName(str(domino))
            domino_layout.setSpacing(0)
            domino_layout.setContentsMargins(0,0,0,0)
            self.ui.handlayout.addWidget(dominowidget)


            self.hand_layout_container.append(domino_layout)

            label = self.label_pixmap("images/" + str(domino.vala) + "/" + couleur + ".png")
            domino_layout.addWidget(label)


            label = self.label_pixmap("images/" + str(domino.valb) + "/" + couleur + ".png")
            domino_layout.addWidget(label)


        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ui.handlayout.addItem(spacerItem)

    def calque_choix_domino(self,joueur):
        dominos_jouables = [str(domino) for domino in joueur.domino_jouable()]
        cnt_layout = 0 # compte l'indice des layout jouables
        for domino_layout in self.hand_layout_container:
            if domino_layout.objectName() in dominos_jouables :
                object_name = domino_layout.objectName()
                vala, valb = object_name[1], object_name[3]
                self.clearLayout(domino_layout)
                label = self.label_pixmap_surligne("images/" + str(vala) + "/" + joueur.couleur + ".png",message= str(cnt_layout))
                domino_layout.addWidget(label)
                label = self.label_pixmap_surligne("images/" + str(valb) + "/" + joueur.couleur + ".png",message= str(cnt_layout))
                domino_layout.addWidget(label)
                cnt_layout += 1

    def calque_choix_extremite(self,plateau):
        extr_a = plateau.extr_a
        extr_b = plateau.extr_b
        pos_extr_a = plateau.pos_extr_a
        pos_extr_b = plateau.pos_extr_b
        couleur_a = plateau[0].couleur
        couleur_b = plateau[-1].couleur


        label = self.label_pixmap_surligne("images/" + str(extr_a) + "/" + couleur_a + ".png",message= str(0))
        self.ui.gridlayout.addWidget(label, pos_extr_a[0] - 1, pos_extr_a[1] - 1)

        label = self.label_pixmap_surligne("images/" + str(extr_b) + "/" + couleur_b + ".png", message=str(1))
        self.ui.gridlayout.addWidget(label, pos_extr_b[0] - 1, pos_extr_b[1] - 1)

    def calque_choix_orientation(self,extr_choisit):

        orientations_legales = self.thread.game.orientations_legales(extr_choisit)
        plateau = self.thread.game.plateau


        for orientation in orientations_legales :
            if extr_choisit == "a":
                pos_extr = plateau.pos_extr_a
                extr_orientation = plateau.orientation_extr_a
            if extr_choisit == "b":
                pos_extr = plateau.pos_extr_b
                extr_orientation = plateau.orientation_extr_b
            i,j = plateau.position_demi_domino(pos_extr, extr_orientation, domino_orientation=orientation)[1]
            label = self.label_pixmap_surligne("images/arrow/" + orientation + ".png" ,message = orientation)
            self.ui.gridlayout.addWidget(label,i-1,j-1)

    def calque_choix_mode(self,num):

        Nb_ligne = self.thread.game.plateau.Nb_ligne
        Nb_colonne = self.thread.game.plateau.Nb_colonne

        self.init_grid_void(Nb_ligne,Nb_colonne) # on s'assure que la grille ne contient des cases totalement tranparantes

        pixmap = QtGui.QPixmap("images/human.png")
        label = ClickableLabel(message = "human")
        label.clicked.connect(self.envoyer)
        label.setPixmap(pixmap)
        label.setFixedSize(99, 99)
        self.ui.gridlayout.addWidget(label, Nb_ligne//2, (Nb_colonne//2)-1)

        pixmap = QtGui.QPixmap("images/bot.png")
        label = ClickableLabel(message="IA_equilibre_global")
        label.clicked.connect(self.envoyer)
        label.setPixmap(pixmap)
        label.setFixedSize(99, 99)
        self.ui.gridlayout.addWidget(label, Nb_ligne //2, (Nb_colonne // 2) + 1)

        # if num == 0 :
        #     self.init_intro_sound()
        #     self.intro_sound.play()


    def calque_choix_pseudo(self):
        pseudo = QtWidgets.QInputDialog.getText(self,"Choix du Pseudo","Entrer votre Pseudo :")[0]
        self.signal_choix_fait.emit(pseudo)

    def choix_nombre_joueur(self):
        nb_joueur = QtWidgets.QInputDialog.getItem(self, "Choix du nombre de Joueurs", "Nombre de Joueurs :",("2","3","4"))[0]
        self.signal_choix_fait.emit(str(nb_joueur))

    def afficher_message_box(self,message):
        msg = QtWidgets.QMessageBox.question(self,None,message,QtWidgets.QMessageBox.Ok)
        self.signal_choix_fait.emit("ok")

    def choix_recommencer(self):
        message = QtWidgets.QInputDialog.getItem(self,"Voulez-vous recommencer la partie ?","Choix :",("Yes","No","Maybe","I don't know","can you repeat the question ?"))[0]
        self.signal_choix_fait.emit(message)
    def label_pixmap(self,image_adresse):
        pixmap = QtGui.QPixmap(image_adresse)
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        label.setFixedSize(49, 49)
        return(label)

    def label_pixmap_surligne(self,image_adresse,message):

        image = QtGui.QImage(image_adresse)
        overlay = QtGui.QImage("images/calque_selection.png")
        painter = QtGui.QPainter()
        painter.begin(image)
        painter.drawImage(0, 0, overlay)
        painter.end()
        label = ClickableLabel(message)
        label.clicked.connect(self.envoyer)
        label.setPixmap(QtGui.QPixmap.fromImage(image))
        label.setFixedSize(49, 49)
        return (label)

    def envoyer(self,message):
        self.signal_choix_fait.emit(message)


    def init_intro_sound(self):
        
        indice_background = str(np.random.randint(0, 4))
        print(indice_background)
        self.setStyleSheet("QMainWindow{ background-image: url(images/textures/texture_" + indice_background + "); }")

        indice_intro = str(np.random.randint(0, 4))
        self.intro_sound = QSound("sounds/intro/intro_" + indice_intro + ".wav")
        self.background_sound.stop()


    def init_background_sound(self):
        # choix des sons au hasard dans la playlist (extrait de Zelda Windwaker)
        indice_theme = str(np.random.randint(0, 5))
        self.background_sound = QSound("sounds/main_theme/theme_" + indice_theme + ".wav")
        self.background_sound.setLoops(-1)

        self.intro_sound.stop()
        sleep(0.2)
        self.background_sound.play()
        print("back_sound")

    def sound_fx(self,adress_sound):
        self.background_sound.stop()
        sleep(0.4)
        self.fx_sound = QSound(adress_sound)
        self.fx_sound.play()

    def resize(self):
        self.ui.setFixedSize(self.ui.centralWidget.size())

    def go(self):

        Nb_ligne = self.thread.game.plateau.Nb_ligne
        Nb_colonne = self.thread.game.plateau.Nb_colonne

        self.init_grid_void(Nb_ligne,Nb_colonne)  # on s'assure que la grille ne contient des cases totalement tranparantes

        pixmap = QtGui.QPixmap("images/manette.png")
        label = ClickableLabel(message="human")
        label.clicked.connect(self.envoyer)
        label.setPixmap(pixmap)
        label.setFixedSize(99, 99)
        self.ui.gridlayout.addWidget(label, Nb_ligne // 2, (Nb_colonne // 2))


        self.init_intro_sound()
        self.intro_sound.play()








class ThreadGame(QtCore.QThread):

    #Signaux customs
    signal_init_grid = QtCore.pyqtSignal()
    signal_poser = QtCore.pyqtSignal(Domino)
    signal_main = QtCore.pyqtSignal(int,str,list,str)
    signal_choix_domino = QtCore.pyqtSignal(Hand)
    signal_choix_extremite = QtCore.pyqtSignal(Plateau)
    signal_refresh_plateau = QtCore.pyqtSignal()
    signal_choix_orientation = QtCore.pyqtSignal(str)
    signal_choix_mode = QtCore.pyqtSignal(int)
    signal_choix_pseudo = QtCore.pyqtSignal()
    signal_message_box = QtCore.pyqtSignal(str)
    signal_choix_recommencer = QtCore.pyqtSignal()
    signal_init_main = QtCore.pyqtSignal()
    signal_terminus = QtCore.pyqtSignal()
    signal_background_sound = QtCore.pyqtSignal()
    signal_sound_fx = QtCore.pyqtSignal(str)
    signal_nb_joueur = QtCore.pyqtSignal()
    signal_go = QtCore.pyqtSignal()


    def __init__(self,UI,parent = None):
        super(ThreadGame,self).__init__(parent)
        self.choix_fait = None
        self.UI = UI
        self.UI.signal_choix_fait.connect(self.update_choix)




    def run(self):
        self.nb_joueur = self.choix_nombre_joueur()

        self.game = Game(thread = self,nb_joueur=self.nb_joueur,scoring = True)
        self.game.jouer_partie()

        self.terminus()


    def choix_domino(self,joueur):
        #print("choix_domino executé")
        #il faut demander à l'IHM de poser de souligner  les dominos de la main qui sont jouables
        # ces dominos devront être clicable et renvoyer un signal avec leurs nom
        self.signal_refresh_plateau.emit()
        self.signal_choix_domino.emit(joueur)
        self.wait_signal(self.UI.signal_choix_fait)
        self.signal_main.emit(joueur.num,joueur.name,joueur,joueur.couleur) # le choix (même invalide) à été fait donc on réaffiche la main pour faire disparaitre le surlignage
        print("choix_fait :" + self.choix_fait)
        return(self.choix_fait)


    def choix_extremite(self,plateau):
        #il faut demander à l'IHM de poser de souligner  les deux extremités du plateau
        # ces demi dominos devront être clicable et renvoyer un signal avec leurs nom
        self.signal_choix_extremite.emit(plateau)
        self.wait_signal(self.UI.signal_choix_fait)
        self.signal_refresh_plateau.emit()
        print("choix_fait :" + self.choix_fait)
        return(self.choix_fait)


    def choix_orientation(self,extr_choisit):
        # il faut demander à l'IHM de poser des fleches (domino transparant ayant une inscription en fleche) clickable qui renvoie leurs orientations
        # Il faut les poser autour de l'extremité choisit et n'afficher que celle appartenant à game.orientation_legale(extr_choisit)

        self.signal_choix_orientation.emit(extr_choisit)
        self.wait_signal(self.UI.signal_choix_fait)
        self.signal_refresh_plateau.emit()
        print("choix_fait :" + self.choix_fait)
        return (self.choix_fait)


    def choix_mode(self,num):
        # il faut demander à l'IHM de poser des icones humain et Ordi pour choisir les modes de jeu

        self.signal_refresh_plateau.emit()
        self.signal_choix_mode.emit(num)
        self.wait_signal(self.UI.signal_choix_fait)
        print("choix_fait :" + self.choix_fait)
        self.signal_init_grid.emit()
        return (self.choix_fait)


    def choix_pseudo(self):
        self.signal_choix_pseudo.emit()
        self.wait_signal(self.UI.signal_choix_fait)
        self.signal_init_grid.emit()
        print("choix_fait :" + self.choix_fait)
        return (self.choix_fait)

    def message_box(self,message,mode_joueur = None):
        if (mode_joueur == None or mode_joueur == "human") :
            self.signal_message_box.emit(message)
            self.wait_signal(self.UI.signal_choix_fait)
            print("choix_fait :" + self.choix_fait)
            return (self.choix_fait)

    def demande_recommencer(self):
        self.signal_choix_recommencer.emit()
        self.wait_signal(self.UI.signal_choix_fait)
        self.signal_init_grid.emit()
        print("choix_fait :" + self.choix_fait)
        return (self.choix_fait)


    def choix_nombre_joueur(self):
        self.signal_nb_joueur.emit()
        self.wait_signal(self.UI.signal_choix_fait)

        print("choix_fait :" + self.choix_fait)
        return (int(self.choix_fait))

    def terminus(self):
        self.signal_terminus.emit()


    def update_choix(self,message):
        self.choix_fait = message

    def init_main(self):
        self.signal_init_main.emit()

    def go(self):

        self.signal_go.emit()
        self.wait_signal(self.UI.signal_choix_fait)
        print("choix_fait :" + self.choix_fait)
        self.signal_init_grid.emit()


    def wait_signal(self,signal): # fonction qui bloque le thread jusqu'a reception du signal

        loop = QtCore.QEventLoop()
        signal.connect(loop.quit)
        loop.exec_()













if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    app.exec_()


