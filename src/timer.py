from datetime import datetime
from itertools import cycle
from time import sleep
from threading import Thread
from playsound import playsound
import configparser as cp
from src.constants import *
from src.logger import TimeLogger


START_SOUND = './sound/start.wav'
STOP_SOUND  = './sound/stop.wav'

class PomodoroTimer():
    def __init__(self, config):
        self._logger = TimeLogger()
        self._logger.log('NEW SESSION')
        self.reset(config)

    def start(self):
        self._running = True
        if self._no_thread_running():
            self._logger.log('WORK')
            self._play_sound_and_start_timer()

    def stop(self):
        if self._timer_thread is not None:
            self._running = False
            self._timer_thread = None
            self._logger.log('IDLE')
        self.set_state(IDLE)
        self._set_state_sequence()
        self._cur_time = self._timer_mapping[WORK]

    def pause(self):
        if self._timer_thread is not None:
            self._running = False
            self._logger.log('PAUSE')

    def next(self):
        next_state = next(self._sequence_iterator)
        self._play_sound_depending_on_state(next_state)
        self._cur_time = self._timer_mapping[next_state]
        self.set_state(next_state)
        self._logger.log(next_state)

    def enlarge_short_rest(self):
        if self.get_state() == SHORT_REST:
            self.set_state(LONG_REST)
            self._set_state_sequence()

    def shorten_long_rest(self):
        if self.get_state() == LONG_REST:
            self.set_state(SHORT_REST)
            self._set_state_sequence()

    def is_running(self):
        return self._running

    def get_time(self):
        return self._cur_time

    def get_state(self):
        try:
            return self._state
        except AttributeError:
            return IDLE

    def set_state(self, state):
        self._state = state
        if state not in [IDLE, PAUSE]:
            self._cur_time = self._timer_mapping[state]

    def reset(self, config):
        self._running = False
        self._timer_thread = None
        self._set_timers_from_config(config)
        self._set_state_sequence()
        self._state = next(self._sequence_iterator)
        self._cur_time = self._timer_mapping[WORK]

    def _no_thread_running(self):
        return (self._timer_thread is None
                or not self._timer_thread.is_alive())

    def _parse_str_to_time(self, time_str):
        dt = datetime.strptime(time_str, '%M:%S')
        return dt.minute * 60 + dt.second

    def _play_sound_and_start_timer(self):
        self._timer_thread = Thread(target=self._update)
        self._timer_thread.start()
        self._sound_thread = Thread(target=playsound, args=[START_SOUND])
        self._sound_thread.start()

    def _play_sound_depending_on_state(self, state):
        if state == WORK:
            self._sound_thread = Thread(target=playsound, args=[START_SOUND])
        else:
            self._sound_thread = Thread(target=playsound, args=[STOP_SOUND])
        self._sound_thread.start()

    def _set_state_sequence(self):
        state = self.get_state()
        if state == SHORT_REST:
            state_sequence = ([WORK, LONG_REST] + [WORK, SHORT_REST] *
                              (self._num_cycles - 1))
        else:
            state_sequence = ([WORK, SHORT_REST] * (self._num_cycles - 1) +
                              [WORK, LONG_REST])
        self._state_sequence = state_sequence
        self._sequence_iterator = cycle(self._state_sequence)

    def _set_timers_from_config(self, config):
        timers = config['timer']
        self._timer_mapping = {
            WORK: timers['work_time'],
            SHORT_REST: timers['short_rest_time'],
            LONG_REST: timers['long_rest_time'] }
        self._timer_mapping = {k: self._parse_str_to_time(v)
                               for k, v in self._timer_mapping.items()}
        self._num_cycles = int(timers['num_cycles'])

    def _update(self):
        while self._running:
            if self._cur_time == 0:
                self.next()
            else:
                self._cur_time -= 1
            sleep(ONE_SECOND / 1000)

