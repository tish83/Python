"""
1. Stwórz ciało węża
2. Poruszanie się węża
3. Kontrolowanie ruchu węża
4. Obsługa kolizji z jedzeniem
5. Tablica wyników
6. Obsługa kolizji ze ścianą
7. Obsługa kolizji z ogonem
"""

import random
import time
from turtle import Turtle, Screen

STARTING_POSITIONS = [(0,0),(-20,0),(-40,0)] #3segmentowy snake
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
ALIGNMENT = "center"
FONT = ("Courier", 18, "normal")

class Snake:
    
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):    
        new_segment = Turtle("square")
        new_segment.color("white")
        #teraz musimy powiedzieć żeby nie rysował linii "podnieś długopis"
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def reset(self):
        for seg in self.segments:
            seg.goto(1000,1000) #wyrzucamy segmenty za planszę
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]

    def extend(self):
        self.add_segment(self.segments[-1].position())
    
    def move(self):
        for seg_num in range(len(self.segments)-1,0,-1):
            new_x = self.segments[seg_num-1].xcor()
            new_y = self.segments[seg_num-1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)
    
    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)
    
    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)


class Apple(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(0.5, 0.5)
        self.color("red")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        rand_x = random.randint(-280, 280)
        rand_y = random.randint(-280, 280)
        self.goto(rand_x, rand_y)

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open('score.txt', 'r') as odczyt: #D:\CKU\Python\programy\snakeGame\snakeGame.py
            score_from_file = int(odczyt.read())
        self.high_score = score_from_file
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High score: {self.high_score}", align=ALIGNMENT, font=FONT)
    
    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('score.txt', 'w') as zapis:
                zapis.write(str(self.high_score))
        self.score = 0
        self.update_scoreboard()

    """funkcja kończąca grę jeżeli nie chcemy zapisywać high_score
    def game_over(self):
        self.goto(0,0)
        self.write(f"GAME OVER!", align=ALIGNMENT, font=FONT)
    """
    
    def increase_score(self):
        self.score +=1
        self.clear()
        self.update_scoreboard()
        
s = Screen()
s.setup(width=600,height=600)
s.bgcolor("black")
s.title("Snake Game i Python")
s.tracer(0) #wyłączamy śledzenie zmian ekranu, będziemy to kontrolować sami żeby nasz wąż poruszał się płynnie

snake = Snake()
apple = Apple()
scoreboard = Scoreboard()

s.listen()
s.onkey(snake.up, "Up")
s.onkey(snake.down, "Down")
s.onkey(snake.left, "Left")
s.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    s.update() #odświeżamy ekran po załadowaniu wszystkich segmentów węża
    time.sleep(0.1) #opóźniamy ruch, żeby były połączone segmenty
    #przesuniemy naszego węża w każdym możliwym kierunku, musi on funkcjonować trochę jak dżdżownica - najpierw przesuwa tył, żeby wypchnąć przód
    snake.move()    

    #kolizja z jedzeniem, skorzystamy z funkcji biblioteki Turtle -> distance
    if snake.head.distance(apple) < 15:
        apple.refresh()
        snake.extend()
        scoreboard.increase_score()

    #kolizja ze ścianą
    if snake.head.xcor() > 290 or snake.head.xcor() <- 290 or snake.head.ycor() > 290 or snake.head.ycor() <- 290:
        #game_is_on = False
        #scoreboard.game_over()
        scoreboard.reset()
        snake.reset()

    #kolizja z ogonem
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) <10 :
            #game_is_on = False
            #scoreboard.game_over()
            scoreboard.reset()
            snake.reset()

s.exitonclick()