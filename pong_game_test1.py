# Pong game portion from Hamdy Abou El Anein

# Import for multiprocessing server
from multiprocessing.connection import Listener

# Imports for game
import random
import pygame
import sys
from pygame import *
from easygui import *

#import for plotting acceleration data
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import hexiwearserial


# Setting up game
image = "/usr/share/daylight/daylightstart/DayLightLogoSunSet.gif"
msg = "                           Welcome to Daylight Pong \n\n\n Rules of Daylight Pong \n\n\n Player 1 \n\n Arrow up = UP \n Arrow down = DOWN\n\n Player 2 \n\n S = UP \n Z = Down"
choices = ["OK"]
buttonbox(msg, image=image, choices=choices)

pygame.init()
fps = pygame.time.Clock()


WHITE = (255, 255, 255)
ORANGE = (255,140,0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0


window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Daylight Pong')


def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = - horz

    ball_vel = [horz, -vert]


def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT //2]
    l_score = 0
    r_score = 0
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)

x1v=0
x2v=0

def setx1(x1):
    x1v=x1
def setx2(x2):
    x2v=x2

def getx1():
    return x1v
def getx2():
    return x2v

def animate(i, ys1, ys2):
    # Add dis and accel to lists

    accel1=getx1()
    accel2=getx2()

    ys1.append(accel1)
    ys2.append(accel2)

    # Limit x and y lists to 200 samples - 2s 
    ys1 = ys1[-x_len:]
    ys2 = ys2[-x_len:]

    # Draw dis and accel lists
    line1.set_ydata(ys1)
    line2.set_ydata(ys2)

    return line1, line2, 

def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

    '''
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel
    '''
    '''
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    if paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    elif paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    if paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    elif paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    '''


    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])


    pygame.draw.circle(canvas, ORANGE, ball_pos, BALL_RADIUS, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)


    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]


    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,
                                                                                 paddle1_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(
            paddle2_pos[1] - HALF_PAD_HEIGHT, paddle2_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)


    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score " + str(l_score), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score " + str(r_score), 1, (255, 255, 0))
    canvas.blit(label2, (470, 20))


# Init pong game
init()

serv = Listener(('',5005))
client = serv.accept()

while True:
    if (client.poll(0)):
        msg = client.recv()
        '''
        if msg == "1":
            paddle1_vel = paddle1_vel + 1
        elif msg == "2":
            paddle1_vel = paddle1_vel - 1
        elif msg == "3":
            paddle2_vel = paddle2_vel + 1
        elif msg == "4":
            paddle2_vel = paddle2_vel - 1
        '''

        print("Received data: ", msg)
        parsed_msg = msg.split(",")
        #paddle1_vel = int(msg)
        #paddle2_vel = int(msg)
        accel1=0
        accel2=0
        if parsed_msg[0] == "1":
            paddle1_pos[1] = 200 + 4*int(parsed_msg[1])
            accel1=int(parsed_msg[1])
            setx1(accel1)
        if parsed_msg[0] == "2":
            paddle2_pos[1] = 200 + 4*int(parsed_msg[1])
            accel2=int(parsed_msg[1])
            setx2(accel2)
        if paddle1_pos[1] > 360:
            paddle1_pos[1] = 360
        if paddle2_pos[1] > 360:
            paddle2_pos[1] = 360
        if paddle1_pos[1] < 40:
            paddle1_pos[1] = 40
        if paddle2_pos[1] < 40:
            paddle2_pos[1] = 40

                # Create figure for plotting
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        plt.title('hw4 Project animated plot')
        ax2 = fig.add_subplot(212)
        ax1.set(ylabel='Acceleration1 (mg)')
        ax2.set(ylabel='Acceleration2 (mg)')

        # plot parameters
        x_len = 200
        accel1_range = [-100, 100]
        accel2_range = [-100, 100]
        xs = list(range(0, 200))
        ys1 = [0] * x_len
        ys2 = [0] * x_len
        ax1.set_ylim(accel1_range)
        line1, = ax1.plot(xs, ys1, animated=True)
        ax2.set_ylim(accel2_range)
        line2, = ax2.plot(xs, ys2, animated=True)
        ani = animation.FuncAnimation(fig, animate, fargs=(ys1, ys2), interval=3, blit=True)
        plt.show()


    draw(window)
    #print("Pad 1 pos: ", paddle1_pos[1])
    #print("Pad 2 pos: ", paddle2_pos[1])
    #print("Drew window")

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(60)
    #print("Updated display")