from datetime import datetime
from parse_datetime import parse_datetime
import base


class Event(base.Base):
    def __init__(self, title, description, reminder, category, 
                 from_datetime, to_datetime, place, participants):
        super().__init__(title, description, reminder, category)
        self.from_datetime = from_datetime
        self.to_datetime = to_datetime
        self.place = place
        self.participants = participants

    @staticmethod
    def create_from_dict(dictionary):
        from_datetime_str = dictionary["from_datetime"].split()
        to_datetime_str = dictionary["to_datetime"].split()
        event = Event(
            dictionary["title"],
            dictionary["description"],
            dictionary["reminder"],
            dictionary["category"],
            parse_datetime(from_datetime_str, 'y/m/d h:m:s'),
            parse_datetime(to_datetime_str, 'y/m/d h:m:s'),
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
               'Description: {description}\n'.format(title=str(self.title), place=str(self.place), category=str(self.category),
                                                    participants=str(self.participants),
                                                    From=str(self.from_datetime), To=str(self.to_datetime),
                                                    reminder=str(self.reminder),
                                                    description=str(self.description))