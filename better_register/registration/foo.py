# coding: utf-8
from bs4 import  BeautifulSoup
from parsers import uoregon_course as uo
import  requests as r

def foo():
    page = r.get('http://classes.uoregon.edu/pls/prod/hwskdhnt.p_viewdetl?term=201402&crn=24638').text
    soup = BeautifulSoup(page)
    return uo.parse_primary_course(soup)
print foo()
