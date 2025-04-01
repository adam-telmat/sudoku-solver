# Sudoku Solver

## Description

Ce projet est un solveur de grilles de Sudoku en Python. Il permet de résoudre des grilles de Sudoku fournies sous forme de fichiers .txt, en utilisant au choix :

- La méthode du backtracking (recherche exhaustive avec retour en arrière)
- La méthode de la force brute (essai systématique de toutes les combinaisons)

Le programme offre également une interface graphique permettant de visualiser le processus de résolution et de comparer les performances des deux algorithmes.

## Contexte du projet

Ce projet a été réalisé dans le cadre du cours de Programmation Avancée. L'objectif était de mettre en œuvre différentes approches algorithmiques pour résoudre un problème classique d'intelligence artificielle et de combinatoire : le Sudoku.

Le Sudoku est un jeu de logique où l'on doit remplir une grille 9x9 avec des chiffres de 1 à 9, de manière à ce que chaque ligne, chaque colonne et chaque sous-grille 3x3 contienne tous les chiffres de 1 à 9 sans répétition.

Ce problème est particulièrement intéressant car il permet d'explorer différentes stratégies de résolution et de comparer leur efficacité.

## Structure du projet

Le projet est organisé en plusieurs modules Python :

- `main.py` : Point d'entrée du programme, permettant de choisir le niveau de difficulté, la méthode de résolution et d'afficher les résultats.
- `src/backtracking.py` : Contient l'implémentation de l'algorithme de résolution par backtracking.
- `src/brute_force.py` : Implémente la résolution par force brute.
- `src/grid.py` : Gère le chargement et la manipulation des grilles Sudoku.
- `src/gui.py` : Fournit une interface graphique interactive pour visualiser le processus de résolution.
- `examples/` : Contient des grilles Sudoku de différents niveaux de difficulté.

## Algorithmes de résolution

### Force Brute

Notre algorithme de force brute fonctionne comme lorsqu'on essaie de trouver la combinaison d'un cadenas :

