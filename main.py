import pygame, sys
from src.utils import create_matrix_from_image
from src.pathfinder_manager import Pathfinder

# pygame setup
pygame.init()
pygame.font.init() # Font modülünü başlat
font = pygame.font.SysFont('Arial', 24)

matrix, map_width, map_height = create_matrix_from_image('assets/map.png') 
screen = pygame.display.set_mode((map_width, map_height))
pygame.display.set_caption("Roomba: A* vs RRT vs RRT*")
clock = pygame.time.Clock()

bg_surf = pygame.image.load('assets/map.png').convert()
pathfinder = Pathfinder(matrix)

def draw_ui(screen, current_algo):
    text_surf = font.render(f"Mode (1: A*, 2: RRT, 3: RRT*): {current_algo.upper()}", True, (200, 0, 0))
    # Arka plana beyaz kutu koyalım ki okunsun
    pygame.draw.rect(screen, (255, 255, 255), (10, 10, text_surf.get_width() + 10, 40))
    screen.blit(text_surf, (15, 15))

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # --- INPUT KONTROLLERİ ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pathfinder.set_algorithm('astar')
                if event.key == pygame.K_2:
                    pathfinder.set_algorithm('rrt')
                if event.key == pygame.K_3:
                    pathfinder.set_algorithm('rrt_star')

            if event.type == pygame.MOUSEBUTTONDOWN:
                pathfinder.create_path()

        screen.blit(bg_surf, (0, 0))
        pathfinder.update(screen)
        
        # UI Çizimi
        draw_ui(screen, pathfinder.current_algo)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()