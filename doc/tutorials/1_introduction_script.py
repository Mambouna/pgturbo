import pgtrun

WIDTH = 800
HEIGHT = 600

player = Actor.Ellipse(40, 60, "lightblue")
player.pos = (WIDTH / 2, HEIGHT / 2)

def update():
    if keyboard.left:
        player.x = player.x - 5
    if keyboard.right:
        player.x = player.x + 5
    if keyboard.up:
        player.y = player.y - 5
    if keyboard.down:
        player.y = player.y + 5

def draw():
    screen.fill("darkgreen")
    player.draw()

pgtrun.go()
