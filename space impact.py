import pygame
import random

pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Impact")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Player setup
player_width, player_height = 50, 30
player_x, player_y = 100, HEIGHT // 2
player_speed = 5
lives = 3
invincible = False
invincibility_timer = 0
INVINCIBILITY_DURATION = 60

player_img = pygame.image.load("c:/xampp/htdocs/space_impact/spaceShips_004.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_width, player_height))
enemy_img = pygame.image.load("c:/xampp/htdocs/space_impact/Ship6.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 30))
bullet_img = pygame.image.load("c:/xampp/htdocs/space_impact/spaceMissiles_040.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (20, 10))
boss_bullet_img = pygame.image.load("c:/xampp/htdocs/space_impact/laser.png").convert_alpha()
boss_bullet_img = pygame.transform.scale(boss_bullet_img, (100, 10))  # Adjust the size as needed

# Boss GIF frames
boss_frames = [pygame.image.load("c:/xampp/htdocs/space_impact/alien.gif").convert_alpha() for _ in range(4)]
current_boss_frame = 0
BOSS_ANIMATION_SPEED = 10

# Backgrounds
backgrounds = [
    pygame.image.load("c:/xampp/htdocs/space_impact/space.jpg").convert(),
    pygame.image.load("c:/xampp/htdocs/space_impact/space2.jpg").convert()
]
backgrounds = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in backgrounds]

# Game variables
bullets = []
bullet_speed = 5
boss_bullets = []
boss_bullet_speed = 8
boss_shoot_timer = 0
boss_shoot_delay = 60

enemies = []
enemy_speed = 3
spawn_timer = 0
spawn_delay = 30

boss_active = False
boss = None
boss_hp = 0
BOSS_VERTICAL_SPEED = 2  # Speed of boss's vertical movement
BOSS_HORIZONTAL_SPEED = 1
BOSS_SPAWN_SCORE = 10
BOSS_WIDTH, BOSS_HEIGHT = 100, 80
BOSS_SPEED = 1
BOSS_HP_BASE = 5

score = 0
player_alive = True

level = 1
level_cleared = False
level_clear_timer = 0
boss_spawned_this_level = False


def draw_player(x, y, sparkle=False):
    if sparkle:
        temp_img = player_img.copy()
        temp_img.fill((255, 255, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(temp_img, (x, y))
    else:
        screen.blit(player_img, (x, y))


def draw_bullets():
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))


def draw_boss_bullets():
    for boss_bullet in boss_bullets:
        screen.blit(boss_bullet_img, boss_bullet)  


def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))


def draw_boss():
    if boss:
        screen.blit(boss_frames[current_boss_frame], (boss.x, boss.y))
        hp_text = font.render(f"Boss HP: {boss_hp}", True, WHITE)
        screen.blit(hp_text, (boss.x, boss.y - 30))


def show_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))


def show_lives():
    lives_text = font.render("Lives: " + str(lives), True, WHITE)
    screen.blit(lives_text, (10, 40))


def show_game_over():
    over_text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))


def show_level_clear():
    clear_text = font.render(f"Level {level} Cleared!", True, WHITE)
    screen.blit(clear_text, (WIDTH // 2 - 120, HEIGHT // 2))


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(backgrounds[min(level - 1, len(backgrounds) - 1)], (0, 0))

    if player_alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
            player_y += player_speed
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 10:
                bullet_rect = pygame.Rect(player_x + player_width, player_y + player_height // 2 - 5, 10, 5)
                bullets.append(bullet_rect)

        if not level_cleared:
            for bullet in bullets[:]:
                bullet.x += bullet_speed
                if bullet.x > WIDTH:
                    bullets.remove(bullet)

            spawn_timer += 1
            if spawn_timer >= spawn_delay and not boss_active:
                enemy_y = random.randint(0, HEIGHT - 30)
                enemy = pygame.Rect(WIDTH, enemy_y, 40, 30)
                enemies.append(enemy)
                spawn_timer = 0

            for enemy in enemies[:]:
                enemy.x -= enemy_speed
                if enemy.x < 0:
                    enemies.remove(enemy)

            if level == 1 and score > 0 and score % BOSS_SPAWN_SCORE == 0 and not boss_active:
                boss = pygame.Rect(WIDTH, HEIGHT // 2 - BOSS_HEIGHT // 2, BOSS_WIDTH, BOSS_HEIGHT)
                boss_hp = BOSS_HP_BASE + (level * 2)
                boss_active = True
                boss_spawned_this_level = True

            if boss_active and boss:
                # Boss vertical movement logic (up and down)
                boss.y += BOSS_VERTICAL_SPEED
                if boss.y <= 0 or boss.y >= HEIGHT - BOSS_HEIGHT:
                    BOSS_VERTICAL_SPEED = -BOSS_VERTICAL_SPEED  # Reverse direction

                # Boss horizontal movement
                boss.x -= BOSS_SPEED
                if boss.x < -BOSS_WIDTH:
                    boss_active = False
                    boss = None

            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

            for enemy in enemies[:]:
                for bullet in bullets[:]:
                    if enemy.colliderect(bullet):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 1
                        break

            if boss_active and boss:
                boss_shoot_timer += 1
                if boss_shoot_timer >= boss_shoot_delay:
                     bullet_y = random.randint(boss.y, boss.y + BOSS_HEIGHT - 10)  # 10 is the bullet's height
                     boss_bullet = pygame.Rect(boss.x, bullet_y, 50, 5)
                     boss_bullets.append(boss_bullet)
                     boss_shoot_timer = 0

            for bullet in boss_bullets[:]:
                bullet.x -= boss_bullet_speed
                if bullet.right < 0:
                    boss_bullets.remove(bullet)

            for bullet in bullets[:]:
                if boss and boss.colliderect(bullet):
                    boss_hp -= 1
                    bullets.remove(bullet)
                    if boss_hp <= 0:
                        score += 10
                        boss_active = False
                        boss = None
                        level_cleared = True
                        level_clear_timer = 180
                        break

            if not invincible:
                for enemy in enemies[:]:
                    if enemy.colliderect(player_rect):
                        lives -= 1
                        invincible = True
                        invincibility_timer = INVINCIBILITY_DURATION
                        enemies.remove(enemy)
                        break
                for bullet in boss_bullets[:]:
                    if bullet.colliderect(player_rect):
                        lives -= 1
                        invincible = True
                        invincibility_timer = INVINCIBILITY_DURATION
                        boss_bullets.remove(bullet)
                        break

                if boss_active and boss and boss.colliderect(player_rect):
                    lives -= 1
                    invincible = True
                    invincibility_timer = INVINCIBILITY_DURATION

            if invincible:
                invincibility_timer -= 1
                if invincibility_timer <= 0:
                    invincible = False

            if lives <= 0:
                player_alive = False

        else:
            level_clear_timer -= 1
            show_level_clear()
            if level_clear_timer <= 0:
                level += 1
                level_cleared = False
                enemy_speed += 1
                BOSS_SPEED += 0.5
                BOSS_SPAWN_SCORE += 10
                boss_spawned_this_level = False
                boss_active = False
                boss = None
                boss_hp = 0

        if boss_active:
            current_boss_frame = (current_boss_frame + 1) % len(boss_frames)

        draw_player(player_x, player_y, sparkle=invincible and invincibility_timer % 10 < 5)
        draw_bullets()
        draw_boss_bullets()
        draw_enemies()
        draw_boss()
        show_score()
        show_lives()
    else:
        show_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
