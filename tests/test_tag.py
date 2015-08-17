import unittest
import responses
import xml.etree.ElementTree   as     xml
from   pyuiuc.url              import URL
from   pyuiuc.tag              import Tag
from   pyuiuc.utils            import InvalidParametersError
from   .                       import utils

class TestTag(unittest.TestCase):
    'tests Tag class'

    def setUp(self):
        self.endpoints = utils.endpoints
        self.params    = utils.get_kv(self.endpoints)
        self.obj       = Tag(**self.params)

    def test_init(self):
        self.assertTrue(bool(self.obj))
        self.assertTrue(isinstance(self.obj.url, URL))

    def test_init_url(self):
        params = {'url':URL.prefix}

        obj          = Tag(**params)
        from_url_obj = Tag.from_url(params['url'])

        self.assertTrue(bool(obj))
        self.assertTrue(bool(from_url_obj))
        self.assertIsInstance(obj.url, URL)
        self.assertIsInstance(from_url_obj.url, URL)

    @responses.activate
    def test_from_element(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        obj    = Tag(**self.params)
        course = obj.find(tag_name='course', tagify=False)[0]

        course_obj = Tag.from_element(course)
        self.assertIsInstance(course_obj, Tag)

    @responses.activate
    def test_element(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        element = self.obj.element
        self.assertIsInstance(element, xml.Element)

    @responses.activate
    def test_make_request_invalid(self):
        responses.add(responses.GET, utils.url_re, body='invalid',
                      status=200, content_type='text/xml')

        with self.assertRaises(InvalidParametersError):
            self.obj.make_request()

    @responses.activate
    def test_get_info(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        info = self.obj.get_info()
        print ('info', info)
        self.assertTrue('description' in info)
        self.assertTrue('label' in info)
        self.assertEqual(len(info), 2)

    def test_eq(self):
        obj = Tag(**self.params)
        self.assertEqual(obj, self.obj)

    def test_str(self):
        self.assertEqual(str(self.obj), "Tag object of URL {}".format(self.obj.url))

    @responses.activate
    def test_new(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        obj  = Tag(**self.params)
        self.assertEqual(id(self.obj), id(obj))

        self.params['course'] = 'course_'
        obj2 = Tag(**self.params)

        self.assertFalse(id(obj2) == id(obj))

    @responses.activate
    def test_children(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        self.assertGreater(len(self.obj.get_children()), len(list(self.obj.element)))

    @responses.activate
    def test_attributes(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        attributes = self.obj.attributes
        self.assertTrue(attributes['name'] == self.obj['name'] == 'test')

    @responses.activate
    def test_grouped_children(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        group_ch = self.obj.get_grouped_children(group_by='type', tagify=False)
        self.assertTrue(list(group_ch.keys()), ['info', 'parent', 'endpoint'])
        self.assertTrue(all(map(lambda o: isinstance(o, xml.Element), sum(group_ch.values(), []))))

        group_ch_type_tagify = self.obj.get_grouped_children(group_by='type')
        group_ch_tag_tagify  = self.obj.get_grouped_children(group_by='tag')

        self.assertTrue(all(map(lambda o: isinstance(o, Tag), group_ch_type_tagify['endpoint'])))
        self.assertTrue(all(map(lambda o: isinstance(o, Tag), group_ch_tag_tagify['course'])))

    @responses.activate
    def test_find(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        with self.assertRaises(ValueError):
            obj = self.obj.find()

        by_name =      self.obj.find(tag_name='course')
        by_type =      self.obj.find(tag_type='endpoint')
        by_name_type = self.obj.find(tag_name='course', tag_type='endpoint')

        self.assertTrue(by_name == by_type == by_name_type)

    @responses.activate
    def test_find_by_attributes(self):
        responses.add(responses.GET, utils.url_re, body=utils.get_xml_body(),
                      status=200, content_type='text/xml')

        elem = self.obj.find_by_attributes(tag_name='course',
                                                   tagify=False, id='id1')

        self.assertEqual(elem.tag, 'course')
        self.assertEqual(elem.attrib['id'], 'id1')

        by_name_attr_none = self.obj.find_by_attributes(tag_name='course',
                                                        tagify=False, test='test')

        self.assertFalse(by_name_attr_none)
