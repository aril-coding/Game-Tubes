import pygame
import random
import os

pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangkap Item")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load gambar

PLAYER1_IMG = pygame.image.load(os.path.join("assets", "images", "player1.png"))
PLAYER1_IMG = pygame.transform.scale(PLAYER1_IMG, (70, 80))

PLAYER2_IMG = pygame.image.load(os.path.join("assets", "images", "player2.png"))
PLAYER2_IMG = pygame.transform.scale(PLAYER2_IMG, (70, 80))

PLAYER3_IMG = pygame.image.load(os.path.join("assets", "images", "player3.png"))
PLAYER3_IMG = pygame.transform.scale(PLAYER3_IMG, (70, 80))



COIN_IMG = pygame.image.load(os.path.join("assets", "images", "coin.png"))
COIN_IMG = pygame.transform.scale(COIN_IMG, (60, 60))

DIAMOND_IMG = pygame.image.load(os.path.join("assets", "images", "diamond.png"))
DIAMOND_IMG = pygame.transform.scale(DIAMOND_IMG, (60, 60))

BOMB_IMG = pygame.image.load(os.path.join("assets", "images", "bomb.png"))
BOMB_IMG = pygame.transform.scale(BOMB_IMG, (60, 60))

MAGNET_IMG = pygame.image.load(os.path.join("assets", "images", "magnet.png"))
MAGNET_IMG = pygame.transform.scale(MAGNET_IMG, (50, 50))


BACKGROUND_IMG = pygame.image.load(os.path.join("assets", "images", "background.jpg"))
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

CHAR_SELECT_BG = pygame.image.load(os.path.join("assets", "images", "char_select_bg.png"))
CHAR_SELECT_BG = pygame.transform.scale(CHAR_SELECT_BG, (WIDTH, HEIGHT))

BG = pygame.image.load(os.path.join("assets", "images", "bg1.png"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


# Suara
coin_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "coin.ogg"))
diamond_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "diamond.ogg"))
bomb_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "bomb.ogg"))

# Font
font = pygame.font.SysFont(None, 36)

# Konfigurasi awal
player_speed = 5
items = []
particles = []  # daftar partikel aktif
fall_speed = 4
players = []
magnet_active = [0, 0]  # durasi magnet aktif per pemain dalam frame
controls = [(pygame.K_LEFT, pygame.K_RIGHT), (pygame.K_a, pygame.K_d)]
selected_players = [PLAYER1_IMG, PLAYER1_IMG]  # default player images
PLAYER1_IMG = pygame.transform.scale(PLAYER1_IMG, (90, 100))
PLAYER2_IMG = pygame.transform.scale(PLAYER2_IMG, (90, 100))
PLAYER3_IMG = pygame.transform.scale(PLAYER3_IMG, (90, 100))



# Event untuk spawn item
item_event = pygame.USEREVENT + 1
pygame.time.set_timer(item_event, 1000)

# Mode permainan
mode = None  # None / "single" / "multi"

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))
        

high_score = load_high_score()

winner_text = ""  # untuk menampilkan pemenang

def spawn_particles(pos, color):
    for _ in range(10):
        radius = random.randint(2, 4)
        dx = random.uniform(-2, 2)
        dy = random.uniform(-2, 2)
        lifetime = random.randint(20, 40)
        particles.append({'pos': list(pos), 'dx': dx, 'dy': dy, 'radius': radius, 'color': color, 'life': lifetime})




