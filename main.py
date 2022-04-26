import pygame, sys

from pygame.constants import K_DOWN

def ball_animation ():
    global ball_speed_x , ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top<=0 or ball.bottom>=window_h:
        ball_speed_y *=-1
    if ball.left<=0 or ball.right>=window_w:
        ball_speed_x *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x*= -1

def player_animation():
    player.y += player_speed
    if player.top<=0:
        player.top=0
    if player.bottom>= window_h:
        player.bottom= window_h

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top+= opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top<=0:
        opponent.top=0
    if opponent.bottom>= window_h:
        opponent.bottom= window_h



#screen size
window_w= 900
window_h=500
window_size=(window_w, window_h)

clock= pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pong")

ball= pygame.Rect(window_w/2-15, window_h/2-15 ,30 ,30)
player=pygame.Rect(window_w-20,window_h/2-70, 10,140)
opponent= pygame.Rect(10,window_h/2-70,10,140)

bg_color=pygame.Color('grey12')
light_grey=(200,200,200)

ball_speed_x=7
ball_speed_y=7
player_speed=0
opponent_speed= 7
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_DOWN:
                player_speed +=7
            if event.key== pygame.K_UP:
                player_speed -=7
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_UP:
                player_speed -=7
            if event.key== pygame.K_DOWN:
                player_speed +=7

    ball_animation() 
    player_animation()
    opponent_ai()


    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey,player)
    pygame.draw.rect(screen, light_grey,opponent)
    pygame.draw.ellipse(screen, light_grey,ball)
    pygame.draw.aaline(screen, light_grey,(window_w/2,0),(window_w/2,window_h))

    pygame.display.flip()
    clock.tick(50)
