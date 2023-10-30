from turtle import Turtle


class Cube(Turtle):
    def __init__(self, position, color,stretch_factor):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=2, stretch_len=stretch_factor)
        self.color(color)
        self.goto(position)
