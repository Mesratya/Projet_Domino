"""
Quelques notes...
"""""

# Images
pixmap = QtGui.QPixmap("images/4/orange.png")


"""Méthodo pour communiquer avec l'IHM' :
Utiliser des signaux """

"1/ créer le signal sous la class ThreadGame:"
    signalGameOk = QtCore.pyqtSignal()

"2/ le connecter à la méthode voulu dans la class UI"
    self.thread.signalGameOk.connect(self.gameOk)

"3/ créeer la méthode si necessaire"

"4/ emettre le signal depuis le game en fesant referance au thread"
    self.thread.signalGameOk.emit()


"générer une boite de dialogue qui récupère un texte"
text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

"générer une message box toute simple --> Comment améliorer le rendu graphique ?"
QtWidgets.QMessageBox.about(self, "orientation", "Choisissez une orientation")