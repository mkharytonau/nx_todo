from ..instances import base
from ..thirdparty.parse_datetime import parse_datetime
from ..reminding.reminder import Reminder


class Event(base.Base):
    def __init__(self, title, description, reminder, category, 
                 from_datetime, to_datetime, place, participants):
        super().__init__(title, description, reminder, category)
        self.from_datetime = from_datetime
        self.to_datetime = to_datetime
        self.place = place
        self.participants = participants

    @staticmethod
    def create_from_dict(dictionary, config):
        from_datetime_str = dictionary["from_datetime"].split()
        to_datetime_str = dictionary["to_datetime"].split()
        reminder = Reminder.create_from_dict(dictionary["reminder"], config)
        event = Event(
            dictionary["title"],
            dictionary["description"],
            reminder,
            dictionary["category"],
            parse_datetime(from_datetime_str, config['date_formats']['ordinary']),
            parse_datetime(to_datetime_str, config['date_formats']['ordinary']),
            dictionary["place"],
            dictionary["participants"]
        )
        return event

    def to_short(self):
        return self.title + '           ' + str(self.place)

    def to_full(self):
        return '{title}     {place}\n' \
               'Category: {category}\n' \
               'Participants: {participants}\n' \
               'From: {From}\n' \
               'To: {To}\n' \
               'Reminder: {reminder}\n' \
               'Description: {description}\n'.format(title=str(self.title), place=str(self.place),
                                                     category=str(self.category), participants=str(self.participants),
                                                     From=str(self.from_datetime), To=str(self.to_datetime),
                                                     reminder=str(self.reminder),
                                                     description=str(self.description))