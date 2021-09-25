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
