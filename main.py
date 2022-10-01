import os
import pygame
from pygame import mixer
import random
import math

# set root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)

# initialise pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load("static/background.png")

# background sound
mixer.music.load("static/wav/background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("static/icon.png")
pygame.display.set_icon(icon)

# player
playerImage = pygame.image.load("static/player.png")
playerX = 368
playerY = 480
playerX_change = 0

# enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemySpeed = 0.2

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load("static/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# bullet
bulletImage = pygame.image.load("static/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.85
bullet_state = "ready"      # ready: can't see bullet   //  fire: bullet is moving

# score
score_value = 0
score_font = pygame.font.Font("static/font/Space Quest.ttf", 32)
scoreX = 10
scoreY = 10

# high score init
highscore_value = ""

# high score name
enterName_font = pygame.font.Font("static/font/Space Quest.ttf", 16) # size -> 294, 18
highScoreName_font = pygame.font.Font("static/font/Space Quest.ttf", 32)
user_text = ""


# game over text
game_over_font = pygame.font.Font("static/font/Space Quest.ttf", 64) # size -> 382, 72
play_again_font = pygame.font.Font("static/font/Space Quest.ttf", 24) # size -> 357, 27


def enemyReset():
    global num_of_enemies, enemyImage, enemyX, enemyY, enemyX_change, enemyY_change, enemySpeed
    num_of_enemies = 6
    enemyImage = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    for i in range(num_of_enemies):
        enemyImage.append(pygame.image.load("static/enemy.png"))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.2)
        enemyY_change.append(40)
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
    enemySpeed = 0.2

def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_highscore():
    global highscore_value
    highscore_value_file = open("highscore.txt", "r+")
    highscore_value_list = highscore_value_file.readlines()
    # highscore_value = "".join(highscore_value_list)
    highscore_value = highscore_value_list[1]
    highscore_name = highscore_value_list[0]
    highscore_value_file.close()
    highscore = score_font.render("High Score: " + highscore_name + "- " + highscore_value, True, (255, 255, 255))
    highscore_rect = highscore.get_rect()
    highscore_rect.topright = (785, 10)
    screen.blit(highscore, highscore_rect)

def game_over_text():
    over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    play_again_text = play_again_font.render("Press Enter to play again", True, (255, 255, 255))
    screen.blit(over_text, (209, 264))
    screen.blit(play_again_text, (221, 326))

def updateHighScoreScreen():
    global user_text

    enterNameText = enterName_font.render("New high score! Enter a name.", True, (255, 255, 255))
    screen.blit(enterNameText, (253, 363))
    highScoreNameText = highScoreName_font.render(user_text, True, (255, 255, 255))
    highScoreNameRect = highScoreNameText.get_rect()
    highScoreNameRect.center = (400, 396)
    screen.blit(highScoreNameText, highScoreNameRect)

def updateHighScore():
    global user_text, score_value
    highscore_value_file = open("highscore.txt", "r+")
    highscore_value_file.write(user_text + "\n" + str(score_value))
    highscore_value_file.close()

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX-bulletX)**2) + ((enemyY-bulletY)**2))
    if distance < 27 and bullet_state == "fire":
        return True
    else:
        return False


# game loop
running = True
gameInProgress = True
lockSpeed = False
lockEnemyCount = False
while running:

    screen.fill((0, 25, 64))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # player movement
            if event.key == pygame.K_a:
                playerX_change = -0.3
            if event.key == pygame.K_d:
                playerX_change = 0.3
            # shooting
            if event.key == pygame.K_SPACE:
                 if bullet_state == "ready":
                    bulletSound = mixer.Sound("static/wav/laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            # play again
            if event.key == pygame.K_RETURN:
                updateHighScore()
                score_value = 0
                enemyReset()
                show_highscore()
                user_text = ""
                continue

            if gameInProgress == False:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0.0

    # player movement boundary
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 440:
            for e in range(num_of_enemies):
                enemyY[e] = 2000
            game_over_text()
            if score_value > int(highscore_value):
                updateHighScoreScreen()
                gameInProgress = False
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemySpeed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = enemySpeed*-1
            enemyY[i] += enemyY_change[i]


        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collideSound = mixer.Sound("static/wav/explosion.wav")
            collideSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
        if enemyY[i] < 440:
            gameInProgress = True

    # speed increase
    if score_value != 0 and score_value % 10 == 0 and lockSpeed == False:
        enemySpeed *= 1.25
        lockSpeed = True

    if score_value != 0 and score_value % 10 == 1:
        lockSpeed = False

    # enemy increase
    if score_value != 0 and score_value % 50 == 0 and lockEnemyCount == False:
        num_of_enemies += 2
        for i in range(2):
            enemyImage.append(pygame.image.load("static/enemy.png"))
            enemyX.append(random.randint(0, 735))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(0.2)
            enemyY_change.append(40)
        lockEnemyCount = True

    if score_value != 0 and score_value % 50 == 1:
        lockEnemyCount = False

    # bullet movement
    if bulletY <= -32:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(scoreX, scoreY)
    show_highscore()
    pygame.display.update()
