import pygame
import os
pygame.font.init()

WIDTH,HEIGHT = 900,500
WIN =pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First game!") #It is equal to say tk.title("")

WHITE = (255,255,255)
BLACK =(0,0,0)
RED =(255,0,0)
YELLOW=(255,255,0)

FPS = 60 #set the fps

VEL = 5 #we set the velocity the ships move around

BULLET_VEL = 7

MAX_BULLET = 5

BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT) #We need to decide where the border is gonna be(x,y)and the width and the height

HEALTH_FONT = pygame.font.SysFont("comicsans",40)
WINNER_FONT = pygame.font.SysFont("comicsans",100)

SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40

YELLOW_HIT =pygame.USEREVENT + 1 #These are events,the numbers represent the id
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load("spaceship_yellow.png")#we set a character
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)#We redimension the image and rotate it


SPACE = pygame.transform.scale(pygame.image.load("space.png"),(WIDTH,HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load("spaceship_red.png")#we set a character
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)#We resize the image




def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    #We make the images appear and asing them the red and yellow x and y from
    pygame.draw.rect(WIN,BLACK,BORDER)
    # variables of main(red,yellow)
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL

    if keys_pressed[pygame.K_s]and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y += VEL


def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT]and red.x - VEL  > BORDER.x:
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT]and red.x + VEL + red.width < WIDTH :
        red.x += VEL

    if keys_pressed[pygame.K_UP]and red.y + VEL + red.height > 0:
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN]and red.y + VEL + red.height < HEIGHT:
        red.y += VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        elif bullet.x < 0:

            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)
def main():
    #this loop will be redrawing the window,updating,checking for collisions,kinda handle the mainloop
    red = pygame.Rect(700,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)#(rectangle),is like,they moving inside of a canvas
    yellow = pygame.Rect(300,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets=[]

    red_health = 10
    yellow_health = 10




    clock = pygame.time.Clock()#set the fps
    run = True

    while run:
        clock.tick(FPS) #set the fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #To close the window when we click x
                run = False

            if event.type == pygame.KEYDOWN and len(yellow_bullets) < MAX_BULLET:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red.x ,red.y + red.height//2-2,10,5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT :
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if yellow_health <= 0 :
            winner_text = "Yellow wins!"

        if red_health <= 0 :
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,yellow_bullets,red_bullets,red_health,yellow_health)



    #We need this to update everything we put
    pygame.quit()

if __name__ =="__main__":
    main()
