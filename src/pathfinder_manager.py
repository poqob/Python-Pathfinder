import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from src.romba_sprite import Roomba
from src.rrt_algorithms import RRTGraph
from src.history_manager import HistoryManager # YENİ IMPORT

class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.select_surf = pygame.image.load('assets/selection.png').convert_alpha()
        
        self.current_algo = 'astar'
        self.path = []
        self.visited_tree = [] 

        self.roomba = pygame.sprite.GroupSingle(Roomba(self.empty_path))
        
        # --- HISTORY ENTENGRASYONU ---
        self.history_manager = HistoryManager()
        self.is_history_mode = False
        self.history_data = []
        self.current_history_index = 0

    def set_algorithm(self, algo_name):
        self.current_algo = algo_name
        self.is_history_mode = False # Algoritma değişirse canlı moda geç
        print(f"Algorithm switched to: {algo_name}")
        self.empty_path()

    def empty_path(self):
        self.path = []
        self.visited_tree = []

    # --- HISTORY KONTROLLERİ ---
    def toggle_history_mode(self):
        self.is_history_mode = not self.is_history_mode
        if self.is_history_mode:
            # Geçmişi yükle
            self.history_data = self.history_manager.load_history()
            if not self.history_data:
                print("No history found!")
                self.is_history_mode = False
                return
            self.current_history_index = len(self.history_data) - 1 # En son kaydı göster
            self.load_history_path()
        else:
            self.empty_path()

    def next_history(self):
        if self.is_history_mode and self.history_data:
            self.current_history_index = (self.current_history_index + 1) % len(self.history_data)
            self.load_history_path()

    def prev_history(self):
        if self.is_history_mode and self.history_data:
            self.current_history_index = (self.current_history_index - 1) % len(self.history_data)
            self.load_history_path()

    def load_history_path(self):
        """Seçili geçmiş kaydını ekrana ve Roomba'ya yükler"""
        entry = self.history_data[self.current_history_index]
        print(f"Viewing History: {entry['algorithm']} - {entry['timestamp']}")
        
        # JSON'dan gelen listeyi Vector2'ye çevir
        raw_path = entry['path']
        self.path = [pygame.math.Vector2(p[0], p[1]) for p in raw_path]
        
        # Roomba'yı hareket ettir (Opsiyonel: Sadece çizgi olarak görmek istersen burayı sil)
        self.roomba.sprite.pos = self.path[0] # Başlangıca ışınla
        self.roomba.sprite.set_path(self.path)

    # --- MEVCUT FONKSİYONLAR ---
    def draw_active_cell(self, screen):
        # History modundaysak fare imlecini çizme
        if self.is_history_mode: return

        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < screen.get_width() and mouse_pos[1] < screen.get_height():
            row = mouse_pos[1] // 32
            col = mouse_pos[0] // 32
            if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[0]):
                if self.matrix[row][col] == 1:
                    rect = pygame.Rect((col * 32, row * 32), (32, 32))
                    screen.blit(self.select_surf, rect)

    def create_path(self):
        # History modundaysak yeni yol oluşturma
        if self.is_history_mode: return

        start_pixel = self.roomba.sprite.rect.center
        mouse_pos = pygame.mouse.get_pos()
        
        end_x, end_y = mouse_pos[0] // 32, mouse_pos[1] // 32
        if not (0 <= end_y < len(self.matrix) and 0 <= end_x < len(self.matrix[0]) and self.matrix[end_y][end_x] == 1):
            return

        print(f"Calculating path using {self.current_algo}...")
        
        if self.current_algo == 'astar':
            self._run_astar(start_pixel, (end_x, end_y))
        elif self.current_algo == 'rrt':
            self._run_rrt(start_pixel, mouse_pos, use_star=False)
        elif self.current_algo == 'rrt_star':
            self._run_rrt(start_pixel, mouse_pos, use_star=True)
        
        # --- KAYDETME İŞLEMİ ---
        # Yol bulunduysa kaydet
        if self.path:
            self.history_manager.save_path(self.current_algo, self.path)

    def _run_astar(self, start_px, end_grid_pos):
        start_node = self.grid.node(start_px[0] // 32, start_px[1] // 32)
        end_node = self.grid.node(end_grid_pos[0], end_grid_pos[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path_nodes, _ = finder.find_path(start_node, end_node, self.grid)
        self.grid.cleanup()
        self.path = [pygame.math.Vector2(p.x * 32 + 16, p.y * 32 + 16) for p in path_nodes]
        self.roomba.sprite.set_path(self.path)

    def _run_rrt(self, start_pos, end_pos, use_star):
        map_dim = (len(self.matrix[0]) * 32, len(self.matrix) * 32)
        rrt = RRTGraph(start_pos, end_pos, map_dim, self.matrix)
        iterations = 2000 if use_star else 1000
        path_points = rrt.generate_rrt(max_iter=iterations, use_rrt_star=use_star)
        
        self.visited_tree = [] # Ağacı temizle (History modunda ağaç göstermiyoruz şimdilik)
        if not self.is_history_mode: # Sadece canlı modda ağacı göster
            for i, node in enumerate(rrt.nodes):
                parent_idx = rrt.parents[i]
                if parent_idx is not None:
                    self.visited_tree.append((rrt.nodes[parent_idx], node))

        self.path = [pygame.math.Vector2(p[0], p[1]) for p in path_points]
        self.roomba.sprite.set_path(self.path)

    def draw_path(self, screen):
        # Ağacı çiz
        if self.visited_tree and not self.is_history_mode:
            for edge in self.visited_tree:
                pygame.draw.line(screen, (100, 200, 100), edge[0], edge[1], 1)

        # Yolu çiz
        if self.path:
            # History modundaysa Mavi, değilse Gri çiz
            color = (0, 100, 255) if self.is_history_mode else '#4a4a4a'
            width = 8 if self.is_history_mode else 5
            
            points = [(p.x, p.y) for p in self.path]
            if len(points) > 1:
                pygame.draw.lines(screen, color, False, points, width)

    def select_history_entry(self, index):
        """UI'dan tıklanan spesifik bir history kaydını yükler"""
        if self.history_data and 0 <= index < len(self.history_data):
            self.current_history_index = index
            self.load_history_path()

    def update(self, screen):
        self.draw_active_cell(screen)
        self.draw_path(screen)
        self.roomba.update()
        self.roomba.draw(screen)