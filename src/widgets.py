import tkinter as tk
from src.constants import OFFSETS, DIGITS


class Digit:
    '''
    Класс цифры, который отрисовывает на канве семь сегментов. Класс также
    содержит метод `show`, который управляет видимостью цифры на канве.
    '''
    def __init__(self, canvas, x=10, y=10, length=20, width=5):
        self.canvas = canvas
        self.segs = []

        for x0, y0, x1, y1 in OFFSETS:
            self.segs.append(canvas.create_line(
                x + x0 * length,
                y + y0 * length,
                x + x1 * length,
                y + y1 * length,
                width=width,
                fill='#CCC'))

    def show(self, num):
        for iid, on in zip(self.segs, DIGITS[num]):
            self.canvas.itemconfigure(
                iid, fill='#111' if on else '#CCC'
            )

class Semicolon:
    def __init__(self, canvas, x=10, y=20, width=5):
        self.canvas = canvas
        self.visible = True
        self.dots = []

        self.dots.append(canvas.create_line(
            x, y, x, y+5, fill='#111', width=width))

        self.dots.append(canvas.create_line(
            x, y+10, x, y+15, fill='#111', width=width))

    def show(self):
        if self.visible:
            for dot in self.dots:
                self.canvas.itemconfigure(dot, state='normal')
            self.visible = False
        else:
            for dot in self.dots:
                self.canvas.itemconfigure(dot, state='hidden')
            self.visible = True


class ToolTip:
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         font=('Arial', 10), wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
