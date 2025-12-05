import pygame

class UIManager:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        
        # Ayarlar
        self.SIDEBAR_WIDTH = 300
        self.ITEM_HEIGHT = 60
        self.SCROLL_SPEED = 20
        
        # Durum
        self.scroll_y = 0
        
        # Fontlar
        pygame.font.init()
        self.font_title = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_detail = pygame.font.SysFont('Arial', 14)

    def handle_sidebar_click(self, pos, pathfinder):
        """Yan panele tıklanma mantığı"""
        mouse_x, mouse_y = pos
        
        # Tıklama sidebar içinde mi?
        if mouse_x > self.width - self.SIDEBAR_WIDTH:
            # Başlığın altından başlat (start_y = 60)
            relative_y = mouse_y - 60 + self.scroll_y
            
            # Hangi indexe denk geldiğini bul
            clicked_index = relative_y // self.ITEM_HEIGHT
            
            # History listesi tersten gösterildiği için indexi düzeltmemiz lazım
            # Ekranda en üstteki (index 0) aslında listenin en son elemanıdır.
            if pathfinder.history_data:
                actual_index = len(pathfinder.history_data) - 1 - int(clicked_index)
                
                if 0 <= actual_index < len(pathfinder.history_data):
                    pathfinder.select_history_entry(actual_index)
                    return True # Tıklama yakalandı
                
        return False

    def handle_scroll(self, event, pathfinder):
        """Scroll işlemini yönetir"""
        if pathfinder.is_history_mode:
            self.scroll_y -= event.y * self.SCROLL_SPEED
            max_scroll = max(0, (len(pathfinder.history_data) * self.ITEM_HEIGHT) - (self.height - 100))
            self.scroll_y = max(0, min(self.scroll_y, max_scroll))

    def draw(self, screen, pathfinder):
        """Tüm UI elemanlarını çizer"""
        if pathfinder.is_history_mode:
            self._draw_sidebar(screen, pathfinder)
        else:
            self._draw_live_info(screen, pathfinder)

    def _draw_live_info(self, screen, pathfinder):
        info_text = self.font_title.render(f"Mode: {pathfinder.current_algo.upper()} (Press H for History)", True, (0, 0, 0))
        keys_text = self.font_detail.render("[1: A*]  [2: RRT]  [3: RRT*]", True, (50, 50, 50))
        
        # Arka plan kutusu
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, 320, 60), border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 320, 60), 2, border_radius=8)
        
        screen.blit(info_text, (20, 15))
        screen.blit(keys_text, (20, 40))

    def _draw_sidebar(self, screen, pathfinder):
        # 1. Yan Panel Arka Planı
        overlay = pygame.Surface((self.SIDEBAR_WIDTH, self.height), pygame.SRCALPHA)
        overlay.fill((30, 30, 30, 240))
        screen.blit(overlay, (self.width - self.SIDEBAR_WIDTH, 0))

        # 2. Başlık
        title = self.font_title.render("HISTORY LOGS", True, (255, 255, 255))
        screen.blit(title, (self.width - self.SIDEBAR_WIDTH + 20, 20))
        pygame.draw.line(screen, (100, 100, 100), (self.width - self.SIDEBAR_WIDTH, 50), (self.width, 50), 1)

        # 3. Liste Elemanları
        start_y = 60 
        
        # Listeyi ters çevirip gösteriyoruz (En yeni en üstte)
        # Ancak orijinal listedeki indexleri kaybetmemek için enumerate yerine range kullanıyoruz
        history_len = len(pathfinder.history_data)
        
        for i in range(history_len):
            # i: 0, 1, 2... (Ekranda çizim sırası)
            # data_index: Listenin sonundan başına doğru (Data sırası)
            data_index = history_len - 1 - i
            entry = pathfinder.history_data[data_index]

            box_y = start_y + (i * self.ITEM_HEIGHT) - self.scroll_y
            
            # Clipping (Sadece ekrandakileri çiz)
            if 50 < box_y + self.ITEM_HEIGHT and box_y < self.height:
                
                is_selected = (data_index == pathfinder.current_history_index)
                color = (60, 60, 60) if not is_selected else (0, 100, 0)
                
                rect_x = self.width - self.SIDEBAR_WIDTH + 10
                rect_width = self.SIDEBAR_WIDTH - 20
                
                # Kutu
                pygame.draw.rect(screen, color, (rect_x, box_y, rect_width, self.ITEM_HEIGHT - 5), border_radius=5)
                if is_selected:
                    pygame.draw.rect(screen, (0, 255, 0), (rect_x, box_y, rect_width, self.ITEM_HEIGHT - 5), 2, border_radius=5)

                # Yazılar
                algo_text = self.font_title.render(f"{entry['algorithm'].upper()}", True, (255, 255, 255))
                time_text = self.font_detail.render(f"Time: {entry['timestamp']}", True, (180, 180, 180))
                
                screen.blit(algo_text, (rect_x + 10, box_y + 5))
                screen.blit(time_text, (rect_x + 10, box_y + 30))