import pygame
import time
import random
import os

pygame.init()

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
WIDTH, HEIGHT = 800, 600
GAME_HEIGHT = HEIGHT 
SCOREBOARD_HEIGHT = 50 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
BLOCK_SIZE = 20
SPEED = 15
RECORD = 0
font_style = pygame.font.SysFont("bahnschrift", 30)
title_font = pygame.font.SysFont("bahnschrift", 55)

def fade_out(duration=100):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(DARK_GREY)
    for alpha in range(0, 255, int(255 / (duration / 10))):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def fade_in(duration=100):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(DARK_GREY)
    for alpha in range(255, 0, -int(255 / (duration / 10))):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def draw_background():
    for y in range(HEIGHT):
        color = tuple(
            DARK_GREY[i] + (GREY[i] - DARK_GREY[i]) * y // HEIGHT for i in range(3)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def draw_text_with_outline(text, font, color, outline_color, x, y):
    text_surface = font.render(text, True, color)
    outline_surfaces = [font.render(text, True, outline_color) for _ in range(8)]
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]
    for offset, outline_surface in zip(offsets, outline_surfaces):
        screen.blit(outline_surface, (x + offset[0], y + offset[1]))
    screen.blit(text_surface, (x, y))

def draw_score_bar(score, record):
    bar_height = 60
    pygame.draw.rect(screen, (50, 50, 50), [0, 0, WIDTH, bar_height])
    draw_text_with_outline(f"Score: {score}", font_style, (255, 255, 255), (0, 0, 0), 15, 15)
    record_x = WIDTH - font_style.size(f"Record: {record}")[0] - 15
    draw_text_with_outline(f"Record: {record}", font_style, (255, 255, 255), (0, 0, 0), record_x, 15)

