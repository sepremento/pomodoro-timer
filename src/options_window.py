import tkinter as tk
from re import match
from time import strptime
from tkinter import messagebox


class OptionsWindow(tk.Toplevel):
    def __init__(self, master=None, config=None):
        super().__init__(master)
        self.master = master
        self.config = config
        self.resizable(False, False)
        self.create_widgets(self.config)

    def create_widgets(self, config=None):
        self.work_time = tk.StringVar(self, self.config['timer']['work_time'])
        self.rest_time = tk.StringVar(self, self.config['timer']['short_rest_time'])
        self.chill_time = tk.StringVar(self, self.config['timer']['long_rest_time'])
        self.num_cycle = tk.StringVar(self, self.config['timer']['num_cycles'])

        val_func = self.register(self.validate_input_time)

        self.workLabel = tk.Label(self, text='Рабочее время').grid(row=0, column=0)
        self.restLabel = tk.Label(self, text='Короткий перерыв').grid(row=1, column=0)
        self.chillLabel = tk.Label(self, text='Длинный перерыв').grid(row=2, column=0)
        self.cycleLabel = tk.Label(self, text='Количество рабочих циклов').grid(row=3, column=0)

        self.workEntry = tk.Entry(self)
        self.workEntry.config(validate="focusout",
                              textvariable=self.work_time,
                              validatecommand=(val_func, 'workEntry %P'))
        self.workEntry.grid(row=0, column=1)

        self.restEntry = tk.Entry(self)
        self.restEntry.config(validate="focusout",
                              textvariable=self.rest_time,
                              validatecommand=(val_func, 'restEntry %P'))
        self.restEntry.grid(row=1, column=1)

        self.chillEntry = tk.Entry(self)
        self.chillEntry.config(validate="focusout",
                               textvariable=self.chill_time,
                               validatecommand=(val_func, 'chillEntry %P'))
        self.chillEntry.grid(row=2, column=1)

        self.cycleEntry = tk.Entry(self)
        self.cycleEntry.config(validate="focusout",
                               textvariable=self.num_cycle,
                               validatecommand=(val_func, 'cycleEntry %P'))
        self.cycleEntry.grid(row=3, column=1)

        self.okBtn = tk.Button(self, text='Ok',
                               command=self.save_config_and_close).grid(row=4, column=1)

    def save_config_and_close(self):
        self.config['timer']['work_time'] = self.work_time.get()
        self.config['timer']['rest_time'] = self.rest_time.get()
        self.config['timer']['chill_time'] = self.chill_time.get()
        self.config['timer']['num_cycle'] = self.num_cycle.get()
        self.config.write_config()
        self.master.config = self.config
        self.master.set_timer()
        self.destroy()

    def validate_input_time(self, entry):
        name, entry = entry.split(' ')
        formats = ['%M:%S']
        check_passed = any([self.check_format(entry, f) for f in formats])
        if name == 'cycleEntry':
            check_passed = match(r'^\d$', entry)

        if check_passed:
            return True

        if name == 'workEntry':
            self.workEntry.delete(0, tk.END)
            self.workEntry.insert(0, '25:00')

        if name == 'restEntry':
            self.restEntry.delete(0, tk.END)
            self.restEntry.insert(0, '5:00')

        if name == 'chillEntry':
            self.chillEntry.delete(0, tk.END)
            self.chillEntry.insert(0, '15:00')

        if name == 'cycleEntry':
            self.cycleEntry.delete(0, tk.END)
            self.cycleEntry.insert(0, '4')

        error_msg = ('Поля принимают текстовые значения в формате "%M:%S". '
                     'Циклы обозначаются одной цифрой.')
        tk.messagebox.showerror('Неверный формат данных', error_msg)

        return False

    def check_format(self, entry, time_format):
        try:
            strptime(entry, time_format)
            return True
        except ValueError:
            return False




