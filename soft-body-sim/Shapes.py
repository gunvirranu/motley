from math import cos, sin, radians
from Entity import Entity
from Node import Node
from Spring import Spring

SPRING_CONSTANT = 0.35
radius = 10


class Pendulum(Entity):

    def init_lists(self):

        self.nodes.append(Node(self, (700, 300), radius, False))
        self.nodes.append(Node(self, (800, 400), radius, True))
        self.nodes.append(Node(self, (900, 500), radius, True))

        self.springs.append(Spring(self, self.nodes[0], self.nodes[1], SPRING_CONSTANT))
        self.springs.append(Spring(self, self.nodes[1], self.nodes[2], SPRING_CONSTANT))


class Triangle(Entity):

    def init_lists(self):

        points = calc_points(200, 300, 3, 100)

        for i in points:
            self.nodes.append(Node(self, i, radius, True))

        for i in self.nodes:
            for n in self.nodes:
                if i != n:
                    self.springs.append(Spring(self, i, n, SPRING_CONSTANT))


class Square(Entity):

    def init_lists(self):

        points = calc_points(700, 450, 4, 100)

        for i in points:
            self.nodes.append(Node(self, i, radius, True))

        for i in self.nodes:
            for n in self.nodes:
                if i != n:
                    self.springs.append(Spring(self, i, n, SPRING_CONSTANT))


class Pentagon(Entity):

    def init_lists(self):

        points = calc_points(700, 450, 5, 100)

        for i in points:
            self.nodes.append(Node(self, i, radius, True))

        for i in self.nodes:
            for n in self.nodes:
                if i != n:
                    self.springs.append(Spring(self, i, n, SPRING_CONSTANT))


class Hexagon(Entity):

    def init_lists(self):

        points = calc_points(700, 450, 6, 100)

        for i in points:
            self.nodes.append(Node(self, i, radius, True))

        for i in self.nodes:
            for n in self.nodes:
                if i != n:
                    self.springs.append(Spring(self, i, n, SPRING_CONSTANT))


class Decagon(Entity):

    def init_lists(self):

        points = calc_points(700, 450, 10, 100)

        for i in points:
            self.nodes.append(Node(self, i, radius, True))

        for i in self.nodes:
            for n in self.nodes:
                if i != n:
                    self.springs.append(Spring(self, i, n, SPRING_CONSTANT))


class CoolDecagon(Entity):

    def init_lists(self):

        points = calc_points(700, 450, 10, 100)

        for i in points:
            self.nodes.append(Node(self, i, radius, True))

        for i in range(len(self.nodes)):
            if i == len(self.nodes) - 1:
                self.springs.append(Spring(self, self.nodes[i], self.nodes[0], SPRING_CONSTANT))
            else:
                self.springs.append(Spring(self, self.nodes[i], self.nodes[i+1], SPRING_CONSTANT))

        for i in range(0, len(self.nodes), 2):
            if i == len(self.nodes) - 2:
                self.springs.append(Spring(self, self.nodes[i], self.nodes[0], SPRING_CONSTANT))
            else:
                self.springs.append(Spring(self, self.nodes[i], self.nodes[i+2], SPRING_CONSTANT))

        for i in range(1, len(self.nodes), 2):
            if i == len(self.nodes) - 1:
                self.springs.append(Spring(self, self.nodes[i], self.nodes[1], SPRING_CONSTANT))
            else:
                self.springs.append(Spring(self, self.nodes[i], self.nodes[i+2], SPRING_CONSTANT))


class Circle(Entity):

    def init_lists(self):

        points = calc_points(700, 450, 26, 100)

        for i in points:
            self.nodes.append(Node(self, i, radius, True))\

        for i in self.nodes:
            for n in self.nodes:
                if i != n:
                    self.springs.append(Spring(self, i, n, SPRING_CONSTANT))


def rotate_point(centre_x, centre_y, x, y, angle):

    new_x = (cos(radians(angle)) * (x-centre_x)) - (sin(radians(angle)) * (y-centre_y)) + centre_x

    new_y = (sin(radians(angle)) * (x-centre_x)) + (cos(radians(angle)) * (y-centre_y)) + centre_y

    return round(new_x), round(new_y)


def calc_points(centre_x, centre_y, sides, shape_radius):
    points = []
    x = centre_x + shape_radius
    y = centre_y
    for i in range(sides):
        x, y = rotate_point(centre_x, centre_y, x, y, 360/sides)
        points.append((x, y))
    return points
