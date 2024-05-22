import pygame
import sys
import random
import json

# Initialize Pygame
pygame.init()

# Define colors and font
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

# High Scores Handling
def load_high_scores():
    try:
        with open("high_scores.json", "r") as file:
            high_scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        high_scores = {"Easy": 0, "Normal": 0, "Hard": 0}
    return high_scores

def save_high_scores(high_scores):
    with open("high_scores.json", "w") as file:
        json.dump(high_scores, file, indent=4)

def update_high_score(difficulty, score):
    high_scores = load_high_scores()
    if score > high_scores[difficulty]:
        high_scores[difficulty] = score
        save_high_scores(high_scores)

# Check Collision
def check_collision(snake_body):
    head = snake_body[0]
    if head in snake_body[1:]:
        return True
    return False

# Change Difficulty
def change_difficulty(screen):
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
                    choosing_difficulty = False
                    return difficulties[current_selection]

        for i, option in enumerate(difficulties):
            color = green if i == current_selection else white
            label = font.render(option, True, color)
            screen.blit(label, (150, 100 + 30 * i))

        pygame.display.update()

# Show High Scores
def show_high_scores(screen):
    high_scores = load_high_scores()
    screen.fill(black)
    y_pos = 100
    for difficulty, score in high_scores.items():
        score_text = font.render(f"{difficulty} High Score: {score}", True, white)
        screen.blit(score_text, (150, y_pos))
        y_pos += 30
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Main Game Function
def main_game(screen, difficulty):
    snake_speed = {"Easy": 5, "Normal": 10, "Hard": 15}[difficulty]
    snake_pos = [300, 300]
    snake_body = [[300, 300], [290, 300], [280, 300]]
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
            update_high_score(difficulty, score)
            break

        screen.fill(black)
        for block in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], 10, 10))
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(snake_speed)

    show_menu(screen)

# Main Menu
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
                        main_game(screen, "Normal")  # Default to Normal if not set
                    elif menu_options[current_selection] == "Change Difficulty":
                        difficulty = change_difficulty(screen)
                        main_game(screen, difficulty)
                    elif menu_options[current_selection] == "View Highscores":
                        show_high_scores(screen)
                    elif menu_options[current_selection] == "Quit":
                        pygame.quit()
                        sys.exit()

        for i, option in enumerate(menu_options):
            color = green if i == current_selection else white
            label = font.render(option, True, color)
            screen.blit(label, (150, 100 + 30 * i))

        pygame.display.update()

# Set up the initial game display and start the menu
screen = pygame.display.set_mode((600, 600))
show_menu(screen)
