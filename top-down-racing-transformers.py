x = 0
y = 0
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import pgzrun
from pgzero.builtins import *

import math
from random import randint
from pygame import image, Color

# controlimage1 = image.load("images/guide1.png")
controlimage2 = image.load("images/guide2.png")
cars = []
carend = False
carnames = {0: "red", 1: "blue", 2: "yellow", 3: "green"}
cartimes = {0: 0, 1: 0, 2: 0, 3: 0}
carfinished = []
timing = 0
twoseconds = 0

for c in range(4):
    cars.append(Actor('car' + str(c), center=(400, 70 + (30 * c))))
    cars[c].speed = 0


def draw():
    screen.blit("track", (0, 0))
    for c in range(4):
        cars[c].draw()
        screen.draw.text(str(round(cartimes[c]/60, 2)), (6+c*64, 6), fontsize=32, color=carnames[c], owidth=1,
                         ocolor=(0, 0, 0))
    if carend:
        screen.draw.text("The " + carnames[carfinished[0]] + " car is the winner!", center=(300, 400), owidth=1.5,
                         ocolor=(0, 0, 0), color=carnames[carfinished[0]], fontsize=48)


def update():
    global timing
    global twoseconds
    if timing < 120:
        timing += 1
        twoseconds = False
    if timing > 119:
        twoseconds = True
    global carend
    global carfinished
    if len(carfinished) > 3:
        carend = True
    if not carend:
        if keyboard.up: cars[0].speed += .15
        if keyboard.down: cars[0].speed -= .15
        if cars[0].speed != 0:
            if keyboard.left: cars[0].angle += 2
            if keyboard.right: cars[0].angle -= 2
        for c in range(4):
            if c not in carfinished:
                crash = False
                cartimes[c] += 1
                for i in range(4):
                    cardist = abs((cars[i].x-cars[c].x)**2 + (cars[i].y-cars[c].y)**2)
                    if cardist**2 < .1 and c != 0 and not twoseconds:
                        cars[c].angle += 1
                    if cars[c].collidepoint(cars[i].center) and c != i:
                        crash = True
                        cars[c].speed += (randint(0, 1))/10
                if crash:
                    newPos = calcNewXY(cars[c].center, randint(1, 20)/10, math.radians(randint(0, 360) -
                                                                                       cars[c].angle))
                else:
                    newPos = calcNewXY(cars[c].center, cars[c].speed * 2, math.radians(180 - cars[c].angle))
                ccol = controlimage2.get_at((int(newPos[0]), int(newPos[1])))
                if ccol == (255, 255, 0):
                    carfinished.append(c)
                if cars[c].speed != 0:
                    if ccol != Color("blue") and ccol != Color("red"):
                        cars[c].center = newPos
                    else:
                        if c > 0:
                            if ccol == Color("blue"):
                                cars[c].angle += 5
                            if ccol == Color("red"):
                                cars[c].angle -= 5
                        cars[c].speed = cars[c].speed / 1.1
                if c > 0 and cars[c].speed < 1.8 + (c / 10):
                    cars[c].speed += randint(0, 1) / 10
                    if crash:
                        # The car needs a negative for a left turn and a positive for right,
                        # hence -136. it needs to scale down that value so the cars dont spin
                        # like mad. The value is then multiplied by speed to adjust the turning
                        # based on the car's current speed.
                        cars[c].angle += ((ccol[1] - 136) / 136) * (2.8 * cars[c].speed)
                    else:
                        cars[c].angle -= ((ccol[1] - 136) / 136) * (2.8 * cars[c].speed)
                else:
                    cars[c].speed = cars[c].speed / 1.1


def calcNewXY(xy, speed, ang):
    x, y = xy
    newx = x - (speed * math.cos(ang))
    newy = y - (speed * math.sin(ang))
    return newx, newy


pgzrun.go()
