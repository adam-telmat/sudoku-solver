# sudoku-solver

Description

Ce projet est un solveur de grilles de Sudoku en Python. Il permet de résoudre des grilles de Sudoku fournies sous forme de fichiers .txt, en utilisant au choix :

La méthode du backtracking (recherche exhaustive avec retour en arrière)

La méthode de la force brute (essai systématique de toutes les combinaisons)

Le programme offre également une interface graphique pour faciliter l'utilisation.

# Structure du projet

Le projet est organisé en plusieurs fichiers Python :

backtracking.py : Contient l'implémentation de l'algorithme de résolution par backtracking.

brute_force.py : Implémente la résolution par force brute.

grid.py : Gère le chargement et la manipulation des grilles Sudoku.

gui.py : Fournit une interface graphique pour interagir avec le solveur.

main.py : Point d'entrée du programme, permettant de choisir la méthode de résolution et d'afficher les résultats.

#Installation

Prérequis

Python 3.x

# Utilisation

Mode ligne de commande

Exécutez le programme en ligne de commande en spécifiant la méthode de résolution et le fichier contenant la grille Sudoku :

python main.py --method backtracking --file sudoku.txt

Ou pour la force brute :

python main.py --method brute_force --file sudoku.txt

Mode graphique

Lancez l'interface graphique avec :

python gui.py

# Format des fichiers Sudoku

Les grilles de Sudoku doivent être stockées dans un fichier texte avec le format suivant :

Une ligne par ligne de la grille

Les chiffres de 1 à 9 pour les cases remplies

. pour les cases vides

Exemple :

5 3 . . 7 . . . .
6 . . 1 9 5 . . .
. 9 8 . . . . 6 .
8 . . . 6 . . . 3
4 . . 8 . 3 . . 1
7 . . . 2 . . . 6
. 6 . . . . 2 8 .
. . . 4 1 9 . . 5
. . . . 8 . . 7 9

# Auteurs

Trajan Letrosne

Adam Telmat

Margaux Troude

Nans Moreno




