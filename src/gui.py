"""
Module contenant l'interface graphique du solveur de Sudoku utilisant Pygame.
"""

import pygame
import sys
import time
from src.backtracking import Backtracking
from src.brute_force import BruteForce

class SudokuGUI:
    """Classe gérant l'interface graphique du solveur de Sudoku."""
    
    def __init__(self, solved_grid=None, original_grid=None, algorithm_name=None):
        """Initialise l'interface graphique.
        
        Args:
            solved_grid (Grid, optional): La grille résolue
            original_grid (Grid, optional): La grille originale
            algorithm_name (str, optional): Le nom de l'algorithme ("backtracking" ou "brute_force")
        """
        pygame.init()
        
        # Constantes
        self.CELL_SIZE = 60
        self.GRID_SIZE = 9
        self.GRID_WIDTH = self.CELL_SIZE * self.GRID_SIZE
        self.WINDOW_WIDTH = self.GRID_WIDTH + 220  # Augmenté pour les textes plus longs
        self.WINDOW_HEIGHT = self.GRID_WIDTH + 100  # Espace pour les boutons en bas
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.HIGHLIGHT = (255, 255, 0, 128)  # Jaune semi-transparent
        
        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Solveur de Sudoku")
        
        # Polices
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 30)
        self.stats_font = pygame.font.Font(None, 24)
        
        # Grilles
        self.solved_grid = solved_grid
        self.original_grid = original_grid
        self.current_grid = None
        
        # État de l'animation
        self.animation_active = False
        self.highlight_cell = None
        self.highlight_color = self.GREEN
        self.animation_grid = None
        self.algorithm_type = algorithm_name  # Utilisez le nom d'algorithme fourni
        self.attempts = 0
        self.max_attempts_to_show = 10000  # Limite d'affichage pour l'animation
    
    def draw_grid(self):
        """Dessine la grille de Sudoku."""
        # Remplir le fond
        self.screen.fill(self.WHITE)
        
        # Dessiner la grille
        grid_area = pygame.Rect(0, 0, self.GRID_WIDTH, self.GRID_WIDTH)
        pygame.draw.rect(self.screen, self.WHITE, grid_area)
        
        # Dessiner les lignes
        for i in range(self.GRID_SIZE + 1):
            # Lignes horizontales
            pygame.draw.line(self.screen, self.BLACK,
                           (0, i * self.CELL_SIZE),
                           (self.GRID_WIDTH, i * self.CELL_SIZE),
                           2 if i % 3 == 0 else 1)
            
            # Lignes verticales
            pygame.draw.line(self.screen, self.BLACK,
                           (i * self.CELL_SIZE, 0),
                           (i * self.CELL_SIZE, self.GRID_WIDTH),
                           2 if i % 3 == 0 else 1)
        
        # Déterminer quelle grille afficher
        grid_to_display = self.animation_grid if self.animation_active else self.solved_grid
        
        # Remplir les cellules
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                # Dessiner la cellule en surbrillance si nécessaire
                if self.highlight_cell and self.highlight_cell == (i, j):
                    pygame.draw.rect(self.screen, self.highlight_color, 
                                   (j * self.CELL_SIZE, i * self.CELL_SIZE, 
                                    self.CELL_SIZE, self.CELL_SIZE))
                
                # Afficher les chiffres
                value = grid_to_display.grid[i][j] if grid_to_display else 0
                if value != 0:
                    # Choisir la couleur en fonction de si c'est une valeur originale
                    is_original = self.original_grid and self.original_grid.original[i][j]
                    color = self.BLUE if is_original else self.BLACK
                    
                    # Créer le texte
                    text = self.font.render(str(value), True, color)
                    
                    # Centrer le texte dans la cellule
                    text_rect = text.get_rect(center=(
                        j * self.CELL_SIZE + self.CELL_SIZE // 2,
                        i * self.CELL_SIZE + self.CELL_SIZE // 2
                    ))
                    
                    # Afficher le texte
                    self.screen.blit(text, text_rect)
        
        # Dessiner les statistiques dans la barre latérale
        self.draw_stats()
    
    def draw_stats(self):
        """Affiche les statistiques dans la barre latérale"""
        # Zone des statistiques
        stats_area = pygame.Rect(self.GRID_WIDTH, 0, 220, self.GRID_WIDTH)
        pygame.draw.rect(self.screen, self.GRAY, stats_area)
        pygame.draw.line(self.screen, self.BLACK, 
                       (self.GRID_WIDTH, 0), 
                       (self.GRID_WIDTH, self.GRID_WIDTH), 2)
        
        # Titre
        title = self.title_font.render("Statistiques", True, self.BLACK)
        title_rect = title.get_rect(center=(self.GRID_WIDTH + 110, 30))
        self.screen.blit(title, title_rect)
        
        # Nom de l'algorithme sur deux lignes si nécessaire
        algo_name = "Backtracking" if self.algorithm_type == "backtracking" else "Force Brute"
        algo_font = pygame.font.Font(None, 28)
        
        # D'abord afficher "Algorithme:"
        algo_label = algo_font.render("Algorithme:", True, self.BLACK)
        self.screen.blit(algo_label, (self.GRID_WIDTH + 20, 60))
        
        # Puis afficher le nom de l'algorithme en dessous
        algo_value = algo_font.render(algo_name, True, self.BLACK)
        self.screen.blit(algo_value, (self.GRID_WIDTH + 40, 90))
        
        # Nombre de tentatives seulement pour force brute
        if self.algorithm_type == "brute_force":
            attempts_text = self.stats_font.render(f"Tentatives: {self.attempts}", True, self.BLACK)
            self.screen.blit(attempts_text, (self.GRID_WIDTH + 20, 120))
        
        # Si on utilise la force brute et qu'on a atteint la limite, l'indiquer
        if self.algorithm_type == "brute_force" and self.attempts > 10000:
            limit_text = self.small_font.render("(Animation limitée à 10000)", True, self.ORANGE)
            y_pos = 150 if self.algorithm_type == "brute_force" else 120
            self.screen.blit(limit_text, (self.GRID_WIDTH + 20, y_pos))
        
        # Instructions avec retours à la ligne pour tenir dans la zone
        instructions = [
            "Fermez la fenêtre",
            "et appuyez sur Entrée",
            "pour continuer."
        ]
        
        for i, instruction in enumerate(instructions):
            line = self.small_font.render(instruction, True, self.BLACK)
            y_pos = 180 + i * 25
            if self.algorithm_type == "brute_force" and self.attempts > 10000:
                y_pos += 30  # Décaler vers le bas si l'avertissement de limite est affiché
            elif self.algorithm_type == "backtracking":
                y_pos = 120 + i * 25  # Positionner plus haut pour le backtracking
            self.screen.blit(line, (self.GRID_WIDTH + 20, y_pos))
    
    def draw_buttons(self):
        """Dessine les boutons de navigation."""
        # Zone des boutons (juste pour le séparateur)
        buttons_area = pygame.Rect(0, self.GRID_WIDTH, self.WINDOW_WIDTH, 100)
        pygame.draw.rect(self.screen, self.GRAY, buttons_area)
        pygame.draw.line(self.screen, self.BLACK, 
                       (0, self.GRID_WIDTH), 
                       (self.WINDOW_WIDTH, self.GRID_WIDTH), 2)
        
        # Diviser l'instruction en deux lignes pour qu'elle tienne dans la fenêtre
        instruction_lines = ["Fermez la fenêtre et appuyez", "sur Entrée pour continuer"]
        for i, line in enumerate(instruction_lines):
            text = self.font.render(line, True, self.BLACK)
            rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH + 30 + i * 30))
            self.screen.blit(text, rect)
    
    def animation_callback(self, row, col, value, action, attempts=None):
        """Fonction de rappel pour l'animation du backtracking.
        
        Args:
            row (int): Index de la ligne
            col (int): Index de la colonne
            value (int): Valeur placée ou retirée
            action (str): Action effectuée ("place", "remove" ou "finished")
            attempts (int, optional): Nombre de tentatives effectuées
        """
        if attempts is not None:
            self.attempts = attempts
            
        if action == "finished":
            # Afficher un message indiquant que l'animation est terminée
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))  # Fond semi-transparent
            
            warning_font = pygame.font.Font(None, 36)
            warning_text = warning_font.render("Animation interrompue", True, self.ORANGE)
            warning_rect = warning_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2 - 50))
            
            info_font = pygame.font.Font(None, 24)
            info_lines = [
                f"Limite de {self.max_attempts_to_show} tentatives atteinte.",
                "La force brute nécessiterait trop de temps.",
                "Cliquez n'importe où ou appuyez",
                "sur une touche pour continuer."
            ]
            
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(warning_text, warning_rect)
            
            for i, line in enumerate(info_lines):
                info_text = info_font.render(line, True, self.BLACK)
                info_rect = info_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2 - 10 + i * 30))
                self.screen.blit(info_text, info_rect)
            
            pygame.display.flip()
            
            # Permettre de quitter immédiatement quand le message est affiché
            self._allow_quit_after_animation()
            return
        
        self.highlight_cell = (row, col)
        self.highlight_color = self.GREEN if action == "place" else self.RED
        
        # Dessiner la grille
        self.draw_grid()
        pygame.display.flip()
    
    def _allow_quit_after_animation(self):
        """Boucle d'événements qui permet de quitter quand l'animation est terminée."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    return True
            
            # Courte pause pour éviter d'utiliser trop de CPU
            pygame.time.wait(100)
    
    def show_animation(self, grid, algorithm_type="backtracking"):
        """Affiche une animation du processus de résolution.
        
        Args:
            grid (Grid): La grille à résoudre
            algorithm_type (str): Type d'algorithme à utiliser ("backtracking" ou "brute_force")
            
        Returns:
            bool: True si la grille a été résolue, False sinon
        """
        self.animation_active = True
        self.animation_grid = grid.copy()
        self.original_grid = grid.copy()
        self.algorithm_type = algorithm_type
        self.attempts = 0
        
        # Créer le solveur approprié
        if algorithm_type == "backtracking":
            solver = Backtracking(self.animation_grid)
            speed = 0.05
        else:  # force brute
            solver = BruteForce(self.animation_grid)
            speed = 0.01  # Plus rapide pour la force brute car il y a beaucoup plus d'étapes
        
        # Vérifier les événements pendant l'animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        solver.set_animation(self.animation_callback, animate=True, speed=speed)
        
        # Lancer la résolution
        return solver.solve()
    
    def wait_without_blocking(self, seconds):
        """Attend le nombre de secondes spécifié sans bloquer l'interface.
        
        Args:
            seconds (float): Temps d'attente en secondes
        """
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
            # Redessiner la grille pour maintenir l'affichage à jour
            self.draw_grid()
            pygame.display.flip()
        
        return True  # Toujours retourner True si l'attente est terminée normalement
    
    def run(self):
        """Lance l'interface graphique."""
        running = True
        
        while running:
            # Dessiner la grille et les instructions
            self.draw_grid()
            self.draw_buttons()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        running = False
        
        return "QUIT"
    
    def run_with_animation(self, grid, algorithm_type="backtracking"):
        """Lance l'interface graphique avec animation de la résolution.
        
        Args:
            grid (Grid): La grille à résoudre
            algorithm_type (str): Type d'algorithme à utiliser ("backtracking" ou "brute_force")
            
        Returns:
            str: "QUIT" pour quitter
        """
        # Configuration de la vitesse selon l'algorithme
        speed = 0.02 if algorithm_type == "backtracking" else 0.001  # Force brute beaucoup plus rapide
        
        # Dessiner la grille initiale
        self.original_grid = grid.copy()
        self.animation_grid = grid.copy()
        self.animation_active = True
        self.algorithm_type = algorithm_type
        
        self.draw_grid()
        pygame.display.flip()
        
        # Vérifier les événements pour détecter la fermeture de la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "QUIT"
        
        # Ajouter des instructions spécifiques pour la force brute
        if algorithm_type == "brute_force":
            # Montrer un avertissement pour la force brute
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))  # Fond semi-transparent
            
            warning_font = pygame.font.Font(None, 36)
            warning_text = warning_font.render("Animation de Force Brute", True, self.BLACK)
            warning_rect = warning_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2 - 50))
            
            info_font = pygame.font.Font(None, 24)
            info_lines = [
                "L'animation est limitée aux 10000",
                "premières tentatives et n'affiche",
                "qu'une tentative sur 10 pour rester fluide.",
                "",
                "La force brute peut prendre du temps.",
                "Pour arrêter, fermez la fenêtre",
                "et appuyez sur Entrée dans le terminal."
            ]
            
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(warning_text, warning_rect)
            
            for i, line in enumerate(info_lines):
                info_text = info_font.render(line, True, self.BLACK)
                info_rect = info_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2 - 10 + i * 30))
                self.screen.blit(info_text, info_rect)
            
            pygame.display.flip()
            
            # Attendre que l'utilisateur appuie sur une touche pour commencer
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return "QUIT"
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
        
        # Attendre un peu pour que l'utilisateur voie la grille initiale
        if not self.wait_without_blocking(1):
            return "QUIT"
        
        # Lancer l'animation
        solved = self.show_animation(grid, algorithm_type)
        
        # Si résolu, mettre à jour la grille résolue
        if solved:
            self.solved_grid = self.animation_grid
            self.highlight_cell = None
            
            # Afficher "Sudoku Résolu !" pendant quelques secondes
            font = pygame.font.Font(None, 60)
            text = font.render("Sudoku Résolu !", True, self.GREEN)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2))
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, text_rect)
            
            # Afficher le nombre total de tentatives
            attempts_text = self.title_font.render(f"Nombre de tentatives: {self.attempts}", True, self.BLACK)
            attempts_rect = attempts_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2 + 50))
            self.screen.blit(attempts_text, attempts_rect)
            
            # Instructions divisées en lignes
            lines = ["Fermez la fenêtre", "et appuyez sur Entrée", "pour continuer"]
            for i, line in enumerate(lines):
                instruction_text = self.small_font.render(line, True, self.BLACK)
                instruction_rect = instruction_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2 + 80 + i * 25))
                self.screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            
            # Attendre jusqu'à ce que l'utilisateur ferme la fenêtre
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return "QUIT"
                
                pygame.time.wait(10)
        else:
            # En cas d'échec (rare avec les grilles valides)
            font = pygame.font.Font(None, 60)
            text = font.render("Impossible à résoudre", True, self.RED)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2))
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, text_rect)
            
            # Instructions divisées en lignes
            lines = ["Fermez la fenêtre", "et appuyez sur Entrée", "pour continuer"]
            for i, line in enumerate(lines):
                instruction_text = self.small_font.render(line, True, self.BLACK)
                instruction_rect = instruction_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.GRID_WIDTH // 2 + 80 + i * 25))
                self.screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            
            # Attendre jusqu'à ce que l'utilisateur ferme la fenêtre
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return "QUIT"
                
                pygame.time.wait(10)
        
        # Continuer l'interface normale
        self.animation_active = False
        return "QUIT" 