from turtle import Turtle


class ScoreBoard(Turtle):
    def __init__(self, position):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.position = position
        self.print_score()

    def print_score(self):
        self.goto(self.position)
        self.write(
            f"{self.score}", False, align="center", font=("Courier", 28, "normal")
        )

    def show_score(self):
        self.score += 1
        self.clear()
        self.print_score()


    def game_over(self):
        self.goto(x=0, y=150)
        self.write(f"GAME OVER", False, align="center", font=("Arial", 32, "bold"))


class HighScore(Turtle):
    def __init__(self, score):
        super().__init__()
        self.high_score = score
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-480,250)
        self.update_high_score()

    def update_high_score(self):
        self.write(
                f"{self.high_score}", False, align="center", font=("Courier", 28, "normal")
            )



class Title(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0,300)
        self.write(
            f"Breakout Game", False, align="center", font=("Courier", 40, "bold"))


class Text(Turtle):
    def __init__(self, position, text):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(position)
        self.write(
            f"{text}", False, align="center", font=("Courier", 28, "normal"))