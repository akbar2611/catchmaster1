# import pygame
# import random

# # Inisialisasi Pygame
# pygame.init()

# # Dimensi Layar
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Catch the Shape and Color")

# # Warna
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# COLORS = {
#     "Red": (255, 0, 0),
#     "Green": (0, 255, 0),
#     "Blue": (0, 0, 255),
#     "Yellow": (255, 255, 0),
#     "Magenta": (255, 0, 255),
#     "Cyan": (0, 255, 255),
#     "Orange": (255, 165, 0),
#     "Purple": (128, 0, 128),
#     "Gray": (192, 192, 192),
#     "Teal": (0, 128, 128),
# }

# # Kecepatan Frame
# FPS = 60
# clock = pygame.time.Clock()

# # Pemain (keranjang)
# player_width = 80
# player_height = 20
# player_x = SCREEN_WIDTH // 2 - player_width // 2
# player_y = SCREEN_HEIGHT - player_height - 10
# player_speed = 8

# # Objek
# object_width = 40
# object_height = 40
# objects = []

# # Target
# current_target = None
# target_type = None  # "color" atau "shape"

# # Skor
# score = 0
# font = pygame.font.Font(None, 36)

# # Fungsi untuk menggambar objek di layar
# def draw_objects():
#     # Gambar pemain
#     pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

#     # Gambar target
#     if target_type == "color":
#         target_text = font.render(f"Catch: {current_target}", True, BLACK)
#     elif target_type == "shape":
#         target_text = font.render(f"Catch: {current_target.capitalize()}", True, BLACK)

#     screen.blit(target_text, (10, 10))

#     # Gambar objek
#     for obj in objects:
#         if obj['type'] == "circle":
#             pygame.draw.circle(screen, obj['color'], obj['rect'].center, obj['rect'].width // 2)
#         elif obj['type'] == "rect":
#             pygame.draw.rect(screen, obj['color'], obj['rect'])
#         elif obj['type'] == "triangle":
#             points = [
#                 (obj['rect'].centerx, obj['rect'].top),
#                 (obj['rect'].left, obj['rect'].bottom),
#                 (obj['rect'].right, obj['rect'].bottom),
#             ]
#             pygame.draw.polygon(screen, obj['color'], points)
#         elif obj['type'] == "parallelogram":
#             points = [
#                 (obj['rect'].left + 10, obj['rect'].top),
#                 (obj['rect'].right, obj['rect'].top),
#                 (obj['rect'].right - 10, obj['rect'].bottom),
#                 (obj['rect'].left, obj['rect'].bottom),
#             ]
#             pygame.draw.polygon(screen, obj['color'], points)
#         elif obj['type'] == "rhombus":
#             points = [
#                 (obj['rect'].centerx, obj['rect'].top),
#                 (obj['rect'].right, obj['rect'].centery),
#                 (obj['rect'].centerx, obj['rect'].bottom),
#                 (obj['rect'].left, obj['rect'].centery),
#             ]
#             pygame.draw.polygon(screen, obj['color'], points)
#         elif obj['type'] == "kite":
#             points = [
#                 (obj['rect'].centerx, obj['rect'].top),
#                 (obj['rect'].right, obj['rect'].centery),
#                 (obj['rect'].centerx, obj['rect'].bottom),
#                 (obj['rect'].left, obj['rect'].centery),
#             ]
#             pygame.draw.polygon(screen, obj['color'], points)

#     # Gambar skor
#     score_text = font.render(f"Score: {score}", True, BLACK)
#     screen.blit(score_text, (10, 40))

# # Fungsi untuk membuat objek jatuh
# def spawn_object():
#     shape = random.choice(["circle", "rect", "triangle", "parallelogram", "rhombus", "kite"])
#     color_name, color_value = random.choice(list(COLORS.items()))
#     x = random.randint(0, SCREEN_WIDTH - object_width)
#     y = random.randint(-100, -40)
#     speed = random.randint(3, 6)

#     return {'type': shape, 'color': color_value, 'name': color_name, 'rect': pygame.Rect(x, y, object_width, object_height), 'speed': speed}

# # Fungsi untuk memilih target baru
# def select_target():
#     global current_target, target_type
#     if target_type == "color":
#         current_target = random.choice(list(COLORS.keys()))
#     elif target_type == "shape":
#         current_target = random.choice(["circle", "rect", "triangle", "parallelogram", "rhombus", "kite"])

# # Fungsi utama game
# def game_loop():
#     global player_x, score, objects, current_target, target_type

#     # Reset kondisi game
#     player_x = SCREEN_WIDTH // 2 - player_width // 2
#     score = 0
#     objects.clear()
#     select_target()

#     running = True
#     game_over = False

#     while running:
#         clock.tick(FPS)
#         screen.fill(WHITE)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return

#         if game_over:
#             # Tampilkan layar Game Over
#             game_over_text = font.render("Game Over! Press R to Restart or M to Menu", True, BLACK)
#             screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_r:  # Restart game
#                         game_loop()
#                         return
#                     elif event.key == pygame.K_m:  # Kembali ke menu utama
#                         main_menu()
#                         return
#             continue

#         # Menggerakkan pemain
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT] and player_x > 0:
#             player_x -= player_speed
#         if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
#             player_x += player_speed

#         # Spawning objek baru
#         if random.random() < 0.02:
#             objects.append(spawn_object())

#         # Memperbarui posisi objek dan memeriksa tabrakan
#         for obj in objects[:]:
#             obj['rect'].y += obj['speed']
#             if obj['rect'].y > SCREEN_HEIGHT:
#                 objects.remove(obj)

#             # Cek tabrakan dengan pemain
#             if obj['rect'].colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
#                 if target_type == "color" and obj['name'] == current_target:
#                     score += 1
#                     select_target()  # Ubah target setelah menangkap objek yang benar
#                 elif target_type == "shape" and obj['type'] == current_target:
#                     score += 1
#                     select_target()  # Ubah target setelah menangkap objek yang benar
#                 else:
#                     game_over = True
#                 objects.remove(obj)

#         # Gambar objek dan skor
#         draw_objects()

#         pygame.display.flip()

# # Fungsi menu utama
# def main_menu():
#     while True:
#         screen.fill(WHITE)
#         menu_text = font.render("Choose a Mode:", True, BLACK)
#         color_mode = font.render("1. Catch by Color", True, BLACK)
#         shape_mode = font.render("2. Catch by Shape", True, BLACK)
#         quit_text = font.render("Q. Quit Game", True, BLACK)

#         screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 100))
#         screen.blit(color_mode, (SCREEN_WIDTH // 2 - color_mode.get_width() // 2, 200))
#         screen.blit(shape_mode, (SCREEN_WIDTH // 2 - shape_mode.get_width() // 2, 300))
#         screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))

#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_1:
#                     global target_type
#                     target_type = "color"
#                     game_loop()
#                 elif event.key == pygame.K_2:
#                     target_type = "shape"
#                     game_loop()
#                 elif event.key == pygame.K_q:
#                     pygame.quit()
#                     return

# # Jalankan game
# if __name__ == "__main__":
#     main_menu()
