import pygame
from color import game_loop_color
from shape import game_loop_shape

# Inisialisasi Pygame
pygame.init()

# Dimensi Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Shape and Color")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Fungsi menu utama
def main_menu():
    while True:
        screen.fill(WHITE)
        menu_text = font.render("Choose a Mode:", True, BLACK)
        color_mode = font.render("1. Catch by Color", True, BLACK)
        shape_mode = font.render("2. Catch by Shape", True, BLACK)
        quit_text = font.render("Q. Quit Game", True, BLACK)

        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 100))
        screen.blit(color_mode, (SCREEN_WIDTH // 2 - color_mode.get_width() // 2, 200))
        screen.blit(shape_mode, (SCREEN_WIDTH // 2 - shape_mode.get_width() // 2, 300))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop_color()
                elif event.key == pygame.K_2:
                    game_loop_shape()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return

# Jalankan game
if __name__ == "__main__":
    main_menu()
