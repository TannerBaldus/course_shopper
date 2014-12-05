__author__ = 'tanner'
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('test_data/uoregon_class.html'))
tag = soup.find(class_="datadisplaytable").find('tr').find_all('td')
text = type(tag[0])
print text