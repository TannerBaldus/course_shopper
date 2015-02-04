__author__ = 'tanner'
from search_page_parser import parse_results
from subject_codes import parse_subject_table
from better_register.course_search.models import Subject
from ..common_ops import url_to_soup




course_search_url = ('http://classes.uoregon.edu/pls/prod/hwskdhnt.P_ListCrse?term_in={}&sel_subj=dummy&sel_day=dummy&'
                  'sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&'
                  'sel_ptrm=dummy&sel_attr=dummy&sel_cred=dummy&sel_tuition=dummy&sel_open=dummy&sel_weekend=dummy'
                  '&sel_title=&sel_to_cred=&sel_from_cred=&sel_subj={}&sel_crse=&sel_crn=&sel_camp=%25&sel_levl=%25'
                  '&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a&submit_btn=Show+Classes')

offering_page = 'http://classes.uoregon.edu/pls/prod/hwskdhnt.p_viewdetl?term={}&crn={}'

subject_code_page = 'http://registrar.uoregon.edu/current-students/subject-codes'


def convert_to_term_number(season, year):
    """
    In the uoregon search url the search term is the year and the term number.
    Here are some examples:

    Fall 2014         201401
    Winter 2015       201402
    Spring 2015       201403
    Summer 2015       201404
    Fall   2015       201501

    :param season:
    :param year:
    :return:
    """
    season = season.lower()
    seasons = ['not_valid', 'fall', 'winter', 'spring', 'summer']

    if season != 'fall':         ## All terms except fall use the previous year in its code
        year -= 1
    return str(year)+str(seasons.index(season.lower()))



def get_subject_codes():
    """

    :return:
    """
    soup = url_to_soup(subject_code_page)
    table = soup.find(id='DataTables_Table_0')
    return parse_subject_table(table)



def get_offerings(season, year):
    """

    :param season:
    :param year:
    :return:
    """
    term = convert_to_term_number(season, year)
    subject_codes = [s.code for s in Subject.objects.all()]
    term_search_url = lambda term, code: course_search_url.format(term, code)

    for code in subject_codes:
        results_soup = url_to_soup(term_search_url(term, code))
        for result in parse_results(results_soup):
            yield result









