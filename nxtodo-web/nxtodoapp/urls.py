from django.conf.urls import (
    url,
    include
)
from . import views


tasks_actions = [
    url(r'^$', views.task_details, name='task_details'),
    url(r'^addsubtask/$', views.add_subtask, name='addsubtask'),
    #url(r'^removesubtask/(?P<s_id>\d+)$', views.remove_subtask, name='removesubtask')
]

tasks_urlpatterns = [
    url(r'^$', views.show_tasks, name='tasks'),
    url(r'add/$', views.add_task, name='task_add'),
    url(r'^(?P<id>\d+)/details/', include(tasks_actions)),
    url(r'^(?P<id>\d+)/edit/$', views.edit_task, name='task_edit'),
    url(r'^(?P<id>\d+)/remove/$', views.remove_task, name='task_remove'),
    url(r'^(?P<id>\d+)/complete/$', views.complete_task, name='task_complete')
]


urlpatterns = [
    url(r'^$', views.blank, name='blank'),
    url(r'^tasks/', include(tasks_urlpatterns)),
    url(r'^events$', views.show_events, name='events'),
    url(r'^plans$', views.show_plans, name='plans'),
    url(r'^reminders$', views.show_reminders, name='reminders'),

]