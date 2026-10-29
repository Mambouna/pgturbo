import pgtrun
import random


# ==================== GAME WINDOW VARIABLES ====================

TITLE = "ASTEROIDS"
ICON = "player"
WIDTH = 800
HEIGHT = 600


# ==================== GAME MECHANICS CONSTANTS ====================

# General constants
INVULNERABLE_DURATION = 4.0
INITIAL_BLOCK_INPUT_DURATION = 1.0
END_BLOCK_INPUT_DURATION = 2.0
SOUND_VOLUME = 0.4
STARS_POSITION = (random.randint(-400, 0), random.randint(-300, 0))

# Player constants
START_LIVES = 3
BLINK_INTERVAL = 0.4
THRUST = 0.2
BRAKE = 0.01
TURN_SPEED = 4

# Bullet constants
BULLET_SIZE = 4
BULLET_SPEED = 10
BULLET_STAY_DURATION = 1.5

# Asteroid constants
ASTEROID_IMAGES = ("asteroid_1", "asteroid_2", "asteroid_3")
SPLIT_SIZE_REDUCTION = 0.4
BIG_SPEED = 1
MEDIUM_SPEED = 2
SMALL_SPEED = 3
BIG_SCORE = 120
MEDIUM_SCORE = 60
SMALL_SCORE = 30


# ==================== GENERAL SETUP ====================

sounds.asteroid_explosion.set_volume(SOUND_VOLUME - 0.1)
sounds.player_explosion.set_volume(SOUND_VOLUME)
sounds.fire.set_volume(SOUND_VOLUME)

storage.load()
storage.setdefault("highscore", 0)

state = {"phase": "start", "level": 1, "input_blocked": True,
         "got_highscore": False}

def unblock_input():
    state["input_blocked"] = False

# Since we start with blocked input, we immediately schedule changing that.
clock.schedule(unblock_input, INITIAL_BLOCK_INPUT_DURATION)

def edge_swap_actor(actor):
    """Teleport the actor so if it left the screen left it reappears at the
    right and same for top and bottom."""
    if actor.right < 0:
        actor.left = WIDTH
    elif actor.left > WIDTH:
        actor.right = 0

    if actor.bottom < 0:
        actor.top = HEIGHT
    elif actor.top > HEIGHT:
        actor.bottom = 0

def start_game(restart):
    player.pos = (WIDTH / 2, HEIGHT / 2)
    player.angle = 90
    player.vel = (0, 0)
    player.data["lives"] = START_LIVES
    make_invulnerable()

    if restart:
        state["level"] = 1
        player.data["score"] = 0

    bullets.clear()

    asteroids.clear()
    spawn_asteroids(state["level"])

    state["phase"] = "game"
    state["got_highscore"] = False
    clock.mark_time("level_start")

def end_game(result):
    state["phase"] = result
    if result == "win":
        state["level"] += 1
    state["input_blocked"] = True
    clock.schedule(unblock_input, END_BLOCK_INPUT_DURATION)

    if player.data["score"] > storage["highscore"]:
        state["got_highscore"] = True
        storage["highscore"] = player.data["score"]
        storage.save()

def get_time_adjusted_score(base_add):
    """Adjust a base score from destroying an asteroid to be lower the later it
    happens."""
    seconds = clock.time_since_mark("level_start")
    return round(base_add / (1 + seconds / 100))


# ==================== PLAYER SETUP ====================

player = Actor("player_horizontal", (WIDTH / 2, HEIGHT / 2))
player.angle = 90
player.data["invulnerable"] = True
player.data["lives"] = START_LIVES
player.data["score"] = 0

def make_vulnerable():
    player.data["invulnerable"] = False
    player.opacity = 1.0
    clock.unschedule(blink_player)

def make_invulnerable():
    player.data["invulnerable"] = True
    clock.schedule(blink_player, BLINK_INTERVAL)
    clock.schedule(make_vulnerable, INVULNERABLE_DURATION)

def blink_player():
    if player.opacity == 0.0:
        player.opacity = 1.0
    else:
        player.opacity = 0.0
    clock.schedule(blink_player, BLINK_INTERVAL)

def lose_life():
    sounds.player_explosion.play()
    player.data["lives"] -= 1
    if player.data["lives"] == 0:
        end_game("dead")
    else:
        player.opacity = 0.0
        make_invulnerable()

def update_player():
    if keyboard.up:
        add_vel = player.velocity_towards_angle(player.angle, THRUST)
        player.vx += add_vel[0]
        player.vy += add_vel[1]
    else:
        player.vx *= 1.0 - BRAKE
        player.vy *= 1.0 - BRAKE

    if keyboard.left:
        player.angle += TURN_SPEED
    elif keyboard.right:
        player.angle -= TURN_SPEED

    player.move_by_vel()
    edge_swap_actor(player)


# ==================== BULLET SETUP ====================

bullets = []

def delete_bullet(bullet):
    bullets.remove(bullet)
    clock.unschedule(delete_bullet, bullet)

