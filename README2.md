# Avis personnels sur le projet

## Trajan : 
La méthode de la force brute teste toutes les possibilités une par une pour une grille de 9x9,
ce qui représente un nombre colossal de possibilités et est donc une perte de temps, tandis que la 
méthode du backtracking, en utilisant la récursivité, réduit progressivement le nombre de cases à 
résoudre et permet un gain sur les cases précédemment résolues. Le backtracking est préférable à 
la force brute dans une optique d'optimisation du temps de calcul.

## Nans : 
Au début on pensait que la méthode force brute ne serait pas si longue, mais en réalité elle doit 
réaliser toutes les combinaisons d'un tableau 9x9 qui est bien trop long.
Au final la méthode backtracking fut beaucoup plus efficace, en essayant de trouver les combinaisons 
case par case, ce qui est bien plus optimisé. 
C'est donc pour cela que la méthode backtracking est la plus rapide en résolvant le Sudoku en moins de 1 seconde
alors que c'est des milliers d'années pour un ordinateur avec la force brute.

## Adam :
Ce projet a révolutionné ma conception des algorithmes. La force brute sur une grille avec 45 cases vides implique 9^45 possibilités, un nombre si colossal qu'il dépasse l'imagination humaine. L'univers entier ne contient que 10^23 étoiles : nous parlons donc d'un nombre quasiment 100 quintillions de fois plus grand !

Face à cette infinité, même avec la dernière RTX 5090 calculant 100 trillions d'opérations par seconde, la résolution par force brute prendrait environ 200 milliards de fois l'âge actuel de l'univers. Pourtant, le backtracking résout ce même problème en 0.002 seconde.

Cette expérience transcende le simple exercice académique : elle m'a enseigné que l'élégance algorithmique est l'essence même de l'informatique, transformant l'impossible en immédiat par la pure puissance de la logique.
