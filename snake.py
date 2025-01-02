import pygame
import time
import random
import os
import json

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

# Dimensioni della finestra di gioco
WIDTH, HEIGHT = 800, 600
GAME_HEIGHT = HEIGHT 
SCOREBOARD_HEIGHT = 50 

# Creazione della finestra di gioco
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Dimensione del blocco e velocità iniziale
BLOCK_SIZE = 20
SPEED = 10
global_records = 0

# Font utilizzati nel gioco
font_style = pygame.font.SysFont("bahnschrift", 30)
font_style_small = pygame.font.SysFont('Arial', 15)
title_font = pygame.font.SysFont("bahnschrift", 55)
CURRENT_DIFFICULTY = "Balanced"

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
        pygame.draw.rect(screen, bg_color, [x - 5, y - 5, text_width + 10, text_height + 10], border_radius=border_radius)
    
    screen.blit(text_surface, (x, y))

def draw_menu(title, options, selected_option, score=None, high_score=None, resolutions=None, is_fullscreen=None, all_high_scores=None):
    """Disegna un menu con il titolo e le opzioni fornite, evidenziando l'opzione selezionata."""
    draw_background()
    option_offset = 0

    if title in ["Pause Menu", "Game Over"] and score is not None and high_score is not None:
        draw_score_bar(score, high_score, CURRENT_DIFFICULTY)

    title_x = (WIDTH - title_font.render(title, True, GREEN).get_width()) // 2
    title_y = HEIGHT // 5
    draw_text_with_options(title, title_font, title_x, title_y, WHITE, BLACK, DARK_GREY)

    if title == "Change Resolution":
        current_resolution = (WIDTH, HEIGHT)
        if is_fullscreen:
            current_index = 4
        elif current_resolution == (1920, 1080):
            current_index = 3  
        else:
            current_index = resolutions.index(current_resolution) if current_resolution in resolutions else 4

    elif title == "Game Over":
        score_text = f"Your Score: {score}"
        score_width = font_style.render(score_text, True, GREEN).get_width()
        draw_text_with_options(
            score_text,
            font_style,
            (WIDTH - score_width) // 2,
            HEIGHT // 3,
            DARK_GREY,
            WHITE
        )
        
        high_score_text = f"High Score: {high_score}"
        high_score_width = font_style.render(high_score_text, True, GREEN).get_width()
        draw_text_with_options(
            high_score_text,
            font_style,
            (WIDTH - high_score_width) // 2,
            HEIGHT // 3 + 40,
            DARK_GREY,
            WHITE
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
            for i, score in enumerate(top_scores):
                record_text = f"{i + 1}. {score}"
                draw_text_with_options(record_text, large_font_style_small, 
                                       column_x + (column_width - large_font_style_small.size(record_text)[0]) // 2, 
                                       y_offset, record_color, BLACK)
                y_offset += 40
        option_offset = 300

    for i, option in enumerate(options):
        color = WHITE if i != selected_option else BLACK
        option_text = font_style.render(option, True, color)
        option_x = WIDTH // 2 - option_text.get_width() // 2
        option_y = HEIGHT // 3 + i * 50 + option_offset

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


def draw_score_bar(score, high_score, current_difficulty):
    """Disegna la barra del punteggio in alto nella finestra di gioco."""
    bar_height = 60
    pygame.draw.rect(screen, (50, 50, 50), [0, 0, WIDTH, bar_height])
    
    draw_text_with_options(f"Score: {score}", font_style, 15, 15, (255, 255, 255), (0, 0, 0))
    
    record_x = WIDTH - font_style.size(f"Record: {high_score}")[0] - 15
    draw_text_with_options(f"Record: {high_score}", font_style, record_x, 15, (255, 255, 255), (0, 0, 0))

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

def our_snake(block_size, snake_list):
    """Disegna il serpente sullo schermo."""
    for i, x in enumerate(snake_list):
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

def is_valid_food_position(x, y, snake_list):
    """Controlla se la posizione del cibo è valida (non collida con il serpente)."""
    for segment in snake_list:
        if segment == [x, y]:
            return False
    return True

def update_speed(score, CURRENT_DIFFICULTY, initial_speed, last_updated_score):
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
    if score - last_updated_score >= threshold:
        last_updated_score = score
        return initial_speed + (score // threshold) * speed_increment, last_updated_score
    return initial_speed + (last_updated_score // threshold) * speed_increment, last_updated_score

def update_records(records, mode, score):
    """Aggiorna i record con il nuovo punteggio per la modalità specificata."""
    if mode not in records:
        records[mode] = []
    records[mode].append(score)
    records[mode] = sorted(records[mode], reverse=True)
    records[mode] = records[mode][:3]
    
    return records

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
        json.dump(records, file)

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
        draw_menu("Snake Game", options, selected_option, score=None, high_score=None, resolutions=None, is_fullscreen=None, all_high_scores=None)
        pygame.display.update()

        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    menu = False
                    gameLoop()
                elif selected_option == 1:
                    showHighScore()
                elif selected_option == 2:
                    changeDifficulty()
                elif selected_option == 3:
                    changeResolution()
                elif selected_option == 4:
                    pygame.quit()
                    quit()

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

def pauseMenu(score, current_high_score):
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
                    gameLoop()
                elif selected_option == 2:
                    gameMenu()                
    return True

def gameOverMenu(score, mode_high_score):
    """Mostra il menu di fine gioco e gestisce la navigazione tra le opzioni."""
    game_close = True
    selected_option = 0
    options = ["Play Again", "Main Menu"]
    score_font = pygame.font.SysFont("bahnschrift", 30)
    records = read_records()
    mode_high_score = max(records[CURRENT_DIFFICULTY], default=0)
    while game_close:
        draw_menu("Game Over", options, selected_option, score, mode_high_score, resolutions=None, is_fullscreen=None, all_high_scores=None)
        pygame.display.update()

        # Gestisci input utente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            selected_option, confirmed = handle_menu_input(options, selected_option, event)
            if confirmed:
                if selected_option == 0:
                    gameLoop()
                elif selected_option == 1:
                    gameMenu()
    return True

#Funzione Principale
def gameLoop():
    """Gestisce il ciclo principale del gioco, inclusi movimento, collisioni e punteggio."""
    global global_records, CURRENT_DIFFICULTY, SPEED, last_updated_score
    game_over = False
    game_close = False
    x1 = WIDTH / 2
    y1 = HEIGHT / 2  
    x1_change = 0
    y1_change = 0
    direction = None
    snake_List = []
    Length_of_snake = 1
    foodx, foody = generate_food(snake_List)
    special_food_timer = 0
    special_foodx, special_foody = None, None
    score = 0
    last_updated_score = 0
    global_records = read_records()
    mode_high_score = max(global_records[CURRENT_DIFFICULTY], default=0)
    
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
            mode_high_score = max(global_records[CURRENT_DIFFICULTY], default=0)
            game_over = not gameOverMenu(score, mode_high_score)
            if not game_over:
                break  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mode_high_score = max(global_records[CURRENT_DIFFICULTY], default=0)
                    pauseMenu(score, mode_high_score)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
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
        SPEED = update_speed(score, CURRENT_DIFFICULTY, SPEED, last_updated_score)
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
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (x, SCOREBOARD_HEIGHT), (x, HEIGHT))
        for y in range(SCOREBOARD_HEIGHT, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))
        draw_background()
        pygame.draw.circle(screen, BLACK, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        pygame.draw.circle(screen, WHITE, (foodx + BLOCK_SIZE // 2, foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2 - 2)
        if special_food_timer > 0:
            pygame.draw.circle(screen, BLACK, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
            pygame.draw.circle(screen, DARK_GREY, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2 -2)
            special_food_timer -= 1
        elif special_food_timer == 0 and random.randint(1, 100) == 1:
            special_foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_food_timer = 100
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for block in snake_List[:-1]:
            if block == snake_Head:
                game_close = True
        our_snake(BLOCK_SIZE, snake_List)
        SPEED, last_updated_score = update_speed(score, CURRENT_DIFFICULTY, initial_speed, last_updated_score)
        draw_score_bar(score, mode_high_score, CURRENT_DIFFICULTY)
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1
            score += 1
        if special_food_timer > 0 and x1 == special_foodx and y1 == special_foody:
            special_foodx, special_foody = None, None
            special_food_timer = 0
            Length_of_snake += 5
            score += 5
        if score > max(global_records[CURRENT_DIFFICULTY], default=0):
            global_records = update_records(global_records, CURRENT_DIFFICULTY, score)
        write_records(global_records)
        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()
    quit()

# Avvio del gioco
global_records = read_records()
gameMenu()