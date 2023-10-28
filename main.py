import time
from turtle import Screen
from paddle import Paddle
from cubes import Cube
from ball import Ball
import random

screen = Screen()
screen.bgcolor("black")
screen.title("Blackout Game")
screen.setup(width=1280, height=720)
screen.tracer(0)

user_paddle = Paddle((0, -320))
ball = Ball()

cubes = []
def generate_cube(color, y_position):
    global start_x, available_width, is_done
    random_width = random.choice([30,32, 35,37, 40])
    gap = 5
    start_x += gap + random_width
    remaining_space = available_width - random_width - gap
    available_width = remaining_space
    if remaining_space > random_width:
        cube = Cube((start_x, y_position), color=color, stretch_factor=random_width / 20)
        cubes.append(cube)
        return cube
    elif 0 < remaining_space < random_width:
        cube = Cube((start_x, y_position), color=color, stretch_factor=(remaining_space - 5) / 20)
        cubes.append(cube)
        return cube
    elif remaining_space <= 0:
        is_done = True
        return is_done


start_x_values = [-650, -650, -650]
available_width = [1280, 1280, 1280]
colors = ["white", "red", "blue"]
height_offsets = [0, 50, 100]

for start_x, color, height_offset, available_width in zip(start_x_values, colors, height_offsets,available_width):
    is_done = False
    while not is_done:
        generate_cube(color, height_offset)


screen.listen()
screen.onkey(fun=user_paddle.right_move, key="Right")
screen.onkey(fun=user_paddle.left_move, key="Left")

is_game_on = True
while is_game_on:
    screen.update()
    time.sleep(ball.movement_speed)
    ball.move()

    if ball.ycor() > 310:
        ball.y_bounce()

    if ball.ycor() < -310:
        ball.refresh(x=user_paddle.xcor(), y=user_paddle.ycor() + 50)

    if ball.xcor() > 615 or ball.xcor() < -615:
        ball.x_bounce()

    if -305 < ball.ycor() < 310 and user_paddle.distance(ball) < 60:
        ball.y_bounce()

    for cube in cubes:
        if (ball.ycor() < 310 and cube.distance(ball) < 40) or (
            ball.ycor() > -310 and cube.distance(ball) < 40
        ):
            ball.y_bounce()
            cube.goto(1000, 1000)
            cubes.remove(cube)
            screen.update()
            print(len(cubes))


screen.exitonclick()
