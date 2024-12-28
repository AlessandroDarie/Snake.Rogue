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


WIDTH, HEIGHT = 800, 600
GAME_HEIGHT = HEIGHT 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

BLOCK_SIZE = 20

SPEED = 15
RECORD = 0

font_style = pygame.font.SysFont("bahnschrift", 30)
title_font = pygame.font.SysFont("bahnschrift", 40)

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
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])

def message(msg, color, position, font=font_style, bg_color=None):
    mesg = font.render(msg, True, color)
    if bg_color:
        pygame.draw.rect(screen, bg_color, [position[0] - 5, position[1] - 5, mesg.get_width() + 10, mesg.get_height() + 10])
    screen.blit(mesg, position)

def gameMenu():
    menu = True
    selected_option = 0
    options = ["Play","High Score", "Difficulty", "Quit"]

    while menu:
        screen.fill(BLACK)
        message("Snake Game", GREEN, [WIDTH / 2 - 100, HEIGHT / 5], font=title_font)

        for i, option in enumerate(options):
            color = WHITE if i != selected_option else YELLOW
            message(option, color, [WIDTH / 2 - 50, HEIGHT / 3 + i * 50])

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
    options = ["Back"]  # Aggiungiamo altre opzioni in futuro se necessario

    while high_score_menu:
        screen.fill(BLACK)

        title_text = title_font.render("High Score", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 5))

        record_text = font_style.render(f"Current Record: {RECORD}", True, WHITE)
        screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, HEIGHT // 3))

        for i, option in enumerate(options):
            color = WHITE if i != selected_option else YELLOW
            option_text = font_style.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 50))

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
                    if selected_option == 0: 
                        high_score_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    if WIDTH / 2 - 50 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 1.5 + i * 50 <= mouse_pos[1] <= HEIGHT / 1.5 + i * 50 + 30:
                        if option == "Back":
                            high_score_menu = False



def changeDifficulty():
    difficulty_menu = True
    selected_option = 0
    options = ["Easy", "Normal", "Hard", "Back"]
    global SPEED

    while difficulty_menu:
        screen.fill(BLACK)
        message("Select Difficulty", GREEN, [WIDTH / 2 - 150, HEIGHT / 5], font=title_font)

        for i, option in enumerate(options):
            color = WHITE if i != selected_option else YELLOW
            message(option, color, [WIDTH / 2 - 50, HEIGHT / 3 + i * 50])

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    if WIDTH / 2 - 50 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 3 + i * 50 <= mouse_pos[1] <= HEIGHT / 3 + i * 50 + 30:
                        if option == "Easy":
                            SPEED = 10
                            difficulty_menu = False
                        elif option == "Normal":
                            SPEED = 15
                            difficulty_menu = False
                        elif option == "Hard":
                            SPEED = 20
                            difficulty_menu = False
                        elif option == "Back":
                            difficulty_menu = False
                            gameMenu()

def pause_menu():
    paused = True
    options = ["Continue", "Change Difficulty", "Main Menu"]
    selected_option = 0

    while paused:
        screen.fill(BLACK)
        message("Paused", GREEN, [WIDTH / 2 - 50, HEIGHT / 4], font=title_font)

        for i, option in enumerate(options):
            color = WHITE if i != selected_option else YELLOW
            message(option, color, [WIDTH / 2 - 50, HEIGHT / 3 + i * 50])

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
                    if selected_option == 0:
                        paused = False
                    elif selected_option == 1:
                        changeDifficulty()
                    elif selected_option == 2:
                        gameMenu()
                elif event.key == pygame.K_ESCAPE:
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    if WIDTH / 2 - 50 <= mouse_pos[0] <= WIDTH / 2 + 100 and HEIGHT / 3 + i * 50 <= mouse_pos[1] <= HEIGHT / 3 + i * 50 + 30:
                        if option == "Continue":
                            paused = False
                        elif option == "Change Difficulty":
                            changeDifficulty()
                        elif option == "Main Menu":
                            gameMenu()

def gameOverMenu(score, record):
    game_close = True
    selected_option = 0
    options = ["Play Again", "Main Menu"]

    while game_close:
        screen.fill(BLACK)
        message("Game Over", RED, [WIDTH / 2 - 100, HEIGHT / 4], font=title_font)
        message(f"Your Score: {score}", WHITE, [WIDTH / 2 - 100, HEIGHT / 3])
        message(f"High Score: {record}", WHITE, [WIDTH / 2 - 100, HEIGHT / 3 + 40])

        for i, option in enumerate(options):
            color = WHITE if i != selected_option else YELLOW
            message(option, color, [WIDTH / 2 - 60, HEIGHT / 2 + i * 60])

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
                    if selected_option == 0: 
                        gameLoop()
                    elif selected_option == 1: 
                        gameMenu()
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

    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

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
                    pause_menu()
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

        if x1 >= WIDTH:
            x1 = 0
        elif x1 < 0:
            x1 = WIDTH - BLOCK_SIZE
        if y1 >= HEIGHT:  
            y1 = 0
        elif y1 < 0:  
            y1 = HEIGHT - BLOCK_SIZE

        x1 += x1_change
        y1 += y1_change

        screen.fill(BLACK)

        pygame.draw.rect(screen, BLUE, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        if special_food_timer > 0:
            pygame.draw.rect(screen, RED, [special_foodx, special_foody, BLOCK_SIZE, BLOCK_SIZE])
            special_food_timer -= 1
        elif special_food_timer == 0 and random.randint(1, 100) == 1:
            special_foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            special_food_timer = 100

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for block in snake_List[:-1]:
            if block == snake_Head:
                game_close = True

        our_snake(BLOCK_SIZE, snake_List)

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            Length_of_snake += 1
            score += 1

        if special_food_timer > 0 and x1 == special_foodx and y1 == special_foody:
            special_foodx, special_foody = None, None
            special_food_timer = 0
            Length_of_snake += 5
            score += 5

        message(f"Score: {score}", WHITE, [10, 10], font=font_style)
        high_score_text = font_style.render(f"High Score: {RECORD}", True, WHITE)
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

        if score > RECORD:
            RECORD = score
            write_record(RECORD)

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()
    quit()

RECORD = read_record()

gameMenu()
