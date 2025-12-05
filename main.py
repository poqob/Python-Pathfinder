import pygame, sys
from src.utils import create_matrix_from_image
from src.pathfinder_manager import Pathfinder

# pygame setup
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

matrix, map_width, map_height = create_matrix_from_image('assets/map.png') 
screen = pygame.display.set_mode((map_width, map_height))
pygame.display.set_caption("Roomba AI with History")
clock = pygame.time.Clock()

bg_surf = pygame.image.load('assets/map.png').convert()
pathfinder = Pathfinder(matrix)

def draw_ui(screen, pathfinder):
    # UI Kutusu
    pygame.draw.rect(screen, (240, 240, 240), (10, 10, 400, 60))
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, 400, 60), 2)
    
    if pathfinder.is_history_mode:
        if pathfinder.history_data:
            entry = pathfinder.history_data[pathfinder.current_history_index]
            idx = pathfinder.current_history_index + 1
            total = len(pathfinder.history_data)
            
            info_text = f"HISTORY MODE ({idx}/{total})"
            detail_text = f"Algo: {entry['algorithm']} | Time: {entry['timestamp'].split(' ')[1]}"
            
            surf1 = font.render(info_text, True, (0, 0, 255))
            surf2 = font.render(detail_text, True, (50, 50, 50))
            
            screen.blit(surf1, (20, 15))
            screen.blit(surf2, (20, 40))
        else:
            surf = font.render("HISTORY EMPTY", True, (255, 0, 0))
            screen.blit(surf, (20, 25))
    else:
        info_text = f"LIVE MODE - Algo: {pathfinder.current_algo.upper()}"
        keys_text = "Keys: [1:A*] [2:RRT] [3:RRT*] [H:History]"
        
        surf1 = font.render(info_text, True, (0, 150, 0))
        surf2 = font.render(keys_text, True, (50, 50, 50))
        
        screen.blit(surf1, (20, 15))
        screen.blit(surf2, (20, 40))

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Mod Değiştirme
                if event.key == pygame.K_1: pathfinder.set_algorithm('astar')
                if event.key == pygame.K_2: pathfinder.set_algorithm('rrt')
                if event.key == pygame.K_3: pathfinder.set_algorithm('rrt_star')
                
                # History Kontrolleri
                if event.key == pygame.K_h:
                    pathfinder.toggle_history_mode()
                
                if pathfinder.is_history_mode:
                    if event.key == pygame.K_LEFT:
                        pathfinder.prev_history()
                    if event.key == pygame.K_RIGHT:
                        pathfinder.next_history()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pathfinder.create_path()

        screen.blit(bg_surf, (0, 0))
        pathfinder.update(screen)
        draw_ui(screen, pathfinder)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()