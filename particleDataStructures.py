# Some suitable functions and data structures for drawing a map and particles

import time
import random
import math
from mcl_algo import *

# A Canvas class for drawing a map and particles:
#     - it takes care of a proper scaling and coordinate transformation between
#      the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self,map_size=210):
        self.map_size    = map_size;    # in cm;
        self.canvas_size = 768;         # in pixels;
        self.margin      = 0.05*map_size;
        self.scale       = self.canvas_size/(map_size+2*self.margin);

    def drawLine(self,line):
        x1 = self.__screenX(line[0]);
        y1 = self.__screenY(line[1]);
        x2 = self.__screenX(line[2]);
        y2 = self.__screenY(line[3]);
        print "drawLine:" + str((x1,y1,x2,y2))

    def drawParticles(self,data):
        display = [(self.__screenX(d[0]),self.__screenY(d[1])) + d[2:] for d in data];
        print "drawParticles:" + str(display);

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls
class Map:
    def __init__(self):
        self.walls = [];

    def add_wall(self,wall):
        self.walls.append(wall)

    def clear(self):
        self.walls = []

    def draw(self):
        for wall in self.walls:
            canvas.drawLine(wall)

# Simple Particles set
class Particles:
    def __init__(self):
        self.n = 100
        self.loc = (84, 30, 0)
        self.data = [(84, 30, 0)] * self.n

    def draw(self):
        #scaled = [(x * 10, y * 10, theta, w) for (x, y, theta, w) in self.data]
        canvas.drawParticles(self.data)

canvas = Canvas();    # global canvas we are going to draw on

mymap = Map()
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
mymap.add_wall((0,0,0,168));        # a
mymap.add_wall((0,168,84,168));     # b
mymap.add_wall((84,126,84,210));    # c
mymap.add_wall((84,210,168,210));   # d
mymap.add_wall((168,210,168,84));   # e
mymap.add_wall((168,84,210,84));    # f
mymap.add_wall((210,84,210,0));     # g
mymap.add_wall((210,0,0,0));        # h
mymap.draw()

from initial import *

points = [(180,30),(180,54),(138,54),(138,168),(114,168),(114,84),(84,84),(84,30)]
initial = (84, 30)

interface = Init()
interface.global_x = initial[0]
interface.global_y = initial[1]
interface.global_theta = 0

interval = 20
particles = Particles()

for i in range(len(points)):
    next_dst = points[i]
    ori = (interface.global_x, interface.global_y, interface.global_theta)
    print "to the next point" + str(next_dst) + " from " + str(ori)
    while True:
        interface.turnToPoint(next_dst[0], next_dst[1])
        ori = (ori[0], ori[1], interface.global_theta)
        print "CURRENT POSITION: " + str(ori)
        next_mov = nextMove(ori, next_dst, interval)
        print "Moving to " + str(next_mov)
        interface.navigateToWaypoint(next_mov[0], next_mov[1])
        sonar_reading = interface.ultrasonic_average_reading()
        print "Sonar reading: " + str(sonar_reading)
        resampled_particles = resample(sample(ori, next_mov, sonar_reading))
        particles.data = resampled_particles
        particles.draw()
        current_pos = averageOf(resampled_particles)
        interface.global_x, interface.global_y, interface.global_theta, _ = current_pos
        ori = (interface.global_x, interface.global_y, interface.global_theta)
        if next_mov == next_dst:
            break
