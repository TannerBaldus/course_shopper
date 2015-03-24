__author__ = 'tanner'
from ..common_ops import url_to_soup
from offering_page_parser import get_primary_offering, parse_associated_section
import logging


def parse_course_result(table_row):

    table_data = table_row.find_all('td')
    class_type_row = table_data[0]
    crn = table_data[1].a.text
    if class_type_row.p and '+' in class_type_row.p.text:
        return 'associated_section', crn
    return 'offering',  crn


def get_details(result, detail_url):

    result_type, crn = result

    logging.info('Scraping data from crn: {}'.format(crn))
    course_page = url_to_soup(detail_url.format(crn))

    if result_type == 'offering':
        return dict(result_type='offering', data=get_primary_offering(course_page))
    return dict(result_type='associated_section', data=parse_associated_section(course_page))


def parse_results(results_url, detail_url):
    results_soup = url_to_soup(results_url)
    result_table = results_soup.find(class_='datadisplaytable')

    is_good_row = lambda row: len(row.find_all('td', class_='dddefault')) > 8
    for tr in result_table.find_all(is_good_row):
        print 'row'
        result = parse_course_result(tr)
        yield get_details(result, detail_url)
















