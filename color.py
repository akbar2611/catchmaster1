import pygame
import random
import json
import cairo

# Inisialisasi Pygame
pygame.init()

# Inisialisasi mixer untuk audio
pygame.mixer.init()

# Dimensi Layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Color")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 51, 102)
HIGHLIGHT_COLOR = (255, 215, 0)
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Magenta": (255, 0, 255),
    "Cyan": (0, 255, 255),
}

# Kecepatan Frame
FPS = 120
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

# Skor dan Level
score = 0
high_score = 0
level = 1
max_level = 1
font = pygame.font.Font(None, 36)

# File untuk menyimpan progres
PROGRESS_FILE = "progress_color.json"

# Suara
correct_sound = pygame.mixer.Sound("assets/correct_sound.wav")
game_over_sound = pygame.mixer.Sound("assets/game_over_sound.mp3")
special_score_sound = pygame.mixer.Sound("assets/special_score.wav")
backsound = pygame.mixer.Sound("assets/Backsound.ogg")
key= pygame.mixer.Sound("assets/key.mp3")
enter = pygame.mixer.Sound("assets/enter.mp3")


# Volume suara
key.set_volume(0.9)
backsound.set_volume(1.0) 
correct_sound.set_volume(0.5)
game_over_sound.set_volume(2.5)
special_score_sound.set_volume(0.7)

# Gunakan channel khusus untuk backsound
backsound_channel = pygame.mixer.Channel(0)
key_channel = pygame.mixer.Channel(1)
enter_channel = pygame.mixer.Channel(2)

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

    # Konversi permukaan ke Pygame Surface untuk ditampilkan
    pygame_surface = pygame.image.frombuffer(surface.get_data(), (SCREEN_WIDTH, SCREEN_HEIGHT), "ARGB")
    screen.blit(pygame_surface, (0, 0))


# Fungsi untuk menyimpan progres
def save_progress():
    progress = {
        "high_score": high_score,
        "max_level": max_level
    }
    with open(PROGRESS_FILE, "w") as file:
        json.dump(progress, file)


# Fungsi untuk memuat progres
def load_progress():
    global high_score, max_level
    try:
        with open(PROGRESS_FILE, "r") as file:
            progress = json.load(file)
            high_score = progress.get("high_score", 0)
            max_level = progress.get("max_level", 1)
    except FileNotFoundError:
        save_progress()


# Fungsi untuk menggambar objek di layar
def draw_objects():
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

    # Gambar target
    target_text = font.render(f"Catch: {current_target}", True, BLACK)
    screen.blit(target_text, (10, 10))

    # Gambar objek
    for obj in objects:
        pygame.draw.circle(screen, obj['color'], obj['rect'].center, obj['rect'].width // 2)

    # Gambar skor
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_game = font.render(f"Level: {level}", True, BLACK)
    high_score_game = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (610, 40))
    screen.blit(level_game, (10, 40))
    screen.blit(high_score_game, (610, 10))


# Fungsi untuk membuat objek jatuh
def spawn_object():
    color_name, color_value = random.choice(list(COLORS.items()))
    x = random.randint(0, SCREEN_WIDTH - object_width)
    y = random.randint(-100, -40)
    speed = random.randint(3, 6 + level)
    return {'type': "circle", 'color': color_value, 'name': color_name, 'rect': pygame.Rect(x, y, object_width, object_height), 'speed': speed}


# Fungsi untuk memilih target baru
def select_target():
    global current_target
    current_target = random.choice(list(COLORS.keys()))


# Fungsi untuk menggambar tombol menu dengan border dan background
def draw_button(text, x, y, width, height, is_selected):
    button_color = DARK_BLUE if is_selected else (180, 180, 180)
    border_color = HIGHLIGHT_COLOR if is_selected else (100, 100, 100)
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    pygame.draw.rect(screen, border_color, (x, y, width, height), 3)
    draw_text_with_shadow(text, font, WHITE, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2, highlight=is_selected)


