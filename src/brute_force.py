"""
Module contenant l'implémentation de l'algorithme de force brute pour résoudre le Sudoku.
"""

class BruteForce:
    """Classe implémentant l'algorithme de force brute pour résoudre le Sudoku."""
    
    def __init__(self, grid):
        """Initialise le solveur avec une grille.
        
        Args:
            grid (Grid): La grille à résoudre
        """
        self.grid = grid
        self.solutions = []
    
    def solve(self):
        """Résout la grille en utilisant la force brute.
        
        Returns:
            bool: True si une solution a été trouvée, False sinon
        """
        return self._solve_recursive(0, 0)
    
    def _solve_recursive(self, row, col):
        """Résout récursivement la grille en essayant toutes les combinaisons possibles.
        
        Args:
            row (int): Index de la ligne actuelle
            col (int): Index de la colonne actuelle
            
        Returns:
            bool: True si une solution a été trouvée, False sinon
        """
        # Si on a atteint la fin de la grille, vérifier si la solution est valide
        if row == 9:
            return self.grid.is_valid_solution()
            
        # Si on a atteint la fin d'une ligne, passer à la ligne suivante
        if col == 9:
            return self._solve_recursive(row + 1, 0)
            
        # Si la case est déjà remplie, passer à la case suivante
        if self.grid.grid[row][col] != 0:
            return self._solve_recursive(row, col + 1)
            
        # Force brute pure : essayer tous les nombres sans validation préalable
        for num in range(1, 10):
            self.grid.grid[row][col] = num
            if self._solve_recursive(row, col + 1):
                return True
            self.grid.grid[row][col] = 0
                
        return False 