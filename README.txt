# Projet_Domino
Projet Domino en python

Auteurs : Mesrati Yassin et Gillian Roth FISE 2021

Source Github:
Notre projet à jour est disponile sur le dépot github : https://github.com/Mesratya/Projet_Domino
(Telecharger le dossier Projet_Domino complet dans la branche master du dépot github)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ____                  _                ____
|  _ \  ___  _ __ ___ (_)_ __   ___    / ___| __ _ _ __ ___   ___
| | | |/ _ \| '_ ` _ \| | '_ \ / _ \  | |  _ / _` | '_ ` _ \ / _ \
| |_| | (_) | | | | | | | | | | (_) | | |_| | (_| | | | | | |  __/
|____/ \___/|_| |_| |_|_|_| |_|\___/   \____|\__,_|_| |_| |_|\___|

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Le jeu se lance en executant le fichier Game.py via Python 3.6
Il suffit de suivre les instructions dans la console
Bon jeu !



Informations complémentaires sur le Module Principal Gamepy 
(infos disponiles dans la doc du Module Game.py) :

Ce module est le coeur du Jeu de Domino. Pour jouer il suffit de lancer ce module. En effet le __main__ instanciera un objet game ce qui lancera automatiquement
le jeu avec les paramètres par défauts. Pour rejouer relancez le module ou instanciez un objet game.
Ce Module n'est pas indépendant !
La présence des modules Dominos et Plateau dans le même repertoire est necessaire ainsi que les fichiers txt score, game_opening et game_ending

Le jeu est en mode console. Il suffit de suivre les instructions de la console. L'état de la chaine de domino, la positon spatiale des valeurs 
et toute information utile sera donné en console. Les erreurs de frappe sont géré par le jeu. 

Warning :
La seul manière de faire planter le jeu est de modifier
les paramètres d'instanciation dans le main (ces derniers ne sont pas encore protégé par des setteur)
c'est le seul endroit ou l'enclapsulation à une utilité puisque, tout autre interaction avec l'utilisateur
se fait en controlant les données reçu
Par défaut la partie se fait à deux, avec un jeu double-six (six points max sur un domino) et 7 domino par joueurs. Ces paramètres sont modifiable lors de l'instanciation
