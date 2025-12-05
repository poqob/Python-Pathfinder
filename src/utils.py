import pygame

def create_matrix_from_image(image_path, cell_size=32):
    image = pygame.image.load(image_path)
    width, height = image.get_size()
    
    cols = width // cell_size
    rows = height // cell_size
    
    generated_matrix = []
    
    for r in range(rows):
        row_list = []
        for c in range(cols):
            pixel_x = (c * cell_size) + (cell_size // 2)
            pixel_y = (r * cell_size) + (cell_size // 2)
            
            if pixel_x < width and pixel_y < height:
                color = image.get_at((pixel_x, pixel_y))
                if sum(color[:3]) < 300:
                    row_list.append(0) # Duvar
                else:
                    row_list.append(1) # Yol
            else:
                row_list.append(0)
                
        generated_matrix.append(row_list)
    
    return generated_matrix, width, height