def show_menu():
    WIN.blit(BG, (0,0))
    title = font.render("Pilih Mode Permainan", True, BLACK)
    sp_text = font.render("1 - Single Player", True, BLACK)
    mp_text = font.render("2 - Multiplayer (2 Pemain)", True, BLACK)
    WIN.blit(title, (WIDTH // 2 - 120, HEIGHT // 2 - 60))
    WIN.blit(sp_text, (WIDTH // 2 - 100, HEIGHT // 2 - 10))
    WIN.blit(mp_text, (WIDTH // 2 - 130, HEIGHT // 2 + 30))
    hs_text = font.render(f"High Score: {high_score}", True, BLACK)
    WIN.blit(hs_text, (WIDTH // 2 - 100, HEIGHT // 2 + 80))

    pygame.display.update()
    
    
def choose_character():
    choosing = True
    current_selection = 0
    character_images = [PLAYER1_IMG, PLAYER2_IMG, PLAYER3_IMG]
    character_positions = [(90, 250), (255, 250), (420, 250)]


    while choosing:
        WIN.blit(CHAR_SELECT_BG, (0, 0))

        # Judul dan instruksi
        title = font.render("Pilih Karakter", True, BLACK)
        inst1 = font.render("Tekan 1, 2, atau 3 untuk memilih karakter", True, BLACK)
        inst2 = font.render("Tekan ENTER untuk konfirmasi", True, BLACK)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        WIN.blit(inst1, (WIDTH // 2 - inst1.get_width() // 2, 90))
        WIN.blit(inst2, (WIDTH // 2 - inst2.get_width() // 2, 120))

        # Gambar karakter
        for i, img in enumerate(character_images):
            x, y = character_positions[i]
            WIN.blit(img, (x, y))
            if current_selection == i:
                highlight = pygame.Rect(x, y, 90, 100)

                pygame.draw.rect(WIN, (0, 255, 0), highlight, 3)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_selection = 0
                elif event.key == pygame.K_2:
                    current_selection = 1
                elif event.key == pygame.K_3:
                    current_selection = 2
                elif event.key == pygame.K_RETURN:
                    return character_images[current_selection]


def init_players(mode):
    players.clear()
    if mode == "single":
        rect = selected_players[0].get_rect(midbottom=(WIDTH // 2, HEIGHT - 110))

        players.append({'rect': rect, 'score': 0, 'lives': 3})
    elif mode == "multi":
        rect1 = selected_players[0].get_rect(midbottom=(WIDTH // 3, HEIGHT - 110))
        rect2 = selected_players[1].get_rect(midbottom=(2 * WIDTH // 3, HEIGHT - 110))

        players.append({'rect': rect1, 'score': 0, 'lives': 3})
        players.append({'rect': rect2, 'score': 0, 'lives': 3})

def draw_window():
    WIN.blit(BACKGROUND_IMG, (0, 0))
    for i, player in enumerate(players):
        WIN.blit(selected_players[i], player['rect'])

        score_text = font.render(f"P{i+1} Skor: {player['score']}", True, BLACK)
        lives_text = font.render(f"Nyawa: {player['lives']}", True, BLACK)
        WIN.blit(score_text, (10, 10 + i * 40))
        WIN.blit(lives_text, (200, 10 + i * 40))
        if magnet_active[i] > 0:
            m_text = font.render("Magnet!", True, (0, 200, 0))
            WIN.blit(m_text, (350, 10 + i * 40))

    for obj in items:
        WIN.blit(obj['img'], obj['rect'])
        # Gambar partikel
    for particle in particles[:]:
        particle['pos'][0] += particle['dx']
        particle['pos'][1] += particle['dy']
        particle['life'] -= 1
        if particle['life'] <= 0:
            particles.remove(particle)
            continue
        pygame.draw.circle(WIN, particle['color'], (int(particle['pos'][0]), int(particle['pos'][1])), particle['radius'])

    pygame.display.update()

def game_over():
    WIN.blit(BG, (0,0))
    over_text = font.render("GAME OVER", True, BLACK)
    restart_text = font.render("Tekan R untuk restart", True, BLACK)
    menu_text = font.render("Tekan M untuk menu utama", True, BLACK)
    highscore_text = font.render(f"High Score: {high_score}", True, BLACK)
    winner_display = font.render(winner_text, True, BLACK)

    WIN.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 100))
    WIN.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 - 60))
    WIN.blit(menu_text, (WIDTH // 2 - 140, HEIGHT // 2 - 20))
    WIN.blit(highscore_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    WIN.blit(winner_display, (WIDTH // 2 - 120, HEIGHT // 2 + 60))

    pygame.display.update()



# Loop utama
run = True
clock = pygame.time.Clock()
game_active = False
showing_menu = True

while run:
    clock.tick(60)

    if showing_menu:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "single"
                    selected_players[0] = choose_character()
                    init_players(mode)
                    items.clear()
                    game_active = True
                    showing_menu = False
                elif event.key == pygame.K_2:
                    mode = "multi"
                    selected_players[0] = choose_character()
                    selected_players[1] = choose_character()
                    init_players(mode)
                    items.clear()
                    game_active = True
                    showing_menu = False


    elif game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == item_event:
                kind = random.choices(['coin', 'diamond', 'bomb', 'magnet'], weights=[0.4, 0.2, 0.35, 0.05])[0]
                img = COIN_IMG if kind == 'coin' else DIAMOND_IMG if kind == 'diamond' else BOMB_IMG
                if kind == 'magnet':
                    img = MAGNET_IMG

                rect = img.get_rect(midtop=(random.randint(20, WIDTH - 20), 0))
                items.append({'img': img, 'rect': rect, 'type': kind})

        # Kontrol pemain
        keys = pygame.key.get_pressed()
        for i, player in enumerate(players):
            if player['lives'] <= 0:
                continue  # Lewati pemain jika nyawanya habis
            left, right = controls[i]
            if keys[left] and player['rect'].left > 0:
                player['rect'].x -= player_speed
            if keys[right] and player['rect'].right < WIDTH:
                player['rect'].x += player_speed


        # Update item
        for obj in items[:]:
            obj['rect'].y += fall_speed
            for player in players:
                if obj['rect'].colliderect(player['rect']):
                    if obj['type'] == 'coin':
                        player['score'] += 1
                        coin_sound.play()
                        spawn_particles(obj['rect'].center, (255, 223, 0))  # kuning keemasan
                    elif obj['type'] == 'diamond':
                        player['score'] += 2
                        diamond_sound.play()
                        spawn_particles(obj['rect'].center, (0, 255, 255))  # biru terang
                    elif obj['type'] == 'bomb':
                        if player['lives'] > 0:
                            player['lives'] -= 1
                            bomb_sound.play()
                            spawn_particles(obj['rect'].center, (255, 0, 0))  # merah
                    elif obj['type'] == 'magnet':
                        magnet_active[i] = 300  # aktif 5 detik (60fps * 5)
                        spawn_particles(obj['rect'].center, (100, 255, 100))  # hijau terang



                    items.remove(obj)
                    break
            else:
                if obj['rect'].top > HEIGHT:
                    items.remove(obj)

        # Naikkan kecepatan jatuh
        for player in players:
            if player['score'] >= 15:
                fall_speed = 9
            elif player['score'] >= 10:
                fall_speed = 6

        if all(p['lives'] <= 0 for p in players):
            max_score = max(p['score'] for p in players)
            if max_score > high_score:
                high_score = max_score
                save_high_score(high_score)

            # Tentukan pemenang jika multiplayer
            if mode == "multi":
                if players[0]['score'] > players[1]['score']:
                    winner_text = "Pemain 1 Menang!"
                elif players[1]['score'] > players[0]['score']:
                    winner_text = "Pemain 2 Menang!"
                else:
                    winner_text = "Seri!"
            else:
                winner_text = ""

            game_active = False

        for i, player in enumerate(players):
            if magnet_active[i] > 0:
                magnet_active[i] -= 1
                for obj in items:
                    if obj['type'] in ['coin', 'diamond']:
                        dx = player['rect'].centerx - obj['rect'].centerx
                        dy = player['rect'].centery - obj['rect'].centery
                        dist = max(1, (dx**2 + dy**2)**0.5)
                        if dist < 150:  # radius magnet
                            obj['rect'].x += int(dx / dist * 3)
                            obj['rect'].y += int(dy / dist * 3)
        draw_window()

    else:
        game_over()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    init_players(mode)
                    items.clear()
                    fall_speed = 4
                    game_active = True
                elif event.key == pygame.K_m:
                    showing_menu = True
                    game_active = False
                    items.clear()
                    fall_speed = 4


pygame.quit()