- Dans l'animation, on observe que l'algorithme remplit instantanément toutes les cases vides avec des 1
- Ensuite, il commence à incrémenter certains de ces chiffres (de 1 à 2, de 2 à 3, etc.)
- À chaque grille complète, il vérifie si elle respecte les règles du Sudoku
- Si elle respecte les règles, l'algorithme s'arrête (comme un cadenas qui s'ouvre)
- Sinon, il continue à tester d'autres combinaisons en incrémentant les chiffres

Cette approche a une complexité théorique de 9^n (où n est le nombre de cases vides). Pour une grille avec 45 cases vides, cela représente potentiellement 9^45 combinaisons possibles, un nombre astronomique rendant la force brute impraticable pour des grilles complexes.

Contrairement au backtracking, la force brute ne vérifie pas la validité après chaque placement individuel de chiffre. Elle remplit d'abord complètement la grille, puis vérifie si l'ensemble de la solution est valide, ce qui la rend beaucoup moins efficace.

### Backtracking

L'algorithme de backtracking est une amélioration de la force brute qui intègre des vérifications de validité à chaque étape. Avant de placer un chiffre, l'algorithme vérifie s'il respecte les règles du Sudoku :
- Pas de répétition dans la même ligne
- Pas de répétition dans la même colonne
- Pas de répétition dans la même sous-grille 3x3

Cette stratégie réduit considérablement l'espace de recherche en éliminant rapidement les branches qui ne mèneront pas à une solution valide.

## Analyse comparative des méthodes

Nos tests ont montré une différence de performance extrême entre les deux approches :

| Niveau de difficulté | Force Brute | Backtracking (temps moyen) | Observation |
|----------------------|-------------|----------------------------|-------------|
| Débutant (45 cases vides)   | Interrompu après 10000 tentatives | ~0.002 secondes | Force brute impraticable |
| Facile (47 cases vides)    | Interrompu après 10000 tentatives | ~0.01 secondes | Force brute impraticable |
| Moyen (50 cases vides)     | Interrompu après 10000 tentatives | ~0.03 secondes  | Force brute impraticable |
| Difficile (56 cases vides) | Interrompu après 10000 tentatives | ~0.05 secondes  | Force brute impraticable |
| Extrême (58 cases vides)   | Interrompu après 10000 tentatives | ~0.1 secondes  | Force brute impraticable |

Observations clés :
1. **Complexité théorique** : La force brute a une complexité de 9^n (où n est le nombre de cases vides). Pour une grille débutante avec 45 cases vides, cela représente théoriquement 9^45 ≈ 1,2 × 10^43 combinaisons potentielles, un nombre astronomique.
2. **Limites pratiques** : Dans notre implémentation, l'algorithme de force brute est interrompu après 10000 tentatives pour des raisons pratiques, car il est mathématiquement impossible qu'il termine en un temps raisonnable.
3. **Efficacité du backtracking** : Le backtracking résout même les grilles les plus difficiles en seulement 0.1 seconde grâce aux vérifications de validité qui éliminent rapidement les branches non prometteuses.

Cette analyse démontre pourquoi la force brute pure n'est jamais utilisée en pratique pour résoudre des problèmes combinatoires complexes comme le Sudoku. Les optimisations du backtracking sont absolument essentielles pour obtenir des solutions en temps raisonnable.

## Interface Graphique

Le projet inclut une interface graphique développée avec Pygame qui permet de :
- Visualiser les grilles de Sudoku
- Observer le processus de résolution étape par étape
- Comparer les performances des deux algorithmes
- Distinguer clairement les valeurs d'origine et les valeurs calculées

L'interface offre également la possibilité de choisir le niveau de difficulté et la méthode de résolution.

## Installation

### Prérequis

- Python 3.x
- Pygame (pour l'interface graphique)

```bash
pip install pygame
```

## Utilisation

Exécutez le programme principal :

```bash
python main.py
```

Le programme vous proposera :
1. De choisir le niveau de difficulté
2. De sélectionner la méthode de résolution
3. De visualiser l'animation du processus ou simplement le résultat final

## Format des fichiers Sudoku

Les grilles de Sudoku sont stockées dans des fichiers texte avec le format suivant :
- Chaque ligne représente une ligne de la grille
- Les chiffres de 1 à 9 pour les cases remplies
- Le caractère underscore (_) pour les cases vides

Exemple :
```
7__92_4__
______7__
__4__8312
4____25__
2___1___3
__85____4
8432__6__
__5______
__2_64__5
```

## Veille technologique

Notre démarche de veille technologique s'est articulée autour de plusieurs axes complémentaires :

### Sources documentaires et théoriques

Pour appréhender les concepts théoriques du backtracking et de la force brute, nous avons exploré diverses ressources :

- **Documentation académique** : Articles et publications scientifiques sur les algorithmes de résolution de contraintes
- **Wikipedia** : Étude des pages dédiées aux algorithmes de backtracking, concepts de force brute et problématiques de Sudoku
- **Tutoriels en ligne** : Ressources pédagogiques expliquant les principes algorithmiques fondamentaux

### Ressources audiovisuelles et démonstratives

Les concepts étant parfois abstraits, nous avons complété notre recherche par des supports visuels :

- **YouTube** : Visualisation de démonstrations d'algorithmes de backtracking et de force brute
- **Conférences en ligne** : Présentations techniques sur l'optimisation des algorithmes de recherche

### Intelligence artificielle comme support d'apprentissage

Les outils d'IA générative nous ont servi à affiner notre compréhension et notre implémentation :

- **ChatGPT** : Clarification des concepts algorithmiques et assistance pour la résolution de problèmes spécifiques
- **Claude Sonnet** : Aide à la conception de l'architecture logicielle et optimisation du code
- **Grok** : Exploration des meilleures pratiques pour l'implémentation Python des algorithmes de résolution

### Application pratique et implémentation

La dernière phase de notre veille s'est concentrée sur l'aspect pratique :

- **Bibliothèques Python** : Évaluation des alternatives comme PyGame pour l'interface graphique
- **Optimisations algorithmiques** : Recherche des techniques spécifiques pour améliorer les performances de résolution
- **Méthodes de test** : Approches pour mesurer et comparer les performances des différents algorithmes

Cette veille multidimensionnelle nous a permis de développer une compréhension approfondie des algorithmes que nous avons implémentés, tout en nous offrant une vision globale des différentes approches possibles pour résoudre le problème du Sudoku.

## Conclusion

Ce projet de solveur de Sudoku représente bien plus qu'un simple exercice académique. Il constitue une exploration approfondie des concepts algorithmiques fondamentaux et une application concrète des compétences en développement logiciel. Nos principales réalisations incluent :

### Apports techniques

- **Maîtrise algorithmique** : Implémentation et comparaison de deux approches de résolution distinctes, démontrant l'importance cruciale des optimisations algorithmiques
- **Visualisation interactive** : Développement d'une interface graphique permettant d'observer et de comprendre le comportement des algorithmes en temps réel
- **Analyse de performance** : Étude quantitative rigoureuse démontrant une différence d'efficacité spectaculaire entre les approches

### Compétences développées

- **Conception logicielle** : Organisation modulaire du code facilitant la maintenance et les évolutions futures
- **Résolution de problèmes complexes** : Approche méthodique face à un problème combinatoire exponentiel
- **Travail collaboratif** : Utilisation efficace d'outils de versionnement et de collaboration pour le développement en équipe

### Perspectives d'amélioration

Pour un développement futur, nous avons identifié plusieurs pistes prometteuses :
- Implémentation d'algorithmes plus avancés
- Ajout de fonctionnalités permettant de générer des grilles de Sudoku
- Intégration d'une caméra pour reconnaître et résoudre des grilles photographiées

Cette expérience nous a permis d'appréhender concrètement l'impact considérable des choix algorithmiques sur les performances d'un système, une leçon fondamentale que nous pourrons appliquer à de nombreux défis informatiques futurs.

## Auteurs

Trajan Letrosne
Adam Telmat
Margaux Troude
Nans Moreno




