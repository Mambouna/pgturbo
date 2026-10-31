import pgtrun
import random


# ===================== GAME WINDOW VARIABLES =====================

TITLE = "Pong"
WIDTH = 800
HEIGHT = 600


# ===================== GAME MECHANICS CONSTANTS =====================

MAIN_COLOR = "yellow"
WIN_POINTS = 11

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_DIAMETER = 20

PLAYER_SPEED = 5
COMPUTER_SPEED = 4
BALL_SPEED = 8


# ===================== COMPUTER SETUP =====================

computer = Actor.Rectangle(PADDLE_WIDTH, PADDLE_HEIGHT, MAIN_COLOR)
computer.pos = (30, HEIGHT / 2)
computer.y_limits = (20, HEIGHT - 20)
computer.data["score"] = 0
computer.data["bounced"] = False

def computer_reset_start_params():
    computer.data["start_direction"] = random.choice((-1, 1))
    computer.data["start_duration"] = random.randint(5, 20) / 10

computer_reset_start_params()

def update_computer():
    if state["phase"] == "start" and state["start_paddle"] == computer:
        computer.y += COMPUTER_SPEED * computer.data["start_direction"]
        if computer.top <= 20 or computer.bottom >= HEIGHT - 20:
            computer.data["start_direction"] *= -1
    elif state["phase"] == "game":
        if (ball.angle + 90) % 360 <= 180:
            computer.move_towards_point((computer.x, HEIGHT / 2),
                                        COMPUTER_SPEED)
        else:
            computer.move_towards_point((computer.x, ball.y), COMPUTER_SPEED)


# ===================== PLAYER SETUP =====================

player = Actor.Rectangle(PADDLE_WIDTH, PADDLE_HEIGHT, MAIN_COLOR)
player.pos = (WIDTH - 30, HEIGHT / 2)
player.y_limits = (20, HEIGHT - 20)
player.data["score"] = 0
player.data["bounced"] = False

def update_player():
    if state["phase"] != "end":
        if keyboard.up:
            player.y -= PLAYER_SPEED
        if keyboard.down:
            player.y += PLAYER_SPEED


# ===================== BALL SETUP =====================

ball = Actor.Ellipse(BALL_DIAMETER, BALL_DIAMETER, MAIN_COLOR)
ball.x = computer.right + BALL_DIAMETER / 2

def ball_scored(paddle):
    paddle.data["score"] += 1
    if ball.x > WIDTH:
        state["start_paddle"] = computer
        ball.x = computer.right + BALL_DIAMETER / 2
        computer_reset_start_params()
        clock.schedule(shoot_ball, computer.data["start_duration"])
    else:
        state["start_paddle"] = player
        ball.x = player.left - BALL_DIAMETER / 2
    ball.y = state["start_paddle"].y

    if paddle.data["score"] < WIN_POINTS:
        state["phase"] = "start"
    else:
        state["phase"] = "end"
        clock.unschedule_all(shoot_ball)

def shoot_ball():
    if state["start_paddle"] == computer:
        if computer.data["start_direction"] == -1:
            angle = 70 - random.randint(1, 25)
        else:
            angle = -70 + random.randint(1, 25)
    else:
        if keyboard.up:
            angle = 180 - 70 + random.randint(1, 25)
        elif keyboard.down:
            angle = 180 + 70 - random.randint(1, 25)
        else:
            angle = 180 - 50 + random.randint(1, 100)
    ball.angle = angle
    state["phase"] = "game"
    computer.data["bounced"] = False
    player.data["bounced"] = False

clock.schedule(shoot_ball, computer.data["start_duration"])

def update_ball():
    if state["phase"] == "start":
        ball.y = state["start_paddle"].y
    elif state["phase"] == "game":
        if ball.y <= 40 or ball.y >= HEIGHT - 40:
            ball.angle = -1 * ball.angle

        ball.move_forward(BALL_SPEED)

        if ball.collidemask(computer) and not computer.data["bounced"]:
            if computer.left <= ball.x <= computer.right:
                ball.angle = -1 * ball.angle
            else:
                ball.angle = 180 - ball.angle
            ball.angle += random.randint(-10, 10)
            computer.data["bounced"] = True
            player.data["bounced"] = False
        elif ball.collidemask(player) and not player.data["bounced"]:
            if player.left <= ball.x <= player.right:
                ball.angle = -1 * ball.angle
            else:
                ball.angle = 180 - ball.angle
            if keyboard.up:
                ball.angle -= random.randint(5, 10)
            elif keyboard.down:
                ball.angle += random.randint(5, 10)
            else:
                ball.angle += random.randint(-10, 10)
            player.data["bounced"] = True
            computer.data["bounced"] = False

        if ball.right < 0:
            ball_scored(player)
        elif ball.left > WIDTH:
            ball_scored(computer)


# ===================== GAME STATE SETUP =====================

state = {"phase": "start", "start_paddle": computer}


# ===================== EVENT HOOKS =====================

def on_key_down(key):
    if (key == keys.SPACE and state["phase"] == "start"
            and state["start_paddle"] == player):
        shoot_ball()


# ===================== GAME LOOP =====================

def update():
    update_computer()

    update_ball()

    update_player()

    
def draw():
    screen.fill((64, 64, 64))

    computer.draw()
    player.draw()

    screen.draw.text("Computer: {}".format(computer.data["score"]),
                     center=(WIDTH / 4, 40), fontsize=48, color=MAIN_COLOR)
    screen.draw.text("Player: {}".format(player.data["score"]),
                     center=(WIDTH * 3/4, 40), fontsize=48, color=MAIN_COLOR)
    screen.draw.line((WIDTH / 2, 40), (WIDTH / 2, HEIGHT - 40), "yellow")

    ball.draw()

    if state["phase"] == "end":
        if player.data["score"] >= WIN_POINTS:
            screen.draw.text("PLAYER WINS", center=(WIDTH / 2, HEIGHT / 2),
                             fontsize=68, color=MAIN_COLOR)
        else:
            screen.draw.text("COMPUTER WINS", center=(WIDTH / 2, HEIGHT / 2),
                             fontsize=68, color=MAIN_COLOR)

pgtrun.go()
