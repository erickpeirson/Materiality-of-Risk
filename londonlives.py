import urllib2
from bs4 import BeautifulSoup
from unidecode import unidecode

from dataclasses import RegistryEntry

ll_ = 'http://www.londonlives.org/'

def parseItemPage(url):
    soup = _soupify(url)
    datatable = _get_datatable(soup)
    data = _enumerate_fields(datatable)

    entry = RegistryEntry(**_map_fields(data))
    return entry
# end parseItemPage

def listItemPages(url):
    """
    """
    soup = _soupify(url)
    table = _get_smalltable(soup)
    urls = _get_view_urls(table)

    return urls
# end listItemPages

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

def _get_smalltable(html):
    for table in html.find_all('table'):
        if table['class'][0] == 'smalltable':
            return table
    return None
# end _get_smalltable

def _get_view_urls(table):
    """
    extract URLs for registry pages.
    """
    urls = []
    for tr in table.children:
        for td in tr.children:
            if hasattr(td, 'a'):
                if td.a is not None:
                    urls.append(ll_ + td.a['href'])
    return urls
# end _get_view_urls

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
    import re

    fieldmappings = {
        'Unique Project ID':                    'u_project_id',
        'Register Date/ Company/ Reference':    'regdate_co_ref',
        'Policy Number':                        'policy_number',
        'Insured Value in PSs':                 'insured_value',
        'Forename\s*([0-9]*)':                  'forename',
        'Surname\s*([0-9]*)':                   'surname',
        'Occupation/Status\s*([A-Z]*)':         'occupation',
        'Joint Occupation':                     'joint_occupation',
        'Address\s*([0-9]*)':                   'address',
        'Address Type\s*([0-9]*)':              'address_type',
        'Street Type\s*([0-9]*)':               'street_type',
        'Place Name\s*([0-9]*)':                'place_name',
        'Place Type\s*([0-9]*)':                'place_type',
        'Location Type\s*([0-9]*)':             'location_type',
        'Location Name\s*([0-9]*)':             'location_name'
        }
    
    listfields = (  'address', 'address_type', 'placename', 'place_type',
                    'occupation', 'street_type', 'location_type',
                    'location_name', 'forename', 'surname'  )

    mapped_data = {}
    for datum in data:
        for pattern, field in fieldmappings.iteritems():
            match = re.search(pattern, datum[0])
            if match is not None:
                if field in listfields:
                    if field not in mapped_data:
                        mapped_data[field] = []                
                    mapped_data[field].append(datum[1])
                else:
                    mapped_data[field] = datum[1]

    return mapped_data
# end _map_fields
