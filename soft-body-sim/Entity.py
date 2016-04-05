from random import randint


class Entity:

    def __init__(self, parent):

        self.root = parent
        self.canvas = parent.canvas

        self.nodes = []
        self.springs = []

        self.color = "#%02x%02x%02x" % (randint(30, 255), randint(30, 255), randint(30, 255))

        self.init_lists()

        self.show()

    def init_lists(self):
        pass

    def show(self):
        for i in self.nodes:
            i.show()
        for i in self.springs:
            i.show()

    def remove(self):
        self.springs = []
        self.nodes = []

    def move(self):
        for i in self.springs:
            i.move()
        for i in self.nodes:
            i.move()
