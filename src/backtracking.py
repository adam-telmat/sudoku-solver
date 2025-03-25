"""
Module contenant l'implémentation de l'algorithme de backtracking pour résoudre le Sudoku.
"""

class Backtracking:
    """Classe implémentant l'algorithme de backtracking pour résoudre le Sudoku."""
    
    def __init__(self, grid):
        """Initialise le solveur avec une grille.
        
        Args:
            grid (Grid): La grille à résoudre
        """
        self.grid = grid
    
    def solve(self):
        """Résout la grille en utilisant le backtracking.
        
        Returns:
            bool: True si une solution a été trouvée, False sinon
        """
        empty = self.grid.find_empty()
        if not empty:
            return True
            
        row, col = empty
        
        for num in range(1, 10):
            if self.grid.is_valid(row, col, num):
                self.grid.grid[row][col] = num
                
                if self.solve():
                    return True
                    
                self.grid.grid[row][col] = 0
                
        return False 