from .url import URL
from .tag import Tag

class ScheduleURL(URL):
    prefix = 'http://courses.illinois.edu/cisapp/explorer/schedule'

    def __str__(self):
        return self.url.split('/explorer')[-1]

class Schedule(Tag):
    url_cls = ScheduleURL
