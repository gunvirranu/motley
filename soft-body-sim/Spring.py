from math import hypot, atan2, degrees
from Node import Node


class Spring:

    def __init__(self, parent, node1, node2, spring_constant):

        self.parent = parent
        self.canvas = parent.canvas

        self.node1 = node1
        self.node2 = node2

        self.line = None

        self.SPRING_CONSTANT = spring_constant

        self.ENERGY_LOSS = 0.95

        dx = self.node1.posX - self.node2.posX
        dy = self.node1.posY - self.node2.posY
        self.relaxed_dist = hypot(dx, dy)

    def show(self):
        self.line = self.canvas.create_line(self.node1.posX, self.node1.posY, self.node2.posX, self.node2.posY,
                                            fill=self.parent.color)

    def move(self):

        dx = self.node1.posX - self.node2.posX
        dy = self.node1.posY - self.node2.posY
        dist = hypot(dx, dy) - self.relaxed_dist

        force = self.SPRING_CONSTANT * dist / 10

        angle = 180 - round(degrees(atan2(dy, dx)))

        self.node1.velocity, self.node1.angle = Node.add_vectors((self.node1.velocity, self.node1.angle),
                                                                 (force/self.node1.mass, angle))

        self.node2.velocity, self.node2.angle = Node.add_vectors((self.node2.velocity, self.node2.angle),
                                                                 (force/self.node2.mass, angle+180))

        self.node1.velocity *= self.ENERGY_LOSS
        self.node2.velocity *= self.ENERGY_LOSS

        self.canvas.coords(self.line, self.node1.posX, self.node1.posY, self.node2.posX, self.node2.posY)
