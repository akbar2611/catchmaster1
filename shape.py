import pygame
import random

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
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Magenta": (255, 0, 255),
    "Cyan": (0, 255, 255),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128),
    "Gray": (192, 192, 192),
    "Teal": (0, 128, 128),
}

# Kecepatan Frame
FPS = 60
clock = pygame.time.Clock()

# Pemain (keranjang)
player_width = 80
player_height = 20
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 8

# Objek
object_width = 40
object_height = 40
objects = []

# Target
current_target = None
target_type = "shape"  # Sudah ditentukan mode shape

# Skor
score = 0
font = pygame.font.Font(None, 36)

# Fungsi untuk menggambar objek di layar
def draw_objects():
    # Gambar pemain
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

    # Gambar target
    target_text = font.render(f"Catch: {current_target}", True, BLACK)
    screen.blit(target_text, (10, 10))

    # Gambar objek
    for obj in objects:
        if obj['type'] == "circle":
            pygame.draw.circle(screen, obj['color'], obj['rect'].center, obj['rect'].width // 2)
        elif obj['type'] == "square":
            pygame.draw.rect(screen, obj['color'], obj['rect'])

    # Gambar skor
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 40))

# Fungsi untuk membuat objek jatuh
def spawn_object():
    shape_type = random.choice(["circle", "square"])
    color_name, color_value = random.choice(list(COLORS.items()))
    x = random.randint(0, SCREEN_WIDTH - object_width)
    y = random.randint(-100, -40)
    speed = random.randint(3, 6)

    return {'type': shape_type, 'color': color_value, 'rect': pygame.Rect(x, y, object_width, object_height), 'speed': speed}

# Fungsi untuk memilih target baru
def select_target():
    global current_target
    current_target = random.choice(["circle", "square"])

# Fungsi untuk game loop (Catch by Shape)
def game_loop_shape():
    global player_x, score, objects, current_target

    # Reset kondisi game
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    score = 0
    objects.clear()
    select_target()

    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if game_over:
            # Tampilkan layar Game Over
            game_over_text = font.render("Game Over! Press R to Restart or M to Menu", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        game_loop_shape()
                        return
                    elif event.key == pygame.K_m:  # Kembali ke menu utama
                        return
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
                if obj['type'] == current_target:
                    score += 1
                    select_target()  # Ubah target setelah menangkap objek yang benar
                else:
                    game_over = True
                objects.remove(obj)

        # Gambar objek dan skor
        draw_objects()

        pygame.display.flip()
