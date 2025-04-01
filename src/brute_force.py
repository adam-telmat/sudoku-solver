"""
Module contenant l'implémentation de l'algorithme de force brute pour résoudre le Sudoku.
"""

import time
import pygame
import sys

class BruteForce:
    """Classe implémentant l'algorithme de force brute pour résoudre le Sudoku."""
    
    def __init__(self, grid):
        """Initialise le solveur avec une grille.
        
        Args:
            grid (Grid): La grille à résoudre
        """
        self.grid = grid
        self.solutions = []
        self.attempts = 0  # Compteur de tentatives
        self.animation_callback = None
        self.animate = False
        self.animation_speed = 0.05
        self.max_attempts_to_show = 10000  # Limite d'affichage pour ne pas ralentir trop
        self.animation_frequency = 10  # N'afficher qu'une tentative sur X (pour la force brute)
    
    def set_animation(self, callback, animate=True, speed=0.05):
        """Active l'animation et définit la fonction de rappel.
        
        Args:
            callback (function): Fonction appelée à chaque étape de l'algorithme
            animate (bool): Si True, active l'animation
            speed (float): Vitesse de l'animation (délai en secondes)
        """
        self.animation_callback = callback
        self.animate = animate
        self.animation_speed = speed
    
    def process_events(self):
        """Traite les événements pygame pour garder l'interface réactive."""
        try:
            import pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return False
        except (ImportError, AttributeError, pygame.error):
            # Si pygame n'est pas disponible ou pas initialisé, ignorer
            pass
        return True
    
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
                running = self.process_events()
                if not running:
                    break
                    
                # Courte pause pour ne pas surcharger le CPU
                pygame.time.wait(5)  # Réduit à 5ms pour être plus réactif
        except (ImportError, AttributeError, pygame.error):
            # Si pygame n'est pas disponible ou pas initialisé, utiliser time.sleep
            time.sleep(seconds)
        
        return True
    
    def solve(self):
        """Résout la grille en utilisant la force brute.
        
        Returns:
            bool: True si une solution a été trouvée, False sinon
        """
        self.attempts = 0  # Réinitialiser le compteur
        return self._solve_recursive(0, 0)
    
    def _solve_recursive(self, row, col):
        """Résout récursivement la grille en essayant toutes les combinaisons possibles.
        
        Args:
            row (int): Index de la ligne actuelle
            col (int): Index de la colonne actuelle
            
        Returns:
            bool: True si une solution a été trouvée, False sinon
        """
        # Vérifier périodiquement les événements même sans animation
        if self.attempts % 1000 == 0:
            if not self.process_events():
                return False  # Permettre d'annuler la résolution

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
            self.attempts += 1  # Incrémenter le compteur de tentatives
            
            # Si on dépasse la limite d'affichage et que l'animation est activée, 
            # arrêter l'animation et interrompre la résolution
            if self.attempts > self.max_attempts_to_show and self.animate and self.animation_callback:
                self.animation_callback(0, 0, 0, "finished", self.attempts)
                # Arrêter complètement la résolution et revenir au menu
                return False
            
            self.grid.grid[row][col] = num
            
            # Animation: montrer le placement d'un chiffre (limitée et avec fréquence réduite)
            if self.animate and self.animation_callback and self.attempts <= self.max_attempts_to_show:
                # N'afficher qu'une tentative sur X pour la force brute (pour fluidité)
                if self.attempts % self.animation_frequency == 0:
                    self.animation_callback(row, col, num, "place", self.attempts)
                    if not self.wait_without_blocking(self.animation_speed):
                        return False  # Permettre d'annuler l'animation
            
            if self._solve_recursive(row, col + 1):
                return True
                
            self.grid.grid[row][col] = 0
            
            # Animation: montrer l'effacement (limité et avec fréquence réduite)
            if self.animate and self.animation_callback and self.attempts <= self.max_attempts_to_show:
                # N'afficher qu'une tentative sur X pour la force brute (pour fluidité)
                if self.attempts % self.animation_frequency == 0:
                    self.animation_callback(row, col, 0, "remove", self.attempts)
                    if not self.wait_without_blocking(self.animation_speed):
                        return False  # Permettre d'annuler l'animation
                
        return False 