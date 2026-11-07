import random

WIDTH = 600
HEIGHT = 400

cars = []

cars_driving = True

def new_car():
    color = random.choice(["red", "blue", "green", "yellow"])
    car = Actor.Rectangle(80, 50, color)
    spawn = random.randint(1, 4)
    if spawn == 1:
        car.x = -45
        car.y = random.randint(25, HEIGHT - 25)
        car.angle = 0
    elif spawn == 2:
        car.x = WIDTH + 45
        car.y = random.randint(25, HEIGHT - 25)
        car.angle = 180
    elif spawn == 3:
        car.x = random.randint(40, WIDTH - 40)
        car.y = -30
        car.angle = 270
    else:
        car.x = random.randint(40, WIDTH - 40)
        car.y = HEIGHT + 30
        car.angle = 90
    cars.append(car)

clock.schedule_interval(new_car, 0.15)

def on_key_down():
    global cars_driving
    if cars_driving:
        clock.unschedule(new_car)
        cars_driving = False
    else:
        clock.schedule_interval(new_car, 0.15)
        cars_driving = True

def update():
    i = 0
    while i < len(cars):
        car = cars[i]
        car.move_forward(10)
        
        if not car.is_onscreen(40):
            cars.pop(i)
        else:
            i = i + 1

def draw():
    screen.clear()
    for car in cars:
        car.draw()

    screen.draw.text("Cars: " + str(len(cars)), fontsize=32,
                     center=(WIDTH / 2, 40))
