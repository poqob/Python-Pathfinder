import pygame
import random
import math

class RRTGraph:
    def __init__(self, start, end, map_dimensions, matrix, step_size=30, search_radius=50):
        self.start = start
        self.end = end
        self.map_w, self.map_h = map_dimensions
        self.matrix = matrix
        
        # Ağaç yapısı: nodes = [(x, y)], parents = {child_index: parent_index}
        self.nodes = [start]
        self.parents = {0: None}
        self.costs = {0: 0} # RRT* için maliyet tutuyoruz
        
        self.goal_reached_index = None
        self.step_size = step_size
        self.search_radius = search_radius # RRT* için komşu arama yarıçapı

    def get_random_point(self):
        # %10 ihtimalle direkt hedefe gitmeye çalış (Bias)
        if random.randint(0, 100) < 10:
            return self.end
        return (random.randint(0, self.map_w), random.randint(0, self.map_h))

    def get_nearest_node_index(self, point):
        min_dist = float('inf')
        idx = -1
        for i, node in enumerate(self.nodes):
            dist = math.hypot(node[0] - point[0], node[1] - point[1])
            if dist < min_dist:
                min_dist = dist
                idx = i
        return idx

    def steer(self, from_point, to_point):
        dist = math.hypot(to_point[0] - from_point[0], to_point[1] - from_point[1])
        
        # Eğer hedef nokta adım mesafesinden yakınsa direkt orayı al
        if dist < self.step_size:
            return to_point
        
        # Değilse, o yöne doğru 'step_size' kadar ilerle
        theta = math.atan2(to_point[1] - from_point[1], to_point[0] - from_point[0])
        new_x = from_point[0] + self.step_size * math.cos(theta)
        new_y = from_point[1] + self.step_size * math.sin(theta)
        return (new_x, new_y)

    def is_collision_free(self, p1, p2):
        # İki nokta arasına örnekleme yap (Line Sampling)
        dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        steps = int(dist // 5) # Her 5 pikselde bir kontrol et
        
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            x = p1[0] + (p2[0] - p1[0]) * t
            y = p1[1] + (p2[1] - p1[1]) * t
            
            # Pikseli matris indexine çevir
            col = int(x // 32)
            row = int(y // 32)
            
            # Sınır kontrolü ve Duvar Kontrolü (0 = Duvar)
            if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[0]):
                if self.matrix[row][col] == 0:
                    return False
            else:
                return False # Harita dışı
        return True

    def generate_rrt(self, max_iter=1000, use_rrt_star=False):
        for _ in range(max_iter):
            rand_point = self.get_random_point()
            nearest_idx = self.get_nearest_node_index(rand_point)
            nearest_node = self.nodes[nearest_idx]
            
            new_node = self.steer(nearest_node, rand_point)
            
            if self.is_collision_free(nearest_node, new_node):
                new_cost = self.costs[nearest_idx] + math.hypot(new_node[0]-nearest_node[0], new_node[1]-nearest_node[1])
                
                # --- RRT* MANTIĞI ---
                parent_idx = nearest_idx
                if use_rrt_star:
                    # Yakındaki düğümleri bul ve daha ucuz bir parent var mı bak
                    min_cost = new_cost
                    nearby_indices = [i for i, n in enumerate(self.nodes) if math.hypot(n[0]-new_node[0], n[1]-new_node[1]) <= self.search_radius]
                    
                    for i in nearby_indices:
                        if self.is_collision_free(self.nodes[i], new_node):
                            potential_cost = self.costs[i] + math.hypot(new_node[0]-self.nodes[i][0], new_node[1]-self.nodes[i][1])
                            if potential_cost < min_cost:
                                min_cost = potential_cost
                                parent_idx = i
                                new_cost = min_cost

                # Düğümü ekle
                self.nodes.append(new_node)
                new_idx = len(self.nodes) - 1
                self.parents[new_idx] = parent_idx
                self.costs[new_idx] = new_cost

                # RRT* Rewiring (Yeniden Bağlama)
                if use_rrt_star:
                    for i in nearby_indices:
                        if i != parent_idx: # Kendisi hariç
                            dist_to_neighbor = math.hypot(new_node[0]-self.nodes[i][0], new_node[1]-self.nodes[i][1])
                            if new_cost + dist_to_neighbor < self.costs[i] and self.is_collision_free(new_node, self.nodes[i]):
                                self.parents[i] = new_idx
                                self.costs[i] = new_cost + dist_to_neighbor

                # Hedefe ulaştık mı?
                if math.hypot(new_node[0] - self.end[0], new_node[1] - self.end[1]) < 20:
                    self.goal_reached_index = new_idx
                    # RRT ise ilk bulduğunda dur, RRT* ise süre bitene kadar optimize et
                    if not use_rrt_star: 
                        break 
        
        return self.trace_path()

    def trace_path(self):
        # Sondan başa doğru parentleri takip et
        path = []
        if self.goal_reached_index is not None:
            curr = self.goal_reached_index
            while curr is not None:
                path.append(self.nodes[curr])
                curr = self.parents[curr]
            path.reverse()
        return path