import pgtrun
import random


# ==================== GAME MECHANICS CONSTANTS ====================

COLUMNS = 4
ROWS = 3
GRID_SIZE = 200
CARD_SIZE_RATIO = 0.90

CARD_COLOR = "lightcoral"
NORMAL_COLOR = "black"
SUCCESS_COLOR = "green"
FAILURE_COLOR = "red"

CARD_FLIP_TIME = 0.1
FAIL_SHOW_TIME = 1.0


# ==================== GAME WINDOW GLOBALS ====================

TITLE = "Memory"
WIDTH = COLUMNS * GRID_SIZE
HEIGHT = ROWS * GRID_SIZE


# ==================== CARD SETUP ====================

cards = []
for i in range(COLUMNS):
    for k in range(ROWS):
        pos = (GRID_SIZE / 2 + GRID_SIZE * i, GRID_SIZE / 2 + GRID_SIZE * k)
        card = Actor.Rectangle(GRID_SIZE * CARD_SIZE_RATIO,
                               GRID_SIZE * CARD_SIZE_RATIO, CARD_COLOR, pos)
        card.data["text_color"] = NORMAL_COLOR
        cards.append(card)

numbers = []
for i in range(COLUMNS * ROWS // 2):
    numbers.append(str(i + 1))
    numbers.append(str(i + 1))

for card in cards:
    card.data["number"] = numbers.pop(random.randint(0, len(numbers) - 1))


# ==================== GENERAL SETUP ====================

state = {"phase": "game", "first_picked": None, "second_picked": None,
         "pairs_to_find": COLUMNS * ROWS / 2, "tries": 0}

def unflip_picked_pair():
    state["first_picked"].data["text_color"] = NORMAL_COLOR
    state["second_picked"].data["text_color"] = NORMAL_COLOR
    state["first_picked"].scale_x = 1.0
    state["second_picked"].scale_x = 1.0

    state["first_picked"] = None
    state["second_picked"] = None

def check_pair():
    first = state["first_picked"]
    second = state["second_picked"]
    state["tries"] += 1

    if first.data["number"] == second.data["number"]:
        first.data["text_color"] = SUCCESS_COLOR
        second.data["text_color"] = SUCCESS_COLOR
        state["pairs_to_find"] -= 1

        if state["pairs_to_find"] == 0:
            state["phase"] = "won"

        state["first_picked"] = None
        state["second_picked"] = None
        
        sounds.success.play()
    else:
        first.data["text_color"] = FAILURE_COLOR
        second.data["text_color"] = FAILURE_COLOR
        clock.schedule(unflip_picked_pair, 1.0)

        sounds.failure.play()


# ==================== EVENT HOOKS ====================

def on_mouse_down(pos):
    if state["first_picked"] and state["second_picked"]:
        return

    for card in cards:
        if card.collidepoint(pos) and card.scale_x == 1.0:
            sounds.flip.play()
            animate(card, duration=CARD_FLIP_TIME, scale_x=0.0)
            if state["first_picked"]:
                state["second_picked"] = card
                check_pair()
            else:
                state["first_picked"] = card


# ==================== GAME LOOP ====================

def draw():
    screen.fill("white")
    for card in cards:
        card.draw()
        if card.scale_x == 0.0:
            screen.draw.text(card.data["number"],
                             center=(card.x, card.y + GRID_SIZE / 10),
                             fontsize=GRID_SIZE, color=card.data["text_color"])
        else:
            screen.draw.text("?", center=(card.x, card.y + GRID_SIZE / 10),
                             fontsize=GRID_SIZE, color=NORMAL_COLOR)

    if state["phase"] == "won":
        screen.draw.text("SOLVED IN\n{} TRIES".format(state["tries"]),
                         center=(WIDTH / 2, HEIGHT / 2), color=NORMAL_COLOR,
                         fontsize=GRID_SIZE*0.6, owidth=0.75, ocolor="white")

pgtrun.go()
