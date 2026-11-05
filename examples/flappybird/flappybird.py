import pgtrun
import random


# ==================== GAME WINDOW VARIABLES ====================

TITLE = 'Flappy Bird'
WIDTH = 400
HEIGHT = 708


# ==================== GAME MECHANICS CONSTANTS ====================

# These constants control the difficulty of the game
GAP = 130
GRAVITY = 0.3
FLAP_STRENGTH = 6.5
SPEED = 3


# ==================== PERSISTENT DATA SETUP ====================

storage.autosave = True
storage.load()
storage.setdefault('highscore', 0)


# ==================== BIRD ACTOR SETUP ====================

bird = Actor('bird', (75, 200))
bird.top_limit = 0
bird.data["dead"] = False
bird.data["score"] = 0

def flap_bird():
    if not bird.data["dead"]:
        bird.vy = -1 * FLAP_STRENGTH

def update_bird():
    bird.vy += GRAVITY
    bird.move_by_vel()

    if not bird.data["dead"]:
        if bird.vy < -3:
            bird.angle = 30
            bird.image = 'bird_up'
        else:
            bird.angle = 0
            bird.image = 'bird'

    if bird.collidemask(pipe_top) or bird.collidemask(pipe_bottom):
        bird.data["dead"] = True
        bird.image = 'bird_dead'

    if bird.top > HEIGHT:
        bird.y = 200
        bird.data["dead"] = False
        bird.data["score"] = 0
        bird.vy = 0
        reset_pipes()


# ==================== PIPE ACTORS SETUP ====================

pipe_top = Actor('top', anchor=('left', 'bottom'))
pipe_bottom = Actor('bottom', anchor=('left', 'top'))

def reset_pipes():
    pipe_gap_y = random.randint(200, HEIGHT - 200)
    pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
    pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)


reset_pipes()  # Set initial pipe positions.

def update_pipes():
    pipe_top.left -= SPEED
    pipe_bottom.left -= SPEED
    if pipe_top.right < 0:
        reset_pipes()
        if not bird.data["dead"]:
            bird.data["score"] += 1
            if bird.data["score"] > storage['highscore']:
                storage['highscore'] = bird.data["score"]


# ==================== EVENT HOOKS ====================

def on_key_down():
    flap_bird()


# ==================== GAME LOOP HOOKS ====================

def update():
    update_pipes()
    update_bird()


def draw():
    screen.blit('background', (0, 0))

    pipe_top.draw()
    pipe_bottom.draw()
    bird.draw()

    screen.draw.text(
        str(bird.data["score"]),
        color='white',
        midtop=(WIDTH // 2, 10),
        fontsize=70,
        shadow=(1, 1)
    )

    screen.draw.text(
        "Best: {}".format(storage['highscore']),
        color=(200, 170, 0),
        midbottom=(WIDTH // 2, HEIGHT - 10),
        fontsize=30,
        shadow=(1, 1)
    )


pgtrun.go()
