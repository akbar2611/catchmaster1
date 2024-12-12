import pygame
import cairo
from color import select_level_color
from shape import select_level_shape

# Inisialisasi Pygame
pygame.init()

# Dimensi Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch Master")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 51, 102)
HIGHLIGHT_COLOR = (255, 215, 0)

main_font = pygame.font.Font(None, 50)
menu_font = pygame.font.Font(None, 36)

key = pygame.mixer.Sound("assets/key.mp3")
enter = pygame.mixer.Sound("assets/enter.mp3")
backsound = pygame.mixer.Sound("assets/Backsound.ogg")

key.set_volume(0.9)

def draw_gradient_background():
    # Buat permukaan untuk menggambar dengan PyCairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, SCREEN_WIDTH, SCREEN_HEIGHT)
    context = cairo.Context(surface)

    # Buat gradasi linear
    gradient = cairo.LinearGradient(0, 0, 0, SCREEN_HEIGHT)
    gradient.add_color_stop_rgb(0, 0.9, 0.9, 1)  # Biru pucat di atas
    gradient.add_color_stop_rgb(1, 0.5, 0.7, 1)  # Biru muda di bawah

    # Isi latar belakang dengan gradasi
    context.rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    context.set_source(gradient)
    context.fill()

    # Konversi permukaan PyCairo menjadi format yang bisa digunakan oleh Pygame
    data = surface.get_data()
    return pygame.image.frombuffer(data, (SCREEN_WIDTH, SCREEN_HEIGHT), "ARGB")

# Fungsi untuk menggambar teks dengan bayangan dan highlight
def draw_text_with_shadow(text, font, color, x, y, highlight=False):
    shadow_offset = 2
    shadow_color = (50, 50, 50)

    # Gambar bayangan
    shadow_text = font.render(text, True, shadow_color)
    screen.blit(shadow_text, (x + shadow_offset, y + shadow_offset))

    # Gambar teks utama
    rendered_text = font.render(text, True, HIGHLIGHT_COLOR if highlight else color)
    screen.blit(rendered_text, (x, y))

# Fungsi untuk menggambar tombol menu dengan border dan background
def draw_button(text, x, y, width, height, is_selected):
    button_color = DARK_BLUE if is_selected else (180, 180, 180)
    border_color = (255, 215, 0) if is_selected else (100, 100, 100)

    # Gambar tombol dengan background
    pygame.draw.rect(screen, button_color, (x, y, width, height))

    # Gambar border tombol
    pygame.draw.rect(screen, border_color, (x, y, width, height), 3)

    # Gambar teks pada tombol
    draw_text_with_shadow(text, menu_font, WHITE, x + (width - menu_font.size(text)[0]) // 2, y + (height - menu_font.size(text)[1]) // 2, highlight=is_selected)

# Fungsi menu utama
def main_menu():
    selected_option = 0
    options = ["Catch by Color", "Catch by Shape", "Quit Game"]

    backsound.stop()

    # Gambar latar belakang gradien
    gradient_background = draw_gradient_background()

    while True:
        # Tampilkan latar belakang gradien di layar
        screen.blit(gradient_background, (0, 0))

        # Gambar judul
        title_text = main_font.render("Catch Master", True, DARK_BLUE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Gambar opsi menu dengan tombol
        button_width = 400
        button_height = 60
        for i, option in enumerate(options):
            is_selected = i == selected_option
            draw_button(option, SCREEN_WIDTH // 2 - button_width // 2, 200 + i * 80, button_width, button_height, is_selected)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Navigasi ke atas
                    selected_option = (selected_option - 1) % len(options)
                    pygame.time.wait(150)  # Delay 150 ms
                    key.play()
                elif event.key == pygame.K_DOWN:  # Navigasi ke bawah
                    selected_option = (selected_option + 1) % len(options)
                    pygame.time.wait(150)  # Delay 150 ms
                    key.play()
                elif event.key == pygame.K_RETURN:  # Pilih opsi
                    enter.play()
                    if selected_option == 0:
                        select_level_color()
                    elif selected_option == 1:
                        select_level_shape()
                    elif selected_option == 2:
                        pygame.quit()
                        return

# Jalankan game
if __name__ == "__main__":
    main_menu()
