import pygame
import random

# Dimensi layar
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GROUND_COLOR = (50, 205, 50)

# Kecepatan frame
FPS = 60
clock = pygame.time.Clock()

# Karakter T-Rex
trex_width, trex_height = 50, 50
trex_x, trex_y = 50, SCREEN_HEIGHT - trex_height - 20
trex_velocity = 0
gravity = 1
jump_strength = -15
is_jumping = False

# Rintangan (Kaktus)
obstacle_x = SCREEN_WIDTH
obstacle_width = 20
obstacle_height = 60
obstacle_y = SCREEN_HEIGHT - obstacle_height - 20
obstacle_speed = 7

# Skor
score = 0

# Inisialisasi pygame
pygame.init()
font = pygame.font.Font(None, 36)

# Suara
jump_sound = pygame.mixer.Sound("assets/jump.mp3")
collision_sound = pygame.mixer.Sound("assets/collision.mp3")
special_score_sound = pygame.mixer.Sound("assets/special_score.wav")  # Suara khusus untuk kelipatan 10

# Fungsi menggambar kaktus solid
def draw_cactus(screen, x, y, width, height):
    # Batang utama
    pygame.draw.rect(screen, GRAY, (x, y, width, height))

    # Cabang kiri
    left_branch_width = width // 2
    left_branch_height = height // 2
    pygame.draw.rect(screen, GRAY, (x - left_branch_width, y + height // 3, left_branch_width, left_branch_height))

    # Cabang kanan
    right_branch_width = width // 2
    right_branch_height = height // 2
    pygame.draw.rect(screen, GRAY, (x + width, y + height // 3, right_branch_width, right_branch_height))

# Fungsi menggambar permainan
def draw_game(screen, score):
    screen.fill(WHITE)  # Latar belakang putih
    pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))  # Tanah
    pygame.draw.rect(screen, BLACK, (trex_x, trex_y, trex_width, trex_height))  # T-Rex
    draw_cactus(screen, obstacle_x, obstacle_y, obstacle_width, obstacle_height)  # Kaktus rintangan
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# Fungsi utama permainan
def game_2(screen):
    global trex_y, trex_velocity, is_jumping, obstacle_x, obstacle_width, obstacle_height, obstacle_y, obstacle_speed, score
    running = True
    game_over = False  # Menandai apakah permainan selesai
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    trex_velocity = jump_strength
                    is_jumping = True
                    jump_sound.play()  # Mainkan suara lompatan

        if not game_over:
            # Gerakan T-Rex
            trex_velocity += gravity
            trex_y += trex_velocity
            if trex_y >= SCREEN_HEIGHT - trex_height - 20:  # T-Rex menyentuh tanah
                trex_y = SCREEN_HEIGHT - trex_height - 20
                is_jumping = False

            # Gerakan rintangan
            obstacle_x -= obstacle_speed
            if obstacle_x + obstacle_width < 0:  # Reset posisi kaktus
                obstacle_x = SCREEN_WIDTH
                obstacle_width = random.randint(20, 30)
                obstacle_height = random.randint(50, 70)
                obstacle_y = SCREEN_HEIGHT - obstacle_height - 20  # Pastikan kaktus tetap di atas tanah
                obstacle_speed += 0.1  # Tambah kecepatan rintangan
                score += 1

                # Cek apakah skor adalah kelipatan 10
                if score % 10 == 0:
                    special_score_sound.play()  # Mainkan suara khusus untuk kelipatan 10

            # Deteksi tabrakan
            if (trex_x < obstacle_x + obstacle_width and
                trex_x + trex_width > obstacle_x and
                trex_y < obstacle_y + obstacle_height and
                trex_y + trex_height > obstacle_y):
                collision_sound.play()  # Mainkan suara tabrakan
                print("Game Over!")  # Menampilkan pesan Game Over
                game_over = True  # Menandai game selesai
        else:
            # Layar Game Over
            screen.fill(WHITE)
            game_over_text = font.render("Game Over! Press R to Restart or M to Return to Menu", True, BLACK)
            score_text = font.render(f"Your Score: {score}", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()

            # Menunggu input untuk restart atau keluar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Tekan R untuk restart
                        restart_game()  # Memulai ulang game
                        game_2(screen)  # Memanggil ulang fungsi game_2 untuk restart
                        return  # Menghentikan loop ini dan memulai game baru
                    elif event.key == pygame.K_m:  # Tekan M untuk kembali ke menu utama
                        return  # Menghentikan loop ini dan kembali ke menu utama

        # Gambar ulang layar
        if not game_over:
            draw_game(screen, score)  # Jika belum game over, terus menggambar game

def restart_game():
    global score, obstacle_speed, obstacle_x
    score = 0
    obstacle_speed = 7
    obstacle_x = SCREEN_WIDTH

