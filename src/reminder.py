from builtins import dict

import thirdparty
from datetime import datetime
from datetime import timedelta
from notification import Notification
from thirdparty import Parent
from parse_datetime import parse_datetime


class Reminder:
    def __init__(self, start_remind_before, start_remind_from, stop_in_moment,
                 remind_in, datetimes, interval, weekdays, parent, kind, *flags):
        if not start_remind_before is None:
            self.start_remind_from = stop_in_moment - start_remind_before
        else:
            self.start_remind_from = datetime.min if start_remind_from is None else start_remind_from
        self.stop_in_moment = stop_in_moment if not stop_in_moment is None else datetime.max
        self.remind_in = remind_in
        self.datetimes = datetimes
        self.interval = interval
        self.weekdays = weekdays
        self.parent = parent
        self.kind = kind
        if len(flags) > 0:
            self.flags = flags[0]
        else:
            self.flags = {
                    'datetimes': 0,
                    'interval': 0,
                    'weekdays': self.start_remind_from.date() - timedelta(days=1)
                }

    @staticmethod
    def create_from_dict(dictionary):
        start_remind_from = parse_datetime(dictionary['start_remind_from'].split(), thirdparty.Formats.ordinary) \
            if not dictionary['start_remind_from'] is None else None
        datetimes = [parse_datetime(s.split(), thirdparty.Formats.ordinary) for s in dictionary['datetimes']] \
            if not dictionary['datetimes'] is None else None
        stop_in_moment = parse_datetime(dictionary['stop_in_moment'].split(), thirdparty.Formats.ordinary) \
            if not dictionary['stop_in_moment'] is None else None
        parent = Parent(dictionary['parent']['title'], dictionary['parent']['deadline'])
        dictionary['flags']['weekdays'] = parse_datetime(dictionary['flags']['weekdays'], thirdparty.Formats.date)
        reminder = Reminder(
            None,
            start_remind_from,
            stop_in_moment,
            parse_datetime(dictionary['remind_in'], thirdparty.Formats.delta),
            datetimes,
            parse_datetime(dictionary['interval'], thirdparty.Formats.delta),
            dictionary['weekdays'],
            parent,
            dictionary['kind'],
            dictionary['flags']
        )
        return reminder

    def check(self):
        now = datetime(2018, 5, 10, 15)
        if self.kind == thirdparty.Classes.task:
            if now > self.stop_in_moment:
                mes = 'You missed the deadline for the task {t}'.format(t=self.parent.title)
                date = self.parent.deadline
                return Notification(mes, date)
            if self.start_remind_from < now and now < self.stop_in_moment:
                notify_remind_in = self.check_remind_in(now)
                notify_datetimes = self.check_datetimes(now)
                notify_interval = self.check_interval(now)
                notify_weekdays = self.check_weekdays(now)

                notify_list = [notify for notify in [notify_remind_in, notify_datetimes,
                                                     notify_interval, notify_weekdays] if notify is not None]
                                    #sort(key=lambda obj: datetime.min if obj is None else obj.date, reverse=True)
                return notify_list

    def check_remind_in(self, now):
        if self.remind_in is None:
            return None
        if self.stop_in_moment - self.remind_in < now:
            mes = 'Remind! In {time} the deadline for the task {t} : remind_in'.format(time=self.remind_in, t=self.parent.title)
            date = self.stop_in_moment - self.remind_in
            return Notification(mes, date)

    def check_datetimes(self, now):
        if self.datetimes is None:
            return None
        counter = 0
        for dt in self.datetimes:
            if dt < now:
                counter += 1
        if counter > self.flags['datetimes']:
            mes = 'Remind! {d} the deadline for the task {t} : datetimes'.format(d=self.parent.deadline, t=self.parent.title)
            date = self.datetimes[counter - 1]
            self.flags['datetime'] = counter
            return Notification(mes, date)

    def check_interval(self, now):
        if self.interval is None:
            return None
        counter = (now - self.start_remind_from) // self.interval
        if counter > self.flags['interval']:
            mes = 'Remind! {d} the deadline for the task {t} : interval'.format(d=self.parent.deadline, t=self.parent.title)
            date = self.start_remind_from + self.interval * counter
            self.flags['interval'] = counter
            return Notification(mes, date)

    def check_weekdays(self, now):
        if self.weekdays is None:
            return None
        day = timedelta(days=1)
        date_now = now.date()
        while self.flags['weekdays'] < date_now:
            if self.weekdays.__contains__(date_now.weekday()):
                mes = 'Remind! {d} the deadline for the task {t} : weekdays'.format(d=self.parent.deadline, t=self.parent.title)
                date = datetime(date_now.year, date_now.month, date_now.day, now.hour, now.minute, now.second)
                self.flags['weekdays'] = date_now
                return  Notification(mes, date)
            date_now -= day