def shoot_bullet():
    sounds.fire.play()
    bullet = Actor.Ellipse(BULLET_SIZE, BULLET_SIZE, "white", player.pos)
    bullet.vel = bullet.velocity_towards_angle(player.angle, BULLET_SPEED)
    bullets.append(bullet)
    clock.schedule(delete_bullet, BULLET_STAY_DURATION, bullet)

def update_bullets():
    for bullet in bullets:
        bullet.move_by_vel()
        edge_swap_actor(bullet)


# ==================== ASTEROID SETUP ====================

asteroids = []

def spawn_asteroids(level):
    for i in range(2 + level):
        new_asteroid = Actor(random.choice(ASTEROID_IMAGES))
        new_asteroid.x = random.randint(100, WIDTH - 100)
        new_asteroid.y = random.randint(100, HEIGHT - 100)
        new_asteroid.angle = random.randint(0, 359)
        new_asteroid.data["speed"] = BIG_SPEED
        asteroids.append(new_asteroid)

def destroy_asteroid(asteroid):
    sounds.asteroid_explosion.play()
    asteroids.remove(asteroid)

    if asteroid.scale_x > 0.5:
        for i in range(3):
            new_asteroid = Actor(random.choice(ASTEROID_IMAGES), asteroid.pos)
            new_asteroid.angle = random.randint(0, 359)
            new_asteroid.scale = asteroid.scale_x - SPLIT_SIZE_REDUCTION
            if new_asteroid.scale_x > 0.5:
                new_asteroid.data["speed"] = MEDIUM_SPEED
            else:
                new_asteroid.data["speed"] = SMALL_SPEED
            asteroids.append(new_asteroid)

    if asteroid.data["speed"] == BIG_SPEED:
        player.data["score"] += get_time_adjusted_score(BIG_SCORE)
    elif asteroid.data["speed"] == MEDIUM_SPEED:
        player.data["score"] += get_time_adjusted_score(MEDIUM_SCORE)
    else:
        player.data["score"] += get_time_adjusted_score(SMALL_SCORE)

    if len(asteroids) == 0:
        end_game("win")

def update_asteroids():
    i = 0
    while i < len(asteroids):
        asteroid = asteroids[i]
        asteroid.move_forward(asteroid.data["speed"])
        edge_swap_actor(asteroid)

        if not player.data["invulnerable"] and asteroid.colliderect(player):
            lose_life()

        hit = False
        k = 0
        while k < len(bullets):
            bullet = bullets[k]
            if asteroid.colliderect(bullet):
                destroy_asteroid(asteroid)
                delete_bullet(bullet)
                hit = True
            else:
                k = k + 1

        if not hit:
            i = i + 1


# ==================== EVENT HOOKS ====================

def on_key_down(key):
    if state["input_blocked"] or key != keys.SPACE:
        return

    if state["phase"] == "game":
        if not player.data["invulnerable"]:
            shoot_bullet()
    elif state["phase"] == "win":
        start_game(False)
    else:
        start_game(True)


# ==================== GAME LOOP HOOKS ====================

def update():
    if state["phase"] == "game":
        update_player()
        update_bullets()
        update_asteroids()

def draw():
    screen.clear()
    screen.blit("stars", STARS_POSITION)

    for bullet in bullets:
        bullet.draw()

    for asteroid in asteroids:
        asteroid.draw()

    player.draw()

    if state["phase"] == "start":
        screen.draw.text("PRESS SPACE TO START",
                         center=(WIDTH / 2, HEIGHT / 2 - 80), fontsize=48)

    elif state["phase"] == "game":
        for i in range(player.data["lives"]):
            screen.blit("player", (5 + 30 * i, 5))

        screen.draw.text("Level: {}    Score: {}".format(state["level"],
                                                         player.data["score"]),
                         midtop=(WIDTH / 2, 10), fontsize=32)
        screen.draw.text("Highscore: {}".format(storage["highscore"]),
                         topright=(WIDTH - 5, 10), fontsize=32)

    else:
        if state["phase"] == "dead":
            main_text = "YOU DIED"
            start_text = "Press SPACE to restart"
        else:
            main_text = "YOU CLEARED LEVEL {}".format(state["level"] - 1)
            start_text = "Press SPACE to start the next level"

        screen.draw.text(main_text, center=(WIDTH / 2, HEIGHT / 2 - 40),
                         fontsize=48)
        screen.draw.text("Score: {}".format(player.data["score"]),
                         center=(WIDTH / 2, HEIGHT / 2 + 40), fontsize=36)

        if state["got_highscore"]:
            screen.draw.text("New Highscore!",
                             center=(WIDTH / 2, HEIGHT / 2 + 80), fontsize=36)

        if not state["input_blocked"]:
            screen.draw.text(start_text, center=(WIDTH / 2, HEIGHT / 2 + 120),
                             fontsize=36)

pgtrun.go()
