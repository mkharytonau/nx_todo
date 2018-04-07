import calendar
from calendar import Calendar
from colored import fg, attr, bg
from task import Task
from event import Event
from thirdparty import Colors


class nxCalendar(Calendar):
    def __init__(self, from_datetime):
        super().__init__()
        self.weeks = []
        self.from_datetime = from_datetime
        self.linked_tasks = None
        self.linked_events = None

    def append_month(self, next_year, next_month, isFirst):
        next_weeks = self.monthdayscalendar(next_year, next_month)
        if isFirst:
            pos = [next_weeks.index(week) for week in next_weeks if self.from_datetime.day in week][0]
            next_weeks = next_weeks[pos:]
            for day in next_weeks[0]:
                if day < self.from_datetime.day:
                    next_weeks[0][next_weeks[0].index(day)] = 0
        for week in next_weeks:
            for i in range(0, 7):
                week[i] = (week[i], 'null')
        self.link_with_objects('linked_tasks', next_weeks, next_year, next_month)
        self.link_with_objects('linked_events', next_weeks, next_year, next_month)
        self.weeks += next_weeks

    def show(self, month_num):
        self.append_month(self.from_datetime.year, self.from_datetime.month, True)
        if month_num > 1:
            for i in range(1, month_num):
                next_year = self.from_datetime.year + (self.from_datetime.month + i) // 12
                next_month = (self.from_datetime.month + i) % 12
                self.append_month(next_year, next_month, False)

        for line in range(0, 7):
            print(calendar.day_name[line][:3], end=' ')
            for week in self.weeks:
                if week[line][0] == 0:
                    symbol = ' '
                else:
                    if week[line][1] == 'null':
                        symbol = '{num}'.format(num=week[line][0])
                    if week[line][1] == 'task':
                        symbol = '{csbg}{csfg}{num}{ce}'.format(csbg=bg(Colors.taskbg), csfg=fg(Colors.foreground),
                                                                num=week[line][0], ce=attr('reset'))
                    if week[line][1] == 'event':
                        symbol = '{csbg}{csfg}{num}{ce}'.format(csbg=bg(Colors.eventbg), csfg=fg(Colors.foreground),
                                                                num=week[line][0], ce=attr('reset'))
                print(symbol, end=' ')
            print()

    def link_to(self, arr):
        if arr is None:
            return
        if isinstance(arr[0], Task):
            self.linked_tasks = arr
        if isinstance(arr[0], Event):
            self.linked_events = arr

    def link_with_objects(self, kind, weeks, year, month):
        arr = self.__getattribute__(kind)
        if arr is None:
            return
        for obj in arr:
            if kind == 'linked_tasks':
                if obj.deadline.year != year:
                    continue
                if obj.deadline.month != month:
                    continue
                for week in weeks:
                    if (obj.deadline.day, 'null') in week:
                        week[week.index((obj.deadline.day, 'null'))] = (obj.deadline.day, 'task')
            if kind == 'linked_events':
                if obj.from_datetime.year != year:
                    continue
                if obj.from_datetime.month != month:
                    continue
                for week in weeks:
                    if (obj.from_datetime.day, 'null') in week:
                        week[week.index((obj.from_datetime.day, 'null'))] = (obj.from_datetime.day, 'event')



