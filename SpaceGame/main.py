import pygame
import os
from pygame import draw
from pygame.event import pump

pygame.font.init()

WIDTH, HEIGTH = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Space War")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGTH)

HEALT_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60

VEL = 6
BULLET_VEL = 15
MAX_BULLETS = 5

SPACESHIP_WIDHT, SPACESHIP_HEIGTH = 100, 100

GREEN_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','GreenSpaceship.png'))
GREEN_SPACESHIP = pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDHT, SPACESHIP_HEIGTH))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','RedSpaceship.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDHT, SPACESHIP_HEIGTH)), 180)

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets','BackGround.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGTH))

pygame.mixer.init(44100, -16,2,2048)
pygame.mixer.set_num_channels(10)
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Piuv.mp3')
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/UHH.mp3')
SOUNDTRACK = pygame.mixer.music.load(os.path.join('Assets', 'soundtrack.mp3'))
pygame.mixer.music.set_volume(0.5)



def draw_window(green, red, green_bullets, red_bullets, green_healt, red_healt):
    pygame.mixer.music.play()
    WIN.blit(BACKGROUND,(0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    green_healt_text = HEALT_FONT.render("Healt:" + str(green_healt), 1, WHITE)
    red_healt_text = HEALT_FONT.render("Healt:" + str(red_healt), 1, WHITE)
    WIN.blit(red_healt_text, (WIDTH - red_healt_text.get_width() - 10, 10))
    WIN.blit(green_healt_text, (10, 10))

    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()

def green_handle_movement(keys_pressed, green):
    if(keys_pressed[pygame.K_a] and (green.x - VEL) > 0): # LEFT
        green.x -= VEL
    if(keys_pressed[pygame.K_d] and (green.x + VEL + green.width) < BORDER.x): # RIGHT
        green.x += VEL    
    if(keys_pressed[pygame.K_w] and (green.y - VEL) > 0): # UP
        green.y -= VEL
    if(keys_pressed[pygame.K_s] and (green.y + VEL + green.height) < HEIGTH): # DOWN
        green.y += VEL 

def red_handle_movement(keys_pressed, red):
    if(keys_pressed[pygame.K_LEFT] and (red.x - VEL) > (BORDER.x + BORDER.width)): # LEFT
        red.x -= VEL
    if(keys_pressed[pygame.K_RIGHT] and (red.x + VEL + red.width) < WIDTH): # RIGHT
        red.x += VEL    
    if(keys_pressed[pygame.K_UP] and (red.y - VEL) > 0): # UP
        red.y -= VEL
    if(keys_pressed[pygame.K_DOWN] and (red.y + VEL + red.height) < HEIGTH): # DOWN
        red.y += VEL

def handle_bullets(green_bullets, red_bullets, green, red):
    for bullet in green_bullets:
        bullet.x += BULLET_VEL
        if(red.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_bullets.remove(bullet)
        elif(bullet.x > WIDTH):
            green_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if(green.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_bullets.remove(bullet)
        elif(bullet.x < 0):
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGTH / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    green = pygame.Rect(100, 200, SPACESHIP_WIDHT, SPACESHIP_HEIGTH)
    red = pygame.Rect(700, 200, SPACESHIP_WIDHT, SPACESHIP_HEIGTH)

    green_bullets = []
    red_bullets = []

    green_healt = 10
    red_healt = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_t and len(green_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(green.x + green.width, green.y + green.height//2, 16, 4)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if(event.key == pygame.K_l and len(red_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 16, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if(event.type == GREEN_HIT):
                green_healt -= 1
                BULLET_HIT_SOUND.play()
                
            if(event.type == RED_HIT):
                red_healt -= 1
                BULLET_HIT_SOUND.play()
                
        winner_text = ""
        if(green_healt <= 0):
            winner_text = "Red Wins!"
        if(red_healt <= 0):            
            winner_text = "Green Wins!"
        if(winner_text != ""):
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed()
        green_handle_movement(keys_pressed, green)
        red_handle_movement(keys_pressed, red)
        handle_bullets(green_bullets, red_bullets, green, red)
        draw_window(green, red, green_bullets, red_bullets, green_healt, red_healt)

    main()

if(__name__ == "__main__"):
    main()