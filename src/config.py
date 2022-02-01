import configparser as cp

class TimerConfig(cp.ConfigParser):
    def __init__(self):
        super().__init__(self)
        self.read('./config.ini')

    def write_config(self):
        with open('./config.ini', 'w') as configfile:
            self.write(configfile)
