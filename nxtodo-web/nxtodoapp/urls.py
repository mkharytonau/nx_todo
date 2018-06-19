from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.redirect_to_tasks, name='to_tasks'),
    url(r'^tasks$', views.show_tasks, name='tasks'),
    url(r'^events$', views.show_events, name='events'),
    url(r'^plans$', views.show_plans, name='plans'),
    url(r'^reminders$', views.show_reminders, name='reminders'),
    url(r'^tasks/(?P<id>\d+)/details/$', views.task_details, name='task_details')
]