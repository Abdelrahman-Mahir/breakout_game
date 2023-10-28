from turtle import Turtle

MOVEMENT_DISTANCE = 60


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=6)
        self.color("white")
        self.goto(position)

    def right_move(self):
        self.goto(x=self.xcor() + MOVEMENT_DISTANCE, y=self.ycor())

    def left_move(self):
        self.goto(x=self.xcor() - MOVEMENT_DISTANCE, y=self.ycor())
