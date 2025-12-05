import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from src.romba_sprite import Roomba
from src.rrt_algorithms import RRTGraph # Yeni import

class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.select_surf = pygame.image.load('assets/selection.png').convert_alpha()
        
        # Algoritma Durumu: 'astar', 'rrt', 'rrt_star'
        self.current_algo = 'astar'
        
        self.path = []
        self.visited_tree = [] # RRT ağacını çizmek için

        self.roomba = pygame.sprite.GroupSingle(Roomba(self.empty_path))

    def set_algorithm(self, algo_name):
        self.current_algo = algo_name
        print(f"Algorithm switched to: {algo_name}")
        self.empty_path()

    def empty_path(self):
        self.path = []
        self.visited_tree = []

    def draw_active_cell(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < screen.get_width() and mouse_pos[1] < screen.get_height():
            row = mouse_pos[1] // 32
            col = mouse_pos[0] // 32
            if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[0]):
                if self.matrix[row][col] == 1:
                    rect = pygame.Rect((col * 32, row * 32), (32, 32))
                    screen.blit(self.select_surf, rect)

    def create_path(self):
        start_pixel = self.roomba.sprite.rect.center
        mouse_pos = pygame.mouse.get_pos()
        
        # Duvar kontrolü
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

    def _run_astar(self, start_px, end_grid_pos):
        # A* Grid tabanlı çalışır
        start_node = self.grid.node(start_px[0] // 32, start_px[1] // 32)
        end_node = self.grid.node(end_grid_pos[0], end_grid_pos[1])
        
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path_nodes, _ = finder.find_path(start_node, end_node, self.grid)
        self.grid.cleanup()
        
        # Roomba'ya vermeden önce Node objelerini vektöre çevir
        # (Roomba sınıfında zaten çevirici var ama format tutarlılığı için)
        # Buradaki path Roomba'ya GridNode olarak gidiyor, Roomba onu çeviriyor.
        # RRT'de ise direkt koordinat gönderiyoruz.
        # Bu yüzden Roomba sınıfı her ikisini de kabul edecek şekilde düzenlenmeli
        # VEYA burada A* sonucunu da koordinat listesine çevirelim:
        
        self.path = [pygame.math.Vector2(p.x * 32 + 16, p.y * 32 + 16) for p in path_nodes]
        self.roomba.sprite.set_path(self.path)

    def _run_rrt(self, start_pos, end_pos, use_star):
        # RRT Piksel tabanlı çalışır
        map_dim = (len(self.matrix[0]) * 32, len(self.matrix) * 32)
        
        # RRTGraph sınıfını başlat
        rrt = RRTGraph(start_pos, end_pos, map_dim, self.matrix)
        
        # Yolu oluştur (RRT* için 2000 iterasyon verelim ki iyileşsin)
        iterations = 2000 if use_star else 1000
        path_points = rrt.generate_rrt(max_iter=iterations, use_rrt_star=use_star)
        
        # Görselleştirme için ağacı al
        self.visited_tree = []
        for i, node in enumerate(rrt.nodes):
            parent_idx = rrt.parents[i]
            if parent_idx is not None:
                parent = rrt.nodes[parent_idx]
                self.visited_tree.append((parent, node))

        # Yolu Roomba'ya gönder (Vector2 listesi olarak)
        self.path = [pygame.math.Vector2(p[0], p[1]) for p in path_points]
        self.roomba.sprite.set_path(self.path)

    def draw_path(self, screen):
        # Önce RRT Ağacını çiz (Varsa)
        if self.visited_tree:
            for edge in self.visited_tree:
                pygame.draw.line(screen, (100, 200, 100), edge[0], edge[1], 1) # Yeşil ince çizgiler

        # Asıl yolu çiz
        if self.path:
            points = [(p.x, p.y) for p in self.path]
            if len(points) > 1:
                pygame.draw.lines(screen, '#4a4a4a', False, points, 5)

    def update(self, screen):
        self.draw_active_cell(screen)
        self.draw_path(screen)
        self.roomba.update()
        self.roomba.draw(screen)