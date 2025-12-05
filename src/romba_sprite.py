import pygame

class Roomba(pygame.sprite.Sprite):
    def __init__(self, empty_path):
        super().__init__()
        self.image = pygame.image.load('assets/roomba.png').convert_alpha()
        self.rect = self.image.get_rect(center=(60, 60))

        # Position needs to be a Vector2 for floating point math
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 3
        self.direction = pygame.math.Vector2(0, 0)

        # Path management
        self.path = []
        self.empty_path = empty_path

    def get_coord(self):
        col = self.rect.centerx // 32
        row = self.rect.centery // 32
        return (col, row)

    def set_path(self, path):
        self.path = []
        for point in path:
            if isinstance(point, pygame.math.Vector2):
                self.path.append(point)
            else:
                self.path.append(pygame.math.Vector2(point[0], point[1]))
        
        # Roomba'nın başlangıç noktasını listeden çıkarıyoruz ama
        # RRT bazen başlangıca çok yakın 2. bir nokta da üretebilir.
        # Bu yüzden burada pop(0) yapmak yerine update içinde dinamik kontrol daha güvenlidir.
        if self.path:
            # Sadece ilk nokta kesinlikle başlangıçsa çıkaralım
            if self.pos.distance_to(self.path[0]) < 1:
                self.path.pop(0)

    def update(self):
        # If we have a path, move towards the next point
        if self.path:
            target = self.path[0]
            
            # Vektörü hesapla
            vec_to_target = target - self.pos
            
            # --- HATA ÇÖZÜMÜ ---
            # Eğer vektörün uzunluğu 0 veya çok çok küçükse, zaten oradayız demektir.
            # Normalize etmeye çalışma, direkt o noktayı geç.
            if vec_to_target.length() < 0.1: 
                self.pos = target
                self.rect.center = self.pos
                self.path.pop(0)
                return # Bu frame'i bitir, sonraki frame yeni hedefe bakar

            # Move vector towards target
            self.direction = vec_to_target.normalize()
            
            # Check distance to the target
            distance = self.pos.distance_to(target)

            # If we are close enough to reach (or overshoot) the target in this frame
            if distance <= self.speed:
                # Snap exactly to the point
                self.pos = target
                self.rect.center = self.pos
                # Remove this point from the path and focus on the next one
                self.path.pop(0)
            else:
                # Otherwise, keep moving normally
                self.pos += self.direction * self.speed
                self.rect.center = round(self.pos.x), round(self.pos.y)
        
        else:
            # No path left, stop moving
            self.direction = pygame.math.Vector2(0, 0)
            self.empty_path()