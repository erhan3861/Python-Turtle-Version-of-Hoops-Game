import turtle
import math
import time
import random
import mlmodel

# Window
screen = turtle.Screen()
screen.title("🏀 Basketball AI 🏀")
screen.addshape("basketball.gif")
screen.addshape("target.gif")
screen.addshape("rim.gif")
screen.tracer(0)

# Variables
shoot = False
score = 0


start_x = random.randint(-200, 50) # ball start x position
start_y = random.randint(-100, 0) # ball start y position

x, y = start_x, start_y # ball's game x and y position

speed_x = 0
speed_y = 0
power = 1
current_direction = 90

# turtle objects
# Ball
ball = turtle.Turtle()
ball.shape("basketball.gif")
ball.up()

# Target
target = turtle.Turtle()
target.shape("target.gif")
target.up()
target.goto(290, 60)

# Left rim
left_rim = turtle.Turtle()
left_rim.shape("rim.gif")
left_rim.up()
left_rim.goto(250, 35)

# Right rim
right_rim = turtle.Turtle()
right_rim.shape("rim.gif")
right_rim.up()
right_rim.goto(310, 35)

# Backboard
backboard = turtle.Turtle()
backboard.shape("circle")
backboard.ht()
backboard.up()
backboard.goto(325, 90) # 110 sağ, 20 yukarı

# Sensor
sensor = turtle.Turtle()
sensor.shape("square")
sensor.ht()
sensor.up()
sensor.goto(280, 10) # 110 sağ, 20 yukarı


# power contoller
power_turtle = turtle.Turtle()
power_turtle.shape("turtle")
power_turtle.color("red")
power_turtle.up()
power_turtle.goto(-150, 200)
power_turtle.down()
power_turtle.fd(-100)

# power writings
power_value = turtle.Turtle()
power_value.ht()
power_value.up()
power_value.goto(-250, 230)
power_value.write("Power = 1" , font=("arial", 15, "bold"))

# green sign on the ball to show shooting direction
sign_turtle = turtle.Turtle()
sign_turtle.shape("classic")
sign_turtle.color("lime")
sign_turtle.shapesize(2)
sign_turtle.up()

# set positions of ball and green sign over it
ball.setpos(start_x, start_y)
sign_turtle.setpos(start_x + 10, start_y)

# Functions
def power_turtle_drag(x,y):
  global power
  if -250 <= power_turtle.xcor() <= -140:
    if x < -250: x = -250
    elif x > -160: x = -160
    
    power_turtle.setx(x)
    power = (power_turtle.xcor() + 250) / 10 
    power = int(power) + 1 # prevent from 0
    power_value.clear()
    power_value.write("Power = " + str(power), font=("arial", 15, "bold"))

    screen.update()

power_turtle.ondrag(power_turtle_drag)

# power contoller
direction_turtle = turtle.Turtle()
direction_turtle.shape("turtle")
direction_turtle.color("red")
direction_turtle.up()
direction_turtle.goto(0, 200)
direction_turtle.down()
direction_turtle.fd(-100)

direction_value = turtle.Turtle()
direction_value.ht()
direction_value.up()
direction_value.goto(-100, 230)
direction_value.write("Direction = 5" , font=("arial", 15, "bold"))

def direction_turtle_drag(x,y):
  global current_direction, shoot
  if -100 <= direction_turtle.xcor() <= 0:
    if x < -100: x = -100
    elif x > 0: x = 0
    
    direction_turtle.setx(x)
    
    current_direction = (direction_turtle.xcor() + 100)
    current_direction = int(current_direction)
    if current_direction <= 5:
      current_direction = 5
    elif current_direction > 80:
      current_direction = 80

    ball.seth(current_direction)
    
    if shoot == False:
      sign_turtle.setpos(ball.pos())
      sign_turtle.fd(10)
      sign_turtle.st()
      sign_turtle.seth(85-current_direction)

    direction_value.clear()
    direction_value.write("Direction = " + str(current_direction), font=("arial", 15, "bold"))

    screen.update()

direction_turtle.ondrag(direction_turtle_drag)

# Score writing
score_turtle = direction_value.clone()
score_turtle.open = False
score_turtle.goto(90, 230)
score_turtle.write("Score = 0" , font=("arial", 15, "bold"))


def shoot_func():
  global shoot, current_direction, speed_x, speed_y

  direction = current_direction * (math.pi/180)
  speed_x = math.sin(direction) * (1.3 * power + 13)
  speed_y = math.cos(direction) * (1.3 * power + 13)
  print(speed_x, speed_y)
  shoot = True
  sign_turtle.ht()

  score_turtle.open = True # for scoring once

def movement():
  global speed_x, speed_y, x, y
  speed_y -= 1
  if ball.ycor() < -257 and (speed_y < 0 or speed_y == 0):
    if abs(speed_x) > 2:
      if speed_x > 0:
        speed_x -= 1
      else:
        speed_x += 1
    else:
      speed_x = 0

    if abs(speed_y) > 3:
      speed_y = 0 - (speed_y + 3)
    else:
      speed_y = 0
  x += speed_x
  y += speed_y
  ball.goto(x, y)
  
