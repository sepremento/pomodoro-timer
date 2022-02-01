#!/usr/bin/python3
import tkinter as tk
from src.main_window import TimeWindow
from src.config import TimerConfig


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('163x120')
    root.resizable(False, False)

    tconf = TimerConfig()
    tw = TimeWindow(root, tconf)

    root.mainloop()
