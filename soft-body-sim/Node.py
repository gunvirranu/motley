from math import radians, cos, sin, hypot, degrees, atan2


class Node:

    GRAVITY = 0.8
    GRAVITY_ANGLE = -90

    def __init__(self, parent, pos, radius, can_move):

        self.parent = parent
        self.canvas = parent.canvas

        self.posX = pos[0]
        self.posY = pos[1]
        self.radius = radius

        self.velocity = 0
        self.angle = 0
        self.mass = 1

        self.elasticity = 0.745
        self.can_move = can_move
        self.temp_move = False

        self.ball = None

    def show(self):
        x1 = self.posX - self.radius
        y1 = self.posY - self.radius
        x2 = self.posX + self.radius
        y2 = self.posY + self.radius
        self.ball = self.canvas.create_oval(x1, y1, x2, y2, outline='black')

    def move_to(self, x, y):
        self.canvas.coords(self.ball, x-self.radius, y-self.radius, x+self.radius, y+self.radius)
        self.posX = x
        self.posY = y

    def collide(self, other):

        dx = self.posX - other.posX
        dy = self.posY - other.posY

        dist = hypot(dx, dy)
        if dist < self.radius + other.radius:
            angle = round(degrees(atan2(dy, dx)))
            total_mass = self.mass + other.mass

            self.velocity, self.angle = Node.add_vectors((self.velocity * (self.mass - other.mass) / total_mass,
                                                          self.angle), (2 * other.velocity * other.mass / total_mass,
                                                                        angle))

            other.velocity, other.angle = Node.add_vectors((other.velocity*(other.mass-self.mass)/total_mass,
                                                            other.angle), (2 * self.velocity * self.mass / total_mass,
                                                                           angle + 180))

            elasticity = self.elasticity * other.elasticity
            self.velocity *= elasticity
            other.velocity *= elasticity

            overlap = 0.5 * (self.radius + other.radius - dist+1)
            self.posX = sin(radians(angle)) * overlap
            self.posY = cos(radians(angle)) * overlap
            other.posX = sin(radians(angle)) * overlap
            other.posY = cos(radians(angle)) * overlap

    def move(self):

        if not self.can_move or self.temp_move:
            temp = self.canvas.coords(self.ball)
            self.posX = temp[0] + self.radius
            self.posY = temp[1] + self.radius
            return

        self.velocity, self.angle = self.add_vectors((self.velocity, self.angle), (self.GRAVITY, self.GRAVITY_ANGLE))

        x_velocity = self.velocity * cos(radians(self.angle))
        y_velocity = -self.velocity * sin(radians(self.angle))

        temp = self.canvas.coords(self.ball)
        pos_x = temp[0] + self.radius + x_velocity
        pos_y = temp[1] + self.radius + y_velocity

        if pos_x < self.radius or pos_x > self.canvas.winfo_width()-self.radius:
            self.angle = 180 - self.angle
            self.velocity *= self.elasticity
            return
        if pos_y > self.canvas.winfo_height()-self.radius-10:
            self.angle = 360 - self.angle
            self.velocity *= self.elasticity
            return

        self.posX = pos_x - x_velocity
        self.posY = pos_y - y_velocity

        # color_rgb = tuple([int(x*255) for x in hls_to_rgb(self.posY/360, 0.5, 1)])
        # color_rgb = "#%02x%02x%02x" % color_rgb
        #
        # self.canvas.itemconfig(self.ball, fill=color_rgb)

        self.canvas.move(self.ball, x_velocity, y_velocity)

    @staticmethod
    def add_vectors(vector1, vector2):
        temp1 = radians(vector1[1])
        temp2 = radians(vector2[1])
        x = vector1[0] * round(cos(temp1), 4) + \
            vector2[0] * round(cos(temp2), 4)
        y = vector1[0] * round(sin(temp1), 4) + \
            vector2[0] * round(sin(temp2), 4)
        magnitude = hypot(x, y)
        angle = round(degrees(atan2(y, x)))
        if angle < 0:
            angle += 360
        return magnitude, angle
