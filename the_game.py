import pygame
import random
import time
from collections import deque
import sys

# Initialize Pygame
pygame.init()

# Music settings
pygame.mixer.music.load("background music.mp3")  # Add your background music file here
pygame.mixer.music.set_volume(0.3)  # Set the music volume
pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

# Load sound effects
solve_sound = pygame.mixer.Sound("correct.mp3")  # Sound effect for solving the maze
lose_sound = pygame.mixer.Sound('loss sound.mp3')  # Sound effect when you lose

# Colors
WHITE = (255, 255, 255)
GREY = (30, 30, 30)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Start point
GREEN = (0, 255, 0)  # End point
BLUE = (0, 0, 255)  # Player
PURPLE = (100, 0, 100)  # Button
LIGHT_RED = (255, 100, 100)  # DFS path
LIGHT_GREEN = (144, 238, 144)  # BFS path

# Screen settings
CELL_SIZE = 25
COLS = 20
ROWS = 20
SCREEN_HEIGHT = ROWS * CELL_SIZE + 100  # Extra space for UI
SCREEN_WIDTH = COLS * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("game.png")  # Photo for the game
pygame.display.set_caption("Maze Solver")  # Game name
pygame.display.set_icon(icon)

background = pygame.image.load("game_background.png")  # Photo for the background

# Font and clock
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72)  # Font for large text
clock = pygame.time.Clock()

# Game variables
difficulty = 1
time_limit = 180  # 3 minutes
player_x, player_y = 0, 0
win = False
game_over = False
start_time = time.time()

# Cell class for maze
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True]  # Top, Right, Bottom, Left

    def draw(self):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE + 100
        if self.walls[0]:  # Top
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y))
        if self.walls[1]:  # Right
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
        if self.walls[2]:  # Bottom
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE))
        if self.walls[3]:  # Left
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x, y))

# Function to generate the maze
def generate_maze():
    global grid, stack, current_cell
    grid = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]
    stack = []
    current_cell = grid[0][0]
    current_cell.visited = True

    while True:
        next_cell = get_random_neighbor(current_cell)
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break

def remove_walls(a, b):
    dx, dy = a.x - b.x, a.y - b.y
    if dx == 1:  # Left
        a.walls[3] = b.walls[1] = False
    elif dx == -1:  # Right
        a.walls[1] = b.walls[3] = False
    if dy == 1:  # Top
        a.walls[0] = b.walls[2] = False
    elif dy == -1:  # Bottom
        a.walls[2] = b.walls[0] = False

def get_random_neighbor(cell):
    neighbors = []
    if cell.y > 0 and not grid[cell.y - 1][cell.x].visited:
        neighbors.append(grid[cell.y - 1][cell.x])  # Top
    if cell.x < COLS - 1 and not grid[cell.y][cell.x + 1].visited:
        neighbors.append(grid[cell.y][cell.x + 1])  # Right
    if cell.y < ROWS - 1 and not grid[cell.y + 1][cell.x].visited:
        neighbors.append(grid[cell.y + 1][cell.x])  # Bottom
    if cell.x > 0 and not grid[cell.y][cell.x - 1].visited:
        neighbors.append(grid[cell.y][cell.x - 1])  # Left
    return random.choice(neighbors) if neighbors else None

# Pathfinding algorithms
def bfs(start, end):
    queue = deque([start])
    visited = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)
    return reconstruct_path(visited, end)

def dfs(start, end):
    stack = [start]
    visited = {start: None}
    while stack:
        current = stack.pop()
        if current == end:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited[neighbor] = current
                stack.append(neighbor)
    return reconstruct_path(visited, end)

def get_neighbors(cell):
    neighbors = []
    x, y = cell.x, cell.y
    if y > 0 and not cell.walls[0]:  # Top
        neighbors.append(grid[y - 1][x])
    if x < COLS - 1 and not cell.walls[1]:  # Right
        neighbors.append(grid[y][x + 1])
    if y < ROWS - 1 and not cell.walls[2]:  # Bottom
        neighbors.append(grid[y + 1][x])
    if x > 0 and not cell.walls[3]:  # Left
        neighbors.append(grid[y][x - 1])
    return neighbors

def reconstruct_path(visited, end):
    path = []
    while end:
        path.append(end)
        end = visited[end]
    path.reverse()
    return path

