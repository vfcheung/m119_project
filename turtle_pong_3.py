from turtle import *
from random import randint, random
from time import sleep

start = 0

sliderH, sliderW = 60,20

totalX, totalY = 400, 400
ballX, ballY = 0.0, 0.0
collision = 0

dX = random() + 1#randint(1,2)
dY = random() + 1#randint(1,2)   

# Screen initia
screen = Screen()                        
screen.setup(totalX+50,totalY+50)
#screen.screensize(totalX,totalY)
#screen.title("Ping Pong Game!")
#print ('Screen size:', screen.screensize())
screen.bgcolor('black')

# Turtle 0 Creation => Draws boundaries for the Ping Pong Game
t0 = Turtle()
t0.hideturtle()
t0.color('white'); t0.speed(5)
t0.penup(); t0.goto(0,totalY//2+10); t0.write("Press 'S' to start", True, align="center")
t0.penup(); t0.goto(-totalX//2,-totalY//2); t0.pendown(); t0.goto(-totalX//2,totalY//2); t0.goto(totalX//2,totalY//2); t0.goto(totalX//2,-totalY//2); t0.goto(-totalX//2,-totalY//2); 
t0.penup(); #t0.goto(-180,200); t0.pendown();t0.goto(-180, -200); t0.penup()


# Turtle 1 Creation => Acts as a slider controlled by 'Up' & 'Down' key
t1 = Turtle()
t1.hideturtle()
screen.register_shape("line", ((-sliderW//2,-sliderH//2), (-sliderW//2,sliderH//2), (sliderW//2,sliderH//2), (sliderW//2,-sliderH//2)))
t1.shape('line')
t1.speed(0)
t1.color('red')
t1.setheading(90) # face east at beginning
t1.penup(); t1.goto(-totalX//2 + 10, 0);
t1.showturtle()
 
def go_up():
    #print ('T1 position:',t1.pos())
    t1.fd(5)

def go_down():
    t1.bk(5)

def start_game():
    global start
    start = 1

screen.onkey(go_up, 'Up')
screen.onkey(go_down, 'Down')
screen.onkey(start_game, 'S')


# Turtle 2 Creation => Acts as the ping pong ball 
t2 = Turtle()
t2.shape('circle'); t2.speed(0)
t2.color('blue')
t2.penup(); t2.goto(ballX,ballY);
t1.setheading(90)
#print ('Ball size:', t2.turtlesize())

def move_t2():
    global sliderH, sliderW
    global totalX, totalY
    global ballX, ballY
    global dX, dY
    global collision
    global start

    t2.goto(ballX, ballY)


##    if ballX < - totalX//2 + 10:
##        dX = -dX
    sliderX, sliderY = t1.pos()

    # Hit on the slider
    if ballY >= (sliderY - sliderH//2)and ballY <= (sliderY + sliderH//2) and ballX <= -totalX//2 + sliderW + 10:
        if collision == 0:
            dX = -dX
            collision = 1
    # Missed the slider
    if ballY <= (sliderY - sliderH//2) or ballY >= (sliderY + sliderH//2):
        if ballX <= -totalX//2 + sliderW + 10 -5:
            start = 0
            #bye()
    
    if ballX >= -totalX//2 + sliderW + 10:
        collision = 0
    
    if ballX > totalX//2 -10:
        dX = -dX
    if ballY > totalY//2 - 10:
        dY = -dY
    if ballY < -totalY//2 + 10:
        dY = -dY       

    if start == 1:
        ballX += dX
        ballY += dY
    else:
        
        ballX = 0
        ballY = 0
    
    screen.ontimer(move_t2,1)

move_t2()

screen.listen()
screen.mainloop()
