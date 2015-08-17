from .url import URL
from .tag import Tag

class ScheduleURL(URL):
    prefix = 'http://courses.illinois.edu/cisapp/explorer/schedule'

class Schedule(Tag):
    url_cls = ScheduleURL
