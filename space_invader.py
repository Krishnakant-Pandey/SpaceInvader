import pygame as pg
import random
import math
from pygame import mixer

color = (0, 0, 0)
# initialize pg
pg.init()

# create a screen
screen = pg.display.set_mode((800, 600))

# background
background = pg.image.load("space_bg.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

# title
pg.display.set_caption("Space Invaders")
icon = pg.image.load("space-shuttle.png")

# player
player_img = pg.image.load("space-invaders.png")
playerX = 367.5
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 4

for i in range(num_enemy):
    enemy_img.append(pg.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(8)
    enemyY_change.append(45)

# bullet
bullet_img = pg.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 18
bullet_state = "ready"


# score
score_value = 0
font = pg.font.Font("YellowRabbit.otf", 52)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render(f"Score :{score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    end = pg.font.Font("freesansbold.ttf", 64)
    game_over = end.render(f"GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))
    # running = False


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, j):
    screen.blit(enemy_img[j], (x[j], y[j]))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y2 - y1) ** 2)
    if distance < 27:
        return True
    else:
        return False


pg.display.set_icon(icon)

# Game Loop
running = True
while running:
    screen.fill(color)
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change -= 10
            if event.key == pg.K_RIGHT:
                playerX_change += 10
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    for i in range(num_enemy):
        enemyX[i] += enemyX_change[i]

    # bullet movement / limitation
    if bullet_state == "fire" and bulletY >= 0:
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change

        if bulletY <= 0:
            bullet_state = "ready"
            bulletX = playerX
            bulletY = playerY

    # player movement / limitation
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement / limitation
    for i in range(num_enemy):
        if enemyY[i] > 440:
            for j in range(num_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

    # collision detector
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()

            bullet_state = "ready"
            bulletX = playerX
            bulletY = playerY

            score_value += 1
            

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)

    player(playerX, playerY)

    for i in range(num_enemy):
        enemy(enemyX, enemyY, i)

    show_score(textX, textY)
    pg.display.update()


