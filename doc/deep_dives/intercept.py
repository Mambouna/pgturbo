WIDTH = 400
HEIGHT = 400

thrower = Actor.Rectangle(40, 40, "blue", (WIDTH / 2, HEIGHT / 2))
catcher = Actor.Rectangle(40, 40, "red", (40, 40))
ball = Actor.Ellipse(20, 20, "white", (WIDTH / 2, HEIGHT / 2))

def on_mouse_down(pos):
    ball.pos = thrower.pos
    ball.vel = ball.velocity_towards_point(pos, 5)
    catcher.pos = (40, 40)
    possible_vel = catcher.intercept_velocity(ball, 10)
    if possible_vel:
        catcher.vel = possible_vel
    else:
        catcher.vel = (0, 0)

def update():
    catcher.move_by_vel()
    ball.move_by_vel()

    if catcher.colliderect(ball):
        ball.vel = (0, 0)
        catcher.vel = (0, 0)

def draw():
    screen.fill("darkgreen")
    thrower.draw()
    catcher.draw()
    ball.draw()
