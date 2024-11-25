# main.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from game_1 import game_1
from game_2 import game_2


# Inisialisasi Pygame
pygame.init()

# Menyiapkan layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Game Collection")

font = pygame.font.Font(None, 48)

def show_menu():
    screen.fill(WHITE)
    menu_title = font.render("Mini Game Collection", True, BLACK)
    option_1 = font.render("1. Catch the Fruit", True, BLACK)
    option_2 = font.render("2. T-Rex", True, BLACK)
    quit_text = font.render("Q. Quit", True, BLACK)

    screen.blit(menu_title, (SCREEN_WIDTH // 2 - menu_title.get_width() // 2, 50))
    screen.blit(option_1, (SCREEN_WIDTH // 2 - option_1.get_width() // 2, 150))
    screen.blit(option_2, (SCREEN_WIDTH // 2 - option_2.get_width() // 2, 200))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 350))

    pygame.display.flip()

def run_game():
    running = True
    while running:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:   
                    game_1(screen)  # Memanggil game 1
                elif event.key == pygame.K_2:
                    game_2(screen)  # Memanggil game 2
                elif event.key == pygame.K_q:
                    running = False
    pygame.quit()

if __name__ == "__main__":
    run_game()
