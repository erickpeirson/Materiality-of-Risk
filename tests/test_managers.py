import unittest
import cPickle as pickle
import bs4

import sys
sys.path.append('/Users/erickpeirson/Visualizing-Risk')
import londonlives

item_url = 'http://www.londonlives.org/browse.jsp?div=fire_1775_1780_0_3'

class TestLondonLives(unittest.TestCase):
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
        table = londonlives._get_datatable(soup)
        data = londonlives._enumerate_fields(table)

        mapped_data = londonlives._map_fields(data)

        self.assertIsInstance(mapped_data, dict)
        self.assertGreater(len(mapped_data), 0)

    def test_parseItemPage(self):
        entry = londonlives.parseItemPage(item_url)

        print entry


if __name__ == '__main__':
    unittest.main()