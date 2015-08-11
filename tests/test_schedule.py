import unittest
import responses
import xml.etree.ElementTree   as     xml
from   pyuiuc.url              import URL
from   pyuiuc.schedule         import Schedule, ScheduleURL
from   .                       import utils

class TestSchedule(unittest.TestCase):
    'tests Schedule class'
    def setUp(self):
        self.endpoints = utils.endpoints
        self.params    = utils.get_kv(self.endpoints)
        self.obj       = Schedule(**self.params)

    def test_init(self):
        self.assertIsInstance(self.obj, Schedule)
        self.assertIsInstance(self.obj.url, ScheduleURL)
