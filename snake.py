import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define colors and font
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Define a global variable for snake speed
snake_speed = 10

def check_collision(snake_body):
    head = snake_body[0]
    if head in snake_body[1:]:
        return True
    return False

def change_difficulty(screen):
    global snake_speed
    difficulties = ["Easy", "Normal", "Hard"]
    current_selection = 0
    choosing_difficulty = True

    while choosing_difficulty:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    if difficulties[current_selection] == "Easy":
                        snake_speed = 10
                    elif difficulties[current_selection] == "Normal":
                        snake_speed = 15
                    elif difficulties[current_selection] == "Hard":
                        snake_speed = 20
                    choosing_difficulty = False
                    break

        for i, option in enumerate(difficulties):
            color = green if i == current_selection else white
            label = font.render(option, True, color)
            screen.blit(label, (150, 100 + 30 * i))

        pygame.display.update()

def show_menu(screen):
    menu_options = ["New Game", "Change Difficulty", "View Highscores", "Quit"]
    current_selection = 0
    menu_running = True

    while menu_running:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[current_selection] == "New Game":
                        main_game(screen)
                        menu_running = False
                    elif menu_options[current_selection] == "Change Difficulty":
                        change_difficulty(screen)
                    elif menu_options[current_selection] == "Quit":
                        pygame.quit()
                        sys.exit()

        for i, option in enumerate(menu_options):
            color = green if i == current_selection else white
            label = font.render(option, True, color)
            screen.blit(label, (150, 100 + 30 * i))

        pygame.display.update()

def main_game(screen):
    global snake_speed
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, 60)*10, random.randrange(1, 60)*10]
    food_spawn = True
    dx, dy = 0, -10
    score = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy != 10:
                    dx, dy = 0, -10
                elif event.key == pygame.K_DOWN and dy != -10:
                    dx, dy = 0, 10
                elif event.key == pygame.K_LEFT and dx != 10:
                    dx, dy = -10, 0
                elif event.key == pygame.K_RIGHT and dx != -10:
                    dx, dy = 10, 0

        snake_pos[0] += dx
        snake_pos[1] += dy
        snake_pos[0] %= 600
        snake_pos[1] %= 600
        snake_body.insert(0, list(snake_pos))
        if snake_body[0] == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, 60)*10, random.randrange(1, 60)*10]
            food_spawn = True

        if check_collision(snake_body):
            break

        screen.fill(black)
        for block in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], 10, 10))
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(snake_speed)

    show_menu(screen)

# Initialize the game display and start the menu
screen = pygame.display.set_mode((600, 600))
show_menu(screen)