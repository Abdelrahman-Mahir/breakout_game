import time
from turtle import Screen
from paddle import Paddle
from cubes import Cube
from ball import Ball
from screen_text import ScoreBoard, Title, Text, HighScore
import random
from datetime import datetime
import os

# TODO: Solve near paddle collision issue - The Problem is when the ball is hitting the edge of the paddle
# TODO: Add extra cube for different levels
# TODO: Randomize ball bounce angle


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


def high_score_tracker(operation, new_score=0):  # High score tracker
    today = datetime.today().strftime('%d-%m-%Y')
    if operation == "read":
        with open("high_score.txt", mode="a+") as file:
            if os.path.getsize('high_score.txt') == 0:
                initialized_score = 0
                file.write(f"{today} User's Highest Score: {initialized_score}\n")
                return initialized_score
            else:
                file.seek(0)  # Move the cursor back to the Start of the line
                data = file.readlines()[-1]
                text = data.split()
                existing_score = int(text[-1])
                return existing_score
    elif operation == "update":
        with open("high_score.txt", mode="a") as file:
            if new_score > high_score_tracker("read"):
                file.write(f"{today} User's Highest Score: {new_score}\n")
            return new_score


screen = Screen()
screen.bgcolor("black")
screen.title("Blackout Game")
screen.setup(width=1280, height=720)
screen.tracer(0)

user_paddle = Paddle((0, -320))
ball = Ball()
title = Title()
score_label = Text((450, 300), "Score")
high_score_label = Text((-480, 300), "High Score")
score = ScoreBoard((450,250))
# high_score = HighScore(10)
high_score = HighScore(high_score_tracker("read"))
cubes = []


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

no_cubes = len(cubes) # Number of cubes is used to increase the speed of the ball as the game progresses
game_lives = 3
is_game_on = True
while is_game_on:
    screen.update()
    time.sleep(ball.movement_speed)
    ball.move()

    if ball.ycor() > 310:
        ball.y_bounce()

    if ball.ycor() < -330:
        ball.refresh(x=user_paddle.xcor() + 10, y=user_paddle.ycor() + 50)
        game_lives -= 1
        if game_lives == 0:
            score.game_over()
            high_score_tracker("update", score.score)
            high_score.clear()
            high_score = HighScore(high_score_tracker("read"))
            is_game_on = False

    if ball.xcor() > 615 or ball.xcor() < -615:
        ball.x_bounce()

    if -310 < ball.ycor() < 310 and user_paddle.distance(ball) < 35:
        ball.y_bounce()

    for cube in cubes:
        if (ball.ycor() < 310 and cube.distance(ball) < 40) or (
            ball.ycor() > -310 and cube.distance(ball) < 40
        ):
            ball.y_bounce()
            cube.goto(1000, 1000)
            cubes.remove(cube)
            score.show_score()
            screen.update()
            print(len(cubes))
            if no_cubes - len(cubes) == 5:
                ball.movement_speed *= 1.1
                no_cubes = len(cubes)
                print(f"Ball speed is {ball.movement_speed}")


screen.exitonclick()
