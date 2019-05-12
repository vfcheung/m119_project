from turtle import *
from random import *

tracer(False)
Screen().setup(480, 360)
colormode(255)
bgcolor("sky blue")

# End of Game Message ****************************************

def endgame(message):
    gameover = Turtle()
    gameover.hideturtle()
    gameover.penup()
    gameover.goto(-200,0)
    gameover.write(message, font = ("Arial", 64, "normal"))

# RE: THE BALL ***********************************************

class ball(Turtle):
    def __init__(self):
        penup()
        shape("circle")
        self.x = self.y = 0
        self.dx = randint(20, 100)/30
        self.dy = randint(-100, -20)/30
        self.alive = True
        update()
    def glide(self):
        self.x += self.dx
        self.y += self.dy
        goto(self.x, self.y)
        update()
    def ifOnEdgeBounce(self):
        if self.x > 235:
            if player1.ycor()-40 < self.y < player1.ycor()+40:
                self.dx = -self.dx
            else:
                self.alive = False
                endgame("Game Over!")
        if self.x < -235:
            if player2.ycor()-40 < self.y < player2.ycor()+40:
                self.dx = -self.dx
            else:
                self.alive = False
                endgame("Game Over!")
        elif self.y > 175 or self.y <-175:
            self.dy = -self.dy

ball = ball()

# Paddles ***************************************************

Screen().register_shape("platform.gif")

player1 = Turtle()
player1.shape("platform.gif")
player1.penup()
player1.setx(230)

def up1():
    player1.sety(player1.ycor()+80)
def down1():
    player1.sety(player1.ycor()-80)

player2 = Turtle()
player2.shape("platform.gif")
player2.penup()
player2.setx(-230)

def up2():
    player2.sety(player2.ycor()+80)
def down2():
    player2.sety(player2.ycor()-80)


# THE GAME LOOP **********************************************

while ball.alive == True:
    ball.glide()
    ball.ifOnEdgeBounce()
    onkey(up1, "Up")
    onkey(down1, "Down")
    onkey(up2, "w")
    onkey(down2, "s")
    listen()
    

Screen().exitonclick()
