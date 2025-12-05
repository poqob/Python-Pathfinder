import pygame, sys
from src.utils import create_matrix_from_image
from src.pathfinder_manager import Pathfinder
from src.ui_manager import UIManager # Yeni Import

# --- SETUP ---
pygame.init()
matrix, map_width, map_height = create_matrix_from_image('assets/map.png') 

screen = pygame.display.set_mode((map_width, map_height))
pygame.display.set_caption("Roomba AI Pathfinder")
clock = pygame.time.Clock()

bg_surf = pygame.image.load('assets/map.png').convert()

# --- YÖNETİCİ SINIFLAR ---
pathfinder = Pathfinder(matrix)
ui = UIManager(map_width, map_height) # UI yöneticisini başlat

def main():
    while True:
        # 1. EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Klavye Girişleri
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: pathfinder.set_algorithm('astar')
                if event.key == pygame.K_2: pathfinder.set_algorithm('rrt')
                if event.key == pygame.K_3: pathfinder.set_algorithm('rrt_star')
                if event.key == pygame.K_h: pathfinder.toggle_history_mode()

            # Mouse Tekerleği (Scroll)
            if event.type == pygame.MOUSEWHEEL:
                ui.handle_scroll(event, pathfinder)

            # Mouse Tıklama
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Sol tık
                    # Önce UI'a tıklandı mı kontrol et
                    if pathfinder.is_history_mode:
                        if ui.handle_sidebar_click(event.pos, pathfinder):
                            continue # UI'a tıklandıysa haritaya yol çizme

                    # UI'a tıklanmadıysa ve History modunda değilsek yol çiz
                    if not pathfinder.is_history_mode:
                        pathfinder.create_path()

        # 2. DRAWING
        screen.blit(bg_surf, (0, 0))       # Arkaplan
        pathfinder.update(screen)          # Yollar ve Robot
        ui.draw(screen, pathfinder)        # Arayüz ve Panel

        # 3. UPDATE DISPLAY
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()