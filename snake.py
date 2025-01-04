import pygame
import time
import random
import os
import json
import math
import uuid
pygame.init()

# Definizione dei colori utilizzati nel gioco
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)
GREY = (200, 200, 200)
DARK_GREY = (50, 50, 50)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 102, 204)
ORANGE = (243, 112, 33)
AQUA = (36, 159, 156)
DARK_AQUA = (3, 122, 118)
PINK = (237, 27, 118)
LIGHT_PINK = (244, 71, 134)

# Dimensioni della finestra di gioco
WIDTH, HEIGHT = 800, 600
GAME_HEIGHT = HEIGHT 
SCOREBOARD_HEIGHT = 50 

# Creazione della finestra di gioco
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Variabili utili al gioco
BLOCK_SIZE = 20
SPEED, SPEED1, SPEED2 = 10, 10, 10
global_records = 0
last_score = 0
CURRENT_DIFFICULTY = "Balanced"
Length_of_snake = 1
current_game_id = None
last_input_time = 0
input_delay = 10
game_mode = "single"

# Font utilizzati nel gioco
font_style = pygame.font.SysFont("bahnschrift", 30)
font_style_small = pygame.font.SysFont('Arial', 15)
title_font = pygame.font.SysFont("bahnschrift", 55)

# Funzioni di disegno
def draw_background():
    """Disegna lo sfondo del gioco con un gradiente di grigio."""
    for y in range(HEIGHT):
        color = tuple(
            DARK_GREY[i] + (GREY[i] - DARK_GREY[i]) * y // HEIGHT for i in range(3)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def draw_text_with_options(text, font, x, y, text_color, outline_color=None, bg_color=None, border_radius=0):
    """Disegna il testo con opzioni per contorno e sfondo."""
    text_surface = font.render(text, True, text_color)
    text_width, text_height = text_surface.get_size()
    
    if outline_color:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            outline_surface = font.render(text, True, outline_color)
            screen.blit(outline_surface, (x + dx, y + dy))
    
    if bg_color:
        pygame.draw.rect(screen, bg_color, [x - 15, y - 7.5, text_width + 30, text_height + 15], border_radius=border_radius)
        pygame.draw.rect(screen, BLACK, [x - 15, y - 7.5, text_width + 30, text_height + 15], border_radius=border_radius, width=3)
    
    screen.blit(text_surface, (x, y))

def draw_menu(title, options, selected_option, score=None, high_score=None, resolutions=None, is_fullscreen=None, all_high_scores=None, game_mode=None):
    """Disegna un menu con il titolo e le opzioni fornite, evidenziando l'opzione selezionata."""
    if title != "Choice a New Ability":
        draw_background()
    option_offset = 0

    if title in ["Pause Menu", "Game Over"] and score is not None and high_score is not None:
        #draw_score_bar(score, high_score, CURRENT_DIFFICULTY)
        draw_score_bar(score, None, SPEED, None, Length_of_snake, None, high_score, CURRENT_DIFFICULTY)


    title_x = (WIDTH - title_font.render(title, True, GREEN).get_width()) // 2
    title_y = HEIGHT // 5
    border_radius_value = 100
    draw_text_with_options(title, title_font, title_x, title_y, WHITE, BLACK, DARK_GREY, border_radius=border_radius_value)

    if title == "Change Resolution":
        current_resolution = (WIDTH, HEIGHT)
        if is_fullscreen:
            current_index = 4
        elif current_resolution == (1920, 1080):
            current_index = 3  
        else:
            current_index = resolutions.index(current_resolution) if current_resolution in resolutions else 4

    elif title == "Game Over":
        if game_mode == "single":
            color = WHITE
            score_text = f"Your Score: {score}"
        if game_mode == "1vs1":
            color = GREEN
            score_text = f"Player 1 Score: {score}"
        score_width = font_style.render(score_text, True, GREEN).get_width()
        draw_text_with_options(
            score_text,
            font_style,
            (WIDTH - score_width) // 2,
            HEIGHT // 3,
            DARK_GREY,
            color
        )
        if game_mode == "single":
            high_score_text = f"High Score: {high_score}"
        if game_mode == "1vs1":
            color = RED
            high_score_text = f"Player 2 Score: {high_score}"
        high_score_width = font_style.render(high_score_text, True, GREEN).get_width()
        draw_text_with_options(
            high_score_text,
            font_style,
            (WIDTH - high_score_width) // 2,
            HEIGHT // 3 + 40,
            DARK_GREY,
            color
        )
        option_offset = 100

    elif title == "High Score":
        column_width = WIDTH // 4
        start_x = (WIDTH - (3 * column_width)) // 2
        y_start = HEIGHT // 3
        record_color = (255, 255, 255)
        large_font_style = pygame.font.SysFont('Arial', 40)
        large_font_style_small = pygame.font.SysFont('Arial', 30) 
        for idx, (mode, scores) in enumerate(all_high_scores.items()):
            column_x = start_x + idx * column_width
            mode_title_text = f"{mode}"
            draw_text_with_options(
                mode_title_text, 
                large_font_style, 
                column_x + ( column_width - large_font_style.size(mode_title_text)[0]) // 2, 
                y_start + 10, 
                BLACK, 
                BLACK, 
                WHITE
            )
            y_offset = y_start + 75 
            top_scores = scores[:3] if scores else ["No Records"]
            for i, score in enumerate(scores):
                record_text = f"{i + 1}. {score['score']}"
                draw_text_with_options(record_text, large_font_style_small, 
                                       column_x + (column_width - large_font_style_small.size(record_text)[0]) // 2, 
                                       y_offset, record_color, BLACK)
                y_offset += 40
        option_offset = 300

    for i, option in enumerate(options):
        color = WHITE if i != selected_option else BLACK
        option_text = font_style.render(option, True, color)
        option_x = WIDTH // 2 - option_text.get_width() // 2
        if title == "Choice a New Ability":
            option_offset = 50
        option_y = HEIGHT // 3 + i * 50 + option_offset

        if title == "Choice a New Ability":
            pygame.draw.rect(screen, BLACK, 
                 [option_x - 8, option_y - 8, option_text.get_width() + 16, option_text.get_height() + 16], 
                 border_radius=100)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            outline_text = font_style.render(option, True, BLACK)
            screen.blit(outline_text, (option_x + dx, option_y + dy))
        screen.blit(option_text, (option_x, option_y))

        if i == selected_option:
            border_color = BLACK
            bg_color = WHITE
            pygame.draw.rect(screen, border_color, 
                             [option_x - 8, option_y - 8, option_text.get_width() + 16, option_text.get_height() + 16],
                             border_radius=20)
            pygame.draw.rect(screen, bg_color, 
                             [option_x - 5, option_y - 5, option_text.get_width() + 10, option_text.get_height() + 10],
                             border_radius=15)

        screen.blit(option_text, (option_x, option_y))

        if title == "Change Mode":
            if CURRENT_DIFFICULTY == option:
                indicator_radius = 6
                indicator_x = option_x - 30
                indicator_y = option_y + option_text.get_height() // 2 
                pygame.draw.circle(screen, BLACK, (indicator_x, indicator_y), indicator_radius + 3)
                pygame.draw.circle(screen, GREEN, (indicator_x, indicator_y), indicator_radius)

        elif title == "Change Resolution":
            if i == current_index:
                indicator_radius = 6
                indicator_x = option_x - 30
                indicator_y = option_y + option_text.get_height() // 2
                pygame.draw.circle(screen, BLACK, (indicator_x, indicator_y), indicator_radius + 3)
                pygame.draw.circle(screen, GREEN, (indicator_x, indicator_y), indicator_radius)


def draw_score_bar(score1, score2, SPEED1, SPEED2, Length_of_snake1, Length_of_snake2, high_score, current_difficulty):
    """Disegna la barra del punteggio in alto nella finestra di gioco."""
    bar_height = 60
    pygame.draw.rect(screen, (50, 50, 50), [0, 0, WIDTH, bar_height])
    
    draw_text_with_options(f"Score: {score1:.1f}", font_style, 15, 15, (255, 255, 255), (0, 0, 0))
    if high_score is None:
        high_score = 0  
    if score2 == None:
        record_x = WIDTH - font_style.size(f"Record: {high_score:.1f}")[0] - 15
        draw_text_with_options(f"Record: {high_score:.1f}", font_style, record_x, 15, (255, 255, 255), (0, 0, 0))
    SPEED = SPEED1
    Length_of_snake = Length_of_snake1
    difficulty_label = "Mode:"
    label_x = (WIDTH - font_style.size(difficulty_label + " " + current_difficulty)[0]) // 2
    draw_text_with_options(difficulty_label, font_style, label_x, 15, (255, 255, 255), (0, 0, 0))
    
    if current_difficulty == "Relaxed":
        difficulty_color = (0, 255, 0)
    elif current_difficulty == "Balanced":
        difficulty_color = (255, 255, 0) 
    elif current_difficulty == "Extreme":
        difficulty_color = (255, 0, 0)
    else:
        difficulty_color = (255, 255, 255)
    
    difficulty_x = label_x + font_style.size(difficulty_label)[0] + 5
    draw_text_with_options(current_difficulty, font_style, difficulty_x, 15, difficulty_color, (0, 0, 0))

    speed_text = f"Speed: {SPEED:.2f}"
    speed_x = 20
    speed_y = 40
    draw_text_with_options(speed_text, font_style_small, speed_x, speed_y, (255, 255, 255), (0, 0, 0))

    length_text = f"Length: {Length_of_snake}"
    length_x = speed_x + font_style_small.size(speed_text)[0] + 20
    draw_text_with_options(length_text, font_style_small, length_x, speed_y, (255, 255, 255), (0, 0, 0))

    if score2:
            draw_text_with_options(f"Score: {score2:.1f}", font_style, WIDTH - 200, 15, (255, 255, 255), (0, 0, 0))
            speed2_text = f"Speed: {SPEED2:.2f}"
            speed2_x = WIDTH - 190
            speed2_y = 40
            draw_text_with_options(speed2_text, font_style_small, speed2_x, speed2_y, (255, 255, 255), (0, 0, 0))

            length2_text = f"Length: {Length_of_snake2}"
            length2_x = speed2_x + font_style_small.size(speed2_text)[0] + 20
            draw_text_with_options(length2_text, font_style_small, length2_x, speed2_y, (255, 255, 255), (0, 0, 0))

def our_snake(block_size, snake_List, player):
    """Disegna il serpente sullo schermo."""
    if player == 2:
        for i, x in enumerate(snake_List):
            color = ( max(0, 255 - i * 5), 0, 0)
            pygame.draw.rect(screen, (0, 0, 0), [x[0] - 2, x[1] - 2, block_size + 4, block_size + 4], border_radius=5)
            pygame.draw.rect(screen, color, [x[0], x[1], block_size, block_size], border_radius=5)
    else:    
        for i, x in enumerate(snake_List):
            color = (0, max(0, 255 - i * 5), 0)
            pygame.draw.rect(screen, (0, 0, 0), [x[0] - 2, x[1] - 2, block_size + 4, block_size + 4], border_radius=5)
            pygame.draw.rect(screen, color, [x[0], x[1], block_size, block_size], border_radius=5)

#Funzioni di Gioco
def generate_food(snake_List):
    """Genera una posizione casuale per il cibo che non collida con il serpente."""
    while True:
        food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(SCOREBOARD_HEIGHT, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        if is_valid_food_position(food_x, food_y, snake_List): 
            return food_x, food_y

def is_valid_food_position(x, y, snake_List):
    """Controlla se la posizione del cibo è valida (non collida con il serpente)."""
    for segment in snake_List:
        if segment == [x, y]:
            return False
    return True

def update_speed(score, CURRENT_DIFFICULTY, current_speed, last_updated_score):
    """Aggiorna la velocità del gioco in base al punteggio e alla difficoltà corrente."""
    if CURRENT_DIFFICULTY == "Relaxed":
        speed_increment = 0.5
        threshold = 10
    elif CURRENT_DIFFICULTY == "Balanced":
        speed_increment = 0.5
        threshold = 5
    elif CURRENT_DIFFICULTY == "Extreme":
        speed_increment = 1
        threshold = 5
    else:
        speed_increment = 0.05
        threshold = 10
    if score // threshold > last_updated_score // threshold:
        last_updated_score = score
        return current_speed + speed_increment, last_updated_score
    return current_speed, last_updated_score

def check_for_special_effect_activation(score, foodx, foody, player, game_mode, mode_high_score):
    """Controlla se attivare il menu degli effetti speciali in base al punteggio."""
    global last_score, last_score1, last_score2
    if game_mode == "single":
        if player == 1 and score > last_score + 5:
            if CURRENT_DIFFICULTY == "Relaxed":
                remainder = math.floor(score) % 15
                if remainder in {0, 1, 2, 3, 4}:
                    last_score = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List)
            elif CURRENT_DIFFICULTY == "Balanced":
                remainder = math.floor(score) % 30
                if remainder in {0, 1, 2, 3, 4}:
                    last_score = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List)
            elif CURRENT_DIFFICULTY == "Extreme":
                remainder = math.floor(score) % 60
                if remainder in {0, 1, 2, 3, 4}:
                    last_score = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List)
    if game_mode == "1vs1":
        if player == 1 and score > last_score1 + 5:
            if CURRENT_DIFFICULTY == "Relaxed":
                remainder = math.floor(score) % 15
                if remainder in {0, 1, 2, 3, 4}:
                    last_score1 = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List1)
            elif CURRENT_DIFFICULTY == "Balanced":
                remainder = math.floor(score) % 30
                if remainder in {0, 1, 2, 3, 4}:
                    last_score1 = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List1)
            elif CURRENT_DIFFICULTY == "Extreme":
                remainder = math.floor(score) % 60
                if remainder in {0, 1, 2, 3, 4}:
                    last_score1 = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List1)
        if player == 2 and score > last_score2 + 5:
            if CURRENT_DIFFICULTY == "Relaxed":
                remainder = math.floor(score) % 15
                if remainder in {0, 1, 2, 3, 4}:
                    last_score2 = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List2)
            elif CURRENT_DIFFICULTY == "Balanced":
                remainder = math.floor(score) % 30
                if remainder in {0, 1, 2, 3, 4}:
                    last_score2 = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List2)
            elif CURRENT_DIFFICULTY == "Extreme":
                remainder = math.floor(score) % 60
                if remainder in {0, 1, 2, 3, 4}:
                    last_score2 = score - remainder
                    show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List2)