def interactions():
  global speed_x, speed_y, score

  if ball.distance(right_rim) < 30:
    ball.seth(math.atan((speed_x / (speed_y + 0.001)) * 1) + (90 - ((speed_y / (abs(speed_y) + 0.001)) * 90)))

    a_vel = math.sqrt((speed_x * speed_x) + (speed_y * speed_y))
    
    ball.seth(2 * (90 + ((math.acos(((right_rim.ycor()-ball.ycor()) / ball.distance(right_rim))* 1)) * (((right_rim.xcor()-ball.xcor())+0.001) / (abs(right_rim.xcor()-ball.xcor())+0.001)))) - ball.heading())

    # ((math.acos((left_rim.ycor()-ball.ycor()) / ball.distance(left_rim))) * (((left_rim.xcor()-ball.xcor())+0.001) / (abs(left_rim.xcor()-ball.xcor())+0.001)))

    speed_x = (math.sin(ball.heading()) * a_vel) * 0.8
    speed_y = (math.cos(ball.heading()) * a_vel) * 0.8
    # if ball.distance(right_rim) < 15: return
    return


  if ball.distance(left_rim) < 30:
      ball.seth(math.atan((speed_x / (speed_y + 0.001)) * 1) + (90 - ((speed_y / (abs(speed_y) + 0.001)) * 90)))

      a_vel = math.sqrt((speed_x * speed_x) + (speed_y * speed_y))
      
      ball.seth(2 * (90 + ((math.acos(((left_rim.ycor()-ball.ycor()) / ball.distance(left_rim))* 1)) * (((left_rim.xcor()-ball.xcor())+0.001) / (abs(left_rim.xcor()-ball.xcor())+0.001)))) - ball.heading())

      # ((math.acos((left_rim.ycor()-ball.ycor()) / ball.distance(left_rim))) * (((left_rim.xcor()-ball.xcor())+0.001) / (abs(left_rim.xcor()-ball.xcor())+0.001)))

      speed_x = (math.sin(ball.heading()) * a_vel) * 0.8
      speed_y = (math.cos(ball.heading()) * a_vel) * 0.8
      return
      # if ball.distance(left_rim) < 15: return

  if collision(ball, backboard):
    speed_x = speed_x * -0.8
    speed_y = speed_y * 0.9  

  if ball.xcor() > 300 or ball.xcor() < -300:
    speed_x *= -0.8

  if ball.distance(sensor) < 18:
    # scoring
    if score_turtle.open : 
      score += 1
      score_turtle.open = False

      # save to csv file
      data_list = [start_x, start_y, round(power), round(current_direction)]
      mlmodel.save_to_csv(data_list, "data.csv")
    score_turtle.clear()
    score_turtle.write("Score = " + str(score), font=("arial", 15, "bold"))
 
def reset_func():
  global x, y, shoot

  shoot = False
  x, y = start_x, start_y
  ball.setpos(x, y)

  sign_turtle.goto(x, y)
  sign_turtle.fd(10)
  sign_turtle.st()

def new_shoot_func():
  global x, y, shoot, start_x, start_y

  shoot = False
  start_x = random.randint(-200, 50) # ball new start x position
  start_y = random.randint(-100, 0) # ball new start y position
  x, y = start_x, start_y
  ball.setpos(x, y)

  sign_turtle.goto(x, y)
  sign_turtle.fd(10)
  sign_turtle.st()

def collision(t1, t2):
  # print(abs(t1.xcor()-t2.xcor()), abs(t1.ycor()-t2.ycor()) )
  if abs(t1.xcor()-t2.xcor()) < 40 and abs(t1.ycor()-t2.ycor()) < 85:
    # print("collision")
    return True

# Keyboard inputs
screen.listen()
screen.onkey(reset_func, "r")
screen.onkey(shoot_func, "s")
screen.onkey(new_shoot_func, "n")


def show_distance(x,y):
  ball.setpos(x,y)
  # print(abs(ball.xcor()-backboard.xcor()), abs(ball.ycor()-backboard.ycor()) )
  print(ball.distance(sensor))
  # print(ball.distance(left_rim), ball.distance(right_rim))
  
screen.onclick(show_distance, 3)

def model_func():
  global power, current_direction

  model = mlmodel.train_model("data.csv")
  result = mlmodel.predict(model, [start_x, start_y])
  power = result[0][0]
  current_direction = result[0][1]
  print(power, current_direction)

  # new values
  power_value.clear()
  power_value.write("Power = " + str(round(power)), font=("arial", 15, "bold"))

  direction_value.clear()
  direction_value.write("Direction = " + str(round(current_direction)), font=("arial", 15, "bold"))

  # shooting
  shoot_func()

screen.onkey(model_func, "m")

# Game loop
while True:
  if shoot:
    movement()
    interactions()
  time.sleep(0.05)
  screen.update()
  

