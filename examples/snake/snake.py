import pgtrun
import random


# ==================== GAME MECHANICS CONSTANTS ====================

# Grid
TILE_PX_SIZE = 24
HORIZONTAL_TILES = 20
VERTICAL_TILES = 15

# Game speed
INITIAL_UPDATE_INTERVAL = 0.4
UPDATE_INTERVAL_DIVISOR = 80


# ==================== GAME WINDOW VARIABLES ====================

TITLE = "Snake"
ICON = "snake_head"
WIDTH = TILE_PX_SIZE * HORIZONTAL_TILES
HEIGHT = TILE_PX_SIZE * VERTICAL_TILES


# ==================== UTILITY FUNCTION ====================

def grid_from_pos(position):
    return (position[0] // TILE_PX_SIZE, position[1] // TILE_PX_SIZE)

def pos_from_grid(grid_coords):
    return ((grid_coords[0]) * TILE_PX_SIZE + TILE_PX_SIZE / 2,
            (grid_coords[1]) * TILE_PX_SIZE + TILE_PX_SIZE / 2)


# ==================== SNAKE / PLAYER SETUP ====================

snake = Actor("snake_head")
snake.pos = pos_from_grid(grid_from_pos((WIDTH / 2, HEIGHT / 2)))
snake.angle = 90
snake.data["alive"] = True
snake.data["next_move"] = "straight"
snake.data["spawn_segment"] = False
snake.data["turns"] = []
snake.data["score"] = 0

def update_snake():
    if snake.data["next_move"] == "turn_left":
        snake.angle += 90
        snake.data["turns"].insert(0, ("left", 0))
    elif snake.data["next_move"] == "turn_right":
        snake.angle -= 90
        snake.data["turns"].insert(0, ("right", 0))
    snake.data["next_move"] = "straight"

    snake.move_forward(TILE_PX_SIZE)

    if not snake.is_onscreen(-1):
        snake.data["alive"] = False

    if snake.distance_to(apple) < TILE_PX_SIZE / 2:
        snake.data["score"] += 1
        apple.pos = pos_from_grid((random.randint(0, HORIZONTAL_TILES - 1),
                                   random.randint(0, VERTICAL_TILES - 1)))
        snake.data["spawn_segment"] = True

def increment_turns():
    k = 0
    while k < len(snake.data["turns"]):
        current_turn = snake.data["turns"][k]
        snake.data["turns"][k] = (current_turn[0], current_turn[1] + 1)

        k = k + 1

    if snake.data["turns"] and snake.data["turns"][-1][1] > len(segments):
        snake.data["turns"].pop(-1)


# ==================== TAIL SETUP ====================

segments = []
for i in range(3):
    segment = Actor("snake_straight")
    segment.x = snake.x
    segment.y = snake.y + TILE_PX_SIZE * (i + 1)
    segment.angle = 90
    segments.append(segment)

segments[-1].image = "snake_tail"

def spawn_segment():
    new_segment = Actor("snake_straight")
    if segments[-1].image == "snake_straight":
        new_segment.angle = segments[-1].angle
    elif segments[-1].image == "snake_turn_left":
        new_segment.angle = segments[-1].angle - 90
    else:
        new_segment.angle = segments[-1].angle + 90
    new_segment.pos = segments[-1].pos
    new_segment.move_backward(TILE_PX_SIZE)
    segments.append(new_segment)
    snake.data["spawn_segment"] = False

def update_segments():
    turn_index = 0
    if len(snake.data["turns"]) > 0:
        next_turn = snake.data["turns"][turn_index]
    else:
        next_turn = ("nothing", -1)

    for i in range(len(segments)):
        segment = segments[i]
        segment.image = "snake_straight"
        segment.move_forward(TILE_PX_SIZE)

        if i == next_turn[1]:
            if next_turn[0] == "left":
                segment.angle += 90
                segment.image = "snake_turn_left"
            else:
                segment.angle -= 90
                segment.image = "snake_turn_right"
            
            turn_index += 1
            if turn_index < len(snake.data["turns"]):
                next_turn = snake.data["turns"][turn_index]

        if segment.distance_to(snake) < TILE_PX_SIZE / 2:
            snake.data["alive"] = False


# ==================== APPLE SETUP ====================

apple = Actor("apple", (-100, -100))
apple.pos = pos_from_grid((random.randint(0, HORIZONTAL_TILES - 1),
                           random.randint(0, VERTICAL_TILES - 1)))


# ==================== EVENT HOOKS ====================

def on_key_down(key):
    if key == keys.LEFT:
        snake.data["next_move"] = "turn_left"
    elif key == keys.RIGHT:
        snake.data["next_move"] = "turn_right"


# ==================== CUSTOM UPDATE FUNCTION ====================

def update_interval():
    if not snake.data["alive"]:
        return

    update_snake()

    update_segments()

    increment_turns()

    if snake.data["spawn_segment"]:
        spawn_segment()

    segments[-1].image = "snake_tail"

    new_interval = (INITIAL_UPDATE_INTERVAL
                    / (1 + snake.data["score"] / UPDATE_INTERVAL_DIVISOR))

    clock.schedule(update_interval, new_interval)
    
# We have to start the custom update cycle manually here.
clock.schedule(update_interval, INITIAL_UPDATE_INTERVAL)


# ==================== GAME LOOP HOOKS ====================

def draw():
    screen.clear()

    for segment in segments:
        segment.draw()

    apple.draw()

    snake.draw()

    score_text = "Score: {}".format(snake.data["score"])

    if snake.data["alive"]:
        screen.draw.text(score_text, topright=(WIDTH - 5, 5))

    else:
        screen.draw.text("YOU DIED", center=(WIDTH / 2, HEIGHT / 2),
                         fontsize=42)
        screen.draw.text(score_text, center=(WIDTH / 2, HEIGHT / 2 + 40))


pgtrun.go()