def snake_input(event, direction, x1_change, y1_change,score, mode_high_score,player=None,game_mode=None):
    """Gestisce l'input dell'utente per il movimento del serpente."""
    global last_input_time
    current_time = pygame.time.get_ticks()

    if current_time - last_input_time < input_delay:
        return direction, x1_change, y1_change

    if event.type == pygame.KEYDOWN:
        last_input_time = current_time
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            if direction != "RIGHT":
                x1_change = -BLOCK_SIZE
                y1_change = 0
                direction = "LEFT"
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            if direction != "LEFT":
                x1_change = BLOCK_SIZE
                y1_change = 0
                direction = "RIGHT"
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            if direction != "DOWN":
                y1_change = -BLOCK_SIZE
                x1_change = 0
                direction = "UP"
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if direction != "UP":
                y1_change = BLOCK_SIZE
                x1_change = 0
                direction = "DOWN"
        elif event.key == pygame.K_ESCAPE:
            pauseMenu(score, mode_high_score,game_mode)
    return direction, x1_change, y1_change

# Funzioni per gli effetti speciali
def decrease_speed(player, game_mode):
    """Diminuisce la velocità del gioco di 5 per il giocatore specificato."""
    global SPEED, SPEED1, SPEED2
    print(f"Attivazione effetti per il Giocatore {player} in modalita {game_mode}")
    if game_mode == "single":
        SPEED = max(1, SPEED - 5)  # Assicurati che la velocità non scenda sotto 1
        print("Velocità diminuita di 5.")
    elif game_mode == "1vs1":
        if player == 1:
            SPEED1 = max(1, SPEED1 - 5)
            print("Velocità del Giocatore 1 diminuita di 5.")
        elif player == 2:
            SPEED2 = max(1, SPEED2 - 5)
            print("Velocità del Giocatore 2 diminuita di 5.")    

