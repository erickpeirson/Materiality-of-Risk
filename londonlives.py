import urllib2
from bs4 import BeautifulSoup
from unidecode import unidecode

from dataclasses import *

def parseItemPage(url):
    soup = _soupify(url)
    datatable = _get_datatable(soup)
    data = _enumerate_fields(datatable)

    entry = RegistryEntry(**_map_fields(data))
    return entry
# end parseItemPage

#### Helpers ####

def _get_datatable(html):
    """
    Extract the ``table`` node containing data.
    
    Parameters
    ----------
    html : :class:`bs4.BeautifulSoup`
    
    Returns
    -------
    table : :class:`bs4.element.Tag`
        Table containing data.
    """

    for table in html.find_all('table'):
        if table['class'][0] == 'jamietable':
            return table
    return None
# end _get_datatable

def _enumerate_fields(datatable):
    """
    Get data fields and values from the datatable.
    
    Parameters
    ----------
    table : :class:`bs4.element.Tag`
        Table containing data.    `
    
    Returns
    -------
    data : list
        A list of (field, value) tuples.
    """

    data = []
    for child in datatable.children:
        if child.name == 'tr':
            key = unidecode(child.th.contents[0])
            if key == 'Surname':    # Has weird js nonsense going on.
                value = child.find('span', class_='jamiePersName').text.strip()
            else:
                value = child.td.contents[0].strip()
            value = _tryInt(unidecode(value))
            
            data.append((key, value))

    return data
# end _enumerate_fields

def _tryInt(value):
    """
    Convert ``value`` string to an integer, if possible. Otherwise just return
    the value.
    
    Parameters
    ----------
    value : str
    
    Returns
    -------
    value : int or str
    """
    
    try:
        value = int(value)
    except:
        pass
    return value
# end _tryInt

def _soupify(url):
    """
    Get a :class:`bs4.BeautifulSoup` object from a remote resource.
    
    Parameters
    ----------
    url : str
    
    Returns
    -------
    soup : :class:`bs4.BeautifulSoup`
    """
    
    response = urllib2.urlopen(url).read()
    soup = BeautifulSoup(response)
    return soup
# end _soupify

def _map_fields(data):
    """
    Map data fields onto attributes of :class:`.RegistryEntry`\.
    
    Parameters
    ----------
    data : list
        A list of (key, value) tuples.
        
    Returns
    -------
    mapped_data : dict
        Keys correspond to :class:`.RegistryEntry` attributes.
    """

    fieldmappings = {
        'Unique Project ID':                    'u_project_id',
        'Register Date/ Company/ Reference':    'regdate_co_ref',
        'Policy Number':                        'policy_number',
        'Insured Value in PSs':                 'insured_value',
        'Forename':                             'forename',
        'Surname':                              'surname',
        'Occupation/Status':                    'occupation',
        'Joint Occupation':                     'joint_occupation',
        'Address':                              'address',
        'Address Type':                         'address_type',
        'Street Type':                          'street_type',
        'Place Name 1':                         'placename_1',
        'Place Name 2':                         'placename_2',
        'Place Type':                           'place_type',
        'Location Type':                        'location_type',
        'Location Name':                        'location_name'
        }

    mapped_data = {}
    for datum in data:
        mapped_data[fieldmappings[datum[0]]] = datum[1]

    return mapped_data
# end _map_fields
