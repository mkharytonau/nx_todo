from django import template
from datetime import datetime

register = template.Library()

@register.inclusion_tag('nxtodoapp/notice_board.html')
def show_datetime():
    return {'time': str(datetime.now())}