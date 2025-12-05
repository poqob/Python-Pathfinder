import pygame
import sys
import os

# --- AYARLAR ---
WIDTH, HEIGHT = 1280, 736
CELL_SIZE = 32
GRID_COLOR = (200, 200, 200) # Grid çizgileri (Gri)
WALL_COLOR = (0, 0, 0)       # Duvar rengi (Siyah)
BG_COLOR = (255, 255, 255)   # Zemin rengi (Beyaz)
BUTTON_COLOR = (50, 150, 50) # Buton rengi
HOVER_COLOR = (70, 180, 70)  # Buton üzerine gelinceki renk
TEXT_COLOR = (255, 255, 255)

# Çıktı Klasörü
OUTPUT_DIR = "assets"
OUTPUT_FILE = "map.png"

# Pygame Başlatma
pygame.init()
pygame.display.set_caption("Roomba Map Editor - (Sol Tık: Çiz | Sağ Tık: Sil)")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20, bold=True)

# Çizim Yüzeyi (Canvas)
# Ekrana butonları vs. çizsek de kaydederken SADECE bu yüzeyi kaydedeceğiz.
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BG_COLOR)

# Buton Tanımları (Rect: x, y, w, h)
btn_save = pygame.Rect(10, HEIGHT - 50, 100, 40)
btn_clear = pygame.Rect(120, HEIGHT - 50, 100, 40)

def draw_grid():
    """Yardımcı ızgara çizgilerini çizer"""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def save_map():
    """Sadece Canvas'ı (duvarları) temiz bir şekilde kaydeder"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    pygame.image.save(canvas, path)
    print(f"Harita kaydedildi: {path}")

def draw_button(rect, text, mouse_pos):
    """Buton çizimi ve hover efekti"""
    color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=5)
    
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def main():
    drawing = False
    erasing = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- TIKLAMA OLAYLARI ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Sol Tık
                    # Butonlara tıklandı mı?
                    if btn_save.collidepoint(mouse_pos):
                        save_map()
                        # Görsel geri bildirim (kısa süreli beyaz flaş)
                        screen.fill((200, 255, 200)) 
                        pygame.display.update()
                        pygame.time.delay(100)
                    elif btn_clear.collidepoint(mouse_pos):
                        canvas.fill(BG_COLOR)
                    else:
                        drawing = True
                
                elif event.button == 3: # Sağ Tık
                    erasing = True

            # --- TIKLAMA BIRAKMA ---
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: drawing = False
                if event.button == 3: erasing = False

        # --- ÇİZİM MANTIĞI ---
        # Mouse basılı tutulduğu sürece boyama yap
        if drawing or erasing:
            # Mouse koordinatını Grid sistemine yuvarla (Snap to Grid)
            grid_x = (mouse_pos[0] // CELL_SIZE) * CELL_SIZE
            grid_y = (mouse_pos[1] // CELL_SIZE) * CELL_SIZE
            
            # Butonların üzerine boyama yapmayı engelle (Opsiyonel)
            if not (btn_save.collidepoint(mouse_pos) or btn_clear.collidepoint(mouse_pos)):
                color = WALL_COLOR if drawing else BG_COLOR
                pygame.draw.rect(canvas, color, (grid_x, grid_y, CELL_SIZE, CELL_SIZE))

        # --- EKRANA ÇİZİM ---
        # 1. Önce Canvas'ı (Duvarları) çiz
        screen.blit(canvas, (0, 0))
        
        # 2. Üzerine Grid çizgilerini çiz (Rehber olması için)
        draw_grid()
        
        # 3. En üste Butonları çiz
        draw_button(btn_save, "KAYDET", mouse_pos)
        draw_button(btn_clear, "TEMİZLE", mouse_pos)

        pygame.display.update()
        clock.tick(120)

if __name__ == "__main__":
    main()