def highlight_path(path, color):
    for cell in path:
        pygame.draw.rect(screen, color, (cell.x * CELL_SIZE + 2, cell.y * CELL_SIZE + 102, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=5)
        pygame.display.flip()
        time.sleep(0.03)

# Function to reset game state
def reset_game():
    global player_x, player_y, win, game_over, start_time
    player_x, player_y = 0, 0
    generate_maze()
    start_time = time.time()
    win = False
    game_over = False

# Main game loop
running = True
generate_maze()  # Generate the initial maze
bfs_button = pygame.Rect(300, 10, 80, 30)  # BFS button
dfs_button = pygame.Rect(400, 10, 80, 30)  # DFS button
moving = False  # variable to track if the player is moving

while running:
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(time_limit - elapsed_time))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw maze
    screen.fill(GREY)
    screen.blit(background, (0, 0))
    for row in grid:
        for cell in row:
            cell.draw()

    # Draw player, start, and end points
    pygame.draw.rect(screen, BLUE, (player_x * CELL_SIZE + 2, player_y * CELL_SIZE + 102, CELL_SIZE - 4, CELL_SIZE - 4))
    pygame.draw.rect(screen, YELLOW, (2, 102, CELL_SIZE - 4, CELL_SIZE - 4))
    pygame.draw.rect(screen, GREEN, ((COLS - 1) * CELL_SIZE + 2, (ROWS - 1) * CELL_SIZE + 102, CELL_SIZE - 4, CELL_SIZE - 4))

    # Display timer and level
    level_text = font.render(f"Level: {difficulty}", True, WHITE)
    timer_text = font.render(f"Time: {remaining_time}s", True, WHITE)
    screen.blit(level_text, (10, 10))
    screen.blit(timer_text, (150, 10))

    # Draw BFS and DFS buttons
    pygame.draw.rect(screen, PURPLE, bfs_button)
    pygame.draw.rect(screen, PURPLE, dfs_button)
    screen.blit(font.render("BFS", True, WHITE), (315, 15))
    screen.blit(font.render("DFS", True, WHITE), (415, 15))

    # Check for win condition (reaching the end)
    if player_x == COLS - 1 and player_y == ROWS - 1:
        win = True

    # Check for game over condition (time runs out)
    if remaining_time == 0 and not game_over:
        game_over = True
        lose_sound.play()  # Play losing sound
        screen.fill(GREY)
        screen.blit(background, (0, 0))

        # Game Over Message
        game_over_text = large_font.render("Game Over!", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(game_over_text, game_over_rect)

        # Restart Button
        restart_text = font.render("Restart", True, WHITE)  
        restart_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 40))
        pygame.draw.rect(screen, PURPLE, restart_button_rect)  # Draw Restart Button
        restart_text_rect = restart_text.get_rect(center=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2) + 20))
        screen.blit(restart_text, restart_text_rect)

        # Exit Button
        exit_text = font.render("Exit", True, WHITE)
        exit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 60, 100, 40))
        pygame.draw.rect(screen, PURPLE, exit_button_rect)  # Draw Exit Button
        exit_text_rect = exit_text.get_rect(center=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2) + 80))
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()
        
        # Wait for player to restart the game or exit
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        reset_game()  # Reset the game state
                        waiting_for_restart = False
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()  # Exit the game
                        sys.exit()  # Ensure the program exits completely

    # Handle key events for manual movement
    keys = pygame.key.get_pressed()

    if not game_over and not win:  # Check if the game is ongoing
        if not moving:  # Only allow movement if not currently moving
            if keys[pygame.K_LEFT] and player_x > 0 and not grid[player_y][player_x].walls[3]:  # Move left
                player_x -= 1
                moving = True
            elif keys[pygame.K_RIGHT] and player_x < COLS - 1 and not grid[player_y][player_x].walls[1]:  # Move right
                player_x += 1
                moving = True
            elif keys[pygame.K_UP] and player_y > 0 and not grid[player_y][player_x].walls[0]:  # Move up
                player_y -= 1
                moving = True
            elif keys[pygame.K_DOWN] and player_y < ROWS - 1 and not grid[player_y][player_x].walls[2]:  # Move down
                player_y += 1
                moving = True

    # Delay for player movement
    if moving:
        pygame.time.delay(200)  # Adjust this value for movement speed
        moving = False  # Reset after moving

    # Check for BFS or DFS button press
    if event.type == pygame.MOUSEBUTTONDOWN:
        if bfs_button.collidepoint(event.pos) and not win and not game_over:
            path = bfs(grid[0][0], grid[ROWS - 1][COLS - 1])
            highlight_path(path, LIGHT_GREEN)
            win = True
        elif dfs_button.collidepoint(event.pos) and not win and not game_over:
            path = dfs(grid[0][0], grid[ROWS - 1][COLS - 1])
            highlight_path(path, LIGHT_RED)
            win = True

    # Check for level completion and display win message
    if win:
        solve_sound.play()
        screen.fill(GREY)
        screen.blit(background, (0, 0))
        well_done_text = large_font.render("Well Done!", True, WHITE)
        well_done_rect = well_done_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        pygame.draw.rect(screen, PURPLE, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 40))  # Next button
        next_text = font.render("Next", True, WHITE)
        next_text_rect = next_text.get_rect(center=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2) + 20))
        screen.blit(well_done_text, well_done_rect)
        screen.blit(next_text, next_text_rect)
        pygame.display.flip()
        
        # Wait for player to go to the next level
        waiting_for_next_level = True
        while waiting_for_next_level:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_next_level = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] in range(SCREEN_WIDTH // 2 - 50, SCREEN_WIDTH // 2 + 50) and event.pos[1] in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2 + 40):
                        difficulty += 1
                        reset_game()  # Generate a new maze for the next level
                        waiting_for_next_level = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()