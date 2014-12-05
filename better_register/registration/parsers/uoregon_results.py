__author__ = 'tanner'
import requests
import  uoregon_course
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
        return dict(course=uoregon_course.parse_primary_course(course_page))
    return dict(associated_section=uoregon_course.parse_associated_section(course_page))


def parse_results(results_soup, get_details_fn, parse_result_fn):
    result_table = results_soup.find(class_='datadisplaytable')
    for tr in result_table.find_all('tr'):
        result = parse_result_fn(tr)
        if result:
            yield get_details_fn(result)