def read_record():
    try:
        with open("record.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def write_record(record):
    with open("record.txt", "w") as file:
        file.write(str(record))

def our_snake(block_size, snake_list):
    for i, x in enumerate(snake_list):
        color = (0, max(0, 255 - i * 5), 0)
        pygame.draw.rect(screen, (0, 0, 0), [x[0] - 2, x[1] - 2, block_size + 4, block_size + 4], border_radius=5)
        pygame.draw.rect(screen, color, [x[0], x[1], block_size, block_size], border_radius=5)

def is_valid_food_position(x, y, snake_list):
    for segment in snake_list:
        if segment == [x, y]:
            return False
    return True

def generate_food(snake_List):
    while True:
        food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(SCOREBOARD_HEIGHT, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        if is_valid_food_position(food_x, food_y, snake_List): 
            return food_x, food_y

def message(msg, color, position, font=font_style, bg_color=None):
    mesg = font.render(msg, True, color)
    x_pos = position[0] - mesg.get_width() // 2
    y_pos = position[1] - mesg.get_height() // 2
    if bg_color:
        pygame.draw.rect(screen, bg_color, [position[0] - 5, position[1] - 5, mesg.get_width() + 10, mesg.get_height() + 10])
    screen.blit(mesg, [x_pos, y_pos])

def gameMenu():
    menu = True
    selected_option = 0
    options = ["Play", "High Score", "Difficulty", "Quit"]
    while menu:
        draw_background()
        title_text = title_font.render("Snake Game", True, GREEN)
        title_width = title_text.get_width()
        title_x = (WIDTH - title_font.render("Snake Game", True, GREEN).get_width()) // 2
        title_y = HEIGHT // 5
        draw_text_with_outline("Snake Game", title_font, GREEN, BLACK, title_x, title_y)
        for i, option in enumerate(options):
            color = WHITE if i != selected_option else BLACK
            option_text = font_style.render(option, True, color)
            option_x = WIDTH // 2 - option_text.get_width() // 2
            option_y = HEIGHT // 3 + i * 50
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
            else:
                bg_color = None
            screen.blit(option_text, (option_x, option_y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    fade_out()  
                    if selected_option == 0:
                        menu = False
                        gameLoop()
                    elif selected_option == 1: 
                         showHighScore()
                    elif selected_option == 2:
                        changeDifficulty()
                    elif selected_option == 3:
                        pygame.quit()
                        quit()
                    fade_in()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    if WIDTH / 2 - 50 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 3 + i * 50 <= mouse_pos[1] <= HEIGHT / 3 + i * 50 + 30:
                        if option == "Play":
                            menu = False
                            gameLoop()
                        elif option == "High Score":
                            showHighScore()
                        elif option == "Difficulty":
                            changeDifficulty()
                        elif option == "Quit":
                            pygame.quit()
                            quit()

def showHighScore():
    high_score_menu = True
    selected_option = 0
    options = ["Back"]
    while high_score_menu:
        draw_background()
        title_text = title_font.render("High Score", True, ORANGE)
        draw_text_with_outline("High Scores", title_font, GREEN, BLACK, 
                           (WIDTH - title_font.render("High Scores", True, GREEN).get_width()) // 2, HEIGHT // 5)
        record_text = font_style.render(f"Current Record: {RECORD}", True, WHITE)
        draw_text_with_outline(f"Current Record: {RECORD}", font_style, DARK_GREY, WHITE, 
                           (WIDTH - record_text.get_width()) // 2, HEIGHT // 3)
        for i, option in enumerate(options):
            color = WHITE if i != selected_option else BLACK
            option_text = font_style.render(option, True, color)
            option_x = WIDTH // 2 - option_text.get_width() // 2
            option_y = HEIGHT // 2 + i * 50
            if i == selected_option:
                border_color = BLACK
                bg_color = WHITE
                pygame.draw.rect(screen, border_color, [option_x - 8, option_y - 8, option_text.get_width() + 16, option_text.get_height() + 16], border_radius=20)
                pygame.draw.rect(screen, bg_color, [option_x - 5, option_y - 5, option_text.get_width() + 10, option_text.get_height() + 10], border_radius=15)
            screen.blit(option_text, (option_x, option_y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:  
                    selected_option = (selected_option - 1) % len(options)
                elif event.key in [pygame.K_DOWN, pygame.K_s]: 
                    selected_option = (selected_option + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: 
                    fade_out()
                    if selected_option == 0: 
                        high_score_menu = False
                    fade_in()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    option_x = WIDTH // 2 - font_style.size(option)[0] // 2
                    option_y = HEIGHT // 2 + i * 50
                    option_width = font_style.size(option)[0]
                    option_height = font_style.size(option)[1]
                    if option_x <= mouse_pos[0] <= option_x + option_width and option_y <= mouse_pos[1] <= option_y + option_height:
                        fade_out()
                        if option == "Back":
                            high_score_menu = False
                        fade_in()

def changeDifficulty():
    difficulty_menu = True
    selected_option = 0
    options = ["Easy", "Normal", "Hard", "Back"]
    global SPEED
    while difficulty_menu:
        draw_background()
        title_text = title_font.render("Select Difficulty", True, DARK_BLUE)
        draw_text_with_outline("Difficulty", title_font, GREEN, BLACK, 
                           (WIDTH - title_font.render("Difficulty", True, GREEN).get_width()) // 2, HEIGHT // 5)
        for i, option in enumerate(options):
            color = WHITE if i != selected_option else BLACK
            option_text = font_style.render(option, True, color)
            option_x = WIDTH // 2 - option_text.get_width() // 2
            option_y = HEIGHT // 3 + i * 50
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
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    fade_out()
                    if selected_option == 0:
                        SPEED = 10
                        difficulty_menu = False
                    elif selected_option == 1:
                        SPEED = 15
                        difficulty_menu = False
                    elif selected_option == 2:
                        SPEED = 20
                        difficulty_menu = False
                    elif selected_option == 3:
                        difficulty_menu = False
                        gameMenu()
                    fade_in() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    option_width = font_style.size(option)[0]
                    option_height = font_style.size(option)[1]
                    option_x = WIDTH // 2 - option_width // 2
                    option_y = HEIGHT // 3 + i * 50
                    if option_x <= mouse_pos[0] <= option_x + option_width and option_y <= mouse_pos[1] <= option_y + option_height:
                        fade_out()
                        if option == "Easy":
                            SPEED = 10
                            difficulty_menu = False
                        elif option == "Normal":
                            SPEED = 15
                            difficulty_menu = False
                        elif option == "Hard":
                            SPEED = 20
                            difficulty_menu = FalseF
                        elif option == "Back":
                            difficulty_menu = False
                            gameMenu()
                        fade_in()

def pauseMenu(score, record):
    paused = True
    selected_option = 0
    options = ["Resume", "Restart", "Main Menu"]
    while paused:
        draw_background()
        draw_score_bar(score, record)
        pause_text = title_font.render("Paused", True, RED)
        draw_text_with_outline("Pause", title_font, GREEN, BLACK, 
                           (WIDTH - title_font.render("Pause", True, GREEN).get_width()) // 2, HEIGHT // 5)
        for i, option in enumerate(options):
            color = WHITE if i != selected_option else BLACK
            option_text = font_style.render(option, True, color)
            option_x = WIDTH // 2 - option_text.get_width() // 2
            option_y = HEIGHT // 3 + i * 50
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
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    fade_out()
                    if selected_option == 0: 
                        paused = False
                    elif selected_option == 1:  
                        gameLoop()
                    elif selected_option == 2: 
                        gameMenu()
                    fade_in()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    option_width = font_style.size(option)[0]
                    option_height = font_style.size(option)[1]
                    option_x = WIDTH // 2 - option_width // 2
                    option_y = HEIGHT // 3 + i * 60
                    if option_x <= mouse_pos[0] <= option_x + option_width and option_y <= mouse_pos[1] <= option_y + option_height:
                        fade_out()
                        if option == "Resume":
                            paused = False
                        elif option == "Restart":
                            gameLoop()
                        elif option == "Main Menu":
                            gameMenu()
                        fade_in()
    return True

def gameOverMenu(score, record):
    game_close = True
    selected_option = 0
    options = ["Play Again", "Main Menu"]
    score_font = pygame.font.SysFont("bahnschrift", 30)
    while game_close:
        draw_background()
        draw_text_with_outline("Game Over", title_font, RED, BLACK, 
                           (WIDTH - title_font.render("Game Over", True, GREEN).get_width()) // 2, HEIGHT // 5)
        score_text = f"Your Score: {score}"
        score_width = score_font.render(score_text, True, GREEN).get_width()
        draw_text_with_outline(score_text, score_font, DARK_GREY, WHITE, 
                            (WIDTH - score_width) // 2, HEIGHT // 3)
        record_text = f"High Score: {record}"
        record_width = score_font.render(record_text, True, GREEN).get_width()
        draw_text_with_outline(record_text, score_font, DARK_GREY, WHITE, 
                            (WIDTH - record_width) // 2, HEIGHT // 3 + 40)
        for i, option in enumerate(options):
            color = WHITE if i != selected_option else BLACK
            option_text = font_style.render(option, True, color)
            option_x = WIDTH // 2 - option_text.get_width() // 2
            option_y = HEIGHT // 2 + i * 60
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
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:  
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: 
                    fade_out()
                    if selected_option == 0: 
                        gameLoop()
                    elif selected_option == 1: 
                        gameMenu()
                    fade_in()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    if WIDTH / 2 - 60 <= mouse_pos[0] <= WIDTH / 2 + 150 and HEIGHT / 2 + i * 60 <= mouse_pos[1] <= HEIGHT / 2 + i * 60 + 30:
                        if option == "Play Again":
                            gameLoop()
                        elif option == "Main Menu":
                            gameMenu()
    return True

def gameLoop():
    global RECORD
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
    while not game_over:
        while game_close:
            game_over = not gameOverMenu(score, RECORD)
            if not game_over:
                break  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade_out()
                    pauseMenu(score, RECORD)
                    fade_in()
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
            pygame.draw.circle(screen, WHITE, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
            pygame.draw.circle(screen, BLACK, (special_foodx + BLOCK_SIZE // 2, special_foody + BLOCK_SIZE // 2), BLOCK_SIZE // 2 -2)
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
        draw_score_bar(score, RECORD)
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1
            score += 1
        if special_food_timer > 0 and x1 == special_foodx and y1 == special_foody:
            special_foodx, special_foody = None, None
            special_food_timer = 0
            Length_of_snake += 5
            score += 5
        if score > RECORD:
            RECORD = score
            write_record(RECORD)
        draw_score_bar(score, RECORD)
        pygame.display.update()
        clock.tick(SPEED)
    pygame.quit()
    quit()
RECORD = read_record()
gameMenu()
