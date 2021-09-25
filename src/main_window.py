import tkinter as tk
from src.widgets import Digit, Semicolon

class TimeWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        screen = tk.Canvas(self.master, width=150, height=60, bg='white')
        screen.pack()

        self.digit_1 = Digit(screen)
        self.digit_2 = Digit(screen, x=40)
        self.semicolon = Semicolon(screen, x=70)
        self.digit_3 = Digit(screen, x=80)
        self.digit_4 = Digit(screen, x=110)

        self.startBtn = tk.Button(
            self.master, text='Старт', width=3)
        self.pauseBtn = tk.Button(
            self.master, text='Пауза', width=3)
        self.stopBtn = tk.Button(
            self.master, text='Стоп', width=3)
        self.startBtn.pack(side=tk.LEFT)
        self.pauseBtn.pack(side=tk.LEFT)
        self.stopBtn.pack(side=tk.LEFT)
