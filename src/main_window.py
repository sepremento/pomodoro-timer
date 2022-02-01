import threading
import tkinter as tk
from datetime import datetime, timedelta
from src.widgets import Digit, Semicolon
from src.options_window import OptionsWindow
from src.splash_screen import SplashScreen
from src.timer import PomodoroTimer
from src.constants import *
from playsound import playsound



class TimeWindow(tk.Frame):
    def __init__(self, master=None, config=None):
        super().__init__(master)
        self.master = master
        self.config = config
        self.timer = PomodoroTimer(self.config)
        self.create_widgets()
        self.set_timer()
        self.active = None
        self.prev_state = None
        self.cur_state = None
        self.splash_window = None

    def set_timer(self):
        cur_time = self.timer.get_time()
        self.show_time(cur_time)

    def create_widgets(self):
        startImg = tk.PhotoImage(file='./img/start.png').subsample(2, 2)
        stopImg = tk.PhotoImage(file='./img/stop.png').subsample(2, 2)
        pauseImg = tk.PhotoImage(file='./img/pause.png').subsample(2, 2)
        configImg = tk.PhotoImage(file='./img/gear.png').subsample(2, 2)
        statsImg = tk.PhotoImage(file='./img/stats.png').subsample(2, 2)
        exitImg = tk.PhotoImage(file='./img/exit.png').subsample(2, 2)

        self.configBtn = tk.Button(self.master, image=configImg, width=50,
                                   borderwidth=0,
                                   command=self.open_options)
        self.configBtn.image = configImg
        self.statsBtn = tk.Button(self.master, image=statsImg, width=50,
                                  borderwidth=0)
        self.statsBtn.image = statsImg
        self.exitBtn = tk.Button(self.master, image=exitImg, width=50,
                                 borderwidth=0,
                                 command=self.close)
        self.exitBtn.image = exitImg

        self.configBtn.grid(row=0, column=0)
        self.statsBtn.grid(row=0, column=1)
        self.exitBtn.grid(row=0, column=2)

        screen = tk.Canvas(self.master, width=160, height=60, bg='white')
        screen.grid(row=1, column=0, columnspan=3)

        self.digit_1 = Digit(screen, x=20)
        self.digit_2 = Digit(screen, x=50)
        self.semicolon = Semicolon(screen, x=80)
        self.digit_3 = Digit(screen, x=90)
        self.digit_4 = Digit(screen, x=120)

        self.startBtn = tk.Button(self.master, image=startImg, width=50,
                                  borderwidth=0,
                                  command=self.start)
        self.startBtn.image = startImg
        self.pauseBtn = tk.Button(self.master, image=pauseImg, width=50,
                                  borderwidth=0,
                                  command=self.pause)
        self.pauseBtn.image = pauseImg
        self.stopBtn = tk.Button(self.master, image=stopImg, width=50,
                                 borderwidth=0,
                                 command=self.stop)
        self.stopBtn.image = stopImg

        self.startBtn.grid(row=2, column=0)
        self.pauseBtn.grid(row=2, column=1)
        self.stopBtn.grid(row=2, column=2)

    def close(self):
        self.timer.stop()
        self.master.destroy()

    def splash(self):
        self.splash_window = SplashScreen(self, self.timer)
        self.wait_window(self.splash_window)

    def open_options(self):
        self.pause()
        options = OptionsWindow(self, self.config)
        options.grab_set()
        self.wait_window(options)

    def pause(self):
        if self.active:
            self.timer.pause()
            self.master.after_cancel(self.active)

    def start(self):
        if not self.timer.is_running():
            self.master.after(ONE_SECOND, self.update)
            self.timer.start()

    def stop(self):
        self.timer.stop()
        if self.active:
            self.master.after_cancel(self.active)
        self.timer.reset(self.config)
        self.show_time(self.timer.get_time())

    def show_time(self, seconds):
        time_str = str(timedelta(seconds=int(seconds)))

        _, mins, secs = time_str.split(':')
        d1, d2 = map(int, list(mins))
        d3, d4 = map(int, list(secs))

        self.digit_1.show(d1)
        self.digit_2.show(d2)
        self.digit_3.show(d3)
        self.digit_4.show(d4)

    def update(self):
        cur_time = self.timer.get_time()
        self.cur_state = self.timer.get_state()
        if self.state_changed_to_rest():
            self.splash()
        self.show_time(cur_time)
        self.semicolon.show()
        self.prev_state = self.cur_state
        self.active = self.master.after(ONE_SECOND, self.update)

    def state_changed_to_rest(self):
        return (self.cur_state != self.prev_state
                and self.cur_state in (SHORT_REST, LONG_REST))

