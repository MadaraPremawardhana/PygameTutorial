import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")
CYAN = (0,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BULLET_VEL = 7
FPS = 60
VEL = 5
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background.png')),(WIDTH, HEIGHT))
BORDER = pygame.Rect((WIDTH//2)-5, 0,10, HEIGHT)
MAX_BULLETS = 3
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Assets_Gun+Silencer.mp3'))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

BLUE_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2

BLUE_WARRIOR_IMAGE = pygame.image.load(os.path.join('Assets','bluewarrior.png'))
RED_WARRIOR_IMAGE = pygame.image.load(os.path.join('Assets','redwarrior.png'))

def draw_window(blue,red, blue_bullets, red_bullets, red_heath, blue_heath):
    #WIN.fill(CYAN)
    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(BLUE_WARRIOR_IMAGE,(blue.x, blue.y))
    WIN.blit(RED_WARRIOR_IMAGE,(red.x,red.y))
    
    red_heath_text = HEALTH_FONT.render("HEALTH:"+ str(red_heath), 1, BLACK)
    blue_heath_text = HEALTH_FONT.render("HEALTH:"+ str(blue_heath), 1, BLACK)
    
    WIN.blit(red_heath_text, (WIDTH- red_heath_text.get_width() - 10, 10))
    WIN.blit(blue_heath_text, (10,10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.draw.rect(WIN, BLACK, BORDER)
    pygame.display.update()



#BLUE MOVEMENTS
def blue_handle_movements(keys_pressed, blue): 
    if keys_pressed[pygame.K_a] and ((blue.x - VEL) > 0): #left
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and ((blue.x + VEL + blue.width) < BORDER.x): #right
        blue.x += VEL
    if keys_pressed[pygame.K_w] and ((blue.y - VEL) > 0): #up
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and ((blue.y + VEL + blue.height) < HEIGHT): #down
        blue.y += VEL

#RED MOVEMENTS
def red_handle_movements(keys_pressed, red): 
    if keys_pressed[pygame.K_LEFT] and ((red.x - VEL) > BORDER.x + BORDER.width): #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and ((red.x + VEL + red.width) < WIDTH): #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and ((red.y - VEL) > 0): #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and ((red.y + VEL + red.height) < HEIGHT): #down
        red.y += VEL

def  handle_bullets(blue_bullets, red_bullets, blue,red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x <0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = HEALTH_FONT.render(text,1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    blue = pygame.Rect(100,300,50,50)
    red = pygame.Rect(700,300,50,50)

    red_bullets = []
    blue_bullets = []

    red_heath = 10
    blue_heath = 10

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and (len(blue_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(blue.x+blue.width, blue.y+blue.height//2 -2, 10,5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and (len(red_bullets) < MAX_BULLETS):   
                    bullet = pygame.Rect(red.x, red.y+red.height//2 -2, 10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            winner_text = ""
            if event.type == RED_HIT:
                red_heath -= 1
                BULLET_HIT_SOUND.play()
            if event.type == BLUE_HIT:
                blue_heath -= 1
                BULLET_HIT_SOUND.play()
        if red_heath <=0:
            winner_text = "BLUE WINS!"

        if blue_heath <= 0:
            winner_text = "RED WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_handle_movements(keys_pressed,blue)
        red_handle_movements(keys_pressed, red)

        handle_bullets(blue_bullets, red_bullets, blue,red)

        draw_window(blue,red, blue_bullets, red_bullets, red_heath, blue_heath)

    main()

#making sure only main is run when this file is run seperately
if __name__=="__main__":
    main()