def increase_food_points(player, game_mode):
    """Il cibo normale fornisce il 20% di punti in più per il giocatore specificato."""
    global food_points_multiplier, food_points_multiplier1, food_points_multiplier2
    print(f"Attivazione effetti per il Giocatore {player} in modalita {game_mode}")
    if game_mode == "single":
        food_points_multiplier += 0.20  # Moltiplicatore per il punteggio del cibo normale
        print("Il cibo normale fornisce il 20% di punti in più.")
    elif game_mode == "1vs1":
        if player == 1:
            food_points_multiplier1 += 0.20
            print("Il cibo normale fornisce il 20% di punti in più per il Giocatore 1.")
        elif player == 2:
            food_points_multiplier2 += 0.20
            print("Il cibo normale fornisce il 20% di punti in più per il Giocatore 2.")

def increase_special_food_points(player, game_mode):
    """Il cibo speciale fornisce il 50% di punti in più per il giocatore specificato."""
    global special_food_points_multiplier, special_food_points_multiplier1, special_food_points_multiplier2
    print(f"Attivazione effetti per il Giocatore {player} in modalita {game_mode}")
    if game_mode == "single":
        special_food_points_multiplier += 0.5  # Moltiplicatore per il punteggio del cibo speciale
        print("Il cibo speciale fornisce il 50% di punti in più.")
    elif game_mode == "1vs1":
        if player == 1:
            special_food_points_multiplier1 += 0.5
            print("Il cibo speciale fornisce il 50% di punti in più per il Giocatore 1.")
        elif player == 2:
            special_food_points_multiplier2 += 0.5
            print("Il cibo speciale fornisce il 50% di punti in più per il Giocatore 2.")
            
