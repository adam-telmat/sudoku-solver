"""
Module contenant l'implémentation de l'algorithme de backtracking pour résoudre le Sudoku.
"""

import time
import pygame

class Backtracking:
    """Classe implémentant l'algorithme de backtracking pour résoudre le Sudoku."""
    
    def __init__(self, grid):
        """Initialise le solveur avec une grille.
        
        Args:
            grid (Grid): La grille à résoudre
        """
        self.grid = grid
        self.animation_callback = None
        self.animation_speed = 0.1  # Temps d'attente en secondes
        self.animate = False
    
    def set_animation(self, callback, animate=True, speed=0.1):
        """Active l'animation et définit la fonction de rappel.
        
        Args:
            callback (function): Fonction appelée à chaque étape de l'algorithme
            animate (bool): Si True, active l'animation
            speed (float): Vitesse de l'animation (délai en secondes)
        """
        self.animation_callback = callback
        self.animate = animate
        self.animation_speed = speed
    
    def wait_without_blocking(self, seconds):
        """Attend le nombre de secondes spécifié sans bloquer l'interface.
        
        Args:
            seconds (float): Temps d'attente en secondes
            
        Returns:
            bool: True si l'attente s'est terminée normalement, False sinon
        """
        try:
            import pygame
            start_time = time.time()
            running = True
            while running and time.time() - start_time < seconds:
                # Traiter les événements pendant l'attente
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return False
                
                # Courte pause pour ne pas surcharger le CPU
                pygame.time.wait(10)  # 10ms pause
        except (ImportError, AttributeError, pygame.error):
            # Si pygame n'est pas disponible ou pas initialisé, utiliser time.sleep
            time.sleep(seconds)
        
        return True  # Retourner True si l'attente s'est terminée normalement
    
    def solve(self):
        """Résout la grille en utilisant le backtracking.
        
        Returns:
            bool: True si une solution a été trouvée, False sinon
        """
        try:
            import pygame
            # Vérifier les événements pour permettre de quitter
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
        except (ImportError, AttributeError, pygame.error):
            # Si pygame n'est pas disponible ou pas initialisé, ignorer
            pass
        
        empty = self.grid.find_empty()
        if not empty:
            return True
            
        row, col = empty
        
        for num in range(1, 10):
            if self.grid.is_valid(row, col, num):
                self.grid.grid[row][col] = num
                
                # Animation: montrer le placement d'un chiffre
                if self.animate and self.animation_callback:
                    self.animation_callback(row, col, num, "place")
                    if not self.wait_without_blocking(self.animation_speed):
                        return False
                
                if self.solve():
                    return True
                    
                self.grid.grid[row][col] = 0
                
                # Animation: montrer l'effacement (backtracking)
                if self.animate and self.animation_callback:
                    self.animation_callback(row, col, 0, "remove")
                    if not self.wait_without_blocking(self.animation_speed):
                        return False
                
        return False 