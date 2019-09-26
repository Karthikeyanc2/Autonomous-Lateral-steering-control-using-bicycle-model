import math
import random
import pygame
from Vec2d import Vec2d
pygame.init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
mouseX = 0
mouseY = 0
drawing = []

ratio = 10
numbers = 80

size = ratio * numbers
screen = pygame.display.set_mode([size*2, size])
pygame.display.set_caption("Path Following")
clock = pygame.time.Clock()


def show_drawing():
    for i in range(drawing.__len__()-1):
        pygame.draw.line(screen, WHITE, [drawing[i].x, drawing[i].y], [drawing[i+1].x, drawing[i+1].y])


class Vehicle:
    def __init__(self, x, y):
        self.pos = Vec2d(x, y)
        self.vel = 5
        self.acc = 0
        self.theta = 0
        self.delta = 0
        self.length = 100
        self.desired = 0
        self.te = 0

    def update(self):
        if self.delta > 1:
            self.delta = 1
        elif self.delta < -1:
            self.delta = -1
        self.vel += self.acc
        self.pos.x += self.vel * math.cos(-self.theta - self.delta)
        self.pos.y += self.vel * math.sin(-self.theta - self.delta)
        self.theta += self.vel * (math.sin(self.delta) / self.length)

    def seek(self, point):

        self.set_desired(point)
        if self.theta > math.pi:
            self.theta -= 2 * math.pi
        elif self.theta < -math.pi:
            self.theta += 2 * math.pi

        if self.desired - self.delta > 0.02:
            self.delta += 0.02

        elif self.delta - self.desired > 0.02:
            self.delta -= 0.02

        if point.distance(self.pos) <= 20:
            drawing.pop(0)

    def set_desired(self, point):

        if abs((point.sub_vect(self.pos)).angle() - self.theta) < abs((point.sub_vect(self.pos)).angle() - self.theta + 2 * math.pi):
            if abs((point.sub_vect(self.pos)).angle() - self.theta) < abs((point.sub_vect(self.pos)).angle() - self.theta - 2 * math.pi):
                self.desired = (point.sub_vect(self.pos)).angle() - self.theta
            else:
                self.desired = (point.sub_vect(self.pos)).angle() - self.theta - 2 * math.pi
        else:
            if abs((point.sub_vect(self.pos)).angle() - self.theta + 2 * math.pi) < abs((point.sub_vect(self.pos)).angle() - self.theta - 2 * math.pi):
                self.desired = (point.sub_vect(self.pos)).angle() - self.theta + 2 * math.pi
            else:
                self.desired = (point.sub_vect(self.pos)).angle() - self.theta - 2 * math.pi

    def show_vehicle(self):
        pygame.draw.polygon(screen, GREEN, rect(self.pos.x - (self.length/2) * math.cos(-self.theta),
                                                self.pos.y - (self.length/2) * math.sin(-self.theta),
                                                -self.theta, self.length, 10))
        pygame.draw.polygon(screen, RED, rect(self.pos.x - self.length * math.cos(-self.theta),
                                              self.pos.y - self.length * math.sin(-self.theta),
                                              -self.theta, 40, 17))
        pygame.draw.polygon(screen, RED, rect(self.pos.x, self.pos.y, -self.delta - self.theta, 40, 17))


def rect(x, y, angle, w, h):
    return [translate(x, y, angle, -w/2,  h/2),
            translate(x, y, angle,  w/2,  h/2),
            translate(x, y, angle,  w/2, -h/2),
            translate(x, y, angle, -w/2, -h/2)]


def translate(x, y, angle, px, py):
    x1 = x + px * math.cos(angle) - py * math.sin(angle)
    y1 = y + px * math.sin(angle) + py * math.cos(angle)
    return [x1, y1]


vehicle = Vehicle(100, size-100)

while not done:

    clock.tick(35)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if pygame.mouse.get_pressed()[0]:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        if not len(drawing):
            drawing.append(Vec2d(mouseX, mouseY))
        if not drawing[-1].x == mouseX and not drawing[-1].y == mouseY:
            drawing.append(Vec2d(mouseX, mouseY))

    show_drawing()
    if len(drawing):
        vehicle.seek(drawing[0])

    vehicle.update()
    vehicle.show_vehicle()
    pygame.display.flip()


pygame.quit()