def decrease_length(player, game_mode):
    """Dimezza la lunghezza del serpente e aggiorna la lista del serpente visivamente per il giocatore specificato."""
    global Length_of_snake, snake_List,Length_of_snake1, Length_of_snake2, snake_List1, snake_List2
    print(f"Attivazione effetti per il Giocatore {player} in modalita {game_mode}")
    if game_mode == "single":
        Length_of_snake = max(1, math.ceil(Length_of_snake / 2))  # Assicurati che la lunghezza non scenda sotto 1
        # Rimuovi gli ultimi segmenti dalla lista del serpente
        while len(snake_List) > Length_of_snake:
            snake_List.pop(0)  # Rimuove l'ultimo segmento
        print("Lunghezza del serpente dimezzata.")
    elif game_mode == "1vs1":
        if player == 1:
            Length_of_snake1 = max(1, math.ceil(Length_of_snake1 / 2))
            while len(snake_List1) > Length_of_snake1:
                snake_List1.pop(0)
            print("Lunghezza del serpente del Giocatore 1 dimezzata.")
        elif player == 2:
            Length_of_snake2 = max(1, math.ceil(Length_of_snake2 / 2))
            while len(snake_List2) > Length_of_snake2:
                snake_List2.pop(0)
            print("Lunghezza del serpente del Giocatore 2 dimezzata.")    

# Definizione degli effetti speciali
special_effects = [
    ("Diminuisci la velocità di 5", decrease_speed),
    ("Il cibo normale fornirà il 20% di punti in più", increase_food_points),
    ("Dimezza la lunghezza del serpente", decrease_length),
    ("Il cibo speciale fornirà il 50% di punti in più", increase_special_food_points)
]
# Funzioni di Gestione dei Record
def read_records():
    """Legge i record dal file 'record.txt' e restituisce un dizionario con i punteggi."""
    try:
        with open("record.txt", "r") as file:
            records = json.load(file)
            return records
    except FileNotFoundError:
        return {
            "Relaxed": [],
            "Balanced": [],
            "Extreme": []
        }

