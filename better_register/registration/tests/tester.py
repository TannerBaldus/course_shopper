__author__ = 'tanner'
import re
import string
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('parser_tests/test_data/uoregon_class.html')).find(class_="datadisplaytable").find('tr').find('td')
print soup.text.split(' ')
