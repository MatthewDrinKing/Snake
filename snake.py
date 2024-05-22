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

# Pause Menu
def pause_menu(screen):
    menu_options = ["Continue", "Restart", "Quit to Main Menu"]
    current_selection = 0
    paused = True

    while paused:
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
                    if menu_options[current_selection] == "Continue":
                        paused = False
                    elif menu_options[current_selection] == "Restart":
                        return "Restart"
                    elif menu_options[current_selection] == "Quit to Main Menu":
                        return "Quit"

        for i, option in enumerate(menu_options):
            color = green if i == current_selection else white
            label = font.render(option, True, color)
            screen.blit(label, (150, 100 + 30 * i))

        pygame.display.update()

# Generate Food
def generate_food(snake_body):
    while True:
        food_pos = [random.randrange(1, 60)*10, random.randrange(1, 60)*10]
        if food_pos not in snake_body:
            return food_pos

# Main Game Function
def main_game(screen, difficulty):
    snake_speed = {"Easy": 5, "Normal": 10, "Hard": 15}[difficulty]
    snake_pos = [300, 300]
    snake_body = [[300, 300], [290, 300], [280, 300]]
    food_pos = generate_food(snake_body)
    food_spawn = True
    dx, dy = 0, -10
    score = 0
    high_scores = load_high_scores()
    high_score = high_scores[difficulty]
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
                elif event.key == pygame.K_ESCAPE:
                    action = pause_menu(screen)
                    if action == "Restart":
                        main_game(screen, difficulty)
                    elif action == "Quit":
                        show_menu(screen)
                        return

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
            food_pos = generate_food(snake_body)
            food_spawn = True

        if check_collision(snake_body):
            update_high_score(difficulty, score)
            break

        screen.fill(black)
        for block in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], 10, 10))
        
        # Draw the snake's face
        head = snake_body[0]
        eye_size = 2
        eye_color = white
        if dx == 10:  # Moving right
            eye1_pos = (head[0] + 8, head[1] + 2)
            eye2_pos = (head[0] + 8, head[1] + 8)
        elif dx == -10:  # Moving left
            eye1_pos = (head[0] + 2, head[1] + 2)
            eye2_pos = (head[0] + 2, head[1] + 8)
        elif dy == 10:  # Moving down
            eye1_pos = (head[0] + 2, head[1] + 8)
            eye2_pos = (head[0] + 8, head[1] + 8)
        elif dy == -10:  # Moving up
            eye1_pos = (head[0] + 2, head[1] + 2)
            eye2_pos = (head[0] + 8, head[1] + 2)
        pygame.draw.circle(screen, eye_color, eye1_pos, eye_size)
        pygame.draw.circle(screen, eye_color, eye2_pos, eye_size)
        
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        score_text = font.render(f"Score: {score}", True, white)
        high_score_text = font.render(f"High Score: {high_score}", True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

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