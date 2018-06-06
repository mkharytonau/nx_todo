from datetime import datetime

from prettytable import PrettyTable

from .colorizer import colorize

SPECIAL_FIELDS = ['title', 'description', 'reminders', 'owners',
                  'participants', 'created_at', 'tasks', 'events']


def style_to_int(style):
    if style == 'DEFAULT':
        return 10
    if style == 'MSWORD_FRIENDLY':
        return 11
    if style == 'PLAIN_COLUMNS':
        return 12
    return 20


def select_priority_color(priority, config):
    if priority == '3':
        return int(config['priority_colors']['low'])
    if priority == '2':
        return int(config['priority_colors']['medium'])
    if priority == '1':
        return int(config['priority_colors']['high'])
    return 255


def split_str(s, length):
    if len(s) <= length:
        return s
    return s[:length] + '\n' + split_str(s[length:], length)


def handle_field(obj, field, config):
    if field == 'title':
        return colorize(obj.title,
                        foreground=select_priority_color(obj.priority, config))
    if field == 'description':
        value = split_str(obj.description, 10) if obj.description else None
        return value
    if field == 'reminders':
        return [reminder.id for reminder in obj.reminder_set.all()]
    if field == 'created_at':
        return datetime.strftime(obj.created_at, '%Y-%m-%d %H:%M:%S')
    if field == 'owners' or field == 'participants':
        return [user.name for user in obj.user_set.all()]
    if field == 'tasks':
        return [task.id for task in obj.tasks.all()]
    if field == 'events':
        return [event.id for event in obj.events.all()]


def configurate_table(table, config):
    table.set_style(style_to_int(config['table_styles']['style']))
    table.junction_char = config['table_styles']['junction_char']
    table.vertical_char = config['table_styles']['vertical_char']
    table.horizontal_char = config['table_styles']['horizontal_char']


def show_task_table(tasks, config):
    config_dict = config['tasks_view']
    fields_to_display = [field for field in config_dict.keys()
                         if config.getboolean('tasks_view', field)]
    table = PrettyTable()
    configurate_table(table, config)
    table.title = colorize('Tasks', background=config['colors']['task_bg'],
                           foreground=config['colors']['foreground'])
    table.field_names = fields_to_display
    for task in tasks:
        row = []
        for field in fields_to_display:
            if field in SPECIAL_FIELDS:
                row.append(handle_field(task, field, config))
            else:
                row.append(getattr(task, field))
        table.add_row(row)
    print(table)


def show_event_table(events, config):
    config_dict = config['events_view']
    fields_to_display = [field for field in config_dict.keys()
                         if config.getboolean('events_view', field)]
    table = PrettyTable()
    configurate_table(table, config)
    table.title = colorize('Events', background=config['colors']['event_bg'],
                           foreground=config['colors']['foreground'])
    table.field_names = fields_to_display
    for event in events:
        row = []
        for field in fields_to_display:
            if field in SPECIAL_FIELDS:
                row.append(handle_field(event, field, config))
            else:
                row.append(getattr(event, field))
        table.add_row(row)
    print(table)


def show_plan_table(plans, config):
    config_dict = config['plans_view']
    fields_to_display = [field for field in config_dict.keys()
                         if config.getboolean('plans_view', field)]
    table = PrettyTable()
    configurate_table(table, config)
    table.title = colorize('Plans',
                           background=config['colors']['plan_bg'],
                           foreground=config['colors']['foreground'])
    table.field_names = fields_to_display
    for plan in plans:
        row = []
        for field in fields_to_display:
            if field in SPECIAL_FIELDS:
                row.append(handle_field(plan, field, config))
            else:
                row.append(getattr(plan, field))
        table.add_row(row)
    print(table)


def show_notification_table(notifications, config):
    config_dict = config['notifications_view']
    fields_to_display = [field for field in config_dict.keys()
                         if config.getboolean('notifications_view', field)]
    table = PrettyTable()
    configurate_table(table, config)
    table.title = colorize('Notifications',
                           background=config['colors']['notification_bg'],
                           foreground=config['colors']['foreground'])
    table.field_names = fields_to_display
    for notification in notifications:
        row = []
        for field in fields_to_display:
            row.append(getattr(notification, field))
        table.add_row(row)
    print(table)


def show_reminder_table(reminders, config):
    config_dict = config['reminders_view']
    fields_to_display = [field for field in config_dict.keys()
                         if config.getboolean('reminders_view', field)]
    table = PrettyTable()
    configurate_table(table, config)
    table.title = colorize('Reminders',
                           background=config['colors']['reminder_bg'],
                           foreground=config['colors']['foreground'])
    table.field_names = fields_to_display
    for reminder in reminders:
        row = []
        for field in fields_to_display:
            if field in SPECIAL_FIELDS:
                row.append(handle_field(reminder, field, config))
            else:
                row.append(getattr(reminder, field))
        table.add_row(row)
    print(table)
