import pygame, sys
from src.utils import create_matrix_from_image
from src.pathfinder_manager import Pathfinder

# --- AYARLAR ---
SIDEBAR_WIDTH = 300  # Yan panel genişliği
ITEM_HEIGHT = 60     # Her bir history kutusunun yüksekliği
SCROLL_SPEED = 20    # Fare tekerleği hızı

# pygame setup
pygame.init()
pygame.font.init()
font_title = pygame.font.SysFont('Arial', 20, bold=True)
font_detail = pygame.font.SysFont('Arial', 14)

matrix, map_width, map_height = create_matrix_from_image('assets/map.png') 
screen = pygame.display.set_mode((map_width, map_height))
pygame.display.set_caption("Roomba AI - Advanced History UI")
clock = pygame.time.Clock()

bg_surf = pygame.image.load('assets/map.png').convert()
pathfinder = Pathfinder(matrix)

# UI Durum Değişkenleri
scroll_y = 0  # Liste kaydırma miktarı

def draw_sidebar(screen, pathfinder):
    """Sağ tarafta history listesini çizer"""
    if not pathfinder.is_history_mode:
        return

    # 1. Yan Panel Arka Planı (Yarı saydam siyah)
    overlay = pygame.Surface((SIDEBAR_WIDTH, map_height), pygame.SRCALPHA)
    overlay.fill((30, 30, 30, 230)) # R,G,B, Alpha
    screen.blit(overlay, (map_width - SIDEBAR_WIDTH, 0))

    # 2. Başlık
    title = font_title.render("HISTORY LOGS", True, (255, 255, 255))
    screen.blit(title, (map_width - SIDEBAR_WIDTH + 20, 20))
    pygame.draw.line(screen, (100, 100, 100), (map_width - SIDEBAR_WIDTH, 50), (map_width, 50), 1)

    # 3. Liste Elemanlarını Çiz
    # Başlangıç Y koordinatı (Başlığın altından başla)
    start_y = 60 
    
    # Görünebilir alanın dışındakileri çizmemek için (Clipping)
    # Pygame'in set_clip özelliğini kullanabiliriz ama basit matematik yeterli.
    
    history_list = reversed(pathfinder.history_data) # En yeniyi en üstte göster
    # Ancak orijinal indexleri korumak için enumerate kullanırken dikkat etmeliyiz.
    # Kolaylık olsun diye düz listeden gidelim, en son eklenen en altta olsun.
    
    for i, entry in enumerate(pathfinder.history_data):
        # Kutunun ekrandaki Y konumu
        box_y = start_y + (i * ITEM_HEIGHT) - scroll_y
        
        # Sadece ekran sınırları içindeyse çiz
        if 50 < box_y + ITEM_HEIGHT and box_y < map_height:
            
            # Seçili olanı vurgula (Yeşil çerçeve)
            is_selected = (i == pathfinder.current_history_index)
            color = (60, 60, 60) if not is_selected else (0, 100, 0)
            
            # Kutu çizimi
            rect_x = map_width - SIDEBAR_WIDTH + 10
            rect_width = SIDEBAR_WIDTH - 20
            
            pygame.draw.rect(screen, color, (rect_x, box_y, rect_width, ITEM_HEIGHT - 5), border_radius=5)
            if is_selected:
                pygame.draw.rect(screen, (0, 255, 0), (rect_x, box_y, rect_width, ITEM_HEIGHT - 5), 2, border_radius=5)

            # Yazılar
            algo_text = font_title.render(f"{entry['algorithm'].upper()}", True, (255, 255, 255))
            time_text = font_detail.render(f"Time: {entry['timestamp']}", True, (200, 200, 200))
            
            screen.blit(algo_text, (rect_x + 10, box_y + 5))
            screen.blit(time_text, (rect_x + 10, box_y + 30))

def handle_sidebar_click(pos, pathfinder):
    """Yan panele tıklandığında ilgili history'yi seçer"""
    global scroll_y
    
    mouse_x, mouse_y = pos
    
    # Tıklama sidebar içinde mi?
    if mouse_x > map_width - SIDEBAR_WIDTH:
        # Başlığın altından başlat (start_y = 60)
        relative_y = mouse_y - 60 + scroll_y
        
        # Hangi indexe denk geldiğini bul
        clicked_index = relative_y // ITEM_HEIGHT
        
        # Geçerli bir index mi?
        if 0 <= clicked_index < len(pathfinder.history_data):
            pathfinder.select_history_entry(int(clicked_index))
            return True # Tıklama yakalandı
            
    return False # Sidebar'a tıklanmadı

def main():
    global scroll_y
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # --- KLAVYE ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: pathfinder.set_algorithm('astar')
                if event.key == pygame.K_2: pathfinder.set_algorithm('rrt')
                if event.key == pygame.K_3: pathfinder.set_algorithm('rrt_star')
                
                if event.key == pygame.K_h:
                    pathfinder.toggle_history_mode()

            # --- MOUSE TEKERLEĞİ (KAYDIRMA) ---
            if event.type == pygame.MOUSEWHEEL and pathfinder.is_history_mode:
                # Scroll miktarını değiştir
                scroll_y -= event.y * SCROLL_SPEED
                
                # Sınırları belirle (Sonsuza kadar kaymasın)
                max_scroll = max(0, (len(pathfinder.history_data) * ITEM_HEIGHT) - (map_height - 100))
                scroll_y = max(0, min(scroll_y, max_scroll))

            # --- MOUSE TIKLAMA ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Sol tık
                    # Önce sidebar'a tıklandı mı kontrol et
                    if pathfinder.is_history_mode:
                        sidebar_clicked = handle_sidebar_click(event.pos, pathfinder)
                        if sidebar_clicked:
                            continue # Haritaya tıklama işlemini yapma

                    # Sidebar'a tıklanmadıysa haritaya yol çiz
                    pathfinder.create_path()

        # ÇİZİM
        screen.blit(bg_surf, (0, 0))
        pathfinder.update(screen)
        
        # UI ÇİZİM
        if pathfinder.is_history_mode:
            draw_sidebar(screen, pathfinder)
        else:
            # Canlı mod bilgi yazısı
            info_text = font_title.render(f"Mode: {pathfinder.current_algo.upper()} (Press H for History)", True, (0, 0, 0))
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, info_text.get_width()+20, 40))
            screen.blit(info_text, (20, 20))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()