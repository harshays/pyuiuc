"""
utils.py
This module contains helper functions for the package
"""
class InvalidParametersError(Exception):
    'Exception for invalid combination of parameters'
    pass

class UnknownTagError(Exception):
    'Exception for tags not in TagsContainer'
    pass

type_tag_map = {

    'parent' : [
        'calendarYears', 'terms', 'subjects', 'courses',
        'sections', 'meetings', 'instructors', 'parents'
    ],

    'endpoint' : [
        'calendarYear', 'term', 'subject', 'course', 'section'
    ],

    'info' : [
        'label','collegeCode','departmentCode','unitName',
        'contactName','contactTitle','statusCode','sectionNumber',
        'sectionNotes', 'partOfTerm','addressLine1','addressLine2',
        'phoneNumber','webSiteURL', 'description','endDate',
        'collegeDepartmentDescription','creditHours',' courseSectionInformation',
        'sectionStatusCode','startDate','enrollmentStatus', 'subjectComment'
    ]
}

tag_type_map = {tag : tagtype for tagtype, tags in
                type_tag_map.items() for tag in tags}

def get_tag_type(tag_name):
    if tag_name in tag_type_map:
        return tag_type_map[tag_name]
    raise UnknownTagError(tag_name)