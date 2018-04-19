import calendar
from calendar import Calendar
from colored import fg, attr, bg
from thirdparty.thirdparty import Colors


class nxCalendar(Calendar):
    def __init__(self, from_datetime):
        super().__init__()
        self.top_line = '    '
        self.weeks = []
        self.from_datetime = from_datetime
        self.linked_objects = []

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
        self.link_with_objects(next_weeks, next_year, next_month)
        self.weeks += next_weeks
        self.top_line += ('{month:^' + str(len(next_weeks) * 3) + '}').format(month=calendar.month_name[next_month])

    def show(self, month_num):
        self.append_month(self.from_datetime.year, self.from_datetime.month, True)
        if month_num > 1:
            for i in range(1, month_num):
                next_year = self.from_datetime.year + (self.from_datetime.month + i) // 12
                next_month = (self.from_datetime.month + i) % 12
                if next_month == 0:
                    next_month = 12
                    next_year -= 1
                self.append_month(next_year, next_month, False)
        print(self.top_line)
        for line in range(0, 7):
            print(calendar.day_name[line][:3], end=' ')
            for week in self.weeks:
                symbol = '{sym:2}'.format(sym='  ')
                if week[line][0] != 0:
                    if week[line][1] == 'null':
                        symbol = '{num:2}'.format(num=week[line][0])
                    else:
                        symbol = '{csbg}{csfg}{num:2}{ce}'.format(csbg=bg(week[line][1]), csfg=fg(Colors.foreground),
                                                              num=week[line][0], ce=attr('reset'))
                print(symbol, end=' ')
            print()

    def link_with_objects(self, weeks, year, month):
        if self.linked_objects is None:
            return
        for obj in self.linked_objects:
            if obj.year != year:
                continue
            if obj.month != month:
                continue
            for week in weeks:
                if (obj.day, 'null') in week:
                    week[week.index((obj.day, 'null'))] = (obj.day, obj.bgcolor)


class ColoredDate():
    def __init__(self, year, month, day, bgcolor):
        self.year = year
        self.month = month
        self.day = day
        self.bgcolor = bgcolor


