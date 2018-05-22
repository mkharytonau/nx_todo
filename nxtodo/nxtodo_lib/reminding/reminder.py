from datetime import datetime
from datetime import timedelta
from ..thirdparty.functions import Parent
from ..thirdparty.enums import Instances
from .notification import Notification


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
                    'weekdays': self.start_remind_from.date() - timedelta(days=1),
                    'remind_in': False,
                    'right_now': False,
                    'missed': False
                }

    @staticmethod
    def create_from_dict(dictionary, config):
        start_remind_from = parse_datetime(dictionary['start_remind_from'].split(), config['date_formats']['ordinary']) \
            if dictionary['start_remind_from'] is not None else None
        datetimes = [parse_datetime(s.split(), config['date_formats']['ordinary']) for s in dictionary['datetimes']] \
            if dictionary['datetimes'] is not None else None
        stop_in_moment = parse_datetime(dictionary['stop_in_moment'].split(), config['date_formats']['ordinary']) \
            if dictionary['stop_in_moment'] is not None else None
        parent = Parent(dictionary['parent']['title'], dictionary['parent']['deadline'],
                        dictionary['parent']['to_datetime']) \
            if 'to_datetime' in dictionary['parent']  \
            else Parent(dictionary['parent']['title'], dictionary['parent']['deadline'])
        dictionary['flags']['weekdays'] = parse_datetime(dictionary['flags']['weekdays'], config['date_formats']['date'])
        reminder = Reminder(
            None,
            start_remind_from,
            stop_in_moment,
            parse_datetime(dictionary['remind_in'], config['date_formats']['delta']),
            datetimes,
            parse_datetime(dictionary['interval'], config['date_formats']['delta']),
            dictionary['weekdays'],
            parent,
            dictionary['kind'],
            dictionary['flags']
        )
        return reminder

    @staticmethod
    def parse_create(args, stop_in_moment, parent, kind):
        start_remind_before = parse_datetime(args.remind_before, config['date_formats']['delta'])
        remind_in = parse_datetime(args.remind_in, config['date_formats']['delta'])
        if (not start_remind_before is None or not remind_in is None) and stop_in_moment is None:
            print('You can not set -rb and -ri arguments, without -d(deadline)')
            raise ValueError
        start_remind_from = parse_datetime(args.remind_from, config['date_formats']['ordinary'])
        datetimes = parse_datetime(args.datetimes, config['date_formats']['ordinary_list'])
        interval = parse_datetime(args.interval, config['date_formats']['delta'])
        weekdays = parse_datetime(args.weekdays, config['date_formats']['weekdays'])
        reminder = Reminder(start_remind_before, start_remind_from, stop_in_moment, remind_in
                            , datetimes, interval, weekdays, parent, kind)
        return reminder

    def check(self, now): #Убрано поле stop in moment, поэтому нужно будет start_remind_before, start_remind_from посмотреть.
        if self.kind == Instances.task:
            if now > self.stop_in_moment:
                mes = 'You missed the deadline for the task {t}'.format(t=self.parent.title)
                date = self.parent.deadline
                self.flags['missed'] = True
                return Notification(mes, date)

        if self.kind == Instances.event:
            if now > self.stop_in_moment:
                if now < parse_datetime(self.parent.to_datetime.split(), config['date_formats']['ordinary']):
                    mes = 'Right now! there is an event {e}, it will last up to {to}'.\
                        format(e=self.parent.title, to=self.parent.to_datetime)
                    date = now
                    self.flags['right_now'] = True
                    return Notification(mes, date)
                mes = 'You missed the event {e}'.format(e=self.parent.title)
                date = self.parent.to_datetime
                self.flags['missed'] = True
                return Notification(mes, date)

        if self.start_remind_from < now < self.stop_in_moment:
            notify_remind_in = self.check_remind_in(now)
            notify_datetimes = self.check_datetimes(now)
            notify_interval = self.check_interval(now)
            notify_weekdays = self.check_weekdays(now)
            notifications = [notify for notify in [notify_remind_in, notify_datetimes,
                                                   notify_interval, notify_weekdays] if notify is not None]
            notifications.sort(key=lambda obj: obj.date, reverse=True)
            return notifications[0] if len(notifications) > 0 else None

    def check_remind_in(self, now):
        if self.remind_in is None:
            return None
        if self.stop_in_moment - self.remind_in < now:
            if self.kind == Instances.task:
                mes = 'Remind! In {time} the deadline for the task {t} : remind_in'\
                    .format(time=self.remind_in, t=self.parent.title)
            if self.kind == Instances.event:
                mes = 'Remind! In {time} the beginning of the event {t} : remind_in'\
                    .format(time=self.remind_in, t=self.parent.title)
            date = self.stop_in_moment - self.remind_in
            self.flags['remind_in'] = True
            return Notification(mes, date)

    def check_datetimes(self, now):
        if self.datetimes is None:
            return None
        counter = 0
        for dt in self.datetimes:
            if dt < now:
                counter += 1
        if counter > self.flags['datetimes']:
            if self.kind == Instances.task:
                mes = 'Remind! {d} the deadline for the task {t} : datetimes'.\
                    format(d=self.parent.deadline, t=self.parent.title)
            if self.kind == Instances.event:
                mes = 'Remind! {d} the beginning of the event {t} : datetimes'.\
                    format(d=self.stop_in_moment, t=self.parent.title)
            date = self.datetimes[counter - 1]
            self.flags['datetimes'] = counter
            return Notification(mes, date)

    def check_interval(self, now):
        if self.interval is None:
            return None
        counter = (now - self.start_remind_from) // self.interval
        if counter > self.flags['interval']:
            if self.kind == Instances.task:
                mes = 'Reminder! {d} the deadline for the task {t} : interval'.\
                    format(d=self.parent.deadline, t=self.parent.title)
            if self.kind == Instances.event:
                mes = 'Reminder! {d} the beginning of the event {t} : interval'.\
                    format(d=self.stop_in_moment, t=self.parent.title)
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
                if self.kind == Instances.task:
                    mes = 'Remind! {d} the deadline for the task {t} : weekdays'.\
                        format(d=self.parent.deadline, t=self.parent.title)
                if self.kind == Instances.event:
                    mes = 'Remind! {d} the beginning of the event {t} : weekdays'.\
                        format(d=self.stop_in_moment, t=self.parent.title)
                date = datetime(date_now.year, date_now.month, date_now.day, now.hour, now.minute, now.second)
                self.flags['weekdays'] = date_now
                return  Notification(mes, date)
            date_now -= day









