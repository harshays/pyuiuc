from .utils import InvalidParametersError
"""
url.py
This modules contains the base class URL to construct CISAPI URLs
"""

class URL(object):
    """
    Base helper class for constructing CISAPI URLs

    parameters
        - named endpoints parameters dict
            - year        year
            - semester    spring, summer or fall 
            - subject     subject abbr
            - course      course number
            - section     section CRN

    info
        - raises ValueError if combination of parameters is invalid
    """

    prefix    = 'http://courses.illinois.edu/cisapp/explorer'
    suffix    = 'xml'
    endpoints = ['year', 'semester', 'subject', 'course', 'section']

    def __init__(self, **params):
        self.endpointsdict = params
        self.setup()
        if not hasattr(self, 'url'):
            build = self.build()
            url_suffix = '/'+build if build else build
            self.url   = '{}{}.{}'.format(self.prefix, url_suffix, self.suffix)

    def setup(self):
        '''build url'''
        if 'url' in self.endpointsdict:
            url = self.endpointsdict['url']
            if not url.startswith(self.prefix):
                raise InvalidParametersError("Invalid URL {}".format(url))
            self.url = url
            return

        for k,v in self.endpointsdict.items():
            self.endpointsdict[k] = str(v)

    def build(self):
        'build endpoints url'
        endpoints = [self.endpointsdict.get(endpt, None)
                     for endpt in self.endpoints]
        mid_url   = []

        for idx, endpoint in enumerate(endpoints):
            if endpoint:
                mid_url.append(endpoint)
                continue
            if (any(endpoints[idx+1:])):
                raise ValueError("{} not provided".format(self.endpoints[idx]))

        return '/'.join(mid_url)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other.url