from pyuiuc.schedule import Schedule
from pprint import pprint

# example - get status of CS 233 and CS 225 sections

cs_courses = Schedule(year=2015, semester='fall', subject='CS')

cs_233 = cs_courses.find_by_attributes(tag_name='course',id=233)
cs_225 = cs_courses.find_by_attributes(tag_name='course',id=225)

for course_name, course in [('225', cs_225), ('233', cs_233)]:
    print (course_name+": \n")
    for section in course.find(tag_name='section'):
        info = section.get_info()

        print (info['sectionNumber'], section['id'], info['enrollmentStatus'])