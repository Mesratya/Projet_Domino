import unittest
from Main import *

"""Ce module contient quelques tests unitaires du Projet Domino
    Ces tests sont pour l'instant écrit à des fins essentiellement pédagogique
    puisque le dévloppement du code pré-IHM c'est fait en testant systématiquement le
    code en faisant jouer des IA (aux stratégies diverses) plutot quand faisant tourner des test unitaires
    """

class Testdomino(unittest.TestCase):
    """Classe de test unitaire pour la classe Domino"""

    def setUp(self):
        """Méthode d'initialisation appelér avant chaque test"""
        pass

    def testInit(self):
        """Test de la méthode d'initialisation des dominos"""
        for i in range(10):
            for j in range(10):
                D = domino(i,j,(7,8),(7,9))
                self.assertEqual(D.vala,i)
                self.assertEqual(D.valb,j)
                self.assertEqual(D.posa,(7,8))
                self.assertEqual(D.posb, (7, 9))

    def testComp(self):
        """Test de la comparaison entre des dominos"""
        for i in range(10):
            for j in range(10):
                D1 = domino(i,j)
                D2 = domino(i+1,j)
                self.assertTrue(D1 < D2)

    def testVal_totale(self):
        for i in range(10):
            for j in range(10):
                val_totale = domino(i,j).val_totale()
                self.assertEqual(val_totale,i+j)

    def testInverser(self):
        """Test de l'inversion d'un domino"""
        for i in range(10):
            for j in range(10):
                D = domino(i,j)
                D_inv = D.inverser()
                self.assertEqual(D.vala,D_inv.valb)
                self.assertEqual(D.valb,D_inv.vala)

class Test_talon(unittest.TestCase):
    """Classe de test unitaire pour la classe talon"""

    def setUp(self):
        """Méthode d'initialisation appelér avant chaque test"""
        pass

    # La classe talon ne necessite pas de test unitaire
    # Le talon généré est valide




if __name__ == '__main__':
    unittest.main()