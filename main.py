"""
Programme principal du solveur de Sudoku.
"""

import time
from src.grid import Grid
from src.brute_force import BruteForce
from src.backtracking import Backtracking
from src.gui import SudokuGUI

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

def solve_grid(grid, method):
    """Résout la grille avec la méthode choisie."""
    if method == 1:
        solver = BruteForce(grid)
        method_name = "force brute"
    else:
        solver = Backtracking(grid)
        method_name = "backtracking"
    
    print(f"\nRésolution par {method_name} en cours...")
    start_time = time.time()
    solver.solve()
    solve_time = time.time() - start_time
    
    print(f"\nSolution par {method_name}:")
    grid.print(highlight_original=True)
    print(f"Temps d'exécution: {solve_time:.6f} secondes")
    return solve_time

def main():
    """Fonction principale du programme."""
    try:
        # Choisir le niveau de difficulté
        file_name = choose_difficulty()
        file_path = f"examples/{file_name}"
        
        # Charger la grille
        grid = Grid()
        grid.load_from_file(file_path)
        
        print("\nGrille originale (les chiffres en gras sont les valeurs d'origine):")
        grid.print(highlight_original=True)
        
        # Choisir la méthode de résolution
        method = choose_method()
        
        # Résoudre la grille
        solve_time = solve_grid(grid, method)
        
        # Affichage graphique
        choice = input("\nVoulez-vous afficher la grille avec l'interface graphique? (o/n): ")
        if choice.lower() == 'o':
            gui = SudokuGUI(grid, grid)  # On passe la même grille deux fois car on veut garder les valeurs d'origine
            gui.run()
            
    except Exception as e:
        print(f"Erreur: {e}")
        print("Assurez-vous que le fichier existe dans le dossier examples/")

if __name__ == "__main__":
    main() 