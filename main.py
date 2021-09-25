import tkinter as tk
# from src.widgets import Digit, Semicolon
from src.main_window import TimeWindow


n = 0

def update():
    global n
    tw.digit_4.show(n)
    tw.semicolon.show()
    n = (n+1) % 10
    root.after(400, update)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('150x90')
    tw = TimeWindow(root)

    tw.digit_1.show(1)
    tw.digit_2.show(2)
    tw.digit_3.show(3)

    root.after(400, update)
    root.mainloop()
