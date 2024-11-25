import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Dimensi Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Fruit Game")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Kecepatan Frame
FPS = 60
clock = pygame.time.Clock()

# Pemain (keranjang)
player_width = 80
player_height = 20
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 8

# Buah & Bom
fruit_width = 40
fruit_height = 40
fruit_speed = 5
objects = []

# Skor
score = 0
font = pygame.font.Font(None, 36)

# Game Over Flag
game_over = False

# Muat suara
fruit_sound = pygame.mixer.Sound("assets/fruit.wav")  # Ganti dengan file suara Anda
bomb_sound = pygame.mixer.Sound("assets/bomb.mp3")  # Ganti dengan file suara Anda

# Fungsi untuk menggambar objek di layar
def draw_objects():
    # Gambar pemain
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

    # Gambar buah dan bom
    for obj in objects:
        pygame.draw.rect(screen, obj['color'], obj['rect'])

    # Gambar skor
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Fungsi untuk membuat objek jatuh (buah atau bom)
def spawn_object():
    object_type = random.choice(['fruit', 'bomb'])
    color = YELLOW if object_type == 'fruit' else RED
    x = random.randint(0, SCREEN_WIDTH - fruit_width)
    y = random.randint(-100, -40)
    speed = random.randint(3, 6) if object_type == 'fruit' else random.randint(4, 7)

    return {'type': object_type, 'color': color, 'rect': pygame.Rect(x, y, fruit_width, fruit_height), 'speed': speed}

# Fungsi untuk kembali ke menu utama
def show_main_menu():
    screen.fill(WHITE)
    menu_text = font.render("Mini Game Collection", True, BLACK)
    instruction_text = font.render("Press 1 for 'Catch the Fruit' Game", True, BLACK)
    quit_text = font.render("Press Q to Quit", True, BLACK)

    screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 100))
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 200))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300))

    pygame.display.flip()

# Fungsi utama game
def game_1(screen):
    global player_x, game_over, score, objects

    # Reset kondisi game
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    score = 0
    game_over = False
    objects.clear()

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_over:
            # Menghitung posisi tengah untuk teks Game Over
            game_over_text = font.render("Game Over! Press R to Restart or M to Return to Menu", True, BLACK)
            game_over_x = (SCREEN_WIDTH - game_over_text.get_width()) // 2  # Tengah horizontal
            game_over_y = (SCREEN_HEIGHT - game_over_text.get_height()) // 2  # Tengah vertikal
            screen.blit(game_over_text, (game_over_x, game_over_y))  # Menampilkan teks di tengah
            pygame.display.flip()

            # Menunggu input pemain untuk restart atau kembali ke menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Tekan R untuk restart
                        game_1(screen)  # Memanggil ulang fungsi game_1 untuk restart
                        return  # Menghentikan loop ini dan memulai game baru
                    elif event.key == pygame.K_m:  # Tekan M untuk kembali ke menu utama
                        return  # Menghentikan loop ini dan kembali ke menu utama
            continue

        # Menggerakkan pemain
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # Spawning objek baru
        if random.random() < 0.02:
            objects.append(spawn_object())

        # Memperbarui posisi objek dan memeriksa tabrakan
        for obj in objects[:]:
            obj['rect'].y += obj['speed']
            if obj['rect'].y > SCREEN_HEIGHT:
                objects.remove(obj)

            # Cek tabrakan dengan pemain
            if obj['rect'].colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                if obj['type'] == 'fruit':
                    score += 1  # Tambah skor jika menangkap buah
                    fruit_sound.play()  # Mainkan suara menangkap buah
                elif obj['type'] == 'bomb':
                    game_over = True  # Game over jika menangkap bom
                    bomb_sound.play()  # Mainkan suara bom meledak
                objects.remove(obj)

        # Gambar objek dan skor
        draw_objects()

        pygame.display.flip()

    pygame.quit() 
