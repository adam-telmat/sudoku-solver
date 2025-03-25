"""
Module contenant l'interface graphique du solveur de Sudoku utilisant Pygame.
"""

import pygame
import sys

class SudokuGUI:
    """Classe gérant l'interface graphique du solveur de Sudoku."""
    
    def __init__(self, solved_grid, original_grid):
        """Initialise l'interface graphique.
        
        Args:
            solved_grid (Grid): La grille résolue
            original_grid (Grid): La grille originale
        """
        pygame.init()
        
        # Constantes
        self.CELL_SIZE = 60
        self.GRID_SIZE = 9
        self.WINDOW_SIZE = self.CELL_SIZE * self.GRID_SIZE
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.BLUE = (0, 0, 255)
        
        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Solveur de Sudoku")
        
        # Polices
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30)
        
        # Grilles
        self.solved_grid = solved_grid
        self.original_grid = original_grid
    
    def draw_grid(self):
        """Dessine la grille de Sudoku."""
        # Remplir le fond
        self.screen.fill(self.WHITE)
        
        # Dessiner les lignes
        for i in range(self.GRID_SIZE + 1):
            # Lignes horizontales
            pygame.draw.line(self.screen, self.BLACK,
                           (0, i * self.CELL_SIZE),
                           (self.WINDOW_SIZE, i * self.CELL_SIZE),
                           2 if i % 3 == 0 else 1)
            
            # Lignes verticales
            pygame.draw.line(self.screen, self.BLACK,
                           (i * self.CELL_SIZE, 0),
                           (i * self.CELL_SIZE, self.WINDOW_SIZE),
                           2 if i % 3 == 0 else 1)
        
        # Remplir les cellules
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                value = self.solved_grid.grid[i][j]
                if value != 0:
                    # Choisir la couleur en fonction de si c'est une valeur originale
                    color = self.BLUE if self.original_grid.original[i][j] else self.BLACK
                    
                    # Créer le texte
                    text = self.font.render(str(value), True, color)
                    
                    # Centrer le texte dans la cellule
                    text_rect = text.get_rect(center=(
                        j * self.CELL_SIZE + self.CELL_SIZE // 2,
                        i * self.CELL_SIZE + self.CELL_SIZE // 2
                    ))
                    
                    # Afficher le texte
                    self.screen.blit(text, text_rect)
    
    def run(self):
        """Lance l'interface graphique."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.draw_grid()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit() 