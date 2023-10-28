from turtle import Turtle
import random


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.shape("circle")
        self.goto(0,-300)
        self.x_cor = 10
        self.y_cor = 10
        self.movement_speed = 0.1

    def move(self):
        self.goto(self.xcor() + self.x_cor, self.ycor() + self.y_cor)

    def y_bounce(self):
        self.y_cor *= -1

    def x_bounce(self):
        self.x_cor *= -1
        self.movement_speed *= 0.9

    def refresh(self,x,y):
        self.movement_speed = 0.1
        self.goto(x,y)
