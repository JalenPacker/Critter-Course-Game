import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
GRID_SIZE = 40
STAGES = 4
COLORS = [(200, 200, 255), (200, 255, 200), (255, 200, 200), (255, 255, 200)]
EXIT_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 48
LARGE_FONT_SIZE = 72
MOVE_INCREMENT = GRID_SIZE // 5  # Increased speed
EXIT_COLLISION_RADIUS = GRID_SIZE
ENEMY_SCALE_FACTOR = 2.5
STAGE_TIMES = [120, 90, 90, 90]  # Reduced time limit for each stage in seconds

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Critter Course')

# Fonts
font = pygame.font.SysFont(None, FONT_SIZE)
large_font = pygame.font.SysFont(None, LARGE_FONT_SIZE)
small_font = pygame.font.SysFont(None, 36)

# Load images
hamster_image = pygame.image.load('hamster.png')
hamster_image = pygame.transform.scale(hamster_image, (int(GRID_SIZE * 0.8), int(GRID_SIZE * 0.8)))

lock_image = pygame.image.load('lock.png')
lock_image = pygame.transform.scale(lock_image, (int(GRID_SIZE * 0.8), int(GRID_SIZE * 0.8)))

key_image = pygame.image.load('key.png')
key_image = pygame.transform.scale(key_image, (int(GRID_SIZE * 0.8), int(GRID_SIZE * 0.8)))

enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (int(GRID_SIZE * 0.8 * ENEMY_SCALE_FACTOR), int(GRID_SIZE * 0.8 * ENEMY_SCALE_FACTOR)))

win_image = pygame.image.load('win.png')  # Add your winning screen image file
lose_image = pygame.image.load('lose.png')  # Add your losing screen image file

# Button images (placeholders)
start_button_image = pygame.image.load('start_button.png')
instructions_button_image = pygame.image.load('instructions_button.png')
credits_button_image = pygame.image.load('credits_button.png')
background_image = pygame.image.load('background.png')
back_button_image = pygame.image.load('back_button.png')

# Button positions
start_button_rect = start_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
instructions_button_rect = instructions_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
credits_button_rect = credits_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
back_button_rect = back_button_image.get_rect(topleft=(50, SCREEN_HEIGHT - 200))

# Functions to handle game stages
def generate_maze_with_unique_path():
    width, height = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
    maze = [[1 for _ in range(height)] for _ in range(width)]
    start = (0, 0)
    end = (width - 1, height - 1)

    def create_path(maze, start, end):
        path = [start]
        current = start
        while current != end:
            x, y = current
            maze[x][y] = 0
            if x < end[0] and random.random() > 0.5:
                current = (x + 1, y)
            elif y < end[1]:
                current = (x, y + 1)
            else:
                current = (x + 1, y)
            path.append(current)
        maze[end[0]][end[1]] = 0
        return path

    path = create_path(maze, start, end)

    def add_obstacles(maze, path):
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if (i, j) not in path and random.random() < 0.3:
                    maze[i][j] = 1
                else:
                    maze[i][j] = 0

    add_obstacles(maze, path)
    return maze

def draw_stage(maze, stage):
    screen.fill(COLORS[stage - 1])
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_hamster(hamster_pos):
    screen.blit(hamster_image, (hamster_pos[0] - GRID_SIZE * 0.4, hamster_pos[1] - GRID_SIZE * 0.4))

def draw_exit(exit_pos):
    pygame.draw.rect(screen, EXIT_COLOR, (exit_pos[0] - GRID_SIZE / 2, exit_pos[1] - GRID_SIZE / 2, GRID_SIZE, GRID_SIZE))

def draw_lock(lock_pos):
    screen.blit(lock_image, (lock_pos[0] - GRID_SIZE * 0.4, lock_pos[1] - GRID_SIZE * 0.4))

def draw_key(key_pos):
    screen.blit(key_image, (key_pos[0] - GRID_SIZE * 0.4, key_pos[1] - GRID_SIZE * 0.4))

def draw_enemy(enemy_pos):
    screen.blit(enemy_image, (enemy_pos[0] - GRID_SIZE * 0.8 * ENEMY_SCALE_FACTOR / 2, enemy_pos[1] - GRID_SIZE * 0.8 * ENEMY_SCALE_FACTOR / 2))

