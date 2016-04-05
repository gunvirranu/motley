import tkinter
import Shapes


class SoftBodySimulator(tkinter.Tk):

    def __init__(self, parent, width, height, title):

        tkinter.Tk.__init__(self, parent)

        self.title(title)

        self.parent = parent

        self.width = width
        self.height = height

        self.canvas = None
        self.is_paused_label = None
        self.floor = None

        self.entities = []
        self.to_destroy = []

        self.is_paused = False
        self.colours = ['red', 'green', 'magenta', 'blue']
        self.moving = None

        self.initialize()

    def initialize(self):

        self.canvas = tkinter.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.init_canvas()

        self.bind('<Button-1>', self.on_left_click)
        self.bind('<B1-Motion>', self.on_left_motion)
        self.bind('<ButtonRelease-1>', self.on_left_release)

        self.bind('p', self.toggle_pause)
        # self.bind('c', self.clear)

    def init_canvas(self):

        self.is_paused_label = self.canvas.create_text(10, 5, text='PAUSED', font=('', 20),
                                                       fill='red', anchor='nw', state='hidden')

        self.floor = self.canvas.create_rectangle(0, self.height-5, self.width,
                                                  self.width, fill='black')

    def clear(self, event):
        for i in self.entities:
            i.remove()
        self.canvas.delete('all')
        self.init_canvas()

    def toggle_pause(self, event):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.canvas.itemconfig(self.is_paused_label, state='normal')
        else:
            self.canvas.itemconfig(self.is_paused_label, state='hidden')

    def on_left_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        closest = self.canvas.find_closest(x, y)
        if closest and self.canvas.type(closest) == 'oval':
            for e in self.entities:
                for i in e.nodes:
                    if closest[0] == i.ball:
                        if (x - i.posX)**2 + (y - i.posY)**2 < i.radius**2:
                            self.moving = i
                            i.temp_move = True
                            return

    def on_left_motion(self, event):
        if self.moving:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            self.moving.move_to(x, y)

    def on_left_release(self, event):
        if self.moving:
            self.moving.temp_move = False
            self.moving = None

    def show(self):
        self.after(100, self.execute)
        self.mainloop()

    def execute(self):

        if not self.is_paused:

            for entity in self.entities:
                entity.move()

            for i in set(self.to_destroy):
                self.entities.remove(i)
            self.to_destroy = []

        self.after(25, self.execute)


if __name__ == '__main__':

    gui = SoftBodySimulator(None, 1400, 900, "Gunvir's Soft Body Simulator!")

    gui.entities.append(Shapes.Pendulum(gui))
    gui.entities.append(Shapes.Triangle(gui))
    gui.entities.append(Shapes.Square(gui))
    gui.entities.append(Shapes.Pentagon(gui))
    # gui.entities.append(Shapes.Hexagon(gui))
    # gui.entities.append(Shapes.Decagon(gui))
    # gui.entities.append(Shapes.CoolDecagon(gui))
    # gui.entities.append(Shapes.Circle(gui))

    gui.show()
