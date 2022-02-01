import tkinter as tk
from src.constants import *

ONE_SECOND = 100

class SplashScreen(tk.Toplevel):
    def __init__(self, master=None, timer=None):
        super().__init__(master)
        self.master = master
        self.wait_visibility(self)
        self.wm_attributes('-alpha', 0.7)
        self.wm_attributes('-fullscreen', True)
        self.timer = timer
        self.time_label = tk.Label(self, text=self.timer.get_time(),
                                   font=('Roboto', 100))
        self.time_label.place(relx=0.5, rely=0.5, anchor='center')
        self.bind('<Motion>', self.close_on_any_action)
        self.bind('<Key>', self.close_on_any_action)
        self.prev_state = None
        self.cur_state = None
        self.after(ONE_SECOND, self.update)

    def close_on_any_action(self, event):
        if event.char == "+":
            self.timer.set_state(LONG_REST)
        elif event.char == "-":
            self.timer.set_state(SHORT_REST)
        else:
            self.timer.start()
            self.destroy()

    def bind_keys(self):
        pass

    def update(self):
        seconds = self.timer.get_time()
        self.cur_state = self.timer.get_state()
        if self.state_changed_to_work():
            self.timer.pause()
        self.time_label.config(text=seconds)
        self.prev_state = self.cur_state
        self.after(ONE_SECOND, self.update)

    def state_changed_to_work(self):
        return (self.cur_state != self.prev_state
                and self.cur_state == WORK)