def draw_instructions(stage):
    if stage == 1:
        instructions = "Stage 1: Reach the exit."
    elif stage == 2:
        instructions = "Stage 2: Collect the KEY to unlock the EXIT."
    elif stage == 3:
        instructions = "Stage 3: Collect 2 KEYS to unlock the EXIT."
    elif stage == 4:
        instructions = "Stage 4: Collect 3 KEYS and avoid ENEMY HANDS to WIN!"
    text_surface = font.render(instructions, True, BLUE)
    text_rect = text_surface.get_rect(topleft=(10, SCREEN_HEIGHT - 70))
    pygame.draw.rect(screen, WHITE, text_rect)  # Draw background for text
    screen.blit(text_surface, text_rect.topleft)

def draw_timer(time_left):
    timer_text = font.render(f"Time left: {int(time_left)}s", True, RED)
    screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 20, 20))

def draw_key_collected(stage, keys_collected):
    if stage >= 2:
        keys_text = f"Keys collected: {keys_collected}"
        text_surface = font.render(keys_text, True, GREEN)
        text_rect = text_surface.get_rect(midtop=(SCREEN_WIDTH // 2, 50))
        pygame.draw.rect(screen, WHITE, text_rect)  # Draw background for text
        screen.blit(text_surface, text_rect.topleft)

def check_collision(hamster_pos, maze):
    x, y = hamster_pos
    grid_x, grid_y = int(x // GRID_SIZE), int(y // GRID_SIZE)

    corners = [
        (x - GRID_SIZE * 0.4, y - GRID_SIZE * 0.4),
        (x + GRID_SIZE * 0.4, y - GRID_SIZE * 0.4),
        (x - GRID_SIZE * 0.4, y + GRID_SIZE * 0.4),
        (x + GRID_SIZE * 0.4, y + GRID_SIZE * 0.4)
    ]

    for corner_x, corner_y in corners:
        corner_grid_x, corner_grid_y = int(corner_x // GRID_SIZE), int(corner_y // GRID_SIZE)
        if 0 <= corner_grid_x < len(maze) and 0 <= corner_grid_y < len(maze[0]):
            if maze[corner_grid_x][corner_grid_y] == 1:
                return True
    return False

def check_bounds(hamster_pos, exit_pos):
    x, y = hamster_pos
    exit_x, exit_y = exit_pos
    if (x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT) and not (abs(x - exit_x) < EXIT_COLLISION_RADIUS and abs(y - exit_y) < EXIT_COLLISION_RADIUS):
        return True
    return False

def check_win(hamster_pos, exit_pos, stage):
    if abs(hamster_pos[0] - exit_pos[0]) < EXIT_COLLISION_RADIUS and abs(hamster_pos[1] - exit_pos[1]) < EXIT_COLLISION_RADIUS:
        if stage < STAGES:
            return stage + 1, [GRID_SIZE // 2, GRID_SIZE // 2], generate_maze_with_unique_path()
        else:
            return None, None, None
    return stage, hamster_pos, None

def check_lock(hamster_pos, lock_pos):
    if abs(hamster_pos[0] - lock_pos[0]) < GRID_SIZE / 2 and abs(hamster_pos[1] - lock_pos[1]) < GRID_SIZE / 2:
        return True
    return False

def check_key(hamster_pos, key_pos):
    if abs(hamster_pos[0] - key_pos[0]) < GRID_SIZE / 2 and abs(hamster_pos[1] - key_pos[1]) < GRID_SIZE / 2:
        return True
    return False

def check_enemy_collision(hamster_pos, enemy_pos):
    if abs(hamster_pos[0] - enemy_pos[0]) < GRID_SIZE * 0.8 * ENEMY_SCALE_FACTOR / 2 and abs(hamster_pos[1] - enemy_pos[1]) < GRID_SIZE * 0.8 * ENEMY_SCALE_FACTOR / 2:
        return True
    return False

def move_enemy(enemy_pos, maze):
    directions = [(0, -MOVE_INCREMENT), (0, MOVE_INCREMENT), (-MOVE_INCREMENT, 0), (MOVE_INCREMENT, 0)]
    random.shuffle(directions)
    for direction in directions:
        new_pos = [enemy_pos[0] + direction[0], enemy_pos[1] + direction[1]]
        if 0 <= new_pos[0] < SCREEN_WIDTH and 0 <= new_pos[1] < SCREEN_HEIGHT:
            grid_x, grid_y = int(new_pos[0] // GRID_SIZE), int(new_pos[1] // GRID_SIZE)
            if maze[grid_x][grid_y] == 0:
                return new_pos
    return enemy_pos

def show_start_screen():
    screen.blit(background_image, (0, 0))
    title_text = large_font.render("Critter Course", True, BLUE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 300))
    screen.blit(start_button_image, start_button_rect)
    screen.blit(instructions_button_image, instructions_button_rect)
    screen.blit(credits_button_image, credits_button_rect)
    pygame.display.flip()

def show_instructions_screen():
    screen.fill(GRAY)
    instructions_text = [
        "Instructions:",
        "1. Use W, A, S, D to move the hamster.",
        "2. Navigate through the maze and reach the green exit.",
        "3. Collect all necessary keys to unlock some exits.",
        "4. Avoid enemies in the final stage."
    ]

    y = 100
    for line in instructions_text:
        text_surface = small_font.render(line, True, BLUE)
        screen.blit(text_surface, (50, y))
        y += 50
    screen.blit(back_button_image, back_button_rect)
    pygame.display.flip()

def show_credits_screen():
    screen.fill(GRAY)
    credits_text = [
        "Credits:",
        "Edwin Rodriguez..........Concept Artist",
        "Ralph Mutai................Product Lead",
        "Jalen Packer.................Programmer",
        "Fabian Mcghee................Programmer"
    ]

    y = 100
    for line in credits_text:
        text_surface = small_font.render(line, True, BLUE)
        screen.blit(text_surface, (50, y))
        y += 50
    screen.blit(back_button_image, back_button_rect)
    pygame.display.flip()

def show_win_screen():
    screen.fill(WHITE)
    screen.blit(win_image, (SCREEN_WIDTH // 2 - win_image.get_width() // 2, SCREEN_HEIGHT // 2 - win_image.get_height() // 2))
    win_text = large_font.render("You Win!", True, BLUE)
    screen.blit(win_text, (SCREEN_WIDTH - win_text.get_width() - 20, 20))
    pygame.display.flip()
    pygame.time.wait(3000)

def show_lose_screen():
    screen.fill(WHITE)
    screen.blit(lose_image, (SCREEN_WIDTH // 2 - lose_image.get_width() // 2, SCREEN_HEIGHT // 2 - lose_image.get_height() // 2))
    lose_text = large_font.render("You Lose!", True, RED)
    screen.blit(lose_text, (SCREEN_WIDTH - lose_text.get_width() - 20, 20))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
def main():
    running = True
    in_start_screen = True
    in_instructions_screen = False
    in_credits_screen = False
    stage = 1
    hamster_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
    exit_pos = [SCREEN_WIDTH - GRID_SIZE // 2, SCREEN_HEIGHT - GRID_SIZE // 2]
    maze = generate_maze_with_unique_path()
    lock_pos = [0, 0]
    key1_pos = [0, 0]
    key2_pos = [0, 0]
    key3_pos = [0, 0]
    enemy1_pos = [0, 0]
    enemy2_pos = [0, 0]
    lock_collected = False
    key1_collected = False
    key2_collected = False
    key3_collected = False
    velocity = [0, 0]
    time_left = STAGE_TIMES[stage - 1]
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(30) / 1000.0  # Amount of seconds between each loop
        time_left -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if in_start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if start_button_rect.collidepoint(x, y):
                        in_start_screen = False
                    elif instructions_button_rect.collidepoint(x, y):
                        in_start_screen = False
                        in_instructions_screen = True
                    elif credits_button_rect.collidepoint(x, y):
                        in_start_screen = False
                        in_credits_screen = True

            if in_instructions_screen or in_credits_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if back_button_rect.collidepoint(x, y):
                        in_instructions_screen = False
                        in_credits_screen = False
                        in_start_screen = True

        if in_start_screen:
            show_start_screen()
        elif in_instructions_screen:
            show_instructions_screen()
        elif in_credits_screen:
            show_credits_screen()
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                velocity[1] = -MOVE_INCREMENT
            elif keys[pygame.K_s]:
                velocity[1] = MOVE_INCREMENT
            else:
                velocity[1] = 0
            if keys[pygame.K_a]:
                velocity[0] = -MOVE_INCREMENT
            elif keys[pygame.K_d]:
                velocity[0] = MOVE_INCREMENT
            else:
                velocity[0] = 0

            next_pos = [hamster_pos[0] + velocity[0], hamster_pos[1] + velocity[1]]

            if not check_collision(next_pos, maze) and not check_bounds(next_pos, exit_pos):
                hamster_pos = next_pos

            if stage == 2 and not lock_collected:
                if check_lock(hamster_pos, lock_pos):
                    lock_collected = True

            keys_collected = 0
            if stage == 3 or stage == 4:
                if not key1_collected:
                    if check_key(hamster_pos, key1_pos):
                        key1_collected = True
                if not key2_collected:
                    if check_key(hamster_pos, key2_pos):
                        key2_collected = True
                if stage == 4 and not key3_collected:
                    if check_key(hamster_pos, key3_pos):
                        key3_collected = True

                keys_collected = key1_collected + key2_collected + key3_collected

            if stage == 4:
                if check_enemy_collision(hamster_pos, enemy1_pos) or check_enemy_collision(hamster_pos, enemy2_pos):
                    show_lose_screen()
                    running = False

            if (lock_collected or stage != 2) and (key1_collected and key2_collected or stage != 3) and (key1_collected and key2_collected and key3_collected or stage != 4):
                stage, hamster_pos, new_maze = check_win(hamster_pos, exit_pos, stage)
                if stage is None:
                    show_win_screen()
                    break
                if new_maze:
                    maze = new_maze
                    time_left = STAGE_TIMES[stage - 1]
                    if stage == 2:
                        while True:
                            lock_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                        random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[lock_pos[0] // GRID_SIZE][lock_pos[1] // GRID_SIZE]:
                                break
                        lock_collected = False
                    if stage == 3:
                        while True:
                            key1_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                        random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[key1_pos[0] // GRID_SIZE][key1_pos[1] // GRID_SIZE]:
                                break
                        while True:
                            key2_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                        random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[key2_pos[0] // GRID_SIZE][key2_pos[1] // GRID_SIZE]:
                                break
                        key1_collected = False
                        key2_collected = False
                    if stage == 4:
                        while True:
                            key1_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                        random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[key1_pos[0] // GRID_SIZE][key1_pos[1] // GRID_SIZE]:
                                break
                        while True:
                            key2_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                        random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[key2_pos[0] // GRID_SIZE][key2_pos[1] // GRID_SIZE]:
                                break
                        while True:
                            key3_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                        random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[key3_pos[0] // GRID_SIZE][key3_pos[1] // GRID_SIZE]:
                                break
                        while True:
                            enemy1_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                          random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[enemy1_pos[0] // GRID_SIZE][enemy1_pos[1] // GRID_SIZE]:
                                break
                        while True:
                            enemy2_pos = [random.randint(1, (SCREEN_WIDTH // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2,
                                          random.randint(1, (SCREEN_HEIGHT // GRID_SIZE) - 2) * GRID_SIZE + GRID_SIZE // 2]
                            if not maze[enemy2_pos[0] // GRID_SIZE][enemy2_pos[1] // GRID_SIZE]:
                                break
                        key1_collected = False
                        key2_collected = False
                        key3_collected = False

            if stage == 4:
                enemy1_pos = move_enemy(enemy1_pos, maze)
                enemy2_pos = move_enemy(enemy2_pos, maze)

            if time_left <= 0:
                show_lose_screen()
                running = False

            draw_stage(maze, stage)
            draw_hamster(hamster_pos)
            draw_exit(exit_pos)
            if stage == 2 and not lock_collected:
                draw_lock(lock_pos)
            if stage == 3 and not key1_collected:
                draw_key(key1_pos)
            if stage == 3 and not key2_collected:
                draw_key(key2_pos)
            if stage == 4:
                if not key1_collected:
                    draw_key(key1_pos)
                if not key2_collected:
                    draw_key(key2_pos)
                if not key3_collected:
                    draw_key(key3_pos)
                draw_enemy(enemy1_pos)
                draw_enemy(enemy2_pos)
            draw_instructions(stage)
            draw_timer(time_left)
            draw_key_collected(stage, keys_collected)
            pygame.display.flip()

# Start the game
main()
pygame.quit()
