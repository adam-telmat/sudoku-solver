#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programme principal du solveur de Sudoku.
"""

import time
import sys
from src.grid import Grid
from src.brute_force import BruteForce
from src.backtracking import Backtracking

# Vérifier si pygame est disponible
PYGAME_AVAILABLE = True
try:
    import pygame
    from src.gui import SudokuGUI
except ImportError:
    PYGAME_AVAILABLE = False
except Exception:
    # Si une autre erreur se produit (comme video system not initialized)
    PYGAME_AVAILABLE = False

def choose_difficulty():
    """Permet à l'utilisateur de choisir le niveau de difficulté."""
    print("\nChoisissez le niveau de difficulté :")
    print("1. Débutant")
    print("2. Facile")
    print("3. Moyen")
    print("4. Difficile")
    print("5. Extrême")
    
    while True:
        try:
            choice = int(input("\nVotre choix (1-5) : "))
            if 1 <= choice <= 5:
                difficulties = {
                    1: "01_beginner.txt",
                    2: "02_easy.txt",
                    3: "03_medium.txt",
                    4: "04_hard.txt",
                    5: "05_extreme.txt"
                }
                return difficulties[choice]
            else:
                print("Veuillez choisir un nombre entre 1 et 5")
        except ValueError:
            print("Veuillez entrer un nombre valide")

def choose_method():
    """Permet à l'utilisateur de choisir la méthode de résolution."""
    print("\nChoisissez la méthode de résolution :")
    print("1. Force brute")
    print("2. Backtracking")
    
    while True:
        try:
            choice = int(input("\nVotre choix (1-2) : "))
            if choice in [1, 2]:
                return choice
            else:
                print("Veuillez choisir 1 ou 2")
        except ValueError:
            print("Veuillez entrer un nombre valide")

def choose_display_mode():
    """Permet à l'utilisateur de choisir le mode d'affichage."""
    if not PYGAME_AVAILABLE:
        print("\nMode graphique non disponible. Utilisation du mode console uniquement.")
        return 1
        
    print("\nChoisissez le mode d'affichage :")
    print("1. Résultat final uniquement")
    print("2. Animation du processus de résolution")
    
    while True:
        try:
            choice = int(input("\nVotre choix (1-2) : "))
            if choice in [1, 2]:
                return choice
            else:
                print("Veuillez choisir 1 ou 2")
        except ValueError:
            print("Veuillez entrer un nombre valide")

def solve_grid_without_animation(grid, method):
    """Résout la grille sans animation.
    
    Args:
        grid (Grid): La grille à résoudre
        method (int): La méthode de résolution (1: force brute, 2: backtracking)
        
    Returns:
        tuple: (Grid résolue, temps d'exécution, nombre de tentatives)
    """
    solver_grid = grid.copy()
    
    if method == 1:
        print("\nRésolution par force brute en cours...")
        solver = BruteForce(solver_grid)
        # Désactiver l'animation pour la force brute
        solver.animate = False
    else:
        print("\nRésolution par backtracking en cours...")
        solver = Backtracking(solver_grid)
        # Désactiver l'animation pour le backtracking
        solver.animate = False
    
    start_time = time.time()
    solver.solve()
    execution_time = time.time() - start_time
    
    # Récupérer le nombre de tentatives (seulement disponible pour BruteForce)
    attempts = getattr(solver, 'attempts', 0)
    
    return solver_grid, execution_time, attempts

def main():
    """Fonction principale du programme."""
    running = True
    
    while running:
        try:
            # Afficher un message de bienvenue
            print("\n" + "="*50)
            print("=== Solveur de Sudoku ===".center(50))
            print("="*50)
            print("Ce programme permet de résoudre des grilles de Sudoku et de comparer")
            print("les performances de deux algorithmes : force brute et backtracking.")
            
            # Choisir le niveau de difficulté
            file_name = choose_difficulty()
            file_path = f"examples/{file_name}"
            
            # Charger la grille
            grid = Grid()
            grid.load_from_file(file_path)
            
            print("\nGrille originale:")
            grid.print()
            
            # Choisir la méthode de résolution
            method = choose_method()
            
            # Choisir le mode d'affichage (seulement si pygame est disponible)
            display_mode = choose_display_mode()
            
            # Si mode animation et pygame disponible
            if display_mode == 2 and PYGAME_AVAILABLE:
                print("\nLancement de l'animation de résolution...")
                gui = SudokuGUI()
                result = gui.run_with_animation(grid, "brute_force" if method == 1 else "backtracking")
                
                if result == "QUIT":
                    print("\nAppuyez sur Entrée pour continuer...")
                    input()
                continue  # Revenir au menu principal
            
            # Sinon, résolution normale sans animation
            solved_grid, execution_time, attempts = solve_grid_without_animation(grid, method)
            
            method_name = "force brute" if method == 1 else "backtracking"
            print(f"\nSolution par {method_name}:")
            solved_grid.print(highlight_original=True)
            print(f"Temps d'exécution: {execution_time:.6f} secondes")
            
            # Affichage graphique du résultat final (seulement si pygame est disponible)
            if PYGAME_AVAILABLE:
                show_gui = input("\nVoulez-vous afficher la grille avec l'interface graphique? (o/n): ")
                if show_gui.lower() == 'o':
                    method_name = "brute_force" if method == 1 else "backtracking"
                    gui = SudokuGUI(solved_grid, grid, algorithm_name=method_name)
                    result = gui.run()
                    
                    if result == "QUIT":
                        print("\nAppuyez sur Entrée pour continuer...")
                        input()
                    continue
            
            # Demander si l'utilisateur veut réessayer
            retry = input("\nVoulez-vous résoudre une autre grille? (o/n): ")
            if retry.lower() != 'o':
                print("\nMerci d'avoir utilisé le solveur de Sudoku !")
                running = False
                
        except Exception as e:
            print(f"Erreur: {e}")
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 