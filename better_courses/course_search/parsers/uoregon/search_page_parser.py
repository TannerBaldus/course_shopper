from offering_page_parser import get_primary_offering, parse_associated_section
from better_register.course_search.models import Subject
__author__ = 'tanner'
import requests
from bs4 import BeautifulSoup



def parse_course_result(table_row,):
    table_data = table_row.find_all('td')
    if len(table_data) <= 8:  #if there are 8 entries the class was cancelled
        return
    class_type = table_data[0].p.text
    crn = table_data[1].a.text
    if '+' in class_type:
        return 'associated_section', crn
    return 'course',  crn


def get_details(result, detail_url):
    course_type, crn = result
    course_page = BeautifulSoup(requests.get(detail_url.format(crn)).text)
    if course_type == 'course':
        return dict(course=get_primary_offering(course_page))
    return dict(associated_section=parse_associated_section(course_page))


def parse_results(results_soup):
    result_table = results_soup.find(class_='datadisplaytable')
    for tr in result_table.find_all('tr'):
        result = parse_course_result(tr)
        if result:
            yield get_details(result)













