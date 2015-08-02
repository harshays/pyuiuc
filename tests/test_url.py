import unittest
from   pyuiuc.url   import URL
from   pyuiuc.utils import InvalidParametersError
from   .utils       import generate_valid_params, generate_invalid_params, get_kv

class TestURL(unittest.TestCase):
    '''
    tests the URL builder class
    '''
    def setUp(self):
        self.endpoints    = URL.endpoints
        self.prefix       = URL.prefix
        self.endpoints_kv = get_kv(self.endpoints)

    def test_init(self):
        url_obj = URL(**self.endpoints_kv)
        self.assertEqual(type(url_obj), URL)
        self.assertEqual(url_obj.endpointsdict, self.endpoints_kv)

    def test_setup(self):
        valid_url = {'url':self.prefix+'/test'}
        url_obj   = URL(**valid_url)

        self.assertEqual(valid_url['url'], url_obj.url)

    def test_setup_invalid(self):
        invalid_url = {'url':'url'}

        with self.assertRaises(InvalidParametersError):
            url_obj = URL(**invalid_url)

    def test_build(self):
        valid_params = generate_valid_params()

        for param in valid_params:
            comps = [self.prefix]
            comps.extend(param)
            topic = '/'.join(comps) + '.xml'
            kv = get_kv(param)
            obj = URL(**kv)
            self.assertEqual(topic, obj.url)

    def test_build_invalid(self):
        invalid_params = generate_invalid_params()

        for param in invalid_params:
            kv = get_kv(param)
            with self.assertRaises(ValueError):
                url_obj = URL(**kv)

    def test_str(self):
        durl = {'url':self.prefix+'/test'}
        obj  = URL(**durl)
        self.assertEqual(str(obj), durl['url'])

    def test_eq(self):
        self.assertEqual(URL(**self.endpoints_kv), URL(**self.endpoints_kv))