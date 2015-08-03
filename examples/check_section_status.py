from pyuiuc.schedule import Schedule
from pprint import pprint

# example - get status of CS 233 sections

cs_233      = Schedule(year=2015, semester='fall', subject='CS', course=233)
cs_233_info = cs_233.get_info() # makes request for cs 233 xml 

cs_233_sections = cs_233.find(tag_name='section', tagify=True)

for section in cs_233_sections: 
    section_info = section.get_info() # makes request for cs 233 section xml
    print (section_info['sectionNumber'], section_info['enrollmentStatus'])