def write_records(records):
    """Scrive i record nel file 'record.txt'."""
    with open("record.txt", "w") as file:
        json.dump(records, file, indent=4)

def update_records(records, mode, score, game_id):
    """Aggiorna i record con il nuovo punteggio per la modalità specificata"""
    if mode not in records:
        records[mode] = []
    
    record_with_id = {"score": round(score, 1), "game_id": game_id}

    filtered_records = [rec for rec in records[mode] if rec["game_id"] != game_id]

    filtered_records.append(record_with_id)
    
    filtered_records = sorted(filtered_records, key=lambda x: x["score"], reverse=True)

    records[mode] = filtered_records[:3]
    
    return records

# Menu e Navigazione
def handle_menu_input(options, selected_option, event):
    """Gestisce l'input dell'utente per i menu."""
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_UP, pygame.K_w]:
            selected_option = (selected_option - 1) % len(options)
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            selected_option = (selected_option + 1) % len(options)
        elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            return selected_option, True
        elif event.key == pygame.K_ESCAPE:
            return len(options) - 1, True
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(options):
            option_x = WIDTH // 2 - font_style.size(option)[0] // 2
            option_y = HEIGHT // 3 + i * 50
            if option_x <= mouse_pos[0] <= option_x + font_style.size(option)[0] and \
               option_y <= mouse_pos[1] <= option_y + font_style.size(option)[1]:
                return i, True
    return selected_option, False

def gameMenu():
    """Mostra il menu principale del gioco e gestisce la navigazione tra le opzioni."""
    menu = True
    selected_option = 0
    options = ["Play", "High Score", "Mode", "Resolution", "Quit"]
    while menu:
        draw_menu("Snake Game", options, selected_option, score=None, high_score=None, resolutions=None, is_fullscreen=None, all_high_scores=None, game_mode=None)
        pygame.display.update()

        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    selectGameMode()
                elif selected_option == 1:
                    showHighScore()
                elif selected_option == 2:
                    changeDifficulty()
                elif selected_option == 3:
                    changeResolution()
                elif selected_option == 4:
                    pygame.quit()
                    quit()

def selectGameMode():
    """Mostra il menu per selezionare la modalità di gioco."""
    mode_menu = True
    selected_option = 0
    options = ["Single", "1vs1", "Back"]
    while mode_menu:
        draw_menu("Select Game Mode", options, selected_option)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    menu = False
                    gameLoop()  # Modalità singola
                elif selected_option == 1:
                    mode_menu = False
                    gameLoop1vs1()  # Modalità 1 vs 1
                elif selected_option == 2:
                    mode_menu = False

def showHighScore():
    """Mostra il menu dei punteggi più alti e gestisce la navigazione."""
    high_score_menu = True
    selected_option = 0
    options = ["Back"]
    all_high_scores = read_records()
    while high_score_menu:
        draw_menu("High Score", options, selected_option, score=None, high_score=None, resolutions=None, is_fullscreen=None, all_high_scores=all_high_scores)
        pygame.display.update()

        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    high_score_menu = False

def changeDifficulty():
    """Mostra il menu per cambiare la difficoltà e gestisce la selezione."""
    difficulty_menu = True
    selected_option = 0
    options = ["Relaxed", "Balanced", "Extreme", "Back"]
    global SPEED, CURRENT_DIFFICULTY
    while difficulty_menu:
        draw_menu("Change Mode", options, selected_option, score=None, high_score=None, resolutions=None, is_fullscreen=None, all_high_scores=None)
        pygame.display.update()
        
        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    SPEED = 8
                    CURRENT_DIFFICULTY = "Relaxed"
                    difficulty_menu = False
                elif selected_option == 1:
                    SPEED = 13
                    CURRENT_DIFFICULTY = "Balanced"
                    difficulty_menu = False
                elif selected_option == 2:
                    SPEED = 20
                    CURRENT_DIFFICULTY = "Extreme"
                    difficulty_menu = False
                elif selected_option == 3:
                    difficulty_menu = False

