import unittest
import responses
import copy
import xml.etree.ElementTree as xml
from   pyuiuc.schedule       import Schedule
from   pyuiuc.catalog        import Catalog, CatalogURL
from   pyuiuc.utils          import InvalidParametersError
from   .                     import utils

class TestCatalog(unittest.TestCase):
    'tests Catalog class'
    def setUp(self):
        self.endpoints = copy.deepcopy(utils.endpoints)
        self.endpoints.pop()
        self.params    = utils.get_kv(self.endpoints)
        self.obj       = Catalog(**self.params)

    def test_init(self):
        self.assertIsInstance(self.obj, Catalog)
        self.assertIsInstance(self.obj.url, CatalogURL)

    def test_invalid_init(self):
        endpoints = utils.endpoints
        params    = utils.get_kv(endpoints)
        with self.assertRaises(InvalidParametersError):
            obj = Catalog(**params)

    @responses.activate
    def test_schedule_tagify(self):
        responses.add(responses.GET, utils.url_re,
                      body=utils.get_xml_body('./catalog.xml'),
                      status=200, content_type='text/xml')
        courses = self.obj.find('course')
        self.assertTrue(all(map(lambda c: isinstance(c, Schedule), courses)))
