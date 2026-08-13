import pygame
import random
import math

pygame.init()

CELL = 22
COLS, ROWS = 30, 25
PANEL = 120
WIDTH, HEIGHT = COLS * CELL + PANEL, ROWS * CELL

# Colors
BG          = (15, 15, 25)
GRID        = (25, 25, 40)
PANEL_BG    = (20, 20, 35)
PANEL_BORDER= (80, 80, 180)
SNAKE_HEAD  = (0, 255, 120)
SNAKE_BODY  = (0, 180, 80)
SNAKE_TAIL  = (0, 100, 50)
FOOD_COLOR  = (255, 60, 60)
FOOD_GLOW   = (255, 120, 120)
WHITE       = (255, 255, 255)
YELLOW      = (255, 220, 50)
DARK_RED    = (180, 30, 30)
CYAN        = (0, 220, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont("Consolas", 36, bold=True)
font_med   = pygame.font.SysFont("Consolas", 22, bold=True)
font_small = pygame.font.SysFont("Consolas", 16)

def draw_grid():
    for x in range(0, COLS * CELL, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (COLS * CELL, y))
    pygame.draw.rect(screen, PANEL_BORDER, (COLS * CELL, 0, PANEL, HEIGHT), 2)

def draw_panel(score, high_score, length):
    panel_x = COLS * CELL
    pygame.draw.rect(screen, PANEL_BG, (panel_x, 0, PANEL, HEIGHT))
    pygame.draw.rect(screen, PANEL_BORDER, (panel_x, 0, PANEL, HEIGHT), 2)

    title = font_med.render("SNAKE", True, SNAKE_HEAD)
    screen.blit(title, (panel_x + PANEL//2 - title.get_width()//2, 20))
    pygame.draw.line(screen, PANEL_BORDER, (panel_x + 10, 55), (panel_x + PANEL - 10, 55), 1)

    screen.blit(font_small.render("SCORE", True, CYAN), (panel_x + 10, 70))
    score_surf = font_med.render(str(score), True, YELLOW)
    screen.blit(score_surf, (panel_x + PANEL//2 - score_surf.get_width()//2, 90))

    pygame.draw.line(screen, PANEL_BORDER, (panel_x + 10, 120), (panel_x + PANEL - 10, 120), 1)
    screen.blit(font_small.render("BEST", True, CYAN), (panel_x + 10, 135))
    best_surf = font_med.render(str(high_score), True, WHITE)
    screen.blit(best_surf, (panel_x + PANEL//2 - best_surf.get_width()//2, 155))

    pygame.draw.line(screen, PANEL_BORDER, (panel_x + 10, 185), (panel_x + PANEL - 10, 185), 1)
    screen.blit(font_small.render("LENGTH", True, CYAN), (panel_x + 10, 200))
    len_surf = font_med.render(str(length), True, WHITE)
    screen.blit(len_surf, (panel_x + PANEL//2 - len_surf.get_width()//2, 220))

    controls = ["", "CONTROLS", "", "↑↓←→ Move", "R  Restart", "Q  Quit"]
    for i, line in enumerate(controls):
        color = CYAN if line == "CONTROLS" else (150, 150, 180)
        surf = font_small.render(line, True, color)
        screen.blit(surf, (panel_x + PANEL//2 - surf.get_width()//2, HEIGHT - 160 + i * 20))

def draw_snake(snake):
    for i, seg in enumerate(snake):
        ratio = i / max(len(snake) - 1, 1)
        r = int(SNAKE_HEAD[0] + (SNAKE_TAIL[0] - SNAKE_HEAD[0]) * ratio)
        g = int(SNAKE_HEAD[1] + (SNAKE_TAIL[1] - SNAKE_HEAD[1]) * ratio)
        b = int(SNAKE_HEAD[2] + (SNAKE_TAIL[2] - SNAKE_HEAD[2]) * ratio)
        color = (r, g, b)
        rect = pygame.Rect(seg[0]*CELL + 2, seg[1]*CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(screen, color, rect, border_radius=6)
        if i == 0:
            pygame.draw.rect(screen, WHITE, rect, 1, border_radius=6)

def draw_food(food, tick):
    pulse = abs(math.sin(tick * 0.1)) * 4
    fx = food[0] * CELL + CELL // 2
    fy = food[1] * CELL + CELL // 2
    pygame.draw.circle(screen, FOOD_GLOW, (fx, fy), int(CELL // 2 + pulse))
    pygame.draw.circle(screen, FOOD_COLOR, (fx, fy), CELL // 2 - 2)
    pygame.draw.circle(screen, (255, 180, 180), (fx - 3, fy - 3), 3)

def draw_overlay(title, subtitle, hint, title_color):
    overlay = pygame.Surface((COLS * CELL, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    box_w, box_h = 360, 180
    box_x = COLS * CELL // 2 - box_w // 2
    box_y = HEIGHT // 2 - box_h // 2
    pygame.draw.rect(screen, (30, 30, 50), (box_x, box_y, box_w, box_h), border_radius=16)
    pygame.draw.rect(screen, PANEL_BORDER, (box_x, box_y, box_w, box_h), 2, border_radius=16)

    t = font_big.render(title, True, title_color)
    screen.blit(t, (COLS * CELL // 2 - t.get_width() // 2, box_y + 25))
    s = font_med.render(subtitle, True, WHITE)
    screen.blit(s, (COLS * CELL // 2 - s.get_width() // 2, box_y + 80))
    h = font_small.render(hint, True, (160, 160, 200))
    screen.blit(h, (COLS * CELL // 2 - h.get_width() // 2, box_y + 130))

def random_food(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos

def run_game(high_score):
    snake = [(COLS//2, ROWS//2)]
    direction = (1, 0)
    next_dir = (1, 0)
    food = random_food(snake)
    score = 0
    tick = 0

    # Start screen
    while True:
        screen.fill(BG)
        draw_grid()
        draw_panel(score, high_score, len(snake))
        draw_overlay("🐍 SNAKE", "Arrow Keys to Move", "Press SPACE to Start", SNAKE_HEAD)
        pygame.display.flip()
        waiting = True
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False, high_score
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    waiting = False
                if e.key == pygame.K_q:
                    return False, high_score
        if not waiting:
            break

    while True:
        clock.tick(10)
        tick += 1

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False, high_score
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != (0, 1):
                    next_dir = (0, -1)
                elif e.key == pygame.K_DOWN and direction != (0, -1):
                    next_dir = (0, 1)
                elif e.key == pygame.K_LEFT and direction != (1, 0):
                    next_dir = (-1, 0)
                elif e.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_dir = (1, 0)
                elif e.key == pygame.K_q:
                    return False, high_score

        direction = next_dir
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in snake:
            high_score = max(high_score, score)
            # Game over screen
            while True:
                screen.fill(BG)
                draw_grid()
                draw_panel(score, high_score, len(snake))
                draw_snake(snake)
                draw_food(food, tick)
                draw_overlay("GAME OVER", f"Score: {score}", "R = Restart   Q = Quit", FOOD_COLOR)
                pygame.display.flip()
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        return False, high_score
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_r:
                            return True, high_score
                        if e.key == pygame.K_q:
                            return False, high_score

        snake.insert(0, head)
        if head == food:
            score += 10
            food = random_food(snake)
        else:
            snake.pop()

        screen.fill(BG)
        draw_grid()
        draw_panel(score, high_score, len(snake))
        draw_snake(snake)
        draw_food(food, tick)
        pygame.display.flip()

high_score = 0
playing = True
while playing:
    playing, high_score = run_game(high_score)

pygame.quit()
