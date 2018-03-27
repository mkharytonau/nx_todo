import base


class Event(base.Base):
    def __init__(self, title, description, reminder, category, 
                 datefrom, timefrom, dateto, timeto, place, participants):
        super().__init__(title, description, reminder, category)
        self.datefrom = datefrom
        self.timefrom = timefrom
        self.dateto = dateto
        self.timeto = timeto
        self.place = place
        self.participants = participants

    @staticmethod
    def create_from_dict(dictionary):
        event = Event(
            dictionary["title"],
            dictionary["description"],
            dictionary["reminder"],
            dictionary["category"],
            dictionary["datefrom"],
            dictionary["timefrom"],
            dictionary["dateto"],
            dictionary["timeto"],
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
               'Description: {description}'.format(title=str(self.title), place=str(self.place), category=str(self.category),
                                                   participants=str(self.participants),
                                                   From=str(self.datefrom)+' '+str(self.timefrom),
                                                   To=str(self.timefrom) + ' ' + str(self.timeto), reminder=str(self.reminder),
                                                   description=str(self.description))