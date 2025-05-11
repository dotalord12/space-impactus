import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Impact")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Player
player_width, player_height = 50, 30
player_x, player_y = 100, HEIGHT // 2
player_speed = 5

# Bullet
bullets = []
bullet_speed = 10

# Enemy
enemies = []
enemy_speed = 3
spawn_timer = 0
spawn_delay = 30  # frames

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

def show_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    clock.tick(60)

    # Input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
        player_y += player_speed
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = pygame.Rect(player_x + player_width, player_y + player_height // 2 - 5, 10, 5)
                bullets.append(bullet_rect)

    # Move bullets
    for bullet in bullets[:]:
        bullet.x += bullet_speed
        if bullet.x > WIDTH:
            bullets.remove(bullet)

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        enemy_y = random.randint(0, HEIGHT - 30)
        enemy = pygame.Rect(WIDTH, enemy_y, 40, 30)
        enemies.append(enemy)
        spawn_timer = 0

    # Move enemies
    for enemy in enemies[:]:
        enemy.x -= enemy_speed
        if enemy.x < 0:
            enemies.remove(enemy)

    # Collision detection
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

    # Drawing
    draw_player(player_x, player_y)
    draw_bullets()
    draw_enemies()
    show_score()

    pygame.display.update()

pygame.quit()
