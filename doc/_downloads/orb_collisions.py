WIDTH = 600
HEIGHT = 400

player = Actor.Triangle(80, 40, "yellow", (WIDTH / 2, HEIGHT / 2),
                        angle=90)
player.angle = 90

orbs = []
for i in range(8):    
    orb = Actor.Ellipse(30, 30, "blue", (100 + 40 * i, 100))
    orbs.append(orb)

def update():
    if mouse.pressed_left:
        player.move_towards_point(mouse.pos, 8)

    i = 0
    while i < len(orbs):
        orb = orbs[i]
        if orb.colliderect(player):
            orbs.pop(i)
        else:
            i = i + 1

def draw():
    screen.clear()
    player.draw()
    for orb in orbs:
        orb.draw()
