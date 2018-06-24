from django.conf.urls import (
    url,
    include
)
from .views import (
    task,
    event,
    reminder,
    plan
)


tasks_actions = [
    url(r'^$', task.task_details, name='details'),
    url(r'^addsubtask/$', task.add_subtask, name='addsubtask'),
    url(r'^removesubtask/(?P<s_id>\d+)$', task.remove_subtask, name='removesubtask'),
    url(r'^addowner/$', task.add_owner, name='addowner'),
    url(r'^removeowner/(?P<o_id>\w+)$', task.remove_owner, name='removeowner'),
    url(r'^addreminder/$', task.add_reminder, name='addreminder'),
    url(r'^removereminder/(?P<r_id>\d+)$', task.remove_reminder, name='removereminder'),
]


events_actions = [
    url(r'^$', event.event_details, name='details'),
    url(r'^addparticipant/$', event.add_participant, name='addparticipant'),
    url(r'^removeparticipant/(?P<p_id>\w+)$', event.remove_participant, name='removeparticipant'),
    url(r'^addreminder/$', event.add_reminder, name='addreminder'),
    url(r'^removereminder/(?P<r_id>\d+)$', event.remove_reminder, name='removereminder'),
]


tasks_urlpatterns = ([
    url(r'^$', task.show_tasks, name='all'),
    url(r'^add/$', task.add_task, name='add'),
    url(r'^(?P<id>\d+)/details/', include(tasks_actions)),
    url(r'^(?P<id>\d+)/edit/$', task.edit_task, name='edit'),
    url(r'^(?P<id>\d+)/remove/$', task.remove_task, name='remove'),
    url(r'^(?P<id>\d+)/complete/$', task.complete_task, name='complete'),
    url(r'^filter/$', task.filter_tasks, name='filter')
], 'tasks')


events_urlpatterns = ([
    url(r'^$', event.show_events, name='all'),
    url(r'^add/$', event.add_event, name='add'),
    url(r'^(?P<id>\d+)/details/', include(events_actions)),
    url(r'^(?P<id>\d+)/edit/$', event.edit_event, name='edit'),
    url(r'^(?P<id>\d+)/remove/$', event.remove_event, name='remove'),
    url(r'^(?P<id>\d+)/complete/$', event.complete_event, name='complete'),
    url(r'^filter/$', event.filter_events, name='filter')
], 'events')


reminder_actions = [
    url(r'^$', reminder.reminder_details, name='details'),
    url(r'^adddatetime/$', reminder.add_datetime, name='adddatetime'),
    url(r'^removedatetime/(?P<dt>\w+)$', reminder.remove_datetime, name='removedatetime')
]


reminder_urlpatterns = ([
    url(r'^$', reminder.show_reminders, name='all'),
    url(r'^add/$', reminder.add_reminder, name='add'),
    url(r'^(?P<id>\d+)/details/', include(reminder_actions)),
    url(r'^(?P<id>\d+)/edit/$', reminder.edit_reminder, name='edit'),
    url(r'^(?P<id>\d+)/remove/$', reminder.remove_reminder, name='remove'),
    url(r'^filter/$', reminder.filter_reminders, name='filter')
], 'reminders')


plans_actions = [
    url(r'^$', plan.plan_details, name='details'),
    url(r'^addowner/$', plan.add_owner, name='addowner'),
    url(r'^removeowner/(?P<o_id>\w+)$', plan.remove_owner, name='removeowner'),

    url(r'^addreminder/$', plan.add_reminder, name='addreminder'),
    url(r'^removereminder/(?P<r_id>\d+)$', plan.remove_reminder, name='removereminder'),

    url(r'^addtask/$', plan.add_task, name='addtask'),
    url(r'^removetask/(?P<t_id>\d+)$', plan.remove_task, name='removetask'),

    url(r'^addevent/$', plan.add_event, name='addevent'),
    url(r'^removeevent/(?P<e_id>\d+)$', plan.remove_event, name='removeevent'),
]


plans_urlpatterns = ([
    url(r'^$', plan.show_plans, name='all'),
    url(r'^add/$', plan.add_plan, name='add'),
    url(r'^(?P<id>\d+)/details/', include(plans_actions)),
    url(r'^(?P<id>\d+)/edit/$', plan.edit_plan, name='edit'),
    url(r'^(?P<id>\d+)/remove/$', plan.remove_plan, name='remove'),
    url(r'^filter/$', plan.filter_plans, name='filter')
], 'plans')


urlpatterns = [
    url(r'^$', task.blank, name='blank'),
    url(r'^tasks/', include(tasks_urlpatterns)),
    url(r'^events/', include(events_urlpatterns)),
    url(r'^plans/', include(plans_urlpatterns)),
    url(r'^reminders/', include(reminder_urlpatterns)),

]