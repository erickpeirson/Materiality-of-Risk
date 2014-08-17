import unittest
import cPickle as pickle
import bs4

import sys
sys.path.append('/Users/erickpeirson/Visualizing-Risk')
import londonlives

from dataclasses import RegistryEntry

#item_url = 'http://www.londonlives.org/browse.jsp?div=fire_1775_1780_0_3'
item_url = 'http://www.londonlives.org/browse.jsp?div=fire_1775_1780_524_52409'
index_url = 'http://www.londonlives.org/browse.jsp?div0Type=fireFile&decade=177'

class TestParseLondonLives(unittest.TestCase):
    """
    Extract data from a registry entry page.
    """
    def setUp(self):
        with open('./tests/testdata/register_item_page.pickle', 'r') as f:
            self.register_item_page = pickle.load(f)

    def test_get_datatable(self):
        soup = bs4.BeautifulSoup(self.register_item_page)
        datatable = londonlives._get_datatable(soup)

        self.assertIsInstance(datatable, bs4.element.Tag)
    
    def test_tryInt(self):
        self.assertIsInstance(londonlives._tryInt('1'), int)
        self.assertIsInstance(londonlives._tryInt('asdf'), str)

    def test_enumerate_fields(self):
        soup = bs4.BeautifulSoup(self.register_item_page)
        table = londonlives._get_datatable(soup)
        data = londonlives._enumerate_fields(table)

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data[0], tuple)

    def test_soupify(self):
        soup = londonlives._soupify(item_url)
        self.assertIsInstance(soup, bs4.BeautifulSoup)

    def test_map_fields(self):
        soup = bs4.BeautifulSoup(self.register_item_page)
#        soup = londonlives._soupify(item_url)
        table = londonlives._get_datatable(soup)
        data = londonlives._enumerate_fields(table)

        mapped_data = londonlives._map_fields(data)

        self.assertIsInstance(mapped_data, dict)
        self.assertGreater(len(mapped_data), 0)

    def test_parseItemPage(self):
        entry = londonlives.parseItemPage(item_url)

        self.assertIsInstance(entry, RegistryEntry)

class TestListLondonLives(unittest.TestCase):
    """
    Generate a list of registry entry pages.
    """

    def test_urls(self):
        soup = londonlives._soupify(index_url)
        table = londonlives._get_smalltable(soup)
        self.assertIsInstance(table, bs4.element.Tag)

        urls = londonlives._get_view_urls(table)
        self.assertIsInstance(urls, list)
        self.assertGreater(len(urls), 0)

        urls_ = londonlives.listItemPages(index_url)
        self.assertEqual(urls, urls_)

if __name__ == '__main__':
    unittest.main()