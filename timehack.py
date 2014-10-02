#!/usr/bin/python

__author__ = 'sitin'

from datetime import datetime, time, date, timedelta
from random import randint
from argparse import ArgumentParser
import dateutil.parser


class TimeHack:
    def __init__(self, start_min, start_max, presence_duration, presence_deviation=time(),
                 absence_duration=time(), absence_deviation=time(), count=1):
        self.iterations_left = count

        self.start_min = self.time_to_timedelta(start_min).total_seconds()
        self.start_max = self.time_to_timedelta(start_max).total_seconds()

        self.presence_duration = self.time_to_timedelta(presence_duration).total_seconds()
        self.presence_deviation = self.time_to_timedelta(presence_deviation).total_seconds()
        self.absence_duration = self.time_to_timedelta(absence_duration).total_seconds()
        self.absence_deviation = self.time_to_timedelta(absence_deviation).total_seconds()

        self.start_delta = self.start_max - self.start_min

    @staticmethod
    def time_to_timedelta(val):
        return timedelta(hours=val.hour, minutes=val.minute, seconds=val.second)

    @staticmethod
    def timedelta_to_time(val):
        return (datetime.combine(date.today(), time()) + val).time()

    def __iter__(self):
        return self

    def _get_presence(self):
        presence = self.presence_duration + randint(-self.presence_deviation, self.presence_deviation)
        absence = self.absence_duration + randint(-self.absence_deviation, self.absence_deviation)

        start = self.start_min + randint(0, self.start_delta)
        end = start + presence + absence

        return {
            "start": timedelta(seconds=start),
            "end": timedelta(seconds=end),
            "presence": timedelta(seconds=presence)
        }

    def next(self):
        if self.iterations_left <= 0:
            raise StopIteration
        else:
            self.iterations_left -= 1
            return self._get_presence()


def get_arguments():
    parser = ArgumentParser(description='Calculates employee fake presence.')
    parser.add_argument('start_min', type=str, help='minimum job start time')
    parser.add_argument('start_max', type=str, help='minimum job start time')
    parser.add_argument('presence', type=str, help='average presence at office')
    parser.add_argument('--presence_deviation', type=str, help='deviation of presence')
    parser.add_argument('--absence', type=str, help='average absence during working day (e.g lunch)')
    parser.add_argument('--absence_deviation', type=str, help='deviation of absence')
    parser.add_argument('--results', type=int, help='number of results')

    args = parser.parse_args()

    for key in args.__dict__:
        value = getattr(args, key)
        if isinstance(value, str):
            setattr(args, key, dateutil.parser.parse(value))

    return args


def print_fake_data(arguments):
    for period in TimeHack(arguments.start_min, arguments.start_max, arguments.presence, arguments.presence_deviation,
                           arguments.absence, arguments.absence_deviation, arguments.results):
        print "%s\t%s\t%s" % (period["start"], period["end"], period["presence"])


print_fake_data(get_arguments())