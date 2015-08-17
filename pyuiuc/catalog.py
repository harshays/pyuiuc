from .url      import URL
from .tag      import Tag
from .schedule import Schedule
from .utils    import get_tag_type, InvalidParametersError

class CatalogURL(URL):
    endpoints = ['year', 'semester', 'subject', 'course']
    prefix    = 'http://courses.illinois.edu/cisapp/explorer/catalog'

    def setup(self):
        super(CatalogURL, self).setup()
        if 'section' in self.endpointsdict:
            raise InvalidParametersError("Invalid Catalog parameter - section")

class Catalog(Tag):
    url_cls = CatalogURL

    @classmethod
    def tagify(cls, elements):
        is_endpoint = lambda e: get_tag_type(e.tag) == 'endpoint'
        for idx, elem in enumerate(elements):
            if not is_endpoint(elem): continue
            url = elem.attrib['href']
            elem_cls = Schedule if '/schedule/' in url else cls
            elements[idx] = elem_cls.from_element(elem)
