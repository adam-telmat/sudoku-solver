"""
Module contenant la classe Grid pour représenter une grille de Sudoku.
"""

class Grid:
    """Classe représentant une grille de Sudoku."""
    
    def __init__(self):
        """Initialise une grille vide de 9x9."""
        self.size = 9
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.original = [[False for _ in range(self.size)] for _ in range(self.size)]
    
    def load_from_file(self, file_path):
        """Charge une grille depuis un fichier texte.
        
        Args:
            file_path (str): Chemin vers le fichier contenant la grille
        """
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        for i in range(self.size):
            line = lines[i].strip()
            for j in range(self.size):
                if line[j] == '_':
                    self.grid[i][j] = 0
                else:
                    self.grid[i][j] = int(line[j])
                    self.original[i][j] = True
    
    def is_valid(self, row, col, num):
        """Vérifie si un nombre peut être placé à la position donnée.
        
        Args:
            row (int): Index de la ligne
            col (int): Index de la colonne
            num (int): Nombre à vérifier
            
        Returns:
            bool: True si le placement est valide, False sinon
        """
        # Vérification de la ligne
        for x in range(self.size):
            if self.grid[row][x] == num:
                return False
                
        # Vérification de la colonne
        for x in range(self.size):
            if self.grid[x][col] == num:
                return False
                
        # Vérification du bloc 3x3
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
                    
        return True
    
    def find_empty(self):
        """Trouve une case vide dans la grille.
        
        Returns:
            tuple: (row, col) de la case vide, ou None si la grille est pleine
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
    
    def copy(self):
        """Crée une copie profonde de la grille.
        
        Returns:
            Grid: Une nouvelle instance de Grid avec les mêmes valeurs
        """
        new_grid = Grid()
        new_grid.grid = [row[:] for row in self.grid]
        new_grid.original = [row[:] for row in self.original]
        return new_grid
    
    def print(self, highlight_original=False):
        """Affiche la grille dans le terminal.
        
        Args:
            highlight_original (bool): Si True, met en évidence les chiffres originaux
        """
        for i in range(self.size):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
            for j in range(self.size):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                if self.grid[i][j] == 0:
                    print("_", end=" ")
                else:
                    if highlight_original and self.original[i][j]:
                        print(f"\033[1m{self.grid[i][j]}\033[0m", end=" ")
                    else:
                        print(self.grid[i][j], end=" ")
            print()
    
    def is_valid_solution(self):
        """Vérifie si la grille complète est une solution valide.
        
        Returns:
            bool: True si la grille est une solution valide, False sinon
        """
        # Vérifier chaque ligne
        for row in range(9):
            if not self._is_valid_line(row):
                return False
                
        # Vérifier chaque colonne
        for col in range(9):
            if not self._is_valid_column(col):
                return False
                
        # Vérifier chaque bloc 3x3
        for block_row in range(0, 9, 3):
            for block_col in range(0, 9, 3):
                if not self._is_valid_block(block_row, block_col):
                    return False
                    
        return True
    
    def _is_valid_line(self, row):
        """Vérifie si une ligne contient tous les chiffres de 1 à 9.
        
        Args:
            row (int): Index de la ligne à vérifier
            
        Returns:
            bool: True si la ligne est valide, False sinon
        """
        seen = [False] * 10
        for col in range(9):
            num = self.grid[row][col]
            if num == 0 or seen[num]:
                return False
            seen[num] = True
        return True
    
    def _is_valid_column(self, col):
        """Vérifie si une colonne contient tous les chiffres de 1 à 9.
        
        Args:
            col (int): Index de la colonne à vérifier
            
        Returns:
            bool: True si la colonne est valide, False sinon
        """
        seen = [False] * 10
        for row in range(9):
            num = self.grid[row][col]
            if num == 0 or seen[num]:
                return False
            seen[num] = True
        return True
    
    def _is_valid_block(self, start_row, start_col):
        """Vérifie si un bloc 3x3 contient tous les chiffres de 1 à 9.
        
        Args:
            start_row (int): Index de la première ligne du bloc
            start_col (int): Index de la première colonne du bloc
            
        Returns:
            bool: True si le bloc est valide, False sinon
        """
        seen = [False] * 10
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                num = self.grid[row][col]
                if num == 0 or seen[num]:
                    return False
                seen[num] = True
        return True 