def changeResolution():
    """Mostra il menu per cambiare la risoluzione e gestisce la selezione."""
    global WIDTH, HEIGHT, screen
    resolutions = [
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1920, 1080),
        'fullscreen' 
    ]
    options = ["800 x 600", "1024 x 768", "1280 x 720", "1920 x 1080", "Fullscreen", "Back"]
    selected_option = 0 
    is_fullscreen = False
    while True:
        draw_menu("Change Resolution", options, selected_option, score=None, high_score=None, resolutions=resolutions, is_fullscreen=is_fullscreen, all_high_scores=None)
        pygame.display.update()

        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 5:
                    return
                elif selected_option == 4:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    WIDTH, HEIGHT = screen.get_size()
                    is_fullscreen = True 
                else:
                    is_fullscreen = False
                    WIDTH, HEIGHT = resolutions[selected_option]  
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Funzione per mostrare il menu degli effetti speciali
def show_special_effect_menu(score, foodx, foody, player, game_mode, mode_high_score, snake_List):
    """Mostra il menu per scegliere un effetto speciale."""
    selected_option = 0
    options = random.sample(special_effects, 3)
    option_texts = [opt[0] for opt in options] 

    # Disegna la situazione attuale
    draw_background()
    our_snake(BLOCK_SIZE, snake_List, player=1)  
    if game_mode == "1vs1":
        our_snake(BLOCK_SIZE, snake_List2, player=2)
    pygame.draw.circle(screen, BLACK, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

    # Disegna il punteggio attuale
    if game_mode == "single":
        draw_score_bar(score, None, SPEED, None, Length_of_snake, None, mode_high_score, CURRENT_DIFFICULTY)
    elif game_mode == "1vs1":
        draw_score_bar(score, None, SPEED, None, Length_of_snake, None, None, CURRENT_DIFFICULTY)

    while True:
        draw_menu("Choice a New Ability", option_texts, selected_option, score=None, high_score=None, resolutions=None, is_fullscreen=None, all_high_scores=None)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            selected_option, confirmed = handle_menu_input(option_texts, selected_option, event)
            if confirmed:
                print(f"Effetto scelto: {options[selected_option][0]}")
                options[selected_option][1](player, game_mode)
                return

def pauseMenu(score, current_high_score,game_mode):
    """Mostra il menu di pausa e gestisce la navigazione tra le opzioni."""
    paused = True
    selected_option = 0
    options = ["Resume", "Restart", "Main Menu"]
    while paused:
        draw_menu("Pause Menu", options, selected_option, score, current_high_score, resolutions=None, is_fullscreen=None, all_high_scores=None)
        pygame.display.update()
        
        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    paused = False
                elif selected_option == 1:
                    if game_mode == "single":
                        gameLoop()  # Riavvia la partita in modalità singola
                    elif game_mode == "1vs1":
                        gameLoop1vs1()  # Riavvia la partita in modalità 1 vs 1
                elif selected_option == 2:
                    gameMenu()                
    return True

def gameOverMenu(score, mode_high_score,game_mode):
    """Mostra il menu di fine gioco e gestisce la navigazione tra le opzioni."""
    game_close = True
    selected_option = 0
    options = ["Play Again", "Main Menu"]
    score_font = pygame.font.SysFont("bahnschrift", 30)
    records = read_records()
    if game_mode == "single":
        mode_high_score = max((rec["score"] for rec in records[CURRENT_DIFFICULTY]), default=0)
    while game_close:
        draw_menu("Game Over", options, selected_option, score, mode_high_score, resolutions=None, is_fullscreen=None, all_high_scores=None, game_mode=game_mode)
        pygame.display.update()

        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    if game_mode == "single":
                        gameLoop()  # Riavvia la partita in modalità singola
                    elif game_mode == "1vs1":
                        gameLoop1vs1()  # Riavvia la partita in modalità 1 vs 1
                elif selected_option == 1:
                    gameMenu()
    return True

#Funzione Principale
def gameLoop():
    """Gestisce il ciclo principale del gioco, inclusi movimento, collisioni e punteggio."""
    global global_records, CURRENT_DIFFICULTY, SPEED, last_updated_score, last_score, Length_of_snake, food_points_multiplier, special_food_points_multiplier, current_game_id, snake_List
    current_game_id = str(uuid.uuid4())
    game_over = False
    game_close = False
    x1, y1 = WIDTH / 2, HEIGHT / 2  
    x1_change, y1_change = 0, 0
    direction = None
    snake_List = []
    Length_of_snake = 1
    foodx, foody = generate_food(snake_List)
    special_food_timer = 0
    special_foodx, special_foody = None, None
    score = 1
    last_updated_score = 0
    global_records = read_records()
    mode_high_score = max((rec["score"] for rec in global_records[CURRENT_DIFFICULTY]), default=0)
    last_score = 0
    food_points_multiplier = 1.0
    special_food_points_multiplier = 1.0
    if CURRENT_DIFFICULTY == "Relaxed":
        initial_speed = 8 
    elif CURRENT_DIFFICULTY == "Balanced":
        initial_speed = 13 
    elif CURRENT_DIFFICULTY == "Extreme":
        initial_speed = 20
    else:
        initial_speed = 5  
    SPEED = initial_speed
    while not game_over:
        while game_close:
            mode_high_score = max((rec["score"] for rec in global_records[CURRENT_DIFFICULTY]), default=0)
            game_over = not gameOverMenu(score, mode_high_score,game_mode="single")
            if not game_over:
                break  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # Gestione input per il movimento del serpente
            direction, x1_change, y1_change = snake_input(event, direction, x1_change, y1_change,score,mode_high_score, player=1,game_mode=game_mode)

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            x1_change = 0
            y1_change = 0
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            x1_change = 0
            y1_change = 0

        # Aggiornamento della posizione del serpente
        x1 += x1_change
        y1 += y1_change
        if x1 < 0:
            x1 = WIDTH - BLOCK_SIZE  
        elif x1 >= WIDTH:
            x1 = 0  
        if y1 < SCOREBOARD_HEIGHT: 
            y1 = HEIGHT - BLOCK_SIZE 
        elif y1 >= HEIGHT:
            y1 = SCOREBOARD_HEIGHT  
        x1 = (x1 // BLOCK_SIZE) * BLOCK_SIZE
        y1 = (y1 // BLOCK_SIZE) * BLOCK_SIZE

        # Disegna la griglia
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (x, SCOREBOARD_HEIGHT), (x, HEIGHT))
        for y in range(SCOREBOARD_HEIGHT, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))
        
        # Disegna lo sfondo e il cibo
        draw_background()
        pygame.draw.circle(screen, BLACK, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        pygame.draw.circle(screen, WHITE, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2 - 2)

        # Gestione del cibo speciale
        if special_food_timer > 0:
            pygame.draw.circle(screen, BLACK, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
            pygame.draw.circle(screen, DARK_GREY, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2 -2)
            special_food_timer -= 1
        elif special_food_timer == 0 and random.randint(1, 100) == 1:
            special_foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_food_timer = 100
        
        # Aggiornamento della lista del serpente
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for block in snake_List[:-1]:
            if block == snake_Head:
                game_close = True

        # Disegna il serpente
        our_snake(BLOCK_SIZE, snake_List,player=1)

        # Aggiorna la velocità e il punteggio
        SPEED, last_updated_score = update_speed(score, CURRENT_DIFFICULTY, SPEED, last_updated_score)
        #draw_score_bar(score, mode_high_score, CURRENT_DIFFICULTY)
        draw_score_bar(score, None, SPEED, None, Length_of_snake, None, mode_high_score, CURRENT_DIFFICULTY)

        # Controllo collisione con il cibo
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1
            score += 1 * food_points_multiplier
            score = round(score, 1)
        if special_food_timer > 0 and x1 == special_foodx and y1 == special_foody:
            special_foodx, special_foody = None, None
            special_food_timer = 0
            Length_of_snake += 5
            score += 5 * special_food_points_multiplier
            score = round(score, 1)

        # Aggiorna i record
        global_records = update_records(global_records, CURRENT_DIFFICULTY, score, current_game_id)
        write_records(global_records)
        check_for_special_effect_activation(score, foodx, foody, player=1, game_mode="single",mode_high_score=mode_high_score)

        # Aggiorna lo schermo
        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()
    quit()

def gameLoop1vs1():
    """Gestisce il ciclo principale del gioco in modalità 1 vs 1."""
    global global_records, CURRENT_DIFFICULTY, SPEED1, SPEED2, last_updated_score, Length_of_snake1, Length_of_snake2, food_points_multiplier, special_food_points_multiplier, last_score1, last_score2, snake_List1, snake_List2, food_points_multiplier, food_points_multiplier1, food_points_multiplier2,special_food_points_multiplier, special_food_points_multiplier1, special_food_points_multiplier2 
    game_over = False
    game_close = False
    x1, y1 = WIDTH / 4, HEIGHT / 2  # Posizione del Giocatore 1
    x2, y2 = 3 * WIDTH / 4, HEIGHT / 2  # Posizione del Giocatore 2
    x1_change, y1_change = 0, 0
    x2_change, y2_change = 0, 0
    direction1, direction2 = None, None
    snake_List1, snake_List2 = [], []
    Length_of_snake1, Length_of_snake2 = 1, 1
    foodx, foody = generate_food(snake_List1 + snake_List2)
    special_food_timer = 0
    special_foodx, special_foody = None, None
    score1, score2 = 1, 1
    last_updated_score1, last_updated_score2 = 0, 0
    last_score1, last_score2 = 0, 0
    SPEED1, SPEED2 = 10, 10  # Velocità iniziale per entrambi i giocatori
    food_points_multiplier1, food_points_multiplier2 = 1.0, 1.0
    special_food_points_multiplier1, special_food_points_multiplier2 = 1.0, 1.0
    if CURRENT_DIFFICULTY == "Relaxed":
        initial_speed = 8 
    elif CURRENT_DIFFICULTY == "Balanced":
        initial_speed = 13 
    elif CURRENT_DIFFICULTY == "Extreme":
        initial_speed = 20
    else:
        initial_speed = 5
    SPEED1 = initial_speed
    SPEED2 = initial_speed
    while not game_over:
        while game_close:
            game_over = not gameOverMenu(score1, score2,game_mode="1vs1")
            if not game_over:
                break  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # Gestione input per il Giocatore 1 (WASD)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    direction1, x1_change, y1_change = snake_input(event, direction1, x1_change, y1_change, score1, None, player=1,game_mode="1vs1")
                elif event.key == pygame.K_ESCAPE:  # Pause menu for Player 1
                    pauseMenu(score1, None, game_mode="1vs1")

            # Gestione input per il Giocatore 2 (Frecce)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    direction2, x2_change, y2_change = snake_input(event, direction2, x2_change, y2_change, score2, None, player=2,game_mode="1vs1")
                elif event.key == pygame.K_BACKSPACE:  # Pause menu for Player 2
                    pauseMenu(score2, None, game_mode="1vs1")

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            x1_change = 0
            y1_change = 0
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            x1_change = 0
            y1_change = 0
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            x2_change = 0
            y2_change = 0
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            x2_change = 0
            y2_change = 0
        
        # Aggiornamento della posizione del serpente 1
        x1 += x1_change
        y1 += y1_change
        if x1 < 0:
            x1 = WIDTH - BLOCK_SIZE
        elif x1 >= WIDTH:
            x1 = 0
        if y1 < SCOREBOARD_HEIGHT:
            y1 = HEIGHT - BLOCK_SIZE
        elif y1 >= HEIGHT:
            y1 = SCOREBOARD_HEIGHT
        x1 = (x1 // BLOCK_SIZE) * BLOCK_SIZE
        y1 = (y1 // BLOCK_SIZE) * BLOCK_SIZE

        # Aggiornamento della posizione del serpente 2
        x2 += x2_change
        y2 += y2_change
        if x2 < 0:
            x2 = WIDTH - BLOCK_SIZE
        elif x2 >= WIDTH:
            x2 = 0
        if y2 < SCOREBOARD_HEIGHT:
            y2 = HEIGHT - BLOCK_SIZE
        elif y2 >= HEIGHT:
            y2 = SCOREBOARD_HEIGHT
        x2 = (x2 // BLOCK_SIZE) * BLOCK_SIZE
        y2 = (y2 // BLOCK_SIZE) * BLOCK_SIZE

        # Disegna la griglia
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (x, SCOREBOARD_HEIGHT), (x, HEIGHT))
        for y in range(SCOREBOARD_HEIGHT, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))
        
        # Disegna lo sfondo e il cibo
        draw_background()
        pygame.draw.circle(screen, BLACK, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        pygame.draw.circle(screen, WHITE, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2 - 2)

        # Gestione del cibo speciale
        if special_food_timer > 0:
            pygame.draw.circle(screen, BLACK, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
            pygame.draw.circle(screen, DARK_GREY, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2 -2)
            special_food_timer -= 1
        elif special_food_timer == 0 and random.randint(1, 100) == 1:
            special_foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_food_timer = 100
        
        # Disegna il serpente 1
        snake_Head1 = [x1, y1]
        snake_List1.append(snake_Head1)
        if len(snake_List1) > Length_of_snake1:
            del snake_List1[0]
        for block in snake_List1[:-1]:
            if block == snake_Head1:
                game_close = True

        our_snake(BLOCK_SIZE, snake_List1, player=1) 

        # Disegna il serpente 2
        snake_Head2 = [x2, y2]
        snake_List2.append(snake_Head2)
        if len(snake_List2) > Length_of_snake2:
            del snake_List2[0]
        for block in snake_List2[:-1]:
            if block == snake_Head2 or block == snake_Head1:
                game_close = True

        our_snake(BLOCK_SIZE, snake_List2, player=2) 

        # Aggiornamento della velocità e punteggio
        SPEED1, last_updated_score1 = update_speed(score1, CURRENT_DIFFICULTY, SPEED1, last_updated_score1)
        SPEED2, last_updated_score2 = update_speed(score2, CURRENT_DIFFICULTY, SPEED2, last_updated_score2)

        #draw_score_bar(score1, score2, CURRENT_DIFFICULTY)
        draw_score_bar(score1, score2, SPEED1, SPEED2, Length_of_snake1, Length_of_snake2, None, CURRENT_DIFFICULTY)

        
        # Controllo collisione con il cibo
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List1 + snake_List2)
            Length_of_snake1 += 1
            score1 += 1 * food_points_multiplier1  # Incremento del punteggio per il cibo normale
            score1 = round(score1, 1)

        if x2 == foodx and y2 == foody:
            foodx, foody = generate_food(snake_List1 + snake_List2)
            Length_of_snake2 += 1
            score2 += 1 * food_points_multiplier2  # Incremento del punteggio per il cibo normale
            score2 = round(score2, 1)

        if special_food_timer > 0 and x1 == special_foodx and y1 == special_foody:
            special_foodx, special_foody = None, None
            special_food_timer = 0
            Length_of_snake1 += 5
            score1 += 5 * special_food_points_multiplier1  # Incremento del punteggio per il cibo speciale
            score1 = round(score1, 1)

        if special_food_timer > 0 and x2 == special_foodx and y2 == special_foody:
            special_foodx, special_foody = None, None
            special_food_timer = 0
            Length_of_snake2 += 5
            score2 += 5 * special_food_points_multiplier2  # Incremento del punteggio per il cibo speciale
            score2 = round(score2, 1)


        # Aggiorna lo schermo
        pygame.display.update()
        clock.tick(min(SPEED1, SPEED2))  # Limita la velocità al più lento dei due giocatori
        check_for_special_effect_activation(score1, foodx, foody, player=1, game_mode="1vs1", mode_high_score = None)
        check_for_special_effect_activation(score2, foodx, foody, player=2, game_mode="1vs1", mode_high_score = None)
    pygame.quit()
    quit()

# Avvio del gioco
global_records = read_records()
gameMenu()