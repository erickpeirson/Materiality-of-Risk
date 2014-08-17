import persistent

class RegistryEntry(persistent.Persistent):
    id = None
    u_project_id = 0
    regdate_co_ref = ''
    policy_number = ''
    insured_value = 0
    forename = []
    surname = []
    occupation = []
    joint_occupation = ''
    address = []
    address_type = []
    street_type = []
    place_type = []
    place_name = []
    location_type = []
    location_name = []
    
    personObject = None
    occupationObject = None
    companyObject = None
    placeObject = None

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_person(self, object):
        if type(object) is Person:
            self.personObject = object
        else:
            raise ValueError('Object must be a Person')

    def set_occupation(self, object):
        if type(object) is Occupation:
            self.occupationObject = object
        else:
            raise ValueError('Object must be an Occupation')

    def set_company(self, object):
        if type(object) is Company:
            self.companyObject = object
        else:
            raise ValueError('Object must be a Company')

    def set_place(self, object):
        if type(object) is Place:
            self.placeObject = object
        else:
            raise ValueError('Object must be a Place')

class Person(persistent.Persistent):
    id = None
    forename = ''
    surname = ''
    
    occupation = None
    location = None

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_occupation(self, object):
        if type(object) is Occupation:
            self.occupation = object
        else:
            raise ValueError('Object must be an Occupation')

    def set_location(self, object):
        if type(object) is Place:
            self.location = object
        else:
            raise ValueError('Object must be a Place')

class Occupation(persistent.Persistent):
    id = None
    name = ''

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

class Company(persistent.Persistent):
    id = None
    name = ''

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)

class Place(persistent.Persistent):
    id = None
    placename_1 = ''
    placename_2 = ''
    type = ''
    
    latitude = None
    longitude = None
    precision = None

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)