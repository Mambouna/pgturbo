import pgtrun
import random

WIDTH = 800
HEIGHT = 600

player = Actor("ninja")
player.pos = (WIDTH / 2, HEIGHT / 2)
player.data["score"] = 0
food_items = []
food_images = ["apple", "pumpkin", "potato", "carrot"]

music.chill.play()
music.set_volume(0.35)

def new_food():
    if len(food_items) < 5:
        food_image = random.choice(food_images)
        fresh_food = Actor(food_image)
        fresh_food.scale = 2.0
        fresh_food.x = random.randint(20, WIDTH - 20)
        fresh_food.y = random.randint(20, HEIGHT - 20)
        fresh_food.angle = random.randint(0, 359)
        food_items.append(fresh_food)

clock.schedule_interval(new_food, 2.0)

def update():
    if keyboard.left:
        player.x = player.x - 5
    if keyboard.right:
        player.x = player.x + 5
    if keyboard.up:
        player.y = player.y - 5
    if keyboard.down:
        player.y = player.y + 5

    i = 0
    while i < len(food_items):
        food = food_items[i]
        if food.collidemask(player):
            food_items.pop(i)
            player.data["score"] = player.data["score"] + 1
            if player.data["score"] % 10 == 0:
                sounds.powerup.play()
            else:
                sounds.bite.play()
        else:
            i = i + 1

def draw():
    screen.fill("darkgreen")
    player.draw()
    for food in food_items:
        food.draw()

    screen.draw.text("Score: " + str(player.data["score"]), fontsize=36,
                     center=(WIDTH / 2, HEIGHT - 40))

pgtrun.go()