# Fungsi untuk menggambar teks dengan bayangan dan highlight
def draw_text_with_shadow(text, font, color, x, y, highlight=False):
    shadow_offset = 2
    shadow_color = (50, 50, 50)
    shadow_text = font.render(text, True, shadow_color)
    screen.blit(shadow_text, (x + shadow_offset, y + shadow_offset))
    rendered_text = font.render(text, True, HIGHLIGHT_COLOR if highlight else color)
    screen.blit(rendered_text, (x, y))

# Fungsi untuk memilih level
def select_level_color():
    global level
    selected_level = 1  # Mulai dengan level 1 yang dipilih
    running = True
    while running:
        draw_gradient_background()
        # screen.fill(WHITE)
        title_text = font.render("Select Level", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Tampilkan level yang bisa dipilih dengan tombol
        for i in range(1, max_level + 1):
            level_text = f"Level {i}"  # Pastikan ini adalah string
            is_selected = i == selected_level
            draw_button(level_text, SCREEN_WIDTH // 2 - 300 //2 , 30 + i * 60, 300, 50, is_selected)

        # Tombol kembali
        back_text = "Press B to go back"  # Pastikan ini adalah string
        back_text_surface = font.render(back_text, True, BLACK)  # Render menjadi Surface
        screen.blit(back_text_surface, (SCREEN_WIDTH // 2 - back_text_surface.get_width() // 2, SCREEN_HEIGHT - 100))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Tekan B untuk kembali
                    enter.play()
                    return
                elif event.key == pygame.K_DOWN:  # Tombol DOWN untuk memilih level berikutnya
                    selected_level = min(selected_level + 1, max_level)  # Batasi agar tidak melebihi max_level
                    key.play()
                elif event.key == pygame.K_UP:  # Tombol UP untuk memilih level sebelumnya
                    selected_level = max(selected_level - 1, 1)  # Batasi agar tidak kurang dari 1
                    key.play()
                elif event.key == pygame.K_RETURN:  # Tombol ENTER untuk memilih level yang dipilih
                    level = selected_level
                    game_loop_color()
                    enter_channel.play(backsound)
                    
                    return

        pygame.display.flip()
backsound_channel = pygame.mixer.Channel(0)
# Fungsi untuk game loop
def game_loop_color():
    global player_x, score, high_score, max_level, objects, current_target, level

    player_x = SCREEN_WIDTH // 2 - player_width // 2
    score = 0
    objects.clear()
    select_target()

    running = True
    game_over = False
    selected_option = 0

    backsound_channel.play(backsound, loops=-1)  # Backsound diputar berulang


    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        # Gambar gradasi latar belakang
        draw_gradient_background()
  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if game_over:
            backsound.stop()
            score_over = font.render(f"Score : {score}", True, BLACK)
            game_over_text = font.render("Game Over!", True, BLACK)
            screen.blit(score_over, (SCREEN_WIDTH // 2 - score_over.get_width() // 2, 220))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))

            options = ["Play Again", "Return to Menu"]
            for i, option in enumerate(options):
                is_selected = i == selected_option
                draw_button(option, SCREEN_WIDTH // 2 - 150, 300 + i * 60, 300, 50, is_selected)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                selected_option = 1
                key_channel.play(key)
            elif keys[pygame.K_UP]:
                selected_option = 0
                key_channel.play(key)
            elif keys[pygame.K_RETURN]:
                enter.play()
                if selected_option == 0:
                    game_loop_color()
                    return
                elif selected_option == 1:
                    select_level_color()

            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        if random.random() < 0.02:
            objects.append(spawn_object())

        for obj in objects[:]:
            obj['rect'].y += obj['speed']
            if obj['rect'].y > SCREEN_HEIGHT:
                objects.remove(obj)
            if obj['rect'].colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                if obj['name'] == current_target:
                    score += 1
                    correct_sound.play()
                    if score % 5 == 0:
                        special_score_sound.play()
                        level += 1
                        max_level = max(max_level, level)
                        save_progress()
                    select_target()
                else:
                    game_over = True
                    game_over_sound.play()
                objects.remove(obj)

        if score > high_score:
            high_score = score
            save_progress()

        draw_objects()
        pygame.display.flip()


# Inisialisasi progres
load_progress()

