import tkinter
from math import sqrt
from random import randrange


class Pong:

    DEFAULT_PADDLE_WIDTH = 120
    DEFAULT_PADDLE_SPEED = 0  # Unused currently

    DEFAULT_BALL_RADIUS = 10
    DEFAULT_BALL_SPEED = 20

    def __init__(
        self,
        width,
        height,
        radius=None,
        speed=None,
        paddle_width=None,
        paddle_speed=None,
    ):
        self.width = width
        self.height = height

        self.score = 0

        self.paddle_x = 0
        self.paddle_height = 10
        self.paddle_width = paddle_width if paddle_width else self.DEFAULT_PADDLE_WIDTH
        self.paddle_speed = paddle_speed if paddle_speed else self.DEFAULT_PADDLE_SPEED

        self.ball_pos = (0, 0)
        self.ball_vel = (0, 0)
        self.ball_rad = radius if radius else self.DEFAULT_BALL_RADIUS
        self.ball_speed = speed if speed else self.DEFAULT_BALL_SPEED
        self.reset_ball()

    def reset_score(self):
        self.score = 0

    def reset_ball(self):
        self.ball_pos = (self.width // 2, self.height // 2)
        # Set towards random direction upwards
        vx = randrange(-self.ball_speed // 2, self.ball_speed // 2)
        vy = -abs(int(sqrt(self.ball_speed ** 2 - vx ** 2)))
        self.ball_vel = (vx, vy)

    def get_score(self):
        return self.score

    def get_ball_pos(self):
        return self.ball_pos

    def set_paddle_x(self, x):
        x -= self.paddle_width / 2
        if x < 0:
            self.paddle_x = 0
        elif x > self.width - self.paddle_width:
            self.paddle_x = self.width - self.paddle_width
        else:
            self.paddle_x = x

    def update(self):
        x, y = self.ball_pos
        vx, vy = self.ball_vel
        # Sides
        if x - self.ball_rad < 5 or x + self.ball_rad > self.width - 5:
            vx = -vx
        # Roof
        if y - self.ball_rad < 5:
            vy = -vy
        # Bottom
        elif y + self.ball_rad > self.height - self.paddle_height:
            # Paddle
            if self.paddle_x < x < self.paddle_x + self.paddle_width:
                self.score += 1
                vy = -vy
            # Lose
            else:
                self.score -= 1
                self.reset_ball()
                return
        self.ball_vel = (vx, vy)
        self.ball_pos = (x + vx, y + vy)


class GUIPong(tkinter.Tk):

    def __init__(self, parent, width, height, callback=None, *args):
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.callback = callback
        self.title("Pong")
        self.pong = Pong(width, height, *args)
        self.canvas = tkinter.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.circle = None
        self.rect = None
        self.score_label = None

    def get_ball_pos(self):
        return self.pong.get_ball_pos()

    def get_score(self):
        return self.pong.get_score()

    def set_paddle_x(self, x):
        self.pong.set_paddle_x(x)

    def show_ball(self):
        x, y = self.pong.ball_pos
        rad = self.pong.ball_rad
        x1, y1 = x - rad, y - rad
        x2, y2 = x + rad, y + rad
        self.circle = self.canvas.create_oval(x1, y1, x2, y2, fill="red")

    def show_paddle(self):
        self.rect = self.canvas.create_rectangle(
            self.pong.paddle_x,
            self.height - self.pong.paddle_height,
            self.pong.paddle_x + self.pong.paddle_width,
            self.height,
            fill="blue",
        )

    def show(self):
        self.show_paddle()
        self.show_ball()
        self.score_label = self.canvas.create_text(
            5, 5, text=0, anchor="nw", font=("", 25)
        )
        self.after(100, self.execute)
        self.mainloop()

    def reset(self):
        x1, y1 = self.x - rad, self.y - rad
        x2, y2 = self.x + rad, self.y + rad
        self.canvas.coords(self.circle, x1, y1, x2, y2)

    def update_paddle(self):
        self.canvas.coords(
            self.rect,
            self.pong.paddle_x,
            self.height - 10,
            self.pong.paddle_x + self.pong.paddle_width,
            self.height,
        )

    def update_ball(self):
        x, y = self.pong.ball_pos
        rad = self.pong.ball_rad
        x1, y1 = x - rad, y - rad
        x2, y2 = x + rad, y + rad
        self.canvas.coords(self.circle, x1, y1, x2, y2)

    def execute(self):
        self.pong.update()
        self.update_paddle()
        self.update_ball()
        self.canvas.itemconfig(self.score_label, text=self.pong.get_score())
        self.after(30, self.execute)
        if self.callback:
            self.callback(self)


if __name__ == "__main__":
    game = GUIPong(None, 600, 600)
    game.show()
