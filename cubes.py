from turtle import Turtle
import random

random_number = random.choice([0.5, 1, 1.25, 1.5, 1.75, 2])
class Cube(Turtle):
    def __init__(self, position, color,stretch_factor):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=2, stretch_len=stretch_factor)
        self.color(color)
        self.goto(position)
