import os
from datetime import datetime
import subprocess

MODE = {0: 'STOP',
        1: 'WORK',
        2: 'SHORT REST',
        3: 'LONG REST',
        4: 'PAUSE'}

class TimeLogger():
    def log(self, mode):
        if isinstance(mode, int):
            mode = MODE[mode]

        now_dt = datetime.now()
        year_month = now_dt.strftime('%Y_%m')
        now = now_dt.strftime('%x %X')
        logline = f'{now},{mode}\n'
        if not os.path.exists('./logs/'):
            os.makedirs('./logs/')
        with open(f'./logs/{year_month}.log', 'a') as logfile:
            logfile.write(logline)

        subprocess.call(['notify-send', 'POMODORO', mode])
