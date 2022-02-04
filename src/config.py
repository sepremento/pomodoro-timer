from pathlib import Path
import configparser as cp

class TimerConfig(cp.ConfigParser):
    path = Path(__file__).absolute().parent.parent
    def __init__(self):
        super().__init__(self)
        self.read(self.path / 'config.ini')

    def write_config(self):
        with open(self.path / 'config.ini', 'w') as configfile:
            self.write(configfile)
