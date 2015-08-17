import os
import re
from   copy       import deepcopy
from   pyuiuc.url import URL

url_re    = re.compile(r'{}.*'.format(URL.prefix))
endpoints = URL.endpoints

get_kv = lambda l: {k:k for k in l}

def generate_valid_params():
    for i in range(len(endpoints)):
        yield endpoints[:i+1]

def generate_invalid_params():
    for i in xrange(4):
        invalid = deepcopy(endpoints)
        del invalid[i]
        yield invalid

def get_xml_body(fname='./test.xml'):
    dpth = os.path.dirname(os.path.abspath(__file__))
    pth = os.path.join(dpth, fname)
    with open(pth, 'r') as f: content = f.read()
    return content
