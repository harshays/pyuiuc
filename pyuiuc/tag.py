from   collections            import defaultdict
from   weakref                import WeakValueDictionary
from   .utils                 import InvalidParametersError, get_tag_type
from   .url                   import URL
import xml.etree.ElementTree  as     xml
import requests

"""
tags.py 
This module contains the base class for reading CISAPI XMLs
"""
class Tag(object):
    """
    Base class to read CISAPI XMLs 

    parameters
        - named endpoints parameters dict
            - year        year
            - semester    spring, summer or fall 
            - subject     subject abbr  (e.g. CS)
            - course      course number (e.g. 225)
            - section     section CRN   (e.g. 12345)
    """
    cache   = WeakValueDictionary()
    url_cls = URL

    def __new__(cls, **params):
        url_obj = cls.url_cls(**params)
        url     = url_obj.url
        if url in cls.cache and cls.cache[url]:
            return cls.cache[url]
        obj = object.__new__(cls)
        cls.cache[url] = obj 
        return obj

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    @classmethod
    def tagify(cls, elements):
        '''
        replaces endpoint xml.Element by its Tag object
        '''
        is_endpoint = lambda e: get_tag_type(e.tag) == 'endpoint'
        for idx, e in enumerate(elements):
            elements[idx] = cls.from_url(e.attrib['href']) if is_endpoint(e) else e

    def __init__(self, **params):
        self.url          = self.url_cls(**params)
        self.made_request = False

    @property
    def element(self):
        '''
        lazily makes request
        returns xml.Element object
        '''
        if not self.made_request: self.make_request()
        return self._element

    @property
    def attributes(self):
        if not self.made_request: self.make_request()
        return self._attributes

    def make_request(self):
        '''
        makes request to get xml content and creates XML.element object
        '''
        self._request = requests.get(self.url.url)
        self._text    = self._request.text
        try:
            self._element     = xml.fromstring(self._text)
            self._attributes  = self._element.attrib
            self.made_request = True
        except xml.ParseError:
            raise InvalidParametersError("One or more parameters are invalid")

    def get_info(self):
        '''
        returns a dictionary mapping tag names to tag cdata
        return only tags that are of type 'info' (see utils)
        '''
        return {ch.tag:ch.text for ch in self.element 
                if get_tag_type(ch.tag) == 'info'}

    def get_children(self, tagify=True):
        '''
        returns list of all xml.Element descendants

        optional keyword arguments
            - tagify      convert valid xml.Element objects to Tag objects
        '''
        ch = Tag._children(self.element, lst=[])
        if tagify: self.tagify(ch)
        return ch

    def get_grouped_children(self, group_by='type', tagify=True):
        '''
        returns a dictionary of xml.Element descendants

        optional keyword arguments
            - group_by    defaults to type
                - type    group by type of tag (info, parent or endpoint)
                - tag     group by name of tag 

            - tagify      convert valid xml.Element objects to Tag objects
        '''
        children = Tag._children(self.element, lst=[])
        d = defaultdict(list)

        if group_by == 'tag': group_fn = lambda tag: tag
        else: group_fn = get_tag_type

        for ch in children: d[group_fn(ch.tag)].append(ch)

        if tagify:
            for group, elems in d.items(): self.tagify(elems)

        return d

    def find(self, tag_name=None, tag_type=None, tagify=True):
        '''
        returns a list of descendants, optionally filtered by tag and tag type
        converts 'endpoint' xml elements to Tag objects

        optional keyword arguments 
            - tag_name   name of tag (e.g. course, sections)
            - tag_type   type of tag (info, parent, endpoint)
            - tagify     defaults to True

        exceptions
            - raises ValueError if no optional kwarg provided
        '''
        if not tag_name and not tag_type:
            raise ValueError('must provide tag or tag_type')

        if tag_type:
            all_dict = self.get_grouped_children(tagify=False)
            filtered = all_dict.get(tag_type, [])
            if tag_name:
                filtered = list(filter(lambda t:t.tag == tag_name, filtered))
        else:
            all_dict = self.get_grouped_children(group_by='tag', tagify=False)
            filtered = all_dict.get(tag_name, [])

        if tagify:
            self.tagify(filtered)

        return filtered

    # change to use from_element
    def find_by_attributes(self, tag_name=None, tagify=True, **attributes):
        '''
        returns the first descendants, that matches tag_name and attributes
        converts 'endpoint' xml elements to Tag objects

        optional keyword arguments
            - tag_name    name of tag
            - attributes  dict of attributes to filter by 
            - tagify      converts to Tag objects. defaults to True
        '''
        all_dict = self.get_grouped_children(group_by='tag', tagify=False)

        tag_filtered = all_dict.get(tag_name, []) if tag_name \
                       else sum(all_dict.values(), [])

        filtered = []

        for elem in tag_filtered:
            for attr, val in attributes.items():
                if elem.attrib.get(attr, None) == str(val):
                    filtered.append(elem)

        if tagify: 
            self.tagify(filtered)

        if filtered:
            return filtered[0]

        return

    @staticmethod
    def _children(element, lst=[]):
        '''
        get all children and subchildren of element 
        '''
        for ch in element:
            lst.append(ch)
            if list(ch):
                Tag._children(ch, lst)
        return lst

    def __str__(self):
        return "{} object of URL {}".format(type(self).__name__, self.url.url)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return False
        return self.url.__eq__(other.url)

    def __getitem__(self, key):
        return self.attributes.__getitem__(key)
