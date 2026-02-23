import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
# sets the dimension of the screen

pygame.display.set_caption("Galaxy Fighters") #sets the title
FPS= 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT= 50,40
VEL=7
BULLET_VEL=9
BORDER= pygame.Rect(WIDTH//2-2.5,0,5,HEIGHT)

MAX_BULLETS=10
BULLET_HIT_SOUND=pygame.mixer.Sound('Grenade+1.mp3')
BULLET_FIRE_SOUND= pygame.mixer.Sound('Gun+Silencer.mp3')
VICTORY=pygame.mixer.Sound('victory.mp3')

RED_HIT=pygame.USEREVENT+1
BLUE_HIT=pygame.USEREVENT+2

HEALTH_FONT= pygame.font.SysFont('inkfree',20)
WINNER_FONT= pygame.font.SysFont('comicsans',50)


RED_SPACESHIP_IMAGE= pygame.image.load('Red_SS.png')
RED_SPACESHIP_IMAGE= pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
BLUE_SPACESHIP_IMAGE= pygame.image.load('Blue_SS.png')
BLUE_SPACESHIP_IMAGE= pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
SPACE=pygame.image.load('space.jpg')
SPACE=pygame.transform.scale(SPACE,(WIDTH,HEIGHT))

def draw_window(red,blue,red_bullets,blue_bullets,red_health,blue_health):
    #WIN.fill((255, 255, 255))  # fills the background with red color
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,(0,0,0),BORDER)

    WIN.blit(RED_SPACESHIP_IMAGE, (red.x,red.y))
    WIN.blit(BLUE_SPACESHIP_IMAGE, (blue.x,blue.y))

    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1,"white")
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health),1,"white")
    WIN.blit(red_health_text,(10,10))
    WIN.blit(blue_health_text,(900,10))



    for bullet in red_bullets:
        pygame.draw.rect(WIN,(0,0,0),bullet)
    for bullet in blue_bullets:
        pygame.draw.rect(WIN,(0,0,0),bullet)

    pygame.display.update()  # updates the display everytime new thing is added


def handle_red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_a] and red.x- VEL>0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x +VEL + red.width <BORDER.x:
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y -VEL >0:
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y +VEL +red.height <HEIGHT:
        red.y += VEL

def handle_blue_movement(keys_pressed,blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - blue.width- VEL +40 >BORDER.x:
        blue.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and blue.x +VEL + blue.width <WIDTH:
        blue.x += VEL
    if keys_pressed[pygame.K_UP] and blue.y -VEL >0:
        blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y +VEL +blue.height <HEIGHT:
        blue.y += VEL

def handle_bullets(red_bullets,blue_bullets,red,blue):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            red_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            red_bullets.remove(bullet)


    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x<0:
            blue_bullets.remove(bullet)

def draw_winner(text): #display winner text
    draw_text=WINNER_FONT.render(text,1,"white")
    WIN.blit(draw_text,(WIDTH//2-(draw_text.get_width()/2)+28,HEIGHT//2-(draw_text.get_height()/2)))

    pygame.display.update()
    pygame.time.delay(10000)


def main(): #contains all the functions of the game
    red= pygame.Rect(50,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    blue=pygame.Rect(900,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets=[]
    blue_bullets=[]
    red_health = 10
    blue_health = 10

    clock= pygame.time.Clock()
    run= True
    while run: #runs the game continuously until run is false
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # for bullet movement
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(red_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x + red.width, red.y+ red.height//2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key==pygame.K_RCTRL and len(blue_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + blue.height //2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type== RED_HIT:
                blue_health-=1
                BULLET_HIT_SOUND.play()

            if event.type==BLUE_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()

        winner_text=""
        if red_health<=0:
            winner_text="Blue Wins!!!"
            VICTORY.play()
        if blue_health<=0:
            winner_text="Red Wins!!!"
            VICTORY.play()

        if winner_text!="":
           draw_winner(winner_text)
           break


        keys_pressed= pygame.key.get_pressed()#movement of the spaceships
        handle_red_movement(keys_pressed,red)
        handle_blue_movement(keys_pressed,blue)

        handle_bullets(red_bullets,blue_bullets,red,blue)

        draw_window(red,blue,red_bullets,blue_bullets, red_health,blue_health)


    main()


if __name__=="__main__":
    main()
