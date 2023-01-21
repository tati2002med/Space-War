
# Building a game of space war

import pygame
import sys
import os
from pygame import mixer

pygame.font.init()
pygame.mixer.init()


# BACKGROUND


WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War 1")
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Images', 'background1.png')), (1080, 720))
BACKGROUND1 = pygame.transform.scale(pygame.image.load(
    os.path.join('Images', 'background.png')), (1080, 720))


# MUSIC


mixer.music.load(os.path.join('Sounds', 'epic.mp3'))
mixer.music.play(-1)


# COLORS


RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (47,79,79)
BLACK = (0, 0, 0)


# SHIPS


W_SCALE, H_SCALE = 67.5, 50
REDSHIP = pygame.transform.scale(pygame.image.load(
    os.path.join('Images', 'redship.png')), (W_SCALE, H_SCALE))
YELLOWSHIP = pygame.transform.scale(pygame.image.load(
    os.path.join('Images', 'yellowship.png')), (W_SCALE, H_SCALE))
W_RED, H_RED = 100, 335
W_YELLOW, H_YELLOW = 912.5, 335
FPS = 60
STEP = 10


# SHOTS


HIT_SOUND = pygame.mixer.Sound(os.path.join('Sounds', 'hit.wav'))
SHOT_SOUND = pygame.mixer.Sound(os.path.join('Sounds', 'shoot.mp3'))
RED_HIT = pygame.USEREVENT +1
YELLOW_HIT = pygame.USEREVENT +2
MAX_SHOTS = 5
SPEED_SHOTS = 20
SW_SCALE, SH_SCALE = 20, 8


# FONTS


HEALTH_FONT = pygame.font.SysFont('comicsans', 50)
SCORE_FONT = pygame.font.SysFont('comicsans', 75)
WINNER_FONT = pygame.font.SysFont('comicsans', 200)
START_FONT = pygame.font.SysFont('plaguard', 100)


# Functions 


def draw_window(red, yellow, red_shots, yellow_shots, red_health, yellow_health, yellow_count, red_count):
    WIN.blit(BACKGROUND, (0, 0))
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, YELLOW)
    score_text = SCORE_FONT.render("SCORE", 1, GREY)
    score_points = HEALTH_FONT.render(str(red_count)+"          "+str(yellow_count), 1, WHITE)
    WIN.blit(red_health_text, (10, 0))
    WIN.blit(yellow_health_text, (900, 0))
    WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 0))
    WIN.blit(score_points, (WIDTH/2 - score_points.get_width()/2, 50))
    WIN.blit(REDSHIP, (red.x, red.y))
    WIN.blit(YELLOWSHIP, (yellow.x, yellow.y))
    for shot in red_shots:
        pygame.draw.rect(WIN, RED, shot)
    for shot in yellow_shots:
        pygame.draw.rect(WIN, YELLOW, shot)
    pygame.display.update()

def red_move(keys_pressed, red):
    if keys_pressed[pygame.K_q] and red.x - STEP > 0:  # LEFT
        red.x -= STEP
    if keys_pressed[pygame.K_d] and red.x - STEP < WIDTH/2 - W_SCALE - 20:  # RIGHT
        red.x += STEP
    if keys_pressed[pygame.K_s] and red.y + STEP < HEIGHT - H_SCALE:  # DOWN
        red.y += STEP
    if keys_pressed[pygame.K_z] and red.y - STEP > 0:  # UP
        red.y -= STEP

def yellow_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - STEP > WIDTH/2 + 10 :  # LEFT
        yellow.x -= STEP
    if keys_pressed[pygame.K_RIGHT] and yellow.x + STEP < WIDTH - W_SCALE:  # RIGHT
        yellow.x += STEP
    if keys_pressed[pygame.K_DOWN] and yellow.y + STEP < HEIGHT - H_SCALE :  # DOWN
        yellow.y += STEP
    if keys_pressed[pygame.K_UP] and yellow.y - STEP > 0:  # UP
        yellow.y -= STEP

def handle_shots(red_shots, yellow_shots, red, yellow):
    for shot in red_shots:
        shot.x += SPEED_SHOTS
        if yellow.colliderect(shot):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_shots.remove(shot)
        elif shot.x > WIDTH:
            red_shots.remove(shot)

    for shot in yellow_shots:
        shot.x -= SPEED_SHOTS
        if red.colliderect(shot):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_shots.remove(shot)
        elif shot.x < 0:
            yellow_shots.remove(shot)

def draw_win(winner):
    if winner == "Yellow Wins!":
        winner = WINNER_FONT.render(winner, 1, YELLOW)
    else:
        winner = WINNER_FONT.render(winner, 1, RED)
    WIN.fill(BLACK)
    WIN.blit(winner, (WIDTH/2 - winner.get_width()/2, HEIGHT/2 - winner.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)
    



def main():
    global yellow_count
    global red_count
    red = pygame.Rect(W_RED, H_RED, W_SCALE, H_SCALE)
    yellow = pygame.Rect(W_YELLOW, H_YELLOW, W_SCALE, H_SCALE)
    clock = pygame.time.Clock()
    red_shots = []
    yellow_shots = []
    red_health = 10
    yellow_health = 10
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_shots) < MAX_SHOTS:
                    shot = pygame.Rect(red.x + W_SCALE +2, red.y + H_SCALE//2, SW_SCALE, SH_SCALE)
                    red_shots.append(shot)
                    SHOT_SOUND.play()
                if event.key == pygame.K_RCTRL and len(yellow_shots) < MAX_SHOTS:
                    shot = pygame.Rect(yellow.x - 2, yellow.y + H_SCALE // 2, SW_SCALE, SH_SCALE)
                    yellow_shots.append(shot)
                    SHOT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                yellow_health += 1
                HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                red_health += 1
                HIT_SOUND.play()
        winner = ""
        if red_health <= 0:
            yellow_count += 1
            winner = "Yellow Wins!"
        if yellow_health <= 0:
            red_count += 1
            winner = "Red Wins!"
        if winner != "":
            draw_win(winner)
            break

        draw_window(red, yellow, red_shots, yellow_shots, red_health, yellow_health, yellow_count, red_count)
        keys_pressed = pygame.key.get_pressed()
        red_move(keys_pressed, red)
        yellow_move(keys_pressed, yellow)
        handle_shots(red_shots, yellow_shots, red, yellow)
    main()

def start():
    WIN.fill(GREY)
    start_text = START_FONT.render("GAME STARTED", 1, WHITE)
    WIN.blit(start_text, (WIDTH/2 - start_text.get_width()/2, HEIGHT/2 - start_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)
    main()
    

# Calling

if __name__ == "__main__":
    yellow_count = 0
    red_count = 0
    start()