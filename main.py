import pygame, sys, random
from pygame.constants import K_DOWN
import cv2
import mediapipe as mp


def ball_animation ():
    global ball_speed_x , ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x*2
    ball.y += ball_speed_y+1

    if ball.top<=0 or ball.bottom>=window_h: # אם הכדור מגיע לאחד מהגבולות הוא חוזר לאמצע ומוסיף נקודה לצד השני
        pygame.mixer.Sound.play(pong_sound) 
        ball_speed_y *=-1
    if ball.left<=0:
        opponent_score += 1
        pygame.mixer.Sound.play(score_sound)
        ball_restart()
    if ball.right>=window_w:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_restart()
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x*= -1
        ball_speed_y+= -1 

def player_animation():
    global player_speed
    player.y += player_speed
    player_speed = 0
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

def ball_restart():
    global ball_speed_x , ball_speed_y
    ball.center= (window_w/2, window_h/2) 
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))


pygame.init()
clock= pygame.time.Clock()

player_score=0
opponent_score=0
game_font= pygame.font.SysFont(None, 32)



#screen size
window_w= 900
window_h=500
window_size=(window_w, window_h)


screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pong")

ball= pygame.Rect(window_w/2-15, window_h/2-15 ,30 ,30)
player=pygame.Rect(window_w-20,window_h/2-70, 10,140)
opponent= pygame.Rect(10,window_h/2-70,10,140)

bg_color=pygame.Color('grey12')
light_grey=(200,200,200)

ball_speed_x= 9 * random.choice((1,-1))
ball_speed_y= 9 * random.choice((1,-1))
player_speed= 0
opponent_speed= 7

pong_sound= pygame.mixer.Sound("pong.ogg")
score_sound= pygame.mixer.Sound("score.ogg")

# define a video capture object
vid = cv2.VideoCapture(0)

mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    # Capture the video frame
	# by frame
    ret, frame = vid.read()
    index_finger_y = 0

    RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    font = cv2.FONT_HERSHEY_SIMPLEX

    org = (50, 50)

    fontScale = 1

    color = (255, 0, 0)

    thickness = 2
    
    frame = cv2.putText(frame, str(index_finger_y), org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    '''for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_DOWN:
                player_speed +=20
            if event.key== pygame.K_UP:
                player_speed -=20
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_UP:
                player_speed -=20
            if event.key== pygame.K_DOWN:
                player_speed +=20'''
    if multiLandMarks:
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(frame, handLms, mp_Hands.HAND_CONNECTIONS)
        index_finger_y = multiLandMarks[0].landmark[5].y  
        index_finger_y1= multiLandMarks[0].landmark[8].y          
        if index_finger_y>0.7:
            player_speed+=20    
        if index_finger_y<0.4:
            player_speed-=20
        if index_finger_y1>index_finger_y:
            pygame.quit()
            sys.exit()
    '''for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            sys.exit()'''

    ball_animation() 
    player_animation()
    opponent_ai()


    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey,player)
    pygame.draw.rect(screen, light_grey,opponent)
    pygame.draw.ellipse(screen, light_grey,ball)
    pygame.draw.aaline(screen, light_grey,(window_w/2,0),(window_w/2,window_h))


    player_text= game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (430,240))

    opponent_text= game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (460,240))


    pygame.display.flip()
    clock.tick(60)

vid.release()

cv2.destroyAllWindows()
