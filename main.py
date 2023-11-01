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
# TODO: Updating the screen as the speed increases


def generate_cube(cube_color, y_position, cube_list):
    """This function generates a cube with random width and random color. The function also keeps track of the
    available width on the screen. The function returns the cube object. The function also randomly generates a cube
    with 2 lives"""
    global start_x, available_width, is_done
    random_width = random.choice([30,32, 35,37, 40])
    double_cube = random.randint(1, 12)
    gap = 5
    start_x += gap + random_width
    remaining_space = available_width - random_width - gap
    available_width = remaining_space
    if double_cube > 2:
        if remaining_space > random_width:
            cube = Cube((start_x, y_position), color=cube_color, stretch_factor=random_width / 20)
            cube_list.append(cube)
            return cube
        elif 0 < remaining_space < random_width:
            cube = Cube((start_x, y_position), color=cube_color, stretch_factor=(remaining_space - 5) / 20)
            cube_list.append(cube)
            return cube
        elif remaining_space <= 0:
            is_done = True
            return is_done
    else:
        if remaining_space > random_width:
            cube = Cube((start_x, y_position), color="#4B0082", stretch_factor=random_width / 20)
            cube_list.append(cube)
            return cube
        elif 0 < remaining_space < random_width:
            cube = Cube((start_x, y_position), color="#4B0082", stretch_factor=(remaining_space - 5) / 20)
            cube_list.append(cube)
            return cube
        elif remaining_space <= 0:
            is_done = True
            return is_done


def high_score_tracker(operation, new_score=0):  # High score tracker
    """This function keeps track of the high score. The function takes in 2 arguments. The first argument
    is the operation, either "read" or "update". It creates or read a file called high_score.txt. The function
    saves the high score with its date. In the case of "update" operation, the function compares the new score with the
     existing one"""
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


def cube_collision(cube_collided, cube_list, list_name):
    """"The function takes in 3 arguments. The first argument is the cube that the ball collided with.
    The second is the list of cubes, and the third is just a color name from the general cubes' dictionary. It measures
    the distance between the ball and the cube, and moves the cube to a far away location if the distance is less
    than 40. The function also increases the ball speed and the score depending on the color of the cube. It also
    changes the double cube color to its row's color"""
    if (ball.ycor() < 310 and cube_collided.distance(ball) < 40) or (
            ball.ycor() > -310 and cube_collided.distance(ball) < 40
    ):
        cube_color = cube_collided.color()
        ball.y_bounce()
        if cube_color[0] == (0.29411764705882354, 0.0, 0.5098039215686274):
            cube_collided.color(list_name)
        else:
            cube_collided.goto(1000, 1000)
            cube_list.remove(cube_collided)
            if cube_color[0] == "white":
                ball.movement_speed *= 1.1
                score.show_score(2)
            elif cube_color[0] == "red":
                ball.movement_speed *= 1.3
                score.show_score(4)
            elif cube_color[0] == "blue":
                ball.movement_speed *= 1.5
                score.show_score(5)
            screen.update()
            print(f"Ball speed is {ball.movement_speed}")


# ----------------------------- Main Program ----------------------------- #
# ----------------------------- GUI Setup ----------------------------- #
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
high_score = HighScore(high_score_tracker("read"))

# ----------------------------- Cubes Setup----------------------------- #
white_cubes = []
red_cubes = []
blue_cubes = []
cubes_list = [white_cubes, red_cubes, blue_cubes]

# The following lists are used to generate the cubes, and they are used in the zip function below
start_x_values = [-650, -650, -650]
available_width = [1280, 1280, 1280]
colors = ["white", "red", "blue"]
height_offsets = [-100, -50, 0]

for start_x, color, height_offset, cubes_list, available_width in zip(start_x_values, colors, height_offsets, cubes_list, available_width):
    is_done = False
    while not is_done:
        generate_cube(color, height_offset, cubes_list)

# ----------------------------- Game Setup ----------------------------- #
# The following code is used to move the paddle
screen.listen()
screen.onkey(fun=user_paddle.right_move, key="Right")
screen.onkey(fun=user_paddle.left_move, key="Left")

# This dictionary is used in the cube_collision function. The keys are passed later as the list_name
# argument to change the purple cubes to their row's color
cubes_dict = {"white": white_cubes, "red": red_cubes, "blue": blue_cubes}
print(f" Initial Ball speed is {ball.movement_speed}") # This is just for testing purposes

# ----------------------------- Game Loop ----------------------------- #
game_lives = 3
is_game_on = True
while is_game_on:
    screen.update()
    time.sleep(0.1)
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

    # Side walls bounce
    if ball.xcor() > 615 or ball.xcor() < -615:
        ball.x_bounce()

    # Paddle bounce. Needs more refinement
    if -310 < ball.ycor() < 310 and user_paddle.distance(ball) < 35:
        ball.y_bounce()

    # Cube collision
    for k,v in cubes_dict.items():
        for cube in v:
            cube_collision(cube_collided=cube, cube_list=v,list_name=k)


screen.exitonclick()
